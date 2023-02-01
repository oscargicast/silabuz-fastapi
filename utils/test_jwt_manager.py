from utils.jwt_manager import create_token, validate_token


class TestJWT:

    def test_jwt(self):
        data = {
            "email": "test@example.com",
            "password": "pass",
        }
        encoded_jwt = create_token(data)
        decrypted_token = validate_token(encoded_jwt)
        assert data == decrypted_token
        assert data["password"] == decrypted_token["password"]