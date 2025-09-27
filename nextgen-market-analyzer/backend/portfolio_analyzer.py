# backend/portfolio_analyzer.py
from itertools import combinations

# To automatically map stock tickers to sectors, we'll create a simple dictionary.
# In a real-world app, this would come from a database or a financial data API.
# This map is created from the sample data you provided.
TICKER_TO_SECTOR = {
    "ITC": "FMCG", "INFY": "IT", "HDFCBANK": "Banking",
    "RELIANCE": "Energy", "TCS": "IT", "AAPL": "Technology",
    "MSFT": "Technology", "GOOGL": "Communication Services", "AMZN": "Consumer Discretionary",
    "TSLA": "Automotive", "NVDA": "Semiconductors"
    # Add more mappings as needed
}

def analyze_portfolio(funds):
    """
    Performs a full portfolio analysis based on the provided fund data.
    Calculates fund overlap, sector diversification, and a final combined score.
    """
    if len(funds) < 2:
        # Cannot calculate overlap with less than 2 funds
        # You can decide how to handle this case, here we provide default scores
        return {
            "error": "At least two funds are required to calculate diversification scores."
        }
        
    # --- Auto-calculate sector weights if not provided ---
    for fund in funds:
        if not fund.get('sectors'):
            fund['sectors'] = {}
            for ticker, weight in fund.get('holdings', {}).items():
                sector = TICKER_TO_SECTOR.get(ticker.upper(), "Other")
                fund['sectors'][sector] = fund['sectors'].get(sector, 0) + weight

    # --- Step 1: Fund Overlap Score ---
    all_holdings = set()
    for fund in funds:
        all_holdings.update(fund['holdings'].keys())

    pairwise_overlaps = []
    for f1, f2 in combinations(funds, 2):
        overlap_sum = 0
        for holding in all_holdings:
            w1 = f1['holdings'].get(holding, 0) * 100
            w2 = f2['holdings'].get(holding, 0) * 100
            overlap_sum += min(w1, w2)
        pairwise_overlaps.append(overlap_sum)
    
    average_overlap_percent = sum(pairwise_overlaps) / len(pairwise_overlaps)
    overlap_score = (1 - (average_overlap_percent / 100)) * 100

    # --- Step 2: Sector Diversification Score ---
    total_portfolio_value = sum(f['amount'] for f in funds)
    all_sectors = set()
    for fund in funds:
        all_sectors.update(fund['sectors'].keys())

    weighted_sector_exposures = {}
    for sector in all_sectors:
        total_sector_weight = 0
        for fund in funds:
            fund_share = fund['amount'] / total_portfolio_value
            sector_weight_in_fund = fund['sectors'].get(sector, 0)
            total_sector_weight += fund_share * sector_weight_in_fund
        weighted_sector_exposures[sector] = total_sector_weight

    # Herfindahl-Hirschman Index (HHI) for sector concentration
    hhi = sum(weight**2 for weight in weighted_sector_exposures.values())
    sector_score = (1 - hhi) * 100

    # --- Step 3: Final Diversification Score ---
    final_score = 0.5 * overlap_score + 0.5 * sector_score

    return {
        "total_value": total_portfolio_value,
        "overlap_score": overlap_score,
        "sector_score": sector_score,
        "final_score": final_score,
        "weighted_sectors": weighted_sector_exposures,
        "num_funds": len(funds)
    }