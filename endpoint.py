import httpx
from typing import Optional, Dict, Any

# GraphQL endpoint URL
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql/"
TIMEOUT = 10  # Set a reasonable timeout for all requests

# Shared async client for connection pooling
client = httpx.AsyncClient(timeout=TIMEOUT)


# Handle errors and return responses in a consistent manner
async def _post_graphql(
    query: str, variables: Optional[dict] = None
) -> Optional[Dict[str, Any]]:
    try:
        response = await client.post(
            GRAPHQL_ENDPOINT, json={"query": query, "variables": variables}
        )
        response.raise_for_status()
        data = response.json()

        # Ensure error handling from GraphQL response
        if "errors" in data:
            raise ValueError(f"GraphQL errors: {data['errors']}")

        return {"status_code": response.status_code, **data}
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"GraphQL error: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    return None


# Fetch all schools
async def fetch_all_schools(limit=10, offset=0, sortBy="school_name"):
    query = """
    query ($limit: Int, $offset: Int, $sortBy: String) {
      allSchools(limit: $limit, offset: $offset, sortBy: $sortBy) {
        id
        school_name
        school_population
        status
        address {
          street
          city
          state
          postal_code
        }
      }
    }
    """
    variables = {
        "limit": limit,
        "offset": offset,
        "sortBy": sortBy,
    }
    return await _post_graphql(query, variables)


# Add a new school with an address
async def add_school(
    school_name: str, school_population: int, address: Dict[str, str], status="ACTIVE"
):
    mutation = """
    mutation ($school_name: String!, $school_population: Int!, $address: AddressInput!, $status: SchoolStatus!) {
      addSchool(school_name: $school_name, school_population: $school_population, address: $address, status: $status) {
        created
        school {
          id
          school_name
          school_population
          status
          address {
            street
            city
            state
            postal_code
          }
        }
        err
      }
    }
    """
    variables = {
        "school_name": school_name,
        "school_population": school_population,
        "address": address,
        "status": status,
    }
    return await _post_graphql(mutation, variables)


# Fetch a school by ID
async def get_school_by_id(school_id: int):
    query = """
    query GetSchoolById($id: Int!) {
      getSchoolById(id: $id) {
        id
        school_name
        school_population
        status
        address {
          street
          city
          state
          postal_code
        }
      }
    }
    """
    variables = {"id": school_id}
    return await _post_graphql(query, variables)


# Update an existing school
async def update_school(
    school_id: int,
    school_name: Optional[str] = None,
    school_population: Optional[int] = None,
    address: Optional[Dict[str, str]] = None,
    status: Optional[str] = None,
):
    mutation = """
    mutation ($id: Int!, $school_name: String, $school_population: Int, $address: AddressInput, $status: SchoolStatus) {
      updateSchool(id: $id, school_name: $school_name, school_population: $school_population, address: $address, status: $status) {
        updated
        school {
          id
          school_name
          school_population
          status
          address {
            street
            city
            state
            postal_code
          }
        }
        err
      }
    }
    """
    variables = {
        "id": school_id,
        "school_name": school_name,
        "school_population": school_population,
        "address": address,
        "status": status,
    }
    return await _post_graphql(mutation, variables)


# Fetch a school by name
async def get_schools_by_name(name: str):
    query = """
    query ($name: String!) {
      getSchoolsByName(name: $name) {
        id
        school_name
        school_population
        status
        address {
          street
          city
          state
          postal_code
        }
      }
    }
    """
    variables = {"name": name}
    return await _post_graphql(query, variables)


# Delete a school by ID
async def delete_school(school_id: int):
    mutation = """
    mutation ($id: Int!) {
      deleteSchool(id: $id) {
        deleted
        school {
          id
          school_name
          status
        }
        err
      }
    }
    """
    variables = {"id": school_id}
    return await _post_graphql(mutation, variables)


# Remember to close the client when done to release resources
async def close_client():
    await client.aclose()
