# 12. The Art of Writing Precise Prompts

## What Is a Prompt

A prompt is the command you give to AI. Good prompts get precise, useful answers from AI; vague prompts only get vague results.

```
Bad Prompt:              Good Prompt:
────────────────       ───────────────────────
"Design a website"      "Design a landing page for a
                        fitness app for women aged 25-35
                        who are office workers,
                        fresh and natural style,
                        main CTA is free trial"
```

## Basic Elements of a Prompt

A complete prompt should include:

| Element | Description | Example |
|---------|-------------|---------|
| **Role** | What identity AI should assume | "You are a professional web designer" |
| **Task** | Specifically what to do | "Help me design a landing page structure" |
| **Context** | Related background info | "This is a promotion page for an online course" |
| **Constraints** | Special requirements | "Within 500 words" |
| **Format** | Output format | "Present in a table" |

## Prompt Framework: ICIO

### I - Instruction

Clearly state what you want AI to do:

```
❌"Help me think"
✓"Help me list 10"
✓"Help me write a paragraph"
✓"Help me check and fix"
```

### C - Context

Provide enough background information:

```
No Context:           With Context:
────────────────     ───────────────────────
"How to lose weight" "I'm an office worker, sit at desk
                      8 hours a day, only have 1 hour
                      at lunch to exercise,
                      how to lose weight?"
```

### I - Input

If there's any data to process, provide to AI:

```
"Please help me write copy based on the following product info:

Product: [product name]
Function: [function description]
Target audience: [description]"

+ Specific product info
```

### O - Output

Explain the expected output format:

```
"Please present in the following format:
1. Title (8 words or less)
2. Subtitle (20 words or less)
3. Three key points (15 words or less each)
4. CTA button text (10 words or less)"
```

## Prompt Examples for Different Scenarios

### Scenario 1: Website Copy

```
Role: You are an experienced web copywriter, skilled at writing
      high-conversion landing page copy.

Task: Help me write Hero section copy for an online course landing page.

Background:
- Course name: Excel from Zero to Advanced
- Target audience: Fresh workplace employees, office workers wanting to improve efficiency
- Course selling points: No need to memorize functions, case-based learning, results in 30 days
- Price: Original $2999, discounted to $1499

Requirements:
1. Main headline: Start with pain point, create resonance
2. Subtitle: Explain course core value
3. 3 Bullet Points: Course features
4. CTA button text
5. Tone should be friendly, not too businesslike

Format: Present in Markdown format
```

### Scenario 2: Code Assistance

```
Role: You are an engineer specialized in front-end development.

Task: Help me write CSS code to add gradient background to my website Hero section.

Requirements:
1. Gradient from #667eea to #764ba2 (top-left to bottom-right)
2. Must completely cover Hero section
3. Text should be white with shadow
4. Responsive: reduce padding on mobile

Use modern CSS (CSS3), avoid outdated syntax.
```

### Scenario 3: Image Generation

```
Using Midjourney or DALL-E:

Theme: Modern minimalist home office setup
Style: Photography, clean aesthetic
Light: Natural window light
Colors: Warm wood tones, white, green plants
Other: MacBook on desk, coffee cup, not cluttered
Aspect ratio: 16:9
```

### Scenario 4: Website Architecture Planning

```
Role: You are an experienced UX designer and information architect.

Task: Help me plan the page structure of an e-commerce website.

Background:
- Product type: Organic skincare products
- Target audience: Health-conscious women aged 25-40
- Main functions: Product sales, membership system, blog

Requirements:
1. List all necessary pages
2. Explain main purpose of each page
3. Suggest navigation structure between pages
4. Point out which functions are "essential" vs "optional"

Present in a table, clear format.
```

## Tips for Improving Prompt Effectiveness

### Tip 1: Break Down Complex Tasks

```
One-time completion (bad):
"Help me design the entire website, including homepage, about page, service page,
each page needs copy and layout suggestions"

Step-by-step (recommended):
Step 1: "Help me plan website structure and pages"
Step 2: "For homepage, help me write copy"
Step 3: "For homepage, give me layout suggestions"
...and so on
```

### Tip 2: Give Examples

```
❌"Write in professional tone"

✓"Write in the following example's tone:
'A course designed for Taiwanese people,
learn authentic American accent without leaving the country'"
```

### Tip 3: Limit Output Scope

```
❌"Give me some title suggestions"

✓"Give me 5 title suggestions, each no more than 15 words,
style should be creative but not clickbait"
```

### Tip 4: Request Multiple Outputs

```
❌"Give me one title"

✓"Give me 3 different style titles:
1. Feature-oriented
2. Emotion-oriented
3. Data-oriented"
```

### Tip 5: Iterate and Optimize

After the first prompt, adjust based on AI's response:

```
First round: "Help me write a website slogan"
After AI responds...

Second round: "Great! But more playful,
         any younger version?"
```

## Common Prompt Mistakes

### Mistake 1: Too Vague

```
❌"Website should look good"
✓"Website should be Nordic minimalist, white as main color, with wood elements,
   lots of white space, give warm and comfortable feeling"
```

### Mistake 2: Asking for Too Much at Once

```
❌"Help me design entire website, write all copy, color scheme,
   font selection, image suggestions"
✓ Ask each requirement separately
```

### Mistake 3: Ignoring Format Requirements

```
❌"List points" → AI presents in paragraphs
✓"Please present in Markdown list format, each point no more than 20 words"
```

### Mistake 4: Not Explaining Usage

```
❌"Help me write product description" → AI doesn't know where to use
✓"Help me write product card description for an e-commerce website,
   within 100 words, for quick scanning on mobile screens"
```

## Advanced Prompt Techniques

### Chain of Thought

Ask AI to think step by step:

```
"Before giving me your answer, explain your thinking logic:
1. What is my need?
2. What factors should be considered?
3. Why do you suggest this solution?"
```

### Few-Shot Learning

Provide a few examples for AI to understand your desired style:

```
"Help me write product titles, style reference:
Example 1: Lose weight without help, exercise at home
Example 2: Lazy person's organization trick, one move makes home tidy
Example 3: 30 days English transformation

Now help me write 5 titles for 'Online yoga course'"
```

### Role Playing

Have AI assume a specific role:

```
"You are now a:
- Top web designer
- Expert in UX psychology
- Direct speaker, give critical feedback
- Focus on conversion rate not just aesthetics

I have a landing page I want you to give feedback on: [describe your page]

Please give me feedback from designer and marketer perspective"
```

## Build Your Prompt Template Library

Recommend building a document to collect prompts you commonly use:

```
# Common Prompt Templates

## Website Copy

### Hero Section Copy
---
Role: You are a...
Task: ...
Background: ...
Requirements: ...
Format: ...
---

### Product Description
---
...
---
```

This way next time you need similar tasks you can copy and modify directly.

## Practice Exercises

### Exercise 1: Write Website Copy Prompt

Try writing a complete prompt for the following scenario:

Scenario: "You need to make a website for a newly opened coffee shop, need homepage copy"

Use ICIO framework, fully describe role, task, background, output format.

### Exercise 2: Optimize Existing Prompts

Change the following vague prompts to detailed ones:

```
Original: "Help me write copy"

Scenario: Write promotion copy for an online English course
```

### Exercise 3: Build Your Own Prompt

For the project you're working on, design a complete prompt,
save it to your template library.

---

In the next chapter, we'll learn how to use AI to do SEO optimization for your website.