import requests

API_KEY = [
    "g8Tpr9cKO6tW4BaojuaYf43VN361o4Yg",
    "ilHjdOqpmiWLok7VIzYotPGmCchltcbX",
    "BwlFRZWXR1URKTlKFDf8vBfBKJPVo5GC",
    "UQrcIZZkkn82UF4gVPFDXUQIm4PkY52Y",
    "tjTckG3gFyzSdzCa2nUkHIhfu70jecxZ",
    "POPj0qes5uDinQEQVUqTtQhmgWsAym4P",
    "rl0zlohwZ0dnngO3u4Xys5nAFuPlTv4K",
    "rzb1ucGorCPGsSvqkhmGGCewrWO6acbZ"
]

def fetch_stock_data(symbol):
    for api_key in API_KEY:
        try:
            url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if data:
                    stock_info = data[0]
                    return {
                        "symbol": stock_info['symbol'],
                        "price": stock_info['price'],
                        "company_name": stock_info['companyName'],
                        "beta": stock_info.get('beta', 'N/A'),
                        "market_cap": stock_info.get('mktCap', 'N/A'),
                        "dividend_yield": stock_info.get('lastDiv', 'N/A'),
                        "range": stock_info.get('range', 'N/A'),
                        "sector": stock_info['sector'],
                        "industry": stock_info['industry'],
                        "website": stock_info['website'],
                        "image": stock_info['image']
                    }
            elif response.status_code == 403:
                print(f"API key {api_key} is invalid")
                continue
            elif response.status_code == 429:
                print(f"Rate limit reached for API key {api_key}")
                continue
            else:
                print(f"Error fetching stock data: {response.status_code}")
        except Exception as e:
            print(f"Exception occurred while fetching stock data: {e}")
    return {"error": "All API keys exhausted or invalid symbol"}
