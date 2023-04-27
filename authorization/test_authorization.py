import os
import requests
import logging

LOG_FILE = os.path.join("logs", "api_test.log")
if not os.path.exists("logs"):
    os.makedirs("logs")

logger: logging.Logger = logging.getLogger("authorization")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
# create formatter
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s", 
                              "%Y-%m-%d %H:%M:%S")
# add formatter to stream_handler
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
if os.environ.get('LOG') == '1':
    logger.info("Writing detailed log to {LOG_FILE}")
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8-sig')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    # add handlers to logger
    logger.addHandler(file_handler)

# définition de l'adresse de l'API
api_address = os.environ.get('API_HOST', 'localhost')
# port de l'API
api_port = 8000
# définition des identifiants de test
credentials_list = [{'username': 'alice',
                     'password': 'wonderland'}, 
                    {'username': 'bob',
                     'password': 'builder'}]
authorizations = {'alice': ['v1', 'v2'],
                  'bob': ['v1']}

for credentials in credentials_list:
    for version in ['v1', 'v2']:
        # requête (avec le mot de passe dans l'URL, pas bien !)
        credentials.update({'sentence': "whatever"})
        r = requests.get(
            url=f'http://{api_address}:{api_port}/{version}/sentiment',
            params= credentials
        )
        logger.info("Requesting %s", r.url)
        expected_return_code = 200 if version in authorizations[credentials['username']] else 403
        if r.status_code == expected_return_code:
            logger.info("API returned code %s as expected", r.status_code)
        else:
            logger.error("API returned code %s; expected code is %s", r.status_code, expected_return_code)
                      