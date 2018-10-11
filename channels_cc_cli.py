#!/usr/bin/env python3

import os
import signal
import readline
import sys
import subprocess
from tui_modules import tx_broadcaster, channel_open, channel_payment,\
channel_close, channel_refund, channels_info

header = "\
 _____  _                                 _       _____  _____ \n\
/  __ \| |                               | |     /  __ \/  __ \\\n\
| /  \/| |__    __ _  _ __   _ __    ___ | | ___ | /  \/| /  \/\n\
| |    | '_ \  / _` || '_ \ | '_ \  / _ \| |/ __|| |    | |    \n\
| \__/\| | | || (_| || | | || | | ||  __/| |\__ \| \__/\| \__/\\\n\
 \____/|_| |_| \__,_||_| |_||_| |_| \___||_||___/ \____/ \____/\n"

colors = {
        'blue': '\033[94m',
        'pink': '\033[95m',
        'green': '\033[92m',
        }

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'

def channel_open_tui():
    acname = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    destpubkey = input("Input channel destination pubkey: ")
    paymentsnumber = input("Input maximum number of payments in this channel: ")
    paymentdenomination = input("Input payment denomination (in sathoshis): ")
    file = open("channels_list", "a")

    try:
        channel_open_hex = channel_open(acname, destpubkey, paymentsnumber, paymentdenomination)
    except subprocess.CalledProcessError as e:
        print("Something went wrong...")
        print(e)
        input("Press [Enter] to continue...")
    else:
        try:
           channel_open_txid = tx_broadcaster(acname, channel_open_hex["hex"])
        except KeyError as e:
            print("No hex for broadcasting.")
            print(channel_open_hex)
            input("Press [Enter] to continue...")
        else:
            print(colorize("Channel opening transaction succesfully broadcasted: " + channel_open_txid, "green"))
            file.writelines(channel_open_txid + "\n")
            file.close()
            print(colorize("Entry added to channels_list file!\n", "blue"))
            input("Press [Enter] to continue...")

def channel_payment_tui():
    acname = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    print("\nList of channels created by this tool on this instance: ")
    try:
        file00 = open("channels_list", "r")
        for line in file00:
            print(line)
        file00.close()
    except IOError as e:
        print(e)
        print("\nLooks like you not created any channels yet\n")
        pass

    opentxid = input("Input txid of channel opening: ")
    paymentamount = input("Input amount of yours payment: ")

    try:
        channel_payment_hex = channel_payment(acname, opentxid, paymentamount)
    except subprocess.CalledProcessError as e:
        print("Something went wrong...")
        print(e)
        input("Press [Enter] to continue...")
    else:
        try:
            channel_payment_txid = tx_broadcaster(acname, channel_payment_hex["hex"])
        except KeyError as e:
            print("No hex for broadcasting.")
            print(channel_payment_hex)
            input("Press [Enter] to continue...")
        else:
            print(colorize("Channel payment transaction succesfully broadcasted: " + channel_payment_txid, "green"))
            input("Press [Enter] to continue...")

def channel_close_tui():
    acname = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    opentxid = input("Input txid of channel opening: ")
#print list of opened
    try:
        channel_close_hex = channel_close(acname, opentxid)
    except subprocess.CalledProcessError as e:
        print("Something went wrong...")
        print(e)
        input("Press [Enter] to continue...")
    else:
        try:
            channel_close_txid = tx_broadcaster(acname, channel_close_hex["hex"])
        except KeyError as e:
            print("No hex for broadcasting.")
            print(channel_close_hex)
            input("Press [Enter] to continue...")
        else:
            print(colorize("Channel closing transaction succesfully broadcasted: " + channel_close_txid, "green"))
            #save closing txid to file?
            input("Press [Enter] to continue...")

def channel_refund_tui():
    acname = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    #print list of opentxid and closetxid
    opentxid = input("Input txid of channel opening: ")
    closetxid = input("Input txid of channel closing: ")

    try:
        channel_refund_hex = channel_refund(acname, opentxid, closetxid)
    except subprocess.CalledProcessError as e:
        print("Something went wrong...")
        print(e)
        input("Press [Enter] to continue...")
    else:
        try:
            channel_refund_txid = tx_broadcaster(acname, channel_refund_hex["hex"])
        except KeyError as e:
            print("No hex for broadcasting.")
            print(channel_refund_hex)
            input("Press [Enter] to continue...")
        else:
            print(colorize("Channel refund transaction succesfully broadcasted: " + channel_refund_txid, "green"))
            input("Press [Enter] to continue...")

def channels_list_tui():
    acname = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    print(channels_info(acname))
    input("Press [Enter] to continue...")

menuItems = [
    { "Open channel" : channel_open_tui },
    { "Make channel payment" : channel_payment_tui },
    { "Close channel" : channel_close_tui },
    { "Channel refund" : channel_refund_tui },
    { "Get channels list" : channels_list_tui },
    { "Exit": exit },
]

def signal_handler(signal, frame):
     os.execv(__file__, sys.argv)

def main():
    while True:
        os.system('clear')
        signal.signal(signal.SIGINT, signal_handler)
        print(colorize(header, 'pink'))
        print(colorize('CLI version 0.1 by Anton Lysakov\n', 'green'))
        for item in menuItems:
            print(colorize("[" + str(menuItems.index(item)) + "] ", 'blue') + list(item.keys())[0])
        choice = input(">> ")
        try:
            if int(choice) < 0 : raise ValueError
            # Call the matching function
            list(menuItems[int(choice)].values())[0]()
        except (ValueError, IndexError):
            pass

if __name__ == "__main__":
    main()
