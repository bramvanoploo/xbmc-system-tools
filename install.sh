#!/bin/bash
#
# @author   Bram van Oploo
# @email    info@sudo-systems.com
# @date     2013-03-21
# @version  1.0.0 alpha 2
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

PROGRAM_PATH=$HOME"/.xsyst"
INITD_PATH="/etc/init.d/xsyst"

cd ~
git clone -q https://github.com/Bram77/xbmc-system-tools.git .xsyst > /dev/null 2>&1
cd $PROGRAM_PATH
git pull > /dev/null 2>&1
sudo cp $PROGRAM_PATH"/initd_ubuntu" $INITD_PATH > /dev/null 2>&1
sudo sed -i "s/|program_path|/$(echo $PROGRAM_PATH | sed -e 's/\\/\\\\/g' -e 's/\//\\\//g' -e 's/&/\\\&/g')/g" $INITD_PATH
sudo chmod +x $INITD_PATH > /dev/null 2>&1
sudo update-rc.d xsyst defaults > /dev/null 2>&1
sudo service xsyst start

SYSTEM_IP=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}')

echo "* Xbmc System Tools has successfully been installed."
echo "* Please open the following address http://"$SYSTEM_IP":8092 in your browser"
exit
