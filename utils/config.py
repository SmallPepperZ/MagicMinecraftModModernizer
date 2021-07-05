import configparser

config_obj = configparser.ConfigParser()
config_obj.read("settings.cfg")
configuration = config_obj["SETTINGS"]