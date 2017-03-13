import os
import sys
import json

try:
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.request import Request, urlopen


CONFIGSTR_TOKEN = os.getenv('CONFIGSTR_TOKEN')
CONFIGSTR_URL = os.getenv('CONFIGSTR_URL')


if CONFIGSTR_TOKEN and CONFIGSTR_URL:
    request = Request(CONFIGSTR_URL, headers={
        'Authorization': 'Bearer {}'.format(CONFIGSTR_TOKEN)
    })
else:
    print(
        'Not properly configured - please set CONFIGSTR_TOKEN and '
        'CONFIGSTR_URL in the environment'
    )
    sys.exit(1)


remote_config = json.loads(
    urlopen(request).read().decode('utf-8')
).get('data', {})

WHERE = os.getenv('WHERE', remote_config.get('where'))
