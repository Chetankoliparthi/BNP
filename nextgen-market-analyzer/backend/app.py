# backend/app.py
import json
from flask import Flask, request, render_template, redirect, url_for
from stock_analyzer import evaluate_stock_metrics
from portfolio_analyzer import analyze_portfolio

app = Flask(__name__)
# ... (rest of the app setup is the same) ...
# ... (stock data loading is the same) ...
# ... (index, stock_evaluator_page, portfolio_analyzer_page, evaluate_stock routes are the same) ...

@app.route('/analyze-portfolio', methods=['POST'])
def analyze_portfolio_submission():
    """Processes portfolio from either the dynamic form or a pasted JSON object."""
    try:
        input_method = request.form.get('input_method')
        funds = []

        if input_method == 'json':
            json_data_str = request.form.get('json_data')
            if not json_data_str:
                return render_template('portfolio_form.html', error="JSON data cannot be empty.")
            
            try:
                portfolio_data = json.loads(json_data_str)
                funds = portfolio_data.get('funds', [])
            except json.JSONDecodeError:
                return render_template('portfolio_form.html', error="Invalid JSON format. Please check your data.")

        else: # Default to 'form' method
            num_funds = int(request.form.get('num_funds', 0))
            for i in range(num_funds):
                fund_data = {
                    "fundCode": f"FUND_{i+1}",
                    "amount": float(request.form.get(f'fund-{i}-amount')),
                    "holdings": {}
                }
                j = 0
                while True:
                    ticker = request.form.get(f'fund-{i}-holding-{j}-ticker')
                    weight = request.form.get(f'fund-{i}-holding-{j}-weight')
                    if ticker and weight:
                        fund_data["holdings"][ticker.upper()] = float(weight)
                        j += 1
                    else:
                        break
                funds.append(fund_data)
        
        if not funds:
            return render_template('portfolio_form.html', error="No fund data was provided.")

        results = analyze_portfolio(funds)
        
        if results.get('error'):
            return render_template('portfolio_form.html', error=results.get('error'))

        return render_template('portfolio_analyzer.html', results=results)

    except Exception as e:
        print(f"Error processing portfolio: {e}")
        return render_template('portfolio_form.html', error="Invalid data submitted. Please check your inputs.")

# --- Keep the rest of app.py the same ---
# ... (The main execution block) ...
if __name__ == '__main__':
    app.run(debug=True, port=5000)