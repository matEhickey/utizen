import re
import os
import sys
import glob
import json
import shutil
from distutils.dir_util import copy_tree
from utils import *
import settings

TMP = "/tmp/utizen"

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


def add_own_privilege(config):
    app, filename = get_config(config)

    for i in app["privileges"]:
        add_privilege(app["app_name"], i)

def add_privilege_to_config(config, privileges):
    app, filename = get_config(config)

    content = {
        "app_name": app["app_name"],
        "app_path": app["app_path"],
        "privileges": privileges
    }

    save_config_file(app["app_name"], content)

def run(config, ip, port):
    app, filename = get_config(config)
    tv_debug = getTvDebugMode(ip)

    package_tmp = os.path.join(TMP, app["app_name"])

    shutil.rmtree(package_tmp, ignore_errors=True)

    package_app(config)


    install_command = "tizen install -s {}:{} -n {}.wgt -- {}".format(ip, port, app["app_name"], package_tmp)
    print(install_command)
    out, err = execute_cmd(install_command)
    print(out)
    if "Fail" in out:
        sys.exit()


    app_id = get_app_id(package_tmp)
    store_uploaded_app(app_id, app["app_name"], ip)

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

def package_app(config):
    app, filename = get_config(config)

    tizen = "~/tizen-studio/tools/ide/bin/tizen"
    app_name = app["app_name"]
    workspace = os.path.join(TMP, app_name)
    tizen_profile = "tv-samsung-5.5"
    tizen_template = "BasicEmptyProject"
    security_profile = "tv-samsung"
    cert_filename = "wiztivi.p12"
    certificate_absolute_path = os.path.join("~/tizen-studio-data/keystore/author", cert_filename)
    cert_alias = "tv-samsung"
    package_format = "wgt"
    output = workspace

    cert_password = settings.get("CERT_PASSWORD")
    cert_email = settings.get("CERT_EMAIL")
    cert_country = settings.get("CERT_COUNTRY")


    tizen_commands = {
        "create": "{tizen} create web-project -n {app_name} -p {tizen_profile} -t {tizen_template} -- {tmp_path}".format(tizen=tizen, app_name=app_name, tizen_profile=tizen_profile, tizen_template=tizen_template, tmp_path=TMP),
        "build": "{tizen} build-web -- {workspace}".format(tizen=tizen, workspace=workspace),
        "generateCertificate": "{tizen} certificate -a {cert_alias} -p {cert_password} -e {cert_email} -c {cert_country} -f {cert_filename}".format(tizen=tizen, cert_alias=cert_alias, cert_email=cert_email, cert_country=cert_country, cert_filename=cert_filename, cert_password=cert_password),
        "generateSecurityProfile": "{tizen} security-profiles add -n {security_profile} -p {cert_password} -a {certificate_absolute_path}".format(tizen=tizen, security_profile=security_profile, cert_password=cert_password, certificate_absolute_path=certificate_absolute_path),
        "generatePackage": "{tizen} package -t {package_format} -s {security_profile} -o {output} -- {workspace}".format(tizen=tizen, package_format=package_format, security_profile=security_profile, output=output, workspace=workspace),
    }

    # create the project
    execute_cmd(tizen_commands["create"])

    # copy project files
    copy_tree(app["app_path"], workspace)

    # move .html to index.html
    other_index = filter(lambda x: os.path.basename(x) != "index.html", glob.glob(workspace + "/*.html"))
    if(len(other_index) > 0):
        other_index = other_index[0]
        shutil.move(other_index, os.path.join(workspace, "index.html"))

    # add privileges
    add_own_privilege(config)

    # executes last steps
    for step in ["build", "generateCertificate", "generateSecurityProfile", "generatePackage"]:
        print("{}: \n\t{}\n".format(step, tizen_commands[step]))
        execute_cmd(tizen_commands[step])