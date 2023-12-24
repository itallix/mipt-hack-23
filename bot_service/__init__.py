from os import getenv

if getenv("FLASK_ENV") != "development":
    import logging

    from google.cloud import logging_v2

    client = logging_v2.Client()
    client.setup_logging(log_level=logging.INFO)
