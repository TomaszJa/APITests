"""
Once the name of the endpoint changes it is easier to change it in one place than updating all methods.
Also, if we wish to test more endpoints, then it's better approach to keep constants in a separate entity rather than
defining them on the class level
"""
class Endpoints:
    PRODUCTS = "products"
    ADD_PRODUCT = f"{PRODUCTS}/add"
    # in future may be extended to other endpoints