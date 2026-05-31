#!/bin/bash
set -euo pipefail # we learned from cloudflare right

echo "Hello! Welcome to the Slick Stats++ Installer :D"
echo "This script will install a daemon via launchctl, as well as setting up a few extras."
echo "Do you consent to this? If not, please enter N. Otherwise, enter Y."

read -p "Enter Y or N: " consent

# continuously read consent until valid input
until [ "$consent" = "Y" ] || [ "$consent" = "N" ]
do
    echo "Please input either Y or N."
    read -p "Enter Y or N: " consent
done

if [ "$consent" = "N" ]; then
    echo "Quitting..."
    exit 0
fi

echo "Dropping script at /tmp/slickstats++ for oauth..."

which python
# drop a simple script to do oauth (located at /scripts/oauth/main.py on github), then wait for it to complete
