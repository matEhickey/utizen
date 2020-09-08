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
5. add utizen to your path
~~~sh
echo 'export PATH=$PATH:/home/user/utizen' >> ~/.bash_profile
~~~
5. install app
6. `utizen install --config refapp/2016 # the config is located at configs/refapp/2016.json`
7. Uninstall all app versions on the device
8. `utizen uninstall --config refapp/2016`