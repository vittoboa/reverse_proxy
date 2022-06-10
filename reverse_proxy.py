import yaml
import requests
import itertools
from http.server import BaseHTTPRequestHandler, HTTPServer


def parse_yaml(file):
    """ Parse a yaml file """

    with open(file, 'r') as stream:
        parsed_obj = yaml.safe_load(stream)

    return parsed_obj


class ReverseProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_HEAD(self):
        """ Serves the 'HEAD' request type """

        self.do_GET(body=False)


    def do_GET(self, body=True):
        """ Serves the 'GET' request type """

        is_request_sent = False

        try:
            # identify the requested service using the Host Http header
            host_header = self.headers.get('Host')
            service = services.get(host_header)

            # identify the host using round robin load balancing strategy
            host = self.round_robin(service['hosts'])

            # define url
            port = host['port']
            address = host['address']
            url = f'http://{address}:{port}{self.path}'

            # send request
            resp = requests.get(url, verify=False)
            msg = resp.text.encode('utf-8')
            is_request_sent = True

            # set headers
            self.send_response(resp.status_code)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', str(len(msg)))
            self.end_headers()

            # forward to the client the requested data
            if body:
                self.wfile.write(msg)
        finally:
            if not is_request_sent:
                self.send_error(404, 'Error occurred while trying to proxy')
    

    def round_robin(self, hosts):
        """ Implement round-robin load balancing strategy by cycling through hosts """

        return next(hosts)


if __name__ == "__main__":
    # retrieve reverse proxy configuration file
    config = parse_yaml('proxy.yaml')

    # organize services by their domain name
    services = {service['domain']: service
                for service in config['proxy']['services']}

    # prepare hosts lists based on the round-robin strategy
    for domain, service in services.items():
        # make an iterator to cycle between hosts
        services[domain]['hosts'] = itertools.cycle(service['hosts'])

    # retrieve server informations
    address = config['proxy']['listen']['address']
    port = config['proxy']['listen']['port']
    server_address = (address, port)
    # create and run the server
    httpd = HTTPServer(server_address, ReverseProxyHTTPRequestHandler)
    httpd.serve_forever()
