import os
import re
import subprocess
import xml.etree.ElementTree as ET

def parseXML(filename):
    return ET.parse(filename).getroot()

def get_app_id(package_tmp):
    filename = "{}/config.xml".format(package_tmp)
    root = parseXML(filename)
    app_id = filter(lambda x: x[0] == "id", root.getchildren()[0].items())[0][1]
    return app_id
    
def execute_cmd(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out, err

def add_network_privilege(appName, privilege):
    scriptPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "addPrivilege.js")
    execute_cmd("node {} {} {}".format(scriptPath, appName, "http://tizen.org/privilege/telephony"))

def store_uploaded_app(app_id, app_name):
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "installed", "{}.txt".format(app_name))
    dirname = os.path.abspath(os.path.abspath(os.path.join(filename, os.pardir)))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        
    execute_cmd("echo '{}' >> {}".format(app_id, filename))

def get_connected_tv_ip_port():
    out, err = execute_cmd("~/tizen-studio/tools/sdb devices")
    match = re.match("List of devices attached \n(\S+\.\S+\.\S+\.\S+:\S+)", out)
    if match:
        return match.groups()[0].split(":")