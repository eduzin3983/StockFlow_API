"""
Product schema module.

Defines input validation and serialization schema for product resources using Marshmallow.
Includes fields for product attributes, timestamps, and optional stock adjustments.
"""

from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    """
    Schema for validating and serializing Product data.

    Fields:
        id (int): Read-only unique identifier of the product.
        created_at (datetime): Read-only creation timestamp.
        updated_at (datetime): Read-only last update timestamp.
        name (str): Name of the product; must be non-empty.
        category (str): Category of the product; must be non-empty.
        current_stock (int): Current stock level; must be zero or positive.
        add_stock (int, optional): Amount to add to stock; if provided, must be positive.
        code (str): Unique product code; length between 1 and 10.
    """
    # Read-only ID assigned by the database
    id = fields.Int(dump_only=True)
    # Read-only timestamp of record creation
    created_at = fields.DateTime(dump_only=True)
    # Read-only timestamp of last record update
    updated_at = fields.DateTime(dump_only=True)

    # Name field: required and non-empty string
    name = fields.Str(
        required=True,
        validate=validate.Length(
            min=1,
            error="Name must not be empty."
        ),
        error_messages={"required": "The name field is required."}
    )

    # Category field: required and non-empty string
    category = fields.Str(
        required=True,
        validate=validate.Length(
            min=1,
            error="Category must not be empty."
        ),
        error_messages={"required": "The category field is required."}
    )

    # Current stock field: required and must be >= 0
    current_stock = fields.Int(
        required=True,
        validate=validate.Range(
            min=0,
            error="Current stock must be zero or positive."
        ),
        error_messages={"required": "The current_stock field is required."}
    )

    # Code field: required, string length between 1 and 10
    code = fields.Str(
        required=True,
        validate=validate.Length(
            min=1,
            max=20,
            error="Code must be between 1 and 20 characters."
        ),
        error_messages={"required": "The code field is required."}
    )