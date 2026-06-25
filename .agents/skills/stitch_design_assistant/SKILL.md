---
name: stitch-design-assistant
description: Instructions and guidelines for calling Stitch MCP tools, setting design system themes, and applying layouts.
---

# Stitch Design Assistant Skill

Use this skill when interacting with the Stitch MCP server, creating design systems, modifying screens, or verifying visual compliance.

## 1. Core Workflow
1.  **Project Initialization**: Create or retrieve project details via `create_project` and `get_project`.
2.  **Theme Configuration**: Create design systems using `create_design_system` specifying primary colors, fonts, and roundness.
3.  **Application**: Apply the design systems using `apply_design_system` to target screen instances.

## 2. Design System Guidelines

*   **Color Presets**: Define a custom primary color (e.g. Signature Gold `#B8933E`) and seed it as the theme primary.
*   **The "No-Line" Rule**: Emphasize background color shifts and whitespace instead of 1px solid borders for visual division.
*   **Glassmorphism**: Implement floating panels with a backdrop-blur (minimum `20px`) and 80% opacity.
*   **Typography pairings**: Pair elegant Serifs (like Noto Serif, EB Garamond) for display/headings with geometric/clean Sans-Serifs (like Inter, Space Grotesk) for UI body/metadata labels.
*   **Roundness**: Use `ROUND_FOUR` (Level 1, 0.25rem or 4px) for precise, clean cut edges in leather goods PLM applications.

## 3. Tool Call Instructions
*   When uploading a design system from a markdown file:
    1. Call the `upload_design_md` tool first.
    2. Immediately call `create_design_system_from_design_md` to generate and apply tokens.
*   When using custom hex codes:
    * Set `colorMode` to `LIGHT` or `DARK`.
    * Set `customColor` to the target primary hex value.
    * Use `overridePrimaryColor`, `overrideSecondaryColor`, and `overrideNeutralColor` for precision mapping.
