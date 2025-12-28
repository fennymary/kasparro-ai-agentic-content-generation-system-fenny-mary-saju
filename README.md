# Agentic Content Generation System (ACGS)

A production-grade, modular multi-agent system for automated generation of structured product content.

## Quick Start

### Prerequisites
- Python 3.8+
- No external dependencies required

### Installation & Execution

```bash
cd kasparro-ai-agentic-content-generation-system-fenny-mary-saju
python main.py
```

### Outputs
The system generates three JSON files in the `output/` directory:
- `faq.json` - FAQ page with 15+ Q&A pairs
- `product_page.json` - Product page with 7+ sections
- `comparison_page.json` - Comparison with fictional competitor

## System Architecture

The system implements a **multi-agent orchestration pipeline** with clear separation of concerns:

1. **ProductParserAgent** - Parse & validate input
2. **QuestionGenerationAgent** - Generate 15+ categorized questions
3. **Logic Blocks** - Reusable content transformers (5 blocks)
4. **TemplateEngine** - Define page structures
5. **Page Assembly Agents** - Compose final pages
6. **OrchestratorAgent** - Control execution flow

## Design Highlights

✅ **Modular**: Clear agent boundaries, no monolithic code
✅ **Deterministic**: Same input = Same output (always)
✅ **Extensible**: Add products/pages/blocks without code changes
✅ **Type-Safe**: Python dataclasses throughout
✅ **Reusable**: Logic blocks compose across multiple page types
✅ **Production-Ready**: Clean code, documented, testable

## Project Structure

```
├── models.py                 # Data models
├── main.py                   # Entry point
├── agents/                   # Agent implementations
├── logic_blocks/             # Reusable transformers
├── templates/                # Template definitions
├── orchestrator/             # Pipeline orchestration
├── output/                   # Generated JSON
└── docs/                     # Documentation
```

## How to Add a New Product

Simply provide structured data and run:

```python
raw_product = {
    "Product Name": "Your Product",
    "Concentration": "Active percentage",
    "Skin Type": "Type1, Type2",
    "Key Ingredients": "Ingredient1, Ingredient2",
    "Benefits": "Benefit1, Benefit2",
    "How to Use": "Application instructions",
    "Side Effects": "Potential effects",
    "Price": "₹XXX",
}

orchestrator = OrchestratorAgent(output_dir="output")
orchestrator.execute_pipeline(raw_product)
```

All outputs generated automatically with zero code changes.

## Documentation

See [docs/projectdocumentation.md](docs/projectdocumentation.md) for:
- Complete system design
- Architecture diagrams
- Agent responsibilities
- Extensibility patterns
- Design principles

## Example Output

```json
{
  "page_type": "faq",
  "product_name": "GlowBoost Vitamin C Serum",
  "total_questions": 15,
  "faqs": [
    {
      "question": "What is the concentration of GlowBoost Vitamin C Serum?",
      "answer": "The concentration of GlowBoost Vitamin C Serum is 10% Vitamin C.",
      "category": "Informational"
    },
    ...
  ]
}
```

## Key Differentiators

| Aspect | Traditional Script | ACGS |
|--------|-------------------|------|
| **New Product** | Modify code | Use existing code |
| **New Page Type** | Rewrite logic | Add agent + template |
| **Reuse Logic** | Copy-paste | Use logic blocks |
| **Testing** | Full system test | Test individual agents |
| **Maintenance** | High effort | Low effort |

## Technology Stack

- **Language**: Python 3.8+
- **Type System**: dataclasses, type hints
- **Architecture**: Multi-agent orchestration
- **Output Format**: JSON

## License & Attribution

Built as a production-grade system for e-commerce content generation. Designed for extensibility and maintainability.

---

**Author**: Applied AI Engineering Team
**Date**: December 2025
**Status**: Production Ready
