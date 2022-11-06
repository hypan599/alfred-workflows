import sys

query = sys.argv[1]

import json

def unescape(val):
    print(json.loads(val))

unescape(query)