import sqlite3
import os
import argparse
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

#load arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', default=False)
init = bool(parser.parse_args().i)

#connect to data base
conn = sqlite3.connect('paper_info.db')
cur = conn.cursor()
res = None

#initialization
if init:
    cur.execute(''' create table INFO
                (ID int primary key,
                TITLE text not null,
                ALIAS text default "Noname",
                PHY int not null default 1,
                ML int not null default 0,
                OTHER int not null default 0,
                KEYWORD text default "None",
                PATH text not null,
                DATE int not null);''')
    cur.execute(''' create table RES_ID
                (RESID int primary key);''')
    conn.commit()
    cur.close()
    conn.close()
    with open('PM.sh', 'w') as f:
        f.write('#!/bin/bash\npython3 paper_manager.py')
    os.system('chmod u+x PM.sh')
    print('Initialization finished.')
    exit()

#main
win = tk.Tk()
win.title('Papaer Manager - Yme')
win.geometry('800x800+200+5')
tk.Label(win, text='Paper Manager', font=('Arial', 32)).pack()

#search
def res_format(res):
    id_ = res[0]
    title, alias, kwd = res[1], res[2], res[6]
    tag_list = [res[3], res[4], res[5]]
    path = res[7]
    rcv_date = res[8]
    tag_list_str = []
    if tag_list[0] == 1:
        tag_list_str.append('physics')
    else:
        tag_list_str.append('')
    if tag_list[1] == 1:
        tag_list_str.append('machine learning')
    else:
        tag_list_str.append('')
    if tag_list[2] == 1:
        tag_list_str.append('Others')
    else:
        tag_list_str.append('')
    text = '%d |%s| <%s> Key word: %s #%s %s %s# %d @%s'%(id_, title, alias, kwd, tag_list_str[0], tag_list_str[1], tag_list_str[2], rcv_date, path)
    return text
def search_cmd():
    search_arg1 = search_combobox.get()
    search_arg2 = search_tag_combobox.get()
    dict1 = {'title':'TITLE', 'alias':'ALIAS', 'PMID':'ID', 'key word':'KEYWORD'}
    dict2 = {'physics':'PHY', 'machine learning':'ML', 'others':'OTHER'}
    key1 = dict1[search_arg1]
    key2 = dict2[search_arg2]
    cur.execute('''select * from INFO where "%s" glob "*%s*" and %s == 1 order by DATE desc;'''%(key1, search_word.get(), key2))
    res = cur.fetchall()
    if res == []:
        search_log.configure(text='No results for current condition.')
        search_res.delete(0, tk.END)
        return
    res_num = len(res)
    search_log.configure(text='%3d result(s) found for current condition.'%res_num)
    search_res.delete(0, tk.END)
    for item in res:
        search_res.insert(tk.END, res_format(item))
    return
def list_all_cmd():
    cur.execute('''select * from INFO order by DATE desc;''')
    res = cur.fetchall()
    if res == []:
        search_log.configure(text='The database is empty.')
        search_res.delete(0, tk.END)
        return
    res_num = len(res)
    search_log.configure(text='%3d result(s) found for current condition.'%res_num)
    search_res.delete(0, tk.END)
    for item in res:
        search_res.insert(tk.END, res_format(item))
    return
tk.Label(win, text='#search presaved paper in paper manager\'s database#').pack()
search_frame = tk.Frame(win)
search_word = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_word, width=40)
search_entry.focus()
search_combobox = ttk.Combobox(search_frame, state='readonly')
search_combobox['values'] = ('title', 'alias', 'PMID', 'key word')
search_combobox.current(0)
search_tag_combobox = ttk.Combobox(search_frame, state='readonly')
search_tag_combobox['values'] = ('physics', 'machine learning', 'others')
search_tag_combobox.current(0)
search_button = tk.Button(search_frame, text='search', command=search_cmd)
search_all_button = tk.Button(search_frame, text='list all', command=list_all_cmd)
search_entry.grid(row=0, column=0)
search_combobox.grid(row=0, column=1)
search_tag_combobox.grid(row=0, column=2)
search_button.grid(row=0, column=3)
search_all_button.grid(row=0, column=4)
search_frame.pack()
search_res_frame = tk.Frame(win)
search_log = tk.Label(win, text='Set your condition and click "search".')
search_log.pack()
search_res_xscroll = tk.Scrollbar(search_res_frame, orient=tk.HORIZONTAL)
search_res_yscroll = tk.Scrollbar(search_res_frame)
search_res = tk.Listbox(search_res_frame, selectmode='BROWSE', width=100, height=40, 
                        xscrollcommand=search_res_xscroll.set,
                        yscrollcommand=search_res_yscroll.set)
search_res_xscroll.config(command=search_res.xview)
search_res_yscroll.config(command=search_res.yview)
search_res_xscroll.pack(side=tk.BOTTOM, fill='both')
search_res.pack(side=tk.LEFT)
search_res_yscroll.pack(side=tk.RIGHT, fill='y')
search_res_frame.pack()

#add paper
def browse_cmd():
    fn = filedialog.askopenfilename(initialdir='./paper_folder')
    if(fn != ''):
        add_path.set(fn)
    return
