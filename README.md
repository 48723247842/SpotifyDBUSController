# Spotify DBUS Controller Server

## Necessary Config

```
redis-cli -n 1 set "CONFIG.SPOTIFY_DBUS_CONTROLLER_SERVER" "{\"port\": 11101}"
```

## Notes

1. For virtualenv , need `sudo apt-get install python-dbus`
2. also `sudo apt-get install python3-virtualenv`
3. `python3 -m venv --system-site-packages venv`


## Docker Build Command

```
sudo docker build -t spotify-dbus-controller .
```

## Docker Run Command
```
sudo docker run -dit --restart='always' \
--name 'spotify-dbus-controller' \
--network host \
spotify-dbus-controller
```