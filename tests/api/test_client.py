from clients.crm_client import CRMClient
import pytest

# Тест без параметризации, открываем один эндпоинт
def test_get_operations(base_url, access_token, id_token):
    test_client = CRMClient(base_url=base_url, access_token=access_token, id_token=id_token)
    resp = test_client.get_operations()
    assert resp.status_code == 200, (
        f"Expected 200, got {resp.status_code}. "
        f"Response: {resp.text}"
    )

class TestGetEndpoints:
    @pytest.mark.parametrize(
        "request_func, endpoint",
        [
            (lambda client: client.get_operations(), "/operations"),
            (lambda client: client.get_waiters_management(), "/employees"),
            (lambda client: client.get_clients(), "/clients"),
        ]
    )
    def test_get_endpoints_return_200(self, base_url, access_token, id_token, request_func, endpoint):
        test_client = CRMClient(
            base_url=base_url,
            access_token=access_token,
            id_token=id_token
        )

        # 1 resp = test_client.get_operations()
        # 2 resp = test_client.get_waiters_management()
        # 3 resp = test_client.get_clients()
        resp = request_func(test_client)

        assert resp.status_code == 200, (
            f"Endpoint {endpoint}: expected 200, got {resp.status_code}. "
            f"Response: {resp.text}"
        )

    @pytest.mark.parametrize(
        "missing_field, expected_error",
        [
            ("base_url", "BASE_URL is not set"),
            ("access_token", "AUTH_ACCESS_TOKEN is not set"),
            ("id_token", "AUTH_ID_TOKEN is not set")
        ]
    )
    def test_client_init_raises_error_if_required_data_is_missing(
            self,
            base_url,
            access_token,
            id_token,
            missing_field,
            expected_error
    ):
        valid_base_url = base_url
        valid_access_token = access_token
        valid_id_token = id_token

        if missing_field == "base_url":
            valid_base_url = ""
        elif missing_field == "access_token":
            valid_access_token = ""
        elif missing_field == "id_token":
            valid_id_token = ""

        with pytest.raises(ValueError) as e:
            CRMClient(
                base_url=valid_base_url,
                access_token=valid_access_token,
                id_token=valid_id_token
            )

        assert str(e.value) == expected_error

