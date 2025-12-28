"""
TemplateEngineAgent: Manages structured template definitions.
Templates define required fields, formatting rules, and logic block dependencies.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable
from models import ContentFragment


@dataclass
class TemplateField:
    """Defines a single field in a template."""
    name: str
    required: bool = True
    data_type: str = "string"  # string, list, dict, number
    formatter: Callable[[Any], Any] = field(default=lambda x: x)


@dataclass
class TemplateDefinition:
    """
    Structured template definition.
    Defines required fields, formatting rules, and dependencies.
    """
    name: str
    page_type: str
    required_fields: List[TemplateField]
    required_logic_blocks: List[str]  # List of block types needed
    sections: Dict[str, List[str]] = field(default_factory=dict)  # Section -> fields mapping

    def validate_content(self, content: Dict[str, Any]) -> bool:
        """
        Validate that content matches template requirements.

        Args:
            content: Content dictionary

        Returns:
            True if valid, raises exception otherwise
        """
        for field in self.required_fields:
            if field.required and field.name not in content:
                raise ValueError(f"Required field missing: {field.name}")
        return True


class TemplateEngineAgent:
    """
    Template engine that manages and applies template definitions.
    No business logic - only template management.
    """

    def __init__(self):
        """Initialize with predefined templates."""
        self.templates: Dict[str, TemplateDefinition] = {}
        self._register_templates()

    def _register_templates(self) -> None:
        """Register all available templates."""
        # FAQ Template
        faq_template = TemplateDefinition(
            name="FAQ Page Template",
            page_type="faq",
            required_fields=[
                TemplateField("page_type", required=True),
                TemplateField("product_name", required=True),
                TemplateField("total_questions", required=True, data_type="number"),
                TemplateField("faqs", required=True, data_type="list"),
            ],
            required_logic_blocks=["benefits", "usage", "safety", "ingredient"],
            sections={
                "meta": ["page_type", "product_name", "total_questions"],
                "content": ["faqs"],
            },
        )
        self.templates["faq"] = faq_template

        # Product Page Template
        product_template = TemplateDefinition(
            name="Product Page Template",
            page_type="product",
            required_fields=[
                TemplateField("page_type", required=True),
                TemplateField("product_name", required=True),
                TemplateField("sections", required=True, data_type="dict"),
            ],
            required_logic_blocks=["benefits", "usage", "safety", "ingredient", "price"],
            sections={
                "meta": ["page_type", "product_name"],
                "content": ["sections"],
            },
        )
        self.templates["product"] = product_template

        # Comparison Page Template
        comparison_template = TemplateDefinition(
            name="Comparison Page Template",
            page_type="comparison",
            required_fields=[
                TemplateField("page_type", required=True),
                TemplateField("product_a_name", required=True),
                TemplateField("product_b_name", required=True),
                TemplateField("comparison_items", required=True, data_type="list"),
            ],
            required_logic_blocks=["comparison"],
            sections={
                "meta": ["page_type", "product_a_name", "product_b_name"],
                "content": ["comparison_items"],
            },
        )
        self.templates["comparison"] = comparison_template

    def get_template(self, template_type: str) -> TemplateDefinition:
        """
        Retrieve a template by type.

        Args:
            template_type: Type of template (faq, product, comparison)

        Returns:
            TemplateDefinition

        Raises:
            KeyError: If template not found
        """
        if template_type not in self.templates:
            raise KeyError(f"Template not found: {template_type}")
        return self.templates[template_type]

    def list_templates(self) -> List[str]:
        """List all available template types."""
        return list(self.templates.keys())

    def validate_against_template(
        self,
        template_type: str,
        content: Dict[str, Any],
    ) -> bool:
        """
        Validate content against a template.

        Args:
            template_type: Type of template
            content: Content to validate

        Returns:
            True if valid
        """
        template = self.get_template(template_type)
        return template.validate_content(content)

    def get_required_blocks(self, template_type: str) -> List[str]:
        """
        Get required logic blocks for a template.

        Args:
            template_type: Type of template

        Returns:
            List of required block types
        """
        template = self.get_template(template_type)
        return template.required_logic_blocks
