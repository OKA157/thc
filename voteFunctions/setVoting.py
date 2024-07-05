import requests
import base64
import json
import time
import os
import sys
import traceback
from phe import paillier
from datetime import datetime, timedelta

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
import utils

test = False
current_dir = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = current_dir+"\\voting.json"
JSON_FILE_PAILLIER = current_dir+"\\votingPaillier.json"
PAILLIER_PUBLIC = current_dir+"\\paillierPublic.json"
PAILLIER_PRIVATE = current_dir+"\\paillierPrivate.json"
URL = "http://127.0.0.1:9380"  # Replace with your actual URL

########## SET VOTES FUNCTIONS ##########

# Creates a vote FHE using the API.
def createVoting(url, data):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return [response.status_code,response.text]
    elif response.status_code == 303:
        return [response.status_code,response.text]
    elif response.status_code == 400:
        return [response.status_code,response.text]
    elif response.status_code == 411:
        return [response.status_code,response.text]
    elif response.status_code == 500:
        return [response.status_code,response.text]
    else:
        return [response.status_code,response.text]

# Store FHE vote in DB.
def saveVoteKey(file_path, key, title, closing, expiry, props):
    # Create the new element as a dictionary
    new_element = {
        'key': key,
        'title': title,
        'closing': closing,
        'expiry': expiry,
        'props': props,
    }

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(new_element)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def makeVote(key, title, closing, expiry, props):
    if test:
        try:
            voteKey = utils.generate_key()
            print(voteKey)
            closing_timestamp = utils.getTimestampTest(closing,3)
            expiry_timestamp = utils.getTimestampTest(expiry,7)
            print(closing_timestamp)
            print(expiry_timestamp)

            data = {
                'key': voteKey,
                'mod': base64.urlsafe_b64encode(b'modulus_for_server').decode('utf-8'),
                'title': utils.urlsafe_base64_encode(title),
                'closing': str(int(closing_timestamp)),  # Example timestamp for vote closing date (3600 = 1 hour from now)
                'expiry': str(int(expiry_timestamp)),   # Example timestamp for vote expiring date (7200 = 2 hours from now)
                'propositions': json.dumps(props)
            }
            result = createVoting(URL, data)
            print(result)
            if result[0] == 200:
                
                print(JSON_FILE)
                saveVoteKey(JSON_FILE, voteKey, title, utils.convert_timestamp(closing_timestamp), utils.convert_timestamp(expiry_timestamp), props)
        except Exception as e:
            print(f"Exception occurred: {e}")
            traceback.print_exc()
    else:
        voteKey = utils.generate_key()
        print(voteKey)
        closing_timestamp = utils.getTimestamp(closing,1)
        expiry_timestamp = utils.getTimestamp(expiry,2)
        data = {
            'key': voteKey,
            'mod': base64.urlsafe_b64encode(b'modulus_for_server').decode('utf-8'),
            'title': utils.urlsafe_base64_encode(title),
            'closing': str(int(closing_timestamp)),  # Example timestamp for vote closing date (3600 = 1 hour from now)
            'expiry': str(int(expiry_timestamp)),   # Example timestamp for vote expiring date (7200 = 2 hours from now)
            'propositions': json.dumps([utils.encode_base64(prop) for prop in props])
        }
        # 'propositions': json.dumps([utils.encode_base64(prop) for prop in props])
        result = createVoting(URL, data)
        print(result)
        if result[0] == 200:
            
            print(JSON_FILE)
            saveVoteKey(JSON_FILE, voteKey, title, utils.convert_timestamp(closing_timestamp), utils.convert_timestamp(expiry_timestamp), props)


def generate_keys(vote_key):
    public_key, private_key = paillier.generate_paillier_keypair()
    key_dir = f"keys/{vote_key}"
    os.makedirs(key_dir, exist_ok=True)
    
    with open(f"{key_dir}/public_key.json", "w") as pub_file:
        json.dump({'n': public_key.n}, pub_file)
        
    with open(f"{key_dir}/private_key.json", "w") as priv_file:
        json.dump({'p': private_key.p, 'q': private_key.q}, priv_file)
    
    return public_key, private_key

