#!/usr/bin/env python2

import os
import sys
import json
import click
import glob
from utizen import run, execute_cmd
from utils import get_connected_tv_ip_port
from pprint import pformat

def get_config_names(ctx, args, incomplete):
    glob_configs = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "configs", "projects", "*.json")
    
    return filter(lambda x: x.startswith(incomplete), map(lambda x: x.split("/")[-1].split(".")[0], glob.glob(glob_configs)))

@click.command()
@click.argument('config', type=click.STRING, autocompletion=get_config_names, metavar='<config name>')
def install(config):
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "configs", "projects", "{}.json".format(config))    
    with open(filename) as f:
        content = json.loads(f.read())
        app_name = str(content["app_name"])
        app_path = str(content["app_path"])
        ip, port = get_connected_tv_ip_port()
                
        run(app_name, app_path, ip, port)
        
@click.command()
@click.argument('config', type=click.STRING, autocompletion=get_config_names, metavar='<config name>')
def uninstall(config):
    ip, port = get_connected_tv_ip_port()
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "configs", "projects", "{}.json".format(config))
    
    with open(filename) as f:
        content = json.loads(f.read())
        app_name = str(content["app_name"])
        installed_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "installed", ip, "{}.txt".format(app_name))
        with open(installed_filename) as installed_file:
            for app_id in installed_file.readlines():
                app_id = app_id.replace("\n", "")
                uninstall_command = "tizen uninstall -p {}".format(app_id)
                print(uninstall_command)
                out, err = execute_cmd(uninstall_command)
                print(out)
        os.remove(installed_filename)
                
@click.command()
@click.option('--name', prompt='App name (camelCaseWithoutSymbols)', help='The name of the app (camelCaseWithoutSymbols)')
@click.option('--app_path', default= '.', help='The path of the app')
def create(name, app_path):
    path = os.path.abspath(os.path.join(os.getcwd(), app_path))
    
    content = {
        "app_name": name,
        "app_path": path
    }
    
    filecontent = json.dumps(content, sort_keys=True, indent=4)
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "configs", "projects", "{}.json".format(name))
    
    dirname = os.path.abspath(os.path.abspath(os.path.join(filename, os.pardir)))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    f = open(filename, "w")
    f.write(filecontent)
    f.close()
    
    print("* Config file created at {}".format(filename))

@click.command()
def tv():
    ip, port = get_connected_tv_ip_port()
    print "{}:{}".format(ip, port)


@click.group()
def cli():
    pass

# autocomplete need this to be defined (when use globaly, __name__ != __main__)
for command in  [install, uninstall, create, tv]:
    cli.add_command(command)
    
if(__name__=="__main__"):
    cli()
