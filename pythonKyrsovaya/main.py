import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, Listbox, Label

conn = sqlite3.connect('office.db')
cursor = conn.cursor()


def entry_def(entry_window):
    login = entry_window.login_entry.get()
    password = entry_window.password_entry.get()

    if not login or not password:
        messagebox.showerror("Ошибка авторизации", "Пожалуйста, введите логин и пароль.")
        return

    if login == "admin" and password == "admin":
        messagebox.showinfo("Успешная авторизация", "Добро пожаловать, HR-менеджер!")
        entry_window.destroy()
        hr_manager_win()
        return

    try:
        cursor.execute("SELECT логин FROM Employee WHERE логин=? AND пароль=?", (login, password))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Успешная авторизация", "Добро пожаловать!")
            entry_window.destroy()
            employee_win(login)
        else:
            messagebox.showerror("Ошибка авторизации", "Неверный логин или пароль.")
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка", str(e))


def register_user(registration_window):
    login = registration_window.login_entry.get()
    password = registration_window.password_entry.get()

    if not login or not password:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return

    try:
        cursor.execute('INSERT INTO Employee (логин, пароль, роль) VALUES (?, ?, ?)', (login, password, 'Сотрудник'))
        conn.commit()
        messagebox.showinfo("Успех", "Регистрация прошла успешно.")
        registration_window.destroy()
        entry_win()
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка", "Этот логин уже существует.")


