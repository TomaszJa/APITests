from playwright.async_api import APIResponse

from response_validator import ResponseValidator
from test_products.product_schema import ProductSchema
from test_products.products_constants import ProductsConstants


class ProductsValidator:
    @staticmethod
    def assert_products_list_in_json_dict(json_response: dict):
        assert ProductsConstants.PRODUCTS_COLLECTION in json_response, "response does not contain products collection"
        assert isinstance(json_response[ProductsConstants.PRODUCTS_COLLECTION], list)

    @staticmethod
    def validate_products_list_in_json_dict(json_response: dict) -> list:
        ProductsValidator.assert_products_list_in_json_dict(json_response)
        products = json_response[ProductsConstants.PRODUCTS_COLLECTION]
        for product in products:
            ProductSchema.model_validate(product)
        return products

    @staticmethod
    def validate_products(response: APIResponse) -> list:
        ResponseValidator.assert_ok_200(response)
        json_response = ResponseValidator.validate_response_is_json_dict(response)
        products = ProductsValidator.validate_products_list_in_json_dict(json_response)
        return products