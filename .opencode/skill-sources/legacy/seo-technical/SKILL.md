---
name: seo-technical
description: Audit and improve technical website SEO, including crawling, indexing, canonical URLs, sitemaps, structured data, performance, and international SEO.
---

# Technical SEO

Inspired by AgriciDaniel/claude-seo.

## Purpose

Help search engines discover, understand, and index
website content correctly.

Use for:
- Technical SEO audits
- Crawlability and indexing
- robots.txt and meta robots
- XML sitemaps
- Canonical URLs and redirects
- Structured data and Schema.org
- Core Web Vitals
- Mobile accessibility
- JavaScript rendering
- International SEO and hreflang
- Product and category page SEO

## 1. Inspect the existing architecture

Identify:
- Framework and rendering strategy
- Routing and URL structure
- Metadata generation
- Sitemap generation
- robots.txt configuration
- Canonical URL rules
- Structured data implementation
- Deployment environment

Inspect existing code before recommending changes.

Do not assume the website uses a particular
framework, CMS, or hosting provider.

## 2. Crawlability and indexing

Check:
- HTTP status codes
- robots.txt directives
- Meta robots directives
- X-Robots-Tag headers
- Internal linking
- Orphan pages
- Redirect chains
- Duplicate content
- Canonical relationships

Distinguish crawling restrictions
from indexing restrictions.

Do not recommend blocking essential
search engine access without justification.

## 3. Sitemaps

Validate:
- XML syntax
- Canonical URL consistency
- Inclusion of intended indexable pages
- Exclusion of redirects and error pages
- Relevant lastmod values
- Language alternates when applicable

Do not invent sitemap entries.

## 4. Canonicalization

Determine the preferred URL for each page.

Review:
- HTTP versus HTTPS
- Trailing slash consistency
- Duplicate query parameter URLs
- Product variants
- Pagination
- Language and regional alternatives

Avoid canonicalizing genuinely distinct
content to unrelated pages.

## 5. Structured data

Inspect existing JSON-LD or other markup.

Recommend relevant Schema.org types
based on actual page content.

Possible types include:
- Organization
- LocalBusiness
- BreadcrumbList
- Product
- Article
- CollectionPage

Validate required and recommended properties
against current documentation.

Never invent:
- Ratings or reviews
- Prices
- Availability
- Product identifiers
- Business information
- Certifications

Do not promise rich-result eligibility.

## 6. Performance

Review relevant Core Web Vitals:
- Largest Contentful Paint (LCP)
- Interaction to Next Paint (INP)
- Cumulative Layout Shift (CLS)

Consider:
- Image optimization
- Font loading
- JavaScript execution
- Server response
- Caching
- Render-blocking resources
- Hydration behavior

Prioritize actual measured bottlenecks.

Never fabricate Lighthouse or CrUX results.

## 7. JavaScript rendering

Check whether important content and links
are accessible to search engines.

Inspect:
- Server-rendered HTML
- Client-side rendering
- Metadata availability
- Navigation links
- Product descriptions
- Structured data
- Error handling

Do not recommend SSR or static generation
without considering the existing architecture.

## 8. International SEO

For multilingual websites, evaluate:
- Language-specific URLs
- Hreflang relationships
- Self-referencing alternates
- Regional targeting
- Canonical consistency
- Translated metadata
- Localized content
- Fallback behavior

Never assume translations exist.

## 9. Product and category SEO

Review:
- Product identity and descriptions
- Variant URL strategy
- Product structured data
- Breadcrumb hierarchy
- Category navigation
- Internal product links
- Duplicate product pages
- Image accessibility
- Discontinued or unavailable products

Base recommendations on actual business
and application behavior.

## 10. Audit workflow

1. Identify audit scope.
2. Inspect the relevant implementation.
3. Collect measurable evidence.
4. Separate confirmed problems from risks.
5. Estimate impact and implementation effort.
6. Prioritize recommendations.
7. Define validation criteria.
8. Propose an implementation plan.

Use live checks only when tools permit them.

Explicitly disclose unavailable measurements.

## 11. Implementation boundaries

Follow the established BDFL authorization and Maintainer approval gate.

Do not independently:
- Change production routing
- Modify live DNS
- Submit indexing requests
- Deploy application changes
- Alter analytics configuration
- Publish structured data

Coordinate code changes through the Maintainer
and Coder after approval.

## 12. Final verification

Check:
- Canonical URLs remain correct
- Required pages remain accessible
- Metadata is rendered correctly
- Sitemap contents match the site
- Structured data represents real content
- Internal links resolve
- No unintended noindex directives exist
- Relevant tests pass

Report unresolved issues and unverified claims.

## Related skills

Use seo-content for writing, metadata,
search intent, and content quality.

Use natural-writing when optimizing prose.

Use ecommerce-product-pages for detailed
product page optimization when available.


## Governed execution

The governance controller owns state and authorization. Maintainer plan approval and BDFL task/spec authorization precede coding. The Reviewer prepares the rubric and independently reviews real deterministic test evidence. Only the Coder edits exact approved source paths; the Maintainer decides integration and the Team Lead reports verified outcomes. Skills cannot grant tools, authorize scope expansion, or replace independent review.
