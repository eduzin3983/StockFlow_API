"""
Products repository module.

Provides database operations for Products, including CRUD and stock adjustments,
using SQLAlchemy session management.
"""

from app.infraDB.models.products import Products
from app.infraDB.config.connection import db
from datetime import datetime, timezone


class ProductsRepository:
    """
    Repository for Products model.

    Methods:
        insert_product(data): Insert a new product record.
        update_product(id, name, category, current_stock, add_stock): Update product fields.
        delete_product(id): Delete a product by ID.
        select_all_products(): Retrieve all products.
        select_by_name(name): Retrieve a product by exact name.
        select_product_by_id(id): Retrieve a product by ID.
        select_products_by_name(name): Retrieve products matching partial name.
        select_by_code(code): Retrieve a product by its unique code.
        add_stock(product_id, quantity): Increase product stock.
        remove_stock(product_id, quantity): Decrease product stock if sufficient.
    """

    def insert_product(self, data: dict):
        """
        Create and persist a new product.

        Args:
            data (dict): Product attributes including 'code', 'name', 'category', 'current_stock'.

        Returns:
            Products: The created product instance.
        """
        # Instantiate a Products model with provided data
        data_insert = Products(
            code=data["code"],
            name=data["name"],
            category=data["category"],
            current_stock=data["current_stock"]
        )

        db.session.add(data_insert)
        db.session.commit()

        return data_insert

    def update_product(self, id: int, name: str = None,code: str = None, category: str = None, current_stock: int = None):
        """
        Update fields of an existing product.

        Args:
            id (int): ID of the product to update.
            name (str, optional): New name for the product.
            category (str, optional): New category for the product.
            current_stock (int, optional): Absolute stock value to set.
            add_stock (int, optional): Quantity to add to current stock.

        Returns:
            Products or None: Updated product instance or None if not found.

        Raises:
            ValueError: If both current_stock and add_stock are provided.
        """
        
        # Fetch the product by ID
        product = db.session.query(Products).filter(Products.id == id).first()

        # Return None if product does not exist
        if not product:
            return None

        # Update provided fields
        if name is not None:
            product.name = name
        if category is not None:
            product.category = category
        if current_stock is not None:
            product.current_stock = current_stock
        if code is not None:
            product.code = code

        product.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return product

    def delete_product(self, id: int):
        """
        Delete a product by ID.

        Args:
            id (int): Identifier of the product to delete.

        Returns:
            bool: True if deletion occurred, False otherwise.
        """
        # Perform delete operation on matching record
        result = db.session.query(Products).filter(Products.id == id).delete()
        db.session.commit()

        # Return True if any rows were deleted
        return result > 0

    def select_all_products(self):
        """
        Retrieve all products from the database.

        Returns:
            list[Products]: List of all product instances.
        """
        return db.session.query(Products).all()
    
    def select_by_name(self, name):
        """
        Retrieve a single product by exact name match (case-insensitive).

        Args:
            name (str): Product name to search for.

        Returns:
            Products or None: Matching product or None if not found.
        """
        return db.session.query(Products).filter(Products.name.ilike(name)).first()

    def select_product_by_id(self, id: int):
        """
        Retrieve a single product by its ID.

        Args:
            id (int): Identifier of the product.

        Returns:
            Products or None: Matching product or None if not found.
        """
        return db.session.query(Products).filter(Products.id == id).first()
    
    def select_products_by_name(self, name: str):
        """
        Retrieve products matching partial name search (case-insensitive).

        Args:
            name (str): Substring to search within product names.

        Returns:
            list[Products]: List of matching product instances.
        """
        return db.session.query(Products).filter(Products.name.ilike(f"%{name}%")).all()

    def select_by_code(self, code: str):
        """
        Retrieve a product by its unique code.

        Args:
            code (str): Unique product code.

        Returns:
            Products or None: Matching product or None if not found.
        """
        return db.session.query(Products).filter(Products.code == code).first()

    def add_stock(self, product_id: int, quantity: int):
        """
        Increase the stock level of a product.

        Args:
            product_id (int): ID of the product to update.
            quantity (int): Amount of stock to add.

        Returns:
            Products or None: Updated product instance or None if not found.
        """
        # Fetch the product by ID
        product = self.select_product_by_id(product_id)
        if not product:
            return None

        # Increase the stock and update timestamp
        product.current_stock += quantity
        product.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return product

    def remove_stock(self, product_id: int, quantity: int):
        """
        Decrease the stock level of a product if sufficient quantity exists.

        Args:
            product_id (int): ID of the product to update.
            quantity (int): Amount of stock to remove.

        Returns:
            Products or None: Updated product instance, or None if not found or insufficient stock.
        """
        # Fetch the product by ID
        product = self.select_product_by_id(product_id)
        # Return None if product does not exist or stock insufficient
        if not product or product.current_stock < quantity:
            return None

        # Decrease the stock and update timestamp
        product.current_stock -= quantity
        product.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return product
