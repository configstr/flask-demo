
# Configstr Flask Demo

This demo seeks to provide an example of a simple integration of Configstr
into a Python project, specifically one using Flask.  The concepts demonstrated
should be simple enough to use in any Python project.

The most up-to-date version of this guide can always be found at our
[GitHub repo](https://github.com/configstr/flask-demo).  Each section below
corresponds to a commit to our repo, allowing you to diff between steps
to easily get a sense of what is required.

This demo has been designed to work on Python 2.7 or
Python 3.6.

## Initial Setup ([`5c2500c`](https://github.com/configstr/flask-demo/commit/5c2500cb5c62866b6ad0bc6e22eae2ee092492ab))

The initial setup step provides a basic flask application
for you to work with.  Install flask in your environment, and
add the following simple Flask "Hello World" application and save it as `src/hello_config.py`:

```Python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'
```

Next create an empty `src/__init__.py` file.  Finally we'll
create a simple manage command to handle running our service:

```Python
import optparse
from src.hello_config import app

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--host', dest='host', default='127.0.0.1')
    parser.add_option('--port', dest='port', default=9999)
    parser.add_option('--debug', action='store_true', default=False)

    (options, args) = parser.parse_args()

    app.run(options.host, options.port, debug=options.debug)
```

With this in place, you should be able to start your service, listening locally on port `9999` like so:

```Bash
$ python manage.py --debug
```

This will start Flask, and ensure any changes you make
reload Flask and are reflected immediately.  Visit your
new Flask site in the browser at
 [http://127.0.0.1:9999/](http://127.0.0.1:9999/).

If all went well, you should see `Hello World!` in the
browser.

## Creating a Centralized Config ([4523ec4](https://github.com/configstr/flask-demo/commit/4523ec433c0049d498063f495c314857682733fa))

Next we'll allow to what we say hello to be dynamically
configurable at runtime.  To accomplish this we'll employ
a fairly common pattern, the configuration module.  This is
a single location which can handle making configuration
available to an application.  Often this means reading it
in from a file or environment variables.  We'll go the
environment variable route.  First, create a file called
`src/config.py`:

```Python
import os

WHERE = os.getenv('WHERE', 'Nowhere')
```

With this, you can import `config` elsewhere in your project
and access `config.WHERE`.  If it's unconfigured, you will
simply get `Nowhere`.  Now edit your `src/hello_config.py`
to use this to be able to configure who you say hello to:

```Python
from flask import Flask
from . import config

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello {}!'.format(config.WHERE)
```

Specifically, we imported our config, `from . import config`
and used it to say hello dynamically: `'Hello {}!'.format(config.WHERE)`.

Now if you refresh your browser, you should see `Hello Nowhere`.  If you hit `ctrl-c` to stop the Flask server and run `export WHERE=somewhere` and then run the server again, you will now see `Hello somewhere` in your browser if you
refresh.

## Using the Configstr Remote Config Service ([28a0570](https://github.com/configstr/flask-demo/commit/28a0570561ff94b140b826b62e33147444dcfe65))

Finally we will use Configstr to allow us to retrieve our
configuration values remotely on start up.  First, sign up
for an account, and create an application, then an
environment, and within that environment push a
config to the environment.  For example:

```Bash
$ curl -X POST \
-H "Content-Type: application/json" \
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0OTAwOTg5MzUsImp0aSI6IjI3YWI4MmQwLWM0OWEtNDEyNy1iNjZjLTE1NmVmYmM3ZmY4MyIsImlhdCI6MTQ4OTQ5NDEzNSwiaXNzIjoiNThjN2UwNzQ3NTg3ZWMwMDA4MGYzNzRhIiwib3JnYW5pemF0aW9uIjoiNThjN2UwNzY3NTg3ZWMwMDA4MGYzNzRjIiwiZ3JhbnRzIjpbImFwcGxpY2F0aW9uOmdldDoqIiwiYXBwbGljYXRpb246cG9zdDoqIiwiYXBwbGljYXRpb246cGF0Y2g6KiIsImFwcGxpY2F0aW9uOmRlbGV0ZToqIiwiY29uZmlnOmdldDoqIiwiY29uZmlnOnBvc3Q6KiIsImVudmlyb25tZW50OmdldDoqIiwiZW52aXJvbm1lbnQ6cG9zdDoqIiwiZW52aXJvbm1lbnQ6cGF0Y2g6KiIsImVudmlyb25tZW50OmRlbGV0ZToqIiwib3JnYW5pemF0aW9uOmdldDoqIiwib3JnYW5pemF0aW9uOnBvc3Q6KiIsIm9yZ2FuaXphdGlvbjpwYXRjaDoqIiwib3JnYW5pemF0aW9uOmRlbGV0ZToqIiwidG9rZW46Z2V0OioiLCJ0b2tlbjpwb3N0OioiLCJ0b2tlbjpkZWxldGU6KiIsInVzZXI6Z2V0OioiLCJ1c2VyOnBvc3Q6KiIsInVzZXI6cGF0Y2g6KiIsInVzZXI6ZGVsZXRlOioiXX0.KFhLF8e3X8BrpAa6Lgh6xLBZybyXwpcrYNdHqXuUqaw" \
-d \
'{
  "comment": "Setting WHERE for the demo app.",
  "data": {
    "WHERE": "from the internet!"
  }
}' \
https://api.configstr.io/api/v1/environment/58c7e0a17587ec00080f3750/versions
```

This curl command can be found on the page for your
environment, just ensure you modify the `data` attribute to
contain the relevant data, also be aware that the specific
token and environment ids shown above won't work for you -
be sure to get these values from your own Dashboard.

When you have added a configuration, head to the page for
the environment and be sure you click "Make Active" so that
you have an active configuration.  This configuration will
now be the one returned for the environment.

You can now set go to the `Account` pane in the Dashboard
so as to create an API token for external access. Hit the
plus button and a token will be created, then `Show` to
display it, and `Copy` to copy the token.  Now you'll want
to put this token in a .env file or simply export it
in the shell, for example:

```Bash
$ export CONFIGSTR_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE0ODk1NzA0MjgsIm9yZ2FuaXphdGlvbiI6IjU4YzdlMDc2NzU4N2VjMDAwODBmMzc0YyIsImlzcyI6IjU4YzdlMDc2NzU4N2VjMDAwODBmMzc0YyIsImp0aSI6IjhkYWM0OWNlLTk4YjMtNGI3NC1iZTNmLTY4ZDdhMzU0ZjhhNCIsIm9uZXRpbWUiOmZhbHNlLCJncmFudHMiOlsiZW52aXJvbm1lbnQ6Z2V0OioiXX0.EWjKRAXutQHPuIBZ8qq03dOiAC6aBLWmU_A5OiroS10
```

You can then provide the URL, which is identical to the one
you posted the config to, except instead of ending with
`versions` it ends with `config`:

```Bash
$ export CONFIGSTR_URL=https://api.configstr.io/api/v1/environment/58c7e0a17587ec00080f3750/config
```

Now we'll update our `src/config.py` to use the remote
configuration:

```Python
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
```

Restarting your flask application you should now see
`Hello from the internet!`.

That's it, you are now using remote configuration!
