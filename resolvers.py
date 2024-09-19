import json
from pathlib import Path
from typing import Tuple
from ariadne import (
    QueryType,
    make_executable_schema,
    fallback_resolvers,
    load_schema_from_path,
    MutationType,
)
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from graphql import GraphQLSchema

# Define path to JSON file
DATA_FILE = Path("schools.json")


# Load or initialize JSON data
def load_schools():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []


def save_schools(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# Helper function to resolve all schools with optional pagination and sorting
def resolve_schools(limit=None, offset=None, sortBy=None):
    schools = load_schools()

    # Sorting
    if sortBy:
        reverse = False
        if sortBy.startswith("-"):
            sortBy = sortBy[1:]
            reverse = True
        schools.sort(key=lambda x: x.get(sortBy, ""), reverse=reverse)

    # Pagination
    if offset is not None:
        schools = schools[offset:]
    if limit is not None:
        schools = schools[:limit]

    return schools


# Helper function to find a school by ID
def find_school_by_id(schools, school_id):
    for school in schools:
        if school["id"] == school_id:
            return school
    return None


# Helper function to filter schools by name
def filter_schools_by_name(name):
    schools = load_schools()
    filtered_schools = [
        school for school in schools if name.lower() in school["school_name"].lower()
    ]
    return filtered_schools


# Load GraphQL schema from file
type_defs = load_schema_from_path("schema.graphql")

# Query type
query = QueryType()


# Query resolver for getting all schools
@query.field("allSchools")
async def resolve_all_schools(_, info, limit=None, offset=None, sortBy=None):
    return resolve_schools(limit=limit, offset=offset, sortBy=sortBy)


# Query resolver for getting a specific school by ID
@query.field("getSchoolById")
def resolve_get_school(_, info, id):
    schools = load_schools()
    school = find_school_by_id(schools, id)
    if school:
        return school
    return None


@query.field("getSchoolsByName")
async def resolve_schools_by_name(_, info, name):
    schools = filter_schools_by_name(name)
    return schools


# Mutation type
mutation = MutationType()


# Mutation resolver for adding a new school
@mutation.field("addSchool")
def resolve_add_school(_, info, school_name, school_population, address, status):
    schools = load_schools()
    new_school = {
        "id": len(schools) + 1,
        "school_name": school_name,
        "school_population": school_population,
        "address": address,
        "status": status,
    }
    schools.append(new_school)
    save_schools(schools)
    return {"created": True, "school": new_school, "err": None}


# Mutation resolver for updating a school's details
@mutation.field("updateSchool")
def resolve_update_school(
    _, info, id, school_name=None, school_population=None, address=None, status=None
):
    schools = load_schools()
    school = find_school_by_id(schools, id)
    if not school:
        return {"updated": False, "err": "School not found"}

    if school_name is not None:
        school["school_name"] = school_name
    if school_population is not None:
        school["school_population"] = school_population
    if address is not None:
        school["address"] = address
    if status is not None:
        school["status"] = status

    save_schools(schools)
    return {"updated": True, "school": school, "err": None}


# Mutation resolver for deleting a school by ID
@mutation.field("deleteSchool")
def resolve_delete_school(_, info, id):
    # schools = load_schools()
    # school = find_school_by_id(schools, id)
    # if not school:
    #     return {"deleted": False, "err": "School not found"}

    # schools = [s for s in schools if s["id"] != id]
    # save_schools(schools)
    # return {"deleted": True, "school": school, "err": None}
    schools = load_schools()
    school = find_school_by_id(schools, id)

    if not school:
        return {"deactivated": False, "err": "School not found"}

    # Update the school's status to "INACTIVE"
    school["status"] = "INACTIVE"

    # Save the updated list of schools
    save_schools(schools)

    return {"deactivated": True, "school": school, "err": None}


# Custom name conversion function
def custom_convert_schema_name(
    graphql_name: str, schema: GraphQLSchema, path: Tuple[str, ...]
) -> str:
    converted_name = ""
    for i, c in enumerate(graphql_name.lower()):
        if i == 0:
            converted_name += c
            continue

        if c != graphql_name[i]:
            converted_name += "_"

        converted_name += c

    return converted_name


# Create executable GraphQL schema
schema = make_executable_schema(
    type_defs,
    [query, mutation],
    fallback_resolvers,
    # convert_names_case=custom_convert_schema_name,
)

# Create GraphQL App instance
graphql_app = GraphQL(
    schema,
    debug=True,
    websocket_handler=GraphQLTransportWSHandler(),
)
