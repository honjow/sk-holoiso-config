#!/bin/bash

alsaconfigPath="/usr/share/wireplumber/main.lua.d/50-alsa-config.lua"

sed -i 's/ \["audio.format"\]/ --\["audio.format"\]/' $alsaconfigPath
sed -i 's/ \["audio.rate"\]/ --\["audio.rate"\]/' $alsaconfigPath
sed -i 's/48000/44100/' $alsaconfigPath 