import tkinter as tk
import wmi

import psutil


# 获取CPU信息
def get_cpu_info():
    cpu_info = {}
    c = wmi.WMI()
    for processor in c.Win32_Processor():
        cpu_info['Name'] = processor.Name
        cpu_info['Manufacturer'] = processor.Manufacturer
        cpu_info['NumberOfCores'] = processor.NumberOfCores
        cpu_info['NumberOfLogicalProcessors'] = processor.NumberOfLogicalProcessors
    return cpu_info

# 获取硬盘信息
def get_disk_info():
    disk_info = []
    for disk in psutil.disk_partitions():
        disk_info.append(disk.device)
    return disk_info

# 获取MAC地址
def get_mac_address():
    mac_address = ''
    for network in psutil.net_if_addrs().values():
        for addr in network:
            if addr.family == psutil.AF_LINK:
                mac_address = addr.address
    return mac_address

# 获取显卡信息
def get_graphics_card_info():
    graphics_card_info = []
    c = wmi.WMI()
    for gpu in c.Win32_VideoController():
        graphics_card_info.append(gpu.Name)
    return graphics_card_info

# 创建UI界面
def create_ui():
    window = tk.Tk()
    window.title('Hardware Info')
    window.geometry('400x300')

    # 创建标签
    cpu_label = tk.Label(window, text='CPU: {}'.format(get_cpu_info()['Name']))
    cpu_label.pack(pady=10)

    disk_label = tk.Label(window, text='Disk: {}'.format(', '.join(get_disk_info())))
    disk_label.pack(pady=10)

    mac_label = tk.Label(window, text='MAC Address: {}'.format(get_mac_address()))
    mac_label.pack(pady=10)

    graphics_card_label = tk.Label(window, text='Graphics Card: {}'.format(', '.join(get_graphics_card_info())))
    graphics_card_label.pack(pady=10)

    window.mainloop()

# 运行UI界面
if __name__ == '__main__':
    create_ui()