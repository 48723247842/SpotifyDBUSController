#!/bin/bash
sudo docker run -dit --restart='always' \
--name 'spotify-dbus-controller' \
--network host \
spotify-dbus-controller