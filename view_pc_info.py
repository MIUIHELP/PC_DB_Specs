from db import db
from interface import info_text, table, search_entry
import tkinter as tk


def on_click(event):
    # noinspection PyGlobalUndefined
    global user_addr, user_rayon, mb_idef, mon_idef, cpu_idef, bp_idef, hdd_idef, user_fio, user_phn, i, ram_type_idef, ram_cap_idef, ram_freq_idef, ram_man_idef
    db_act = db.cursor()  # вывод информации о пк по нажатию на строку в таблице
    try:

        items = table.selection()  # получение выбранных строк
        info_text.delete("1.0", "end")  # очистка виджета

        for item in items:

            pc_name = table.item(item, "values")[0]
            # получение имени ПК из строки

            db_act.execute(f"""SELECT 
                    PC_INFO.PC_NAME, ADDRESS_INFO.ADDRESS, PC_INFO.USER_NAME, PC_INFO.MB_SERIAL, AREA_INFO.AREA, PC_INFO.USER_PHONE, 
                    RAM_MAN_INFO.RAM_MAN, RAM_FREQ_INFO.RAM_FREQ, RAM_CAP_INFO.RAM_CAP, RAM_TYPE_INFO.RAM_TYPE, 
                    MONITOR_INFO.MON_MODEL, MONITOR_INFO.MON_SR, CPU_INFO.CPU_NAME, HDD_INFO.PC_ID, MB_INFO.MB_MODEL, BP_INFO.BP_MODEL 
                    FROM PC_INFO 
                    LEFT JOIN ADDRESS_INFO ON PC_INFO.ADR_ID = ADDRESS_INFO.ADR_ID
                    LEFT JOIN AREA_INFO ON PC_INFO.AR_ID = AREA_INFO.AR_ID 
                    LEFT JOIN RAM_MAN_INFO ON PC_INFO.RAM_MAN_ID = RAM_MAN_INFO.RAM_MAN_ID 
                    LEFT JOIN RAM_FREQ_INFO ON PC_INFO.RAM_FREQ_ID = RAM_FREQ_INFO.RAM_FREQ_ID 
                    LEFT JOIN RAM_CAP_INFO ON PC_INFO.RAM_CAP_ID = RAM_CAP_INFO.RAM_CAP_ID 
                    LEFT JOIN RAM_TYPE_INFO ON PC_INFO.RAM_TYPE_ID = RAM_TYPE_INFO.RAM_TYPE_ID 
                    LEFT JOIN MONITOR_INFO ON PC_INFO.MON_ID = MONITOR_INFO.MON_ID
                    LEFT JOIN CPU_INFO ON PC_INFO.CPU_ID = CPU_INFO.CPU_ID
                    LEFT JOIN HDD_INFO ON PC_INFO.HDD_ID = HDD_INFO.HDD_ID 
                    LEFT JOIN BP_INFO ON PC_INFO.BP_ID = BP_INFO.BP_ID 
                    LEFT JOIN MB_INFO ON PC_INFO.MB_ID = MB_INFO.MB_ID 

                    WHERE PC_INFO.PC_NAME = '{pc_name}'""")
            result = db_act.fetchall()

            if result:
                pc_name,  user_addr, user_fio, mb_serial, user_rayon, user_phn, \
                    ram_man_name, ram_freq, ram_cap, ram_type, \
                    mon_model, mon_sr, cpu_name, hdd_id, mb_name, bp_man = result[0]

                # получение информации о всех жестких дисках для данного PC_ID
                db_act.execute(f"SELECT  HDD_NAME, HDD_SERIAL, HDD_SIZE FROM HDD_INFO WHERE PC_ID = '{hdd_id}'")
                hdd_info_list = db_act.fetchall()

                info_text.insert(tk.END, f"Имя ПК: {pc_name}\n")
                info_text.insert(tk.END, f"ФИО пользователя: {user_fio}\n")
                info_text.insert(tk.END, f"Адрес приписки ПК: {user_addr}\n")
                info_text.insert(tk.END, f"Район: {user_rayon}\n", "bold")
                info_text.insert(tk.END, f"Номер телефона: {user_phn}\n")
                info_text.insert(tk.END, f"Модель МП: {mb_name}\n")
                info_text.insert(tk.END, f"Серийный № МП: {mb_serial}\n")
                info_text.insert(tk.END, f"Производитель RAM: {ram_man_name}\n")
                info_text.insert(tk.END, f"Частота RAM: {ram_freq} MГц\n")
                info_text.insert(tk.END, f"Объём RAM: {ram_cap} Гб\n")
                info_text.insert(tk.END, f"Тип RAM: {ram_type}\n")
                info_text.insert(tk.END, f"CPU: {cpu_name}\n")
                info_text.insert(tk.END, f"Модель Монитора: {mon_model}\n")
                info_text.insert(tk.END, f"Серийный № монитора: ")

                if mon_sr != "":
                    info_text.insert(tk.END, f" {mon_sr}")
                else:
                    info_text.insert(tk.END, "Серийный номер монитора не указан.\n")

                for i, hdd_info in enumerate(hdd_info_list):
                    hdd_numb = i + 1
                    if hdd_info:
                        info_text.insert(tk.END, f"\nHDD № {hdd_numb}:")
                        info_text.insert(tk.END,
                                         f"\nМодель: {hdd_info[0]} \nСерийный №: {hdd_info[1]} \nОбъём: {hdd_info[2]} ГБ")
                    else:
                        info_text.insert(tk.END, "Нет информации о жестком диске\n", "italic")
                info_text.insert(tk.END, "\nМодель БП: ", "bold")
                if bp_man != "":
                    info_text.insert(tk.END, f"{bp_man}\n")
                else:
                    info_text.insert(tk.END, "Не указан.\n")
                db_act.close()
    except Exception as e:
        if db is not None:
            print(e)
            db_act.close()
        else:
            raise e


