""" Implement the Amenity Management Endpoints """
import uuid

from tests import test_functions
from tests import assertStatus
from tests.client import Client


def test_get_amenities(client: Client):
    """
    Test to retrieve all amenities
    Sends a GET request to /amenities and checks that the response status is 200
    and the returned data is a list.
    """
    response = client.get("/amenities")
    assertStatus(response, 200)
    assert isinstance(
        response.json(), list
    ), f"Expected response to be a list but got {type(response.json())}"


def test_post_amenity(client: Client):
    """
    Test to create a new amenity
    Sends a POST request to /amenities with new amenity data and checks that the
    response status is 201 and the returned data matches the sent data.
    """
    unique_amenity_name = f"Test Amenity {uuid.uuid4()}"
    new_amenity = {"name": unique_amenity_name}

    # no login -> 401
    response = client.post("/amenities", new_amenity)
    assertStatus(response, 401)
    
    # no admin -> 403
    response = client.post("/amenities", new_amenity, client.user.access_token)
    assertStatus(response, 403)

    # admin -> 201
    response = client.post("/amenities", new_amenity, client.superuser.access_token)
    assertStatus(response, 201)

    amenity_data = response.json()
    assert (
        amenity_data["name"] == new_amenity["name"]
    ), f"Expected name to be {new_amenity['name']} but got {amenity_data['name']}"
    assert "id" in amenity_data, "Amenity ID not in response"
    assert "created_at" in amenity_data, "Created_at not in response"
    assert "updated_at" in amenity_data, "Updated_at not in response"
    return amenity_data["id"]  # Return the ID of the created amenity for further tests


def test_get_amenity(client: Client):
    """
    Test to retrieve a specific amenity by ID
    Creates a new amenity, then sends a GET request to /amenities/{id} and checks that the
    response status is 200 and the returned data matches the created amenity's data.
    """
    amenity_id = client.factory.create_unique_amenity()

    # Retrieve the newly created amenity
    response = client.get(f"/amenities/{amenity_id}")
    assertStatus(response, 200)
    amenity_data = response.json()
    assert (
        amenity_data["id"] == amenity_id
    ), f"Expected amenity ID to be {amenity_id} but got {amenity_data['id']}"
    assert "name" in amenity_data, "Name not in response"
    assert "created_at" in amenity_data, "Created_at not in response"
    assert "updated_at" in amenity_data, "Updated_at not in response"


def test_put_amenity(client: Client):
    """
    Test to update an existing amenity
    Creates a new amenity, then sends a PUT request to /amenities/{id} with updated amenity data
    and checks that the response status is 200 and the returned data matches the updated data.
    """
    amenity_id = client.factory.create_unique_amenity()

    # Update the newly created amenity
    updated_amenity = {"name": f"Updated Amenity {uuid.uuid4()}"}

    # no login -> 401
    response = client.put(f"/amenities/{amenity_id}", updated_amenity)
    assertStatus(response, 401)
    
    # no admin -> 403
    response = client.put(f"/amenities/{amenity_id}", updated_amenity, client.user.access_token)
    assertStatus(response, 403)

    # admin -> 200
    response = client.put(f"/amenities/{amenity_id}", updated_amenity, client.superuser.access_token)
    assertStatus(response, 200)

    amenity_data = response.json()
    assert (
        amenity_data["name"] == updated_amenity["name"]
    ), f"Expected updated name to be {updated_amenity['name']} but got {amenity_data['name']}"
    assert "id" in amenity_data, "Amenity ID not in response"
    assert "created_at" in amenity_data, "Created_at not in response"
    assert "updated_at" in amenity_data, "Updated_at not in response"


def test_delete_amenity(client: Client):
    """
    Test to delete an existing amenity
    Creates a new amenity, then sends a DELETE request to /amenities/{id} and checks that the
    response status is 204 indicating successful deletion.
    """
    amenity_id = client.factory.create_unique_amenity()

    # no login -> 401
    response = client.delete(f"/amenities/{amenity_id}")
    assertStatus(response, 401)
    
    # no admin -> 403
    response = client.delete(f"/amenities/{amenity_id}", client.user.access_token)
    assertStatus(response, 403)

    # admin -> 204
    response = client.delete(f"/amenities/{amenity_id}", client.superuser.access_token)
    assertStatus(response, 204)


if __name__ == "__main__":
    # Run the tests
    test_functions(
        [
            test_get_amenities,
            test_post_amenity,
            test_get_amenity,
            test_put_amenity,
            test_delete_amenity,
        ]
    )
