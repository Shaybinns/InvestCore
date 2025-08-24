import requests
import json

def test_api():
    symbol = "NVDA"
    url = "https://yahoo-finance166.p.rapidapi.com/api/market/get-quote-v2"
    querystring = {"symbols": symbol, "fields": "quoteSummary"}
    
    headers = {
        "x-rapidapi-key": "5440e1fc4cmshf3f532851e0252cp1e9e06jsnebae0559f24b",
        "x-rapidapi-host": "yahoo-finance166.p.rapidapi.com"
    }
    
    print(f"Making API call to {url}")
    print(f"Headers: {headers}")
    print(f"Params: {querystring}")
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            if 'quoteSummary' in data:
                print("Found quoteSummary!")
                quote_summary = data['quoteSummary']
                print(f"quoteSummary keys: {list(quote_summary.keys())}")
                
                if 'result' in quote_summary and len(quote_summary['result']) > 0:
                    result = quote_summary['result'][0]
                    print(f"Result keys: {list(result.keys())}")
                    print(f"Sample data: {json.dumps(result, indent=2)[:500]}...")
                else:
                    print("No result found in quoteSummary")
            else:
                print("No quoteSummary found in response")
                print(f"Full response: {json.dumps(data, indent=2)[:1000]}...")
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    test_api()
