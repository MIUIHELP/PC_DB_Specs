import tkinter as tk
import customtkinter
from db import db, create_table
from edit_pc import edit_pcs
from interface import window, table
from new_pc import add_pc
from view_pc_info import search_user
import xlwt

customtkinter.set_default_color_theme("dark-blue")

create_table()


def view_pcs(sort_order="PC_NAME"):
    table.delete(*table.get_children())
    # Просмотр сведений о всех ПК в таблице интерфейса, отсортированных по заданному параметру
    db_act = db.cursor()
    db_act.execute(
        f"SELECT PC_INFO.PC_NAME, PC_INFO.USER_NAME, ADDRESS_INFO.ADDRESS, PC_INFO.USER_PHONE, AREA_INFO.AREA FROM "
        f"PC_INFO LEFT JOIN ADDRESS_INFO ON PC_INFO.ADR_ID = ADDRESS_INFO.ADR_ID LEFT JOIN AREA_INFO ON PC_INFO.AR_ID = "
        f"AREA_INFO.AR_ID ORDER BY {sort_order};")

    result = db_act.fetchall()

    db_act.close()

    for row in result:
        table.insert('', tk.END, values=row)
    table.heading("PC_NAME", text="Имя ПК")
    table.heading("PC_NAME", command=lambda: view_pcs("PC_NAME"))
    table.heading("USER_NAME", text="ФИО")
    table.heading("USER_NAME", command=lambda: view_pcs("USER_NAME"))
    table.heading("ADDRESS", text="Адрес ПК")
    table.heading("ADDRESS", command=lambda: view_pcs("ADDRESS"))
    table.heading("AREA", text="Район")
    table.heading("AREA", command=lambda: view_pcs("AREA"))


def on_select(event):
    try:
        item = event.selection()[0]
        pc_name = event.item(item)['values'][0]

        edit_pcs(pc_name)

    except Exception as e:
        print(e)
        pass


def on_row_select(event):
    # получение выбранной строки
    selection = event.widget.selection()
    if selection:
        # получение имени выбранного ПК
        pc_name = event.widget.item(selection)['values'][0]
        # открытие нового окна с информацией о ПК

        # привязка события Button-2 для каждой строки таблицы
    table.bind('<ButtonRelease-2>', on_row_select)


def export_csv():
    global user_addr, user_rayon, mb_idef, mon_idef, cpu_idef, bp_idef, hdd_idef, user_fio, user_phn, i, ram_type_idef, ram_cap_idef, ram_freq_idef, ram_man_idef, data, col
    db_act = db.cursor()  # вывод информации о пк по нажатию на строку в таблице
    try:

        items = table.selection()  # получение выбранных строк

        for item in items:

            area = table.item(item, "values")[4]
            # получение имени ПК из строки

            db_act.execute(f"""SELECT 
                        PC_INFO.PC_NAME, ADDRESS_INFO.ADDRESS, PC_INFO.USER_NAME, PC_INFO.MB_SERIAL, AREA_INFO.AREA, PC_INFO.USER_PHONE, 
                        RAM_MAN_INFO.RAM_MAN, RAM_FREQ_INFO.RAM_FREQ, RAM_CAP_INFO.RAM_CAP, RAM_TYPE_INFO.RAM_TYPE, 
                        MONITOR_INFO.MON_MODEL, MONITOR_INFO.MON_SR, CPU_INFO.CPU_NAME, MB_INFO.MB_MODEL, BP_INFO.BP_MODEL 
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

                        WHERE AREA_INFO.AREA = '{area}'""")
            result = db_act.fetchall()

            if result:
                workbook = xlwt.Workbook()
                worksheet = workbook.add_sheet('Результаты')  # Создание листа
                header_style = xlwt.easyxf('font:bold on; align: horiz center; align: wrap on; align: vert center')
                data_style = xlwt.easyxf('align: horiz center; align: wrap on; align: vert center')
                column_width = 4000
                columns_to_set_width = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

                for col in columns_to_set_width:
                    worksheet.col(col).width = column_width
                # Заголовки столбцов
                headers = ['ИМЯ ПК', 'Адрес ПК', 'ФИО пользователя', 'Серийный № МП/ПК', 'Район', 'Номер телефона',
                           'Производитель RAM', 'Частота RAM', 'Объем RAM', 'Тип RAM', 'Модель монитора',
                           'Серийный № монитора',
                           'Модель CPU', 'HDD_1', 'HDD_2', 'HDD_3', 'Модель БП']

                # Запись заголовков столбцов
                for col, header in enumerate(headers):
                    worksheet.write(0, col, header, header_style)

                row = 1
                for row_data in result:
                    pc_name, user_addr, user_fio, mb_serial, user_rayon, user_phn, \
                        ram_man_name, ram_freq, ram_cap, ram_type, \
                        mon_model, mon_sr, cpu_name, hdd_id, bp_man = row_data

                    db_act.execute(f"SELECT HDD_NAME, HDD_SERIAL, HDD_SIZE FROM HDD_INFO WHERE PC_ID = '{pc_name}'")
                    hdd_info_list = db_act.fetchall()

                    hdd_list = []  # Initialize hdd_list

                    for hdd_info in hdd_info_list:
                        hdd_name, hdd_serial, hdd_size = hdd_info
                        hdd_list.append(hdd_info)

                    # Handle HDD_2 and HDD_3 based on the number of disks
                    if len(hdd_list) == 1:
                        hdd_list.extend(['', ''])
                    elif len(hdd_list) == 2:
                        hdd_list.extend([''])

                        # Запись данных
                    data = [pc_name, user_addr, user_fio, mb_serial, user_rayon, user_phn,
                            ram_man_name, ram_freq, ram_cap, ram_type,
                            mon_model, mon_sr, cpu_name]
                    data.extend([', '.join(hdd_info) for hdd_info in hdd_list])
                    data.append(bp_man)

                    # Запись данных в строки
                    for col, item in enumerate(data):
                        worksheet.write(row, col, item, data_style)
                    row += 1  # Увеличение номера строки

                # Сохранение рабочей книги
                workbook.save(f'{area}.xls')

    except Exception as e:
        print(e)


export_csv_button = customtkinter.CTkButton(window, text="Экспорт ПК", command=export_csv,
                                            corner_radius=20)

export_csv_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='sw')

add_button = customtkinter.CTkButton(window, text="Добавить ПК(Текущий)", command=add_pc, corner_radius=10, width=290)
add_button.grid(row=4, column=0, padx=15, pady=5, sticky='nw')

view_button = customtkinter.CTkButton(window, text="Просмотреть все ПК", command=view_pcs, corner_radius=10, width=180,
                                      height=40)
view_button.grid(row=3, column=0, padx=605, pady=3, sticky='nw')

edit_button = customtkinter.CTkButton(window, text="Обновить\Изменить", command=lambda: on_select(table),
                                      corner_radius=10, width=180, height=40)
edit_button.grid(row=2, column=0, padx=605, pady=1, sticky='nw')

search_button = customtkinter.CTkButton(window, text="Найти ПК", command=search_user, corner_radius=10, width=150)
search_button.grid(row=0, column=0, padx=635, pady=5, sticky='nw')

window.mainloop()
