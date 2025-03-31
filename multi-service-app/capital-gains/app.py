import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Get service URL from environment variable - updated default URL
STOCKS_URL = os.getenv('STOCKS_URL', 'http://stocks-service:5001')

def get_stock_data(service_url):
    """Fetch all stocks from a specific service"""
    try:
        response = requests.get(f"{service_url}/stocks")
        if response.status_code == 200:
            return response.json()
        print(f"Failed to fetch stocks. Status code: {response.status_code}")  # Added debugging
        return []
    except Exception as e:
        print(f"Error fetching stocks from {service_url}: {str(e)}")
        return []

def get_current_stock_value(service_url, stock_id):
    """Get current value of a specific stock"""
    try:
        response = requests.get(f"{service_url}/stock-value/{stock_id}")
        if response.status_code == 200:
            return response.json().get('stock value', 0)
        print(f"Failed to fetch stock value. Status code: {response.status_code}")  # Added debugging
        return 0
    except Exception as e:
        print(f"Error fetching stock value from {service_url}: {str(e)}")
        return 0

def calculate_stock_gain(service_url, stock):
    """Calculate capital gain for a single stock"""
    current_value = get_current_stock_value(service_url, stock['id'])
    purchase_value = float(stock['purchase price']) * stock['shares']
    gain = current_value - purchase_value
    print(f"Stock {stock['id']}: Current Value = {current_value}, Purchase Value = {purchase_value}, Gain = {gain}")  # Added debugging
    return gain

def filter_stocks(stocks, num_shares_gt=None, num_shares_lt=None):
    """Filter stocks based on number of shares criteria"""
    filtered_stocks = stocks.copy()
    
    if num_shares_gt is not None:
        filtered_stocks = [s for s in filtered_stocks if s['shares'] > num_shares_gt]
    
    if num_shares_lt is not None:
        filtered_stocks = [s for s in filtered_stocks if s['shares'] < num_shares_lt]
    
    return filtered_stocks

@app.route('/capital-gains', methods=['GET'])
def get_capital_gains():
    try:
        # Get query parameters
        num_shares_gt = request.args.get('numsharesgt')
        num_shares_lt = request.args.get('numshareslt')

        # Validate num_shares_gt
        if num_shares_gt is not None:
            try:
                num_shares_gt = int(num_shares_gt)
                if num_shares_gt < 0:
                    return {"error": "numsharesgt must be non-negative"}, 400
            except ValueError:
                return {"error": "numsharesgt must be a valid integer"}, 400

        # Validate num_shares_lt
        if num_shares_lt is not None:
            try:
                num_shares_lt = int(num_shares_lt)
                if num_shares_lt < 0:
                    return {"error": "numshareslt must be non-negative"}, 400
            except ValueError:
                return {"error": "numshareslt must be a valid integer"}, 400

        # Convert share number filters to integers if provided
        if num_shares_gt is not None:
            num_shares_gt = int(num_shares_gt)
        if num_shares_lt is not None:
            num_shares_lt = int(num_shares_lt)

        print(f"Using STOCKS_URL: {STOCKS_URL}")  # Debug URL being used
        
        # Get and process stocks
        stocks = get_stock_data(STOCKS_URL)
        print(f"Retrieved stocks: {stocks}")  # Debug retrieved stocks
        
        filtered_stocks = filter_stocks(stocks, num_shares_gt, num_shares_lt)
        print(f"Filtered stocks: {filtered_stocks}")  # Debug filtered stocks
        
        total_gain = 0
        for stock in filtered_stocks:
            gain = calculate_stock_gain(STOCKS_URL, stock)
            total_gain += gain
            print(f"Stock {stock['id']}: Gain = {gain}, Running total = {total_gain}")  # Added debugging
        
        # Round to 2 decimal places
        total_gain = round(total_gain, 2)
        print(f"Final total gain: {total_gain}")  # Debug final result
        
        return jsonify(total_gain)
    
    except ValueError as ve:
        return {"error": "Invalid parameter values"}, 400
    except Exception as e:
        print(f"Error in get_capital_gains: {str(e)}")  # Added error debugging
        return {"error": f"Server error: {str(e)}"}, 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)