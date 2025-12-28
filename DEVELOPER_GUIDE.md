# Developer Quick Reference

## System Architecture at a Glance

```
Raw Product Data
       ↓
[ProductParserAgent] → Validated Product
       ↓
[QuestionGenerationAgent] → 15+ Questions
       ↓
[Logic Blocks] (5 blocks) → Content Fragments
       ↓
[TemplateEngine] → Structure Definition
       ↓
[Page Agents] → FAQ, Product, Comparison Pages
       ↓
JSON Outputs (3 files)
```

## Agent Responsibilities

| Agent | File | Input | Output | Purpose |
|-------|------|-------|--------|---------|
| ProductParserAgent | agents/parser_agent.py | Dict | Product | Parse & validate |
| QuestionGenerationAgent | agents/question_agent.py | Product | List[Question] | Generate Q&A |
| FAQPageAgent | agents/page_agents.py | Product, Questions, Blocks | FAQPage | Assemble FAQ |
| ProductPageAgent | agents/page_agents.py | Product, Blocks | ProductPage | Assemble product |
| ComparisonPageAgent | agents/page_agents.py | Product | ComparisonPage | Create comparison |
| OrchestratorAgent | orchestrator/pipeline.py | Raw data | JSON outputs | Coordinate flow |

## Logic Blocks Available

```python
# Transform product data into content fragments
BenefitsLogicBlock.generate(product)      # → Benefits content
UsageLogicBlock.generate(product)         # → Usage instructions
SafetyLogicBlock.generate(product)        # → Safety information
IngredientLogicBlock.generate(product)    # → Ingredient details
PriceLogicBlock.generate(product)         # → Price analysis
ComparisonLogicBlock.generate(p1, p2)    # → Comparison metrics
```

## Adding a New Agent

1. **Create file**: `agents/new_agent.py`
```python
class NewAgent:
    def generate(self, product: Product) -> OutputType:
        """Transform product into output."""
        # implementation
        return output
```

2. **Add to orchestrator**: `orchestrator/pipeline.py`
```python
new_agent = NewAgent()
output = new_agent.generate(product)
```

3. **Register template** (if needed): `templates/template_engine.py`
```python
template = TemplateDefinition(
    name="New Template",
    page_type="new_type",
    required_fields=[...],
    required_logic_blocks=[...],
)
self.templates["new_type"] = template
```

## Adding a Logic Block

1. **Create in** `logic_blocks/blocks.py`:
```python
class NewLogicBlock:
    @staticmethod
    def generate(product: Product) -> ContentFragment:
        content = {
            "field": product.field,
            # ...
        }
        return ContentFragment(
            block_type="new_block",
            content=content,
            product_name=product.name,
        )
```

2. **Use in page agent**:
```python
logic_blocks["new_block"] = NewLogicBlock.generate(product)
# Automatically available in pages
```

## Data Model Hierarchy

```
Product (validated model)
├── name: str
├── concentration: Optional[str]
├── skin_types: List[str]
├── key_ingredients: List[str]
├── benefits: List[str]
├── usage_instructions: str
├── side_effects: List[str]
└── price: str

Question
├── category: str
├── question: str
└── context: str

ContentFragment
├── block_type: str
├── content: Dict[str, Any]
└── product_name: str

FAQPage → to_dict() → JSON
ProductPage → to_dict() → JSON
ComparisonPage → to_dict() → JSON
```

## Running the Pipeline

### Standard Execution
```python
from orchestrator.pipeline import OrchestratorAgent

orchestrator = OrchestratorAgent(output_dir="output")
orchestrator.execute_pipeline(raw_product_dict)
```

### Command Line
```bash
python main.py
```

## Testing Patterns

### Test an Agent
```python
# Test parser
parser = ProductParserAgent()
product = parser.parse(raw_data)
assert product.name == "Expected"

# Test question generation
question_agent = QuestionGenerationAgent()
questions = question_agent.generate(product)
assert len(questions) >= 15
assert all(q.category in [...] for q in questions)
```

