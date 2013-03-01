#!/bin/sh
#
# @author   Bram van Oploo
# @date     2013-02-12
# @version  3.0.0 alpha 1
#

clear

echo ""
echo "XBMC System Tools installation script"
echo ""
echo "* Updating software sources, upgrading packages and installing requirements..."
sudo apt-get update > /dev/null 2>&1
sudo apt-get -y dist-upgrade > /dev/null 2>&1
sudo apt-get -y install git-core python-software-properties software-properties-common ppa-purge python python-flask python-apt python-beautifulsoup python-git unzip tar > /dev/null 2>&1

echo "* Downloading and configuring Xbmc System Tools as a system service"
cd /usr/local/share
sudo git clone -q https://github.com/Bram77/xbmc-system-tools.git xsyst > /dev/null 2>&1
cd ./xsyst > /dev/null 2>&1
sudo cp ./initd_ubuntu /etc/init.d/xsyst > /dev/null 2>&1
sudo chmod +x /etc/init.d/xsyst > /dev/null 2>&1
sudo update-rc.d xsyst defaults > /dev/null 2>&1
sudo service xsyst start

SYSTEM_IP=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}')

echo "* Xbmc System Tools has successfully been installed."
echo "* Please open the following address http://"$SYSTEM_IP":8091 in your browser"
exit
