import hashlib
import json

def hash_data(data):
    """
    Given `data` (bytes), returns a hexadecimal hash of the data.
    """

    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()

def hash_list(data):
    """
    Hashes a list of strings.
    """

    return hash_data("\n".join(data).encode("utf-8"))

def dump(d):
    """
    Dumps a dictionary to a JSON string.
    """

    print(json.dumps(d, indent=2))
