#!/usr/bin/env python2

import os
import sys
import json
import click
import glob
import pick
from utizen import run, execute_cmd, add_privilege_to_config
from utils import get_connected_tv_ip_port, get_all_privileges, get_config, save_config_file

def get_config_names_autocomplete(ctx, args, incomplete):
    glob_configs = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "configs", "projects", "*.json")
    
    return filter(lambda x: x.startswith(incomplete), map(lambda x: x.split("/")[-1].split(".")[0], glob.glob(glob_configs)))

@click.command()
@click.argument('config', type=click.STRING, autocompletion=get_config_names_autocomplete, metavar='<config name>')
def install(config):
    ip, port = get_connected_tv_ip_port()
    run(config, ip, port)
        
@click.command()
@click.argument('config', type=click.STRING, autocompletion=get_config_names_autocomplete, metavar='<config name>')
def uninstall(config):
    app, filename = get_config(config)
    app_name = app["app_name"]
    ip, port = get_connected_tv_ip_port()
    
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
        "app_path": path,
        "privileges": [
            "http://tizen.org/privilege/telephony",
            "http://tizen.org/privilege/internet"
        ]
    }
    
    save_config_file(name, content)

@click.command()
def tv():
    ip, port = get_connected_tv_ip_port()
    print "{}:{}".format(ip, port)

@click.command()
@click.argument('config', type=click.STRING, autocompletion=get_config_names_autocomplete, metavar='<config name>')
def set_privileges(config):
    title = 'Choose the privileges to set to the app (press SPACE to mark, ENTER to continue):'
    options = get_all_privileges()
    selected = pick.pick(options, title, multiselect=True, min_selection_count=0)
    
    privileges = [s[0] for s in selected]
    click.secho("Will set the following privileges to {}:".format(config), bg='red', fg='white')
    for i in privileges:
        click.secho(i)
    
    
    click.secho("Are you sure ?", bg='red', fg='white')
    if not click.confirm(""):
        click.secho("Aborted", bg='black', fg='white')
    else:
        add_privilege_to_config(config, privileges)
        print("{} privileges set to {}".format(len(privileges), config))

@click.command()
@click.argument('config', type=click.STRING, autocompletion=get_config_names_autocomplete, metavar='<config name>')
def show_privileges(config):
    app, filename = get_config(config)
    click.secho("Privileges of '{}' app:", bg="blue")
    for i in app["privileges"]:
        click.secho(i)
    
    
@click.group()
def cli():
    pass

# autocomplete need this to be defined (when use globaly, __name__ != __main__)
for command in  [install, uninstall, create, tv, set_privileges, show_privileges]:
    cli.add_command(command)
    
if(__name__=="__main__"):
    cli()
