import customtkinter
from tkinter import messagebox

from db import db
from interface import window, table


def edit_pcs(pc_name):
    # noinspection PyGlobalUndefined
    global window_height, user_name, adr_result, area_result, user_ph, mb_man, cpu_result, ram_man_result, \
        ram_freq_result, ram_cap_result, ram_type_result, monitor_model, monitor_sr, bp_result, i, create_remove_button, mb_serial
    db_act = db.cursor()
    selected_item = table.focus()
    values = table.item(selected_item, 'values')
    if not values:
        messagebox.showinfo(title="Ошибка!", message="Не выбрана запись для редактирования.", icon="warning")
        return
    pc_name = values[0]

    db_act.execute(f"""SELECT PC_INFO.PC_NAME, ADDRESS_INFO.ADDRESS, PC_INFO.USER_NAME, PC_INFO.MB_SERIAL, AREA_INFO.AREA, 
    PC_INFO.USER_PHONE, RAM_MAN_INFO.RAM_MAN, RAM_FREQ_INFO.RAM_FREQ, RAM_CAP_INFO.RAM_CAP, RAM_TYPE_INFO.RAM_TYPE, 
    MONITOR_INFO.MON_MODEL, MONITOR_INFO.MON_SR, CPU_INFO.CPU_NAME, HDD_INFO.PC_ID, MB_INFO.MB_MODEL, 
    BP_INFO.BP_MODEL FROM PC_INFO LEFT JOIN ADDRESS_INFO ON PC_INFO.ADR_ID = ADDRESS_INFO.ADR_ID LEFT JOIN AREA_INFO 
    ON PC_INFO.AR_ID = AREA_INFO.AR_ID LEFT JOIN RAM_MAN_INFO ON PC_INFO.RAM_MAN_ID = RAM_MAN_INFO.RAM_MAN_ID LEFT 
    JOIN RAM_FREQ_INFO ON PC_INFO.RAM_FREQ_ID = RAM_FREQ_INFO.RAM_FREQ_ID LEFT JOIN RAM_CAP_INFO ON 
    PC_INFO.RAM_CAP_ID = RAM_CAP_INFO.RAM_CAP_ID LEFT JOIN RAM_TYPE_INFO ON PC_INFO.RAM_TYPE_ID = 
    RAM_TYPE_INFO.RAM_TYPE_ID LEFT JOIN MONITOR_INFO ON PC_INFO.MON_ID = MONITOR_INFO.MON_ID LEFT JOIN CPU_INFO ON 
    PC_INFO.CPU_ID = CPU_INFO.CPU_ID LEFT JOIN HDD_INFO ON PC_INFO.HDD_ID = HDD_INFO.HDD_ID LEFT JOIN BP_INFO ON 
    PC_INFO.BP_ID = BP_INFO.BP_ID LEFT JOIN MB_INFO ON PC_INFO.MB_ID = MB_INFO.MB_ID
    WHERE PC_INFO.PC_NAME = '{pc_name}'""")
    result = db_act.fetchall()

    if result:
        pc_name, adr_result, user_name, mb_serial, area_result, user_ph, \
            ram_man_result, ram_freq_result, ram_cap_result, ram_type_result, \
            monitor_model, monitor_sr, cpu_result, hdd_id, mb_man, bp_result = result[0]

    db_act.execute(f"SELECT * FROM HDD_INFO WHERE PC_ID ='{pc_name}'")
    hdd_result = db_act.fetchall()

    db_act.close()
    # Создание нового окна для редактирования информации о ПК
    if not hasattr(window, 'edit_window') or not window.edit_window.winfo_exists():
        window.edit_window = customtkinter.CTkToplevel(window)
        window.edit_window.title(f"Редактирование сведений о ПК {pc_name}")
        window.edit_window.grab_set()
        window_height = 550

        # Создание формы для редактирования информации о ПК
        customtkinter.CTkLabel(window.edit_window, text="Имя ПК:").grid(row=0, column=0, padx=5)
        pc_new_name_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        pc_new_name_entry.grid(row=0, column=1, sticky='w')
        pc_new_name_entry.insert(0, pc_name)

        customtkinter.CTkLabel(window.edit_window, text="Имя пользователя:").grid(row=1, column=0, padx=5)
        user_name_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        user_name_entry.grid(row=1, column=1, sticky='w')
        user_name_entry.insert(0, user_name)

        customtkinter.CTkLabel(window.edit_window, text="Адрес пользователя:").grid(row=2, column=0, padx=5)
        user_address_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        user_address_entry.grid(row=2, column=1, sticky='w')
        user_address_entry.insert(0, adr_result)

        customtkinter.CTkLabel(window.edit_window, text="Район:").grid(row=3, column=0, padx=5)
        user_area_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        user_area_entry.grid(row=3, column=1, sticky='w')
        user_area_entry.insert(0, area_result)

        customtkinter.CTkLabel(window.edit_window, text="Телефон пользователя:").grid(row=4, column=0, padx=5)
        user_phone_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        user_phone_entry.grid(row=4, column=1, sticky='w')
        user_phone_entry.insert(0, user_ph)

        customtkinter.CTkLabel(window.edit_window, text="Модель МП:").grid(row=5, column=0, padx=5)
        mb_model_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        mb_model_entry.grid(row=5, column=1, sticky='w')
        mb_model_entry.insert(0, mb_man)

        customtkinter.CTkLabel(window.edit_window, text="Серийный № МП:").grid(row=6, column=0, padx=5)
        mb_serial_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        mb_serial_entry.grid(row=6, column=1, sticky='w')
        mb_serial_entry.insert(0, mb_serial)

        customtkinter.CTkLabel(window.edit_window, text="CPU:").grid(row=8, column=0, padx=5)
        cpu_name_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        cpu_name_entry.grid(row=8, column=1, sticky='w')
        cpu_name_entry.insert(0, cpu_result)

        customtkinter.CTkLabel(window.edit_window, text="Производитель RAM:").grid(row=9, column=0, padx=5)
        ram_man_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        ram_man_entry.grid(row=9, column=1, sticky='w')
        ram_man_entry.insert(0, ram_man_result)

        customtkinter.CTkLabel(window.edit_window, text="Частота RAM:").grid(row=10, column=0, padx=5)
        ram_freq_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        ram_freq_entry.grid(row=10, column=1, sticky='w')
        ram_freq_entry.insert(0, ram_freq_result)

        customtkinter.CTkLabel(window.edit_window, text="Объём RAM:").grid(row=11, column=0, padx=5)
        ram_cap_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        ram_cap_entry.grid(row=11, column=1, sticky='w')
        ram_cap_entry.insert(0, ram_cap_result)

        customtkinter.CTkLabel(window.edit_window, text="Тип RAM:").grid(row=12, column=0, padx=5)
        ram_type_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        ram_type_entry.grid(row=12, column=1, sticky='w')
        ram_type_entry.insert(0, ram_type_result)

        customtkinter.CTkLabel(window.edit_window, text="Модель монитора:").grid(row=13, column=0, padx=5)
        monitor_model_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        monitor_model_entry.grid(row=13, column=1, sticky='w')
        monitor_model_entry.insert(0, monitor_model)

        customtkinter.CTkLabel(window.edit_window, text="Серийный № монитора:").grid(row=14, column=0, padx=5)
        monitor_serial_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        monitor_serial_entry.grid(row=14, column=1, sticky='w')
        monitor_serial_entry.insert(0, monitor_sr)

        customtkinter.CTkLabel(window.edit_window, text="Блок питания:").grid(row=15, column=0, padx=5)
        bp_model_entry = customtkinter.CTkEntry(window.edit_window, width=500)
        bp_model_entry.grid(row=15, column=1, sticky='w')
        bp_model_entry.insert(0, bp_result)

        hdd_widgets = []

        # Создать виджеты для каждого жесткого диска
        for i, row in enumerate(hdd_result):
            hdd_numbers = i + 1
            hdd_model = row[1]
            hdd_sr = row[2]
            hdd_cp = row[3]
            hdd_num = row[4]

            if hdd_num == 1:
                window.edit_window.geometry(f"680x515")
            elif hdd_num == 2:
                window.edit_window.geometry(f"680x555")
            elif hdd_num == 3:
                window.edit_window.geometry(f"680x578")
            elif hdd_num == 4:
                window.edit_window.geometry(f"680x615")
            # Создать метку для номера жесткого диска
            hdd_nm_label = customtkinter.CTkLabel(window.edit_window, text="HDD")
            hdd_nm_label.grid(row=16, column=0)

            hdd_model_label = customtkinter.CTkLabel(window.edit_window, text="Модель")
            hdd_model_label.grid(row=16, column=1, sticky='nw')

            # Создать метку для заголовка серийного номера
            hdd_serial_label = customtkinter.CTkLabel(window.edit_window, text="Серийный номер")
            hdd_serial_label.grid(row=16, column=1, sticky='nw', padx=210)

            # Создать метку для заголовка емкости
            hdd_cap_label = customtkinter.CTkLabel(window.edit_window, text="Объём")
            hdd_cap_label.grid(row=16, column=1, sticky='nw', padx=360)

            hdd_nmb_label = customtkinter.CTkLabel(window.edit_window, text="Номер HDD")
            hdd_nmb_label.grid(row=16, column=1, sticky='nw', padx=415)
            hdd_label = customtkinter.CTkLabel(window.edit_window, text=f"HDD №{hdd_numbers}:")
            hdd_label.grid(row=17 + i, column=0)

            # Создать текстовое поле для имени жесткого диска

            hdd_name_entry = customtkinter.CTkEntry(window.edit_window, width=190)
            hdd_name_entry.grid(row=17 + i, column=1, sticky='nw', pady=2)
            hdd_name_entry.insert(0, hdd_model)

            # Создать текстовое поле для серийного номера жесткого диска
            hdd_serial_entry = customtkinter.CTkEntry(window.edit_window)
            hdd_serial_entry.grid(row=17 + i, column=1, sticky='nw', padx=210, pady=2)
            hdd_serial_entry.insert(0, hdd_sr)

            # Создать текстовое поле для емкости жесткого диска
            hdd_cap_entry = customtkinter.CTkEntry(window.edit_window, width=50)
            hdd_cap_entry.grid(row=17 + i, column=1, sticky='nw', padx=360, pady=2)
            hdd_cap_entry.insert(0, hdd_cp)

            hdd_numb_entry = customtkinter.CTkEntry(window.edit_window, width=6)
            hdd_numb_entry.grid(row=17 + i, column=1, sticky='nw', padx=415, pady=2)
            hdd_numb_entry.insert(0, hdd_num)

            def update_hdd_numbers():
                for i in range(len(hdd_widgets)):
                    hdd_numbers = i + 1
                    hdd_widgets[i][0].configure(text=f"HDD №{hdd_numbers}")

            deleted_values = []  # Create a list to store deleted values
            deleted_items = []

            def delete_hdd_widget(index):

                global hdd_name_value, hdd_serial_values, hdd_size_value, hdd_numb_values
                for widget in hdd_widgets:
                    hdd_name_value = widget[1].get()
                    hdd_serial_values = widget[2].get()
                    hdd_size_value = widget[3].get()
                    hdd_numb_values = widget[4].get()

                # Print the values before deleting the widgets
                # print(hdd_name_value, hdd_serial_values, hdd_size_value, hdd_numb_values)

                # Destroy the widgets
                hdd_widgets[index][0].destroy()
                hdd_widgets[index][1].destroy()
                hdd_widgets[index][2].destroy()
                hdd_widgets[index][3].destroy()
                hdd_widgets[index][4].destroy()
                hdd_widgets[index][5].destroy()

                # Store the deleted widget and its values

                deleted_items.append([hdd_name_value, hdd_serial_values, hdd_size_value, hdd_numb_values])

                # Remove the deleted widget from the hdd_widgets list
                del hdd_widgets[index]

                # Print the deleted values

                for i in range(index, len(hdd_widgets)):
                    hdd_widgets[i][0].grid(row=17 + i, column=0)
                    hdd_widgets[i][1].grid(row=17 + i, column=1, sticky='nw', pady=2)
                    hdd_widgets[i][2].grid(row=17 + i, column=1, sticky='nw', padx=210, pady=2)
                    hdd_widgets[i][3].grid(row=17 + i, column=1, sticky='nw', padx=360, pady=2)
                    hdd_widgets[i][4].grid(row=17 + i, column=1, sticky='nw', padx=415, pady=2)
                    hdd_widgets[i][5].grid(row=17 + i, column=1, padx=440)
                for i in range(index, len(hdd_widgets)):
                    hdd_label, hdd_name_entry, hdd_serial_entry, hdd_cap_entry, hdd_numb_entry, delete_button = hdd_widgets[i][0:7]

                    # Обновить номер
                    hdd_numbers = i + 1
                    hdd_label.configure(text=f"HDD №{hdd_numbers}")

                    # Обновить координаты
                    hdd_label.grid(row=17 + i, column=0)
                    hdd_name_entry.grid(row=17 + i, column=1, sticky='nw', pady=2)
                    hdd_serial_entry.grid(row=17 + i, column=1, sticky='nw', padx=210, pady=2)
                    hdd_cap_entry.grid(row=17 + i, column=1, sticky='nw', padx=360, pady=2)
                    hdd_numb_entry.grid(row=17 + i, column=1, sticky='nw', padx=415, pady=2)

            def delete_button_click(index):
                delete_hdd_widget(index)
                update_hdd_numbers()

            delete_button = customtkinter.CTkButton(window.edit_window, text="Удалить", width=10)
            delete_button.grid(row=17 + i, column=1, padx=440)
            delete_button.configure(command=lambda index=i: delete_button_click(index))

            # Добавить виджеты в список
            hdd_widgets.append(
                (hdd_label, hdd_name_entry, hdd_serial_entry, hdd_cap_entry, hdd_numb_entry, delete_button))

        hdd_new_entries = []
        hdd_lbls = []

        # Добавления поля ДОП HDD
        def add_hdd_entry():
            # Подсчёт HDD
            row_nums = len(hdd_new_entries) + 19 + i
            hdd_num_new = len(hdd_widgets) + 1

            # перемещение кнопок "Добавить HDD" и "Сохранить" при добавлении новых строк ввода
            add_hdd_button.grid_forget()
            save_button.grid_forget()
            add_hdd_button.grid(row=row_nums + 2, column=1, padx=5, sticky='w')
            save_button.grid(row=row_nums + 2, column=0)
            del_hdd_button.grid(row=row_nums + 2, column=1, sticky='w')
            # Создание полей ввода нового HDD со смещением +1

            hdd_lbl = customtkinter.CTkLabel(window.edit_window, text=f"HDD №{hdd_num_new + len(hdd_new_entries)}:")
            hdd_lbl.grid(row=row_nums + 1, column=0)
            hdd_lbls.append(hdd_lbl)
            # create the new entry widgets and add them to the window and the list
            hdd_new_name_entry = customtkinter.CTkEntry(window.edit_window, width=190)
            hdd_new_name_entry.grid(row=row_nums + 1, column=1, sticky='w', pady=2)
            hdd_new_serial_entry = customtkinter.CTkEntry(window.edit_window)
            hdd_new_serial_entry.grid(row=row_nums + 1, column=1, sticky='nw', padx=210, pady=2)
            hdd_new_cap_entry = customtkinter.CTkEntry(window.edit_window, width=50)
            hdd_new_cap_entry.grid(row=row_nums + 1, column=1, sticky='nw', padx=360, pady=2)
            hdd_new_numb_entry = customtkinter.CTkEntry(window.edit_window, width=2)
            hdd_new_numb_entry.grid(row=row_nums + 1, column=1, sticky='nw', padx=415, pady=2)
            hdd_new_entries.append((hdd_new_name_entry, hdd_new_serial_entry, hdd_new_cap_entry, hdd_new_numb_entry))

            window_scale()
            show_button()

        # create a button to add more HDD entries
        add_hdd_button = customtkinter.CTkButton(window.edit_window, text="Добавить HDD", command=add_hdd_entry,
                                                 corner_radius=10)
        add_hdd_button.grid(row=19 + i, column=1, sticky='w', pady=2, padx=5)

        def window_scale():
            # noinspection PyGlobalUndefined
            global window_height
            window_height += 20
            window.edit_window.geometry(f"680x{window_height}")

        def delete_hdd_entries():
            # noinspection PyGlobalUndefined
            global window_height
            if len(hdd_new_entries) > 0:
                hdd_lbls[-1].grid_forget()
                del hdd_lbls[-1]
            else:
                del_hdd_button.grid_remove()
            for widget in hdd_new_entries[-1]:
                widget.grid_forget()

            hdd_new_entries.pop()
            window_height -= 30
            window.edit_window.geometry(f"680x{window_height}")

        # Создаем кнопку, но изначально не отображаем ее
        del_hdd_button = customtkinter.CTkButton(window.edit_window, text="Удалить HDD", command=delete_hdd_entries,
                                                 corner_radius=10)
        del_hdd_button.grid(row=18 + 1, column=1, sticky='nw', padx=150, pady=2)
        del_hdd_button.grid_remove()

        def show_button():

            del_hdd_button = customtkinter.CTkButton(window.edit_window, text="Удалить HDD", command=delete_hdd_entries,
                                                     corner_radius=10)

        def save_changes():

            db_save = db.cursor()
            query = "SELECT PC_ID FROM PC_INFO WHERE pc_name = %s"
            data = (str(pc_new_name_entry.get()),)
            db_save.execute(query, data)
            results = db_save.fetchone()

            if results and pc_name != pc_new_name_entry.get():

                messagebox.showinfo(title="Ошибка!", message="ПК с таким именем уже существует.")
            else:
                # Получение новых значений полей из формы
                new_pc_name = pc_new_name_entry.get()
                new_user_name = user_name_entry.get()
                new_user_address = user_address_entry.get()
                new_user_phone = user_phone_entry.get()
                new_mb_model = mb_model_entry.get()
                new_mb_serial = mb_serial_entry.get()
                new_cpu_name = cpu_name_entry.get()
                new_ram_man = ram_man_entry.get()
                new_ram_freq = ram_freq_entry.get()
                new_ram_cap = ram_cap_entry.get()
                new_ram_type = ram_type_entry.get()
                new_monitor_model = monitor_model_entry.get()
                new_monitor_serial = monitor_serial_entry.get()
                new_bp_name = bp_model_entry.get()
                new_user_area = user_area_entry.get()

                adr_ids = new_address_compare(db, new_user_address)
                ar_ids = new_area_compare(db, new_user_area)
                mb_ids = new_mb_compare(db, new_mb_model)
                ram_man_ids = new_ram_man_compare(db, new_ram_man)
                ram_freq_ids = new_ram_freq_compare(db, new_ram_freq)
                ram_cap_ids = new_ram_cap_compare(db, new_ram_cap)
                ram_type_ids = new_ram_type_compare(db, new_ram_type)
                cpu_ids = new_cpu_compare(db, new_cpu_name)
                bp_ids = new_bp_compare(db, new_bp_name)
                mon_ids = new_monitor_compare(db, new_monitor_model, new_monitor_serial)

                db_save = db.cursor()
                for widget in hdd_widgets:
                    hdd_new_name = widget[1].get()
                    hdd_new_serial = widget[2].get()
                    hdd_new_cap = widget[3].get()
                    hdd_new_num = widget[4].get()

                    if new_pc_name != pc_name:
                        db_save.execute(
                            f"UPDATE HDD_INFO SET HDD_NAME = '{hdd_new_name}', HDD_SERIAL = '{hdd_new_serial}', \
                            HDD_SIZE = '{hdd_new_cap}', PC_ID ='{new_pc_name}' WHERE HDD_NUMBER = '{hdd_new_num}' \
                            AND PC_ID = '{pc_name}'")
                    else:
                        db_save.execute(
                            f"UPDATE HDD_INFO SET HDD_NAME = '{hdd_new_name}', HDD_SERIAL = '{hdd_new_serial}', \
                            HDD_SIZE = '{hdd_new_cap}' WHERE HDD_NUMBER = '{hdd_new_num}' AND PC_ID = '{pc_name}'")
                for i, hdd_entry in enumerate(hdd_new_entries):
                    hdd_new_model = hdd_entry[0].get()
                    hdd_new_sr = hdd_entry[1].get()
                    hdd_new_cp = hdd_entry[2].get()
                    hdd_new_nm = hdd_entry[3].get()

                    hdd_new_data_info = [(str(hdd_new_model), str(hdd_new_sr), str(hdd_new_cp), str(hdd_new_nm),
                                          str(pc_name))]
                    hdd_pc_new_info = "INSERT INTO HDD_INFO (HDD_NAME, HDD_SERIAL, HDD_SIZE, HDD_NUMBER, PC_ID) " \
                                      "VALUES (%s, %s, %s, %s, %s)"
                    db_save.executemany(hdd_pc_new_info, hdd_new_data_info)
                for i, hdd_widget in enumerate(deleted_items):
                    hdd_deleted_model = hdd_widget[0]
                    hdd_deleted_serial = hdd_widget[1]
                    hdd_deleted_size = hdd_widget[2]
                    hdd_deleted_numb = hdd_widget[3]
                    delete_hdd = "DELETE FROM HDD_INFO WHERE HDD_NAME = %s AND HDD_SERIAL = %s AND HDD_SIZE = %s AND HDD_NUMBER = %s AND PC_ID = %s"
                    delete_data = [(str(hdd_deleted_model), str(hdd_deleted_serial), str(hdd_deleted_size),
                                    str(hdd_deleted_numb), str(pc_name))]
                    db_save.executemany(delete_hdd, delete_data)

                db_save.execute(
                    f"UPDATE PC_INFO SET PC_NAME = '{str(new_pc_name)}', AR_ID = '{ar_ids}', \
                    USER_NAME = '{str(new_user_name)}', MB_SERIAL = '{new_mb_serial}', ADR_ID = '{adr_ids}', USER_PHONE = '{str(new_user_phone)}', \
                    RAM_MAN_ID = '{ram_man_ids}', RAM_FREQ_ID = '{ram_freq_ids}', RAM_CAP_ID = '{ram_cap_ids}', \
                    RAM_TYPE_ID = '{ram_type_ids}', MON_ID = '{mon_ids}', CPU_ID = '{cpu_ids}', MB_ID = '{mb_ids}', \
                    BP_ID = '{bp_ids}' WHERE PC_NAME = '{pc_name}'")

                db_save.close()

                window.edit_window.destroy()

                refresh_table()

        save_button = customtkinter.CTkButton(window.edit_window, text="Сохранить", command=save_changes,
                                              corner_radius=10)
        save_button.grid(row=19 + i, column=0, pady=2, padx=5)


