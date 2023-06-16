#!/bin/bash

sudo dnf nstall httpd

sudo dnf install git

sudo dnf install vim

dnf install openvpn easy-rsa

dnf install gpsd-clients.x86_64

sudo dnf -y install dnf-plugins-core

sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose

sudo systemctl start docker

