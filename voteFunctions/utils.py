from datetime import datetime, timedelta
import random
import string
import base64
import calendar

# Convert Timestap to Readable Time-Date
def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# gives timestamp with +1h
def getTimestamp(myDate, extraHour):
        one_hour_from_now = datetime.now() + timedelta(hours=extraHour-2)

        # Extract the time component
        time_component = one_hour_from_now.time()

        # Merge the time component with the date string to form a new datetime object
        merged_datetime_str = f"{myDate} {time_component}"
        merged_datetime_obj = datetime.strptime(merged_datetime_str, '%Y-%m-%d %H:%M:%S.%f')

        # Convert the merged datetime object to a Unix timestamp in UTC
        timestamp = int(calendar.timegm(merged_datetime_obj.timetuple()))
        return timestamp

#doesn't work
def getTimestampTest(myDate, extraMinutes):
    one_hour_from_now = datetime.now() + timedelta(minutes=extraMinutes)
    time_component = one_hour_from_now.time()
    merged_datetime_str = f"{myDate} {time_component:%H:%M:%S}"
    try:
        merged_datetime_obj = datetime.strptime(merged_datetime_str, '%Y-%m-%d %H:%M:%S')
        timestamp = int(calendar.timegm(merged_datetime_obj.timetuple()))
        return timestamp
    except Exception as e:
        print(f"Error in getTimestamp with {merged_datetime_str}: {e}")
        return None

# For base64 Encoding in requests
def encode_base64(data):
    return base64.urlsafe_b64encode(data.encode()).decode()

# For base64 Decoding in requests
def decode_base64(data):
    return base64.urlsafe_b64decode(data).decode('utf-8')

# For base64 ENCODING in requests
def urlsafe_base64_encode(data):
    """Encode data using URL-safe base64."""
    return base64.urlsafe_b64encode(data.encode('utf-8')).decode('utf-8')

def urlsafe_base64_decode(data):
    """Decode data using URL-safe base64."""
    return base64.urlsafe_b64decode(data.encode('utf-8')).decode('utf-8')

def decode_base64_results(data):
    """Decode data using URL-safe base64."""
    try:
        # Adjust padding if necessary
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        
        # Decode the base64 data
        return base64.urlsafe_b64decode(data).decode('utf-8')
    except Exception as e:
        print(f"Error decoding base64 data: {e}")
        return None

def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# For base64 DECODING in requests
def results_base64_decode(data):
    try:
        # Adjust padding
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return base64.urlsafe_b64decode(data).decode('utf-8')
    except Exception as e:
        print(f"Error decoding base64 data: {e}")
        return None

def decode_propositions(propositions):
    decoded_props = []
    for prop in propositions:
        decoded_prop = base64.urlsafe_b64decode(prop).decode('utf-8')
        decoded_props.append(decoded_prop)
    return decoded_props

# generate key for SET VOTE
def generate_key(length=8):
    """Generate a URL-safe base64 encoded string."""
    key = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=length))
    return key
