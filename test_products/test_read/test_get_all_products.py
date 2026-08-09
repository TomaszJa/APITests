import pytest
from playwright.sync_api import Error

from endpoints import Endpoints
from response_validator import ResponseValidator
from test_products.product_schema import ProductSchema
from test_products.products_constants import ProductsConstants
from test_products.products_validator import ProductsValidator


class TestGetAllProducts:
    def test_response_ok(self, api_context):
        response = api_context.get(Endpoints.PRODUCTS)

        ResponseValidator.assert_ok_200(response)

    def test_response_type_json(self, api_context):
        response = api_context.get(Endpoints.PRODUCTS)

        ResponseValidator.assert_ok_200(response)

        assert "application/json" in response.headers["content-type"]

    def test_response_not_empty(self, api_context):
        """
        Check if the response is not empty. and we are not browsing the empty db.
        """
        response = api_context.get(Endpoints.PRODUCTS)

        ResponseValidator.assert_ok_200(response)
        json_response = ResponseValidator.validate_response_is_json_dict(response)
        products = ProductsValidator.validate_products_list_in_json_dict(json_response)

        assert len(products)>0

    def test_response_contains_valid_objects(self, api_context):
        """
        Check if the response contains valid objects.
        """
        response = api_context.get(Endpoints.PRODUCTS)

        ResponseValidator.assert_ok_200(response)
        json_response = ResponseValidator.validate_response_is_json_dict(response)
        products = ProductsValidator.validate_products_list_in_json_dict(json_response)

        assert len(products)>0
        for product in products:
            ProductSchema.model_validate(product)

    def test_delayed_response_less_than_timeout(self, api_context):
        """
        Testing delayed response that is smaller than timeout
        """
        response = api_context.get(Endpoints.PRODUCTS, params={"delay": 2000}, timeout=5000)

        ResponseValidator.assert_ok_200(response)

    def test_delayed_response_times_out(self, api_context):
        """
        Testing delayed response that will throw an exception.
        """
        with pytest.raises(Error) as e:
            api_context.get(Endpoints.PRODUCTS, params={"delay": 3000}, timeout=1000)

        assert e.typename == "TimeoutError"

    def test_response_contains_default_number_of_products(self, api_context):
        """
        Want to make sure that even though the response may contain more than one product, the default number hasn't
        been changed as stated in the docs. https://dummyjson.com/docs/products#products-all
        """
        response = api_context.get(Endpoints.PRODUCTS)

        products = ProductsValidator.validate_products(response)

        assert len(products) == ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT

