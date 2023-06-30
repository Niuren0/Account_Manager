from tkinter import Tk, Menu, CENTER, END, S, Label, ttk, messagebox, Button, Entry, Toplevel
import sqlite3 as sql
import random, string

def create_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def table_exists():
    with sql.connect("vt.db") as conn:
        cursor = conn.cursor()

        # PRAGMA komutu ile tabloların listesini alıyoruz
        cursor.execute("PRAGMA table_info(user)")
        tables = cursor.fetchall()

    if len(tables) == 0:        
        firstTop = Tk()
        firstTop.geometry("310x180")
        firstTop.title(f"Hoşgeldin!")
        firstTop.iconbitmap("icon.ico")
        firstTop.resizable(False, False)
        firstTop.protocol("WM_DELETE_WINDOW", lambda:None)

        Label(firstTop, text="Hoşgeldin, uygulama şifreni sakın unutma!\nHesap silerken veya diğer önemli\nişlemlerde bu şifreyi girmen gerekecek!").place(x=10, y=10)
        Label(firstTop, text="Uygulama Şifren:").place(x=10, y=97)
        password = Entry(firstTop)
        password.place(x=130, y=100)
        password.insert(0, f"{create_password(12)}")

        createButton = Button(firstTop, text="Şifre Üret", command=lambda: (password.delete(0, END), password.insert(0, f"{create_password(12)}")))
        createButton.place(relx=0.35, rely=0.85, anchor=CENTER)

        def save():
            if len(str(password.get())) >= 3:
                with sql.connect("vt.db") as vt:
                    im = vt.cursor()
                    
                    try:
                        im.execute("DELETE FROM user")
                    except:
                        pass
                    im.execute("""CREATE TABLE IF NOT EXISTS user(password)""")

                    im.execute("""INSERT INTO user (password) VALUES (?)""", (str(password.get()),))
                    vt.commit()

                firstTop.destroy()

            else:
                messagebox.showerror("Kısa Şifre", "Şifre en az 3 karakter olmalı!")

        saveButton = Button(firstTop, text="Kaydet", command=save)
        saveButton.place(relx=0.65, rely=0.85, anchor=CENTER)

        firstTop.mainloop()

table_exists()

root = Tk()
root.iconbitmap("icon.ico")
root.geometry("700x300")
root.title("Hesap Yöneticisi - Niuren_")
root.resizable(False, False)

def item_clicked(event):    
    global last_click_time
    current_time = event.time
    delta = current_time - last_click_time
    if delta < 300:
        item_selected(event)
    last_click_time = current_time