def new_address_compare(db, new_user_address):
    db_act = db.cursor()
    db_act.execute("SELECT ADR_ID FROM ADDRESS_INFO WHERE ADDRESS = %s", (new_user_address,))
    adr_id = db_act.fetchone()
    if adr_id:
        # Адрес уже есть в таблице, используем полученный ADR_ID для обновления записи в таблице PC_INFO
        return adr_id[0]

        # Адреса нет в таблице, добавляем его и получаем новый ADR_ID
    db_act.execute("INSERT INTO ADDRESS_INFO (ADDRESS) VALUES (%s)", (new_user_address,))
    adr_id = db_act.lastrowid  # получаем ID новой записи
    db_act.close()
    return adr_id


def new_area_compare(db, new_user_area):
    db_act = db.cursor()
    db_act.execute("SELECT AR_ID FROM AREA_INFO WHERE AREA = %s", (new_user_area,))
    ar_id = db_act.fetchone()
    if ar_id:
        # Адрес уже есть в таблице, используем полученный AR_ID для обновления записи в таблице PC_INFO
        return ar_id[0]
        # Адреса нет в таблице, добавляем его и получаем новый ADR_ID
    db_act.execute("INSERT INTO AREA_INFO (AREA) VALUES (%s)", (new_user_area,))
    ar_id = db_act.lastrowid
    db_act.close()
    return ar_id


