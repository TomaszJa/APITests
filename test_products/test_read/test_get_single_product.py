import pytest

from endpoints import Endpoints
from test_products.products_constants import ProductsConstants


class TestGetSingleProduct:
    @pytest.mark.parametrize(
    "product_id",
    [
        1,
        2,
        ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT,
        ProductsConstants.ALL_ITEMS_COUNT,
    ],
    ids = ["id_1",
           "id_2",
           f"id_{ProductsConstants.DEFAULT_GET_ALL_ITEMS_COUNT}",
           f"id_{ProductsConstants.ALL_ITEMS_COUNT}",]

    )
    def test_invalid_limit_response_returns_bad_request(self, api_context, product_id):
        """
        Testing invalid limit values doesn't raise an exception
        """
        response = api_context.get(f"{Endpoints.PRODUCTS}/{product_id}")

        assert response.ok
        assert response.status == 200