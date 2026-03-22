# 35. Responsive Design and Accessibility

## Responsive Design Fundamentals

```
┌─────────────────────────────────────────────────────────┐
│                   Responsive Design                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Mobile First                                           │
│   └─ Start from smallest screen, progressively enhance  │
│                                                         │
│   Breakpoints                                            │
│   └─ sm: 640px, md: 768px, lg: 1024px, xl: 1280px       │
│                                                         │
│   Fluid Layout                                           │
│   └─ Use relative units, not fixed pixels                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted Responsive Design

### CSS Media Queries

```
You:
Please explain the best practices for responsive CSS.

AI:
## Responsive CSS

### 1. Mobile First
```css
/* Default (mobile) */
.container {
  width: 100%;
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    margin: 0 auto;
    padding: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
  }
}

/* Large */
@media (min-width: 1280px) {
  .container {
    max-width: 1140px;
  }
}
```

### 2. Grid System
```css
.grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1rem;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
  }
}
```

### 3. Flexible Units
```css
/* Relative units */
.rem    /* Relative to root font size */
.em     /* Relative to parent font size */
.vw/vh  /* Viewport width/height */
.%       /* Relative to parent */

/* Recommended approach */
:root {
  --spacing: 1rem;
}

.card {
  padding: var(--spacing);
  font-size: 1rem;  /* 16px */
}

@media (min-width: 768px) {
  .card {
    font-size: 1.125rem;  /* 18px */
  }
}
```

### 4. Flexbox Responsive
```css
/* Navigation */
.navbar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .navbar {
    flex-direction: row;
    justify-content: space-between;
  }
}
```

### 5. Responsive Images
```css
/* Adaptive images */
img {
  max-width: 100%;
  height: auto;
}

/* Background images */
.hero {
  background-image: url('/mobile.jpg');
}

@media (min-width: 768px) {
  .hero {
    background-image: url('/tablet.jpg');
  }
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('/desktop.jpg');
  }
}
```

### 6. Modern Solution: CSS Container
```css
.container {
  container-type: inline-size;
}

.card {
  display: grid;
  grid-template-columns: 1fr;
}

@container (min-width: 400px) {
  .card {
    grid-template-columns: 2fr 1fr;
  }
}
```
```

## Accessibility Design

```
You:
How do I implement accessible web design?

AI:
## Accessibility Design

### 1. Semantic HTML
```html
<!-- ❌ Not semantic -->
<div onclick="toggle()">Click</div>
<div class="button">Button</div>

<!-- ✅ Semantic -->
<button onclick="toggle()">Click</button>
<button class="btn">Button</button>
```

### 2. Semantic Tags
```html
<header>Header</header>
<nav>Navigation</nav>
<main>
  <article>
    <section>
      <h1>Title</h1>
      <p>Content</p>
    </section>
  </article>
</main>
<aside>Sidebar</aside>
<footer>Footer</footer>
```

### 3. Form Accessibility
```html
<!-- Properly associated labels -->
<label for="email">Email</label>
<input type="email" id="email" aria-describedby="email-help" />
<span id="email-help">Please enter a valid email address</span>

<!-- Error messages -->
<div id="email-error" role="alert" aria-live="polite">
  Invalid email format
</div>
```

### 4. Keyboard Navigation
```css
/* Focus styles */
:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* Skip link */
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  padding: 1rem;
  background: #0066cc;
  color: white;
}

.skip-link:focus {
  top: 0;
}
```

```html
<a href="#main-content" class="skip-link">Skip to main content</a>

<nav>...</nav>

<main id="main-content">
  <!-- Main content -->
</main>
```

### 5. ARIA Attributes
```html
<!-- Button state -->
<button aria-expanded="false" aria-controls="menu">
  Menu
</button>

<!-- Dynamic content -->
<div aria-live="polite" aria-atomic="true">
  <!-- Announces updates automatically -->
</div>

<!-- Dialog -->
<dialog aria-labelledby="title" aria-describedby="desc">
  <h2 id="title">Title</h2>
  <p id="desc">Description</p>
</dialog>
```

### 6. Color Contrast
```css
/* Meet WCAG AA standards */
.text {
  color: #333;        /* Dark gray text */
  background: #fff;   /* White background */
  /* Contrast ratio 12.6:1 ✅ */
}

.text-secondary {
  color: #666;        /* Light gray text */
  background: #fff;   /* White background */
  /* Contrast ratio 5.7:1 ✅ */
}

/* Avoid using color alone to convey information */
.error {
  color: red;  /* ❌ Color blind users can't see this */
  /* Should use icons or text alongside */
}

.error::before {
  content: "⚠️ ";
}
```
```

## Modern CSS Frameworks

### Tailwind CSS

```
You:
What are the advantages of Tailwind CSS?

AI:
## Tailwind CSS

### Advantages
1. **Atomic CSS** - Only generates used styles
2. **No file switching** - Write styles directly in HTML
3. **Consistent spacing and colors** - Design systemization
4. **Simple responsive** - Just add prefixes

### Usage Example
```html
<button class="
  px-4 py-2           /* Padding */
  bg-blue-500         /* Background color */
  text-white          /* Text color */
  font-medium         /* Font weight */
  rounded-lg          /* Border radius */
  hover:bg-blue-600   /* Hover state */
  focus:ring-2        /* Focus state */
  disabled:opacity-50 /* Disabled state */
">
  Button
</button>
```

### Responsive
```html
<div class="
  grid
  grid-cols-1         /* Mobile: 1 column */
  md:grid-cols-2      /* Tablet: 2 columns */
  lg:grid-cols-4      /* Desktop: 4 columns */
  gap-4
">
  <!-- Content -->
</div>
```

### Componentization
```javascript
// button.js
export function Button({ variant = 'primary', children }) {
  const variants = {
    primary: 'bg-blue-500 hover:bg-blue-600',
    secondary: 'bg-gray-200 hover:bg-gray-300',
    danger: 'bg-red-500 hover:bg-red-600'
  }
  
  return (
    <button className={`px-4 py-2 ${variants[variant]}`}>
      {children}
    </button>
  )
}
```
```

## Hands-On Exercises

```
1. Transform your pages using responsive design
2. Add accessibility features
3. Test keyboard navigation
4. Verify color contrast
5. Check accessibility with Lighthouse
```

**Responsive and accessible are not optional—they are essential characteristics every website must have.**

(End of file - total 377 lines)
