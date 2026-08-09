import pytest
from playwright.sync_api import APIResponse

from endpoints import Endpoints
from test_products.products_constants import ProductsConstants


class TestSkipLimitProducts:
    # Extracted for code reusability
    def assert_ok(self, response: APIResponse) -> None:
        assert response.ok
        assert response.status == 200

    def assert_response_is_json_dict(self, response: APIResponse) -> dict:
        assert "application/json" in response.headers["content-type"]
        assert isinstance(response.json(), dict)
        return response.json()

    def assert_products_key_in_json_dict(self, json_response: dict) -> list:
        assert ProductsConstants.PRODUCTS_COLLECTION in json_response
        return json_response[ProductsConstants.PRODUCTS_COLLECTION]


    @pytest.mark.parametrize(
        "limit, expected_count",
        [
            (1, 1),
            (15, 15),
            (ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT, ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT),
            (ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT + 1, ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT + 1),
        ],
        ids=["1",
             "15",
             f"default_{ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT}",
             f"default_plus_one_{ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT+1}"]
    )
    def test_limit_response_contains_desired_number_of_products(self, api_context, limit, expected_count):
        """
        Testing valid limit values
        """
        params = {ProductsConstants.LIMIT: limit}

        response = api_context.get(Endpoints.PRODUCTS, params=params)

        self.assert_ok(response)
        json_response = self.assert_response_is_json_dict(response)
        products = self.assert_products_key_in_json_dict(json_response)

        assert len(products) == expected_count

    @pytest.mark.parametrize(
        "limit, expected_count",
        [
            (0, ProductsConstants.ALL_ITEMS_COUNT),
            (ProductsConstants.ALL_ITEMS_COUNT + 1, ProductsConstants.ALL_ITEMS_COUNT),
        ],
        ids=[
             f"all",
             f"more_than_all_return_all"]
    )
    def test_limit_equal_or_greater_than_all_contains_all_products(self, api_context, limit, expected_count):
        """
        I think here it would be better to check the number of all with the server as this value is passed in response.
        """
        params = {ProductsConstants.LIMIT: limit}

        response = api_context.get(Endpoints.PRODUCTS, params=params)

        self.assert_ok(response)
        json_response = self.assert_response_is_json_dict(response)
        products = self.assert_products_key_in_json_dict(json_response)

        assert ProductsConstants.PRODUCTS_ALL_KEY in json_response
        assert len(products) == json_response[ProductsConstants.PRODUCTS_ALL_KEY]

    @pytest.mark.parametrize(
        "limit",
        [
            -1,
            -100,
        ],
        ids=["-1",
             "-100"]
    )
    def test_invalid_limit_response_returns_bad_request(self, api_context, limit):
        """
        Testing invalid limit values doesn't raise an exception
        """
        params = {ProductsConstants.LIMIT: limit}

        response = api_context.get(Endpoints.PRODUCTS, params=params)

        assert not response.ok
        assert response.status == 400

    @pytest.mark.parametrize(
        "limit, skip",
        [
            (1, 1),
            (5,5),
            (5,6),
            (5,10),
            (ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT,
              ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT)
        ],
        ids=["limit_1_skip_1",
             "limit_5_skip_5",
             "limit_5_skip_6",
             "limit_5_skip_10",
             f"limit_{ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT}_skip_{ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT}"]
    )
    def test_skip_greater_or_equal_to_limit_returns_two_different_arrays(self, api_context, limit, skip):
        """
        Testing if pagination works for default limit responses.
        """
        params = {ProductsConstants.LIMIT: limit}

        first_products_response = api_context.get(Endpoints.PRODUCTS, params=params)
        self.assert_ok(first_products_response)
        json_response = self.assert_response_is_json_dict(first_products_response)
        first_products = self.assert_products_key_in_json_dict(json_response)
        assert len(first_products) == limit


        params[ProductsConstants.SKIP] = skip
        second_products_response = api_context.get(Endpoints.PRODUCTS, params=params)
        self.assert_ok(second_products_response)
        json_response = self.assert_response_is_json_dict(second_products_response)
        second_products = self.assert_products_key_in_json_dict(json_response)
        assert len(second_products) == limit

        assert not any(first_products) in second_products


    def test_skip_equal_to_default_limit_returns_two_different_arrays(self, api_context):
        """
        Testing if pagination works for default limit responses.
        """

        first_products_response = api_context.get(Endpoints.PRODUCTS)
        self.assert_ok(first_products_response)
        json_response = self.assert_response_is_json_dict(first_products_response)
        first_products = self.assert_products_key_in_json_dict(json_response)
        assert len(first_products) == ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT

        params = {ProductsConstants.SKIP: ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT}
        second_products_response = api_context.get(Endpoints.PRODUCTS, params=params)
        self.assert_ok(second_products_response)
        json_response = self.assert_response_is_json_dict(second_products_response)
        second_products = self.assert_products_key_in_json_dict(json_response)
        assert len(second_products) == ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT

        assert not any(first_products) in second_products


    @pytest.mark.parametrize(
        "limit, skip, overlapping",
        [
            (5, 1, 4),
            (5, 4, 1),
            (5, 0, 5)
        ],
        ids=["limit_5_skip_1_overlapping_4",
             "limit_5_skip_4_overlapping_1",
             "limit_5_skip_0_overlapping_5"]
    )
    def test_skip_lower_than_limit_returns_two_overlapping_arrays(self, api_context, limit, skip, overlapping):
        """
        Testing if skips allows for overlapping.
        """
        params = {ProductsConstants.LIMIT: limit}

        first_products_response = api_context.get(Endpoints.PRODUCTS, params=params)
        self.assert_ok(first_products_response)
        json_response = self.assert_response_is_json_dict(first_products_response)
        first_products = self.assert_products_key_in_json_dict(json_response)
        assert len(first_products) == limit

        params[ProductsConstants.SKIP] = skip
        second_products_response = api_context.get(Endpoints.PRODUCTS, params=params)
        self.assert_ok(second_products_response)
        json_response = self.assert_response_is_json_dict(second_products_response)
        second_products = self.assert_products_key_in_json_dict(json_response)
        assert len(second_products) == limit

        in_both = [product for product in second_products if product in first_products]

        assert len(in_both) == overlapping

    @pytest.mark.parametrize(
        "skip",
        [
            -1,
            -100,
        ],
        ids=["-1",
             "-100"]
    )
    def test_invalid_skip_value(self, api_context, skip):
        params = {ProductsConstants.SKIP: skip}

        response = api_context.get(Endpoints.PRODUCTS, params=params)

        assert not response.ok
        assert response.status == 400