"""
Logic Blocks: Reusable content transformation components.
Each block transforms product data into structured content fragments.
"""

from typing import Dict, Any, List
from models import Product, ContentFragment


class BenefitsLogicBlock:
    """Transforms product benefits into structured content."""

    @staticmethod
    def generate(product: Product) -> ContentFragment:
        """
        Generate benefits content fragment.

        Args:
            product: Product model

        Returns:
            ContentFragment with benefits content
        """
        benefits_content = {
            "title": f"{product.name} Benefits",
            "items": product.benefits,
            "description": f"Experience {len(product.benefits)} key benefits with {product.name}",
            "highlighted_benefits": product.benefits[:2] if len(product.benefits) >= 2 else product.benefits,
        }

        return ContentFragment(
            block_type="benefits",
            content=benefits_content,
            product_name=product.name,
        )


class UsageLogicBlock:
    """Transforms usage instructions into structured content."""

    @staticmethod
    def generate(product: Product) -> ContentFragment:
        """
        Generate usage content fragment.

        Args:
            product: Product model

        Returns:
            ContentFragment with usage content
        """
        # Parse usage instructions into steps
        steps = [step.strip() for step in product.usage_instructions.split("\n") if step.strip()]
        if not steps and product.usage_instructions:
            steps = [product.usage_instructions]

        usage_content = {
            "title": f"How to Use {product.name}",
            "instructions": product.usage_instructions,
            "steps": steps,
            "frequency": "Daily",  # Inferred from usage instructions
            "application_timing": "Morning before sunscreen" if "morning" in product.usage_instructions.lower() else "As directed",
        }

        return ContentFragment(
            block_type="usage",
            content=usage_content,
            product_name=product.name,
        )


class SafetyLogicBlock:
    """Transforms safety information into structured content."""

    @staticmethod
    def generate(product: Product) -> ContentFragment:
        """
        Generate safety content fragment.

        Args:
            product: Product model

        Returns:
            ContentFragment with safety content
        """
        safety_content = {
            "title": f"Safety Information for {product.name}",
            "side_effects": product.side_effects,
            "warning": "Test on a small area first if you have sensitive skin",
            "precautions": [
                "Perform a patch test before full application",
                "Use sunscreen when using Vitamin C serums",
                "Avoid mixing with certain acids initially",
            ],
            "mild_side_effects": product.side_effects if product.side_effects else ["None commonly reported"],
        }

        return ContentFragment(
            block_type="safety",
            content=safety_content,
            product_name=product.name,
        )


class IngredientLogicBlock:
    """Transforms ingredient information into structured content."""

    @staticmethod
    def generate(product: Product) -> ContentFragment:
        """
        Generate ingredient content fragment.

        Args:
            product: Product model

        Returns:
            ContentFragment with ingredient content
        """
        ingredients_content = {
            "title": f"Key Ingredients in {product.name}",
            "ingredients": product.key_ingredients,
            "concentration": product.concentration or "As formulated",
            "ingredient_count": len(product.key_ingredients),
            "ingredient_descriptions": {
                "Vitamin C": "Powerful antioxidant for brightening and skin radiance",
                "Hyaluronic Acid": "Hydration booster that plumps and moisturizes skin",
            },
        }

        return ContentFragment(
            block_type="ingredient",
            content=ingredients_content,
            product_name=product.name,
        )


class PriceLogicBlock:
    """Transforms price information into structured content."""

    @staticmethod
    def generate(product: Product) -> ContentFragment:
        """
        Generate price content fragment.

        Args:
            product: Product model

        Returns:
            ContentFragment with price content
        """
        # Extract numeric price for comparison
        price_numeric = "".join(filter(str.isdigit, product.price.split()[0] if product.price else "0"))

        price_numeric_val = int(price_numeric) if price_numeric else 0
        
        price_content = {
            "title": f"Pricing for {product.name}",
            "price": product.price,
            "price_numeric": price_numeric_val,
            "currency": "INR" if "₹" in product.price else "USD",
            "value_proposition": "Premium quality at accessible pricing",
            "price_range": "Mid-range premium" if price_numeric_val > 500 else "Affordable",
        }

        return ContentFragment(
            block_type="price",
            content=price_content,
            product_name=product.name,
        )


class ComparisonLogicBlock:
    """Generates comparison content between two products."""

    @staticmethod
    def generate(product_a: Product, product_b: Product) -> ContentFragment:
        """
        Generate comparison content fragment.

        Args:
            product_a: First product
            product_b: Second product

        Returns:
            ContentFragment with comparison content
        """
        comparison_content = {
            "title": f"{product_a.name} vs {product_b.name}",
            "product_a": {
                "name": product_a.name,
                "concentration": product_a.concentration,
                "benefits": product_a.benefits,
                "price": product_a.price,
                "skin_types": product_a.skin_types,
            },
            "product_b": {
                "name": product_b.name,
                "concentration": product_b.concentration,
                "benefits": product_b.benefits,
                "price": product_b.price,
                "skin_types": product_b.skin_types,
            },
            "comparison_metrics": [
                {
                    "metric": "Concentration",
                    "product_a": product_a.concentration or "N/A",
                    "product_b": product_b.concentration or "N/A",
                },
                {
                    "metric": "Price",
                    "product_a": product_a.price,
                    "product_b": product_b.price,
                },
                {
                    "metric": "Suitable Skin Types",
                    "product_a": ", ".join(product_a.skin_types),
                    "product_b": ", ".join(product_b.skin_types),
                },
            ],
        }

        return ContentFragment(
            block_type="comparison",
            content=comparison_content,
            product_name=f"{product_a.name} and {product_b.name}",
        )
