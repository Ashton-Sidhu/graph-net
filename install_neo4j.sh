#!/bin/bash

# Add repo keys
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list

# Install packages
sudo apt-get update
sudo apt-get install neo4j -y

echo "Please run:"
echo "echo neo4j-admin set-initial-password `your_password`" 
