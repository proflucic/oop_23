import tkinter as tk
from tkinter import ttk, messagebox

from klase.aktivnosti import Aktivnost, Razgledavanje, Izlet
from klase.putovanje import Putovanje, Avion, Autobus


class SortirajPretraziApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pretraživanje i sortiranje objekata")
        self.root.geometry("1050x650")
        self.aktivnosti = []
        self.putovanja = []

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_aktivnosti = ttk.Frame(notebook, padding=10)
        self.tab_putovanja = ttk.Frame(notebook, padding=10)
        notebook.add(self.tab_aktivnosti, text="Aktivnosti")
        notebook.add(self.tab_putovanja, text="Putovanja")

        self._napravi_tab_aktivnosti()
        self._napravi_tab_putovanja()

    def _napravi_tab_aktivnosti(self):
        tab = self.tab_aktivnosti
        top = ttk.Frame(tab)
        top.pack(fill="x", pady=(0, 8))

        ttk.Label(top, text="Vrsta objekta:").pack(side="left")
        self.vrsta_aktivnosti = tk.StringVar(value="Aktivnost")
        izbor = ttk.Combobox(
            top, textvariable=self.vrsta_aktivnosti, state="readonly",
            values=["Aktivnost", "Razgledavanje", "Izlet"], width=18
        )
        izbor.pack(side="left", padx=6)
        izbor.bind("<<ComboboxSelected>>", lambda e: self._polja_aktivnosti())

        self.polja_a = ttk.Frame(tab)
        self.polja_a.pack(fill="x", pady=5)
        self.unosi_a = {}
        self._polja_aktivnosti()

        ttk.Button(top, text="Dodaj objekt", command=self._dodaj_aktivnost).pack(side="left", padx=8)

        search = ttk.Frame(tab)
        search.pack(fill="x", pady=8)
        ttk.Label(search, text="Pretraži:").pack(side="left")
        self.upit_a = tk.StringVar()
        unos = ttk.Entry(search, textvariable=self.upit_a, width=35)
        unos.pack(side="left", padx=6)
        self.upit_a.trace_add("write", lambda *_: self._osvjezi_aktivnosti())
        ttk.Button(search, text="Očisti", command=lambda: self.upit_a.set("")).pack(side="left")

        cols = ("vrsta", "naziv", "lokacija", "cijena", "kapacitet")
        self.tablica_a = ttk.Treeview(tab, columns=cols, show="headings", height=16)
        headers = {
            "vrsta": "Vrsta", "naziv": "Naziv", "lokacija": "Grad / relacija",
            "cijena": "Cijena", "kapacitet": "Kapacitet"
        }
        widths = {"vrsta": 150, "naziv": 240, "lokacija": 250, "cijena": 120, "kapacitet": 140}
        for col in cols:
            self.tablica_a.heading(col, text=headers[col],
                command=lambda c=col: self._sortiraj(self.tablica_a, c, False))
            self.tablica_a.column(col, width=widths[col], anchor="w")
        self.tablica_a.pack(fill="both", expand=True)
        self._osvjezi_aktivnosti()

    def _polja_aktivnosti(self):
        for child in self.polja_a.winfo_children():
            child.destroy()
        vrsta = self.vrsta_aktivnosti.get()
        polja = ["Naziv", "Kapacitet"]
        if vrsta == "Razgledavanje":
            polja += ["Grad", "Cijena"]
        elif vrsta == "Izlet":
            polja += ["Polazište", "Odredište", "Cijena"]
        self.unosi_a = {}
        for i, naziv in enumerate(polja):
            ttk.Label(self.polja_a, text=naziv + ":").grid(row=0, column=i * 2, sticky="w", padx=(0, 4), pady=3)
            unos = ttk.Entry(self.polja_a, width=16)
            unos.grid(row=0, column=i * 2 + 1, sticky="w", padx=(0, 12), pady=3)
            self.unosi_a[naziv] = unos

    def _dodaj_aktivnost(self):
        podaci = {k: v.get().strip() for k, v in self.unosi_a.items()}
        if any(not value for value in podaci.values()):
            messagebox.showwarning("Nedostaju podaci", "Ispunite sva prikazana polja.")
            return
        try:
            vrsta = self.vrsta_aktivnosti.get()
            if vrsta == "Aktivnost":
                obj = Aktivnost(podaci["Naziv"], podaci["Kapacitet"])
            elif vrsta == "Razgledavanje":
                obj = Razgledavanje(podaci["Naziv"], podaci["Kapacitet"], podaci["Grad"], podaci["Cijena"])
            else:
                obj = Izlet(podaci["Naziv"], podaci["Kapacitet"], podaci["Polazište"],
                            podaci["Odredište"], podaci["Cijena"])
            self.aktivnosti.append(obj)
            for unos in self.unosi_a.values():
                unos.delete(0, tk.END)
            self._osvjezi_aktivnosti()
        except (KeyError, TypeError, ValueError) as exc:
            messagebox.showerror("Greška", f"Objekt nije dodan: {exc}")

    def _red_aktivnosti(self, obj):
        if isinstance(obj, Razgledavanje):
            return ("Razgledavanje", obj.n, obj.g, obj.c, obj.k)
        if isinstance(obj, Izlet):
            return ("Izlet", obj.n, f"{obj.p} – {obj.o}", obj.c, obj.k)
        return ("Aktivnost", obj.n, "—", "—", obj.k)

    def _osvjezi_aktivnosti(self):
        if not hasattr(self, "tablica_a"):
            return
        upit = self.upit_a.get().casefold().strip()
        for item in self.tablica_a.get_children():
            self.tablica_a.delete(item)
        for obj in self.aktivnosti:
            red = self._red_aktivnosti(obj)
            if upit and upit not in " ".join(map(str, red)).casefold():
                continue
            self.tablica_a.insert("", "end", values=red)

    def _napravi_tab_putovanja(self):
        tab = self.tab_putovanja
        top = ttk.Frame(tab)
        top.pack(fill="x", pady=(0, 8))
        ttk.Label(top, text="Vrsta objekta:").pack(side="left")
        self.vrsta_putovanja = tk.StringVar(value="Putovanje")
        izbor = ttk.Combobox(
            top, textvariable=self.vrsta_putovanja, state="readonly",
            values=["Putovanje", "Avion", "Autobus"], width=18
        )
        izbor.pack(side="left", padx=6)
        izbor.bind("<<ComboboxSelected>>", lambda e: self._polja_putovanja())
        ttk.Button(top, text="Dodaj objekt", command=self._dodaj_putovanje).pack(side="left", padx=8)

        self.polja_p = ttk.Frame(tab)
        self.polja_p.pack(fill="x", pady=5)
        self.unosi_p = {}
        self._polja_putovanja()

        search = ttk.Frame(tab)
        search.pack(fill="x", pady=8)
        ttk.Label(search, text="Pretraži:").pack(side="left")
        self.upit_p = tk.StringVar()
        ttk.Entry(search, textvariable=self.upit_p, width=35).pack(side="left", padx=6)
        self.upit_p.trace_add("write", lambda *_: self._osvjezi_putovanja())
        ttk.Button(search, text="Očisti", command=lambda: self.upit_p.set("")).pack(side="left")

        cols = ("vrsta", "polaziste", "odrediste", "trajanje", "dodatno")
        self.tablica_p = ttk.Treeview(tab, columns=cols, show="headings", height=16)
        headers = {"vrsta": "Vrsta", "polaziste": "Polazište", "odrediste": "Odredište",
                   "trajanje": "Trajanje", "dodatno": "Dodatni podatak"}
        widths = {"vrsta": 150, "polaziste": 220, "odrediste": 220, "trajanje": 150, "dodatno": 200}
        for col in cols:
            self.tablica_p.heading(col, text=headers[col],
                command=lambda c=col: self._sortiraj(self.tablica_p, c, False))
            self.tablica_p.column(col, width=widths[col], anchor="w")
        self.tablica_p.pack(fill="both", expand=True)
        self._osvjezi_putovanja()

    def _polja_putovanja(self):
        for child in self.polja_p.winfo_children():
            child.destroy()
        vrsta = self.vrsta_putovanja.get()
        polja = ["Polazište", "Odredište"]
        if vrsta == "Avion":
            polja += ["Izravno (da/ne)", "Trajanje"]
        elif vrsta == "Autobus":
            polja += ["Trajanje", "Vrsta autobusa"]
        self.unosi_p = {}
        for i, naziv in enumerate(polja):
            ttk.Label(self.polja_p, text=naziv + ":").grid(row=0, column=i * 2, sticky="w", padx=(0, 4), pady=3)
            unos = ttk.Entry(self.polja_p, width=18)
            unos.grid(row=0, column=i * 2 + 1, sticky="w", padx=(0, 12), pady=3)
            self.unosi_p[naziv] = unos

    def _dodaj_putovanje(self):
        podaci = {k: v.get().strip() for k, v in self.unosi_p.items()}
        if any(not value for value in podaci.values()):
            messagebox.showwarning("Nedostaju podaci", "Ispunite sva prikazana polja.")
            return
        vrsta = self.vrsta_putovanja.get()
        if vrsta == "Putovanje":
            obj = Putovanje(podaci["Polazište"], podaci["Odredište"])
        elif vrsta == "Avion":
            izravno = podaci["Izravno (da/ne)"].casefold()
            if izravno not in ("da", "ne"):
                messagebox.showwarning("Neispravan unos", "Polje 'Izravno' mora biti 'da' ili 'ne'.")
                return
            obj = Avion(podaci["Polazište"], podaci["Odredište"], izravno == "da", podaci["Trajanje"])
        else:
            obj = Autobus(podaci["Polazište"], podaci["Odredište"],
                          podaci["Trajanje"], podaci["Vrsta autobusa"])
        self.putovanja.append(obj)
        for unos in self.unosi_p.values():
            unos.delete(0, tk.END)
        self._osvjezi_putovanja()

    def _red_putovanja(self, obj):
        if isinstance(obj, Avion):
            return ("Avion", obj.polaziste, obj.odrediste, obj.trajanje,
                    "Izravno" if obj.izravno else "S presjedanjem")
        if isinstance(obj, Autobus):
            return ("Autobus", obj.polaziste, obj.odrediste, obj.trajanje, obj.vrsta)
        return ("Putovanje", obj.polaziste, obj.odrediste, "—", "—")

    def _osvjezi_putovanja(self):
        if not hasattr(self, "tablica_p"):
            return
        upit = self.upit_p.get().casefold().strip()
        for item in self.tablica_p.get_children():
            self.tablica_p.delete(item)
        for obj in self.putovanja:
            red = self._red_putovanja(obj)
            if upit and upit not in " ".join(map(str, red)).casefold():
                continue
            self.tablica_p.insert("", "end", values=red)

    @staticmethod
    def _sortiraj(tablica, stupac, obrnuto):
        stavke = [(tablica.set(item, stupac), item) for item in tablica.get_children("")]
        def kljuc(par):
            vrijednost = par[0].strip()
            try:
                return (0, float(vrijednost.replace(",", ".")))
            except ValueError:
                return (1, vrijednost.casefold())
        stavke.sort(key=kljuc, reverse=obrnuto)
        for indeks, (_, item) in enumerate(stavke):
            tablica.move(item, "", indeks)
        tablica.heading(stupac, command=lambda: SortirajPretraziApp._sortiraj(tablica, stupac, not obrnuto))


if __name__ == "__main__":
    root = tk.Tk()
    app = SortirajPretraziApp(root)
    root.mainloop()
