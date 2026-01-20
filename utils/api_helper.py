import requests


class APIHelper:

    
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.session = requests.Session()
        # Set default headers
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        })
    
    def get(self, endpoint, params=None, headers=None, **kwargs):

        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint
        response = self.session.get(url, params=params, headers=headers, **kwargs)
        print(f"GET {url} -> Status: {response.status_code}")
        return response .json()
    
    def post(self, endpoint, data=None, json=None, headers=None, **kwargs):
       
        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint
        response = self.session.post(url, data=data, json=json, headers=headers, **kwargs)
        print(f"POST {url} -> Status: {response.status_code}")
        return response .json()
    
    def close(self):
        """Close the session"""
        self.session.close()
