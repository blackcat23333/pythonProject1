import platform
import tkinter as tk
import wmi

import mysql.connector
import netifaces
import psutil

global_cpu_info = None
global_gpu_info = None
global_mac_info = None
global_memory_info = None
global_system_info = None

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

    global global_cpu_info, global_gpu_info, global_memory_info, global_system_info
    global_cpu_info = cpu_info
    global_gpu_info = gpu_info
    global_memory_info = memory_info
    global_system_info = system_info

    return {
        'cpu': cpu_info,
        'gpu': gpu_info,
        'memory': memory_info,
        'system': system_info
    }

get_hardware_info()

def get_mac_addresses():
    mac_addresses = []
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if netifaces.AF_LINK in netifaces.ifaddresses(interface):
            mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            mac_addresses.append(mac_address)

    global global_mac_info
    global_mac_info = mac_addresses

    return mac_addresses

mac_addresses = get_mac_addresses()

get_mac_addresses()

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

def insert_data(hostname, username, password, database, table_name, data):
    # 创建与数据库的连接
    cnx = mysql.connector.connect(
        host=hostname,
        port=3306,
        user=username,
        password=password,
        database=database,
        allow_local_infile=True
    )

    # 创建一个光标对象
    cursor = cnx.cursor()

    # 插入数据的SQL语句
    insert_query = '''
        INSERT INTO {} (CPU, MAC, GPU, MEMORY, SYSTEMversion)
        VALUES (%s, %s, %s, %s, %s)
    '''.format(table_name)

    try:
        # 执行SQL语句插入数据
        cursor.execute(insert_query, data)
        cnx.commit()
        print("数据插入成功")
    except mysql.connector.Error as err:
        print(f"数据插入失败: {err}")
        cnx.rollback()
    finally:
        # 关闭光标和数据库连接
        cursor.close()
        cnx.close()

my_list_gpu = ','.join(map(str, global_gpu_info))
my_list_mac = ','.join(map(str, global_mac_info))

# 调用函数来插入数据
data = (global_cpu_info, my_list_gpu, my_list_mac, global_memory_info, global_system_info)  # 假设要插入的数据值
insert_data('10.30.162.188', 'root', '123456', 'hardware', 'mytable', data)