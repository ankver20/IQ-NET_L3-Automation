*** Settings ***
Documentation     A test suite with tests for P2P conenctivity.
...               Topology:-
...               ____________________________
...
...
...               Testplan Goals:-
...               1. CHECK P2P EPL service.
Suite Setup       Setup Actions
Suite Teardown    Teardown Actions
Metadata          Version    1.0\nMore Info For more information about Robot Framework see http://robotframework.org\nAuthor Sathishkumar murugesan\nDate 12 Dec 2017\nExecuted At HOST\nTest Framework Robot Framework Python
Variables         ${CURDIR}/../Variables/P2P/Variables.py
Variables         ${CURDIR}/../libraries/templates.py
Library           Collections
Library           String
Library           OperatingSystem
Library           ${CURDIR}/../libraries/Commands.py
Library           ${CURDIR}/../libraries/BasicTraffic.py
Resource          ../libraries/Resource.robot
Resource          ../libraries/Resource.robot

*** Test Cases ***

L3_Test
    [Tags]    L3_Test

    #show version
    ${template_data}=    Create Dictionary    blank='blank'
    ${show_result}=    SHOW COMMAND    ${CPE_R1_net_connect}    Sh_Ver    ${template_data}
    #log to console    ${show_result}
    ${ver}=    Get Matches    ${show_result}    regexp=\\S+\\d+\\.\\d+\\.\\d+
    log to console    ${ver}
    ${template_data}=    Create Dictionary    blank='blank'
    ${show_result}=    SHOW COMMAND    ${CPE_R2_net_connect}    Sh_Ver    ${template_data}
    #log to console    ${show_result}
    ${ver}=    Get Matches    ${show_result}    regexp=\\S+\\d+\\.\\d+\\.\\d+
    log to console  ${ver}

    log to console  testdone


