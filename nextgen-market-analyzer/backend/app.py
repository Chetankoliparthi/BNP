# backend/app.py
import json
from flask import Flask, request, render_template, redirect, url_for
from stock_analyzer import evaluate_stock_metrics
from portfolio_analyzer import analyze_portfolio  # Import the new function

app = Flask(__name__)

# --- Load Data on Startup ---
try:
    with open('StockTickerSymbols.json', 'r') as f:
        stocks_data = {stock['stockSymbol']: stock for stock in json.load(f)}
    print(f"Successfully loaded {len(stocks_data)} stocks.")
except Exception as e:
    print(f"ERROR loading stock data: {e}")
    stocks_data = {}

# --- HTML Rendering Routes ---

@app.route('/')
def index():
    return redirect(url_for('stock_evaluator_page'))

@app.route('/stock-evaluator')
def stock_evaluator_page():
    return render_template('stock_evaluator.html')

@app.route('/portfolio')
def portfolio_analyzer_page():
    """Renders the new form for portfolio input."""
    return render_template('portfolio_form.html')
    
@app.route('/evaluate', methods=['POST'])
def evaluate_stock():
    # ... (This function remains unchanged)
    error = None
    result = None
    try:
        symbol = request.form.get('stock_symbol')
        if not symbol:
            error = "Stock symbol cannot be empty."
        else:
            stock_to_evaluate = stocks_data.get(symbol.upper())
            if not stock_to_evaluate:
                error = f"Stock symbol '{symbol}' not found in our database."
            else:
                result = evaluate_stock_metrics(stock_to_evaluate)
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")
        error = "An internal error occurred. Please try again later."
    return render_template('stock_evaluator.html', result=result, error=error)

@app.route('/analyze-portfolio', methods=['POST'])
def analyze_portfolio_submission():
    """Processes the dynamic portfolio form and displays the results."""
    try:
        form_data = request.form
        num_funds = int(form_data.get('num_funds', 0))
        
        funds = []
        for i in range(num_funds):
            fund_data = {
                "fundCode": f"FUND_{i+1}",
                "amount": float(form_data.get(f'fund-{i}-amount')),
                "holdings": {}
            }
            # Find all holdings for the current fund
            j = 0
            while True:
                ticker = form_data.get(f'fund-{i}-holding-{j}-ticker')
                weight = form_data.get(f'fund-{i}-holding-{j}-weight')
                if ticker and weight:
                    fund_data["holdings"][ticker.upper()] = float(weight)
                    j += 1
                else:
                    break # No more holdings for this fund
            funds.append(fund_data)
        
        # Perform the analysis
        results = analyze_portfolio(funds)
        
        # If the analysis returns an error, show the form again with the error
        if results.get('error'):
            return render_template('portfolio_form.html', error=results.get('error'))

        return render_template('portfolio_analyzer.html', results=results)

    except Exception as e:
        print(f"Error processing portfolio: {e}")
        return render_template('portfolio_form.html', error="Invalid data submitted. Please check your inputs and try again.")

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)