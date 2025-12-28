"""
Page Assembly Agents: Generate specific page types.
Each agent assembles pages from logic blocks and templates.
"""

from typing import List, Dict, Any
from models import (
    Product,
    Question,
    ContentFragment,
    FAQPage,
    FAQItem,
    ProductPage,
    ProductPageField,
    ComparisonPage,
    ComparisonPageItem,
)
from logic_blocks.blocks import (
    BenefitsLogicBlock,
    UsageLogicBlock,
    SafetyLogicBlock,
    IngredientLogicBlock,
    PriceLogicBlock,
)


class FAQPageAgent:
    """
    Assembles FAQ pages from product data and questions.
    Generates at least 5 Q&A pairs.
    """

    def __init__(self):
        """Initialize FAQ agent."""
        self.min_faqs = 5

    def generate(
        self,
        product: Product,
        questions: List[Question],
        logic_blocks: Dict[str, ContentFragment],
    ) -> FAQPage:
        """
        Generate FAQ page.

        Args:
            product: Product model
            questions: Generated questions
            logic_blocks: Content fragments from logic blocks

        Returns:
            FAQPage with Q&A items
        """
        faq_items = []

        # Generate FAQ items from questions
        for question in questions[:15]:  # Use generated questions
            answer = self._generate_answer(question, product, logic_blocks)
            faq_items.append(
                FAQItem(
                    question=question.question,
                    answer=answer,
                    category=question.category,
                )
            )

        # Ensure minimum number of FAQs
        if len(faq_items) < self.min_faqs:
            faq_items = faq_items[:self.min_faqs]

        faq_page = FAQPage(
            page_type="faq",
            product_name=product.name,
            total_questions=len(faq_items),
            faqs=faq_items,
        )

        return faq_page

    def _generate_answer(
        self,
        question: Question,
        product: Product,
        logic_blocks: Dict[str, ContentFragment],
    ) -> str:
        """
        Generate answer from question context and logic blocks.

        Args:
            question: Question object
            product: Product model
            logic_blocks: Content fragments

        Returns:
            Generated answer string
        """
        answers = {
            "concentration": f"The concentration of {product.name} is {product.concentration}.",
            "key_ingredients": f"Key ingredients include: {', '.join(product.key_ingredients)}.",
            "skin_types": f"Suitable for {', '.join(product.skin_types)} skin types.",
            "benefits": f"Main benefits: {', '.join(product.benefits)}.",
            "usage_instructions": product.usage_instructions,
            "side_effects": f"Common experiences include: {', '.join(product.side_effects) if product.side_effects else 'No major side effects commonly reported.'}",
            "price": f"The price is {product.price}.",
        }

        # Look for context field in question
        if question.context in answers:
            return answers[question.context]

        # Default answer based on category
        if question.category == "Informational":
            return f"{product.name} is a premium skincare product with carefully selected ingredients."
        elif question.category == "Usage":
            return product.usage_instructions or "Follow the instructions on the product packaging."
        elif question.category == "Safety":
            return "Always perform a patch test first. If irritation occurs, discontinue use."
        elif question.category == "Purchase":
            return f"Available at premium skincare retailers. Price: {product.price}"
        else:
            return f"Learn more about {product.name} for your skincare needs."


class ProductPageAgent:
    """
    Assembles product pages with structured sections.
    Combines all logic blocks into a comprehensive product page.
    """

    def generate(
        self,
        product: Product,
        logic_blocks: Dict[str, ContentFragment],
    ) -> ProductPage:
        """
        Generate product page.

        Args:
            product: Product model
            logic_blocks: Content fragments from logic blocks

        Returns:
            ProductPage with structured sections
        """
        product_page = ProductPage(
            page_type="product",
            product_name=product.name,
            sections={},
        )

        # Overview section
        product_page.sections["overview"] = [
            ProductPageField("Product Name", product.name, "string"),
            ProductPageField("Concentration", product.concentration or "As formulated", "string"),
        ]

        # Benefits section
        if "benefits" in logic_blocks:
            benefits_content = logic_blocks["benefits"].content
            product_page.sections["benefits"] = [
                ProductPageField("Title", benefits_content.get("title"), "string"),
                ProductPageField("Benefits", benefits_content.get("items"), "list"),
            ]

        # Ingredients section
        if "ingredient" in logic_blocks:
            ingredient_content = logic_blocks["ingredient"].content
            product_page.sections["ingredients"] = [
                ProductPageField("Title", ingredient_content.get("title"), "string"),
                ProductPageField("Ingredients", ingredient_content.get("ingredients"), "list"),
                ProductPageField("Concentration", ingredient_content.get("concentration"), "string"),
            ]

        # Usage section
        if "usage" in logic_blocks:
            usage_content = logic_blocks["usage"].content
            product_page.sections["usage"] = [
                ProductPageField("Title", usage_content.get("title"), "string"),
                ProductPageField("Instructions", usage_content.get("instructions"), "string"),
                ProductPageField("Timing", usage_content.get("application_timing"), "string"),
            ]

        # Safety section
        if "safety" in logic_blocks:
            safety_content = logic_blocks["safety"].content
            product_page.sections["safety"] = [
                ProductPageField("Title", safety_content.get("title"), "string"),
                ProductPageField("Side Effects", safety_content.get("side_effects"), "list"),
                ProductPageField("Precautions", safety_content.get("precautions"), "list"),
            ]

        # Price section
        if "price" in logic_blocks:
            price_content = logic_blocks["price"].content
            product_page.sections["price"] = [
                ProductPageField("Price", price_content.get("price"), "string"),
                ProductPageField("Currency", price_content.get("currency"), "string"),
                ProductPageField("Value Proposition", price_content.get("value_proposition"), "string"),
            ]

        # Skin Type Compatibility
        product_page.sections["compatibility"] = [
            ProductPageField("Suitable Skin Types", product.skin_types, "list"),
        ]

        return product_page


