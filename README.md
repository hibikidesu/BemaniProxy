# UNFINSHED PROJECT - NOT READY FOR USE

# BemaniProxy
Adds the ablity to record your stats, track progress, enable flags from which the server does not provide.
This is not made for editing outbound data.

## Usage

- Download Python 3
- Download this repo
- run `<python3 interpreter> -m pip install -Ur requirements.txt`
- run `uwsgi --ini bemaniproxy.ini`

Edit the config.json in this directory and enter your server url. Set your game url to http://YOURIP:8050

A web server will also be running which you can access with your web browser which records your data

## Features

- Unlimited Paseli
- Score tracking (sdvx5)
- Shop name change locally (not server side)
- paseli force disable

## TODO
- opcheckin
- iidx support
- sdvx<5 support
- pcbevents
