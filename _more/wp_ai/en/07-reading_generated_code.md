# 7. Understanding AI-Generated Code

## Why You Need to Understand Code

You might ask: "Since I'm using an AI building platform, why do I need to understand code?"

The reasons are simple:

1. **Better communication**: Understanding basic concepts lets you describe needs to AI more precisely
2. **Necessary adjustments**: When platform-provided features are limited, you need to modify code yourself
3. **Troubleshooting**: When problems occur on the website, you can roughly know where to look
4. **Learning and growth**: This is a stepping stone into the website development world

## Basic Components of a Website

### Three-Layer Structure

Any website consists of three parts:

```
┌─────────────────────────────────────┐
│          HTML (Content Layer)       │
│     "This is a heading" "This is a paragraph"  │
├─────────────────────────────────────┤
│          CSS (Style Layer)          │
│   "The heading is blue" "Text should be 16px"  │
├─────────────────────────────────────┤
│       JavaScript (Interaction Layer)│
│    "Clicking the button should pop up a window" │
└─────────────────────────────────────┘
```

### Using a House as a Metaphor

| Concept | House Metaphor |
|---------|---------------|
| HTML | Structure of the house: walls, doors, rooms |
| CSS | Decoration of the house: paint color, floor material, curtain style |
| JavaScript | Electrical/mechanical of the house: light switches, doorbell, AC remote |

## HTML Basics

### What Are Tags

HTML uses "Tags" to define content. Tags usually come in pairs:

```html
<tagname>content</tagname>
```

### Common HTML Tags

**Headings**:
```html
<h1>This is a level 1 heading</h1>
<h2>This is a level 2 heading</h2>
<h3>This is a level 3 heading</h3>
```

**Paragraphs and text**:
```html
<p>This is a paragraph</p>
<strong>This is bold text</strong>
<em>This is italic text</em>
```

**Links**:
```html
<a href="https://example.com">Click here</a>
```

**Images**:
```html
<img src="photo.jpg" alt="Image description">
```

**Lists**:
```html
<ul>
  <li>First item</li>
  <li>Second item</li>
  <li>Third item</li>
</ul>
```

### Understanding class and id

To make it easier for CSS and JavaScript to find specific elements, we add "names":

```html
<!-- class: used for a group of elements -->
<div class="header">Header section</div>
<div class="header">Another header</div>

<!-- id: used for unique elements -->
<div id="main-menu">Main menu</div>
```

## CSS Basics

### What Is CSS

CSS is used to control the "appearance" of HTML elements.

### Basic Syntax

```css
selector {
  property: value;
}
```

### Common CSS Properties

**Colors**:
```css
color: blue;              /* text color */
background-color: #f0f0f0; /* background color */
```

**Fonts**:
```css
font-size: 16px;           /* font size */
font-family: Arial;       /* font type */
font-weight: bold;         /* font weight */
```

**Dimensions**:
```css
width: 100px;              /* width */
height: 200px;             /* height */
max-width: 100%;           /* maximum width */
```

**Margins and padding**:
```css
margin: 20px;              /* outer margin */
padding: 15px;             /* inner padding */
```

**Alignment**:
```css
text-align: center;        /* text alignment */
display: flex;             /* flexbox layout */
justify-content: center;   /* horizontal centering */
```

### Types of Selectors

```css
/* Tag selector */
h1 {
  color: red;
}

/* Class selector */
.container {
  width: 1000px;
}

/* ID selector */
#header {
  background: white;
}

/* Compound selector */
.header .logo {
  width: 50px;
}
```

## JavaScript Basics

### What Is JavaScript

JavaScript is used to control the "behavior" and "interaction" of web pages.

### Basic Syntax

**Variables**:
```javascript
let name = "Xiao Ming";
let age = 25;
let isMember = true;
```

**Functions**:
```javascript
function sayHello() {
  alert("Hello!");
}
```

**Event Listeners**:
```javascript
// When button is clicked, execute
button.addEventListener('click', function() {
  alert("Button clicked!");
});
```

### Common Use Cases

| Function | JavaScript |
|----------|------------|
| Click button to show more content | `addEventListener('click')` |
| Validate form input | `if (input.value === "")` |
| Scroll to top of page | `window.scrollTo(0, 0)` |
| Countdown timer | `setInterval()` |

## Viewing Code in AI Tools

### Wix Code Options

In Wix editor:
1. Click "Developer Tools"
2. You can see HTML, CSS, JavaScript
3. You can add custom code here

### Durable Code Export

Durable can export code:
1. Click "Export" or "Download"
2. Choose download format
3. Get HTML, CSS, JavaScript files

### WordPress Code Editing

WordPress theme editor location:
1. Appearance → Theme File Editor
2. Choose file to edit
3. Make modifications (be careful not to break the website)

## Simple Code Modification Examples

### Example 1: Change Text Color

**Before**:
```css
h1 {
  color: black;
}
```

**Change to blue**:
```css
h1 {
  color: blue;
}
```

### Example 2: Adjust Spacing

**Before**:
```css
.container {
  padding: 10px;
}
```

**Increase top and bottom spacing**:
```css
.container {
  padding: 40px 10px;
}
```

### Example 3: Hide Unwanted Elements

Sometimes you don't want a certain section, you can temporarily hide it:

```css
.unwanted-section {
  display: none;
}
```

## Using AI to Help You Write Code

### Directly Ask AI to Modify

You can say to Claude or ChatGPT:

```
"Help me change this section's background color to dark gray,
text to white."

"Help me write a JavaScript code that shows 'Thank you for subscribing!'
when user clicks the button."
```

### Ask AI to Explain Code

If you see code you don't understand, just ask:

```
"What does this code do?
.hello {
  color: red;
  font-size: 24px;
}"
```

AI will explain it for you.

### Modify AI-Generated Code

When AI-generated code doesn't fully meet your needs:

```
"Thanks! But I want:
1. This button on the left, not in the middle
2. Button color changed from blue to green
Can you adjust it?"
```

## Useful Code Snippets

### Center an Image

```css
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
```

### Stack Elements on Mobile

```css
.container {
  display: flex;
  flex-wrap: wrap;
}

.item {
  width: 100%;
}

@media (min-width: 768px) {
  .item {
    width: 33.33%;
  }
}
```

### Simple Button Style

```css
.button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.button:hover {
  background-color: #0056b3;
}
```

## Important Reminders

### Always Backup First

Before modifying code, copy the original version. This way you can restore if you break something.

### Be Careful with Syntax Errors

Code is very "strict," one missing semicolon or bracket can break everything:

```
Wrong: color: red
Right: color: red;

Wrong: .header { color: blue }
Right: .header { color: blue; }
```

### Start Small

If testing modifications, change a small part first, confirm it's fine before continuing.

### Ask AI When Confused

Now you have Claude as a powerful tool! Any code-related questions can be asked to it.

## You Don't Need to Know

These complex parts, you don't need to know yourself:

- Backend programming (PHP, Python, Node.js, etc.)
- Database design
- Server setup
- Complex JavaScript logic
- Network security

Leave these to professional platforms or engineers.

## You Need to Know

These basic concepts, you should understand:

- What is HTML
- CSS controls appearance
- JavaScript handles interaction
- How to find elements you want to modify
- How to edit code in AI tools
- How to ask AI to write or modify code

---

Now you have a comprehensive understanding of website basics. Next, we enter the practical exercise section where we'll actually build four types of websites!