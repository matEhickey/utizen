import os
import re
import sys
import subprocess
import json
import glob
import xml.etree.ElementTree as ET

def get_configs_files():
    glob_configs = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "configs", "projects", "*.json")
    return glob.glob(glob_configs)

def get_configs_names():
    config_files = get_configs_files()
    return map(lambda x: x.split("/")[-1].split(".")[0], config_files)

def get_configs_names_autocomplete(ctx, args, incomplete):
    config_names = get_configs_names()
    return filter(lambda x: x.startswith(incomplete), config_names)

def parseXML(filename):
    return ET.parse(filename).getroot()

def get_app_id(package_tmp):
    filename = "{}/config.xml".format(package_tmp)
    root = parseXML(filename)
    app_id = filter(lambda x: x[0] == "id", root.getchildren()[0].items())[0][1]
    return app_id

def execute_cmd(cmd):
    # proc = subprocess.Popen(cmd, shell=True)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out, err

def add_privilege(appName, privilege):
    scriptPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "addPrivilege.js")
    execute_cmd("node {} {} {}".format(scriptPath, appName, privilege))

def store_uploaded_app(app_id, app_name, ip):
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "installed", ip, "{}.txt".format(app_name))
    dirname = os.path.abspath(os.path.abspath(os.path.join(filename, os.pardir)))
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    execute_cmd("echo '{}' >> {}".format(app_id, filename))

def get_connected_tv_ip_port():
    out, err = execute_cmd("~/tizen-studio/tools/sdb devices")
    match = re.match("List of devices attached \n(\S+\.\S+\.\S+\.\S+:\S+)", out)
    if match:
        return match.groups()[0].split(":")
    else:
        print("No TV connected")
        sys.exit(-1)

def get_config(config_name):
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "configs", "projects", "{}.json".format(config_name))

    config = {}
    with open(filename) as f:
        content = json.loads(f.read())
        config["app_name"] = str(content["app_name"])
        config["app_path"] = str(content["app_path"])
        config["privileges"] = content["privileges"] if "privileges" in content else []

    return config, filename

def save_config_file(name, content):
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "configs", "projects", "{}.json".format(name))
        filecontent = json.dumps(content, sort_keys=True, indent=4)

        dirname = os.path.abspath(os.path.abspath(os.path.join(filename, os.pardir)))
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        f = open(filename, "w")
        f.write(filecontent)
        f.close()

        print("* Config file created at {}".format(filename))


def get_all_privileges():
    privilege_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "configs", "privileges.txt")
    f = open(privilege_file)
    content = f.readlines()
    f.close()

    content = map(lambda x: x.replace("\n", ""), content)
    return content