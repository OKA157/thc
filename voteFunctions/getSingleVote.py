import requests
import base64
import json
import time
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
import TimeRecorder
import utils

def getVote(url, vote_key):
    # Construct the full URL
    full_url = f"{url}/{vote_key}/ballots"
    
    headers = {
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(full_url, headers=headers)
        
        if response.status_code == 200:
            try:
                ballots = response.json()
                print("Ballots:")
                for ballot in ballots:
                    decoded_ballot = {k: utils.decode_base64(v) if isinstance(v, str) else v for k, v in ballot.items()}
                    print(json.dumps(decoded_ballot, indent=4))
            except ValueError as e:
                print("Response is not in JSON format or could not be parsed:", e)
        else:
            print(f"Unexpected status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == '__main__':
    url = "http://127.0.0.1:9380"  # Replace with your actual URL
    vote_key = "Qv_BFF3F"  # Replace with the actual vote key
    getVote(url, vote_key)
