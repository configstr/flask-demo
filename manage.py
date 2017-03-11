import optparse
from src.hello_config import app

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--host', dest='host', default='127.0.0.1')
    parser.add_option('--port', dest='port', default=9999)
    parser.add_option('--debug', action='store_true', default=False)

    (options, args) = parser.parse_args()

    app.run(options.host, options.port, debug=options.debug)
