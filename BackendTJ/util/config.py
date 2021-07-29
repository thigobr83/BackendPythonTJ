import yaml
import logging.config


class Configuration:

    def __init__(self):

        with open('config.yml', 'r') as stream:
            self.configurations = config = yaml.load(stream, Loader=yaml.FullLoader)

        logging.config.dictConfig(config)
        self.logger = logging.getLogger('client')

    def get_db_url(self):
        return self.configurations['mongodb']['url']

    def get_db_name(self):
        return self.configurations["mongodb"]["db"]

    def get_logger(self):
        return self.logger
