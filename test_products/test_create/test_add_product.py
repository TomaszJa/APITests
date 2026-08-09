from endpoints import Endpoints
from response_validator import ResponseValidator
from test_products.products_constants import ProductsConstants
from test_products.test_create.sample_product import SAMPLE_NEW_PRODUCT, SAMPLE_EXISTING_PRODUCT


class TestAddProduct:
    def test_add_new_product_returns_success(self, api_context):
        add_endpoint = f"{Endpoints.PRODUCTS}/add"

        first_response = api_context.post(add_endpoint, data=SAMPLE_NEW_PRODUCT)
        ResponseValidator.assert_created_201(first_response)

        json_response = first_response.json()

        assert json_response["id"] == ProductsConstants.ALL_ITEMS_COUNT + 1

    def test_add_existing_product_returns_bad_request(self, api_context):
        """
        In my opinion it should return a 400 or 409 when a product already exists.
        """
        add_endpoint = f"{Endpoints.PRODUCTS}/add"

        first_response = api_context.post(add_endpoint, data=SAMPLE_EXISTING_PRODUCT)
        ResponseValidator.assert_bad_request(first_response)

    def test_new_product_with_wrong_data_returns_bad_request(self, api_context):
        """
        In my opinion it should return a 400 or 409 when a product already exists.
        """
        add_endpoint = f"{Endpoints.PRODUCTS}/add"

        first_response = api_context.post(add_endpoint, data=SAMPLE_EXISTING_PRODUCT)
        ResponseValidator.assert_bad_request(first_response)