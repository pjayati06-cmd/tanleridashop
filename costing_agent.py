"""
SPC Leather Costing Agent
Calculates accurate costs for Bulk (B2B) and Retail (D2C) orders.
Handles: Leather consumption, waste factors, labor, compliance, shipping, and margins.
"""

import json
from typing import Optional

class CostingAgent:
    def __init__(self):
        # Base Constants (You can adjust these based on current market rates)
        self.currency = "USD"
        self.leather_waste_factor_bulk = 0.15  # 15% waste for bulk cutting
        self.leather_waste_factor_retail = 0.20 # 20% waste for small batch/retail
        self.labor_rate_per_hour = 2.50  # Example: India labor rate
        self.compliance_markup = 0.08    # 8% for LWG/REACH overhead
        
        # Configuration
        self.bulk_moq = 50
        self.retail_moq = 1

    def calculate_leather_cost(self, sqft_per_unit: float, price_per_sqft: float, qty: int, is_bulk: bool = True):
        """Calculates total leather cost including waste."""
        waste_factor = self.leather_waste_factor_bulk if is_bulk else self.leather_waste_factor_retail
        total_sqft_needed = sqft_per_unit * (1 + waste_factor) * qty
        total_leather_cost = total_sqft_needed * price_per_sqft
        return {
            "raw_leather_cost": total_leather_cost,
            "waste_factor": waste_factor,
            "total_sqft_used": total_sqft_needed,
            "cost_per_unit_leather": total_leather_cost / qty
        }

    def calculate_bulk_cost(self, product_type: str, sqft_per_unit: float, leather_price: float, 
                            labor_hours: float, hardware_cost: float, shipping_per_unit: float, qty: int):
        """
        Calculates B2B Bulk Cost (FOB).
        Includes: Leather, Labor, Overhead, Compliance, Packaging, Shipping.
        """
        if qty < self.bulk_moq:
            return {"error": f"Quantity {qty} is below B2B MOQ of {self.bulk_moq}"}

        # 1. Leather
        leather_data = self.calculate_leather_cost(sqft_per_unit, leather_price, qty, is_bulk=True)
        
        # 2. Labor
        total_labor_cost = labor_hours * self.labor_rate_per_hour * qty
        
        # 3. Hardware & Consumables
        total_hardware = hardware_cost * qty
        
        # 4. Overhead & Compliance (Factory rent, utilities, LWG audit, R&D)
        # Usually calculated as % of direct costs or fixed per unit
        direct_costs = leather_data["raw_leather_cost"] + total_labor_cost + total_hardware
        overhead_cost = direct_costs * 0.10 # 10% overhead
        compliance_cost = direct_costs * self.compliance_markup
        
        # 5. Packaging & Logistics
        packaging_cost = 1.50 * qty # Example: $1.50 per unit for polybag/carton
        total_shipping = shipping_per_unit * qty
        
        # Total Cost
        total_cost = (leather_data["raw_leather_cost"] + total_labor_cost + total_hardware + 
                      overhead_cost + compliance_cost + packaging_cost + total_shipping)
        
        cost_per_unit = total_cost / qty
        
        # Add Profit Margin (e.g., 20% for Bulk)
        margin = 0.20
        selling_price = cost_per_unit / (1 - margin)
        
        return {
            "type": "BULK_B2B",
            "qty": qty,
            "breakdown": {
                "leather": f"{leather_data['cost_per_unit_leather']:.2f}",
                "labor": f"{(total_labor_cost/qty):.2f}",
                "hardware": f"{hardware_cost:.2f}",
                "overhead": f"{(overhead_cost/qty):.2f}",
                "compliance": f"{(compliance_cost/qty):.2f}",
                "packaging": f"{packaging_cost/qty:.2f}",
                "shipping": f"{shipping_per_unit:.2f}",
                "total_cost_per_unit": f"{cost_per_unit:.2f}"
            },
            "recommended_fob_price": f"{selling_price:.2f}",
            "margin_applied": f"{margin*100}%",
            "notes": "Price valid for FOB India. MOQ applies."
        }

    def calculate_retail_cost(self, product_type: str, sqft_per_unit: float, leather_price: float,
                              labor_hours: float, hardware_cost: float, marketing_per_unit: float):
        """
        Calculates Retail (D2C/Tan Lerida) Cost.
        Includes: Higher waste, packaging, marketing, platform fees, higher margin.
        """
        # 1. Leather (Higher waste for small batches)
        leather_data = self.calculate_leather_cost(sqft_per_unit, leather_price, 1, is_bulk=False)
        
        # 2. Labor (Often higher per unit for small batch attention)
        labor_cost = labor_hours * self.labor_rate_per_hour
        
        # 3. Hardware
        hardware_total = hardware_cost
        
        # 4. Premium Packaging (Gift boxes, dust bags)
        premium_packaging = 4.00 
        
        # 5. Marketing & Platform Fees (Amazon/Shopify + Ads)
        marketing_cost = marketing_per_unit
        
        # Total Cost
        total_cost = (leather_data["raw_leather_cost"] + labor_cost + hardware_total + 
                      premium_packaging + marketing_cost)
        
        # Retail Margin (Usually 3.5x to 5x cost)
        margin_multiplier = 4.0 
        retail_price = total_cost * margin_multiplier
        
        return {
            "type": "RETAIL_D2C",
            "breakdown": {
                "leather": f"{leather_data['cost_per_unit_leather']:.2f}",
                "labor": f"{labor_cost:.2f}",
                "hardware": f"{hardware_cost:.2f}",
                "packaging": f"{premium_packaging:.2f}",
                "marketing": f"{marketing_cost:.2f}",
                "total_cost_per_unit": f"{total_cost:.2f}"
            },
            "recommended_retail_price": f"{retail_price:.2f}",
            "margin_multiplier": f"{margin_multiplier}x",
            "notes": "Includes premium packaging and marketing. Price for Tan Lerida brand."
        }

    def run_costing_session(self):
        """Interactive CLI to run costing."""
        print("--- SPC Leather Costing Agent ---")
        print("1. Bulk Order (B2B)")
        print("2. Retail Order (Tan Lerida D2C)")
        choice = input("Select mode (1 or 2): ")

        # Common Inputs
        product = input("Product Name (e.g., Bomber Jacket): ")
        sqft = float(input("Leather usage per unit (sq ft): "))
        leather_price = float(input("Leather cost per sq ft ($): "))
        labor_hrs = float(input("Labor hours per unit: "))
        hardware = float(input("Hardware cost per unit ($): "))

        if choice == "1":
            qty = int(input("Quantity (MOQ 50+): "))
            shipping = float(input("Estimated shipping per unit to destination ($): "))
            result = self.calculate_bulk_cost(product, sqft, leather_price, labor_hrs, hardware, shipping, qty)
        else:
            marketing = float(input("Estimated marketing/platform fee per unit ($): "))
            result = self.calculate_retail_cost(product, sqft, leather_price, labor_hrs, hardware, marketing)

        print("\n--- COSTING RESULT ---")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    agent = CostingAgent()
    agent.run_costing_session()