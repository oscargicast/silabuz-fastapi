import pytest
from main import app
from fastapi.testclient import TestClient
from utils.jwt_manager import create_token
from schemas.item import StatusItem


client = TestClient(app)


@pytest.fixture
def user():
    return {
        "email": "user@example.com",
        "password": "pass",
    }


@pytest.fixture
def url_login():
    return "/login/"


def test_read_root():
    response = client.get("/")
    assert response.status_code == 201
    assert response.text == "<h1>Hello world</h1>"
    # assert response.json() == {"msg": "Hello World"}


# def test_login_error():
#     response = client.post(
#         "/login/",
#         json={
#             "email": "admin@gmail.com",
#             "password": "badpassword",
#         }
#     )
#     assert response.status_code == 401
#     assert response.json() == {"message": "Check the email or password!"}


# def test_login_success():
#     response = client.post(
#         "/login/",
#         json={
#             "email": "admin@gmail.com",
#             "password": "admin",
#         }
#     )
#     assert response.status_code == 200


class TestLogin:

    # def __init__(self):
    #     self.url = "/login/"
    #     super()

    def test_login_error(self, url_login):
        response = client.post(
            # self.url,
            # "/login/"
            url_login,
            json={
                "email": "admin@gmail.com",
                "password": "badpassword",
            }
        )
        assert response.status_code == 403
        assert response.json() == {"message": "Check the email or password!"}


    def test_login_success(self, url_login):
        data = {
            "email": "admin@gmail.com",
            "password": "admin",
        }
        response = client.post(
            # self.url,
            url_login,
            json=data,
        )
        assert response.status_code == 200
        token = create_token(data)
        assert token == response.json()



class TestCreateItem:

    def get_token(self):
        user = {
            "email": "admin@gmail.com",
            "password": "admin",
        }
        token: str = create_token(user)
        return f"Bearer {token}"

    def test_login_error(self, url_login):
        data = {
            "new_item": {
                "name": "test",
                "price": 100,
                "status": StatusItem.bad,
            },
            "add_depreciation": True,
        }
        # Request without token -> 401.
        response = client.post(
            "/items/",
            json=data,
        )
        assert response.status_code == 403
        # Adding token -> 201.
        response = client.post(
            "/items/",
            json=data,
            headers={
                "Authorization": self.get_token(),
            }
        )
        assert response.status_code == 201
        result = response.json()
        assert result["name"] == "test"
        assert result["price"] == 70