### Test a Logic Block
```python
# Logic blocks are pure functions
fragment = BenefitsLogicBlock.generate(product)
assert fragment.block_type == "benefits"
assert "title" in fragment.content
```

### Test Complete Pipeline
```python
orchestrator = OrchestratorAgent(output_dir="test_output")
orchestrator.execute_pipeline(test_product)
# Verify JSON files exist and are valid
```

## JSON Output Structure

### FAQ Output
```json
{
  "page_type": "faq",
  "product_name": "String",
  "total_questions": 15,
  "faqs": [{
    "question": "String",
    "answer": "String",
    "category": "Informational|Usage|Safety|Purchase|Comparison"
  }]
}
```

### Product Page Output
```json
{
  "page_type": "product",
  "product_name": "String",
  "sections": {
    "overview": [{"label": "String", "value": "Any", "data_type": "string"}],
    "benefits": [...],
    "ingredients": [...],
    "usage": [...],
    "safety": [...],
    "price": [...],
    "compatibility": [...]
  }
}
```

### Comparison Output
```json
{
  "page_type": "comparison",
  "product_a_name": "String",
  "product_b_name": "String",
  "comparison_items": [{
    "attribute": "String",
    "product_a": "String",
    "product_b": "String"
  }]
}
```

## Debugging Tips

### Enable Verbose Output
Add to orchestrator.py:
```python
print(f"DEBUG: Product = {product.to_dict()}")
print(f"DEBUG: Questions count = {len(questions)}")
```

### Check Generated Blocks
```python
logic_blocks = orchestrator._generate_logic_blocks(product)
for name, block in logic_blocks.items():
    print(f"{name}: {block.content}")
```

### Validate Against Templates
```python
template = orchestrator.template_engine.get_template("faq")
template.validate_content(faq_output.to_dict())
```

## Performance Considerations

- **Single process**: ~100ms for small products
- **No I/O blocking**: File writes are synchronous
- **No external calls**: All deterministic
- **Memory efficient**: No caching, ~2-5MB per run

## File Modification Checklist

When modifying files:

- [ ] Update docstrings if logic changes
- [ ] Run `python main.py` to verify
- [ ] Check JSON output format
- [ ] Verify all agents still work together
- [ ] Update documentation if adding features

## Common Scenarios

### Scenario 1: Add New Question Category
1. Add method `_generate_<category>_questions()` in QuestionGenerationAgent
2. Add category name to `self.categories`
3. Run main.py - questions generated automatically

### Scenario 2: Add New Product Field
1. Add field to models.Product dataclass
2. Update parser_agent.py with field name mappings
3. Update relevant logic blocks to use new field
4. Update templates if needed
5. Run main.py with new product data

### Scenario 3: Change Page Output Format
1. Modify models.ProductPage.to_dict() format
2. Update template in template_engine.py if structure changed
3. Run main.py - JSON regenerated with new format

### Scenario 4: Add Custom Content Logic
1. Create new logic block following BenefitsLogicBlock pattern
2. Register in orchestrator._generate_logic_blocks()
3. Use in page agent's generate() method
4. Output automatically included

## Key Design Principles

✅ **DRY** - Logic blocks reused across pages
✅ **SOLID** - Single responsibility per agent
✅ **Composable** - Blocks combine into pages
✅ **Deterministic** - Same input = same output
✅ **Testable** - Each component independent
✅ **Maintainable** - Clear structure and naming
✅ **Extensible** - Easy to add new agents/blocks

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Required field missing" | Check raw_product_dict field names match expected keys |
| Import errors | Verify __init__.py files exist in all directories |
| JSON encoding error | Ensure UTF-8 handling, use .encode('utf-8') if needed |
| Agent produces empty output | Check input Product has required fields |
| Comparison product not generated | ComparisonPageAgent creates fictional product B automatically |

---

**Last Updated**: December 28, 2025
**Version**: 1.0
**Maintainer**: Applied AI Engineering Team
