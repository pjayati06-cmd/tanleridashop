# Shopify Integration Guide

This guide details how to implement the custom brand-compliant **Atelier Hero** section and **Visual Style Overrides** into your Shopify store admin or via local theme development.

---

## 1. Quick Copy/Paste Integration (Shopify Admin)

If you are modifying your active theme directly in the browser:

### Step A: Add the Atelier Hero Section
1. Log in to your Shopify Admin and go to **Online Store > Themes**.
2. Click the **three dots (...)** next to your active theme (e.g., Dawn) and select **Edit code**.
3. Under the **Sections** folder, click **Add a new section**.
4. Name the section `atelier-hero` (this creates `sections/atelier-hero.liquid`).
5. Open [atelier-hero.liquid](file:///c:/Open%20code%20AI/Tan%20Lerida/Shopify-Theme/sections/atelier-hero.liquid) in the workspace, copy the entire file contents, and paste them into the editor.
6. Click **Save**.

### Step B: Add Custom Styling Overrides
1. Inside the Shopify code editor, find the **Assets** folder.
2. Select your main CSS stylesheet (usually named `theme.css`, `base.css`, or `global.css`).
3. Scroll to the very bottom of this stylesheet.
4. Open [tan-lerida-custom.css](file:///c:/Open%20code%20AI/Tan%20Lerida/Shopify-Theme/assets/tan-lerida-custom.css) in the workspace, copy the style overrides, and paste them at the bottom of your file.
5. Click **Save**.

### Step C: Configure Section in Customizer
1. Go back to **Online Store > Themes** and click **Customize** on your active theme.
2. In the home page editor, click **Add section** in the left sidebar and select **Atelier Hero**.
3. In the section settings panel, upload your matched image pair:
   - **Base image**: The finished leather item lying on the work bench.
   - **Reveal image**: The exact same framing/angle photo taken during the cutting/stitching process.
4. Edit the text and button URL as required. The spotlight tracking reveal effect will activate automatically!

---

## 2. Developer Integration (Shopify CLI)

If you are developing locally using the Shopify CLI:

### Step A: Environment Configuration
Make sure the environment variables are active in your local project workspace:
```env
SHOPIFY_STORE_DOMAIN=tan-lerida.myshopify.com
SHOPIFY_THEME_ID=197507121233
```

### Step B: Sync Files using Shopify CLI
1. Log in to your Shopify organization using terminal:
   ```bash
   shopify login
   ```
2. Navigate to your theme directory and pull the latest code:
   ```bash
   shopify theme pull --store=tan-lerida.myshopify.com
   ```
3. Copy the folders `sections/`, `layout/`, `templates/`, and `assets/` from `Tan Lerida/Shopify-Theme` directly into your local theme directory.
4. Deploy the theme changes:
   ```bash
   shopify theme push --store=tan-lerida.myshopify.com --theme=197507121233
   ```

---

## 3. Custom shopify MCP Server

To let your AI coding assistant directly read, edit, and sync files on your Shopify theme via the Shopify Admin API:
1. Generate an Admin API access token in Shopify Admin (**Settings > Apps and sales channels > Develop apps**). Ensure it has `write_theme_assets` and `read_theme_assets` access scopes.
2. Set this token in your local `.env` or `.env.local` file:
   ```env
   SHOPIFY_ADMIN_API_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxxxxx
   ```
3. The custom **shopify** MCP server is registered in [mcp_config.json](file:///c:/Open%20code%20AI/mcp_config.json) and will now expose theme manipulation tools directly to the assistant.
