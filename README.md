# Utizen

## Introduction

## Requirements

### Samsung Tizen SDK and cli
Install Tizen Studio 3.6 or above with CLI installer.  
Available here: https://developer.tizen.org/development/tizen-studio/download  

Requires the Tizen Studio CLI binaries added to your $PATH for access to the tizen and sdb command-line utilities.

```
$ echo 'export PATH="$HOME/tizen-studio/tools/ide/bin:$PATH"' >> ~/.bashrc
$ echo 'export PATH="$HOME/tizen-studio/tools:$PATH"' >> ~/.bashrc
```

## Installation

1. Clone this repository using git  
`git clone https://github.com/matEhickey/utizen && cd utizen`

3. Install some npm libraries (wip to remove)  
`npm i`

4. Install utizen via pip  
~~~sh
pip install .
# or editable mode
pip install -e .
~~~

5. (Recommended) Add autocomplete to your \_shrc
~~~bash
# utizen autocomplete
if [ ! -n "$BASH" ] # if bash use this
then 
	. ~/Prog/utizen/utizen-zsh-complete.sh
else # you are probably using zsh
	. ~/Prog/utizen/utizen-bash-complete.sh
fi
~~~


## How to use
### Configuring tv:  
Fill all your tv IP and their model (year) in configs/TVs.json as:  
~~~json
{
  "10.1.110.126": "2016",
  "10.1.110.28": "2017",
  "10.1.110.32": "2018",
  "10.1.110.42": "2019",
  "10.1.110.46": "2020"
}
~~~

Utizen will upload apps on the tv connected via the device manager  

### Configuring application
Navigate to your deployement folder, and type:  
~~~sh
utizen create
~~~  

And add the app name when asked, or use the cli arguments to define name or path (utizen --help)

To show the config, just type:  
~~~sh
utizen config <config>
~~~  

To list all the config availables:  
~~~sh
utizen ls
~~~  


### Install app
~~~sh
utizen install <config>
~~~

### Tweakings privileges of a config
~~~sh
utizen show-privileges <config> # to show all privileges that the app have
utizen set-privileges <config> # select in a list all the privileges needed
~~~

### Uninstall
Every new installation will be differents to keep track of changes, regenerating the tizen each time.  
It might be long to uninstall all version by hand, so this command will delete all <config> app installed on the TV  

~~~sh
utizen uninstall <config>
~~~
