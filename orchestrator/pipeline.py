"""
OrchestratorAgent: Controls pipeline execution.
Responsibility: Orchestration only - no business logic.
Manages execution order and passes outputs between agents.
"""

import json
from typing import Dict, Any
from pathlib import Path

from agents.parser_agent import ProductParserAgent
from agents.question_agent import QuestionGenerationAgent
from agents.page_agents import FAQPageAgent, ProductPageAgent, ComparisonPageAgent
from logic_blocks.blocks import (
    BenefitsLogicBlock,
    UsageLogicBlock,
    SafetyLogicBlock,
    IngredientLogicBlock,
    PriceLogicBlock,
)
from templates.template_engine import TemplateEngineAgent


class OrchestratorAgent:
    """
    Orchestrates the entire content generation pipeline.
    Controls execution order and data flow between agents.
    Contains no business logic.
    """

    def __init__(self, output_dir: str = "output"):
        """
        Initialize orchestrator.

        Args:
            output_dir: Directory for JSON outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize all agents
        self.parser_agent = ProductParserAgent()
        self.question_agent = QuestionGenerationAgent()
        self.template_engine = TemplateEngineAgent()
        self.faq_agent = FAQPageAgent()
        self.product_page_agent = ProductPageAgent()
        self.comparison_agent = ComparisonPageAgent()

    def execute_pipeline(self, raw_product: Dict[str, Any]) -> None:
        """
        Execute the complete pipeline.

        Pipeline flow:
        1. Parse and validate product data
        2. Generate questions from product
        3. Generate logic blocks
        4. Assemble pages (FAQ, Product, Comparison)
        5. Save outputs to JSON

        Args:
            raw_product: Raw product dictionary
        """
        print("=" * 80)
        print("ORCHESTRATOR: Starting Content Generation Pipeline")
        print("=" * 80)

        # Step 1: Parse product
        print("\n[STEP 1] ProductParserAgent: Parsing and validating product data...")
        product = self.parser_agent.parse(raw_product)
        print(f"[OK] Product parsed: {product.name}")

        # Step 2: Generate questions
        print("\n[STEP 2] QuestionGenerationAgent: Generating questions...")
        questions = self.question_agent.generate(product)
        print(f"[OK] Generated {len(questions)} questions across {self.question_agent.categories}")
        for q in questions[:3]:
            print(f"  - [{q.category}] {q.question}")
        print(f"  ... and {len(questions) - 3} more questions")

        # Step 3: Generate logic blocks
        print("\n[STEP 3] Logic Blocks: Generating content fragments...")
        logic_blocks = self._generate_logic_blocks(product)
        print(f"[OK] Generated {len(logic_blocks)} logic blocks")
        for block_name in logic_blocks.keys():
            print(f"  - {block_name}")

        # Step 4: Generate FAQ page
        print("\n[STEP 4] FAQPageAgent: Assembling FAQ page...")
        faq_page = self.faq_agent.generate(product, questions, logic_blocks)
        self._save_output("faq.json", faq_page.to_dict())
        print(f"[OK] FAQ page generated with {faq_page.total_questions} Q&A pairs")

        # Step 5: Generate product page
        print("\n[STEP 5] ProductPageAgent: Assembling product page...")
        product_page = self.product_page_agent.generate(product, logic_blocks)
        self._save_output("product_page.json", product_page.to_dict())
        print(f"[OK] Product page generated with {len(product_page.sections)} sections")

        # Step 6: Generate comparison page
        print("\n[STEP 6] ComparisonPageAgent: Assembling comparison page...")
        comparison_page = self.comparison_agent.generate(product)
        self._save_output("comparison_page.json", comparison_page.to_dict())
        print(f"[OK] Comparison page generated ({product.name} vs {comparison_page.product_b_name})")

        print("\n" + "=" * 80)
        print("ORCHESTRATOR: Pipeline Complete")
        print(f"Outputs saved to: {self.output_dir}")
        print("=" * 80)

    def _generate_logic_blocks(self, product) -> Dict[str, Any]:
        """
        Generate all logic blocks.

        Args:
            product: Parsed product model

        Returns:
            Dictionary of block_name -> ContentFragment
        """
        logic_blocks = {}

        # Generate each logic block
        logic_blocks["benefits"] = BenefitsLogicBlock.generate(product)
        logic_blocks["usage"] = UsageLogicBlock.generate(product)
        logic_blocks["safety"] = SafetyLogicBlock.generate(product)
        logic_blocks["ingredient"] = IngredientLogicBlock.generate(product)
        logic_blocks["price"] = PriceLogicBlock.generate(product)

        return logic_blocks

    def _save_output(self, filename: str, data: Dict[str, Any]) -> None:
        """
        Save output to JSON file.

        Args:
            filename: Output filename
            data: Data to save
        """
        output_path = self.output_dir / filename
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