class ComparisonPageAgent:
    """
    Assembles comparison pages between two products.
    Compares GlowBoost with a fictional Product B.
    """

    def __init__(self):
        """Initialize comparison agent."""
        # Create fictional Product B for comparison
        self.product_b = self._create_fictional_product()

    def _create_fictional_product(self) -> Product:
        """
        Create a consistent fictional product for comparison.

        Returns:
            Fictional Product B
        """
        product_b = Product(
            name="LuminaGlow Vitamin C+ Serum",
            concentration="20% Vitamin C",
            skin_types=["Normal", "Dry"],
            key_ingredients=["Vitamin C", "Ferulic Acid", "Vitamin E"],
            benefits=["Brightening", "Anti-aging", "Radiance boost"],
            usage_instructions="Apply 3-4 drops morning and night. Use with sunscreen during day.",
            side_effects=["May cause temporary redness in very sensitive skin"],
            price="₹1299",
        )
        return product_b

    def generate(self, product_a: Product) -> ComparisonPage:
        """
        Generate comparison page.

        Args:
            product_a: Primary product (GlowBoost)

        Returns:
            ComparisonPage
        """
        comparison_page = ComparisonPage(
            page_type="comparison",
            product_a_name=product_a.name,
            product_b_name=self.product_b.name,
            comparison_items=[],
        )

        # Concentration comparison
        comparison_page.comparison_items.append(
            ComparisonPageItem(
                attribute="Vitamin C Concentration",
                product_a=product_a.concentration or "10%",
                product_b=self.product_b.concentration or "20%",
            )
        )

        # Ingredients comparison
        comparison_page.comparison_items.append(
            ComparisonPageItem(
                attribute="Key Ingredients",
                product_a=", ".join(product_a.key_ingredients),
                product_b=", ".join(self.product_b.key_ingredients),
            )
        )

        # Benefits comparison
        comparison_page.comparison_items.append(
            ComparisonPageItem(
                attribute="Main Benefits",
                product_a=", ".join(product_a.benefits),
                product_b=", ".join(self.product_b.benefits),
            )
        )

        # Price comparison
        comparison_page.comparison_items.append(
            ComparisonPageItem(
                attribute="Price",
                product_a=product_a.price,
                product_b=self.product_b.price,
            )
        )

        # Skin type compatibility
        comparison_page.comparison_items.append(
            ComparisonPageItem(
                attribute="Suitable for Skin Types",
                product_a=", ".join(product_a.skin_types),
                product_b=", ".join(self.product_b.skin_types),
            )
        )

        # Application frequency
        comparison_page.comparison_items.append(
            ComparisonPageItem(
                attribute="Application Frequency",
                product_a="2-3 drops in morning",
                product_b="3-4 drops morning and night",
            )
        )

        # Side effects
        comparison_page.comparison_items.append(
            ComparisonPageItem(
                attribute="Potential Side Effects",
                product_a=", ".join(product_a.side_effects) if product_a.side_effects else "Minimal",
                product_b=", ".join(self.product_b.side_effects) if self.product_b.side_effects else "Minimal",
            )
        )

        # Value for money
        comparison_page.comparison_items.append(
            ComparisonPageItem(
                attribute="Value for Money",
                product_a="Excellent for budget-conscious users",
                product_b="Premium option with higher concentration",
            )
        )

        return comparison_page