EPL_PTP_NCS-NCS_SubIntf
    [Tags]    EPL_PTP_NCS-NCS_SubIntf

    #configure Policy map egr on R1 & R2
    CONFIGURE POLICY-MAP-EGR    ${R1_net_connect}    ${Pol_map_egr_template}    ${Pol_map_egr_data}
    CONFIGURE POLICY-MAP-EGR    ${R2_net_connect}    ${Pol_map_egr_template}    ${Pol_map_egr_data}
    #configure service Policy map ingress on R1 & R2
    CONFIGURE SERVICE-POLICY-MAP    ${R1_net_connect}    ${Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
    CONFIGURE SERVICE-POLICY-MAP    ${R2_net_connect}    ${Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
    #configure interface on R1 & R2
    CONFIGURE INTERFACE    ${R1_net_connect}    ${PORT_R1_10}    ${NCS_int_template}    ${R1_interface_data}
    CONFIGURE INTERFACE    ${R2_net_connect}    ${PORT_R2_10}    ${NCS_int_template}    ${R2_interface_data}
    #configure sub-interface on R1 & R2
    CONFIGURE SUB-INTERFACE    ${R1_net_connect}    ${PORT_R1_10}.${sub_interface_4095}    ${NCS_sub_int_PFD_template}    ${R1_sub_interface_data}
    CONFIGURE SUB-INTERFACE    ${R2_net_connect}    ${PORT_R2_10}.${sub_interface_4095}    ${NCS_sub_int_PFD_template}    ${R2_sub_interface_data}
    #configure service Policy map on sub-intf in ingress
    CONFIGURE SERVICE-POLICY-MAP-INTF    ${R1_net_connect}    ${PORT_R1_10}.${sub_interface_4095}    ${Ser_Pol_map_intf_template}    ${Ser_Pol_map_1G_data}
    CONFIGURE SERVICE-POLICY-MAP-INTF    ${R2_net_connect}    ${PORT_R2_10}.${sub_interface_4095}    ${Ser_Pol_map_intf_template}    ${Ser_Pol_map_1G_data}

    #start spirent traffic
    ${spirent_traffic}=    spi1
    log to console  ${spirent_traffic}
    run keyword and continue on failure    should not contain    ${spirent_traffic}    fail
    SLEEP  20
    ${spirent_traffic}=    spi2
    log to console  ${spirent_traffic}
    run keyword and continue on failure    should not contain    ${spirent_traffic}    fail
    SLEEP  10




#    #verify status of main intf status R1
#    ${template_data}=    Create Dictionary    interface=${PORT_R1_10}
#    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_interface_template    ${template_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${intf_status}
#    #verify status of sub intf status R1
#    ${template_data}=    Create Dictionary    interface=${PORT_R1_10}.${sub_interface_4095}
#    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_interface_template    ${template_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${intf_status}
#    #verify status of main intf status R2
#    ${template_data}=    Create Dictionary    interface=${PORT_R2_10}
#    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_interface_template    ${template_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${intf_status}
#    #verify status of sub intf status R2
#    ${template_data}=    Create Dictionary    interface=${PORT_R2_10}.${sub_interface_4095}
#    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_interface_template    ${template_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${intf_status}
#    #configure EPL & L2VPN on R1 & R2
#    CONFIGURE EVPN    ${R1_net_connect}    ${EVPN_template}    ${R1_evpn_data}
#    CONFIGURE L2VPN    ${R1_net_connect}    ${PORT_R1_10}.${sub_interface_4095}    ${L2VPN_template}    ${R1_l2vpn_data}
#    CONFIGURE EVPN    ${R2_net_connect}    ${EVPN_template}    ${R2_evpn_data}
#    CONFIGURE L2VPN    ${R2_net_connect}    ${PORT_R2_10}.${sub_interface_4095}    ${L2VPN_template}    ${R2_l2vpn_data}
#    #verify L2VPN status R1
#    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_L2VPN_template    ${R1_l2vpn_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${L2VPN_status}
#    #verify L2VPN status R2
#    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_L2VPN_template    ${R2_l2vpn_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${L2VPN_status}
#    #configure CFM on R1 & R2
#    CONFIGURE CFM    ${R1_net_connect}    ${CFM_template}    ${R1_cfm_data}
#    CONFIGURE CFM    ${R2_net_connect}    ${CFM_template}    ${R2_cfm_data}
#    CONFIGURE CFM-INTF    ${R1_net_connect}    ${PORT_R1_10}.${sub_interface_4095}    ${CFM_intf_template}    ${R1_cfm_data}
#    CONFIGURE CFM-INTF    ${R2_net_connect}    ${PORT_R2_10}.${sub_interface_4095}    ${CFM_intf_template}    ${R2_cfm_data}
#    #verify the CFM status on R1 & R2
#    #wait 80 sec for CFM to exchnage msgs & come up
#    Sleep   80
#    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_eth_cfm_template    ${R1_cfm_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${local_mep_info}
#    run keyword and continue on failure    should contain    ${show_result}    ${peer_mep_info}
#    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_eth_cfm_template    ${R2_cfm_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${local_mep_info}
#    run keyword and continue on failure    should contain    ${show_result}    ${peer_mep_info}
#    #verify L2VPN status R1 !!!AGAIN!!!
#    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_L2VPN_template    ${R1_l2vpn_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${L2VPN_status}
#    #verify L2VPN status R2 !!!AGAIN!!!
#    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_L2VPN_template    ${R2_l2vpn_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${L2VPN_status}
#    #verify the CFM status on R1 & R2 again at the interval of 4 sec !!! to check CFM is not flapping!!!
#    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_eth_cfm_template    ${R1_cfm_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${local_mep_info}
#    run keyword and continue on failure    should contain    ${show_result}    ${peer_mep_info}
#    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_eth_cfm_template    ${R2_cfm_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${local_mep_info}
#    run keyword and continue on failure    should contain    ${show_result}    ${peer_mep_info}
#    Sleep   4
#    #check the CFM status again !!! to check flapping ater 4 sec !!!
#    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_eth_cfm_template    ${R1_cfm_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${local_mep_info}
#    run keyword and continue on failure    should contain    ${show_result}    ${peer_mep_info}
#    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_eth_cfm_template    ${R2_cfm_data}
#    log to console    ${show_result}
#    run keyword and continue on failure    should contain    ${show_result}    ${local_mep_info}
#    run keyword and continue on failure    should contain    ${show_result}    ${peer_mep_info}
#    #uncofigure all the paremeters - interface, sub-interface, CFM, evpn & l2vpn,
    UNCONFIGURE SUB-INTF    ${R1_net_connect}    ${PORT_R1_10}.${sub_interface_4095}    ${Del_NCS_sub_int_template}    ${R1_sub_interface_data}
    UNCONFIGURE SUB-INTF    ${R2_net_connect}    ${PORT_R2_10}.${sub_interface_4095}    ${Del_NCS_sub_int_template}    ${R2_sub_interface_data}
    UNCONFIGURE INTF    ${R1_net_connect}    ${PORT_R1_10}    ${Del_NCS_int_template}    ${R1_interface_data}
    UNCONFIGURE INTF    ${R2_net_connect}    ${PORT_R2_10}    ${Del_NCS_int_template}    ${R2_interface_data}
#    UNCONFIGURE SERVICE-POLICY-MAP  ${R1_net_connect}    ${Del_Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
#    UNCONFIGURE SERVICE-POLICY-MAP  ${R2_net_connect}    ${Del_Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
#    UNCONFIGURE CFM    ${R1_net_connect}    ${Del_CFM_template}    ${R1_cfm_data}
#    UNCONFIGURE CFM    ${R2_net_connect}    ${Del_CFM_template}    ${R2_cfm_data}
#    UNCONFIGURE EVPN    ${R1_net_connect}    ${Del_EVPN_template}    ${R1_evpn_data}
#    UNCONFIGURE EVPN    ${R2_net_connect}    ${Del_EVPN_template}    ${R2_evpn_data}
#    UNCONFIGURE L2VPN    ${R1_net_connect}    ${Del_L2VPN_template}    ${R1_l2vpn_data}
#    UNCONFIGURE L2VPN    ${R2_net_connect}    ${Del_L2VPN_template}    ${R2_l2vpn_data}
    log to console    END OF TEST CASE


EPL_PTP_NCS-NCS_MainIntf
    [Tags]    EPL_PTP_NCS-NCS_MainIntf
    #configure Policy map egr on R1 & R2
    CONFIGURE POLICY-MAP-EGR    ${R1_net_connect}    ${Pol_map_egr_template}    ${Pol_map_egr_data}
    CONFIGURE POLICY-MAP-EGR    ${R2_net_connect}    ${Pol_map_egr_template}    ${Pol_map_egr_data}
    #configure service Policy map ingress on R1 & R2
    CONFIGURE SERVICE-POLICY-MAP    ${R1_net_connect}    ${Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
    CONFIGURE SERVICE-POLICY-MAP    ${R2_net_connect}    ${Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
    #configure main interface on R1 & R2
    CONFIGURE INTERFACE    ${R1_net_connect}    ${PORT_R1_10}    ${NCS_main_int_template}    ${R1_interface_data}
    CONFIGURE INTERFACE    ${R2_net_connect}    ${PORT_R2_10}    ${NCS_main_int_template}    ${R2_interface_data}
    #configure service Policy map on main-intf in ingress
    CONFIGURE SERVICE-POLICY-MAP-INTF    ${R1_net_connect}    ${PORT_R1_10}    ${Ser_Pol_map_main_intf_template}    ${Ser_Pol_map_1G_data}
    CONFIGURE SERVICE-POLICY-MAP-INTF    ${R2_net_connect}    ${PORT_R2_10}    ${Ser_Pol_map_main_intf_template}    ${Ser_Pol_map_1G_data}

    #verify status of main intf status R1
    ${template_data}=    Create Dictionary    interface=${PORT_R1_10}
    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_interface_template    ${template_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${intf_status}
    #verify status of main intf status R2
    ${template_data}=    Create Dictionary    interface=${PORT_R2_10}
    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_interface_template    ${template_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${intf_status}

    #configure EPL & L2VPN on R1 & R2
    CONFIGURE EVPN    ${R1_net_connect}    ${EVPN_template}    ${R1_evpn_data}
    CONFIGURE L2VPN    ${R1_net_connect}    ${PORT_R1_10}    ${L2VPN_template}    ${R1_l2vpn_data}
    CONFIGURE EVPN    ${R2_net_connect}    ${EVPN_template}    ${R2_evpn_data}
    CONFIGURE L2VPN    ${R2_net_connect}    ${PORT_R2_10}    ${L2VPN_template}    ${R2_l2vpn_data}
    #verify L2VPN status R1
    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_L2VPN_template    ${R1_l2vpn_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${L2VPN_status}
    #verify L2VPN status R2
    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_L2VPN_template    ${R2_l2vpn_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${L2VPN_status}

    #configure CFM on R1 & R2
    CONFIGURE CFM    ${R1_net_connect}    ${CFM_template}    ${R1_cfm_data}
    CONFIGURE CFM    ${R2_net_connect}    ${CFM_template}    ${R2_cfm_data}
    CONFIGURE CFM-INTF    ${R1_net_connect}    ${PORT_R1_10}    ${CFM_intf_template}    ${R1_cfm_data}
    CONFIGURE CFM-INTF    ${R2_net_connect}    ${PORT_R2_10}    ${CFM_intf_template}    ${R2_cfm_data}
    #verify the CFM status on R1 & R2
    #wait 80 sec for CFM to exchnage msgs & come up
    Sleep   80
    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_eth_cfm_template    ${R1_cfm_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${local_mep_info}
    run keyword and continue on failure    should contain    ${show_result}    ${peer_mep_info}
    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_eth_cfm_template    ${R2_cfm_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${local_mep_info}
    run keyword and continue on failure    should contain    ${show_result}    ${peer_mep_info}

    #uncofigure all the paremeters - interface, sub-interface, CFM, evpn & l2vpn,
    UNCONFIGURE INTF    ${R1_net_connect}    ${PORT_R1_10}    ${Del_NCS_int_template}    ${R1_interface_data}
    UNCONFIGURE INTF    ${R2_net_connect}    ${PORT_R2_10}    ${Del_NCS_int_template}    ${R2_interface_data}
    UNCONFIGURE SERVICE-POLICY-MAP  ${R1_net_connect}    ${Del_Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
    UNCONFIGURE SERVICE-POLICY-MAP  ${R2_net_connect}    ${Del_Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
    UNCONFIGURE CFM    ${R1_net_connect}    ${Del_CFM_template}    ${R1_cfm_data}
    UNCONFIGURE CFM    ${R2_net_connect}    ${Del_CFM_template}    ${R2_cfm_data}
    UNCONFIGURE EVPN    ${R1_net_connect}    ${Del_EVPN_template}    ${R1_evpn_data}
    UNCONFIGURE EVPN    ${R2_net_connect}    ${Del_EVPN_template}    ${R2_evpn_data}
    UNCONFIGURE L2VPN    ${R1_net_connect}    ${Del_L2VPN_template}    ${R1_l2vpn_data}
    UNCONFIGURE L2VPN    ${R2_net_connect}    ${Del_L2VPN_template}    ${R2_l2vpn_data}
    log to console    END OF TEST CASE

EPL_PTP_NCS-NCS_MainIntf_LLF
    [Tags]    EPL_PTP_NCS-NCS_MainIntf_LLF
    #configure Policy map egr on R1 & R2
    CONFIGURE POLICY-MAP-EGR    ${R1_net_connect}    ${Pol_map_egr_template}    ${Pol_map_egr_data}
    CONFIGURE POLICY-MAP-EGR    ${R2_net_connect}    ${Pol_map_egr_template}    ${Pol_map_egr_data}
    #configure service Policy map ingress on R1 & R2
    CONFIGURE SERVICE-POLICY-MAP    ${R1_net_connect}    ${Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
    CONFIGURE SERVICE-POLICY-MAP    ${R2_net_connect}    ${Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
    #configure main interface on R1 & R2
    CONFIGURE INTERFACE    ${R1_net_connect}    ${PORT_R1_10}    ${NCS_main_int_template}    ${R1_interface_data}
    CONFIGURE INTERFACE    ${R2_net_connect}    ${PORT_R2_10}    ${NCS_main_int_template}    ${R2_interface_data}
    #configure service Policy map on main-intf in ingress
    CONFIGURE SERVICE-POLICY-MAP-INTF    ${R1_net_connect}    ${PORT_R1_10}    ${Ser_Pol_map_main_intf_template}    ${Ser_Pol_map_1G_data}
    CONFIGURE SERVICE-POLICY-MAP-INTF    ${R2_net_connect}    ${PORT_R2_10}    ${Ser_Pol_map_main_intf_template}    ${Ser_Pol_map_1G_data}

    #verify status of main intf status R1
    ${template_data}=    Create Dictionary    interface=${PORT_R1_10}
    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_interface_template    ${template_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${intf_status}
    #verify status of main intf status R2
    ${template_data}=    Create Dictionary    interface=${PORT_R2_10}
    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_interface_template    ${template_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${intf_status}

    #configure EPL & L2VPN on R1 & R2
    CONFIGURE EVPN    ${R1_net_connect}    ${EVPN_template}    ${R1_evpn_data}
    CONFIGURE L2VPN    ${R1_net_connect}    ${PORT_R1_10}    ${L2VPN_template}    ${R1_l2vpn_data}
    CONFIGURE EVPN    ${R2_net_connect}    ${EVPN_template}    ${R2_evpn_data}
    CONFIGURE L2VPN    ${R2_net_connect}    ${PORT_R2_10}    ${L2VPN_template}    ${R2_l2vpn_data}
    #verify L2VPN status R1
    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_L2VPN_template    ${R1_l2vpn_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${L2VPN_status}
    #verify L2VPN status R2
    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_L2VPN_template    ${R2_l2vpn_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${L2VPN_status}

    #configure CFM on R1 & R2
    CONFIGURE CFM    ${R1_net_connect}    ${CFM_template}    ${R1_cfm_data}
    CONFIGURE CFM    ${R2_net_connect}    ${CFM_template}    ${R2_cfm_data}
    CONFIGURE CFM-INTF    ${R1_net_connect}    ${PORT_R1_10}    ${CFM_intf_template}    ${R1_cfm_data}
    CONFIGURE CFM-INTF    ${R2_net_connect}    ${PORT_R2_10}    ${CFM_intf_template}    ${R2_cfm_data}
    #verify the CFM status on R1 & R2
    #wait 80 sec for CFM to exchnage msgs & come up
    Sleep   80
    ${show_result}=    SHOW COMMAND    ${R1_net_connect}    show_eth_cfm_template    ${R1_cfm_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${local_mep_info}
    run keyword and continue on failure    should contain    ${show_result}    ${peer_mep_info}
    ${show_result}=    SHOW COMMAND    ${R2_net_connect}    show_eth_cfm_template    ${R2_cfm_data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${local_mep_info}
    run keyword and continue on failure    should contain    ${show_result}    ${peer_mep_info}

    #configure LLF
    CONFIGURE LLF    ${R1_net_connect}    ${PORT_R1_10}    ${LLF_template}    ${LLF_data}
    CONFIGURE LLF    ${R2_net_connect}    ${PORT_R2_10}    ${LLF_template}    ${LLF_data}
    #LLF verification needs to be added

    #uncofigure all the paremeters - interface, sub-interface, CFM, evpn & l2vpn,
    UNCONFIGURE INTF    ${R1_net_connect}    ${PORT_R1_10}    ${Del_NCS_int_template}    ${R1_interface_data}
    UNCONFIGURE INTF    ${R2_net_connect}    ${PORT_R2_10}    ${Del_NCS_int_template}    ${R2_interface_data}
    UNCONFIGURE SERVICE-POLICY-MAP  ${R1_net_connect}    ${Del_Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
    UNCONFIGURE SERVICE-POLICY-MAP  ${R2_net_connect}    ${Del_Ser_Pol_map_template}    ${Ser_Pol_map_1G_data}
    UNCONFIGURE CFM    ${R1_net_connect}    ${Del_CFM_template}    ${R1_cfm_data}
    UNCONFIGURE CFM    ${R2_net_connect}    ${Del_CFM_template}    ${R2_cfm_data}
    UNCONFIGURE EVPN    ${R1_net_connect}    ${Del_EVPN_template}    ${R1_evpn_data}
    UNCONFIGURE EVPN    ${R2_net_connect}    ${Del_EVPN_template}    ${R2_evpn_data}
    UNCONFIGURE L2VPN    ${R1_net_connect}    ${Del_L2VPN_template}    ${R1_l2vpn_data}
    UNCONFIGURE L2VPN    ${R2_net_connect}    ${Del_L2VPN_template}    ${R2_l2vpn_data}

    log to console    END OF TEST CASE

test
    [Tags]    test
    log to console  STARTING TEST
    #Enable Port
    ENABLE ACCEDIAN-PORT    ${R3_net_connect}    ${PORT_R3_1}    ${port_enable_template}    ${R3_port_data}
    #verify status of port on R3
    ${template_data}=    Create Dictionary    port_name=${PORT_R3_1}
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    port_show_template    ${template_data}
    #log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${accedian_port_status}

    #Configure Regulator on Accedian
    CONFIGURE ACCEDAIN-REGULATOR    ${R3_net_connect}    ${bw_regulator_template}    ${UNI_1G_regulator_data}
    #verify BW Regulator is created
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    bw_regulator_show_template    ${UNI_1G_regulator_data}
    log to console    ${show_result}

    #Configure L2 Filter on Accedian
    CONFIGURE ACCEDAIN-FILTER    ${R3_net_connect}    ${filter_template}    ${Filter_1051_data}
    #verify L2 filter is created
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    filter_show_template    ${Filter_1051_data}
    log to console    ${show_result}

    #Configure VID Set on Accedian
    CONFIGURE VID-SET    ${R3_net_connect}    ${vid_set_template}    ${vid_set_123_data}
    #verify VID Set is created
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    vid_set_show_template    ${vid_set_123_data}
    log to console    ${show_result}

    #Configure Traffic-Policy
    CONFIGURE TRAFFIC-POLICY    ${R3_net_connect}    ${policy_template}    ${Traffic_1_Policy_data}

    #Configure CFM MEG & MEP on Accedian
    CONFIGURE CFM-MEG-ACCEDIAN    ${R3_net_connect}    ${CFM_MEG_accedian_template}    ${CFM_MEG_ANK_Data}
    CONFIGURE CFM-MEP-ACCEDIAN    ${R3_net_connect}    ${CFM_MEP_accedian_template}    ${CFM_MEP_ANK_Data}
    #verify CFM MEP status
    sleep  30
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    cfm_show_mep_database_template    ${CFM_MEP_ANK_Data}
    log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${mep_status}

    #Disable Traffic-policy on Accedian
    UNCONFIGURE TRAFFIC-POLICY    ${R3_net_connect}    ${Del_policy_template}    ${Traffic_1_Policy_data}
    #Un-configure VID Set on Accedian
    UNCONFIGURE VID-SET    ${R3_net_connect}    ${Del_vid_set_template}    ${vid_set_123_data}
    #Un-configure L2 Filter on Accedian
    UNCONFIGURE ACCEDAIN-FILTER    ${R3_net_connect}    ${Del_filter_template}    ${Filter_1051_data}
    #Un-configure Regulator
    UNCONFIGURE ACCEDAIN-REGULATOR    ${R3_net_connect}    ${Del_bw_regulator_template}    ${UNI_1G_regulator_data}
    #Un-configure CFM MEG & MEP
    UNCONFIGURE CFM-MEP-ACCEDIAN    ${R3_net_connect}    ${Del_CFM_MEP_accedian_template}    ${CFM_MEP_ANK_Data}
    UNCONFIGURE CFM-MEG-ACCEDIAN    ${R3_net_connect}    ${Del_CFM_MEG_accedian_template}    ${CFM_MEG_ANK_Data}

EPL_PTP_NCS-LTS
    [Tags]    EPL_PTP_NCS-LTS
    log to console  STARTING EPL_PTP_NCS-LTS
    #Enable R3 Uni Port 1 & 5
    ENABLE ACCEDIAN-PORT    ${R3_net_connect}    ${PORT_R3_1}    ${port_enable_template}    ${R3_port1_data}
    ENABLE ACCEDIAN-PORT    ${R3_net_connect}    ${PORT_R3_1}    ${port_enable_template}    ${R3_port1_data}
    #verify status of port 1 & 5 on R3
    ${template_data}=    Create Dictionary    port_name=${PORT_R3_1}
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    port_show_template    ${template_data}
    run keyword and continue on failure    should contain    ${show_result}    ${accedian_port_status}
    ${template_data}=    Create Dictionary    port_name=${PORT_R3_5}
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    port_show_template    ${template_data}
    run keyword and continue on failure    should contain    ${show_result}    ${accedian_port_status}

    #Configure Regulator on R3 - 1G UNI and 10G NNI
    CONFIGURE ACCEDAIN-REGULATOR    ${R3_net_connect}    ${bw_regulator_template}    ${R3_1G_UNI_regulator_data}
    #verify BW Regulator is created
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    bw_regulator_show_template    ${R3_1G_UNI_regulator_data}
    #log to console    ${show_result}
    CONFIGURE ACCEDAIN-REGULATOR    ${R3_net_connect}    ${bw_regulator_template}    ${R3_1G_NNI_regulator_data}
    #verify BW Regulator is created
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    bw_regulator_show_template    ${R3_1G_NNI_regulator_data}
    #log to console    ${show_result}

    #Configure L2 filter on R3 for Port 5
    CONFIGURE ACCEDAIN-FILTER    ${R3_net_connect}    ${filter_template}    ${R3_Filter_Traffic5_data}
    #verify L2 filter is created
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    filter_show_template    ${R3_Filter_Traffic5_data}
    #log to console    ${show_result}

    #Configure Traffic Policy on R3 - Traffic 1 & 5
    CONFIGURE TRAFFIC-POLICY    ${R3_net_connect}    ${policy_template}    ${R3_Traffic1_Policy_data}
    CONFIGURE TRAFFIC-POLICY    ${R3_net_connect}    ${policy_template}    ${R3_Traffic5_Policy_data}

    #Configure CFM MEG & MEP on R3
    CONFIGURE CFM-MEG-ACCEDIAN    ${R3_net_connect}    ${CFM_MEG_accedian_template}    ${R3_CFM_MEG_Traffic5_Data}
    CONFIGURE CFM-MEP-ACCEDIAN    ${R3_net_connect}    ${CFM_MEP_accedian_template}    ${R3_CFM_MEP_Traffic5_Data}
    #Verify the CFM MEP Status after sleep time of 40 sec
    sleep  120
    ${show_result}=    SHOW COMMAND    ${R3_net_connect}    cfm_show_mep_database_template    ${R3_CFM_MEP_Traffic5_Data}
    #log to console    ${show_result}
    run keyword and continue on failure    should contain    ${show_result}    ${mep_status}

    #Unconfigure Traffic-policy on 1 & 5 on R3
    UNCONFIGURE TRAFFIC-POLICY    ${R3_net_connect}    ${Del_policy_template}    ${R3_Traffic1_Policy_data}
    UNCONFIGURE TRAFFIC-POLICY    ${R3_net_connect}    ${Del_policy_template}    ${R3_Traffic5_Policy_data}
    #Unconfigure Filter on R3
    UNCONFIGURE ACCEDAIN-FILTER    ${R3_net_connect}    ${Del_filter_template}    ${R3_Filter_Traffic5_data}
    #Unconfigure Regulator on R3
    UNCONFIGURE ACCEDAIN-REGULATOR    ${R3_net_connect}    ${Del_bw_regulator_template}    ${R3_1G_UNI_regulator_data}
    UNCONFIGURE ACCEDAIN-REGULATOR    ${R3_net_connect}    ${Del_bw_regulator_template}    ${R3_1G_NNI_regulator_data}
    #Unconfigure CFM MEG & MEP on R3
    UNCONFIGURE CFM-MEP-ACCEDIAN    ${R3_net_connect}    ${Del_CFM_MEP_accedian_template}    ${R3_CFM_MEP_Traffic5_Data}
    UNCONFIGURE CFM-MEG-ACCEDIAN    ${R3_net_connect}    ${Del_CFM_MEG_accedian_template}    ${R3_CFM_MEG_Traffic5_Data}

*** Keywords ***