def load_keys(vote_key):
    key_dir = f"keys/{vote_key}"
    
    with open(f"{key_dir}/public_key.json", "r") as pub_file:
        pub_data = json.load(pub_file)
        public_key = paillier.PaillierPublicKey(n=pub_data['n'])
        
    with open(f"{key_dir}/private_key.json", "r") as priv_file:
        priv_data = json.load(priv_file)
        private_key = paillier.PaillierPrivateKey(
            public_key, p=priv_data['p'], q=priv_data['q']
        )
        
    return public_key, private_key

########## GET VOTES FUNCTIONS ##########

# Get SINGLE FHE vote using the API by key.
def getVote(url,voteKey):
    full_url = f"{url}/{voteKey}"
    
    headers = {
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(full_url, headers=headers)
        
        if response.status_code == 200:
            try:
                vote_info = response.json()
                return vote_info
            except ValueError:
                print("Response is not in JSON format")
                return 'error'
        elif response.status_code == 404:
            print(f"404 Not Found: {response.text}")
            return 'error'
        else:
            print(f"Unexpected status code {response.status_code}: {response.text}")
            return 'error'
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return 'error'

# Get all the FHE vote from the DB.
def getAllVotingsIDs(file_path, filter):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                if filter == "Active":
                    now = datetime.now()
                    filtered_data = [element for element in data if datetime.strptime(element['closing'], '%Y-%m-%d %H:%M:%S') > now]
                    return filtered_data
                elif filter == "Closed":
                    now = datetime.now()
                    filtered_data = [element for element in data 
                                if datetime.strptime(element['closing'], '%Y-%m-%d %H:%M:%S') < now < datetime.strptime(element['expiry'], '%Y-%m-%d %H:%M:%S')]
                    return filtered_data
                else:
                    return data
                
            except json.JSONDecodeError:
                return []
    else:
        return []


# Get ALL FHE vote using the API by key. [JSON -> ids // API -> Info]
def getVotings(url, voteJsons):
    votings = []
    for vote in voteJsons:
        vote_data = getVote(url, vote['key'])
        if vote_data != "error":
            vote_data['key'] = vote['key']
            votings.append(vote_data)
    if test:
        print("VOTINGS: ",votings)
    return votings

# Read FHE Voting INFO.
def readVoteInfo(votings):
    for voting in votings:
        if voting != 'error':
            encoded_propositions = json.loads(voting['propositions'][0])
            decoded_propositions = utils.decode_propositions(encoded_propositions)
            voting['title'] = utils.urlsafe_base64_decode(voting['title'])
            voting['propositions'] = decoded_propositions
            voting['closing'] = utils.convert_timestamp(voting['closing'])
            voting['expiry'] = utils.convert_timestamp(voting['expiry'])
        print("Vote Information:", voting)

# Format FHE Voting INFO.
def formatVoteInfo(votings):
    for voting in votings:
        if voting != 'error':
            encoded_propositions = json.loads(voting['propositions'][0])
            decoded_propositions = utils.decode_propositions(encoded_propositions)
            # decoded_propositions = encoded_propositions
            voting['title'] = utils.urlsafe_base64_decode(voting['title'])
            voting['propositions'] = decoded_propositions
            voting['closing'] = utils.convert_timestamp(voting['closing'])
            voting['expiry'] = utils.convert_timestamp(voting['expiry'])
    return votings
# Full implementation - FHE Vote Getter.
def getVotingList():
    voteJsons = getAllVotingsIDs(JSON_FILE, "All")
    votings = getVotings(URL, voteJsons)
    # readVoteInfo(votings)
    return votings

# Full implementation - FHE Vote Getter.
def getActiveVotingList():
    voteJsons = getAllVotingsIDs(JSON_FILE, "Active")
    votings = getVotings(URL, voteJsons)
    result = formatVoteInfo(votings)
    return votings

def getClosedVotingList():
    try:
        voteJsons = getAllVotingsIDs(JSON_FILE, "Closed")
        print("*1*")
        votings = getVotings(URL, voteJsons)
        print("*2*")
        result = formatVoteInfo(votings)
        return result
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()


if __name__ == '__main__':
    active = getAllVotingsIDs(JSON_FILE, "Closed")
    # getVote(URL,"WX-x8dq6")
    # for element in active:
    #     closing = element['closing']
    #     print(f'Closing: {closing}.\n')
    # makeVote("key", "title", "closing", "expiry", "props")