"""
ProductParserAgent: Parses and validates raw product data.
Responsibility: Normalization, schema enforcement, validation.
Input: Raw product dictionary
Output: Validated Product model
"""

from typing import Dict, Any, List
from models import Product


class ProductParserAgent:
    """
    Parses raw product dictionary into validated Product model.
    Enforces schema, normalizes data, validates constraints.
    """

    def __init__(self):
        """Initialize parser with validation rules."""
        self.required_fields = ["name"]
        self.optional_fields = [
            "concentration",
            "skin_types",
            "key_ingredients",
            "benefits",
            "usage_instructions",
            "side_effects",
            "price",
        ]

    def parse(self, raw_product: Dict[str, Any]) -> Product:
        """
        Parse and validate raw product data.

        Args:
            raw_product: Dictionary containing product data

        Returns:
            Validated Product model

        Raises:
            ValueError: If required fields missing or invalid
        """
        # Validate required fields
        self._validate_required_fields(raw_product)

        # Extract and normalize data with flexible field name matching
        product = Product(
            name=self._get_field(raw_product, ["name", "Name", "Product Name", "product_name"]),
            concentration=self._get_field(raw_product, ["concentration", "Concentration"]),
            skin_types=self._normalize_list_field(raw_product, ["skin_types", "Skin Type", "skin type"]),
            key_ingredients=self._normalize_list_field(raw_product, ["key_ingredients", "Key Ingredients"]),
            benefits=self._normalize_list_field(raw_product, ["benefits", "Benefits"]),
            usage_instructions=self._get_field(raw_product, ["usage_instructions", "How to Use", "how to use"]),
            side_effects=self._normalize_list_field(raw_product, ["side_effects", "Side Effects"]),
            price=self._get_field(raw_product, ["price", "Price"]),
        )

        return product

    def _get_field(self, data: Dict[str, Any], possible_keys: List[str]) -> str:
        """
        Get a field from dictionary using multiple possible key names.

        Args:
            data: Dictionary to search
            possible_keys: List of possible key names

        Returns:
            Normalized string value or empty string
        """
        for key in possible_keys:
            if key in data:
                return self._normalize_string(data[key])
        return ""

    def _normalize_list_field(self, data: Dict[str, Any], possible_keys: List[str]) -> List[str]:
        """
        Get and normalize a list field using multiple possible key names.

        Args:
            data: Dictionary to search
            possible_keys: List of possible key names

        Returns:
            Normalized list
        """
        for key in possible_keys:
            if key in data:
                return self._normalize_list(data[key])
        return []

    def _validate_required_fields(self, data: Dict[str, Any]) -> None:
        """
        Validate that required fields are present.

        Args:
            data: Product data dictionary

        Raises:
            ValueError: If required fields missing
        """
        # Check for product name field in various formats
        has_name = any(
            key in data for key in ["name", "Name", "Product Name", "product_name"]
        )
        if not has_name:
            raise ValueError("Required field missing: product name")

    def _normalize_string(self, value: Any) -> str:
        """Normalize string values."""
        if value is None:
            return ""
        return str(value).strip()

    def _normalize_list(self, primary: Any, secondary: Any = None) -> List[str]:
        """
        Normalize list values from primary or secondary source.
        Handles both list and comma-separated string formats.
        """
        # Use primary if available, otherwise secondary
        source = primary if primary else secondary

        if not source:
            return []

        # If already a list, process it
        if isinstance(source, list):
            return [self._normalize_string(item) for item in source]

        # If string, split by comma
        if isinstance(source, str):
            return [self._normalize_string(item) for item in source.split(",")]

        return []
