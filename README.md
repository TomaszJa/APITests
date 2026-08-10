# Automated API Testing Framework

An automated API test suite designed for high readability, scalability, and code reusability. The framework separates test execution, endpoint routing, session context, and response validation into modular components. Although currently configured for the products endpoint, the architecture allows for straightforward extension to support additional endpoints.

---

## 🏗️ Architecture & Project Structure

Tests and supporting assets are organized by API domain modules. CRUD operations and functional capabilities are split into dedicated subdirectories and individual test files:

```text
.
├── endpoints.py                 # Centralized endpoint management
├── response_validator.py        # Static class for global HTTP assertions
├── conftest.py                  # Session-scoped API context fixture
├── requirements.txt             # Project dependencies
└── test_products/              # Products domain module
    ├── product_schema.py        # Schema checks for product payload structures
    ├── products_constants.py     # Product-specific constants
    ├── products_validator.py    # Static class for product-specific validation
    ├── test_create/             # CRUD: Create module
    │   ├── sample_product.py    # Payload samples
    │   └── test_add_product.py # Tests for product creation
    └── test_read/               # CRUD: Read module
        ├── test_get_all_products.py     # Retrieve all items
        ├── test_get_single_product.py  # Retrieve single item
        ├── test_limit_skip_products.py # Limit and skip pagination
        └── test_sort_products.py       # Sorting capabilities
```

---

## 🔑 Key Design Principles

### 1. Centralized Route Management (`endpoints.py`)
All API paths and URLs are centralized in `endpoints.py`. Hardcoded strings inside test files are avoided so route changes can be updated in a single file.

### 2. Session-Scoped API Context (`conftest.py`)
The API context and connection client are scoped to the test session. Reusing the session across tests reduces overhead and enables faster execution.

### 3. Layered Validation Architecture
To keep test cases focused on test logic, assertions are delegated to static validation helpers and schema modules:
* **`ResponseValidator` (`response_validator.py`):** Root-level static class for common HTTP checks, such as validating `response.ok` status and verifying expected status codes.
* **`ProductsValidator` (`test_products/products_validator.py`):** Module-level static class for domain checks, such as collection integrity and dataset assertions.
* **`product_schema` (`test_products/product_schema.py`):** JSON schema definitions used to verify expected fields and structure of returned product objects.

### 4. Granular CRUD & Readability Breakdown
Tests are grouped into separate modules by CRUD operation (`test_create`, `test_read`) for readability. Within each operation folder, distinct files cover specific API functionality (e.g., retrieving all products, single lookup, filtering via limit/skip, and sorting).

---

## 🎯 Testing Scope & Approach

The test suite covers:
* **HTTP Integrity:** Verifying responses are OK and status codes match expectations.
* **Collection Non-Emptiness:** Ensuring list endpoints return non-empty collections when data is expected.
* **Schema Accuracy:** Verifying response objects contain all required product fields.
* **Edge Cases:** Testing parameter bounds, non-existent entities, skip/limit behavior, and error handling.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.9+

### Installation
1. Clone the repository and navigate to the root directory:
   ```bash
   git clone https://github.com/TomaszJa/APITests.git
   cd APITests
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

Run all tests in the repository:
```bash
pytest
```

Run tests only for the **Products** domain:
```bash
pytest test_products/
```

Run tests specifically for **Read** operations:
```bash
pytest test_products/test_read/
```

Run a single test module (e.g., sorting):
```bash
pytest test_products/test_read/test_sort_products.py
```

---

## ➕ Extending to New Endpoints

To extend coverage to a new endpoint (e.g., `/users`):
1. Add the new route definitions to `endpoints.py`.
2. Create a top-level domain folder, such as `test_users/`.
3. Include domain-specific schema (`user_schema.py`) and validator classes (`UsersValidator`) within the module.
4. Organize tests by operation subdirectories (`test_users/test_create/`, `test_users/test_read/`).
