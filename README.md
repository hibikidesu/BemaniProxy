# UNFINSHED PROJECT - NOT READY FOR USE

# BemaniProxy
Adds the ablity to record your stats, track progress, enable flags from which the server does not provide.
This is not made for editing outbound data.

## Requirements
- [Python 3](https://www.python.org/downloads/)

## Installation

```bash
pip install git+https://github.com/hibikidesu/BemaniProxy.git
```

or download this repo and run `<python3 interpreter> setup.py install`

## Usage

Run the proxy with 

```bash
bemaniproxy example.com
```

Set your server url on your game to http://ip:port displayed on proxy launch

A web server will also be running which you can access with your web browser which records your data

A sqlite db file will be used or created at your current working directory.