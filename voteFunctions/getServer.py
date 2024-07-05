import requests

def make_post_request(url):
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            json_response = response.json()
            print("Response JSON:", json_response)
        except ValueError:
            print("Response is not in JSON format")
    else:
        print(f"Request failed with status code {response.status_code}")

if __name__ == '__main__':
    url = "http://127.0.0.1:9380"  # Replace with your actual URL
    data = {
        'key1': 'value1',
        'key2': 'value2'
    }
    make_post_request(url)