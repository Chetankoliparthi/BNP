from itertools import combinations

TICKER_TO_SECTOR = {
    "ITC": "FMCG", "INFY": "IT", "HDFCBANK": "Banking",
    "RELIANCE": "Energy", "TCS": "IT", "AAPL": "Technology",
    "MSFT": "Technology", "GOOGL": "Communication Services", "AMZN": "Consumer Discretionary",
    "TSLA": "Automotive", "NVDA": "Semiconductors"
}

def analyze_portfolio(funds):
    if len(funds) < 2:
        return {"error": "At least two funds are required for diversification analysis."}
        
    for fund in funds:
        if not fund.get('sectors'):
            fund['sectors'] = {}
            for ticker, weight in fund.get('holdings', {}).items():
                sector = TICKER_TO_SECTOR.get(ticker.upper(), "Other")
                fund['sectors'][sector] = fund['sectors'].get(sector, 0) + weight

    all_holdings = set(key for fund in funds for key in fund['holdings'].keys())
    pairwise_overlaps = [
        sum(min(f1['holdings'].get(h, 0) * 100, f2['holdings'].get(h, 0) * 100) for h in all_holdings)
        for f1, f2 in combinations(funds, 2)
    ]
    
    average_overlap_percent = sum(pairwise_overlaps) / len(pairwise_overlaps)
    overlap_score = (1 - (average_overlap_percent / 100)) * 100

    total_portfolio_value = sum(f['amount'] for f in funds)
    if not total_portfolio_value:
        return {"error": "The total value of the portfolio cannot be zero."}
    
    all_sectors = set(key for fund in funds for key in fund['sectors'].keys())
    weighted_sector_exposures = {
        sector: sum((fund['amount'] / total_portfolio_value) * fund['sectors'].get(sector, 0) for fund in funds)
        for sector in all_sectors
    }

    hhi = sum(weight**2 for weight in weighted_sector_exposures.values())
    sector_score = (1 - hhi) * 100
    final_score = 0.5 * overlap_score + 0.5 * sector_score

    risk_info = {}
    if final_score >= 75:
        risk_info['level'] = 'Low Risk'
        risk_info['bar_color'] = 'bg-green-500'
        risk_info['badge_color'] = 'bg-green-100 text-green-800'
    elif 50 <= final_score < 75:
        risk_info['level'] = 'Moderate'
        risk_info['bar_color'] = 'bg-amber-500'
        risk_info['badge_color'] = 'bg-amber-100 text-amber-800'
    else:
        risk_info['level'] = 'High Risk'
        risk_info['bar_color'] = 'bg-red-500'
        risk_info['badge_color'] = 'bg-red-100 text-red-800'

    # This is the crucial part: assigning a color to each sector
    colors = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#3b82f6', '#8b5cf6']
    sorted_sectors = sorted(weighted_sector_exposures.items(), key=lambda item: item[1], reverse=True)
    
    sector_data_for_template = [
        {"name": sector, "weight": weight, "color": colors[i % len(colors)]}
        for i, (sector, weight) in enumerate(sorted_sectors)
    ]

    results = {
        "total_value": total_portfolio_value,
        "overlap_score": overlap_score,
        "sector_score": sector_score,
        "final_score": final_score,
        "sector_data": sector_data_for_template,
        "num_funds": len(funds),
        "risk_info": risk_info
    }
    results["total_value_formatted"] = f"{results['total_value']:,.0f}"
    
    return results