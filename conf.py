import json


class Config:
    @staticmethod
    def get_config(item):
        config = Config.__open_config_file()
        return config[item]

    @staticmethod
    def set_last_prize(value):
        config = Config.__open_config_file()
        config['last_prize_scraped'] = value
        with open("conf.json", "w") as full_config:
            json.dump(config, full_config)

    @staticmethod
    def __open_config_file():
        with open("conf.json", "r") as full_config:
            config = json.load(full_config)
            return config
