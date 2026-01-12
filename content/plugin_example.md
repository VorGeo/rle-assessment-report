---
title: Ecosystem Config Plugin Example
ecosystem_id: MMR-T1.1.1
---

# Ecosystem Config Plugin Demo

This document demonstrates the three ways to use the ecosystem config plugin.

## 1. Transform (Automatic Loading)

When you add `ecosystem_id` to the frontmatter, the ecosystem data is automatically loaded.

**Ecosystem Name:** {frontmatter.ecosystem.ecosystem_name}

**Country:** {frontmatter.ecosystem.country_name}

**IUCN Status:** {frontmatter.ecosystem.iucn_status}

## 2. Directive (Block-Level Display)

### Display specific field as markdown

:::{ecosystem-config} MMR-T1.1.1
:field: ecosystem_names_local
:::

### Display criteria status as YAML

:::{ecosystem-config} MMR-T1.1.1
:field: criteria_status
:format: yaml
:::

### Display entire config as JSON (truncated example)

:::{ecosystem-config} MMR-T1.1.1
:field: ecosystem_image
:format: json
:::

## 3. Role (Inline References)

The ecosystem {eco}`MMR-T1.1.1:ecosystem_name` is located in {eco}`MMR-T1.1.1:country_name`.

It is classified as {eco}`MMR-T1.1.1:functional_group` within the {eco}`MMR-T1.1.1:biome` biome.

The ecosystem is also known locally as {eco}`MMR-T1.1.1:ecosystem_names_local`.

### Nested field access

The assessment was conducted on {eco}`MMR-T1.1.1:date_assessed` and assessed by {eco}`MMR-T1.1.1:assessment_credits.assessed_by`.

Criterion B1 status: {eco}`MMR-T1.1.1:criteria_status.B.B1`

## Notes

- The transform automatically injects all ecosystem data when `ecosystem_id` is in frontmatter
- Directives are great for displaying formatted blocks of data
- Roles are perfect for inline references within paragraphs
- The `ecosystem_names_local` field is specially formatted with citations
