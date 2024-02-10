# Django Models and ORM

This Django project has been extended to include a new `Product` model and related views for handling CRUD operations and additional product-related queries.

## Changes Made

1. **Added Product Model**: Introduced a new `Product` model with fields such as `name`, `price`, `description`, `category`, and `created_at`.

2. **Added Product Views**: Created new views (`product_view`, `product_detail_view`, `products_by_price_desc`, `products_in_price_range`, `products_recently_added`, `products_by_keyword`, `products_by_category`) to handle CRUD operations and additional product-related queries.

3. **URL Pattern Updates**: Modified `urls.py` to include new URL patterns for product-related views.

4. **JSON Encoder Usage**: Utilized Django's `DjangoJSONEncoder` in the `json.dumps` method to handle serialization of `DateTimeField` in the `Product` model.

5. **Code Formatting and Documentation**: Improved code formatting and added comments to enhance readability and understanding.

6. **Additional Product Queries**: Implemented views for retrieving products ordered by price, within a specified price range, recently added products, products containing a keyword, and products in a specific category.

7. **Challenges Faced**: There were no significant challenges faced during the assignment. The main focus was on extending the existing codebase to include product-related functionalities.
