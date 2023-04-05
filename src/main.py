import logging
import json

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w")
    logger = logging.getLogger(__name__)

    logger.info("Starting up")

    logger.info("Reading config")
    with open("conf.json") as f:
        config = json.load(f)

    logger.info("Config: {}".format(config))

    logger.info("Shutting down")