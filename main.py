"""
Main entry point for the agentic content generation system.
Executes the pipeline with sample product data.
"""

from orchestrator.pipeline import OrchestratorAgent


def main():
    """
    Main function: Execute the content generation pipeline.
    """

    # Product data - ONLY SOURCE OF TRUTH
    raw_product_data = {
        "Product Name": "GlowBoost Vitamin C Serum",
        "Concentration": "10% Vitamin C",
        "Skin Type": "Oily, Combination",
        "Key Ingredients": "Vitamin C, Hyaluronic Acid",
        "Benefits": "Brightening, Fades dark spots",
        "How to Use": "Apply 2–3 drops in the morning before sunscreen",
        "Side Effects": "Mild tingling for sensitive skin",
        "Price": "₹699",
    }

    # Initialize and execute orchestrator
    orchestrator = OrchestratorAgent(output_dir="output")
    orchestrator.execute_pipeline(raw_product_data)


if __name__ == "__main__":
    main()