def double(Dname):
    setTop = Toplevel(root)
    setTop.geometry("300x290")
    setTop.title(f"Hesap: {Dname}")
    setTop.iconbitmap("icon.ico")
    setTop.resizable(False, False)
    setTop.grab_set()

    def key_pressed(event):
        if event.keysym == "Escape":
            setTop.destroy()

    setTop.bind('<Key>', key_pressed)

    with sql.connect("vt.db") as vt:
        im = vt.cursor()
        im.execute("""SELECT * FROM datas WHERE name=?""", (Dname,))
        result = im.fetchone()
        Dnickname = result[1]
        Dmail = result[2]
        Dpassword = result[3]
        Dnote = result[4]
        
        im.execute("""SELECT password FROM user""")
        Dpassword2 = im.fetchone()[0]
    
    Label(setTop, text="İsim: ").place(x=10, y=10)
    name = Entry(setTop)
    name.place(x=110, y=10)
    name.insert(0, f"{Dname}")

    Label(setTop, text="Kullanıcı Adı:").place(x=10, y=50)
    nickname = Entry(setTop)
    nickname.place(x=110, y=50)
    nickname.insert(0, Dnickname)

    Label(setTop, text=("e-Mail:")).place(x=10, y=90)
    mail = Entry(setTop)
    mail.place(x=110, y=90)
    mail.insert(0, Dmail)

    Label(setTop, text=("Not: ")).place(x=10, y=130)
    note = Entry(setTop)
    note.place(x=110, y=130)
    note.insert(0, Dnote)

    Label(setTop, text=("Şifre: ")).place(x=10, y=170)
    password = Entry(setTop, show="*")
    password.place(x=110, y=170)

    Label(setTop, text=("Yeni Şifre: ")).place(x=10, y=210)
    repassword = Entry(setTop, show="*")
    repassword.place(x=110, y=210)

    def save():
        with sql.connect("vt.db") as vt:
            im = vt.cursor()

            if str(repassword.get()) != "":
                if len(str(repassword.get())) >= 3:
                    if str(password.get()) != Dpassword:
                        messagebox.showerror("Hatalı Şifre", "Mevcut şifre girilenle uyuşmuyor!")
                        return
                    else:
                        im.execute("""UPDATE datas SET password=?""", (str(repassword.get()),))
                else:
                    messagebox.showerror("Kısa Şifre", "Şifre en az 3 karakter olmalı!")
                    return

            if str(name.get()) != Dname:
                im.execute("""UPDATE datas SET name=? WHERE name=?""", (str(name.get()), str(Dname),))
            if str(nickname.get()) != Dnickname:
                im.execute("""UPDATE datas SET nickname=? WHERE name=?""", (str(name.get()), str(Dname),))
            if str(mail.get()) != Dmail:
                im.execute("""UPDATE datas SET mail=? WHERE name=?""", (str(name.get()), str(Dname),))
            if str(note.get()) != Dnote:
                im.execute("""UPDATE datas SET note=? WHERE name=?""", (str(name.get()), str(Dname),))
            
            vt.commit()

            tree.delete(*tree.get_children())

            im.execute("SELECT name, nickname, mail FROM datas")
            contacts = im.fetchall()

            for contact in contacts:
                tree.insert('', END, values=contact)

            setTop.destroy()

            messagebox.showinfo("Başarıyla Kaydedildi", "Girilen bilgiler başarıyla güncellendi.")
    
    saveButton = Button(setTop, text="Kaydet", command=save)
    saveButton.place(relx=0.4, rely=0.9, anchor=CENTER)

    def delete():
        if str(password.get()) != Dpassword2:
            messagebox.showerror("Hatalı Şifre", "Hesabı silmek için uygulama şifresini kullanmanız gerekli!")
        else:
            with sql.connect("vt.db") as vt:
                im = vt.cursor()
                im.execute("""DELETE FROM datas WHERE NAME=?""", (Dname,))
                vt.commit()

            tree.delete(*tree.get_children())

            im.execute("SELECT name, nickname, mail FROM datas")
            contacts = im.fetchall()

            for contact in contacts:
                tree.insert('', END, values=contact)

            setTop.destroy()
            messagebox.showinfo("Hesap Silindi", "Hesap başarıyla silindi.")

    deleteButton = Button(setTop, text="Sil", command=delete)
    deleteButton.place(relx=0.6, rely=0.9, anchor=CENTER)

    setTop.mainloop()

tree = ttk.Treeview(root, columns=("İsim", "Kullanıcı Adı", "e-Mail"), show="headings")
tree.place(relx=.5, rely=.5, anchor=CENTER)

tree.heading("#0", text="sfd")
tree.heading("İsim", text="İsim")
tree.heading("Kullanıcı Adı", text="Kullanıcı Adı")
tree.heading("e-Mail", text="e-Mail")

def item_selected(event):
    global double
    selected_item = tree.focus()
    try:
        values = tree.item(selected_item)["values"][0]
        double(values)
    except IndexError:
        pass

last_click_time = 0
tree.bind('<Button-1>', item_clicked)

def copy2board(event):
    tree = event.widget
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
        
        with sql.connect("vt.db") as vt:
            im = vt.cursor()
            im.execute("""SELECT password FROM datas WHERE name=?""", (record[0],))
            copy = im.fetchone()[0]

        root.clipboard_clear()
        root.clipboard_append(copy)
        root.update()

tree.bind('<<TreeviewSelect>>', copy2board)

tree.delete(*tree.get_children())
with sql.connect("vt.db") as vt:
    im = vt.cursor()

    try:
        im.execute("SELECT name, nickname, mail FROM datas")
        contacts = im.fetchall()
    except:
        contacts = []

for contact in contacts:
    tree.delete()
    tree.insert('', END, values=contact)

def new():
    newTop = Toplevel(root)
    newTop.geometry("300x250")
    newTop.title("Yeni Hesap")
    newTop.iconbitmap("icon.ico")
    newTop.resizable(False, False)
    newTop.grab_set()

    def key_pressed(event):
        if event.keysym == "Escape":
            newTop.destroy()

    newTop.bind('<Key>', key_pressed)

    
    Label(newTop, text="İsim: ").place(x=10, y=10)
    name = Entry(newTop)
    name.place(x=110, y=10)

    Label(newTop, text="Kullanıcı Adı:").place(x=10, y=50)
    nickname = Entry(newTop)
    nickname.place(x=110, y=50)

    Label(newTop, text=("e-Mail:")).place(x=10, y=90)
    mail = Entry(newTop)
    mail.place(x=110, y=90)

    Label(newTop, text=("Şifre: ")).place(x=10, y=130)
    password = Entry(newTop, show="*")
    password.place(x=110, y=130)

    Label(newTop, text=("Not: ")).place(x=10, y=170)
    note = Entry(newTop)
    note.place(x=110, y=170)

    def add():
        if str(name.get()) != "":

            if str(password.get()) != "":        
                with sql.connect("vt.db") as vt:
                    im = vt.cursor()

                    im.execute("""CREATE TABLE IF NOT EXISTS datas(name, nickname, mail, password, note)""")

                    im.execute("""SELECT COUNT(*) FROM datas WHERE name = ?""", (str(name.get()),))
                    result = im.fetchone()

                    if result[0] == 0:
                        im.execute("""INSERT INTO datas(name, nickname, mail, password, note) VALUES (?, ?, ?, ?, ?)""", (str(name.get()), str(nickname.get()), str(mail.get()), str(password.get()), str(note.get()),))

                        tree.delete(*tree.get_children())

                        im.execute("SELECT name, nickname, mail FROM datas")
                        contacts = im.fetchall()

                        for contact in contacts:
                            tree.insert('', END, values=contact)

                        newTop.destroy()
                        newTop.destroy()
                        messagebox.showinfo("Başarılı", "Yeni hesap başarıyla kaydedildi.")
                        

                    else:
                        messagebox.showwarning("Çakışan İsim!", "Aynı isimde bir dosya zaten var!")

                    vt.commit()
                
            else:
                messagebox.showwarning("Eksik Bilgi!", "Parola girmeniz gerekiyor!")

                
        else:
            messagebox.showwarning("Eksik Bilgi!", "İsim girmeniz gerekiyor!")
        
    
    saveButton = Button(newTop, text="Ekle", command=add)
    saveButton.place(relx=0.5, rely=0.9, anchor=CENTER)

    newTop.mainloop()

def settings():
    setsTop = Toplevel(root)
    setsTop.geometry("300x160")
    setsTop.title("Ayarlar")
    setsTop.iconbitmap("icon.ico")
    setsTop.resizable(False, False)
    setsTop.grab_set()

    Label(setsTop, text="Uygulama Şifresi: ").place(x=10, y=10)
    password = Entry(setsTop, show="*")
    password.place(x=130, y=10)

    Label(setsTop, text="Yeni Şifre:").place(x=10, y=50)
    password2 = Entry(setsTop, show="*")
    password2.place(x=130, y=50)

    Label(setsTop, text="Yeni Şifre Tekrar:").place(x=10, y=90)
    repassword2 = Entry(setsTop, show="*")
    repassword2.place(x=130, y=90)

    def save():
        with sql.connect("vt.db") as vt:
            im = vt.cursor()
            
            im.execute("""SELECT password FROM user""")
            Dpassword2 = im.fetchone()[0]
        
        
        if str(password.get()) != Dpassword2:
            messagebox.showerror("Hatalı Şifre", "Uygulama şifresi hatalı!")
        else:
            if len(str(password2.get())) >= 3:
                if str(password2.get()) != str(repassword2.get()):
                    messagebox.showerror("Hatalı Şifre", "Şifreler Uyuşmuyor!")
                else:
                    with sql.connect("vt.db") as vt:
                        im = vt.cursor()
                        im.execute("""UPDATE user SET password=?""", (str(password2.get()),))
                        
                    setsTop.destroy()
                    messagebox.showinfo("Başarıyla Kaydedildi", "Şifre başarıyla güncellendi!")
            else:
                messagebox.showerror("Kısa Şifre", "Şifre en az 3 karakter olmalı!")

    saveButton = Button(setsTop, text="Kaydet", command=save)
    saveButton.place(relx=0.5, rely=0.85, anchor=CENTER)

menu_bar = Menu(root)
menu_bar.add_command(label="Yeni", command=new)
menu_bar.add_command(label="Ayarlar", command=settings)
menu_bar.add_command(label="Çıkış", command=root.quit)

def key_pressed(event):
    if event.keysym == "Escape":
        root.quit()
    elif event.keysym == "n" or event.keysym == "plus":
        new()

root.bind('<Key>', key_pressed)

root.config(menu=menu_bar)
root.mainloop()