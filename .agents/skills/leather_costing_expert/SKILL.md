---
name: leather-costing-expert
description: Calculations and logic for raw leather costing, waste factors, compliance markups, and margin models.
---

# Leather Costing Expert Skill

Use this skill when calculating costs, preparing price quotes, or analyzing manufacturing margins for B2B bulk or D2C retail orders.

## 1. Direct Costs Formula

*   **Direct Material Cost (Leather)**:
    $$\text{Leather Cost} = \text{sqft per unit} \times (1 + \text{Waste Factor}) \times \text{Quantity} \times \text{Price per sqft}$$
    *   *Bulk (B2B) Waste Factor*: `0.15` (15%)
    *   *Retail (D2C) Waste Factor*: `0.20` (20%)
*   **Direct Labor Cost**:
    $$\text{Labor Cost} = \text{Labor Hours} \times \text{Labor Rate per Hour} \times \text{Quantity}$$
    *   *Default Labor Rate*: `$2.50` per hour (India factory base rate)
*   **Hardware & Consumables Cost**:
    $$\text{Hardware Cost} = \text{Hardware Cost per unit} \times \text{Quantity}$$

## 2. Overhead & Compliance Markups

Overhead and compliance markups are applied directly to the sum of direct costs (Leather + Labor + Hardware):
*   **Direct Costs Subtotal**:
    $$\text{Direct Costs} = \text{Leather Cost} + \text{Labor Cost} + \text{Hardware Cost}$$
*   **Factory Overhead**: `10%` of Direct Costs ($0.10 \times \text{Direct Costs}$)
*   **Compliance Markup**: `8%` of Direct Costs ($0.08 \times \text{Direct Costs}$) for LWG Gold / SEDEX audits and overhead.
*   **Packaging**:
    *   *Bulk (B2B)*: `$1.50` per unit for standard carton packaging.
    *   *Retail (D2C)*: `$4.00` per unit for premium gift boxes and dust bags.

## 3. Selling Price & Margin Models

### Bulk (B2B) Pricing Model
*   **Minimum Order Quantity (MOQ)**: 50 units.
*   **Total FOB Cost**: Direct Costs + Overhead + Compliance + Packaging + Shipping.
*   **Target Profit Margin**: `20%` (FOB Selling Price = Cost per unit / 0.80).

### Retail (D2C) Pricing Model
*   **Minimum Order Quantity (MOQ)**: 1 unit.
*   **Total Cost per unit**: Direct Costs + Packaging + Marketing/Platform Fees.
*   **Target Multiplier**: `4.0x` (Retail Selling Price = Cost per unit * 4).
