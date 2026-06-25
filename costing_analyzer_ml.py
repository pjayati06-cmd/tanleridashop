import os
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from jinja2 import Template

class CostingMLAnalyzer:
    def __init__(self):
        # Brand Tokens (for styling output reports)
        self.brand_colors = {
            "ink_black": "#1A1714",
            "signature_gold": "#B8933E",
            "tannery_green": "#2C4A3E",
            "warm_white": "#F5F0E8",
            "stone_grey": "#8C8680"
        }
        self.grade_map = {"A": 0.10, "B": 0.15, "C": 0.22}
        self.model = None
        self._generate_historical_data()
        self._train_model()

    def _generate_historical_data(self):
        """Generates synthetic historical batch data to train the model."""
        np.random.seed(42)
        n_samples = 200
        
        # Random quantities (10 to 500 units)
        quantities = np.random.randint(10, 500, n_samples)
        
        # Random hide grades (A, B, or C)
        grades = np.random.choice(["A", "B", "C"], n_samples)
        
        # Real waste factor baseline depends on grade (A=10%, B=15%, C=22%)
        # Large quantities reduce waste slightly (up to -3%) due to nesting optimization
        waste_factors = []
        for qty, grade in zip(quantities, grades):
            base_waste = self.grade_map[grade]
            qty_discount = min(0.04, (qty / 1000.0))  # nesting discount
            random_noise = np.random.normal(0, 0.015)   # random human factor
            actual_waste = max(0.05, base_waste - qty_discount + random_noise)
            waste_factors.append(actual_waste)
            
        self.df = pd.DataFrame({
            "quantity": quantities,
            "grade": grades,
            "actual_waste": waste_factors
        })
        
    def _train_model(self):
        """Trains a Linear Regression model to predict waste factors."""
        # Convert grades to numeric features (One-Hot Encoding)
        X = pd.get_dummies(self.df[["quantity", "grade"]], columns=["grade"], drop_first=True)
        y = self.df["actual_waste"]
        
        self.model = LinearRegression()
        self.model.fit(X, y)
        
        # Save features list to ensure correct columns when predicting
        self.feature_cols = X.columns.tolist()

    def predict_waste_factor(self, quantity: int, grade: str) -> float:
        """Predicts waste factor using the trained ML model."""
        input_data = pd.DataFrame([{"quantity": quantity, "grade": grade}])
        X_pred = pd.get_dummies(input_data, columns=["grade"])
        
        # Align with training columns
        for col in self.feature_cols:
            if col not in X_pred.columns:
                X_pred[col] = 0
        X_pred = X_pred[self.feature_cols]
        
        predicted = self.model.predict(X_pred)[0]
        # Keep within logical boundaries [5%, 40%]
        return float(np.clip(predicted, 0.05, 0.40))

    def calculate_ml_costing(self, product: str, sqft_per_unit: float, price_per_sqft: float,
                              labor_hours: float, hardware_cost: float, qty: int, grade: str) -> dict:
        """Calculates costing details using the ML predicted waste factor."""
        predicted_waste = self.predict_waste_factor(qty, grade)
        
        # 1. Direct Material
        total_sqft = sqft_per_unit * (1 + predicted_waste) * qty
        leather_cost = total_sqft * price_per_sqft
        
        # 2. Direct Labor
        labor_cost = labor_hours * 2.50 * qty  # $2.50 / hr
        
        # 3. Direct Hardware
        hardware_total = hardware_cost * qty
        
        # 4. Direct Cost Subtotal
        direct_subtotal = leather_cost + labor_cost + hardware_total
        
        # 5. Overheads & Markups
        overhead = direct_subtotal * 0.10
        compliance = direct_subtotal * 0.08
        packaging = 1.50 * qty if qty >= 50 else 4.00 * qty
        
        total_cost = direct_subtotal + overhead + compliance + packaging
        cost_per_unit = total_cost / qty
        
        # Margins: 20% for bulk (qty >= 50), 4.0x multiplier for retail (qty < 50)
        if qty >= 50:
            selling_price = cost_per_unit / 0.80
            margin_type = "20% Margin (Bulk B2B)"
        else:
            selling_price = cost_per_unit * 4.0
            margin_type = "4.0x Multiplier (Retail D2C)"

        return {
            "product": product,
            "quantity": qty,
            "grade": grade,
            "predicted_waste": f"{predicted_waste * 100:.2f}%",
            "sqft_per_unit": sqft_per_unit,
            "total_sqft_used": f"{total_sqft:.2f}",
            "breakdown": {
                "leather_cost_unit": f"${(leather_cost/qty):.2f}",
                "labor_cost_unit": f"${(labor_cost/qty):.2f}",
                "hardware_cost_unit": f"${hardware_cost:.2f}",
                "overhead_unit": f"${(overhead/qty):.2f}",
                "compliance_unit": f"${(compliance/qty):.2f}",
                "packaging_unit": f"${(packaging/qty):.2f}",
                "total_cost_unit": f"${cost_per_unit:.2f}"
            },
            "recommended_price": f"${selling_price:.2f}",
            "margin_applied": margin_type
        }

    def generate_html_report(self, costing_result: dict, filename: str = "costing_report.html"):
        """Generates a premium HTML report following the brand design rules."""
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tan Lerida - ML Costing Pack</title>
            <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
            <style>
                :root {
                    --ink-black: {{ colors.ink_black }};
                    --sig-gold: {{ colors.signature_gold }};
                    --tan-green: {{ colors.tannery_green }};
                    --warm-white: {{ colors.warm_white }};
                    --stone-grey: {{ colors.stone_grey }};
                }
                body {
                    background-color: var(--warm-white);
                    color: var(--ink-black);
                    font-family: 'Inter', sans-serif;
                    margin: 0;
                    padding: 40px 20px;
                    line-height: 1.6;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 40px;
                    border-radius: 4px;
                    box-shadow: 0px 8px 24px rgba(26, 23, 20, 0.04);
                }
                header {
                    text-align: center;
                    border-bottom: 2px solid var(--warm-white);
                    padding-bottom: 30px;
                    margin-bottom: 30px;
                }
                .brand-title {
                    font-family: 'Cormorant Garamond', serif;
                    font-size: 2.5rem;
                    letter-spacing: 0.05em;
                    color: var(--sig-gold);
                    margin: 0;
                    text-transform: uppercase;
                    font-weight: 600;
                }
                .brand-tagline {
                    font-family: 'Cormorant Garamond', serif;
                    font-style: italic;
                    color: var(--stone-grey);
                    margin-top: 5px;
                    font-size: 1.1rem;
                }
                h2 {
                    font-family: 'Cormorant Garamond', serif;
                    font-size: 1.8rem;
                    color: var(--ink-black);
                    margin-top: 0;
                    margin-bottom: 20px;
                    font-weight: 600;
                }
                .meta-table {
                    width: 100%;
                    margin-bottom: 30px;
                    background-color: var(--warm-white);
                    border-radius: 4px;
                    padding: 20px;
                }
                .grid-2 {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                }
                .meta-item {
                    display: flex;
                    justify-content: space-between;
                    padding: 8px 0;
                }
                .meta-label {
                    color: var(--stone-grey);
                    font-weight: 600;
                    font-size: 0.85rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
                .meta-value {
                    font-weight: 600;
                    color: var(--ink-black);
                }
                table.breakdown-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 30px 0;
                }
                table.breakdown-table th {
                    text-align: left;
                    background-color: var(--ink-black);
                    color: #ffffff;
                    padding: 12px;
                    font-size: 0.85rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
                table.breakdown-table td {
                    padding: 12px;
                    border-bottom: 1px solid var(--warm-white);
                }
                table.breakdown-table tr:hover {
                    background-color: var(--warm-white);
                }
                .total-row {
                    font-weight: 600;
                    background-color: var(--warm-white);
                }
                .pricing-card {
                    background-color: var(--ink-black);
                    color: #ffffff;
                    padding: 30px;
                    border-radius: 4px;
                    text-align: center;
                    margin-top: 30px;
                }
                .price-title {
                    font-family: 'Cormorant Garamond', serif;
                    font-size: 1.2rem;
                    color: var(--sig-gold);
                    margin: 0;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
                .price-value {
                    font-size: 3rem;
                    font-weight: 600;
                    color: #ffffff;
                    margin: 10px 0;
                }
                .price-badge {
                    background-color: var(--tan-green);
                    display: inline-block;
                    padding: 6px 15px;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin-top: 5px;
                }
                footer {
                    margin-top: 40px;
                    text-align: center;
                    font-size: 0.75rem;
                    color: var(--stone-grey);
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <div class="brand-title">Tan Lerida</div>
                    <div class="brand-tagline">Made for Living  ·  Luxury is Handmade</div>
                </header>
                
                <h2>Machine Learning Costing Pack</h2>
                
                <div class="meta-table grid-2">
                    <div>
                        <div class="meta-item">
                            <span class="meta-label">Product Spec</span>
                            <span class="meta-value">{{ data.product }}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Order Quantity</span>
                            <span class="meta-value">{{ data.quantity }} units</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Leather Hide Grade</span>
                            <span class="meta-value">Grade {{ data.grade }}</span>
                        </div>
                    </div>
                    <div>
                        <div class="meta-item">
                            <span class="meta-label">ML Predicted Waste</span>
                            <span class="meta-value" style="color: var(--sig-gold);">{{ data.predicted_waste }}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Sqft/Unit (Net)</span>
                            <span class="meta-value">{{ data.sqft_per_unit }} sq ft</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Total Sqft (Gross)</span>
                            <span class="meta-value">{{ data.total_sqft_used }} sq ft</span>
                        </div>
                    </div>
                </div>

                <h2>Cost Breakdown (Per Unit)</h2>
                <table class="breakdown-table">
                    <thead>
                        <tr>
                            <th>Cost Head</th>
                            <th>Cost Per Unit</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Direct Material (Leather with waste)</td>
                            <td>{{ data.breakdown.leather_cost_unit }}</td>
                        </tr>
                        <tr>
                            <td>Direct Labor (Manufacturing)</td>
                            <td>{{ data.breakdown.labor_cost_unit }}</td>
                        </tr>
                        <tr>
                            <td>Hardware & Consumables</td>
                            <td>{{ data.breakdown.hardware_cost_unit }}</td>
                        </tr>
                        <tr>
                            <td>Factory Overhead (10%)</td>
                            <td>{{ data.breakdown.overhead_unit }}</td>
                        </tr>
                        <tr>
                            <td>LWG Gold & SEDEX Compliance (8%)</td>
                            <td>{{ data.breakdown.compliance_unit }}</td>
                        </tr>
                        <tr>
                            <td>Packaging & Gift Box</td>
                            <td>{{ data.breakdown.packaging_unit }}</td>
                        </tr>
                        <tr class="total-row">
                            <td>Total Cost Per Unit (Excluding Shipping)</td>
                            <td>{{ data.breakdown.total_cost_unit }}</td>
                        </tr>
                    </tbody>
                </table>

                <div class="pricing-card">
                    <div class="price-title">Recommended Selling Price</div>
                    <div class="price-value">{{ data.recommended_price }}</div>
                    <div class="price-badge">{{ data.margin_applied }}</div>
                </div>

                <footer>
                    Established 1991  ·  LWG Gold Certified  ·  SEDEX Compliant  ·  Tan Lerida Leather House
                </footer>
            </div>
        </body>
        </html>
        """
        template = Template(html_template)
        rendered_html = template.render(data=costing_result, colors=self.brand_colors)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        print(f"Report generated successfully: {filename}")

if __name__ == "__main__":
    analyzer = CostingMLAnalyzer()
    # Let's run a test calculation for a B2B Bomber Jacket order
    res = analyzer.calculate_ml_costing(
        product="Bomber Jacket",
        sqft_per_unit=18.0,
        price_per_sqft=4.20,
        labor_hours=6.5,
        hardware_cost=12.50,
        qty=120,
        grade="B"
    )
    analyzer.generate_html_report(res)
