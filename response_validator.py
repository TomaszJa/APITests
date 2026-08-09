from playwright.sync_api import APIResponse


class ResponseValidator:
    @staticmethod
    def assert_ok_200(response: APIResponse) -> None:
        assert response.ok
        assert response.status == 200

    @staticmethod
    def validate_response_is_json_dict(response: APIResponse) -> dict:
        assert "application/json" in response.headers["content-type"]
        assert isinstance(response.json(), dict)
        return response.json()

    @staticmethod
    def assert_bad_request(response: APIResponse):
        assert not response.ok
        assert response.status == 400

    @staticmethod
    def assert_not_found(response: APIResponse):
        assert not response.ok
        assert response.status == 404