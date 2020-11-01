#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify an new MAC, use --help for more info.")
    elif not checking_new_mac_format(options):
        parser.error("[-] MAC address entered incorrectly. Please specify an new MAC, use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}.")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = str(subprocess.check_output(["ifconfig", interface]))
    pattern = "\w\w:\w\w:\w\w:\w\w:\w\w:\w\w"
    mac_address_search_result = re.search(pattern, ifconfig_result)
    return mac_address_search_result.group(0) if mac_address_search_result else print("[-] Could not read MAC address.")


def checking_new_mac_format(options):
    pattern = "[0-9,a-f][0-9,a-f]:[0-9,a-f][0-9,a-f]:[0-9,a-f][0-9,a-f]:[0-9,a-f][0-9,a-f]:[0-9,a-f][0-9,a-f]:[0-9,a-f][0-9,a-f]"
    return True if re.match(pattern, options.new_mac) else False


def get_response_if_change_mac(options, old_mac):
    current_mac = get_current_mac(options.interface)
    if current_mac == options.new_mac and current_mac != old_mac:
        print(f"[+] MAC address was successfully changed from {old_mac} to {current_mac}")
    else:
        print("[-] MAC address did not get changed.")


if __name__ == '__main__':
    options = get_arguments()
    old_mac_address = get_current_mac(options.interface)
    if old_mac_address:
        change_mac(options.interface, options.new_mac)
        get_response_if_change_mac(options, old_mac_address)
