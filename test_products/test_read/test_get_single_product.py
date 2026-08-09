import pytest
from playwright.sync_api import Error

from endpoints import Endpoints
from test_products.product_schema import ProductSchema
from test_products.products_constants import ProductsConstants
from response_validator import ResponseValidator


class TestGetSingleProduct:
    @pytest.mark.parametrize(
    "product_id",
    [
        0,
        -1,
        ProductsConstants.ALL_ITEMS_COUNT+1
    ],
    ids = ["id_0",
           "id_-1",
           f"id_{ProductsConstants.ALL_ITEMS_COUNT+1}"]

    )
    def test_invalid_id_response_returns_not_found(self, api_context, product_id):
        """
        Testing invalid id values returns not found
        """
        response = api_context.get(f"{Endpoints.PRODUCTS}/{product_id}")

        ResponseValidator.assert_not_found(response)

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
    def test_response_for_valid_id_is_json_object(self, api_context, product_id):
        """
        Testing invalid limit values doesn't raise an exception
        """
        response = api_context.get(f"{Endpoints.PRODUCTS}/{product_id}")

        ResponseValidator.assert_ok_200(response)
        ResponseValidator.validate_response_is_json_dict(response)

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
    def test_product_schema(self, api_context, product_id):
        """
        Testing product schema validation
        should be much more extensive, but as it is only for demonstration purposes I kept in concise.
        """
        response = api_context.get(f"{Endpoints.PRODUCTS}/{product_id}")

        ResponseValidator.assert_ok_200(response)

        data = response.json()
        product = ProductSchema.model_validate(data)

        assert product.id == product_id
        assert len(product.title) > 0, "Product should have a title"
        assert len(product.tags) > 0, "Product should have at least one tag"

        assert product.meta.createdAt <= product.meta.updatedAt, "Product should have been updated after creation"

    def test_delayed_response_less_than_timeout(self, api_context):
        """
        Testing delayed response that is smaller than timeout
        """
        response = api_context.get(f"{Endpoints.PRODUCTS}/{1}", params={"delay": 2000}, timeout=5000)

        ResponseValidator.assert_ok_200(response)

    def test_delayed_response_times_out(self, api_context):
        """
        Testing delayed response that will throw an exception.
        """
        with pytest.raises(Error) as e:
            api_context.get(f"{Endpoints.PRODUCTS}/{1}", params={"delay": 3000}, timeout=1000)

        assert e.typename == "TimeoutError"
