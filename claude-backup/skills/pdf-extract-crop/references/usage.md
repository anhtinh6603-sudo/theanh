# Usage

## Goal

This skill is meant for practical PDF tasks:
- read catalog text
- capture whole pages as images
- cut out a table, model line, or information block

## Recommended order

1. Extract text first if the PDF contains selectable text.
2. If the user wants visuals, render the relevant page to an image.
3. Crop the exact region from the page image.

## Why this approach

Direct PDF cropping is often brittle across environments. Rendering the page first, then cropping the image, is more reliable when you need something visible in chat.

## Common cases

- "Cut model HA1600/570PVC from this catalog" -> render page -> crop row/block
- "Read this brochure and summarize it" -> extract text first
- "Show me page 3 of this PDF" -> page-shot
