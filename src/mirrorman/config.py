import configparser
import os
import sys

config = configparser.ConfigParser()
# check environment variables
configPath = os.environ.get("MIRRORMAN_CONFIG")
if configPath is None:
    configPath = "mirrorman.conf"
config.read(configPath)
# check config file
if not config.has_section("mirrorman"):
    print("Error: config file is missing the mirrorman section")
    sys.exit(1)
# the funny getter
def get(option, default=None):
    if config.has_option("mirrorman", option):
        return config.get("mirrorman", option)
    else:
        return default
