#!/usr/bin/env python
import time
from jinja2 import Template
import templates as t1
import os
import jinja2
import textfsm

file_path = os.path.dirname(os.path.realpath(__file__))

def show_commands(net_connect, **kwargs):

    template = Template(kwargs['template_name'])
    tempalte_data = kwargs['template_data']
    #print(tempalte_data)
    show_cmd = template.render(component=kwargs['template_data'])
    print(show_cmd)
    # output1 = net_connect.send_command_expect(show_cmd, strip_prompt=False, strip_command=False)
    prompt = net_connect.find_prompt()
    output1 = net_connect.send_command_expect(show_cmd)
    # display the output
    output2 = prompt + show_cmd + output1
    print(output2)
    output2_list = output2.split('\n')
    return output2_list
    # template_fsm = open(file_path + "/TEXTFSM/" + kwargs['textfsm_template'])
    # out_table = textfsm.TextFSM(template_fsm)
    # # print(out_table)
    # # fsm_results = out_table.ParseText(output1.encode("utf-8"))
    # fsm_results = out_table.ParseText(output1)
    # fsm_results_str = ""
    # fsm_results_str+= "     ".join(out_table.header) + "\n"     # 8 spaces
    # for row in fsm_results:
    #     fsm_results_str += "        ".join(row) + "\n"          # 8 spaces
    # return fsm_results_str



def configure_commands(net_connect, **kwargs):

    template = Template(kwargs['template_name'])
    tempalte_data = kwargs['template_data']
    cmds = template.render(component = kwargs['template_data'])
    config_commands = [cmds]
    #print(config_commands)
    output1 = net_connect.send_config_set(config_commands, cmd_verify=False)
    print(output1)
    output2 = net_connect.commit()
    print(output2)
    output3 = net_connect.exit_config_mode()
    print(output3)
    return output2

def configure_accedian_commands(net_connect, **kwargs):

    template = Template(kwargs['template_name'])
    tempalte_data = kwargs['template_data']
    cmds = template.render(component = kwargs['template_data'])
    config_commands = [cmds]
    #print(config_commands)
    output1 = net_connect.send_config_set(config_commands, cmd_verify=False)
    # print(output1)
    # output2 = net_connect.commit()
    # print(output2)
    # output3 = net_connect.exit_config_mode()
    # print(output3)
    return output1


def configure_cpe_commands(net_connect, **kwargs):

    template = Template(kwargs['template_name'])
    tempalte_data = kwargs['template_data']
    cmds = template.render(component = kwargs['template_data'])
    config_commands = [cmds]
    #print(config_commands)
    output1 = net_connect.send_config_set(config_commands, cmd_verify=False)
    # print (output1)
    # output2 = net_connect.commit()
    # print (output2)
    output3 = net_connect.exit_config_mode()
    print(output3)
    return output1

