import requests
import base64
import json
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
import TimeRecorder
import paillierVote as paillier
import utils

URL = "http://127.0.0.1:9380"  # Replace with your actual URL

@TimeRecorder.track_time('thc_vote.txt')
def postVote(url, vote_key, author, votes, fingerprint):
    # Construct the full URL
    full_url = f"{url}/{vote_key}"
    
    # Prepare the POST data
    data = {
        'author': utils.encode_base64(author),
        'votes': json.dumps([utils.encode_base64(vote) for vote in votes]),
        'fingerprint': utils.encode_base64(fingerprint)
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        response = requests.post(full_url, data=data, headers=headers)
        
        if response.status_code == 200:
            print(f"Vote Sumbitted Successfully (code {response.status_code})!: {response.text}")
            return "Vote Sumbitted Successfully!"
        elif response.status_code == 303:
            print(f"303 See Other: {response.headers['Location']}")
            return "Vote  failed. Try again later."
        elif response.status_code == 400:
            print(f"400 Bad Request: {response.text}")
            return "Vote  failed. Try again later."
        elif response.status_code == 403:
            print(f"403 Forbidden: {response.text}")
            return "Vote  failed. Try again later."
        elif response.status_code == 404:
            print(f"404 Not Found: {response.text}")
            return "Vote  failed. Try again later."
        elif response.status_code == 411:
            print(f"411 Length Required: {response.text}")
            return "Vote  failed. Try again later."
        elif response.status_code == 500:
            print(f"500 Internal Server Error: {response.text}")
            return "Vote  failed. Try again later."
        else:
            print(f"Unexpected status code {response.status_code}: {response.text}")
            return "Vote  failed. Try again later."
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return "Vote  failed. Try again later."
    
@TimeRecorder.track_time('thc_vote.txt')
def setVote(vote_key, option):
    author = "author_name"
    vote = [option]
    fingerprint= json.dumps([utils.generate_random_string()])
    result = postVote(URL, vote_key, author, vote, fingerprint)
    paillier.voteSave(vote_key, author, [option], fingerprint)
    return result

if __name__ == '__main__':
    url = "http://127.0.0.1:9380"
    vote_key = "Qv_BFF3F" 
    
    author = "author_name" 
    votes = [utils.encode_base64("Yes")] 
    fingerprint = json.dumps(["fingerprint1"])
    postVote(url, vote_key, author, votes, fingerprint)