def entry_win():
    root.withdraw()

    entry_window = tk.Tk()
    entry_window.title('Вход')
    entry_window.geometry('500x400+650+300')
    entry_window.resizable(width=False, height=False)
    entry_window['bg'] = '#272930'

    main_label = Label(entry_window, text='Вход', font='Roboto 18', fg='white', bg='#272930')
    main_label.place(relx=0.5, rely=0.2, anchor='center')

    login_label = Label(entry_window, text='Логин:', font='Roboto 17', fg='white', bg='#272930')
    login_label.place(relx=0.33, rely=0.38, anchor='center')
    entry_window.login_entry = Entry(entry_window, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    entry_window.login_entry.place(relx=0.56, rely=0.38, anchor='center')

    password_label = Label(entry_window, text='Пароль:', font='Roboto 17', fg='white', bg='#272930')
    password_label.place(relx=0.31, rely=0.5, anchor='center')
    entry_window.password_entry = Entry(entry_window, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12, show='*')
    entry_window.password_entry.place(relx=0.56, rely=0.5, anchor='center')

    btn_entry = Button(entry_window, text='Войти', font='Roboto 17', fg='white', bg='#83c775', borderwidth=0, width=18,
                       command=lambda: entry_def(entry_window))
    btn_entry.place(relx=0.5, rely=0.7, anchor='center')

    back_btn = Button(entry_window, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [entry_window.destroy(), root.deiconify()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')


def registration_win():
    root.withdraw()

    registration_window = tk.Tk()
    registration_window.title('Регистрация')
    registration_window.geometry('500x400+650+300')
    registration_window.resizable(width=False, height=False)
    registration_window['bg'] = '#272930'

    main_label = Label(registration_window, text='Регистрация', font='Roboto 18', fg='white', bg='#272930')
    main_label.place(relx=0.5, rely=0.2, anchor='center')

    login_label = Label(registration_window, text='Логин:', font='Roboto 17', fg='white', bg='#272930')
    login_label.place(relx=0.33, rely=0.38, anchor='center')
    registration_window.login_entry = Entry(registration_window, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    registration_window.login_entry.place(relx=0.56, rely=0.38, anchor='center')

    password_label = Label(registration_window, text='Пароль:', font='Roboto 17', fg='white', bg='#272930')
    password_label.place(relx=0.31, rely=0.5, anchor='center')
    registration_window.password_entry = Entry(registration_window, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12, show='*')
    registration_window.password_entry.place(relx=0.56, rely=0.5, anchor='center')

    btn_register = Button(registration_window, text='Зарегистрироваться', font='Roboto 17', fg='white', bg='#83c775',
                          borderwidth=0, width=18,
                          command=lambda: register_user(registration_window))
    btn_register.place(relx=0.5, rely=0.7, anchor='center')

    back_btn = Button(registration_window, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [registration_window.destroy(), root.deiconify()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')


def check_request_status(login):
    try:
        cursor.execute("SELECT id FROM Employee WHERE логин=?", (login,))
        employee_id = cursor.fetchone()[0]

        cursor.execute("""
            SELECT статус 
            FROM vacation_request 
            WHERE id_сотрудника=? 
            AND (статус='Одобрено' OR статус='Не одобрено')
            ORDER BY id DESC LIMIT 1
        """, (employee_id,))

        result = cursor.fetchone()
        if result:
            status = result[0]
            if status == 'Одобрено':
                messagebox.showinfo("Статус запроса", "Ваш запрос на отпуск был одобрен!")
            else:
                messagebox.showinfo("Статус запроса", "Ваш запрос на отпуск был отклонен.")
            cursor.execute("""
                UPDATE vacation_request 
                SET статус='Просмотрено' 
                WHERE id_сотрудника=? 
                AND (статус='Одобрено' OR статус='Не одобрено')
            """, (employee_id,))
            conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка", str(e))


def employee_win(login):
    global employee_window
    employee_window = tk.Tk()
    employee_window.title('Кабинет Сотрудника')
    employee_window.geometry('500x400+650+300')
    employee_window.resizable(width=False, height=False)
    employee_window['bg'] = '#272930'

    cursor.execute('SELECT id FROM Employee WHERE логин=?', (login,))
    log = cursor.fetchall()
    id_login = log[0][0]

    id_label = Label(employee_window, text=f'Ваш ID: {id_login}', font='Roboto 18', fg='white', bg='#272930')
    id_label.place(relx=0.5, rely=0.25, anchor='center')

    profile_btn = Button(employee_window, text='Профиль', font='Roboto 18', fg='white', bg='#83c775', borderwidth=0,
                         width=21, command=lambda: [profile(id_login)])
    profile_btn.place(relx=0.5, rely=0.5, anchor='center')

    vacation_btn = Button(employee_window, text='Запрос на отпуск', font='Roboto 18', fg='white', bg='#83c775',
                          borderwidth=0, width=21, command=request)
    vacation_btn.place(relx=0.5, rely=0.65, anchor='center')

    back_btn = Button(employee_window, text='Выйти из аккаунта', font='Roboto 13', fg='white', bg='#f33f3f',
                      borderwidth=0,
                      command=lambda: [employee_window.destroy(), root.deiconify()])
    back_btn.place(relx=0.82, rely=0.06, anchor='center')

    employee_window.after(1000, lambda: check_request_status(login))


def profile(id_login):
    employee_window.withdraw()

    employee_profile = tk.Tk()
    employee_profile.title('Профиль')
    employee_profile.geometry('500x400+650+300')
    employee_profile.resizable(width=False, height=False)
    employee_profile['bg'] = '#272930'

    profile_title_label = Label(employee_profile, text='Профиль сотрудника', font='Roboto 20', fg='white', bg='#272930')
    profile_title_label.place(relx=0.52, rely=0.2, anchor='center')

    name_label = Label(employee_profile, text='Имя:', font='Roboto 17', fg='white', bg='#272930')
    name_label.place(relx=0.38, rely=0.35, anchor='center')
    employee_profile.name_entry = Label(employee_profile, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    employee_profile.name_entry.place(relx=0.6, rely=0.35, anchor='center')

    surname_label = Label(employee_profile, text='Фамилия:', font='Roboto 17', fg='white', bg='#272930')
    surname_label.place(relx=0.33, rely=0.45, anchor='center')
    employee_profile.surname_entry = Label(employee_profile, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    employee_profile.surname_entry.place(relx=0.6, rely=0.45, anchor='center')

    date_label = Label(employee_profile, text='Дата рождения:', font='Roboto 17', fg='white', bg='#272930')
    date_label.place(relx=0.26, rely=0.55, anchor='center')
    employee_profile.date_entry = Label(employee_profile, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    employee_profile.date_entry.place(relx=0.6, rely=0.55, anchor='center')

    info_label = Label(employee_profile, text='Номер телефона:', font='Roboto 17', fg='white', bg='#272930')
    info_label.place(relx=0.24, rely=0.65, anchor='center')
    employee_profile.info_entry = Label(employee_profile, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    employee_profile.info_entry.place(relx=0.6, rely=0.65, anchor='center')

    back_btn = Button(employee_profile, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [employee_profile.destroy(), employee_window.deiconify()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')

    cursor.execute("SELECT * from profile")
    date = cursor.fetchall()
    for element in date:
        if int(id_login) == element[1]:
            employee_profile.name_entry['text'] = element[2]
            employee_profile.surname_entry['text'] = element[3]
            employee_profile.date_entry['text'] = element[4]
            employee_profile.info_entry['text'] = element[5]


def save_request(request):
    name_req = request.name_req_entry.get()
    date_from = request.start_entry.get()
    date_to = request.finish_entry.get()
    employee_id = request.id_req_entry.get()

    if name_req and date_from and date_to and employee_id:
        cursor.execute("INSERT INTO vacation_request (id_сотрудника, имя, дата_начала, дата_окончания, статус) VALUES (?, ?, ?, ?, ?)",(employee_id, name_req, date_from, date_to, 'В ожидании'))
        conn.commit()
        request.name_req_entry.delete(0, tk.END)
        request.start_entry.delete(0, tk.END)
        request.finish_entry.delete(0, tk.END)
        request.id_req_entry.delete(0, tk.END)
        messagebox.showinfo("Информация", "Запрос на отпуск отправлен.")
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")


def show_requests(request_list_win):
    request_list_win.employee_listbox.delete(0, tk.END)
    cursor.execute("SELECT id, имя, дата_начала, дата_окончания, статус  FROM vacation_request WHERE статус='В ожидании'")
    requests = cursor.fetchall()

    for req in requests:
        request_list_win.employee_listbox.insert(tk.END, f"ID: {req[0]} | Имя: {req[1]} | Даты: {req[2]} - {req[3]} | Статус: {req[4]}")


def update_status(status, request_list_win):
    try:
        selected_request = request_list_win.employee_listbox.get(request_list_win.employee_listbox.curselection())
        request_id = int(selected_request.split("|")[0].split(":")[1].strip())
        cursor.execute("UPDATE vacation_request SET статус=? WHERE id=?", (status, request_id))
        conn.commit()
        show_requests(request_list_win)
        messagebox.showinfo("Информация", f"Запрос {status.lower()} для ID {request_id}.")
    except tk.TclError:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите запрос из списка.")


def request():
    employee_window.withdraw()

    request = tk.Tk()
    request.title('Запрос на отпуск')
    request.geometry('500x400+650+300')
    request.resizable(width=False, height=False)
    request['bg'] = '#272930'

    request_title_label = Label(request, text='Запрос', font='Roboto 20', fg='white', bg='#272930')
    request_title_label.place(relx=0.52, rely=0.15, anchor='center')

    id_req_label = Label(request, text='ID сотрудника', font='Roboto 17', fg='white', bg='#272930')
    id_req_label.place(relx=0.36, rely=0.3, anchor='center')
    request.id_req_entry = Entry(request, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    request.id_req_entry.place(relx=0.68, rely=0.3, anchor='center')

    name_req_label = Label(request, text='Имя', font='Roboto 17', fg='white', bg='#272930')
    name_req_label.place(relx=0.46, rely=0.41, anchor='center')
    request.name_req_entry = Entry(request, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    request.name_req_entry.place(relx=0.68, rely=0.41, anchor='center')

    start_label = Label(request, text='Дата начала', font='Roboto 17', fg='white', bg='#272930')
    start_label.place(relx=0.37, rely=0.52, anchor='center')
    request.start_entry = Entry(request, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    request.start_entry.place(relx=0.68, rely=0.52, anchor='center')

    finish_label = Label(request, text='Дата окончания', font='Roboto 17', fg='white', bg='#272930')
    finish_label.place(relx=0.33, rely=0.63, anchor='center')
    request.finish_entry = Entry(request, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    request.finish_entry.place(relx=0.68, rely=0.63, anchor='center')

    def validate_date_input(char):
        if char in '0123456789.':
            return True
        return False

    vcmd_date = request.register(validate_date_input)
    request.start_entry.config(validate='key', validatecommand=(vcmd_date, '%S'))
    request.finish_entry.config(validate='key', validatecommand=(vcmd_date, '%S'))

    back_btn = Button(request, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [request.destroy(), employee_window.deiconify()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')

    request_btn = Button(request, text='Отправить запрос', font='Roboto 18', fg='white', bg='#83c775', borderwidth=0, width=21, command=lambda: [save_request(request)])
    request_btn.place(relx=0.5, rely=0.78, anchor='center')


def hr_manager_win():
    global hr_manager_window
    hr_manager_window = tk.Tk()
    hr_manager_window.title('Панель HR-менеджера')
    hr_manager_window.geometry('500x400+650+300')
    hr_manager_window.resizable(width=False, height=False)
    hr_manager_window['bg'] = '#272930'

    welcome_label = Label(hr_manager_window, text='Добро пожаловать !', font='Roboto 20', fg='white', bg='#272930')
    welcome_label.place(relx=0.52, rely=0.2, anchor='center')

    report_btn = Button(hr_manager_window, text='Изменить данные сотрудника', font='Roboto 16', fg='white', bg='#83c775', borderwidth=0, width=24, command=id_profile_test)
    report_btn.place(relx=0.5, rely=0.36, anchor='center')

    employee_management_btn = Button(hr_manager_window, text='Список сотрудников', font='Roboto 16', fg='white', bg='#83c775', borderwidth=0, width=24, command=hr_list)
    employee_management_btn.place(relx=0.5, rely=0.48, anchor='center')

    report_btn = Button(hr_manager_window, text='Составить отчет', font='Roboto 16', fg='white', bg='#83c775', borderwidth=0, width=24, command=id_time_test)
    report_btn.place(relx=0.5, rely=0.6, anchor='center')

    report_list_btn = Button(hr_manager_window, text='Список отчетов', font='Roboto 16', fg='white', bg='#83c775', borderwidth=0, width=24, command=rep_list)
    report_list_btn.place(relx=0.5, rely=0.72, anchor='center')

    request_list_btn = Button(hr_manager_window, text='Запросы на отпуск', font='Roboto 16', fg='white', bg='#83c775', borderwidth=0, width=24, command=request_list_get)
    request_list_btn.place(relx=0.5, rely=0.84, anchor='center')

    back_btn = Button(hr_manager_window, text='Выйти из аккаунта', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0,
                      command=lambda: [hr_manager_window.destroy(), root.deiconify()])
    back_btn.place(relx=0.82, rely=0.06, anchor='center')


def request_list_get():
    hr_manager_window.withdraw()

    request_list_win = Tk()
    request_list_win.title('Список Запросов')
    request_list_win.geometry('500x400+650+300')
    request_list_win.resizable(width=False, height=False)
    request_list_win['bg'] = '#272930'

    welcome_label = Label(request_list_win, text='Список запросов', font='Roboto 18', fg='white', bg='#272930')
    welcome_label.place(relx=0.5, rely=0.1, anchor='center')

    request_list_win.employee_listbox = tk.Listbox(request_list_win, width=65, height=13)
    request_list_win.employee_listbox.place(relx=0.5, rely=0.55, anchor='center')

    show_requests_button = tk.Button(request_list_win, text="Показать запросы", font='Roboto 14', fg='white', bg='#83c775', borderwidth=0, width=16,
                                     command=lambda: [show_requests(request_list_win)])
    show_requests_button.place(relx=0.5, rely=0.21, anchor='center')

    approve_button = tk.Button(request_list_win, text="Одобрено", font='Roboto 14', fg='white', bg='#83c775', borderwidth=0, width=12, command=lambda: update_status('Одобрено', request_list_win))
    approve_button.place(relx=0.36, rely=0.9, anchor='center')

    reject_button = tk.Button(request_list_win, text="Отклонено", font='Roboto 14', fg='white', bg='#83c775', borderwidth=0, width=12, command=lambda: update_status('Не одобрено', request_list_win))
    reject_button.place(relx=0.66, rely=0.9, anchor='center')

    scrollbar = ttk.Scrollbar(request_list_win, orient="vertical", command=request_list_win.employee_listbox.yview)
    scrollbar.place(relx=0.89, rely=0.55, anchor='center', height=212)

    request_list_win.employee_listbox.config(yscrollcommand=scrollbar.set)

    back_btn = Button(request_list_win, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [request_list_win.destroy(), hr_manager_win()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')


def rep_list():
    hr_manager_window.withdraw()

    rep_list_window = Tk()
    rep_list_window.title('Список отчетов')
    rep_list_window.geometry('500x400+650+300')
    rep_list_window.resizable(width=False, height=False)
    rep_list_window['bg'] = '#272930'

    welcome_label = Label(rep_list_window, text='Список отчетов', font='Roboto 18', fg='white', bg='#272930')
    welcome_label.place(relx=0.5, rely=0.1, anchor='center')

    cursor.execute('SELECT id, дата, время_начала, время_окончания FROM time_tracking')
    rows = cursor.fetchall()
    rep_list_window.employee_listbox = Listbox(rep_list_window, width=70, height=18)
    rep_list_window.employee_listbox.place(relx=0.5, rely=0.55, anchor='center')

    for row in rows:
        employee_info = f"{row[0]}, дата: {row[1]}, время_начала: {row[2]}, время_окончания: {row[3]}"
        rep_list_window.employee_listbox.insert(tk.END, employee_info)

    scrollbar = ttk.Scrollbar(rep_list_window, orient="vertical", command=rep_list_window.employee_listbox.yview)
    scrollbar.place(relx=0.94, rely=0.55, anchor='center', height=292)

    rep_list_window.employee_listbox.config(yscrollcommand=scrollbar.set)

    back_btn = Button(rep_list_window, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [rep_list_window.destroy(), hr_manager_win()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')


def save_time_tr(time_tr_full, id_employee):
    date = time_tr_full.date_tr_entry.get()
    start_t = time_tr_full.time_start_entry.get()
    finish_t = time_tr_full.time_finish_entry.get()

    if not date or not start_t or not finish_t:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return

    cursor.execute('INSERT INTO time_tracking (id_сотрудника, дата, время_начала, время_окончания) VALUES (?, ?, ?, ?)',(id_employee, date, start_t, finish_t))
    conn.commit()
    messagebox.showinfo("Успех", "Данные успешно сохранены.")


def update_time_tr(time_tr_full, id_employee):
    date = time_tr_full.date_tr_entry.get()
    start_t = time_tr_full.time_start_entry.get()
    finish_t = time_tr_full.time_finish_entry.get()

    if not date or not start_t or not finish_t:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return

    try:
        cursor.execute('UPDATE time_tracking SET дата= ?, время_начала=?, время_окончания=? WHERE id_сотрудника = ?',(date, start_t, finish_t, id_employee))
        conn.commit()
        messagebox.showinfo("Успех", "Данные успешно сохранены.")
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка", "Этот ID уже занят")


def id_date_check():
    flag = False
    id_employee = id_time.id_entry.get()
    cursor.execute("SELECT id_сотрудника FROM time_tracking")
    id_array = cursor.fetchall()
    for id in id_array:
        if int(id_employee) == id[0]:
            flag = True
            time_tr_full_win(id_employee)
        else:
            flag = False
    if flag == False:
        time_tr(id_employee)


def id_time_test():
    hr_manager_window.withdraw()

    global id_time
    id_time = tk.Tk()
    id_time.title('ID')
    id_time.geometry('500x400+650+300')
    id_time.resizable(width=False, height=False)
    id_time['bg'] = '#272930'

    profile_title_label = Label(id_time, text='Профиль сотрудника', font='Roboto 20', fg='white', bg='#272930')
    profile_title_label.place(relx=0.52, rely=0.17, anchor='center')

    id_label = Label(id_time, text='ID Сотрудника', font='Roboto 20', fg='white', bg='#272930')
    id_label.place(relx=0.5, rely=0.38, anchor='center')
    id_time.id_entry = Entry(id_time, font='Roboto 20', fg='white', bg='#353a4b', borderwidth=0, width=12)
    id_time.id_entry.place(relx=0.5, rely=0.51, anchor='center')

    get_btn = Button(id_time, text='Найти профиль', font='Roboto 18', fg='white', bg='#83c775', borderwidth=0, command=id_date_check)
    get_btn.place(relx=0.5, rely=0.74, anchor='center')

    back_btn = Button(id_time, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [id_time.destroy(), hr_manager_window.deiconify()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')


def time_tr_full_win(id_employee):
    id_time.withdraw()

    time_tr_full = tk.Tk()
    time_tr_full.title('Отчет')
    time_tr_full.geometry('500x400+650+300')
    time_tr_full.resizable(width=False, height=False)
    time_tr_full['bg'] = '#272930'

    tracing_title_label = Label(time_tr_full, text='Отчет', font='Roboto 20', fg='white', bg='#272930')
    tracing_title_label.place(relx=0.52, rely=0.2, anchor='center')

    date_tr = Label(time_tr_full, text='Дата:', font='Roboto 17', fg='white', bg='#272930')
    date_tr.place(relx=0.38, rely=0.38, anchor='center')
    time_tr_full.date_tr_entry = Entry(time_tr_full, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    time_tr_full.date_tr_entry.place(relx=0.6, rely=0.38, anchor='center')

    time_start = Label(time_tr_full, text='Время начала:', font='Roboto 17', fg='white', bg='#272930')
    time_start.place(relx=0.28, rely=0.5, anchor='center')
    time_tr_full.time_start_entry = Entry(time_tr_full, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    time_tr_full.time_start_entry.place(relx=0.6, rely=0.5, anchor='center')

    time_finish = Label(time_tr_full, text='Время окончания:', font='Roboto 17', fg='white', bg='#272930')
    time_finish.place(relx=0.25, rely=0.62, anchor='center')
    time_tr_full.time_finish_entry = Entry(time_tr_full, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    time_tr_full.time_finish_entry.place(relx=0.6, rely=0.62, anchor='center')

    def validate_date_input(char):
        if char in '0123456789.':
            return True
        return False

    vcmd_date = time_tr_full.register(validate_date_input)
    time_tr_full.date_tr_entry.config(validate='key', validatecommand=(vcmd_date, '%S'))

    def validate_time_input(char):
        if char in '0123456789:':
            return True
        return False

    vcmd_time = time_tr_full.register(validate_time_input)
    time_tr_full.time_start_entry.config(validate='key', validatecommand=(vcmd_time, '%S'))
    time_tr_full.time_finish_entry.config(validate='key', validatecommand=(vcmd_time, '%S'))

    save_btn = Button(time_tr_full, text='Отправить отчет', font='Roboto 18', fg='white', bg='#83c775', borderwidth=0, width=21,
                      command=lambda: update_time_tr(time_tr_full, id_employee))
    save_btn.place(relx=0.5, rely=0.8, anchor='center')

    back_btn = Button(time_tr_full, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [time_tr_full.destroy(), id_time.deiconify()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')

    cursor.execute("SELECT * from time_tracking")
    date = cursor.fetchall()
    for element in date:
        if int(id_employee) == element[1]:
            time_tr_full.date_tr_entry.insert(0, element[2])
            time_tr_full.time_start_entry.insert(0, element[3])
            time_tr_full.time_finish_entry.insert(0, element[4])


def time_tr(id_employee):
    id_time.withdraw()

    time_tr_win = tk.Tk()
    time_tr_win.title('Отчет')
    time_tr_win.geometry('500x400+650+300')
    time_tr_win.resizable(width=False, height=False)
    time_tr_win['bg'] = '#272930'

    tracing_title_label = Label(time_tr_win, text='Отчет', font='Roboto 20', fg='white', bg='#272930')
    tracing_title_label.place(relx=0.52, rely=0.2, anchor='center')

    date_tr = Label(time_tr_win, text='Дата:', font='Roboto 17', fg='white', bg='#272930')
    date_tr.place(relx=0.38, rely=0.38, anchor='center')
    time_tr_win.date_tr_entry = Entry(time_tr_win, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    time_tr_win.date_tr_entry.place(relx=0.6, rely=0.38, anchor='center')

    time_start = Label(time_tr_win, text='Время начала:', font='Roboto 17', fg='white', bg='#272930')
    time_start.place(relx=0.28, rely=0.5, anchor='center')
    time_tr_win.time_start_entry = Entry(time_tr_win, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    time_tr_win.time_start_entry.place(relx=0.6, rely=0.5, anchor='center')

    time_finish = Label(time_tr_win, text='Время окончания:', font='Roboto 17', fg='white', bg='#272930')
    time_finish.place(relx=0.25, rely=0.62, anchor='center')
    time_tr_win.time_finish_entry = Entry(time_tr_win, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    time_tr_win.time_finish_entry.place(relx=0.6, rely=0.62, anchor='center')

    def validate_date_input(char):
        if char in '0123456789.':
            return True
        return False

    vcmd_date = time_tr_win.register(validate_date_input)
    time_tr_win.date_tr_entry.config(validate='key', validatecommand=(vcmd_date, '%S'))

    def validate_time_input(char):
        if char in '0123456789:':
            return True
        return False

    vcmd_time = time_tr_win.register(validate_time_input)
    time_tr_win.time_start_entry.config(validate='key', validatecommand=(vcmd_time, '%S'))
    time_tr_win.time_finish_entry.config(validate='key', validatecommand=(vcmd_time, '%S'))

    save_btn = Button(time_tr_win, text='Отправить отчет', font='Roboto 18', fg='white', bg='#83c775', borderwidth=0, width=21,
                      command=lambda: save_time_tr(time_tr_win, id_employee))
    save_btn.place(relx=0.5, rely=0.8, anchor='center')

    back_btn = Button(time_tr_win, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [time_tr_win.destroy(), id_time.deiconify()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')


def date_profile(hr_manager_profile_full, id_employee):
    name = hr_manager_profile_full.name_entry.get()
    surname = hr_manager_profile_full.surname_entry.get()
    date = hr_manager_profile_full.date_entry.get()
    info = hr_manager_profile_full.info_entry.get()

    if not name or not surname or not date or not info:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return

    cursor.execute('INSERT INTO profile (id_сотрудника, имя, фамилия, дата_рождения, информация) VALUES (?, ?, ?, ?, ?)',(id_employee, name, surname, date, info))
    conn.commit()
    messagebox.showinfo("Успех", "Данные успешно сохранены.")


def date_update(hr_manager_profile_full, id_employee):
    name = hr_manager_profile_full.name_entry.get()
    surname = hr_manager_profile_full.surname_entry.get()
    date = hr_manager_profile_full.date_entry.get()
    info = hr_manager_profile_full.info_entry.get()

    if not name or not surname or not date or not info:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return

    try:
        cursor.execute('UPDATE profile SET имя = ?, фамилия=?, дата_рождения=?, информация=? WHERE id_сотрудника = ?', (name, surname, date, info, id_employee))
        conn.commit()
        messagebox.showinfo("Успех", "Данные успешно сохранены.")
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка", "Этот ID уже занят")


def id_check():
    flag = False
    id_employee = id_profile.id_entry.get()
    cursor.execute("SELECT id_сотрудника FROM profile")
    id_array = cursor.fetchall()
    for id in id_array:
        if int(id_employee) == id[0]:
            flag = True
            hr_profile_full(id_employee)
        else:
            flag = False
    if flag == False:
        hr_profile(id_employee)


def id_profile_test():
    hr_manager_window.withdraw()

    global id_profile
    id_profile = tk.Tk()
    id_profile.title('ID')
    id_profile.geometry('500x400+650+300')
    id_profile.resizable(width=False, height=False)
    id_profile['bg'] = '#272930'

    profile_title_label = Label(id_profile, text='Профиль сотрудника', font='Roboto 20', fg='white', bg='#272930')
    profile_title_label.place(relx=0.52, rely=0.17, anchor='center')

    id_label = Label(id_profile, text='ID Сотрудника', font='Roboto 20', fg='white', bg='#272930')
    id_label.place(relx=0.5, rely=0.38, anchor='center')
    id_profile.id_entry = Entry(id_profile, font='Roboto 20', fg='white', bg='#353a4b', borderwidth=0, width=12)
    id_profile.id_entry.place(relx=0.5, rely=0.51, anchor='center')

    get_btn = Button(id_profile, text='Найти профиль', font='Roboto 18', fg='white', bg='#83c775', borderwidth=0, command=id_check)
    get_btn.place(relx=0.5, rely=0.74, anchor='center')

    back_btn = Button(id_profile, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [id_profile.destroy(), hr_manager_win()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')


def hr_profile_full(id_employee):
    id_profile.withdraw()

    hr_manager_profile_full = tk.Tk()
    hr_manager_profile_full.title('Профиль')
    hr_manager_profile_full.geometry('500x400+650+300')
    hr_manager_profile_full.resizable(width=False, height=False)
    hr_manager_profile_full['bg'] = '#272930'

    profile_title_label = Label(hr_manager_profile_full, text='Профиль сотрудника', font='Roboto 20', fg='white', bg='#272930')
    profile_title_label.place(relx=0.52, rely=0.2, anchor='center')

    name_label = Label(hr_manager_profile_full, text='Имя:', font='Roboto 17', fg='white', bg='#272930')
    name_label.place(relx=0.38, rely=0.35, anchor='center')
    hr_manager_profile_full.name_entry = Entry(hr_manager_profile_full, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    hr_manager_profile_full.name_entry.place(relx=0.6, rely=0.35, anchor='center')

    surname_label = Label(hr_manager_profile_full, text='Фамилия:', font='Roboto 17', fg='white', bg='#272930')
    surname_label.place(relx=0.33, rely=0.45, anchor='center')
    hr_manager_profile_full.surname_entry = Entry(hr_manager_profile_full, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    hr_manager_profile_full.surname_entry.place(relx=0.6, rely=0.45, anchor='center')

    date_label = Label(hr_manager_profile_full, text='Дата рождения:', font='Roboto 17', fg='white', bg='#272930')
    date_label.place(relx=0.26, rely=0.55, anchor='center')

    hr_manager_profile_full.date_entry = Entry(hr_manager_profile_full, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    hr_manager_profile_full.date_entry.place(relx=0.6, rely=0.55, anchor='center')

    def validate_date_input(char):
        if char in '0123456789.':
            return True
        return False

    vcmd = hr_manager_profile_full.register(validate_date_input)
    hr_manager_profile_full.date_entry.config(validate='key', validatecommand=(vcmd, '%S'))

    info_label = Label(hr_manager_profile_full, text='Номер телефона:', font='Roboto 17', fg='white', bg='#272930')
    info_label.place(relx=0.24, rely=0.65, anchor='center')
    hr_manager_profile_full.info_entry = Entry(hr_manager_profile_full, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    hr_manager_profile_full.info_entry.place(relx=0.6, rely=0.65, anchor='center')

    save_btn = Button(hr_manager_profile_full, text='Сохранить данные', font='Roboto 18', fg='white', bg='#83c775', borderwidth=0, width=21,
                      command=lambda: date_update(hr_manager_profile_full, id_employee))
    save_btn.place(relx=0.5, rely=0.8, anchor='center')

    back_btn = Button(hr_manager_profile_full, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [hr_manager_profile_full.destroy(), id_profile.deiconify()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')

    cursor.execute("SELECT * from profile")
    date = cursor.fetchall()
    for element in date:
        if int(id_employee) == element[1]:
            hr_manager_profile_full.name_entry.insert(0, element[2])
            hr_manager_profile_full.surname_entry.insert(0, element[3])
            hr_manager_profile_full.date_entry.insert(0, element[4])
            hr_manager_profile_full.info_entry.insert(0, element[5])


def hr_profile(id_employee):
    id_profile.withdraw()

    hr_manager_profile = tk.Tk()
    hr_manager_profile.title('Профиль')
    hr_manager_profile.geometry('500x400+650+300')
    hr_manager_profile.resizable(width=False, height=False)
    hr_manager_profile['bg'] = '#272930'

    profile_title_label = Label(hr_manager_profile, text='Профиль сотрудника', font='Roboto 20', fg='white', bg='#272930')
    profile_title_label.place(relx=0.52, rely=0.2, anchor='center')

    name_label = Label(hr_manager_profile, text='Имя:', font='Roboto 17', fg='white', bg='#272930')
    name_label.place(relx=0.38, rely=0.35, anchor='center')
    hr_manager_profile.name_entry = Entry(hr_manager_profile, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    hr_manager_profile.name_entry.place(relx=0.6, rely=0.35, anchor='center')

    surname_label = Label(hr_manager_profile, text='Фамилия:', font='Roboto 17', fg='white', bg='#272930')
    surname_label.place(relx=0.33, rely=0.45, anchor='center')
    hr_manager_profile.surname_entry = Entry(hr_manager_profile, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    hr_manager_profile.surname_entry.place(relx=0.6, rely=0.45, anchor='center')

    date_label = Label(hr_manager_profile, text='Дата рождения:', font='Roboto 17', fg='white', bg='#272930')
    date_label.place(relx=0.26, rely=0.55, anchor='center')
    hr_manager_profile.date_entry = Entry(hr_manager_profile, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    hr_manager_profile.date_entry.place(relx=0.6, rely=0.55, anchor='center')

    def validate_date_input(char):
        if char in '0123456789.':
            return True
        return False

    vcmd = hr_manager_profile.register(validate_date_input)
    hr_manager_profile.date_entry.config(validate='key', validatecommand=(vcmd, '%S'))

    info_label = Label(hr_manager_profile, text='Номер телефона:', font='Roboto 17', fg='white', bg='#272930')
    info_label.place(relx=0.24, rely=0.65, anchor='center')
    hr_manager_profile.info_entry = Entry(hr_manager_profile, font='Roboto 17', fg='white', bg='#353a4b', borderwidth=0, width=12)
    hr_manager_profile.info_entry.place(relx=0.6, rely=0.65, anchor='center')

    save_btn = Button(hr_manager_profile, text='Сохранить данные', font='Roboto 18', fg='white', bg='#83c775', borderwidth=0, width=21,
                      command=lambda: date_profile(hr_manager_profile, id_employee))
    save_btn.place(relx=0.5, rely=0.8, anchor='center')

    back_btn = Button(hr_manager_profile, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [hr_manager_profile.destroy(), id_profile.deiconify()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')


def hr_list():
    hr_manager_window.destroy()

    hr_manager_list = Tk()
    hr_manager_list.title('Список сотрудников')
    hr_manager_list.geometry('500x400+650+300')
    hr_manager_list.resizable(width=False, height=False)
    hr_manager_list['bg'] = '#272930'

    welcome_label = Label(hr_manager_list, text='Список сотрудников', font='Roboto 18', fg='white', bg='#272930')
    welcome_label.place(relx=0.5, rely=0.1, anchor='center')

    cursor.execute('''
        SELECT Employee.id, profile.имя, profile.фамилия 
        FROM Employee 
        INNER JOIN profile ON Employee.id = profile.id
    ''')
    rows = cursor.fetchall()

    hr_manager_list.employee_listbox = Listbox(hr_manager_list, width=50, height=18)
    hr_manager_list.employee_listbox.place(relx=0.5, rely=0.55, anchor='center')

    for row in rows:
        employee_info = f"{row[0]}, имя: {row[1]}, фамилия: {row[2]}"
        hr_manager_list.employee_listbox.insert(tk.END, employee_info)

    scrollbar = ttk.Scrollbar(hr_manager_list, orient="vertical", command=hr_manager_list.employee_listbox.yview)
    scrollbar.place(relx=0.82, rely=0.55, anchor='center', height=292)

    hr_manager_list.employee_listbox.config(yscrollcommand=scrollbar.set)

    back_btn = Button(hr_manager_list, text='Назад', font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9,
                      command=lambda: [hr_manager_list.destroy(), hr_manager_win()])
    back_btn.place(relx=0.9, rely=0.06, anchor='center')


def close_app(root):
    root.destroy()


root = tk.Tk()
root.title('Авторизация')
root['bg'] = '#272930'
root.geometry('500x400+650+300')
root.resizable(width=False, height=False)

label = Label(root, text='Авторизация', font='Roboto 20', fg='white', bg='#272930')
label.place(relx=0.5, rely=0.2, anchor='center')

entry_btn = Button(root, text='Войти', font='Roboto 18', fg='white', bg='#83c775', borderwidth=0, width=18,
                   command=entry_win)
entry_btn.place(relx=0.5, rely=0.43, anchor='center')

registration_btn = Button(root, text='Регистрация', font='Roboto 18', fg='white', bg='#83c775', borderwidth=0, width=18,
                          command=registration_win)
registration_btn.place(relx=0.5, rely=0.6, anchor='center')

close_button = tk.Button(root, text="Закрыть", font='Roboto 13', fg='white', bg='#f33f3f', borderwidth=0, width=9, command=lambda: close_app(root))
close_button.place(relx=0.9, rely=0.06, anchor='center')

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Программа была завершена пользователем.")
conn.commit()
conn.close()
