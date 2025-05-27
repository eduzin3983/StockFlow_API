"""
Product service module.

Contains business logic for product operations, including creation, retrieval,
update, and deletion, interacting with ProductsRepository for persistence and
applying domain rules such as uniqueness checks and data normalization.
"""

from app.infraDB.repositories.products_repositorie import ProductsRepository


def create_product(data):
    """
    Create a new product after normalizing fields and validating uniqueness.

    Args:
        data (dict): Raw product data containing 'code', 'name', 'category', and 'current_stock'.

    Returns:
        Products: The newly created product instance from the repository.

    Raises:
        ValueError: If a product with the same code or name already exists.
    """
    repo = ProductsRepository()

    # Normalize the 'name' field to title case if provided
    if "name" in data:
        data["name"] = data["name"].strip().title()

    # Normalize the 'category' field to title case if provided
    if "category" in data:
        data["category"] = data["category"].strip().title()

    # Ensure product code is unique
    existingCode = repo.select_by_code(data["code"])
    if existingCode:
        raise ValueError("A product with this code already exists.")

    # Ensure product name is unique
    existing = repo.select_by_name(data["name"])
    if existing:
        raise ValueError("A product with this name already exists.")

    # Delegate insertion to repository
    produto = repo.insert_product(data)
    return produto


def get_all_products(name=None, code=None):
    """
    Retrieve products with optional filtering by exact code or partial name match.

    Args:
        name (str, optional): Substring to search within product names.
        code (str, optional): Exact product code to filter.

    Returns:
        list[Products]: List of matching product instances (empty if none found).
    """
    repo = ProductsRepository()

    # Filter by code first, returning a single-product list if found
    if code:
        product = repo.select_by_code(code)
        return [product] if product else []

    # If name filter provided, perform partial match search
    if name:
        return repo.select_products_by_name(name)

    # No filters: return all products
    return repo.select_all_products()


def get_product_by_id(id: int):
    """
    Retrieve a single product by its identifier.

    Args:
        id (int): Identifier of the product to fetch.

    Returns:
        Products or None: Matching product instance or None if not found.
    """
    repo = ProductsRepository()
    # Delegate fetch by ID to repository
    return repo.select_product_by_id(id)


def update_product(id: int, data: dict):
    """
    Update fields of an existing product, applying normalization and
    enforcing business rules on uniqueness and stock adjustments.

    Args:
        id (int): Identifier of the product to update.
        data (dict): Dictionary of fields to update ('name', 'category', 'current_stock', 'add_stock').

    Returns:
        Products: The updated product instance.

    Raises:
        ValueError: If product not found, name conflict, or both stock fields provided.
    """
    repo = ProductsRepository()

    # Ensure the product exists before attempting update
    existing = repo.select_product_by_id(id)
    if not existing:
        raise ValueError("Product not found")

    # Normalize and check uniqueness when updating name
    if "name" in data:
        data["name"] = data["name"].strip().title()
        same_name = repo.select_by_name(data["name"])
        # If another product with the same name exists, prevent update
        if same_name and same_name.id != id:
            raise ValueError("Another product with this name already exists.")
    
    # Normalize category if provided
    if "category" in data:
        data["category"] = data["category"].strip().title()

    if "code" in data:
        data["code"] = data["code"].strip()
        same_name = repo.select_by_code(data["code"])
        # If another product with the same name exists, prevent update
        if same_name and same_name.id != id:
            raise ValueError("Another product with this name already exists.")

    # Delegate update to repository with validated fields
    return repo.update_product(
        id=id,
        code=data.get("code"),
        name=data.get("name"),
        category=data.get("category"),
        current_stock=data.get("current_stock"),
    )


def delete_product(id: int):
    """
    Delete an existing product by its identifier.

    Args:
        id (int): Identifier of the product to remove.

    Returns:
        None

    Raises:
        ValueError: If the product to delete does not exist.
    """
    repo = ProductsRepository()
    # Attempt deletion; repository returns True if deleted
    deleted = repo.delete_product(id)
    if not deleted:
        # No record deleted implies non-existence
        raise ValueError("Product not found")