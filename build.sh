#!/usr/bin/env bash
# Install Firefox
apt-get update
apt-get install -y firefox-esr

# Install geckodriver
GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -o 'v[0-9]\.[0-9]\.[0-9]'`
wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz
tar -xzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz
chmod +x geckodriver
mv geckodriver /usr/local/bin/