def new_ram_man_compare(db, new_ram_man):
    db_act = db.cursor()
    db_act.execute("SELECT RAM_MAN_ID FROM RAM_MAN_INFO WHERE RAM_MAN = %s", (new_ram_man,))
    old_ram_man_id = db_act.fetchone()
    if old_ram_man_id:
        # Адрес уже есть в таблице, используем полученный ADR_ID для обновления записи в таблице PC_INFO
        return old_ram_man_id[0]
        # Адреса нет в таблице, добавляем его и получаем новый ADR_ID
    db_act.execute(
        "INSERT INTO RAM_MAN_INFO (RAM_MAN) VALUES (%s)",
        (new_ram_man,))
    new_ram_man_id = db_act.lastrowid  # получаем ID новой записи
    db_act.close()
    return new_ram_man_id


def new_ram_freq_compare(db, new_ram_freq):
    db_act = db.cursor()
    db_act.execute("SELECT RAM_FREQ_ID FROM RAM_FREQ_INFO WHERE RAM_FREQ = %s", (new_ram_freq,))
    old_ram_freq_id = db_act.fetchone()
    if old_ram_freq_id:
        # Адрес уже есть в таблице, используем полученный ADR_ID для обновления записи в таблице PC_INFO
        return old_ram_freq_id[0]
        # Адреса нет в таблице, добавляем его и получаем новый ADR_ID
    db_act.execute(
        "INSERT INTO RAM_FREQ_INFO (RAM_FREQ) VALUES (%s)",
        (new_ram_freq,))
    new_ram_freq_id = db_act.lastrowid  # получаем ID новой записи
    db_act.close()
    return new_ram_freq_id


