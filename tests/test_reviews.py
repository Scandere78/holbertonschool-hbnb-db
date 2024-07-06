""" Implement the Review Management Endpoints """
from tests import test_functions
from tests import assertStatus
from tests.client import Client


def test_get_reviews_from_place(client: Client):
    """
    Test to retrieve all reviews from a place
    Sends a GET request to /places/{place_id}/reviews and checks that the response status is 200
    and the returned data is a list.
    """
    place_id = client.factory.create_place()
    user = client.factory.create_unique_user()
    new_review = {
        "place_id": place_id,
        "user_id": user['id'],
        "comment": "Great place to stay!",
        "rating": 5.0,
    }
    response = client.post(f"/places/{place_id}/reviews", new_review, client.superuser.access_token)
    assertStatus(response, 201)

    review_id = response.json()["id"]

    response = client.get(f"/places/{place_id}/reviews")
    assertStatus(response, 200)
    assert isinstance(
        response.json(), list
    ), f"Expected response to be a list but got {type(response.json())}"

    assert any(
        review["id"] == review_id for review in response.json()
    ), f"Expected review with ID {review_id} to be in response but it wasn't"


def test_get_reviews_from_user(client: Client):
    """
    Test to retrieve all reviews from a user
    Sends a GET request to /users/{user_id}/reviews and checks that the response status is 200
    and the returned data is a list.
    """
    place_id = client.factory.create_place()
    user = client.factory.create_unique_user()
    new_review = {
        "place_id": place_id,
        "user_id": user['id'],
        "comment": "Great place to stay!",
        "rating": 5.0,
    }
    response = client.post(f"/places/{place_id}/reviews", new_review, client.superuser.access_token)
    assertStatus(response, 201)

    review_id = response.json()["id"]

    response = client.get(f"/users/{user['id']}/reviews")
    assertStatus(response, 200)
    assert isinstance(
        response.json(), list
    ), f"Expected response to be a list but got {type(response.json())}"

    assert any(
        review["id"] == review_id for review in response.json()
    ), f"Expected review with ID {review_id} to be in response but it wasn't"


def test_post_review(client: Client):
    """
    Test to create a new review
    Sends a POST request to /reviews with new review data and checks that the
    response status is 201 and the returned data matches the sent data.
    """
    place_id = client.factory.create_place()
    user = client.factory.create_unique_user()
    new_review = {
        "user_id": user['id'],
        "comment": "This place is amazing!",
        "rating": 4.5,
    }

    # no login -> 401
    response = client.post(f"/places/{place_id}/reviews", new_review)
    assertStatus(response, 401)

    # no owner -> 403
    response = client.post(f"/places/{place_id}/reviews", new_review, client.user.access_token)
    assertStatus(response, 403)

    # login -> 201
    access_token = client.login(user)
    response = client.post(f"/places/{place_id}/reviews", new_review, access_token)
    assertStatus(response, 201)

    review_data = response.json()
    for key in new_review:
        assert (
            review_data[key] == new_review[key]
        ), f"Expected {key} to be {new_review[key]} but got {review_data[key]}"
    assert "id" in review_data, "Review ID not in response"
    assert "created_at" in review_data, "Created_at not in response"
    assert "updated_at" in review_data, "Updated_at not in response"
    return review_data["id"]  # Return the ID of the created review for further tests


def test_get_review(client: Client):
    """
    Test to retrieve a specific review by ID
    Creates a new review, then sends a GET request to /reviews/{id} and checks that the
    response status is 200 and the returned data matches the created review's data.
    """
    place_id = client.factory.create_place()
    user = client.factory.create_unique_user()
    new_review = {
        "place_id": place_id,
        "user_id": user['id'],
        "comment": "Great place to stay!",
        "rating": 5.0,
    }
    response = client.post(f"/places/{place_id}/reviews", new_review, client.superuser.access_token)
    assertStatus(response, 201)
    review_id = response.json()["id"]

    # Retrieve the newly created review
    response = client.get(f"/reviews/{review_id}")
    assertStatus(response, 200)
    review_data = response.json()
    for key in new_review:
        assert (
            review_data[key] == new_review[key]
        ), f"Expected {key} to be {new_review[key]} but got {review_data[key]}"
    assert "id" in review_data, "Review ID not in response"
    assert "created_at" in review_data, "Created_at not in response"
    assert "updated_at" in review_data, "Updated_at not in response"


def test_put_review(client: Client):
    """
    Test to update an existing review
    Creates a new review, then sends a PUT request to /reviews/{id} with updated review data
    and checks that the response status is 200 and the returned data matches the updated data.
    """
    place_id = client.factory.create_place()
    user = client.factory.create_unique_user()
    access_token = client.login(user)
    new_review = {
        "user_id": user['id'],
        "comment": "Nice place!",
        "rating": 4.0,
    }
    response = client.post(f"/places/{place_id}/reviews", new_review, access_token)
    assertStatus(response, 201)
    review_id = response.json()["id"]

    # Update the newly created review
    updated_review = {
        "place_id": place_id,
        "user_id": user['id'],
        "comment": "Amazing place, had a great time!",
        "rating": 4.8,
    }

    # no login -> 401
    response = client.put(f"/reviews/{review_id}", updated_review)
    assertStatus(response, 401)

    # no owner -> 403
    response = client.put(f"/reviews/{review_id}", updated_review, client.user.access_token)
    assertStatus(response, 403)

    # login -> 200
    response = client.put(f"/reviews/{review_id}", updated_review, access_token)
    assertStatus(response, 200)

    review_data = response.json()
    for key in updated_review:
        assert (
            review_data[key] == updated_review[key]
        ), f"Expected updated {key} to be {updated_review[key]} but got {review_data[key]}"
    assert "id" in review_data, "Review ID not in response"
    assert "created_at" in review_data, "Created_at not in response"
    assert "updated_at" in review_data, "Updated_at not in response"


def test_delete_review(client: Client):
    """
    Test to delete an existing review
    Creates a new review, then sends a DELETE request to /reviews/{id} and checks that the
    response status is 204 indicating successful deletion.
    """
    place_id = client.factory.create_place()
    user = client.factory.create_unique_user()
    access_token = client.login(user)
    new_review = {
        "user_id": user['id'],
        "comment": "Decent place.",
        "rating": 3.5,
    }
    response = client.post(f"/places/{place_id}/reviews", new_review, access_token)
    assertStatus(response, 201)
    review_id = response.json()["id"]

    # no login -> 401
    response = client.delete(f"/reviews/{review_id}")
    assertStatus(response, 401)

    # no owner -> 403
    response = client.delete(f"/reviews/{review_id}", client.user.access_token)
    assertStatus(response, 403)

    # login -> 204
    response = client.delete(f"/reviews/{review_id}", access_token)
    assertStatus(response, 204)


if __name__ == "__main__":
    # Run the tests
    test_functions(
        [
            test_get_reviews_from_place,
            test_get_reviews_from_user,
            test_post_review,
            test_get_review,
            test_put_review,
            test_delete_review,
        ]
    )
