import pytest

from endpoints import Endpoints
from response_validator import ResponseValidator
from test_products.products_constants import ProductsConstants
from test_products.products_validator import ProductsValidator


class TestSortProducts:
    @pytest.mark.parametrize(
        "sort_field",
        [
            "title",
            "rating",
        ],
        ids=["title",
            "rating" ]

    )
    def test_sort_products_asc(self, api_context, sort_field):
        params = {ProductsConstants.LIMIT: 0}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        products = ProductsValidator.validate_products(response)
        manually_sorted = sorted(products, key=lambda x: x[sort_field])

        params = {ProductsConstants.SORTBY: sort_field,
                  ProductsConstants.ORDER: "asc",
                  ProductsConstants.LIMIT: 0}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        sorted_products = ProductsValidator.validate_products(response)

        assert manually_sorted == sorted_products

    @pytest.mark.parametrize(
        "sort_field",
        [
            "title",
            "rating",
        ],
        ids=["title",
            "rating" ]

    )
    def test_sort_products_dsc(self, api_context, sort_field):
        params = {ProductsConstants.LIMIT: 0}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        products = ProductsValidator.validate_products(response)
        manually_sorted = sorted(products, key=lambda x: x[sort_field], reverse=True)

        params = {ProductsConstants.SORTBY: sort_field,
                  ProductsConstants.ORDER: "desc",
                  ProductsConstants.LIMIT: 0}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        sorted_products = ProductsValidator.validate_products(response)

        assert manually_sorted == sorted_products

    @pytest.mark.parametrize(
        "order",
        [
            "a",
            "asec",
            "dsc",
        ]
    )
    def test_sort_products_order_misspelled_returns_bad_request(self, api_context, order):
        """
        I think that misspelled order by shout return default ordering, but it is what it is.
        """
        params = {ProductsConstants.SORTBY: "title",
                  ProductsConstants.ORDER: order}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        ResponseValidator.assert_bad_request(response)

    @pytest.mark.parametrize(
        "sort_field",
        [
            "jd",
            "ttle",
            "rting",
        ]
    )
    def test_sort_products_sort_misspelled_returns_default_order(self, api_context, sort_field):
        """
        Strange api behaviour if order misspelled makes it a bad request, but non-existing field doesn't, but it is what
        it is
        """
        response = api_context.get(Endpoints.PRODUCTS)
        products = ProductsValidator.validate_products(response)

        params = {ProductsConstants.SORTBY: sort_field,
                  ProductsConstants.ORDER: "asc"}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        sorted_products = ProductsValidator.validate_products(response)

        assert products == sorted_products

    @pytest.mark.parametrize(
        "sort_field",
        [
            "title",
            "rating",
        ],
        ids=["title",
            "rating" ]
    )
    def test_sort_products_order_missing_(self, api_context, sort_field):
        """
        tests if default ordering is working as expected.
        """
        params = {ProductsConstants.LIMIT: 0}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        products = ProductsValidator.validate_products(response)
        manually_sorted = sorted(products, key=lambda x: x[sort_field])

        params = {ProductsConstants.SORTBY: sort_field,
                  ProductsConstants.LIMIT: 0}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        sorted_products = ProductsValidator.validate_products(response)

        assert manually_sorted == sorted_products

    def test_sort_products_by_id_with_sort_missing_order_asc(self, api_context):
        """
        tests if default ordering is sorting by id
        """
        params = {ProductsConstants.LIMIT: 0}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        products = ProductsValidator.validate_products(response)
        manually_sorted = sorted(products, key=lambda x: x["id"])

        params = {ProductsConstants.ORDER: "asc",
                  ProductsConstants.LIMIT: 0}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        sorted_products = ProductsValidator.validate_products(response)

        assert manually_sorted == sorted_products

    def test_sort_products_by_id_with_sort_missing_order_desc(self, api_context):
        """
        tests if default ordering is sorting by id in descending order. This one fails, but I think that this should be
        the proper behaviour for API.
        """
        params = {ProductsConstants.LIMIT: 0}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        products = ProductsValidator.validate_products(response)
        manually_sorted = sorted(products, key=lambda x: x["id"], reverse=True)

        params = {ProductsConstants.ORDER: "desc",
                  ProductsConstants.LIMIT: 0}

        response = api_context.get(Endpoints.PRODUCTS, params=params)
        sorted_products = ProductsValidator.validate_products(response)

        assert manually_sorted == sorted_products