# backend/stock_analyzer.py
import os
import json
import requests

# The old evaluate_stock_metrics function is now replaced by this one.
def evaluate_stock_metrics(stock):
    """
    Analyzes a stock's financial parameters by sending the data to an LLM
    via the OpenRouter API and asking for a structured JSON response.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    stock_parameters = stock.get('parameters', {})

    # We create a detailed prompt that tells the AI exactly what to do.
    # This acts as our "knowledge base".
    prompt = f"""
    You are an expert financial analyst AI. Your task is to analyze the provided stock data and generate a detailed feedback report.

    Here are the analysis guidelines:
    - P/E Ratio: A low P/E (< 15) is cheap; a high P/E (> 30) is expensive.
    - EPS: Higher EPS is better. Below 1 is low.
    - Dividend Yield: Above 3% is attractive for income. 0% means no dividend.
    - Market Cap: Use terms like "sizable player", "large, stable company", or "one of the world's giants".
    - Debt-to-Equity: Below 0.5 is low leverage. Above 1.5 is high leverage.
    - ROE: Above 15% is very strong. Below 8% is below average.
    - Current Ratio: Above 1 suggests good short-term liquidity. Below 1 signals potential issues.

    Stock Data:
    {json.dumps(stock_parameters, indent=2)}

    Based on the data and guidelines, generate a JSON object with two keys: "feedback" and "summary".
    - The "feedback" object should contain a one-sentence analysis for each of the 10 financial metrics.
    - The "summary" should be a 2-3 sentence paragraph synthesizing the most important points.

    Return ONLY the raw JSON object, with no other text or explanations.
    """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}"
            },
            data=json.dumps({
                "model": "mistralai/mistral-7b-instruct", # A fast and capable model
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"} # Enforce JSON output
            })
        )

        response.raise_for_status() # This will raise an error for bad responses (4xx or 5xx)

        # The AI's response is a JSON string, which we need to parse into a Python dict
        ai_response_content = response.json()['choices'][0]['message']['content']
        analysis_data = json.loads(ai_response_content)

        # We construct the final dictionary to match the template's expectations
        final_result = {
            "stockSymbol": stock.get('stockSymbol'),
            "parameters": stock_parameters,
            "feedback": analysis_data.get('feedback', {}),
            "summary": analysis_data.get('summary', "AI analysis could not be generated.")
        }
        return final_result

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"error": "Failed to connect to the analysis service."}
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Failed to parse AI response: {e}")
        return {"error": "Received an invalid response from the analysis service."}