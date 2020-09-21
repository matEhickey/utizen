# Tizen-upload

## Introduction

## Requirements

### WTV smart-tv-cli package
wtv-package is required to package and sign apps. It can be downloaded from the internal nexus repository using: 
```
$ npm i -g wtv-smart-tv-cli
```

### Samsung Tizen SDK and cli
Install Tizen Studio 3.6 or above with CLI installer.  
Available here: https://developer.tizen.org/development/tizen-studio/download  

Requires the Tizen Studio CLI binaries added to your $PATH for access to the tizen and sdb command-line utilities.

For bash:

```
$ echo 'export PATH="$HOME/tizen-studio/tools/ide/bin:$PATH"' >> ~/.bash_profile
$ echo 'export PATH="$HOME/tizen-studio/tools:$PATH"' >> ~/.bash_profile
```

For Ubuntu Desktop:  

```
$ echo 'export PATH="$HOME/tizen-studio/tools/ide/bin:$PATH"' >> ~/.bashrc
$ echo 'export PATH="$HOME/tizen-studio/tools:$PATH"' >> ~/.bashrc
```

For Zsh:  

```
$ echo 'export PATH="$HOME/tizen-studio/tools/ide/bin:$PATH"' >> ~/.zshrc
$ echo 'export PATH="$HOME/tizen-studio/tools:$PATH"' >> ~/.zshrc
```

## Installation

1. Clone this repository using git
2. `cd utizen`
3. `npm i`
5. install utizen in dev mode (for now)
~~~sh
pip install -e .
~~~

6. add autocomplete to your bashrc
~~~sh
echo 'eval "$(_UTIZEN_COMPLETE=source_bash utizen)"' >> ~/.bashrc
~~~


## How to use

### Configuring tv:  
put all your tv ip and their model (year) in configs/TVs.json  
ex:  
~~~json
{
  "10.1.110.126": "2016",
  "10.1.110.28": "2017",
  "10.1.110.32": "2018",
  "10.1.110.42": "2019",
  "10.1.110.46": "2020"
}
~~~

### Configuring application
Navigate to your deployement folder, and type:  
~~~
utizen create
~~~
And add the app name when asked, or use the cli arguments to define name or path (utizen --help)

### Install app
~~~sh
utizen install --config appname
~~~


### Uninstall all app versions on the device
~~~sh
utizen uninstall --config appname
~~~