import os
import requests
import logging

LOG_FILE = os.path.join("logs", "api_test.log")
if not os.path.exists("logs"):
    os.makedirs("logs")

logger: logging.Logger = logging.getLogger("content")
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
    logger.info(f"Writing detailed log to {LOG_FILE}")
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8-sig')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    # add handlers to logger
    logger.addHandler(file_handler)

# définition de l'adresse de l'API
api_address = os.environ.get('API_HOST', 'localhost')
# port de l'API
api_port = 8000
credentials = {'username': 'alice',
               'password': 'wonderland'}
# définition des phrases de test et du sentiment attendu en retour
test_sentences = [('I love you', 'positive'),
                  ('I hate you', 'negative'),
                  ('life is beautiful', 'positive'),
                  ('that sucks', 'negative')]

for sentence, expected_sentiment in test_sentences:
    for version in ['v1', 'v2']:
        # requête (avec le mot de passe dans l'URL, pas bien !)
        credentials.update({'sentence': sentence})
        r = requests.get(
            url=f'http://{api_address}:{api_port}/{version}/sentiment',
            params= credentials
        )
        logger.info("Requesting %s", r.url)
        score = r.json()["score"]
        sentiment = 'positive' if score > 0 else 'negative'
        if sentiment == expected_sentiment:
            logger.info("API returned %s sentiment as expected (score=%s)", sentiment, score)
        else:
            logger.error("API returned %s sentiment, when a %s was expected (score=%s)", 
                         sentiment, expected_sentiment, score)
                      