"""
QuestionGenerationAgent: Generates categorized user questions.
Responsibility: Generate user questions from product data.
Input: Product model
Output: List of categorized questions
"""

from typing import List, Dict
from models import Product, Question


class QuestionGenerationAgent:
    """
    Generates at least 15 user questions across 5 categories.
    Categories: Informational, Usage, Safety, Purchase, Comparison
    """

    def __init__(self):
        """Initialize with question templates."""
        self.min_questions = 15
        self.categories = [
            "Informational",
            "Usage",
            "Safety",
            "Purchase",
            "Comparison",
        ]

    def generate(self, product: Product) -> List[Question]:
        """
        Generate categorized questions for product.

        Args:
            product: Validated product model

        Returns:
            List of Question objects
        """
        questions: List[Question] = []

        # Informational questions (3-4)
        questions.extend(self._generate_informational_questions(product))

        # Usage questions (3-4)
        questions.extend(self._generate_usage_questions(product))

        # Safety questions (3-4)
        questions.extend(self._generate_safety_questions(product))

        # Purchase questions (3-4)
        questions.extend(self._generate_purchase_questions(product))

        # Comparison questions (2-3)
        questions.extend(self._generate_comparison_questions(product))

        return questions

    def _generate_informational_questions(self, product: Product) -> List[Question]:
        """Generate informational questions about the product."""
        questions = []

        questions.append(
            Question(
                category="Informational",
                question=f"What is the concentration of {product.name}?",
                context="concentration",
            )
        )

        questions.append(
            Question(
                category="Informational",
                question=f"What are the key ingredients in {product.name}?",
                context="key_ingredients",
            )
        )

        questions.append(
            Question(
                category="Informational",
                question=f"What skin types is {product.name} suitable for?",
                context="skin_types",
            )
        )

        questions.append(
            Question(
                category="Informational",
                question=f"What are the main benefits of {product.name}?",
                context="benefits",
            )
        )

        return questions

    def _generate_usage_questions(self, product: Product) -> List[Question]:
        """Generate usage-related questions."""
        questions = []

        questions.append(
            Question(
                category="Usage",
                question=f"How do I use {product.name}?",
                context="usage_instructions",
            )
        )

        questions.append(
            Question(
                category="Usage",
                question=f"When should I apply {product.name} in my skincare routine?",
                context="usage_instructions",
            )
        )

        questions.append(
            Question(
                category="Usage",
                question=f"How many drops of {product.name} should I use per application?",
                context="usage_instructions",
            )
        )

        questions.append(
            Question(
                category="Usage",
                question=f"Can I use {product.name} both morning and night?",
                context="usage_instructions",
            )
        )

        return questions

    def _generate_safety_questions(self, product: Product) -> List[Question]:
        """Generate safety-related questions."""
        questions = []

        questions.append(
            Question(
                category="Safety",
                question=f"What are the side effects of {product.name}?",
                context="side_effects",
            )
        )

        questions.append(
            Question(
                category="Safety",
                question=f"Is {product.name} safe for sensitive skin?",
                context="side_effects",
            )
        )

        questions.append(
            Question(
                category="Safety",
                question=f"Can I use {product.name} with other active ingredients?",
                context="side_effects",
            )
        )

        questions.append(
            Question(
                category="Safety",
                question=f"Are there any contraindications or interactions with {product.name}?",
                context="side_effects",
            )
        )

        return questions

    def _generate_purchase_questions(self, product: Product) -> List[Question]:
        """Generate purchase-related questions."""
        questions = []

        questions.append(
            Question(
                category="Purchase",
                question=f"What is the price of {product.name}?",
                context="price",
            )
        )

        questions.append(
            Question(
                category="Purchase",
                question=f"Is {product.name} value for money?",
                context="price",
            )
        )

        questions.append(
            Question(
                category="Purchase",
                question=f"Where can I purchase {product.name}?",
                context="price",
            )
        )

        questions.append(
            Question(
                category="Purchase",
                question=f"Does {product.name} offer a money-back guarantee?",
                context="price",
            )
        )

        return questions

    def _generate_comparison_questions(self, product: Product) -> List[Question]:
        """Generate comparison-related questions."""
        questions = []

        questions.append(
            Question(
                category="Comparison",
                question=f"How does {product.name} compare to other vitamin C serums?",
                context="benefits",
            )
        )

        questions.append(
            Question(
                category="Comparison",
                question=f"Is {product.name} better than alternative products?",
                context="concentration",
            )
        )

        questions.append(
            Question(
                category="Comparison",
                question=f"What makes {product.name} unique in the market?",
                context="key_ingredients",
            )
        )

        return questions