def new_ram_cap_compare(db, new_ram_cap):
    db_act = db.cursor()
    db_act.execute("SELECT RAM_CAP_ID FROM RAM_CAP_INFO WHERE RAM_CAP = %s", (new_ram_cap,))
    old_ram_cap_id = db_act.fetchone()
    if old_ram_cap_id:
        # Адрес уже есть в таблице, используем полученный ADR_ID для обновления записи в таблице PC_INFO
        return old_ram_cap_id[0]
        # Адреса нет в таблице, добавляем его и получаем новый ADR_ID
    db_act.execute(
        "INSERT INTO RAM_CAP_INFO (RAM_CAP) VALUES (%s)",
        (new_ram_cap,))
    new_ram_cap_id = db_act.lastrowid  # получаем ID новой записи
    db_act.close()
    return new_ram_cap_id


def new_ram_type_compare(db, new_ram_type):
    db_act = db.cursor()
    db_act.execute("SELECT RAM_TYPE_ID FROM RAM_TYPE_INFO WHERE RAM_TYPE = %s", (new_ram_type,))
    old_ram_type_id = db_act.fetchone()
    if old_ram_type_id:
        # Адрес уже есть в таблице, используем полученный ADR_ID для обновления записи в таблице PC_INFO
        return old_ram_type_id[0]
        # Адреса нет в таблице, добавляем его и получаем новый ADR_ID
    db_act.execute(
        "INSERT INTO RAM_TYPE_INFO (RAM_TYPE) VALUES (%s)",
        (new_ram_type,))
    new_ram_type_id = db_act.lastrowid  # получаем ID новой записи
    db_act.close()
    return new_ram_type_id


