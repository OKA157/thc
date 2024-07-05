# import requests
# import base64
# import json
# import os
# from datetime import datetime

# def getVote(url,voteKey):
#     full_url = f"{url}/{voteKey}"
    
#     headers = {
#         'Accept': 'application/json'
#     }
    
#     try:
#         response = requests.get(full_url, headers=headers)
        
#         if response.status_code == 200:
#             try:
#                 vote_info = response.json()
#                 return vote_info
#             except ValueError:
#                 print("Response is not in JSON format")
#                 return 'error'
#         elif response.status_code == 404:
#             print(f"404 Not Found: {response.text}")
#             return 'error'
#         else:
#             print(f"Unexpected status code {response.status_code}: {response.text}")
#             return 'error'
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return 'error'

# def decode_propositions(propositions):
#     decoded_props = []
#     for prop in propositions:
#         decoded_prop = base64.urlsafe_b64decode(prop).decode('utf-8')
#         decoded_props.append(decoded_prop)
#     return decoded_props

# def convert_timestamp(timestamp):
#     return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# def getAllVotingsIDs(file_path):
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as file:
#             try:
#                 data = json.load(file)
#                 return data
#             except json.JSONDecodeError:
#                 return []
#     else:
#         return []

# def getAllVotings(file_path, url):
#     voteJsons = getAllVotingsIDs(file_path)
#     votings = []
#     for vote in voteJsons:
#         votings.append(getVote(url, vote['key']))
#     return votings

# def readVoteInfo(votings):
#     for voting in votings:
#         if voting != 'error':
#             encoded_propositions = json.loads(voting['propositions'][0])
#             decoded_propositions = decode_propositions(encoded_propositions)
#             voting['propositions'] = decoded_propositions
#             voting['closing'] = convert_timestamp(voting['closing'])
#             voting['expiry'] = convert_timestamp(voting['expiry'])
#         print("Vote Information:", voting)

# if __name__ == '__main__':
#     url = "http://127.0.0.1:9380"
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     jsonFile = current_dir+"\\voting.json"
#     votings = getAllVotings(jsonFile, url)
#     readVoteInfo(votings)
