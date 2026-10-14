from klase.putovanje import *
from klase.aktivnosti import *
from klase.smjestaj import *
from tkinter import *

def trazi_aktivnost(e,izbor):
    L_razgl=[
        Razgledavanje('Izložba',10,'Zagreb','100 kn'),
        Razgledavanje('Muzej',25,'Zagreb','50 kn'),
        Razgledavanje('Predstava',5,'Rijeka','120 kn')]
    L_izl=[
        Izlet('Plitvice', 10,'Zagreb', 'Zagreb', '500 kn'),
        Izlet('Krka', 10,'Split', 'Split', '500 kn'),
        Izlet('Pozdrav Suncu', 10,'Zadar', 'Zadar', '500 kn')]
    kapacitet=int(e.get())
   
    novi=Toplevel(p)
    Label(novi,text='Rezultati pretraživanja:').pack()
    if izbor.get()==1:
        for i in range(len(L_razgl)):
            if L_razgl[i].k>=kapacitet:
                Label(novi,text=L_razgl[i]).pack()
    else:
        for i in range(len(L_izl)):
            if L_izl[i].k>=kapacitet:
                Label(novi,text=L_izl[i]).pack()
    novi.mainloop()

def test_aktivnosti():
    l=Label(p,text='Unesi podatke o aktivnosti')
    l.grid(row=0,column=0)
    l=Label(p,text='Vrsta aktivnosti:')
    l.grid(row=1,column=0)
    izbor=IntVar()
    Radiobutton(p,variable=izbor,text='Razgledavanje',value=1).grid(row=1,column=1)
    Radiobutton(p,variable=izbor,text='Izlet',value=2).grid(row=1,column=2)
    l=Label(p,text='Broj osoba:')
    l.grid(row=2,column=0)
    e=Entry(p, width=20)
    e.grid(row=2,column=1)
    b=Button(p,text='PRETRAZI',command=lambda:trazi_aktivnost(e,izbor))
    b.grid(row=3,column=0)
def test_putovanja():
    pass
def test_smjestaj():
    pass

if __name__=='__main__':
    p=Tk()
    p.geometry('600x300+100+100')
    menibar=Menu(p)
    podmeni=Menu(menibar)
    podmeni.add_command(label='Aktivnosti', command=test_aktivnosti)
    podmeni.add_command(label='Putovanja',command=test_putovanja)
    podmeni.add_command(label='Smještaj',underline= 1, command=test_smjestaj)
    podmeni.add_command(label="Izlaz", underline= 1, command= exit, accelerator= "Ctrl+Q")
    menibar.add_cascade(label='Izbornik', menu=podmeni)
    p.config(menu=menibar)
    test_aktivnosti()
    p.mainloop()
