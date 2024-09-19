import asyncio
from time import sleep
from faker import Faker

from endpoint import (
    add_school,
    close_client,
    delete_school,
    fetch_all_schools,
    get_school_by_id,
    get_schools_by_name,
    update_school,
)

# Initialize Faker
fake = Faker()


# Fetch the latest school ID
async def fetch_latest_school():
    schools = await fetch_all_schools()
    if schools and schools.get("data"):
        school_list = schools.get("data").get("allSchools", [])
        if school_list:
            return school_list[-1].get("id")
    return None


# Example to fetch all schools
async def fetch_schools_example():
    schools = await fetch_all_schools()
    if schools and schools.get("status_code") == 200:
        print("Fetch all schools:", len(schools.get("data", {}).get("allSchools", [])))
    else:
        print("Failed to fetch all schools")


# Example to add a new school with an address using Faker
async def add_school_example():
    school_name = fake.company()  # Generates a fake school name
    school_population = fake.random_int(min=100, max=2000)  # Random population
    address = {
        "street": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "postal_code": fake.postcode(),
    }
    result = await add_school(school_name, school_population, address)
    if result and result.get("status_code") == 200:
        print(f"Add school: Success - {school_name}")
    else:
        print("Failed to add school")


# Example to fetch a school by ID
async def fetch_school_by_id_example():
    school_id = await fetch_latest_school()
    if school_id:
        result = await get_school_by_id(school_id)
        if result and result.get("status_code") == 200:
            print(f"Fetch school by ID {school_id}: Success")
        else:
            print(f"Failed to fetch school by ID {school_id}")
    else:
        print("No school ID found to fetch")


# Example to update an existing school using Faker
async def update_school_example():
    school_id = await fetch_latest_school()
    if school_id:
        school_name = fake.company()  # Generates a fake updated school name
        school_population = fake.random_int(min=500, max=3000)  # Random new population
        address = {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "postal_code": fake.postcode(),
        }
        result = await update_school(school_id, school_name, school_population, address)
        if result and result.get("status_code") == 200:
            print(f"Update school: Success - {school_name}")
        else:
            print(f"Failed to update school with ID {school_id}")
    else:
        print("No school ID found to update")


# Example to delete a school by ID
async def delete_school_example():
    school_id = await fetch_latest_school()
    print(f"Deleting school with ID {school_id}")
    if school_id:
        result = await delete_school(school_id)
        if result and result.get("status_code") == 200:
            print(f"Delete school: Success - School ID {school_id}")
        else:
            print(f"Failed to delete school with ID {school_id}")
    else:
        print("No school ID found to delete")


# Example to fetch schools by name
async def fetch_schools_by_name_example():
    name = "Codavatar"
    result = await get_schools_by_name(name)
    if result and result.get("status_code") == 200:
        print(
            f"Fetch schools by name: {len(result.get('data', {}).get('getSchoolsByName', []))}"
        )
    else:
        print(f"Failed to fetch schools by name {name}")


# Test the endpoints
async def test_endpoint():
    # await asyncio.gather(
    #     add_school_example(),
    #     update_school_example(),
    #     delete_school_example(),
    #     fetch_school_by_id_example(),
    #     fetch_schools_by_name_example(),
    #     fetch_schools_example(),
    # )
    await add_school_example()
    await update_school_example()
    await delete_school_example()
    await fetch_school_by_id_example()
    await fetch_schools_by_name_example()
    await fetch_schools_example()
    await close_client()


# Run the test
if __name__ == "__main__":
    asyncio.run(test_endpoint())
