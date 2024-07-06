""" Implement the User Management Endpoints """
import uuid

from tests import PASSWORD_USER
from tests import test_functions
from tests import assertStatus
from tests.client import Client


def test_get_users(client: Client):
    """
    Test to retrieve all users
    Sends a GET request to /users and checks that the response status is 200
    and the returned data is a list.
    """
    response = client.get("/users")
    assertStatus(response, 200)
    assert isinstance(
        response.json(), list
    ), f"Expected response to be a list but got {type(response.json())}"


def test_post_user(client: Client):
    """
    Test to create a new user
    Sends a POST request to /users with new user data and checks that the
    response status is 201 and the returned data matches the sent data.
    """
    unique_email = f"test.user.{uuid.uuid4()}@example.com"
    new_user = {
        "email": unique_email,
        "first_name": "John",
        "last_name": "Doe",
        "is_admin": False,
        "password": "test"
    }
    response = client.post("/users", new_user)
    assertStatus(response, 201)
    user_data = response.json()
    assert (
        user_data["email"] == new_user["email"]
    ), f"Expected email to be {new_user['email']} but got {user_data['email']}"
    assert (
        user_data["first_name"] == new_user["first_name"]
    ), f"Expected first name to be {new_user['first_name']} but got {user_data['first_name']}"
    assert (
        user_data["last_name"] == new_user["last_name"]
    ), f"Expected last name to be {new_user['last_name']} but got {user_data['last_name']}"
    assert (
        user_data["is_admin"] == new_user["is_admin"]
    ), f"Expected is_admin to be {new_user['is_admin']} but got {user_data['is_admin']}"
    assert "id" in user_data, "User ID not in response"
    assert "created_at" in user_data, "Created_at not in response"
    assert "updated_at" in user_data, "Updated_at not in response"
    return user_data["id"]  # Return the ID of the created user for further tests


def test_get_user(client: Client):
    """
    Test to retrieve a specific user by ID
    Creates a new user, then sends a GET request to /users/{id} and checks that the
    response status is 200 and the returned data matches the created user's data.
    """
    user = client.factory.create_unique_user()

    # Retrieve the newly created user
    response = client.get(f"/users/{user['id']}")
    assertStatus(response, 200)
    user_data = response.json()
    assert (
        user_data["id"] == user["id"]
    ), f"Expected user ID to be {user['id']} but got {user_data['id']}"
    assert "email" in user_data, "Email not in response"
    assert "first_name" in user_data, "First name not in response"
    assert "last_name" in user_data, "Last name not in response"
    assert "created_at" in user_data, "Created_at not in response"
    assert "updated_at" in user_data, "Updated_at not in response"


def test_put_user(client: Client):
    """
    Test to update an existing user
    Creates a new user, then sends a PUT request to /users/{id} with updated user data
    and checks that the response status is 200 and the returned data matches the updated data.
    """
    user = client.factory.create_unique_user()

    # Update the newly created user
    updated_user = {
        "email": f"updated.user.{uuid.uuid4()}@example.com",
        "first_name": "John",
        "last_name": "Smith"
    }

    # no login -> 401
    response = client.put(f"/users/{user['id']}", updated_user)
    assertStatus(response, 401)

    # not owner -> 403
    response = client.put(f"/users/{user['id']}", updated_user, client.user.access_token)
    assertStatus(response, 403)

    # login -> 200
    access_token = client.login(user)
    response = client.put(f"/users/{user['id']}", updated_user, access_token)
    assertStatus(response, 200)

    user_data = response.json()
    assert (
        user_data["email"] == updated_user["email"]
    ), f"Expected updated email to be {updated_user['email']} but got {user_data['email']}"
    assert (
        user_data["first_name"] == updated_user["first_name"]
    ), f"Expected updated first name to be {updated_user['first_name']} but got {user_data['first_name']}"
    assert (
        user_data["last_name"] == updated_user["last_name"]
    ), f"Expected updated last name to be {updated_user['last_name']} but got {user_data['last_name']}"
    assert "id" in user_data, "User ID not in response"
    assert "created_at" in user_data, "Created_at not in response"
    assert "updated_at" in user_data, "Updated_at not in response"

    # admin -> 200
    updated_user['first_name'] = "John Updated"
    response = client.put(f"/users/{user['id']}", updated_user, client.superuser.access_token)
    assertStatus(response, 200)

    user_data = response.json()
    assert (
        user_data["first_name"] == updated_user["first_name"]
    ), f"Expected updated first name to be {updated_user['first_name']} but got {user_data['first_name']}"



def test_delete_user(client: Client):
    """
    Test to delete an existing user
    Creates a new user, then sends a DELETE request to /users/{id} and checks that the
    response status is 204 indicating successful deletion.
    """
    user = client.factory.create_unique_user()

    # no login -> 401
    response = client.delete(f"/users/{user['id']}")
    assertStatus(response, 401)

    # no owner -> 403
    response = client.delete(f"/users/{user['id']}", client.user.access_token)
    assertStatus(response, 403)

    # login -> 204
    access_token = client.login(user)
    response = client.delete(f"/users/{user['id']}", access_token)
    assertStatus(response, 204)

    # admin -> 204
    user = client.factory.create_unique_user()
    response = client.delete(f"/users/{user['id']}", client.superuser.access_token)
    assertStatus(response, 204)



def test_login_user(client: Client):
    """
    Test to login an existing user
    Creates a new user, then sends a POST request to /login and checks that the
    response status is 201 indicating successful login.
    """
    user = client.factory.create_unique_user()

    response = client.post("/login", {
        "email": user['email'],
        "password": "wrong"
    })
    assertStatus(response, 401)

    response = client.post("/login", {
        "email": user['email'],
        "password": PASSWORD_USER
    })
    assertStatus(response, 201)


def test_login_user_protected_page(client: Client):
    """
    Test access token on protected page
    """
    user = client.factory.create_unique_user()
    access_token = client.login(user)

    # Without token
    response = client.get("/protected")
    assertStatus(response, 401)

    # Good token
    response = client.get("/protected", access_token)
    data = response.json()
    assertStatus(response, 200)
    assert user["id"] == data['logged_in_as'], "Logged with wrong user"


def test_login_user_restricted_page(client: Client):
    """
    Test access token on restricted page, ADMIN
    """
    user_no = client.factory.create_unique_user(False)
    access_token_no = client.login(user_no)

    # Without Admin permission
    response = client.get("/restricted", access_token_no)
    assertStatus(response, 403)

    user_admin = client.factory.create_unique_user(True)
    access_token_admin = client.login(user_admin)

    # With Admin permission
    response = client.get("/restricted", access_token_admin)
    assertStatus(response, 200)

    data = response.json()
    assert user_admin['id'] == data['logged_in_as'], "Logged with wrong user"
    assert data['is_admin'], "Not admin!"


if __name__ == "__main__":
    # Run the tests
    test_functions(
        [
            test_get_users,
            test_post_user,
            test_get_user,
            test_put_user,
            test_delete_user,
            test_login_user,
            test_login_user_protected_page,
            test_login_user_restricted_page
        ]
    )
