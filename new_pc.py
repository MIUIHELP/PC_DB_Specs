import re
import subprocess
import tkinter as tk
import psutil
from tkinter import messagebox
from db import db
from interface import userid_entry, address_entry, phone_entry, place_entry
from pc_specs import get_monitor_model, get_monitor_serial_number, ram_manufacturer, get_cpu_type, \
    pc_names, ram_speed, ram_types, mother_board_model, get_bios_serial_number


def add_pc():
    # Глобал
    global hdd_ids
    db_act = db.cursor()

    # Чтение данных ввода
    user_fio, user_address, user_phone, user_place = userid_entry.get(), address_entry.get(), phone_entry.get(), place_entry.get()

    # Получение данных с других функций
    mon_model, mon_serial = get_monitor_model(), get_monitor_serial_number()
    mb_model = mother_board_model()
    cpu_type, ram_vendor, ram_type = get_cpu_type(), ram_manufacturer(), ram_types()
    ram_hz = ram_speed()
    ram_freq, ram_cap = f"{ram_hz}", f"{str(round(psutil.virtual_memory().total / (1024.0 ** 3)))}"
    default = "Не указан"
    # Проверка на дубликат
    if check_duplicate(pc_names()):
        messagebox.showinfo(title="Ошибка!", message="ПК с таким именем уже существует.", icon="warning")
    else:
        ram_man_ids = insert_ram_man_info(db, ram_vendor)

        ram_freq_ids = insert_ram_freq_info(db, ram_freq)

        ram_cap_ids = insert_ram_cap_info(db, ram_cap)

        ram_type_ids = insert_ram_type_info(db, ram_type)

        cpu_ids = insert_cpu_info(db, cpu_type)

        mb_ids = insert_mb_info(db, mb_model)

        adr_ids = insert_address_info(db, user_address)

        ar_ids = insert_area_info(db, user_place)

        bp_ids = insert_bp_info(db, default)

        # Запись информации в таблицу MONITOR_INFO
        mon_info = "INSERT INTO MONITOR_INFO (MON_MODEL, MON_SR) VALUES (%s, %s)"
        mon_data = [(str(mon_model), str(mon_serial))]
        db_act.executemany(mon_info, mon_data)
        mon_ids = db_act.lastrowid

        # Обработка HDD
        result = subprocess.run(['wmic', 'diskdrive', 'get', 'model,serialnumber,size'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        headers = [header.lower() for header in re.split('\s\s+', lines.pop(0))]
        disks = []
        hdd_numbers = 1
        for line in lines:
            values = re.split('\s\s+', line)
            # извлекаем только цифры из строки размера
            size = re.findall(r'\d+', values[2])[0]
            # конвертируем в ГБ
            size_gb = round(float(size) / 1000000000, 2)
            # Наполнение словаря данными о дисках и последнем авто PC_ID
            disks.append({
                'model': values[0],
                'serialnumber': values[1],
                'size': size_gb,
                'hdd_number': hdd_numbers,
                'pc_id': pc_names()
            })
            # увеличиваем значение счетчика на 1
            hdd_numbers += 1

        # сохранение данных в базу данных

        add_disk = "INSERT INTO HDD_INFO (HDD_NAME, HDD_SERIAL, HDD_SIZE, HDD_NUMBER, PC_ID) VALUES (%(model)s, " \
                   "%(serialnumber)s, %(size)s, %(hdd_number)s, %(pc_id)s)"
        hdd_ids = []
        for disk in disks:
            db_act.execute(add_disk, disk)
            ids = db_act.lastrowid
            hdd_ids.append(ids)
        print(hdd_ids)
        # Запись информации в таблицу PC_INFO
        pc_info = "INSERT INTO PC_INFO (PC_NAME, USER_NAME, MB_SERIAL, ADR_ID, USER_PHONE, AR_ID, RAM_MAN_ID, RAM_FREQ_ID, RAM_CAP_ID, RAM_TYPE_ID, MON_ID, " \
                  "CPU_ID, HDD_ID, MB_ID, BP_ID) VALUES (%s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data_pc = [(
            str(pc_names()), str(user_fio), str(get_bios_serial_number()), str(adr_ids), str(user_phone), str(ar_ids), ram_man_ids, ram_freq_ids, ram_cap_ids, ram_type_ids, mon_ids,
            cpu_ids, hdd_ids[0], mb_ids, bp_ids)]
        db_act.executemany(pc_info, data_pc)

        db_act.close()
        userid_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        place_entry.delete(0, tk.END)


def insert_ram_man_info(db, ram_vendor):
    db_act = db.cursor()

    # Проверяем, есть ли уже запись с такими же данными
    select_query = "SELECT RAM_MAN_ID FROM RAM_MAN_INFO WHERE RAM_MAN = %s"
    db_act.execute(select_query, (ram_vendor,))
    existing_ram_man = db_act.fetchone()
    if existing_ram_man:
        # Если запись уже есть, возвращаем её ID
        return existing_ram_man[0]

    # Если записи нет, добавляем новую
    insert_query = "INSERT INTO RAM_MAN_INFO (RAM_MAN) VALUES (%s)"
    ram_data = (ram_vendor,)
    db_act.execute(insert_query, ram_data)
    ram_man_ids = db_act.lastrowid

    db_act.close()
    return ram_man_ids


