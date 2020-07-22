import sqlite3 as sql
import tkinter as tk
from sqlite3 import Error

my_db = sql.connect("myDB.db")
c = my_db.cursor()

# Angajat(id#, (!)nume, prenume, (!=)email, tel)
# (!) = not null
# (!=) = unique

def add_angajat(id, nume, prenume, email,tel):
    c.execute("""
        insert into angajat
        values (?,?,?,?,?)
        """, (id,nume,prenume,email,tel))

def get_angajat():
    c.execute("""
            select *
            from angajat
        """)
    return c.fetchall()

def delete(id):
    c.execute("""
        delete from angajat
        where id = ?
    """,(id,))

def commitFunc():
    my_db.commit()

def rollback():
    my_db.rollback()
    show()


root = tk.Tk()

class element:
    def __init__(self, i):
        self.poz = tk.Frame(scrolable)
        self.poz.pack()
        self.id = tk.Entry(self.poz,  borderwidth = 1,justify = "center")
        self.id.pack(side = tk.LEFT)
        a = tk.Entry(self.poz,  borderwidth=1, justify = "center")
        a.pack(side = tk.LEFT)
        b=tk.Entry(self.poz,  borderwidth=1,justify = "center")
        b.pack(side = tk.LEFT)
        c = tk.Entry(self.poz,  borderwidth=1,justify = "center")
        c.pack(side = tk.LEFT)
        d = tk.Entry(self.poz, borderwidth=1,justify = "center")
        d.pack(side = tk.LEFT)
        self.id.insert(0,str(i[0]))
        self.id.configure(state = tk.DISABLED)
        a.insert(0, str(i[1]))
        a.configure(state=tk.DISABLED)
        b.insert(0, str(i[2]))
        b.configure(state=tk.DISABLED)
        c.insert(0, str(i[3]))
        c.configure(state=tk.DISABLED)
        d.insert(0, str(i[4]))
        d.configure(state=tk.DISABLED)
        tk.Button(self.poz, text = "DEL", command = self.delete).pack(side = tk.LEFT)

    def delete(self):
        delete(int(self.id.get()))
        self.poz.destroy()

def rama(val):
    poz = tk.Frame(val)
    poz.pack()
    id = tk.Entry(poz, borderwidth=1, justify="center")
    id.pack(side=tk.LEFT)
    a = tk.Entry(poz,  borderwidth=1, justify="center")
    a.pack(side=tk.LEFT)
    b = tk.Entry(poz, borderwidth=1, justify="center")
    b.pack(side=tk.LEFT)
    c = tk.Entry(poz,  borderwidth=1, justify="center")
    c.pack(side=tk.LEFT)
    d = tk.Entry(poz,  borderwidth=1, justify="center")
    d.pack(side=tk.LEFT)
    id.insert(0, "ID")
    id.configure(state=tk.DISABLED)
    a.insert(0, "NUME")
    a.configure(state=tk.DISABLED)
    b.insert(0, "PRENUME")
    b.configure(state=tk.DISABLED)
    c.insert(0, "EMAIL")
    c.configure(state=tk.DISABLED)
    d.insert(0, "TELEFON")
    d.configure(state=tk.DISABLED)

def show():
    global showZone
    global canvasShow, scrolable
    if canvasShow != None:
        canvasShow.destroy()
    if addZone != None:
        addZone.destroy()
    if showZone != None:
        showZone.destroy()
    showZone = tk.LabelFrame(root, text="SHOW", padx=5, pady=5)
    showZone.grid(padx = 10,pady = 10, row = 0, column = 1, rowspan = 4)
    canvasShow = tk.Canvas(showZone, width = 650)
    canvasShow.pack(side = tk.LEFT)
    scrolable = tk.Frame(canvasShow)
    scrolable.bind(
        "<Configure>",
        lambda e: canvasShow.configure(
            scrollregion=canvasShow.bbox("all")
        )
    )
    canvasShow.create_window((0, 0), window=scrolable, anchor="nw")
    scroll = tk.Scrollbar(showZone, command=canvasShow.yview,orient="vertical")
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    canvasShow.configure(yscrollcommand=scroll.set)
    rama(scrolable)
    row = get_angajat()
    row.sort(key = lambda a:a[0])
    showButton.configure(state = tk.DISABLED)
    addButton.configure(state = "normal")
    for i in row:
        g = element(i)

def add():
    global addZone
    addZone = tk.LabelFrame(root, text="ADD", padx=5, pady=5)
    addButton.configure(state = tk.DISABLED)
    showButton.configure(state = "normal")
    if showZone != None:
        showZone.destroy()
    addZone.grid(padx = 10,pady = 10, row = 0, column = 1, rowspan = 4)
    rama(addZone)
    lista = [tk.Entry(addZone, borderwidth = 1, justify = "center") for i in range(5)]
    for i in lista:
        i.pack(side = tk.LEFT)
    def submit():
        i = [j.get() for j in lista]
        import re
        if re.fullmatch('\d+',i[0]):
            i[0] = int(i[0])
            try:
                add_angajat(i[0],i[1],i[2],i[3],i[4])
            except Error as e:
                pass
        for i in lista:
            i.delete(0,tk.END)

    tk.Button(addZone,text = "ADD EMPLOYEE",command = submit).pack()


addButton = tk.Button(root, text = " ADD ", bg = "black", fg = "white", command = add)
addButton.grid(padx = 10,pady = 10, row = 0, column = 0)

addZone = None

showButton = tk.Button(root, text = " SHOW ", bg = "black", fg = "white", command = show)
showButton.grid(padx = 10,pady = 10, row = 1, column = 0)

showZone = None
canvasShow = None
scrolable = None

commitButton = tk.Button(root, text = " COMMIT ", bg = "black", fg = "white", command = commitFunc)
commitButton.grid(padx = 10,pady = 10, row = 2, column = 0)

rollbackButton = tk.Button(root, text = " ROLLBACK ", bg = "black", fg = "white", command = rollback)
rollbackButton.grid(padx = 10,pady = 10, row = 3, column = 0)

show()
root.mainloop()

my_db.close()