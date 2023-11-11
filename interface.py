from tkinter import ttk, messagebox
import tkinter as tk
import customtkinter

from db import db

window = customtkinter.CTk()
window.title("Учет ПК")
window.geometry('800x765')
window.resizable(False, False)

userid_entry = customtkinter.CTkEntry(window, placeholder_text="ФИО сотрудника", width=290)
userid_entry.grid(row=0, column=0, padx=15, pady=5, sticky='nw', rowspan=4)

address_entry = customtkinter.CTkEntry(window, placeholder_text="Адрес ПК", width=290)
address_entry.grid(row=1, column=0, padx=15, pady=5, sticky='nw', rowspan=4)

phone_entry = customtkinter.CTkEntry(window, placeholder_text="Номер телефона", width=290)
phone_entry.grid(row=2, column=0, padx=15, pady=5, sticky='nw', rowspan=4)

place_entry = customtkinter.CTkEntry(window, placeholder_text="Район города", width=290)
place_entry.grid(row=3, column=0, padx=15, pady=5, sticky='nw', rowspan=4)

# # создание виджета для вывода информации
info_text = customtkinter.CTkTextbox(window, width=785, height=275)
info_text.grid(row=6, column=0, padx=10, pady=2, sticky='w')

# Доп функционал поиск
search_entry = customtkinter.CTkEntry(window, placeholder_text="Поиск", width=230)
search_entry.grid(row=0, column=0, padx=400, pady=5, sticky='nw')

style = ttk.Style()
style.configure('Treeview')
table = ttk.Treeview(window, height=11)
DEFAULT_COLUMNS = ('PC_NAME', 'USER_NAME', 'ADDRESS', 'USER_PHONE', 'AREA')

# размещаем таблицу ниже полей для ввода
table.grid(row=5, column=0, padx=10, sticky='w', columnspan=2)

# задание ширины колонок
table['columns'] = DEFAULT_COLUMNS
table.column('#0', stretch=False, width=0)
table.column('PC_NAME', anchor='center', width=150)
table.column('USER_NAME', anchor='center', width=180)
table.column('ADDRESS', anchor='center', width=142)
table.column('USER_PHONE', anchor='center', width=142)
table.column('AREA', anchor='center', width=162)

# задание заголовков колонок
table.heading('#0')
table.heading('PC_NAME', text='Имя ПК', anchor='center')
table.heading('USER_NAME', text='ФИО', anchor='center')
table.heading('ADDRESS', text='Адрес ПК', anchor='center')
table.heading('USER_PHONE', text='Номер тел.', anchor='center')
table.heading('AREA', text='Район', anchor='center')


def clear_text():
    info_text.delete('1.0', tk.END)


def delete_all_rows():
    try:
        table.delete(*table.get_children())  # удаление всех строк из таблицы
        clear_text()
    except Exception as e:
        info_text.insert(tk.END, "Ошибка при удалении строк из таблицы.\n")


def toggle_theme():
    if switch_theme.get() == 1:
        switch_theme.configure(text="Светлая\n тема")
        customtkinter.set_appearance_mode("light")
    else:
        switch_theme.configure(text="Тёмная\n тема")
        customtkinter.set_appearance_mode("dark")


def delete_pc():
    try:
        # Получение выбранного элемента в таблице
        cur_item = table.focus()

        # Если выбранного элемента нет, завершить функцию
        if not cur_item:
            return

        # Получение ID выбранного элемента из базы данных
        pc_name = table.item(cur_item)['values'][0]
        delete_query = "DELETE FROM PC_INFO WHERE PC_NAME = %s"
        delete_values = (pc_name,)

        # Удаление выбранного элемента из таблицы
        table.delete(cur_item)

        # Удаление выбранного элемента из базы данных
        db_act = db.cursor()
        db_act.execute(delete_query, delete_values)
    except Exception as e:
        messagebox.showinfo(title="Ошибка!", message=f"Ошибка удаления ПК {e}.", icon="cancel")


switch_theme = customtkinter.CTkSwitch(window, text="Тема", command=toggle_theme)
switch_theme.grid(row=7, column=0, padx=695, pady=5, sticky='nw')

delete_all_button = customtkinter.CTkButton(window, text='Очистить всё', command=delete_all_rows, corner_radius=20)
delete_all_button.grid(row=7, column=0, columnspan=2, padx=310, pady=5, sticky='sw')

delete_button = customtkinter.CTkButton(window, text="Удалить ПК", command=delete_pc, corner_radius=10, width=150)
delete_button.grid(row=1, column=0, padx=635, pady=5, sticky='nw')
