# Prompt Engineering Patterns

A collection of proven prompt engineering patterns for building reliable AI applications.

## Table of Contents

1. [Instruction Prompts](#instruction-prompts)
2. [Few-Shot Learning](#few-shot-learning)
3. [Chain-of-Thought](#chain-of-thought)
4. [Structured Outputs](#structured-outputs)
5. [System Prompts](#system-prompts)
6. [Role Prompting](#role-prompting)
7. [Constraints and Guidelines](#constraints-and-guidelines)

---

## Instruction Prompts

Direct, clear instructions for specific tasks.

### Pattern

```
[Clear instruction]
[Context/input data]
[Output format specification]
```

### Example

```python
def summarize_text(text: str) -> str:
    prompt = f"""Summarize the following text in 2-3 sentences.
Focus on the main points and key takeaways.

Text: {text}

Summary:"""
    return client.generate(prompt)
```

### Best Practices

- Start with action verbs (Summarize, Extract, Classify, etc.)
- Be specific about output format
- Include relevant context
- Set clear boundaries

---

## Few-Shot Learning

Provide examples to teach the pattern.

### Pattern

```
[Task description]

Example 1:
Input: [example input 1]
Output: [example output 1]

Example 2:
Input: [example input 2]
Output: [example output 2]

Now do:
Input: [actual input]
Output:
```

### Example

```python
def classify_sentiment(text: str) -> str:
    prompt = f"""Classify the sentiment as positive, negative, or neutral.

Example 1:
Text: "I absolutely love this product! Best purchase ever."
Sentiment: positive

Example 2:
Text: "Terrible quality, complete waste of money."
Sentiment: negative

Example 3:
Text: "It arrived on time and matches the description."
Sentiment: neutral

Now classify:
Text: "{text}"
Sentiment:"""

    return client.generate(prompt).strip()
```

### Best Practices

- Use 2-5 examples (more isn't always better)
- Examples should cover edge cases
- Keep examples diverse
- Use consistent formatting

---

## Chain-of-Thought

Break complex reasoning into steps.

### Pattern

```
[Task description]

Think through this step by step:
1. [Step description]
2. [Step description]
...

[Input]
```

### Example

```python
def solve_math_word_problem(problem: str) -> str:
    prompt = f"""Solve this math problem step by step.

Problem: {problem}

Let's solve this step by step:
1. Identify what we know
2. Identify what we need to find
3. Set up the equation
4. Solve the equation
5. State the answer

Solution:"""

    return client.generate(prompt)
```

### Best Practices

- Explicitly ask for step-by-step reasoning
- Number the steps
- Request final answer at the end
- Works best for complex reasoning tasks

---

## Structured Outputs

Request specific output formats (JSON, tables, lists).

### Pattern

```
[Task description]

Return the result as [format specification].

[Input]

[Format]:
```

### Example (JSON)

```python
import json
from typing import Dict

def extract_contact_info(text: str) -> Dict:
    prompt = f"""Extract contact information from the text.

Return a JSON object with these fields:
- name: string (person's full name)
- email: string (email address, or null if not found)
- phone: string (phone number, or null if not found)
- company: string (company name, or null if not found)

Text: {text}

JSON:"""

    response = client.generate(prompt)

    # Parse and validate
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Handle malformed JSON
        raise ValueError("Failed to parse response as JSON")
```

### Example (Markdown Table)

```python
def compare_products(products: List[str]) -> str:
    prompt = f"""Compare these products in a markdown table.

Products: {', '.join(products)}

Create a table with columns: Product, Pros, Cons, Price Range

Markdown Table:"""

    return client.generate(prompt)
```

### Best Practices

- Specify exact format (JSON schema, table structure, etc.)
- Include example output if format is complex
- Validate and parse the output
- Handle malformed responses gracefully

---

## System Prompts

Set behavior, persona, or constraints for the entire conversation.

### Pattern

```
System: [Role definition, constraints, behavior guidelines]

User: [Actual query]
```

### Example

```python
SYSTEM_PROMPT = """You are a Python code reviewer.

Your responses must:
- Focus on code quality, not functionality
- Identify security vulnerabilities
- Suggest specific improvements
- Follow PEP 8 style guidelines
- Be concise and actionable

Do not:
- Rewrite the entire code
- Suggest alternative approaches unless critical
- Include generic praise
"""

def review_code(code: str) -> str:
    return client.generate(
        prompt=f"Review this code:\n\n{code}",
        system=SYSTEM_PROMPT
    )
```

### Best Practices

- Define role clearly
- Set explicit constraints
- Specify what NOT to do
- Keep it under 500 words
- Test with edge cases

---

## Role Prompting

Assign an expert persona to improve response quality.

### Pattern

```
You are [specific expert role] with expertise in [domain].

[Task with context]
```

### Example

```python
def get_legal_summary(document: str) -> str:
    prompt = f"""You are an experienced contract lawyer specializing in technology agreements.

Analyze this contract clause and summarize:
1. Key obligations
2. Potential risks
3. Recommended actions

Clause: {document}

Analysis:"""

    return client.generate(prompt)
```

### Best Practices

- Be specific about expertise level
- Match role to task domain
- Include relevant context
- Combine with constraints

---

## Constraints and Guidelines

Set boundaries and quality standards.

### Pattern

```
[Task description]

Requirements:
- [Constraint 1]
- [Constraint 2]
...

[Input]
```

### Example

```python
def generate_product_description(product_name: str, features: List[str]) -> str:
    prompt = f"""Write a product description for {product_name}.

Requirements:
- Maximum 150 words
- Include all features: {', '.join(features)}
- Write in second person ("you")
- Highlight benefits, not just features
- Use active voice
- No superlatives (best, greatest, etc.)

Product Description:"""

    return client.generate(prompt, max_tokens=300)
```

### Best Practices

- List constraints explicitly
- Be specific with numbers (word count, format, etc.)
- Include quality guidelines
- Test boundary conditions

---

## Advanced Patterns

### Self-Consistency

Ask for multiple reasoning paths and aggregate.

```python
def answer_with_confidence(question: str, n_samples: int = 3) -> Dict:
    """Generate multiple answers and check for consistency."""
    answers = []

    for i in range(n_samples):
        prompt = f"""Answer this question with step-by-step reasoning.

Question: {question}

Reasoning and Answer:"""

        response = client.generate(prompt, temperature=0.8)
        answers.append(response)

    # Count most common answer (simplified)
    # In production, use more sophisticated aggregation
    return {
        "answers": answers,
        "consistency": "High" if len(set(answers)) == 1 else "Low"
    }
```

### Prompt Chaining

Break complex tasks into sequential prompts.

```python
def write_blog_post(topic: str) -> str:
    # Step 1: Generate outline
    outline_prompt = f"""Create a blog post outline for: {topic}

Include:
- Introduction hook
- 3-4 main points
- Conclusion

Outline:"""

    outline = client.generate(outline_prompt)

    # Step 2: Expand outline into full post
    expansion_prompt = f"""Write a complete blog post based on this outline.

Outline:
{outline}

Requirements:
- 500-700 words
- Engaging, conversational tone
- Include specific examples

Blog Post:"""

    return client.generate(expansion_prompt, max_tokens=1500)
```

---

## Testing Prompts

### Validation Checklist

- [ ] Test with typical inputs
- [ ] Test with edge cases
- [ ] Test with invalid inputs
- [ ] Verify output format
- [ ] Check token usage
- [ ] Measure latency
- [ ] Test at different temperatures

### Example Test

```python
def test_sentiment_classifier():
    """Test sentiment classification prompt."""
    test_cases = [
        ("I love this!", "positive"),
        ("Terrible experience", "negative"),
        ("It's okay", "neutral"),
        ("", "neutral"),  # Edge case: empty
        ("Love it! But expensive", "positive"),  # Edge case: mixed
    ]

    for text, expected in test_cases:
        result = classify_sentiment(text)
        assert result.lower() == expected, f"Failed for: {text}"
```

---

## Cost Optimization

1. **Be concise**: Shorter prompts = fewer tokens
2. **Cache system prompts**: Reuse when possible
3. **Use appropriate models**: Don't use Opus for simple tasks
4. **Set max_tokens**: Limit output length
5. **Batch requests**: Process multiple items together when possible

```python
# Good: Batch processing
def classify_batch(texts: List[str]) -> List[str]:
    prompt = f"""Classify sentiment (positive/negative/neutral) for each text.

Texts:
{chr(10).join(f'{i+1}. {text}' for i, text in enumerate(texts))}

Results (format: "1. positive"):"""

    response = client.generate(prompt)
    # Parse response...

# Bad: Individual requests
for text in texts:
    classify_sentiment(text)  # Too many API calls!
```

---

*These patterns are battle-tested and work reliably with Claude and other modern LLMs.*
