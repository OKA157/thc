import requests
import json
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
import paillierVote as paillier
import TimeRecorder
import utils

def get_results_final(vote_key):
    res = paillier.voteLoad(vote_key)
    print(res)
    return res

def get_specific_result(vote_key, vote_option):
    # Assuming get_results_final returns a Counter object
    results = get_results_final(vote_key)
    # Access the count for the specified vote_option, defaulting to 0 if not found
    result_count = results.get(vote_option, 0)
    return result_count

def get_results(url, vote_key):
    # Construct the full URL
    full_url = f"{url}/{vote_key}/results"
    
    headers = {
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(full_url, headers=headers)
        
        if response.status_code == 200:
            try:
                # Print raw response for debugging
                print("Raw Response Text:", response.text)
                
                results = response.json()
                print("Parsed Results:", results)
                
                for result in results:
                    # Decode the proposition list
                    encoded_propositions = json.loads(result['proposition'])
                    decoded_propositions = [utils.decode_base64(prop) for prop in encoded_propositions]
                    
                    # Decode the score
                    decoded_score = utils.decode_base64(result['score'])
                    
                    print(f"Propositions: {decoded_propositions}, Score: {decoded_score}")

                    print(paillier.voteLoad(vote_key))
            except ValueError as e:
                print("Response is not in JSON format or could not be parsed:", e)
        elif response.status_code == 403:
            print(f"403 Forbidden: {response.text}")
        elif response.status_code == 404:
            print(f"404 Not Found: {response.text}")
        else:
            print(f"Unexpected status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def get_results_old(url, vote_key):
    # Construct the full URL
    full_url = f"{url}/{vote_key}/results"
    
    headers = {
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(full_url, headers=headers)
        
        if response.status_code == 200:
            try:
                results = response.json()
                print("Results:",results)
                # for result in results:
                #     props = []
                #     # for prop in result['proposition']:
                #     #     props.append(utils.decode_base64(prop))
                #     # decoded_propositions = [utils.decode_base64(prop) for prop in result['proposition']]
                    
                #     print(f"Proposition: {utils.decode_base64(result['proposition'])}, Score: {result['score']}")
            except ValueError as e:
                print("Response is not in JSON format or could not be parsed:", e)
        elif response.status_code == 403:
            print(f"403 Forbidden: {response.text}")
        elif response.status_code == 404:
            print(f"404 Not Found: {response.text}")
        else:
            print(f"Unexpected status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == '__main__':
    url = "http://127.0.0.1:9380"  # Replace with your actual URL
    vote_key = "KTFZsQHF"  # Replace with the actual vote key
    
    get_results_final(vote_key)
