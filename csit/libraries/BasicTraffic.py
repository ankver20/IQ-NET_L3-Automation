
##############################################################
#Loading HLTAPI for Python
##############################################################
from __future__ import print_function
import sth
import time
import json
import os
import sys
import yaml
import re
from pprint import pprint


# file_path =  os.path.pardir()
# print file_path
# file_path =  os.path.dirname(os.path.basename(__file__))
file_path = os.path.dirname(os.path.realpath(__file__))
def spirent_items():
    # data = yaml.load(open('Spirent_Test_Topology.yaml'), Loader=yaml.Loader)

    with open( file_path + '\..\libraries\Spirent_Test_Topology.yaml') as data_file:
        data = yaml.load(data_file,Loader=yaml.FullLoader)
    interface_config = data['sth_interface_config']
    Booked_ports = data['Spirent_Port_Booking']
    Stream_config = data['Spirent_stream_config']
    Spirent_Test_Infra = data['Spirent_Test_Infrastructure']
    return (Booked_ports, interface_config, Stream_config, Spirent_Test_Infra)


def spi2():
    Booked_ports, Interface_config, Stream_config, Spirent_Test_Infra = spirent_items()
    test_sta = sth.test_config (
            log                                              = '1',
            logfile                                          = 'SteamConfig-WithPercentageTraffic_logfile',
            vendorlogfile                                    = 'SteamConfig-WithPercentageTraffic_stcExport',
            vendorlog                                        = '1',
            hltlog                                           = '1',
            hltlogfile                                       = 'SteamConfig-WithPercentageTraffic_hltExport',
            hlt2stcmappingfile                               = 'SteamConfig-WithPercentageTraffic_hlt2StcMapping',
            hlt2stcmapping                                   = '1',
            log_level                                        = '7');
    Number_of_ports = Spirent_Test_Infra['Number_of_ports']
    status = test_sta['status']
    if (status == '0') :
        print("run sth.test_config failed")
        print(test_sta)
    ##############################################################
    #config the parameters for optimization and parsing
    ##############################################################

    test_ctrl_sta = sth.test_control (
            action                                           = 'enable');

    status = test_ctrl_sta['status']
    if (status == '0') :
        print("run sth.test_control failed")
        print(test_ctrl_sta)
    ##############################################################
    #connect to chassis and reserve port list
    ##############################################################
    i = 0
    device = "10.91.113.124"
    port_list = list(Booked_ports.values())
    port_handle = []
    intStatus = sth.connect (
            device                                           = device,
            port_list                                        = port_list,
            break_locks                                      = 1,
            offline                                          = 0 )

    status = intStatus['status']

    if (status == '1') :
        for port in port_list :
            port_handle.append(intStatus['port_handle'][device][port])
            i += 1
    else :
        print("\nFailed to retrieve port handle!\n")
        print(port_handle)

    ##############################################################
    #interface config
    ##############################################################

    Interface_config['port_handle'] = port_handle[0]
    int_ret0 = sth.interface_config (**Interface_config)
    status = int_ret0['status']
    if (status == '0') :
        print("run sth.interface_config failed")
        print(int_ret0)
    Interface_config['port_handle'] = port_handle[1]
    int_ret1 = sth.interface_config (**Interface_config)
    status = int_ret1['status']
    if (status == '0') :
        print("run sth.interface_config failed")
        print(int_ret0)
    ##############################################################
    #stream config
    ##############################################################
    Stream_config['port_handle'] = port_handle[0]
    Stream_config['dest_port_list'] = port_handle[1]
    Stream_config['name'] =  'Stream From 9-3 to 9-4'
    streamblock_ret1 = sth.traffic_config(**Stream_config)
    status = streamblock_ret1['status']
    if (status == '0') :
        print("run sth.traffic_config failed")
        print(streamblock_ret1)
    Stream_config['port_handle'] = port_handle[1]
    Stream_config['dest_port_list'] = port_handle[0]
    Stream_config['name'] =  'Stream From 9-4 to 9-3'
    streamblock_ret1 = sth.traffic_config(**Stream_config)
    status = streamblock_ret1['status']
    if (status == '0') :
        print("run sth.traffic_config failed")
        print(streamblock_ret1)
    #############################################################
    #start traffic
    ##############################################################
    print("Traffic Started")
    traffic_ctrl_ret = sth.traffic_control (
            port_handle                                      = [port_handle[0],port_handle[1]],
            action                                           = 'run',
            duration                                         = '30');

    status = traffic_ctrl_ret['status']
    if (status == '0') :
        print("run sth.traffic_control failed")
        print(traffic_ctrl_ret)
    print("Test Traffic Stopped now adding delay before collecting stats")
    time.sleep(10)
    print("Traffic collection started")
    ##############################################################
    #start to get the traffic results
    ##############################################################
    traffic_results_ret = sth.traffic_stats (
            port_handle                                      = [port_handle[0],port_handle[1]],
            mode                                             = 'all');

    status = traffic_results_ret['status']
    if (status == '0') :
        print("run sth.traffic_stats failed")
        print(traffic_results_ret)


    # ##############################################################
    # #Get required values from Stats
    # ##############################################################
    # Streams_rx_stat = []
    # Streams_tx_stat = []
    # for i in range(1,Number_of_ports+1):
    # 	Port_Index = 'port'+ str(i)
    # 	Stream_Index = 'streamblock' + str(i)
    # 	Streams_rx_stats = traffic_results_ret[Port_Index]['stream'][Stream_Index]['rx']
    # 	Streams_tx_stats = traffic_results_ret[Port_Index]['stream'][Stream_Index]['tx']
    # 	Streams_rx_stat.append(int(Streams_rx_stats['total_pkt_bytes']))
    # 	Streams_tx_stat.append(int(Streams_tx_stats['total_pkt_bytes']))
    #
    # if((Streams_tx_stat[0] == Streams_rx_stat[1]) and (Streams_tx_stat[1] == Streams_rx_stat[0])):
    # 	print("Great Test Case is passed")
    # 	print("streamblock1 TX = ", Streams_tx_stat[0], "streamblock1 RX = ", Streams_rx_stat[0], "streamblock2 TX = ", Streams_tx_stat[1], "streamblock2 RX = ", Streams_rx_stat[1])
    #
    # 	stats = "streamblock1 TX = ", Streams_tx_stat[0], "streamblock1 RX = ", Streams_rx_stat[0], "streamblock2 TX = ", Streams_tx_stat[1], "streamblock2 RX = ", Streams_rx_stat[1]
    # 	status = "Great Test Case is passed\n" + str(stats)
    # 	return status
    #
    # else:
    # 	print("Oops Tst Case Failed")
    # 	print("streamblock1 TX = ", Streams_tx_stat[0], "streamblock1 RX = ", Streams_rx_stat[0], "streamblock2 TX = ", Streams_tx_stat[1], "streamblock2 RX = ", Streams_rx_stat[1])
    #
    # 	stats = "streamblock1 TX = ", Streams_tx_stat[0], "streamblock1 RX = ", Streams_rx_stat[0], "streamblock2 TX = ", Streams_tx_stat[1], "streamblock2 RX = ", Streams_rx_stat[1]
    # 	status = "Oops Tst Case Failed" + str(stats)
    # 	return status
    # 	Stream1_packet_loss_in_msec = ((Streams_tx_stat[0] - Streams_rx_stat[1]) / 1000)
    # 	Stream2_packet_loss_in_msec = ((Streams_tx_stat[1] - Streams_rx_stat[0]) / 1000)

    ##############################################################
    #Get required values from Stats
    ##############################################################

    result = SpirentResult(traffic_results_ret, port_list)
    return result