def add_cmd():
    cur.execute('select * from RES_ID order by RESID;')
    res = cur.fetchall()
    if res == []:#no residule id
        cur.execute('select count(*) from INFO;')
        id_ = cur.fetchone()[0] + 1
    else:
        id_ = res[0][0]
        cur.execute('delete from RES_ID where RESID == ?;', (id_, ))
        conn.commit()
    if add_phy_bool.get():
        tag_phy = 1
    else:
        tag_phy =0
    if add_ml_bool.get():
        tag_ml = 1
    else:
        tag_ml =0
    if add_other_bool.get():
        tag_other = 1
    else:
        tag_other =0
    datenow = datetime.datetime.now().strftime('%Y%m%d%H%M')
    cur.execute('insert into INFO values(?, ?, ?, ?, ?, ?, ?, ?, ?);', (id_, add_title_str.get(), add_alias_str.get(), tag_phy, tag_ml, tag_other, add_kwd_str.get(), add_path.get(), datenow))
    conn.commit()
    messagebox.showinfo('Notice', 'Successfully added paper to database!')
    add_title_entry.delete(0, tk.END)
    add_alias_entry.delete(0, tk.END)
    add_kwd_entry.delete(0, tk.END)
    add_entry.delete(0, tk.END)
    add_phy_check.deselect()
    add_ml_check.deselect()
    add_other_check.deselect()
    return
tk.Label(win, text='#add new paper into paper manager\'s database#').pack()
add_frame = tk.Frame(win)
add_path = tk.StringVar()
add_entry = tk.Entry(add_frame, textvariable=add_path, width=80)
add_browse_button = tk.Button(add_frame, text='browse', command=browse_cmd)
add_confirm_button = tk.Button(add_frame, text='add', command=add_cmd)
add_title_str = tk.StringVar()
add_title_label = tk.Label(add_frame, text='Title:')
add_title_entry = tk.Entry(add_frame, textvariable=add_title_str, width=40)
add_alias_str = tk.StringVar()
add_alias_label = tk.Label(add_frame, text='Alias:')
add_alias_entry = tk.Entry(add_frame, textvariable=add_alias_str, width=40)
add_kwd_str = tk.StringVar()
add_kwd_label = tk.Label(add_frame, text='Key word:')
add_kwd_entry = tk.Entry(add_frame, textvariable=add_kwd_str, width=40)
add_phy_bool = tk.BooleanVar()
add_phy_check = tk.Checkbutton(add_frame, text='PHY', variable=add_phy_bool)
add_ml_bool = tk.BooleanVar()
add_ml_check = tk.Checkbutton(add_frame, text='ML', variable=add_ml_bool)
add_other_bool = tk.BooleanVar()
add_other_check = tk.Checkbutton(add_frame, text='OTHER', variable=add_other_bool)
add_entry.grid(row=0, column=0, columnspan=3)
add_browse_button.grid(row=0, column=3)
add_title_label.grid(row=1, column=0)
add_title_entry.grid(row=1, column=1, columnspan=2)
add_alias_label.grid(row=2, column=0)
add_alias_entry.grid(row=2, column=1, columnspan=2)
add_kwd_label.grid(row=3, column=0)
add_kwd_entry.grid(row=3, column=1, columnspan=2)
add_phy_check.grid(row=4, column=0)
add_ml_check.grid(row=4, column=1)
add_other_check.grid(row=4, column=2)
add_confirm_button.grid(row=4, column=3)
add_frame.pack()

#open/showinfo/delete paper file
def menu_open():
    info = search_res.get(search_res.curselection())
    path = info.split('@')[1]
    print(path)
    if os.path.exists(path):
        os.system('xdg-open %s'%path)
    else:
        messagebox.showwarning('Warning', 'Target paper doesn\'t exsist!')
    return
def menu_showinfo():
    info = search_res.get(search_res.curselection())
    path = info.split('@')[1]
    title = info.split('|')[1]
    alias = info.split('>')[0].split('<')[1]
    messagebox.showinfo('Details', 'Title: %s\nAlias: %s\nFile path: %s'%(title, alias, path))
    return
def menu_delete():
    info = search_res.get(search_res.curselection())
    id_ = int(info.split('|')[0][:-1])
    title = info.split('|')[1]
    cur.execute('delete from INFO where ID == ?', (id_,))
    cur.execute('insert into RES_ID values(?);', (id_,))
    conn.commit()
    messagebox.showinfo('Notice', 'Target paper dropped out from database.\nTitle: %s'%title)
    search_cmd()
    return
def show_menu(event):
    menu.post(event.x_root, event.y_root)
    return
menu = tk.Menu(win)
menu.add_command(label='open this paper', command=menu_open)
menu.add_command(label='show detailed information', command=menu_showinfo)
menu.add_separator()
menu.add_command(label='delete this paper', command=menu_delete)
search_res.bind('<Button-3>', show_menu)

#about me
def aboutme_cmd():
    messagebox.showinfo('about me', '''Version: 0.1.1\nMy email: yghuang@mails.ccnu.edu.cn\nhttps://github.com/LearnerYme/paper_manager''')
    return
aboutme = tk.Button(win, text='about me', command=aboutme_cmd)
aboutme.pack()

win.mainloop()
