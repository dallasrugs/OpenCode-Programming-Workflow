---
name: ecommerce-product-pages
description: Audit, design, write, and optimize product detail pages for retail, wholesale, B2B, DTC, and inquiry-based commerce. Covers product data, usability, conversion, SEO, and accessibility.
---

# eCommerce Product Pages

Inspired by:
- amanamabasiakpan/Claude-Skills-for-eCommerce
- AgriciDaniel/claude-seo

## Purpose

Help businesses build accurate, useful, and
conversion-focused product detail pages.

Use for:
- Product page design
- Product page audits
- Product information architecture
- Product descriptions
- Variant presentation
- Product SEO
- Conversion optimization
- Mobile product experiences
- Product schema recommendations

Support both direct checkout and inquiry-based commerce.

## 1. Understand the business model

Identify the page's intended conversion:

- Purchase
- Request a quote
- Request a sample
- Ask about availability
- Contact a sales representative
- Schedule an appointment
- Submit a product inquiry

Do not assume online checkout exists.

Align every recommendation with the actual
customer journey.

## 2. Inspect existing implementation

Before proposing changes, inspect:

- Current product page layout
- Existing components
- Product data structure
- Available attributes
- Product variants
- Image handling
- Navigation
- Existing calls to action
- Responsive behavior
- SEO implementation

Reuse established application patterns.

Do not invent product data or assume
specific database structures.

## 3. Product identity

A visitor should quickly understand:

- What the product is
- Its category or product type
- Its distinguishing characteristics
- Its available configurations
- Its intended use

Use descriptive product names.

Preserve official names, identifiers,
and existing catalog conventions.

## 4. Product information

Present verified information such as:

- Materials
- Construction
- Dimensions
- Color
- Finish
- Origin
- Weight
- Features
- Care instructions
- Product identifiers
- Available options

Prioritize attributes that affect
customer decisions.

Do not fabricate missing specifications.

Distinguish unavailable information
from information that is not applicable.

## 5. Product variants

When variants exist:

- Identify shared product attributes.
- Identify variant-specific attributes.
- Present available choices clearly.
- Keep variant identifiers accurate.
- Update relevant specifications consistently.
- Preserve valid product URLs when applicable.
- Avoid showing unavailable configurations
  as immediately purchasable.

Do not invent variant relationships.

## 6. Product images

Evaluate:

- Main image clarity
- Image resolution
- Gallery organization
- Aspect ratio consistency
- Mobile presentation
- Zoom or detail views
- Appropriate alternative text
- Loading performance

Recommend contextual or detail images
when they would materially help customers.

Do not claim images exist without inspection.

## 7. Content and brand voice

Use ecommerce-brand-voice to maintain
the appropriate business identity.

Use ecommerce-copywriting for persuasive,
accurate product explanations.

Use natural-writing for natural prose.

Avoid:
- Generic AI descriptions
- Repetitive promotional claims
- Unsupported superlatives
- Excessive adjectives
- Duplicate product information
- Misleading urgency

Describe meaningful product differences.

## 8. Conversion and usability

Help visitors answer:

1. What is this?
2. Is it right for my needs?
3. What options are available?
4. What information supports my decision?
5. How do I proceed?

Review:

- Primary call to action
- Above-the-fold clarity
- Mobile usability
- Navigation
- Variant selectors
- Information hierarchy
- Trust signals
- Contact or inquiry experience

Avoid unnecessary interface complexity.

## 9. SEO

Use seo-content for:

- Search intent
- Product descriptions
- Titles and metadata
- Meaningful headings
- Internal linking

Use seo-technical for:

- Canonical URLs
- Structured data
- Indexability
- Image performance
- Rendering
- Variant URL strategy

Never create fake reviews, prices,
availability, or ratings for structured data.

Only recommend Schema.org properties
supported by actual product information.

## 10. Accessibility

Review:

- Semantic headings
- Keyboard navigation
- Accessible controls
- Form labeling
- Image descriptions
- Focus behavior
- Contrast
- Mobile touch targets
- Error messages

Product selectors and inquiry controls
must be usable without a mouse.

## 11. Performance

Consider:

- Image loading
- Layout stability
- JavaScript execution
- Initial rendering
- Unnecessary client-side requests
- Caching
- Responsive image sizes

Prioritize measured performance issues.

Do not invent Lighthouse results.

## 12. Audit workflow

1. Understand the page and business model.
2. Inspect existing components and product data.
3. Identify customer information needs.
4. Evaluate content and usability.
5. Evaluate relevant SEO.
6. Identify verified issues and opportunities.
7. Prioritize changes by impact and effort.
8. Present recommendations with acceptance criteria.

Separate confirmed problems from assumptions.

## 13. Implementation workflow

For approved product page improvements:

1. Follow the existing Planner approval process.
2. Delegate through the Supervisor.
3. Implement using established components.
4. Preserve catalog data integrity.
5. Add or update relevant tests.
6. Verify desktop and mobile behavior.
7. Confirm accessibility and SEO behavior.
8. Report actual verification results.

Do not independently deploy changes.

## 14. Final quality checklist

Confirm:

- Product identity is immediately clear.
- Specifications match the source data.
- Variant behavior is correct.
- Images support customer understanding.
- Copy reflects the intended brand.
- Calls to action match the sales model.
- SEO metadata is accurate.
- Accessibility requirements are considered.
- No unsupported claims are present.
- Relevant tests pass.

## Boundaries

Never invent product information.

Never alter catalog records, pricing,
availability, or inventory without approval.

Never publish website changes automatically.

Follow the existing four-agent architecture.
