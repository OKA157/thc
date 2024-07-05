import json
import os
import traceback
from phe import paillier

def save_keys(key_dict, filename="all_keys.json"):
    with open(filename, "w") as file:
        json.dump(key_dict, file, ensure_ascii=False)

def load_keys_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
    else:
        print(f"File not found: {filename}")
    return {}

def generate_or_load_key(vote_key, filename="all_keys.json"):
    keys = load_keys_from_file(filename)
    if vote_key in keys:
        try:
            public_key_data = keys[vote_key]["public"]
            public_key = paillier.PaillierPublicKey(n=int(public_key_data['n']))
            private_key_data = keys[vote_key]["private"]
            private_key = paillier.PaillierPrivateKey(public_key, p=int(private_key_data['p']), q=int(private_key_data['q']))
            print("Keys loaded successfully.")
            return public_key, private_key
        except Exception as e:
            print(f"Error processing existing keys: {e}")
    else:
        print("No keys found, generating new ones.")
    
    return regenerate_keys(vote_key, keys, filename)

def load_keys(vote_key, filename="all_keys.json"):
    try:
        # print("VOTE_KEY: ", vote_key)
        keys = load_keys_from_file(filename)
        # print("Keys loaded from file:", keys)  # Debug output
        if vote_key in keys:
            public_key_data = keys[vote_key]["public"]
            private_key_data = keys[vote_key]["private"]
            public_key = paillier.PaillierPublicKey(n=int(public_key_data['n']))
            private_key = paillier.PaillierPrivateKey(public_key, p=int(private_key_data['p']), q=int(private_key_data['q']))
            return public_key, private_key
        else:
            print("Vote key not found in keys file.")  # Debug output
            return None, None
    except Exception as e:
        print(f"Failed to load keys: {e}")
        traceback.print_exc()
        return None, None


def regenerate_keys(vote_key, keys, filename):
    print("Generating new keys due to error or missing key.")
    public_key, private_key = paillier.generate_paillier_keypair()
    keys[vote_key] = {
        "public": {"n": str(public_key.n)},
        "private": {"p": str(private_key.p), "q": str(private_key.q)}
    }
    try:
        save_keys(keys, filename)
        print("Keys saved successfully.")
    except Exception as e:
        print(f"Failed to save keys: {e}")
    return public_key, private_key

if __name__ == '__main__':
    vote_key = "KTFZsQHF"
    public_key, private_key = generate_or_load_key(vote_key)
