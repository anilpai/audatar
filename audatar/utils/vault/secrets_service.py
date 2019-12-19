import time
import logging
import json
import sys
import os

from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from .environ import environment

SLEEP = 1
MAX_ATTEMPTS = 300
secrets_service = None


class SecretsClientResource(BaseHTTPRequestHandler):
    """Http REST Resource Class for receving the secrets from Secret-Service
    Server."""
    secrets = None

    def do_GET(self):
        """ @GET /alive.txt
        For Multi-Paas health check
        :return: Response "OK" if successful
        """
        if self.path == '/alive.txt':
            self.send_response_and_message(200, 'OK')
        else:
            self.send_response_and_message(404, 'NOT FOUND')

    def do_POST(self):
        """ @POST /v1/secrets
        Receive the Secrets and store in variable 'secrets_service.secrets'
        :return: Response "OK" if successful
        """
        message = 'NOT FOUND'
        response = 404

        if self.path == '/v1/secrets':
            message = 'OK'
            response = 200
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            secrets_service.secrets = data.decode(encoding='utf8')

        self.send_response_and_message(response, message)

    def send_response_and_message(self, response, message):
        """Helper method to build the http response."""
        self.send_response(response)
        self.send_header('Content-type',  'text/plain')
        self.end_headers()
        self.wfile.write(str(message).encode('utf8'))


class SecretServiceException(Exception):
    pass


class SecretsService:
    """Class that has methods to start and stop the HTTP secret-service client
    server."""

    def __init__(self):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.setLevel(logging.INFO)
        self.secretClientHttpServer = HTTPServer(('', HTTP_PORT), SecretsClientResource)
        self.secrets = None
        self.server_thread = Thread(name='SecretService', target=self.secretClientHttpServer.serve_forever)
        print('Http server for receiving Secrets Initialized in port...' + str(HTTP_PORT))

    def start_server(self):
        """Start the HTTP server in the provided HTTP_PORT.

        :return: None
        """
        self.server_thread.start()
        self.logger.info('start_server: server started')
        print('HTTP Server started...')

    def stop_server(self):
        """Check if the HTTP server has started already then proceed to stop.

        :return: None
        """
        if self.server_thread.is_alive():
            self.secretClientHttpServer.shutdown()
            self.server_thread.join()
            self.logger.info('stop_server: server stopped')
            print('HTTP Server Stopped.')

    def wait_for_secrets(self):
        """This method waits for remote Secret-Service server to POST the
        secrets to SecretsClientResource.do_POST method."""
        attempts = 0
        while not self.secrets:
            message = 'wait_for_secrets: secrets not recieved. (attempt=%d)' % (attempts + 1)
            print(message)
            self.logger.info(message)
            time.sleep(SLEEP)
            attempts += 1
            if attempts >= MAX_ATTEMPTS:
                message = 'wait_for_secrets: no secrets received after %s seconds.' % MAX_ATTEMPTS
                self.logger.warning(message)
                raise SecretServiceException(message)
        return self.secrets


def accept_secrets_and_write_to_a_file(required_secrets):
    """Receive the secrets, and write to a file secrets.properties.

    :param required_secrets: required secrets for writing
    :return: None
    """

    print('Waiting for secrets.....')
    print('Environment:{0}'.format(environment))

    secrets_json = secrets_service.wait_for_secrets()
    secrets = json.loads(secrets_json)
    secret_tokens = secrets['secretTokens']

    if required_secrets is not None:
        for req in required_secrets:
            if req not in secret_tokens:
                print(str(secret_tokens))
                raise Exception('`' + req + '` not in found in secrets.')

    print('Writing secrets properties.....')
    file_path = os.path.sep.join(os.path.dirname(__file__).split(os.path.sep)[:-3])
    env_file_url = os.path.join(file_path, 'secrets.properties')
    with open(env_file_url, 'w+') as secrets_file:
        for key in secret_tokens:
            secrets_file.write(key + '=' + str(secret_tokens[key]))
            secrets_file.write('\n')
    print('Finished writing secrets properties...')

    print('Writing to ui environment.....')
    file_path = os.path.sep.join(os.path.dirname(__file__).split(os.path.sep)[:-3])
    env_file_url = os.path.join(file_path, 'audatar-ui/.env')
    with open(env_file_url, 'w+') as env_file:
        for key in secret_tokens:
            if key == 'react_app.base_api_url':
                env_file.write('REACT_APP_BASE_API_URL=' + secret_tokens[key])
                env_file.write('\n')
    print('Finished writing to env file...')

    print('Writing flower credentials.....')
    file_path = os.path.sep.join(os.path.dirname(__file__).split(os.path.sep)[:-3])
    env_file_url = os.path.join(file_path, 'setup_scripts/flower_creds.txt')
    with open(env_file_url, 'w+') as env_file:
        if 'flower.username' in secret_tokens and 'flower.password' in secret_tokens:
            env_file.write('{0}:{1}'.format(secret_tokens['flower.username'], secret_tokens['flower.password']))
            env_file.write('\n')
    print('Finished writing flower credentials...')


""" Application Starts here."""


def main(port=10080, attempts=300, required_secrets=None):
    """Handle exceptions while starting HTTP server in the HTTP_PORT.

    :param port: HTTP port, default is 10080
    :param attempts: attempts to fetch secrets, default is 300
    :param required_secrets: secrets required
    :return: None
    """
    global HTTP_PORT, secrets_service, MAX_ATTEMPTS
    try:
        HTTP_PORT = port
        print('HTTP Port:' + str(HTTP_PORT))
        MAX_ATTEMPTS = attempts

        secrets_service = SecretsService()
        secrets_service.start_server()
        accept_secrets_and_write_to_a_file(required_secrets)
        secrets_service.stop_server()
    except SecretServiceException:
        print('fatal: Error getting secrets. Shutting down.')
        secrets_service.stop_server()
        sys.exit(1)
