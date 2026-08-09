import pytest

from endpoints import Endpoints
from test_products.products_constants import ProductsConstants


class TestGetAllProducts:
    def test_response_ok(self, api_context):
        response = api_context.get(Endpoints.PRODUCTS)

        assert response.ok
        assert response.status == 200

    def test_response_type_json(self, api_context):
        response = api_context.get(Endpoints.PRODUCTS)

        assert response.ok
        assert response.status == 200

        assert "application/json" in response.headers["content-type"]

    def test_response_not_empty(self, api_context):
        """
        Check if the response is not empty. and we are not browsing the empty db.
        """
        response = api_context.get(Endpoints.PRODUCTS)

        assert response.ok
        assert response.status == 200

        products = response.json().get(ProductsConstants.PRODUCTS_COLLECTION)

        assert len(products)>0

    def test_response_contains_default_number_of_products(self, api_context):
        """
        Want to make sure that even though the response may contain more than one product, the default number hasn't
        been changed as stated in the docs. https://dummyjson.com/docs/products#products-all
        """
        response = api_context.get(Endpoints.PRODUCTS)

        assert response.ok
        assert response.status == 200

        products = response.json().get(ProductsConstants.PRODUCTS_COLLECTION)

        assert len(products) == ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT




