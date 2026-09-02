import pytest
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_get_all_mechanics(client):
    response=client.get("/mechanics/")
    assert response.status_code==200

@pytest.mark.django_db
def test_create_mechanic():
    client = APIClient()

    data = {
        "name": "ABC Motors",
        "phone": "9876543210",
        "location": "Delhi",
        "rating": "4.5",
        "is_open": True,
        "services": [
            "Oil Change",
            "Brake Repair"
        ]
    }

    response = client.post(
        "/mechanics/",
        data=data,
        format="json"
    )

    assert response.status_code == 201
    assert response.data["name"] == "ABC Motors"
    assert response.data["phone"] == "9876543210"

@pytest.mark.django_db
def test_get_mechanic_by_id(client):
    # Create a mechanic
    data = {
        "name": "ABC Motors",
        "phone": "9876543210",
        "location": "Delhi",
        "rating": "4.5",
        "is_open": True,
        "services": ["Oil Change"]
    }

    create_response = client.post("/mechanics/", data, format="json")
    mechanic_id = create_response.data["id"]

    response = client.get(f"/mechanics/{mechanic_id}/")

    assert response.status_code == 200

@pytest.mark.django_db
def test_patch_mechanic():
    client = APIClient()

    create_response = client.post(
        "/mechanics/",
        data={
            "name": "ABC Motors",
            "phone": "9876543210",
            "location": "Delhi",
            "rating": "4.5",
            "is_open": True,
            "services": [
                "Oil Change",
                "Brake Repair"
            ]
        },
        format="json"
    )

    mechanic_id = create_response.data["id"]

    response = client.patch(
        f"/mechanics/{mechanic_id}/",
        data={
            "rating": "4.8"
        },
        format="json"
    )

    assert response.status_code == 200
    assert response.data["rating"] == "4.8"
    assert response.data["name"] == "ABC Motors"

