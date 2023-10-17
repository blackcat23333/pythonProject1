import platform
import tkinter as tk
import wmi

import netifaces
import psutil


def get_graphics_card_info():
    graphics_card_info = []
    c = wmi.WMI()
    for gpu in c.Win32_VideoController():
        graphics_card_info.append(gpu.Name)
    return graphics_card_info

def get_hardware_info():
    cpu_info = platform.processor()

    gpu_info = get_graphics_card_info()
    memory_info = round(psutil.virtual_memory().total/1024/1024/1024)
    system_info = platform.platform()

    return {
        'cpu': cpu_info,


        'gpu': gpu_info,
        'memory': memory_info,
        'system': system_info
    }

def get_mac_addresses():
    mac_addresses = []
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if netifaces.AF_LINK in netifaces.ifaddresses(interface):
            mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            mac_addresses.append(mac_address)
    return mac_addresses

mac_addresses = get_mac_addresses()

def create_ui():
    window = tk.Tk()
    window.title('硬件信息获取工具')
    window.geometry('500x200')

    info = get_hardware_info()

    info_label1 = tk.Label(window, text=f'CPU: {info["cpu"]}')
    info_label1.pack()


    info_label3 = tk.Label(window, text=f'MAC地址: {mac_addresses}')
    info_label3.pack()

    info_label4 = tk.Label(window, text=f'显卡: {info["gpu"]}')
    info_label4.pack()


    info_label5 = tk.Label(window, text=f'内存: {info["memory"]} GB')
    info_label5.pack()

    info_label6 = tk.Label(window, text=f'系统版本: {info["system"]}')
    info_label6.pack()

    window.mainloop()


if __name__ == '__main__':
    create_ui()