def new_mb_compare(db, new_mb_model):
    db_act = db.cursor()
    db_act.execute("SELECT MB_ID FROM MB_INFO WHERE MB_MODEL = %s", (new_mb_model,))
    mb_id = db_act.fetchone()

    if mb_id:
        # Адрес уже есть в таблице, используем полученный ADR_ID для обновления записи в таблице PC_INFO
        return mb_id[0]
        # Адреса нет в таблице, добавляем его и получаем новый ADR_ID
    db_act.execute(
        "INSERT INTO MB_INFO (MB_MODEL) VALUES (%s)", (new_mb_model,))
    mb_id = db_act.lastrowid  # получаем ID новой записи
    db_act.close()
    return mb_id


def new_cpu_compare(db, new_cpu_name):
    db_act = db.cursor()
    db_act.execute("SELECT CPU_ID FROM CPU_INFO WHERE CPU_NAME = %s", (new_cpu_name,))
    cpu_id = db_act.fetchone()

    if cpu_id:
        # Адрес уже есть в таблице, используем полученный ADR_ID для обновления записи в таблице PC_INFO
        return cpu_id[0]
        # Адреса нет в таблице, добавляем его и получаем новый ADR_ID
    db_act.execute(
        "INSERT INTO CPU_INFO (CPU_NAME) VALUES (%s)", (new_cpu_name,))
    cpu_id = db_act.lastrowid  # получаем ID новой записи
    db_act.close()
    return cpu_id


