#!/bin/bash

# script to initalize settings of buildroot for Raspberry Pi zero linux system compilation

tar -xzf buildroot-2023.02_bike.tar.gz

echo "Specify your SSID and password in file zero_w_bike/etc/wpa_supplicant.conf"

echo "Specify your openvpn sertificates in file zero_w_bike/etc/openvpn/client/openvpn-user-r.conf"

echo "Specify your root password in file buildroot-2023.02/.config in line BR2_TARGET_GENERIC_ROOT_PASSWD"


