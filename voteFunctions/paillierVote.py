import requests
import utils
import json
import os
import sys
from collections import Counter
import base64
import traceback
import paillierKeyGen as keyGen
from phe import paillier

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
import TimeRecorder

def encode_for_json(data):
    """Encode bytes data to string using base64 for JSON serialization."""
    if isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')
    return data

def str_to_int(data_str):
    """Convert a string to an integer based on UTF-8 encoding."""
    return int.from_bytes(data_str.encode('utf-8'), 'big')

def int_to_str(data_int):
    """Convert an integer back to a string assuming UTF-8 encoding."""
    return data_int.to_bytes((data_int.bit_length() + 7) // 8, 'big').decode('utf-8')


def post_vote(vote_key, author, votes, fingerprint):
    try:
        public_key, private_key = keyGen.load_keys(vote_key)
        if public_key is None or private_key is None:
            return json.dumps({"error": "Key loading failed, keys may not exist or there was an error."})
        
        serialized_votes = paillierEncrypt(public_key, votes)

        data = {
            'author': utils.encode_base64(author),
            'votes': serialized_votes,
            'fingerprint': utils.encode_base64(fingerprint)
        }
        print("Data prepared for submission:", data)
        return json.dumps(data)  # Return data as JSON string
        
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()
        return json.dumps({"error": str(e)})


@TimeRecorder.track_time('paillier_vote.txt')
def paillierEncrypt(public_key, votes):
    encrypted_votes = [public_key.encrypt(str_to_int(vote)) for vote in votes]
    serialized_votes = [{'ciphertext': str(vote.ciphertext()), 'exponent': vote.exponent} for vote in encrypted_votes]
    return serialized_votes

def save_votes_to_file(poll_id, data, filename="votesPailler.json"):
    """Save serialized votes data under a specific poll ID."""
    try:
        full_data = {'votes': [{'ciphertext': vote['ciphertext'], 'exponent': vote['exponent']} for vote in data['votes']]}
        
        if os.path.exists(filename) and os.path.getsize(filename) > 0:  # Check if file is not empty
            with open(filename, 'r+') as file:
                existing_data = json.load(file)
                if poll_id in existing_data:
                    existing_data[poll_id]['votes'].extend(full_data['votes'])
                else:
                    existing_data[poll_id] = full_data
                file.seek(0)
                file.truncate()  # Clear the file before writing
                json.dump(existing_data, file, indent=4)
        else:
            with open(filename, 'w') as file:
                json.dump({poll_id: full_data}, file, indent=4)
    except Exception as e:
        print(f"Failed to save votes: {e}")
        traceback.print_exc()

def retrieve_votes_from_file(poll_id, filename="votesPailler.json"):
    """Retrieve votes for a specific poll from a JSON file."""
    with open(filename, 'r') as file:
        all_data = json.load(file)
        poll_data = all_data.get(poll_id, {})
    return poll_data

def decrypt_votes(data, private_key, public_key):
    """Decrypt votes from serialized data for a specific poll."""
    print("Data being decrypted:", data)  # Debugging line
    decrypted_votes = []
    for vote_data in data.get('votes', []):
        try:
            encrypted_number = paillier.EncryptedNumber(
                public_key,
                int(vote_data['ciphertext']),
                vote_data['exponent']
            )
            decrypted_vote = private_key.decrypt(encrypted_number)
            decrypted_votes.append(decrypted_vote)
        except KeyError as e:
            print(f"Key error in vote_data: {vote_data} with error {e}")
    return decrypted_votes


def count_votes(votes):
    """Count the occurrences of each vote in a list."""
    vote_count = Counter(votes)
    return vote_count

def homomorphic_sum(encrypted_votes, public_key):
    """Sum encrypted votes using Paillier's additive homomorphism."""
    sum_encrypted = encrypted_votes[0]  # Start with the first encrypted vote
    for enc_vote in encrypted_votes[1:]:
        sum_encrypted = sum_encrypted + enc_vote  # Utilize Paillier's additive property
    return sum_encrypted


def testingMain():
    vote_key = "KTFZsQHF"
    author = "John Doe"
    votes = ["Yes", "No"]
    fingerprint = "sample_fingerprint"

    result_json = post_vote(vote_key, author, votes, fingerprint)
    result = json.loads(result_json)  # Parse the JSON once

    if 'error' not in result:
        save_votes_to_file(vote_key, result, "votesPailler.json")
        saved_data = retrieve_votes_from_file(vote_key, "votesPailler.json")
        public_key, private_key = keyGen.load_keys(vote_key)
        decrypted_results = decrypt_votes(saved_data, private_key, public_key)
        readable_results = [int_to_str(vote) for vote in decrypted_results]
        print("Decrypted Results:", readable_results)
        vote_tally = count_votes(readable_results)
        print("Vote Tally:", vote_tally)
    else:
        print("Error:", result['error'])

def voteSave(vote_key, author, votes, fingerprint):
    # vote_key = "KTFZsQHF"
    # author = "John Doe"
    # votes = ["Yes", "No"]  # Encoding "Yes" as 1 and "No" as 0
    # fingerprint = "sample_fingerprint"

    # Post vote and handle the result
    result_json = post_vote(vote_key, author, votes, fingerprint)
    result = json.loads(result_json)
    save_votes_to_file(vote_key, result, "votesPailler.json")

def voteLoad(vote_key):
    # vote_key = "KTFZsQHF"
    
    # Retrieve the saved votes
    saved_data = retrieve_votes_from_file(vote_key, "votesPailler.json")
    public_key, private_key = keyGen.load_keys(vote_key)

    # Homomorphically sum the encrypted votes
    encrypted_votes = [paillier.EncryptedNumber(public_key, int(vote['ciphertext']), int(vote['exponent']))
                        for vote in saved_data['votes']]
    total_encrypted_votes = sum(encrypted_votes, start=paillier.EncryptedNumber(public_key, 0))  # Sum encrypted votes

    # Decrypt the total to find the number of "Yes" votes
    total_yes_votes = private_key.decrypt(total_encrypted_votes)
    # print(f"Total 'Yes' votes: {total_yes_votes}")

    # Optionally, decrypt individual votes to verify (not required for tally)
    decrypted_results = [private_key.decrypt(vote) for vote in encrypted_votes]
    readable_results = [int_to_str(vote) for vote in decrypted_results]
    print("Decrypted individual votes:", readable_results)

    vote_tally = count_votes(readable_results)
    print("Detailed Vote Tally:", vote_tally)
    return vote_tally

if __name__ == '__main__':
    voteLoad("KTFZsQHF")