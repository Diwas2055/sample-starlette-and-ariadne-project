# School Management GraphQL API With Starlette and Ariadne

## Overview

The School Management GraphQL API provides a robust interface for managing school data. It supports various operations such as adding, updating, querying, and soft-deleting schools. This API uses GraphQL to offer flexible and efficient querying capabilities.

## Features

- **Query Schools**: Retrieve a list of schools with optional pagination, sorting, and filtering by status.
- **Get School by ID**: Fetch detailed information about a specific school using its ID.
- **Add School**: Add a new school with details including its name, population, address, and status.
- **Update School**: Modify the details of an existing school.
- **Soft Delete School**: Mark a school as inactive instead of permanently deleting it.

## GraphQL Schema

### Types

- **School**
  ```graphql
    type School {
      id: Int!
      school_name: String!
      school_population: Int!
      address: Address
      status: SchoolStatus!
    }

- **Address**
  ```graphql
    type Address {
      street: String!
      city: String!
      state: String!
      postal_code: String!
    }
  ```
- **SchoolStatus**
  ```graphql
    enum SchoolStatus {
      ACTIVE
      INACTIVE
      BANNED
    }
  ```

### Queries

- `getSchoolById(id: Int!): School` Retrieves a school by its ID.
- `getSchoolsByName(name: String!): [School!]!` Fetches schools filtered by their name.
- `allSchools(limit: Int, offset: Int, sortBy: String, status: SchoolStatus): [School!]!` Retrieves a list of schools with optional pagination, sorting, and status filtering.

### Mutations

- `addSchool(school_name: String!, school_population: Int!, address: AddressInput!, status: SchoolStatus!): SchoolResponse!` Adds a new school to the system.
- `updateSchool(id: Int!, school_name: String, school_population: Int, address: AddressInput): SchoolResponse!` Updates details of an existing school.
- `deleteSchool(id: Int!): SchoolResponse!` Soft-deletes a school by setting its status to INACTIVE.

### Input Types

- **AddressInput**
  ```graphql
    input AddressInput {
      street: String!
      city: String!
      state: String!
      postal_code: String!
    }
  ```
### Response Types

- **SchoolResponse**
  ```graphql
    type SchoolResponse {
      success: Boolean!
      message: String!
      school: School
    }
  ```
### Endpoints

- **GraphQL API**: `http://localhost:8000/graphql/`

### Setup Instructions

1. **Install the required Python packages using pip:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Server:**
    ```bash
    uvicorn main:app --reload
    ```

3. **Run the Tests:**

    ```bash
    python test_endpoints.py
    ```


### Testing

> The project includes asynchronous tests for the following functionalities:

- **Adding a new school**
- **Fetching all schools**
- **Fetching a school by ID**
- **Updating an existing school**
- **Soft-deleting a school**
- **Fetching schools by name**

### Notes

- Ensure the `schools.json` file exists for data persistence.
- The API uses `httpx` for making asynchronous GraphQL requests.
- Schools are soft-deleted by setting their status to `INACTIVE` rather than removing them from the database.


# Test the GraphQL API
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"query": "{ all_schools { id school_name school_population address { street city state postal_code } } }"}' http://localhost:8000/graphql/
```
