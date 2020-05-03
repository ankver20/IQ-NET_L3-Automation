#!/usr/bin/env python

from datetime import datetime
from netmiko import ConnectHandler
import time
import json
import yaml
import os
import sys

# file_path =  os.path.pardir()
# print file_path
# file_path =  os.path.dirname(os.path.basename(__file__))

file_path = os.path.dirname(os.path.realpath(__file__))

def get_data():
    with open(file_path + '/../Topology/IP_ServicesTopology.yml') as data_file:
        data = yaml.load(data_file, Loader=yaml.FullLoader)
    return data

# Added to check above yml file details while testing only
# devices_dict = get_data()
# devicename = '9K_R2'
# a_device = devices_dict['Device_Details'][devicename]
# print (a_device)


def make_connection(a_device):
    #devices_dict = get_data()
    #a_device = devices_dict['Device_Details']['R1']
    net_connect = ConnectHandler(**a_device)
    net_connect.enable()
    print (net_connect)
    time.sleep(5)
    print("{}: {}".format(net_connect.device_type, net_connect.find_prompt()))
    return net_connect

def make_connection_accedian(a_device):
    #devices_dict = get_data()
    #a_device = devices_dict['Device_Details']['R1']
    net_connect = ConnectHandler(**a_device)
    #net_connect.enable()
    print(net_connect)
    time.sleep(5)
    print("{}: {}".format(net_connect.device_type, net_connect.find_prompt()))
    return net_connect

def close_connection(net_connect):
    net_connect.disconnect()
    print(str(net_connect) + " connection closed")


def main():
    start_time = datetime.now()


if __name__ == "__main__":
    main()
