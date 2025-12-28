"""
Data models and type definitions for the agentic content generation system.
Ensures type safety and clear contracts between agents.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Product:
    """
    Validated internal product model.
    Single source of truth after parsing.
    """
    name: str
    concentration: Optional[str] = None
    skin_types: List[str] = field(default_factory=list)
    key_ingredients: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    usage_instructions: str = ""
    side_effects: List[str] = field(default_factory=list)
    price: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "concentration": self.concentration,
            "skin_types": self.skin_types,
            "key_ingredients": self.key_ingredients,
            "benefits": self.benefits,
            "usage_instructions": self.usage_instructions,
            "side_effects": self.side_effects,
            "price": self.price,
        }


@dataclass
class Question:
    """
    Represents a single Q&A item with category.
    """
    category: str  # Informational, Usage, Safety, Purchase, Comparison
    question: str
    context: str  # Source field from product data


@dataclass
class ContentFragment:
    """
    Output from a logic block.
    Reusable content building block.
    """
    block_type: str  # benefits, usage, safety, etc.
    content: Dict[str, Any]
    product_name: str


@dataclass
class FAQItem:
    """Single FAQ entry."""
    question: str
    answer: str
    category: str


@dataclass
class FAQPage:
    """FAQ page structure."""
    page_type: str = "faq"
    product_name: str = ""
    total_questions: int = 0
    faqs: List[FAQItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_type": self.page_type,
            "product_name": self.product_name,
            "total_questions": self.total_questions,
            "faqs": [
                {
                    "question": faq.question,
                    "answer": faq.answer,
                    "category": faq.category,
                }
                for faq in self.faqs
            ],
        }


@dataclass
class ProductPageField:
    """Single field in product page."""
    label: str
    value: Any
    data_type: str


@dataclass
class ProductPage:
    """Product page structure."""
    page_type: str = "product"
    product_name: str = ""
    sections: Dict[str, List[ProductPageField]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_type": self.page_type,
            "product_name": self.product_name,
            "sections": {
                section_name: [
                    {"label": field.label, "value": field.value, "data_type": field.data_type}
                    for field in fields
                ]
                for section_name, fields in self.sections.items()
            },
        }


@dataclass
class ComparisonPageItem:
    """Single comparison item."""
    attribute: str
    product_a: str
    product_b: str


@dataclass
class ComparisonPage:
    """Comparison page structure."""
    page_type: str = "comparison"
    product_a_name: str = ""
    product_b_name: str = ""
    comparison_items: List[ComparisonPageItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_type": self.page_type,
            "product_a_name": self.product_a_name,
            "product_b_name": self.product_b_name,
            "comparison_items": [
                {
                    "attribute": item.attribute,
                    "product_a": item.product_a,
                    "product_b": item.product_b,
                }
                for item in self.comparison_items
            ],
        }
