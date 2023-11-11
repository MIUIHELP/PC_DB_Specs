import os
import re
import socket
import subprocess
import sys

import wmi
from win32com.client import GetObject


def pc_names():
    # имя пк
    return socket.gethostname()


def monic_model():
    objWMI = GetObject('winmgmts:\\\\.\\root\\WMI').InstancesOf('WmiMonitorID')
    for obj in objWMI:
        if obj.UserFriendlyName is not None:
            res = ''.join(chr(i) for i in obj.UserFriendlyName)
            return str(res)


def monic_serial():
    objWMI = GetObject('winmgmts:\\\\.\\root\\WMI').InstancesOf('WmiMonitorID')
    for obj in objWMI:
        if obj.serialnumberid != None:
            res = ''.join(chr(i) for i in obj.serialnumberid)
            return str(res)


def ram_manufacturer():
    # Производитель оперативы
    ram_man_com = 'WMIC MEMORYCHIP GET Manufacturer /value'.split()
    ram_manufacturer = str(subprocess.check_output(ram_man_com, shell=True)).strip().split("\\n")
    for num, ram_m in enumerate(ram_manufacturer):
        if 'Manufacturer=' in ram_m:
            return ram_m.split("\\r")[0].split("=")[1].strip()


def ram_speed():
    # Частота оперативы
    ram_spf_com = 'WMIC MEMORYCHIP GET Speed /value'.split()
    ram_speed_frequency = str(subprocess.check_output(ram_spf_com, shell=True)).strip().split("\\n")
    for num, rsf in enumerate(ram_speed_frequency):
        if 'Speed=' in rsf:
            return rsf.split("\\r")[0].split("=")[1].strip()


def ram_types():
    memory_type_dict = {
        '22': 'DDR2',
        '24': 'DDR3',
        '26': 'DDR4',
        '34': 'DDR5'
    }
    result = subprocess.run(["wmic", "memorychip", "get", "SMBIOSMemoryType"], capture_output=True, text=True)

    # Разделить вывод по строкам и получить последнюю непустую строку
    output_lines = result.stdout.strip().split('\n')
    memory_type_line = output_lines[-1].strip()

    # Получить значение типа памяти из строки и преобразовать его в строку
    memory_type_value = memory_type_line.split()[-1]
    memory_type_value_string = str(memory_type_value)

    # Получите строковое значение типа памяти из словаря или установите значение «Неизвестно».
    memory_type_string = memory_type_dict.get(memory_type_value_string, 'Тип не известен')

    return memory_type_string


def get_cpu_type():
    # ЦПУ
    from win32com.client import GetObject
    root_winmgmts = GetObject("winmgmts:root\cimv2")
    cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
    return cpus[0].Name


def mother_board_man():
    # производитель МП
    c = wmi.WMI()
    mb_manufacturer = c.Win32_BaseBoard()[0].Manufacturer
    return mb_manufacturer


def mother_board_model():
    # модель МП
    c = wmi.WMI()
    mb_model = c.Win32_Baseboard()[0].Product
    return mb_model


def getMachine_addr():
    # Серийный номер МП
    os_type = sys.platform.lower()
    if "win" in os_type:
        command = "wmic bios get serialnumber"
        return os.popen(command).read().replace("\n", "").replace("	", "").replace(" ", "").replace('SerialNumber',
                                                                                                       '')


def get_monitor_model():
    c = wmi.WMI(namespace="root\WMI")
    for monitor in c.WmiMonitorID():
        user_friendly_name = monitor.UserFriendlyName
        if user_friendly_name:
            # Convert the model name to a string
            model_name = ''.join(chr(i) for i in user_friendly_name)
            return model_name


def get_monitor_serial_number():
    c = wmi.WMI(namespace="root\WMI")
    for monitor in c.WmiMonitorID():
        serial_number = monitor.SerialNumberID
        if serial_number:
            # Convert the serial number to a string
            serial_number = ''.join(chr(i) for i in serial_number)
            return serial_number


def get_disk():
    # выполнение команды wmic для получения информации о жестких дисках
    result = subprocess.run(['wmic', 'diskdrive', 'get', 'model,serialnumber,size'], capture_output=True, text=True)

    # обработка вывода команды с помощью регулярных выражений
    lines = result.stdout.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    headers = [header.lower() for header in re.split('\s\s+', lines.pop(0))]
    disks = []
    for line in lines:
        values = re.split('\s\s+', line)
        disks.append(dict(zip(headers, values)))
    return disks


def get_bios_serial_number():
    command = "wmic Bios Get SerialNumber /value"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    serial_number = None

    for line in output.split('\n'):
        if line.startswith("SerialNumber="):
            serial_number = line.split('=')[1]
            break

    return serial_number
