# backend/stock_analyzer.py

def evaluate_stock_metrics(stock):
    """
    Analyzes a stock's financial parameters based on predefined rules.
    """
    p = stock['parameters']
    feedback = {}

    # 1. Price-Earnings Ratio
    pe_ratio = p.get('priceEarningsRatio', 0)
    if pe_ratio < 15:
        feedback['priceEarningsRatio'] = f"The P/E ratio of {pe_ratio} suggests the stock is cheap relative to earnings."
    elif 15 <= pe_ratio <= 30:
        feedback['priceEarningsRatio'] = f"The P/E ratio of {pe_ratio} is fairly typical."
    else:
        feedback['priceEarningsRatio'] = f"The P/E ratio of {pe_ratio} indicates the stock is relatively expensive."

    # 2. Earnings Per Share
    eps = p.get('earningsPerShare', 0)
    if eps < 1:
        feedback['earningsPerShare'] = f"The EPS of {eps} is low; profitability may be a concern."
    elif eps < 5:
        feedback['earningsPerShare'] = f"The EPS of {eps} shows modest profitability."
    else:
        feedback['earningsPerShare'] = f"The EPS of {eps} is a strong indicator of profitability."

    # 3. Dividend Yield
    div_yield = p.get('dividendYield', 0)
    if div_yield < 1:
        feedback['dividendYield'] = f"The dividend yield of {div_yield}% is lower than the market average."
    elif div_yield <= 3:
        feedback['dividendYield'] = f"The dividend yield of {div_yield}% is around the market norm."
    else:
        feedback['dividendYield'] = f"The dividend yield of {div_yield}% is attractive for income-focused investors."

    # 4. Market Cap
    market_cap = p.get('marketCap', 0)
    mc_trillions = market_cap / 1e12
    if market_cap >= 5e14: # 500 Trillion
        feedback['marketCap'] = f"The market cap of ${mc_trillions:.1f} trillion makes this one of the world's giants."
    elif market_cap >= 1e14: # 100 Trillion
        feedback['marketCap'] = f"The market cap of ${mc_trillions:.1f} trillion indicates a very large, stable company."
    else:
        feedback['marketCap'] = f"The market cap of ${mc_trillions:.2f} trillion indicates a sizable player."

    # 5. Debt-to-Equity Ratio
    de_ratio = p.get('debtToEquityRatio', 0)
    if de_ratio < 0.5:
        feedback['debtToEquityRatio'] = f"The debt-to-equity ratio of {de_ratio} suggests very little leverage."
    elif de_ratio <= 1.5:
        feedback['debtToEquityRatio'] = f"The debt-to-equity ratio of {de_ratio} suggests a moderate level of leverage."
    else:
        feedback['debtToEquityRatio'] = f"The debt-to-equity ratio of {de_ratio} indicates high leverage."

    # 6. Return on Equity
    roe = p.get('returnOnEquity', 0) * 100
    if roe < 8:
        feedback['returnOnEquity'] = f"The ROE of {roe:.0f}% is below average."
    elif roe <= 15:
        feedback['returnOnEquity'] = f"The ROE of {roe:.0f}% is healthy."
    else:
        feedback['returnOnEquity'] = f"The ROE of {roe:.0f}% is very strong."

    # 7. Return on Assets
    roa = p.get('returnOnAssets', 0) * 100
    if roa < 5:
        feedback['returnOnAssets'] = f"The ROA of {roa:.0f}% is modest."
    elif roa <= 10:
        feedback['returnOnAssets'] = f"The ROA of {roa:.0f}% indicates efficient asset utilization."
    else:
        feedback['returnOnAssets'] = f"The ROA of {roa:.0f}% is excellent."

    # 8. Current Ratio
    current_ratio = p.get('currentRatio', 0)
    if current_ratio < 1:
        feedback['currentRatio'] = f"The current ratio of {current_ratio} signals potential short-term liquidity issues."
    elif current_ratio <= 2:
        feedback['currentRatio'] = f"The current ratio of {current_ratio} suggests a good short-term liquidity position."
    else:
        feedback['currentRatio'] = f"The current ratio of {current_ratio} indicates a very comfortable liquidity cushion."

    # 9. Quick Ratio
    quick_ratio = p.get('quickRatio', 0)
    if quick_ratio < 1:
        feedback['quickRatio'] = f"The quick ratio of {quick_ratio} may be insufficient for immediate obligations."
    elif quick_ratio <= 2:
        feedback['quickRatio'] = f"The quick ratio of {quick_ratio} indicates a strong ability to meet short-term obligations."
    else:
        feedback['quickRatio'] = f"The quick ratio of {quick_ratio} shows an exceptionally strong liquidity position."

    # 10. Book Value Per Share
    bvps = p.get('bookValuePerShare', 0)
    feedback['bookValuePerShare'] = f"The book value per share of {bvps} is a measure of the company's net asset value."

    # Build summary
    summary = (
        f"Overall, {stock['stockSymbol']} has some notable financial metrics. "
        f"{feedback['earningsPerShare']} {feedback['returnOnEquity']} "
        f"However, {feedback['priceEarningsRatio'].lower()} "
        f"The company's leverage is characterized by the following: {feedback['debtToEquityRatio'].lower()} "
        f"Finally, its liquidity position appears as follows: {feedback['currentRatio'].lower()}"
    )

    return {
            "stockSymbol": stock['stockSymbol'],
            "parameters": p, # Add this line to pass raw parameters
            "feedback": feedback,
            "summary": summary
        }