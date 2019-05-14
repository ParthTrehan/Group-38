#!/bin/bash
#rm hosts
#echo -e "[webserver]\n[harvesters]\n[all]" > hosts
#chmod 777 hosts
. ./openrc.sh;
#ansible-playbook -i hosts --ask-become-pass nectar.yaml
#sleep 180s
ansible-playbook -i hosts --ask-become-pass instance_init.yaml
