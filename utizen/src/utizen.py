import re
import os
import sys
import glob
import json
import shutil
from distutils.dir_util import copy_tree
from utils import add_privilege, execute_cmd, store_uploaded_app, get_app_id

debug_mode = {
    "2016": "NO_DEBUG",
    "2017": "WITH_TIMEOUT",
    "2018": "WITHOUT_TIMEOUT",
    "2019": "WITH_TIMEOUT",
    "2020": "WITHOUT_TIMEOUT"
}

def getTvDebugMode(ip): 
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "configs", "TVs.json")
    with open(filename) as f:
        content = json.loads(f.read())
        return debug_mode[content[ip]]
    
    raise "No tv debug mode for {}".format(ip)


def add_all_privilege(app_name):
    privilege_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "configs", "privileges.txt")
    f = open(privilege_file)
    content = f.readlines()
    f.close()
    
    content = map(lambda x: x.replace("\n", ""), content)
    for i in content:
        add_privilege(app_name, i)

def run(app_name, app_path, ip, port):
    tv_debug = getTvDebugMode(ip)
    
    tizen_profile = "tv-samsung-5.5"
    tizen_template = "BasicEmptyProject"
    tmp = "/tmp/utizen"
    package_tmp = "{}/{}".format(tmp, app_name)

    current_path = os.path.dirname(os.path.realpath(__file__))
    configsFiles = glob.glob(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../configs/*"))
    
    shutil.rmtree(package_tmp, ignore_errors=True);
    
    bootstrap_command = "tizen create web-project -n {} -p {} -t {} -- {}".format(app_name, tizen_profile, tizen_template, tmp);
    print(bootstrap_command)
    out, err = execute_cmd(bootstrap_command)
    if not re.match("Project Location: {}\n".format(package_tmp), out):
        print("Cannot create the project")
        print(out)
        sys.exit()
    
    # copy project file
    copy_tree(app_path, package_tmp)
    
    # move .html to index.html
    other_index = filter(lambda x: os.path.basename(x) != "index.html", glob.glob(package_tmp + "/*.html"))
    if(len(other_index) > 0):
        other_index = other_index[0]
        shutil.move(other_index, os.path.join(package_tmp, "index.html"))
        
    add_all_privilege(app_name)
    # add_privilege(app_name, "http://tizen.org/privilege/telephony")
    # add_privilege(app_name, "http://developer.samsung.com/privilege/drmplay")
    # add_privilege(app_name, "http://developer.samsung.com/privilege/contentsdownload")
    # add_privilege(app_name, "http://developer.samsung.com/privilege/drminfo")
    # add_privilege(app_name, "http://developer.samsung.com/privilege/network.public")
    # add_privilege(app_name, "http://developer.samsung.com/privilege/productinfo")
    # add_privilege(app_name, "http://developer.samsung.com/privilege/sso.partner")
    # add_privilege(app_name, "http://developer.samsung.com/privilege/widgetdata")


    package_command = "wtv-package --with-workspace-only {} --profile {} --output {} -v tizen".format(package_tmp, app_name, package_tmp)
    print(package_command)
    out, err = execute_cmd(package_command)


    install_command = "tizen install -s {}:{} -n {}.wgt -- {}".format(ip, port, app_name, package_tmp)
    print(install_command)
    out, err = execute_cmd(install_command)
    print(out)
    if "Fail" in out:
        sys.exit()


    app_id = get_app_id(package_tmp)
    store_uploaded_app(app_id, app_name, ip)

    run_command = "tizen run -p {}".format(app_id)
    print(run_command)
    out, err = execute_cmd(run_command)

    error_message = "There is no connected target"
    if re.match(error_message, out):
        print(error_message)
        sys.exit()


        debug_command = ""
    if(tv_debug == "NO_DEBUG"):
        print("No debugging needed, exiting now")
        sys.exit()
    elif(tv_debug == "WITH_TIMEOUT"):
        debug_command = "~/tizen-studio/tools/sdb -s {}:{} shell 0 debug {} 300".format(ip, port, app_id)
    elif(tv_debug == "WITHOUT_TIMEOUT"):
        debug_command = "~/tizen-studio/tools/sdb -s {}:{} shell 0 debug {}".format(ip, port, app_id)
    else:
        print("no '{}' debug mode".format(tv_debug))
        sys.exit()
        
    print(debug_command)
    out, err = execute_cmd(debug_command)
    print("'{}'".format(out))
    print("** wip implement parsing to get the debug port")
    # print("debug port: ${port}".format(debug_port))
