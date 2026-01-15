import os
import json

class ConfigReader:
    _config=None
    
    @staticmethod
    def load_config():
        """Load configuration from testsetting.json if not already loaded"""
        if ConfigReader._config is None:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'testsetting.json')
            with open(config_path, 'r') as config_file:
                ConfigReader._config= json.load(config_file)
        return ConfigReader._config

    @staticmethod
    def get_base_url():
        """Get the base URL from the configuration"""
        return ConfigReader.load_config()['base_url']
    @staticmethod
    def get_api_url():
        """Get the API URL from the configuration"""
        return ConfigReader.load_config()['api_url']
    @staticmethod
    def get_username():
        """Get the username from the configuration"""
        return ConfigReader.load_config()['credentials']['username']
    @staticmethod
    def get_password():
        """Get the password from the configuration"""
        return ConfigReader.load_config()['credentials']['password']
    @staticmethod
    def get_time_out():
        """Get the timeout configuration"""
        return ConfigReader.load_config()['timeout']


