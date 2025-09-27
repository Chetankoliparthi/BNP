# backend/app.py
import os
from dotenv import load_dotenv

load_dotenv()
import json
from flask import Flask, request, render_template, redirect, url_for
from stock_analyzer import evaluate_stock_metrics
from portfolio_analyzer import analyze_portfolio

app = Flask(__name__)

# --- Load All Data on Startup ---
try:
    with open('StockTickerSymbols.json', 'r') as f:
        stocks_data = {stock['stockSymbol']: stock for stock in json.load(f)}
    STOCK_SYMBOLS_LIST = sorted(stocks_data.keys())
    
    with open('ClientPortfolio.json', 'r') as f:
        clients_data = {client['clientId']: client for client in json.load(f)}
    CLIENT_ID_LIST = sorted(clients_data.keys())
    
    print("Successfully loaded all data files.")
except Exception as e:
    print(f"ERROR loading data files: {e}")
    stocks_data, STOCK_SYMBOLS_LIST, clients_data, CLIENT_ID_LIST = {}, [], {}, []

# --- Routes ---

@app.route('/')
def index():
    return redirect(url_for('stock_evaluator_page'))

@app.route('/stock-evaluator')
def stock_evaluator_page():
    result = None
    selected_symbol = request.args.get('stock_symbol')
    if selected_symbol and selected_symbol in stocks_data:
        result = evaluate_stock_metrics(stocks_data[selected_symbol])
    
    return render_template('stock_evaluator.html', stock_symbols=STOCK_SYMBOLS_LIST, result=result)

@app.route('/portfolio')
@app.route('/portfolio/<client_id>')
def portfolio_analyzer_page(client_id=None):
    results = None
    if client_id and client_id in clients_data:
        portfolio = clients_data[client_id]
        results = analyze_portfolio(portfolio.get('funds', []))
    
    return render_template('portfolio_analyzer.html', client_ids=CLIENT_ID_LIST, selected_client_id=client_id, results=results)

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)