@pytest.mark.django_db
def test_put_mechanic():
    client = APIClient()

    create_response = client.post(
        "/mechanics/",
        data={
            "name": "ABC Motors",
            "phone": "9876543210",
            "location": "Delhi",
            "rating": "4.5",
            "is_open": True,
            "services": [
                "Oil Change",
                "Brake Repair"
            ]
        },
        format="json"
    )

    mechanic_id = create_response.data["id"]

    response = client.put(
        f"/mechanics/{mechanic_id}/",
        data={
            "name": "XYZ Motors",
            "phone": "9876543211",
            "location": "Noida",
            "rating": "4.8",
            "is_open": False,
            "services": [
                "Oil Change",
                "Engine Repair"
            ]
        },
        format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "XYZ Motors"
    assert response.data["location"] == "Noida"
    assert response.data["rating"] == "4.8"
    assert response.data["is_open"] is False

@pytest.mark.django_db
def test_delete_mechanic():
    client = APIClient()

    create_response = client.post(
        "/mechanics/",
        data={
            "name": "ABC Motors",
            "phone": "9876543210",
            "location": "Delhi",
            "rating": "4.5",
            "is_open": True,
            "services": [
                "Oil Change",
                "Brake Repair"
            ]
        },
        format="json"
    )

    mechanic_id = create_response.data["id"]

    response = client.delete(
        f"/mechanics/{mechanic_id}/"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/mechanics/{mechanic_id}/"
    )

    assert get_response.status_code == 404

@pytest.mark.django_db
def test_create_service_request():
    client = APIClient()

    mechanic_response = client.post(
        "/mechanics/",
        data={
            "name": "ABC Motors",
            "phone": "9876543210",
            "location": "Delhi",
            "rating": "4.5",
            "is_open": True,
            "services": [
                "Oil Change",
                "Brake Repair"
            ]
        },
        format="json"
    )

    mechanic_id = mechanic_response.data["id"]

    response = client.post(
        "/service-requests/",
        data={
            "customer_name": "XYZ",
            "customer_phone": "9876543210",
            "vehicle_number": "DL01AB1234",
            "mechanic_id": mechanic_id,
            "service": "Oil Change",
            "problem_description": "Engine making noise"
        },
        format="json"
    )

    assert response.status_code == 201
    assert response.data["customer_name"] == "XYZ"
    assert response.data["mechanic_id"] == mechanic_id
    assert response.data["service"] == "Oil Change"
    assert response.data["status"] == "PENDING"

@pytest.mark.django_db
def test_get_nonexistent_mechanic():
    client = APIClient()

    response = client.get("/mechanics/999/")

    assert response.status_code == 404
    assert response.data["detail"] == "Mechanic with id 999 does not exist."

@pytest.mark.django_db
def test_put_nonexistent_mechanic():
    client = APIClient()

    response = client.put(
        "/mechanics/999/",
        data={
            "name": "ABC Motors",
            "phone": "9876543210",
            "location": "Delhi",
            "rating": "4.5",
            "is_open": True,
            "services": ["Oil Change"]
        },
        format="json"
    )

    assert response.status_code == 404

    assert "detail" in response.data
    assert response.data["detail"] == "Mechanic with id 999 does not exist."

@pytest.mark.django_db
def test_patch_nonexistent_mechanic():
    client = APIClient()

    response = client.patch(
        "/mechanics/999/",
        data={"rating": "4.8"},
        format="json"
    )

    assert response.status_code == 404
    assert response.data["detail"] == "Mechanic with id 999 does not exist."

@pytest.mark.django_db
def test_delete_nonexistent_mechanic():
    client = APIClient()

    response = client.delete("/mechanics/999/")

    assert response.status_code == 404
    assert response.data["detail"] == "Mechanic with id 999 does not exist."

@pytest.mark.django_db
def test_service_request_invalid_phone():
    client = APIClient()

    mechanic_response = client.post(
        "/mechanics/",
        data={
            "name": "ABC Motors",
            "phone": "9876543210",
            "location": "Delhi",
            "rating": "4.5",
            "is_open": True,
            "services": ["Oil Change"]
        },
        format="json"
    )

    mechanic_id = mechanic_response.data["id"]

    response = client.post(
        "/service-requests/",
        data={
            "customer_name": "XYZ",
            "customer_phone": "987654321",
            "vehicle_number": "DL01AB1234",
            "mechanic_id": mechanic_id,
            "service": "Oil Change",
            "problem_description": "Engine making noise"
        },
        format="json"
    )

    assert response.status_code == 400
    assert response.data["customer_phone"] == [
        "Customer phone number must be a 10-digit number."
    ]

@pytest.mark.django_db
def test_service_request_invalid_vehicle_number():
    client = APIClient()

    mechanic_response = client.post(
        "/mechanics/",
        data={
            "name": "ABC Motors",
            "phone": "9876543210",
            "location": "Delhi",
            "rating": "4.5",
            "is_open": True,
            "services": ["Oil Change"]
        },
        format="json"
    )

    mechanic_id = mechanic_response.data["id"]

    response = client.post(
        "/service-requests/",
        data={
            "customer_name": "XYZ",
            "customer_phone": "9876543210",
            "vehicle_number": "INVALID",
            "mechanic_id": mechanic_id,
            "service": "Oil Change",
            "problem_description": "Engine making noise"
        },
        format="json"
    )

    assert response.status_code == 400
    assert "vehicle_number" in response.data

@pytest.mark.django_db
def test_service_request_required_field_missing():
    client = APIClient()

    mechanic_response = client.post(
        "/mechanics/",
        data={
            "name": "ABC Motors",
            "phone": "9876543210",
            "location": "Delhi",
            "rating": "4.5",
            "is_open": True,
            "services": ["Oil Change"]
        },
        format="json"
    )

    mechanic_id = mechanic_response.data["id"]

    response = client.post(
        "/service-requests/",
        data={
            "customer_phone": "9876543210",
            "vehicle_number": "DL01AB1234",
            "mechanic_id": mechanic_id,
            "service": "Oil Change",
            "problem_description": "Engine making noise"
        },
        format="json"
    )

    assert response.status_code == 400
    assert response.data["customer_name"] == ["This field is required."]

@pytest.mark.django_db
def test_service_request_invalid_service():
    client = APIClient()

    mechanic_response = client.post(
        "/mechanics/",
        data={
            "name": "ABC Motors",
            "phone": "9876543210",
            "location": "Delhi",
            "rating": "4.5",
            "is_open": True,
            "services": ["Oil Change"]
        },
        format="json"
    )

    mechanic_id = mechanic_response.data["id"]

    response = client.post(
        "/service-requests/",
        data={
            "customer_name": "Mayuri",
            "customer_phone": "9876543210",
            "vehicle_number": "DL01AB1234",
            "mechanic_id": mechanic_id,
            "service": "Engine Repair",
            "problem_description": "Engine making noise"
        },
        format="json"
    )

    assert response.status_code == 400
    assert response.data["service"] == [
        "This service is not provided by the selected mechanic."
    ]

@pytest.mark.django_db
def test_service_request_invalid_mechanic_id():
    client = APIClient()

    response = client.post(
        "/service-requests/",
        data={
            "customer_name": "Mayuri",
            "customer_phone": "9876543210",
            "vehicle_number": "DL01AB1234",
            "mechanic_id": "abc",
            "service": "Oil Change",
            "problem_description": "Engine making noise"
        },
        format="json"
    )

    assert response.status_code == 400
    assert response.data["mechanic_id"] == [
        "Incorrect type. Expected pk value, received str."
    ]