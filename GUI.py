import os
from Tkinter import *
import Tkinter
import tkMessageBox


##############################
# Data

def ping(host):
    """
    Returns True if host responds to a ping request
    """
    import os
    import platform

    # Ping parameters as function of OS
    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"

    # Ping
    return os.system("ping " + ping_str + " " + host) == 0


def ping_callback(address_pinged):
    ping_result = "Address Successfully Responded" if ping(address_pinged) == 1 else "Address Not Responding"
    tkMessageBox.showinfo("Pinging Result", ping_result)


def get_ipv4_address():
    if os.name.lower() == "nt":
        return os.popen("ipconfig | findstr /i \"ipv4\"").read().split(': ')[1].rstrip()
    else:
        return os.popen('ifconfig en0').read().split('inet ')[1].split('/')[0].split(' ')[0]


def get_ipv6_address():
    if os.name.lower() == "nt":
        return os.popen("ipconfig | findstr /i \"ipv6\"").read().split("IPv6 Address. . . . . . . . . . . :")[1].split(None,1)[0]
    else:
        return os.popen('ifconfig en0').read().split('inet6 ')[1].split('/')[0].split('%')[0]


def get_ipv4_netmask():
    if os.name.lower() == "nt":
        return os.popen("ipconfig | findstr /i \"subnet mask\"").read().split(": ")[1]
    else:
        return os.popen('ifconfig en0').read().split('inet ')[1].split('/')[0].split(' ')[2]


def get_mac_address():
    if os.name.lower() == "nt":
        return os.popen("ipconfig /all | findstr /i \"physical address\"").read().split(':')[1].split(None,1)[0]
    else:
        return os.popen('ifconfig en1').read().split(' ')[4]

def get_active_count():
    if os.name.lower() == "nt":
        return len(os.popen("netstat -a -n").read().split(None, 1))
    else:
        return len(
        os.popen('ifconfig | pcregrep -M -o \'^[^\t:]+:([^\n]|\n\t)*status: active\'').read().split('active')) - 1


##############################
# Security

def login_callback(username, password):
    not_found = True
    # read file
    with open('login', 'r') as f:
        for line in f:
            # split line by spaces
            cred_list = line.split("\n")[0].split(" ")
            read_user = cred_list[0]
            read_pass = cred_list[1]
            auth = cred_list[2]
            if username == read_user and password == read_pass and auth == '1':
                main(True)
            if username == read_user and password == read_pass and auth == '2':
                main(False)

    if not_found:
        tkMessageBox.showinfo("Login Failed", "Username or Password are incorrect")


##############################
# GUI Login

def login_gui():
    login_root = Tk()
    login_root.wm_title("Please Login First")

    Label(login_root, text="Username:", anchor=W, justify=LEFT).grid(column=0, row=0)
    name_entry = Entry(login_root)
    name_entry.grid(column=1, row=0)
    Label(login_root, text="Password:", anchor=W, justify=LEFT).grid(column=0, row=1)
    pass_entry = Entry(login_root, show='*')
    pass_entry.grid(column=1, row=1)
    login_button = Tkinter.Button(login_root, text="Login",
                                  command=lambda: login_callback(name_entry.get(), pass_entry.get()))
    login_button.grid(column=1, row=4)
    login_root.mainloop()


##############################
# GUI Main

def main(is_authorised):
    root = Tk()
    root.wm_title("Network Details")

    Label(root, text="IPv6 Address:", anchor=W, justify=LEFT).grid(column=0, row=0)
    v6_label = Label(root, text=get_ipv6_address(), justify=LEFT)
    v6_label.grid(column=1, row=0)

    Label(root, text="IPv4 Address:", justify=LEFT).grid(column=0, row=1)
    v4_label = Label(root, text=get_ipv4_address(), justify=LEFT)
    v4_label.grid(column=1, row=1)

    Label(root, text="IPv4 Subnet Mask:").grid(column=0, row=2)
    netmask_label = Label(root, text=get_ipv4_netmask())
    netmask_label.grid(column=1, row=2)

    Label(root, text="MAC Address:").grid(column=0, row=3)
    mac_label = Label(root, text=get_mac_address())
    mac_label.grid(column=1, row=3)

    Label(root, text="Active Connections:").grid(column=0, row=4)
    act_con_label = Label(root, text=get_active_count())
    act_con_label.grid(column=1, row=4)

    # add ping option if user is authorised
    if is_authorised:
        ping_entry = Entry(root, fg="green", bg="black")
        ping_entry.grid(column=0, row=5)
        ping_entry.insert(0, '127.0.0.1')
        ping_button = Tkinter.Button(root, text="Ping Address", command=lambda: ping_callback(ping_entry.get()))
        ping_button.grid(column=1, row=5)

    root.mainloop()


def is_user_connected():
    if  os.name.lower() == "nt":
        return True
    else:
        return os.popen('ifconfig en0').read().split("status: ")[1].rstrip() == "active"


# network
if is_user_connected():
    login_gui()
else:
    tkMessageBox.showinfo("No Network Connection", "No Active Network Detected")