def new_monitor_compare(db, new_monitor_model, new_monitor_serial):
    db_act = db.cursor()
    db_act.execute("SELECT MON_ID FROM MONITOR_INFO WHERE MON_MODEL = %s AND MON_SR = %s",
                   (new_monitor_model, new_monitor_serial,))
    mon_ids_list = db_act.fetchall()
    if len(mon_ids_list) > 0:
        mon_ids = mon_ids_list[0][0]
        # Адрес уже есть в таблице, используем полученный ADR_ID для обновления записи в таблице PC_INFO
        db_act.close()
        return mon_ids

    db_insert = db.cursor()
    db_insert.execute(
        "INSERT INTO MONITOR_INFO (MON_MODEL, MON_SR) VALUES (%s, %s)",
        (new_monitor_model, new_monitor_serial,))
    mon_ids = db_insert.lastrowid  # получаем ID новой записи
    db_insert.close()
    return mon_ids


def new_bp_compare(db, new_bp_name):
    db_act = db.cursor()
    db_act.execute("SELECT BP_ID FROM BP_INFO WHERE BP_MODEL = %s", (new_bp_name,))
    bp_id_list = db_act.fetchall()
    if len(bp_id_list) > 0:
        bp_id = bp_id_list[0][0]
        # Адрес уже есть в таблице, используем полученный ADR_ID для обновления записи в таблице PC_INFO
        db_act.close()
        return bp_id

    # Адреса нет в таблице, добавляем его и получаем новый ADR_ID
    db_insert = db.cursor()
    db_insert.execute("INSERT INTO BP_INFO (BP_MODEL) VALUES (%s)", (new_bp_name,))
    bp_id = db_insert.lastrowid
    db_insert.close()
    db_act.close()
    return bp_id


def refresh_table(sort_order="PC_NAME"):
    db_act = db.cursor()

    # Выполняем запрос к БД для получения данных
    db_act.execute(
        f"SELECT PC_INFO.PC_NAME, PC_INFO.USER_NAME, ADDRESS_INFO.ADDRESS, PC_INFO.USER_PHONE, AREA_INFO.AREA FROM "
        f"PC_INFO LEFT JOIN ADDRESS_INFO ON PC_INFO.ADR_ID = ADDRESS_INFO.ADR_ID LEFT JOIN AREA_INFO ON PC_INFO.AR_ID = "
        f"AREA_INFO.AR_ID ORDER BY {sort_order};")
    rows = db_act.fetchall()
    db_act.close()

    # Сохраняем список элементов перед обновлением таблицы
    old_items = table.get_children()

    # Удаляем все строки таблицы
    table.delete(*old_items)

    # Добавляем новые строки с обновленными значениями
    for row in rows:
        table.insert('', 'end', values=row)

    # Выделяем обновленные элементы
    new_items = table.get_children()
    updated_items = list(set(old_items) & set(new_items))
    for item in updated_items:
        table.selection_add(item)