table.bind("<ButtonRelease-1>", on_click)


def search_user():
    # Получаем текст из поля поиска
    table.delete(*table.get_children())
    # noinspection PyGlobalUndefined
    global db_search
    search_text = search_entry.get()
    # Проверяем, заполнено ли поле поиска
    if not search_text:
        # Если поле поиска пустое, ничего не делаем
        info_text.insert(tk.END, "Вы не ввели данные для поиска.\n")
        return
    # Поиск по запросу Фамилии пользователя
    try:
        db_search = db.cursor()
        query = (
            "SELECT PC_INFO.PC_NAME, PC_INFO.USER_NAME, ADDRESS_INFO.ADDRESS, PC_INFO.USER_PHONE, AREA_INFO.AREA "
            "FROM PC_INFO "
            "LEFT JOIN ADDRESS_INFO ON PC_INFO.ADR_ID = ADDRESS_INFO.ADR_ID "
            "LEFT JOIN AREA_INFO ON PC_INFO.AR_ID = AREA_INFO.AR_ID "
            "WHERE PC_INFO.USER_NAME LIKE %s OR ADDRESS_INFO.ADDRESS LIKE %s "
            "OR PC_INFO.PC_NAME LIKE %s OR PC_INFO.USER_PHONE LIKE %s "
            "OR AREA_INFO.AREA LIKE %s;"
        )

        search_term = "%" + search_text + "%"

        db_search.execute(query, (search_term, search_term, search_term, search_term, search_term,))

        result = db_search.fetchall()

    except Exception as e:
        info_text.insert(tk.END, "По вашему запросу ничего не найдено.\n")
        result = []
    if len(result) > 0:
        for row in result:


            # добавление каждой строки в таблицу

            table.insert('', tk.END, values=row[0:6])
            db_search.close()
            table.bind("<ButtonRelease-1>", on_click)