def spi1():

    ##############################################################
    #config the parameters for the logging
    ##############################################################

    test_sta = sth.test_config (
            log                                              = '1',
            logfile                                          = 'BasciTraffic_logfile',
            vendorlogfile                                    = 'BasciTraffic_stcExport',
            vendorlog                                        = '1',
            hltlog                                           = '1',
            hltlogfile                                       = 'BasciTraffic_hltExport',
            hlt2stcmappingfile                               = 'BasciTraffic_hlt2StcMapping',
            hlt2stcmapping                                   = '1',
            log_level                                        = '7');

    status = test_sta['status']
    if (status == '0') :
        print("run sth.test_config failed")
        print(test_sta)
    else:
        print("***** run sth.test_config successfully")


    ##############################################################
    #config the parameters for optimization and parsing
    ##############################################################

    test_ctrl_sta = sth.test_control (
            action                                           = 'enable');

    status = test_ctrl_sta['status']
    if (status == '0') :
        print("run sth.test_control failed")
        print(test_ctrl_sta)
    else:
        print("***** run sth.test_control successfully")


    ##############################################################
    #connect to chassis and reserve port list
    ##############################################################

    i = 0
    device = "10.91.113.124"
    port_list = ['8/5','8/6']
    port_handle = []
    intStatus = sth.connect (
            device                                           = device,
            port_list                                        = port_list,
            break_locks                                      = 1,
            offline                                          = 0 )

    status = intStatus['status']

    if (status == '1') :
        for port in port_list :
            port_handle.append(intStatus['port_handle'][device][port])
            print("\n reserved ports",port,":", port_handle[i])
            i += 1
    else :
        print("\nFailed to retrieve port handle!\n")
        print(port_handle)


    ##############################################################
    #interface config
    ##############################################################

    int_ret0 = sth.interface_config (
            mode                                             = 'config',
            port_handle                                      = port_handle[0],
            create_host                                      = 'false',
            intf_mode                                        = 'ethernet',
            phy_mode                                         = 'fiber',
            scheduling_mode                                  = 'RATE_BASED',
            port_loadunit                                    = 'FRAMES_PER_SECOND',
            port_load                                        = '1000',
            enable_ping_response                             = '0',
            control_plane_mtu                                = '1500',
            flow_control                                     = 'false',
            speed                                            = 'ether1000',
            data_path_mode                                   = 'normal',
            autonegotiation                                  = '1');

    status = int_ret0['status']
    if (status == '0') :
        print("run sth.interface_config failed")
        print(int_ret0)
    else:
        print("***** run sth.interface_config successfully")

    int_ret1 = sth.interface_config (
            mode                                             = 'config',
            port_handle                                      = port_handle[1],
            create_host                                      = 'false',
            intf_mode                                        = 'ethernet',
            phy_mode                                         = 'fiber',
            scheduling_mode                                  = 'RATE_BASED',
            port_loadunit                                    = 'FRAMES_PER_SECOND',
            port_load                                        = '1000',
            enable_ping_response                             = '0',
            control_plane_mtu                                = '1500',
            flow_control                                     = 'false',
            speed                                            = 'ether1000',
            data_path_mode                                   = 'normal',
            autonegotiation                                  = '1');

    status = int_ret1['status']
    if (status == '0') :
        print("run sth.interface_config failed")
        print(int_ret1)
    else:
        print("***** run sth.interface_config successfully")


    ##############################################################
    #create device and config the protocol on it
    ##############################################################

    #start to create the device: ar1-100
    device_ret0 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[0],
            vlan_user_pri                                    = '7',
            vlan_cfi                                         = '0',
            vlan_id                                          = '100',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.3',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:03',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '172.16.146.0',
            intf_prefix_len                                  = '31',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '172.16.146.1',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:a7:42:16:5f:23',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret0['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret0)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: ar6-100
    device_ret1 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[1],
            vlan_user_pri                                    = '7',
            vlan_cfi                                         = '0',
            vlan_id                                          = '100',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.4',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:04',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '172.17.146.0',
            intf_prefix_len                                  = '31',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '172.17.146.1',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:a7:42:36:12:8f',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret1['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret1)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: ar1-101
    device_ret2 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[0],
            vlan_user_pri                                    = '7',
            vlan_cfi                                         = '0',
            vlan_id                                          = '101',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.5',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:05',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '172.18.146.0',
            intf_prefix_len                                  = '31',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '172.18.146.1',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:a7:42:16:5f:23',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret2['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret2)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: ar1-111 L2
    device_ret3 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[0],
            vlan_user_pri                                    = '5',
            vlan_cfi                                         = '0',
            vlan_id                                          = '111',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.6',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:11:11:00:00:01',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '192.168.111.10',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '192.168.111.2',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:10:94:00:00:07',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret3['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret3)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: ar6-111 L2
    device_ret4 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[1],
            vlan_user_pri                                    = '5',
            vlan_cfi                                         = '0',
            vlan_id                                          = '111',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.7',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:07',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '192.168.111.2',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '192.168.111.10',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:11:11:00:00:01',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret4['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret4)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: ar1-110 L2
    device_ret5 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[0],
            vlan_user_pri                                    = '3',
            vlan_cfi                                         = '0',
            vlan_id                                          = '110',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.6',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:06',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '110.168.110.111',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '110.168.110.112',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:10:94:00:00:07',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret5['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret5)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: ar6-110 L2
    device_ret6 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[1],
            vlan_user_pri                                    = '3',
            vlan_cfi                                         = '0',
            vlan_id                                          = '110',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.7',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:07',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '110.168.110.112',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '110.168.110.111',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:10:94:00:00:06',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret6['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret6)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: ar6-112 L2
    device_ret7 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[1],
            vlan_user_pri                                    = '3',
            vlan_cfi                                         = '0',
            vlan_id                                          = '112',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.7',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:07',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '112.112.12.1',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '112.112.12.2',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:12:94:00:00:06',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret7['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret7)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: ar1-112 L2
    device_ret8 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[0],
            vlan_user_pri                                    = '3',
            vlan_cfi                                         = '0',
            vlan_id                                          = '112',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.6',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:12:94:00:00:06',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '112.112.12.2',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '112.112.12.1',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:10:94:00:00:07',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret8['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret8)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: ar1-113 L2
    device_ret9 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[0],
            vlan_user_pri                                    = '3',
            vlan_cfi                                         = '0',
            vlan_id                                          = '113',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.6',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:12:94:00:00:06',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '13.113.13.2',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '13.113.13.1',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:10:94:00:00:07',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret9['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret9)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: ar6-113 L2
    device_ret10 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii_vlan',
            port_handle                                      = port_handle[1],
            vlan_user_pri                                    = '3',
            vlan_cfi                                         = '0',
            vlan_id                                          = '113',
            vlan_tpid                                        = '33024',
            vlan_id_repeat_count                             = '0',
            vlan_id_step                                     = '0',
            router_id                                        = '192.0.0.7',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:07',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '13.113.13.1',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '13.113.13.2',
            gateway_ip_addr_step                             = '0.0.0.0',
            gateway_mac                                      = '00:12:94:00:00:06',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret10['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret10)
    else:
        print("***** run sth.emulation_device_config successfully")


    ##############################################################
    #create traffic
    ##############################################################

    src_hdl = device_ret0['handle'].split()[0]

    dst_hdl = device_ret1['handle'].split()[0]


    streamblock_ret1 = sth.traffic_config (
            mode                                             = 'create',
            port_handle                                      = port_handle[0],
            emulation_src_handle                             = src_hdl,
            emulation_dst_handle                             = dst_hdl,
            l3_protocol                                      = 'ipv4',
            ip_id                                            = '0',
            ip_ttl                                           = '255',
            ip_hdr_length                                    = '5',
            ip_protocol                                      = '253',
            ip_fragment_offset                               = '0',
            ip_dscp                                          = '10',
            enable_control_plane                             = '0',
            l3_length                                        = '1500',
            name                                             = 'ar1-100_B3',
            fill_type                                        = 'constant',
            fcs_error                                        = '0',
            fill_value                                       = '0',
            frame_size                                       = '1500',
            traffic_state                                    = '1',
            high_speed_result_analysis                       = '1',
            length_mode                                      = 'fixed',
            dest_port_list                                   = ['port2','port1'],
            tx_port_sending_traffic_to_self_en               = 'false',
            disable_signature                                = '0',
            enable_stream_only_gen                           = '1',
            pkts_per_burst                                   = '1',
            inter_stream_gap_unit                            = 'bytes',
            burst_loop_count                                 = '30',
            transmit_mode                                    = 'continuous',
            inter_stream_gap                                 = '12',
            rate_pps                                         = '1000',
            mac_discovery_gw                                 = '172.16.146.1');

    status = streamblock_ret1['status']
    if (status == '0') :
        print("run sth.traffic_config failed")
        print(streamblock_ret1)
    else:
        print("***** run sth.traffic_config successfully")

    src_hdl = device_ret1['handle'].split()[0]

    dst_hdl = device_ret0['handle'].split()[0]


    streamblock_ret2 = sth.traffic_config (
            mode                                             = 'create',
            port_handle                                      = port_handle[1],
            emulation_src_handle                             = src_hdl,
            emulation_dst_handle                             = dst_hdl,
            l3_protocol                                      = 'ipv4',
            ip_id                                            = '0',
            ip_ttl                                           = '255',
            ip_hdr_length                                    = '5',
            ip_protocol                                      = '253',
            ip_fragment_offset                               = '0',
            ip_dscp                                          = '10',
            enable_control_plane                             = '0',
            l3_length                                        = '1500',
            name                                             = 'ar6-100_B3',
            fill_type                                        = 'constant',
            fcs_error                                        = '0',
            fill_value                                       = '0',
            frame_size                                       = '1500',
            traffic_state                                    = '1',
            high_speed_result_analysis                       = '1',
            length_mode                                      = 'fixed',
            dest_port_list                                   = ['port2','port1'],
            tx_port_sending_traffic_to_self_en               = 'false',
            disable_signature                                = '0',
            enable_stream_only_gen                           = '1',
            pkts_per_burst                                   = '1',
            inter_stream_gap_unit                            = 'bytes',
            burst_loop_count                                 = '30',
            transmit_mode                                    = 'continuous',
            inter_stream_gap                                 = '12',
            rate_pps                                         = '1000',
            mac_discovery_gw                                 = '172.17.146.1');

    status = streamblock_ret2['status']
    if (status == '0') :
        print("run sth.traffic_config failed")
        print(streamblock_ret2)
    else:
        print("***** run sth.traffic_config successfully")

    #config part is finished

    ##############################################################
    #start devices
    ##############################################################


    ##############################################################
    #start traffic
    ##############################################################

    traffic_ctrl_ret = sth.traffic_control (
            port_handle                                      = [port_handle[0],port_handle[1]],
            action                                           = 'run',
            duration                                         = '30');



    status = traffic_ctrl_ret['status']
    if (status == '0') :
        print("run sth.traffic_control failed")
        print(traffic_ctrl_ret)
    else:
        print("***** run sth.traffic_control successfully")


    ##############################################################
    #start to get the device results
    ##############################################################

    time.sleep(30)

    ##############################################################
    #start to get the traffic results
    ##############################################################

    traffic_results_ret = sth.traffic_stats (
            port_handle                                      = [port_handle[0],port_handle[1]],
            mode                                             = 'all');

    status = traffic_results_ret['status']
    if (status == '0') :
        print("run sth.traffic_stats failed")
        print(traffic_results_ret)


    else:
        print("***** run sth.traffic_stats successfully, and results is:")
        print(traffic_results_ret)



    ##############################################################
    #clean up the session, release the ports reserved and cleanup the dbfile
    ##############################################################

    cleanup_sta = sth.cleanup_session (
            port_handle                                      = [port_handle[0],port_handle[1]],
            clean_dbfile                                     = '1');

    status = cleanup_sta['status']
    if (status == '0') :
        print("run sth.cleanup_session failed")
        print(cleanup_sta)
    else:
        print("***** run sth.cleanup_session successfully")


    print("**************Finish***************")

    result = SpirentResult(traffic_results_ret, port_list)
    return result



def SpirentResult(traffic_results_ret, port_list):

    ##############################################################
    #Get required values from Stats
    ##############################################################

    traffic_result = str(traffic_results_ret)

    #regex to get rx, tx and streams from traffic_results_ret
    RX = '(streamblock\d+)\S+\s+\S+(rx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'
    TX = '(streamblock\d+).*?(tx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'
    StreamBlock = 'streamblock\d+'


    print('Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list)))
    PortStatus = 'Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list))

    StreamBlock = re.findall(StreamBlock, traffic_result)
    print('Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock)))
    StreamStatus = 'Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock))

    rx_stats = re.findall(RX, traffic_result)
    tx_stats = re.findall(TX, traffic_result)

    print('rx_stats= ' + str(rx_stats))
    print('tx_stats= ' + str(tx_stats))

    stats = 'rx_stats= ' + str(rx_stats) + '\ntx_stats= ' + str(tx_stats)

    StreamResult = []

    for i in range(0,len(StreamBlock)):
        if rx_stats[i][2] == tx_stats[i][2]:
            print(str(rx_stats[i][0] + ' = pass'))
            StreamResult.append('pass')

        else:
            print(str(rx_stats[i][0] + ' = fail'))
            StreamResult.append('fail')

    print(str(StreamResult))

    OverallStatus = '\n' + PortStatus + '\n' + StreamStatus + '\n' + stats + '\n' + str(StreamResult)
    print(OverallStatus)

    return OverallStatus