def insert_ram_freq_info(db, ram_freq):
    db_act = db.cursor()

    # Проверяем, есть ли уже запись с такими же данными
    select_query = "SELECT RAM_FREQ_ID FROM RAM_FREQ_INFO WHERE RAM_FREQ = %s"
    db_act.execute(select_query, (ram_freq,))
    existing_freq_record = db_act.fetchone()
    if existing_freq_record:
        # Если запись уже есть, возвращаем её ID
        return existing_freq_record[0]

    # Если записи нет, добавляем новую
    insert_query = "INSERT INTO RAM_FREQ_INFO (RAM_FREQ) VALUES (%s)"
    ram_data = (ram_freq,)
    db_act.execute(insert_query, ram_data)
    ram_freq_ids = db_act.lastrowid

    db_act.close()
    return ram_freq_ids


def insert_ram_cap_info(db, ram_cap):
    db_act = db.cursor()

    # Проверяем, есть ли уже запись с такими же данными
    select_query = "SELECT RAM_CAP_ID FROM RAM_CAP_INFO WHERE RAM_CAP = %s"
    db_act.execute(select_query, (ram_cap,))
    existing_cap_record = db_act.fetchone()
    if existing_cap_record:
        # Если запись уже есть, возвращаем её ID
        return existing_cap_record[0]

    # Если записи нет, добавляем новую
    insert_query = "INSERT INTO RAM_CAP_INFO (RAM_CAP) VALUES (%s)"
    ram_data = (ram_cap,)
    db_act.execute(insert_query, ram_data)
    ram_cap_ids = db_act.lastrowid

    db_act.close()
    return ram_cap_ids


def insert_ram_type_info(db, ram_type):
    db_act = db.cursor()

    # Проверяем, есть ли уже запись с такими же данными
    select_query = "SELECT RAM_TYPE_ID FROM RAM_TYPE_INFO WHERE RAM_TYPE = %s"
    db_act.execute(select_query, (ram_type,))
    existing_type_record = db_act.fetchone()
    if existing_type_record:
        # Если запись уже есть, возвращаем её ID
        return existing_type_record[0]

    # Если записи нет, добавляем новую
    insert_query = "INSERT INTO RAM_TYPE_INFO (RAM_TYPE) VALUES (%s)"
    ram_data = (ram_type,)
    db_act.execute(insert_query, ram_data)
    ram_type_ids = db_act.lastrowid

    db_act.close()
    return ram_type_ids


def insert_cpu_info(db, cpu_type):
    db_act = db.cursor()
    cpu_info_query = "SELECT CPU_ID FROM CPU_INFO WHERE CPU_NAME = %s"
    cpu_data = (str(cpu_type),)
    db_act.execute(cpu_info_query, cpu_data)
    existing_cpu = db_act.fetchone()

    if existing_cpu:
        cpu_ids = existing_cpu[0]
        return cpu_ids

    cpu_info_insert = "INSERT INTO CPU_INFO (CPU_NAME) VALUES (%s)"
    db_act.execute(cpu_info_insert, cpu_data)
    cpu_ids = db_act.lastrowid
    db_act.close()
    return cpu_ids


def insert_mb_info(db, mb_model):
    db_act = db.cursor()
    mb_info_query = "SELECT MB_ID FROM MB_INFO WHERE MB_MODEL = %s"
    mb_data = (str(mb_model),)
    db_act.execute(mb_info_query, mb_data)
    existing_mb = db_act.fetchone()

    if existing_mb:
        mb_ids = existing_mb[0]
        return mb_ids

    mb_info_insert = "INSERT INTO MB_INFO (MB_MODEL) VALUES (%s)"
    db_act.execute(mb_info_insert, mb_data)
    mb_ids = db_act.lastrowid
    db_act.close()
    return mb_ids


def insert_address_info(db, user_address):
    db_act = db.cursor()
    adr_info_query = "SELECT ADR_ID FROM ADDRESS_INFO WHERE ADDRESS = %s"
    adr_data = (str(user_address),)
    db_act.execute(adr_info_query, adr_data)
    existing_adr = db_act.fetchone()

    if existing_adr:
        adr_ids = existing_adr[0]
        return adr_ids

    adr_info_insert = "INSERT INTO ADDRESS_INFO (ADDRESS) VALUES (%s)"
    db_act.execute(adr_info_insert, adr_data)
    adr_ids = db_act.lastrowid
    db_act.close()
    return adr_ids


def insert_area_info(db, user_place):
    db_act = db.cursor()
    plc_info_query = "SELECT AR_ID FROM AREA_INFO WHERE AREA = %s"
    plc_data = (str(user_place),)
    db_act.execute(plc_info_query, plc_data)
    existing_plc = db_act.fetchone()

    if existing_plc:
        plc_ids = existing_plc[0]
        return plc_ids

    cpu_info_insert = "INSERT INTO AREA_INFO (AREA) VALUES (%s)"
    db_act.execute(cpu_info_insert, plc_data)
    plc_ids = db_act.lastrowid
    db_act.close()
    return plc_ids


def insert_bp_info(db, default):
    db_act = db.cursor()
    bp_info_query = "SELECT BP_ID FROM BP_INFO WHERE BP_MODEL = %s"
    bp_data = (str(default),)
    db_act.execute(bp_info_query, bp_data)
    existing_bp = db_act.fetchone()

    if existing_bp:
        bp_id = existing_bp[0]
        return bp_id

    bp_info = "INSERT INTO BP_INFO (BP_MODEL) VALUES (%s)"
    bp_data = [(str(default))]
    db_act.execute(bp_info, bp_data)
    bp_id = db_act.lastrowid
    db_act.close()
    return bp_id


def check_duplicate(pc_name):  # Проверка на дуликат имени PC используется в def add_pc
    db_act = db.cursor()
    query = "SELECT * FROM PC_INFO WHERE pc_name = %s"
    data = (pc_name,)
    db_act.execute(query, data)
    result = db_act.fetchone()

    if result is not None:  # проверяем, что есть результат
        return True
    else:
        return False
