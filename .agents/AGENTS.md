# Open Code AI Project Rules

## 1. General Principles

*   **Professional & Conversational**: Write in a warm, direct, and professional tone. Avoid corporate jargon.
*   **Conciseness**: Keep summaries under 300 words. Say the thing and stop.
*   **Decisive Recommendations**: Provide one strong recommendation rather than multiple choices unless specifically asked.
*   **Memory System**: Read MEMORY.md at the start of every session to align with the current state.
*   **No Placeholders**: Never use placeholder images or content. Use `generate_image` or real assets.

---

## 2. Email Copywriting & Formality Rules (Email HQ)

*   **Preparation**: Before drafting, check if a thread with the recipient exists. Reply in the existing thread instead of starting a new one.
*   **Opener Rhythm**: Use the structure: warm opener (1 sentence) → context (1-2 sentences) → ask/information (1-2 sentences) → brief close.
*   **Greeting Defaults**:
    *   Named contacts: "Hi [Name],"
    *   Institutional/generic: "Hi," with no name.
*   **Sign-off**: Default sign-off is "Best regards" followed by a line break and "Jayti Pargal."
*   **Formality by Recipient**:
    *   *Institutional / Complaints*: Prose only, no bullets. State precise facts (numbers, dates, expected vs. actual). End with: "Could you please check this at your end and let me know." No drama.
    *   *Professional Contacts*: Use warmth words ("lovely", "genuinely excited").
*   **Prose Over Bullets**: Use prose for email bodies. Bullet only genuinely parallel items.
*   **Single Ask**: One ask per email. Sequence multiple points as short paragraphs.

---

## 3. Brand Compliance & Creative Rules (Tan Lerida)

*   **Colors**:
    *   Ink Black: `#1A1714` (packaging, background, hero surfaces)
    *   Signature Gold: `#B8933E` (logo, accents, typography)
    *   Tannery Green: `#2C4A3E` (CTAs and buttons only)
    *   Warm White: `#F5F0E8` (editorial backgrounds)
    *   Stone Grey: `#8C8680` (secondary text)
*   **Typography**:
    *   Headings/Display: Cormorant Garamond / EB Garamond
    *   UI labels/Navigation: Inter
    *   Specs/Measurements: Courier New / Courier Prime
*   **The "No-Line" Rule**: Do not use 1px solid borders to section off major layout areas. Define boundaries using background color shifts (e.g. `surface-container-low` on `surface`) or whitespace.
*   **Visual Aesthetics**:
    *   Use directional warm natural lighting. No flat studio fill, no white backgrounds.
    *   Use 0.25rem (`ROUND_FOUR`) corner radius for buttons and interactive elements.
    *   Always show natural leather texture and patina.
*   **Vocabulary Compliance**:
    *   *Reach for*: `you`, `we`, `our tannery`, `full-grain`, `35 years`, `70 years`, `softens`, `shaped`, `patina`, `at source`, `hide to hand`, `made for living`.
    *   *Never use*: `luxury` (standalone), `premium`, `exclusive`, `elevate`, `curated`, `effortless`, `sustainable` (standalone), `discerning`, `artisanal`, `bespoke`.

---

## 4. Costing & Manufacturing Rules (SPC Leather)

*   **Waste Factors**: Use `0.15` (15%) waste for bulk/B2B cutting, and `0.20` (20%) waste for retail/small-batch.
*   **Profit Margins**: Apply 20% margin for Bulk (FOB price = cost / 0.80) and 4x multiplier for Retail D2C.
*   **Compliance & Overhead**: Apply 10% overhead and 8% compliance markup (LWG Gold/SEDEX) to direct costs (materials, labor, hardware).
