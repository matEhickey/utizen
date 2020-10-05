import os
import time
from .utils import get_config

def get_connected_device():
    return "LG"

def run(config):
    app, filename = get_config(config)
    # app = {
    #     "app_name": "example",
    #     "app_path": "/home/mdidier/Prog/LG_first/src",
    #     "LG": {}
    # }

    package_id = "com.wtv.{}".format(app["app_name"])
    version = "0.0.1"
    device = get_connected_device()

    input_folder = app["app_path"]
    package_tmp = "/tmp/utizenLG/{}".format(app["app_name"])
    package_file = os.path.join(package_tmp, "{}_{}_all.ipk".format(package_id, version))


    COMMANDS = {
        "package": "ares-package --no-minify {} -o {}".format(input_folder, package_tmp),
        "install": "ares-install --device {} {}".format(device, package_file),
        "launch": "ares-launch --device {} {}".format(device, package_id)
    }

    for step in ["package", "install", "launch"]:
        print(step)
        print("\t\t", COMMANDS[step])
        time.sleep(0.5)