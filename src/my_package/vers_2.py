import tkinter as tk
from tkinter import ttk, messagebox
def calculate_sepsis(infection, sofa, pao2, vent, vaso, lact, map_low, plt, inr, gcs, bilirubin, creat, age):
    phoenix = 0
    if vent and pao2 < 100:
        phoenix += 3
    elif vent and pao2 <= 200:
        phoenix += 2
    elif pao2 < 400:
        phoenix += 1
    phoenix += min(vaso, 2)
    if lact >= 5: phoenix += 2 if lact >= 11 else 1
    if map_low: phoenix += 1
    if plt < 100: phoenix += 1
    if inr > 1.3: phoenix += 1
    if gcs <= 10: phoenix += 2 if gcs <= 6 else 1
    if bilirubin > 2: phoenix += 1
    if creat > 1.5: phoenix += 2 if creat > 2.5 else 1

    sepsis = infection and (sofa >= 2 or phoenix >= 2)
    shock = sepsis and (
                (vaso > 0 and lact > 2) or (min(vaso, 2) + (1 if lact >= 5 else 0) + (1 if map_low else 0) >= 2))

    if shock:
        severity = ("КРИТИЧЕСКАЯ","ОРИТ немедленно!")
    elif phoenix >= 10 or lact > 4:
        severity = ("ТЯЖЁЛАЯ", "ОРИТ срочно!")
    elif phoenix >= 6 or sofa >= 2:
        severity = ("СРЕДНЯЯ","Госпитализация")
    elif phoenix >= 2:
        severity = ("ЛЁГКАЯ","Амбулаторно")
    else:
        severity = ("МИНИМАЛЬНАЯ","Наблюдение")
    risk = 5
    if phoenix <= 2:
        risk = 5
    elif phoenix <= 5:
        risk = 12
    elif phoenix <= 8:
        risk = 25
    elif phoenix <= 12:
        risk = 45
    else:
        risk = 65
    if shock: risk += 30
    if lact > 4: risk += 15
    if gcs <= 8: risk += 15
    if plt < 50: risk += 15
    if vaso >= 2: risk += 20
    age_mult = {"<40": 0.6, "40-60": 1.0, "60-80": 1.5, ">80": 2.2}
    risk = min(int(risk * age_mult.get(age, 1.0)), 95)
    return phoenix, sepsis, shock, severity, risk

class SepsisApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Сепсис")
        self.root.geometry("550x700")
        self.root.configure(bg='#f0f0f0')

        tk.Label(self.root, text="ДИАГНОСТИКА СЕПСИСА",
                 font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#8B0000').pack(pady=10)
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(padx=20, fill="both", expand=True)
        fields = [
            ("Инфекция", "infection", "check", True),
            ("ΔSOFA", "sofa", "entry", "0"),
            ("PaO₂/FiO₂", "pao2", "entry", "400"),
            ("ИВЛ", "vent", "check", False),
            ("Вазопрессоры (кол-во)", "vaso", "entry", "0"),
            ("Лактат", "lact", "entry", "2.0"),
            ("Низкое MAP", "map_low", "check", False),
            ("Тромбоциты", "plt", "entry", "150"),
            ("INR", "inr", "entry", "1.0"),
            ("GCS (3-15)", "gcs", "entry", "15"),
            ("Билирубин", "bili", "entry", "0.5"),
            ("Креатинин", "creat", "entry", "0.8"),
        ]

        self.vars = {}
        row = 0
        for label, key, typ, *default in fields:
            tk.Label(frame, text=label, bg='#f0f0f0', width=20, anchor="w").grid(row=row, column=0, pady=3)

            if typ == "check":
                var = tk.BooleanVar(value=default[0])
                tk.Checkbutton(frame, variable=var, bg='#f0f0f0').grid(row=row, column=1, sticky="w")
                self.vars[key] = var
            else:
                var = tk.StringVar(value=default[0])
                tk.Entry(frame, textvariable=var, width=10).grid(row=row, column=1, sticky="w")
                self.vars[key] = var
            row += 1
        tk.Label(frame, text="Возраст", bg='#f0f0f0').grid(row=row, column=0, pady=3)
        self.age = ttk.Combobox(frame, values=["<40", "40-60", "60-80", ">80"], width=8)
        self.age.set("40-60")
        self.age.grid(row=row, column=1, sticky="w")

        tk.Button(frame, text="РАССЧИТАТЬ", command=self.calc,bg='#8B0000', fg='white', font=('Arial', 10, 'bold'),padx=20, pady=5).grid(row=row + 1, column=0, columnspan=2, pady=15)
        result_frame = tk.LabelFrame(self.root, text="РЕЗУЛЬТАТ", font=('Arial', 10, 'bold'))
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.result = tk.Text(result_frame, height=15, font=('Consolas', 10), wrap=tk.WORD)
        self.result.pack(fill="both", expand=True, padx=5, pady=5)
        self.status = tk.Label(self.root, text="Готов", relief="sunken", anchor="w", bg='#f0f0f0')
        self.status.pack(fill="x", side="bottom")

    def calc(self):
        try:
            infection = self.vars["infection"].get()
            sofa = float(self.vars["sofa"].get())
            pao2 = float(self.vars["pao2"].get())
            vent = self.vars["vent"].get()
            vaso = int(self.vars["vaso"].get())
            lact = float(self.vars["lact"].get())
            map_low = self.vars["map_low"].get()
            plt = float(self.vars["plt"].get())
            inr = float(self.vars["inr"].get())
            gcs = int(self.vars["gcs"].get())
            bili = float(self.vars["bili"].get())
            creat = float(self.vars["creat"].get())
            age = self.age.get()

            phoenix, sepsis, shock, severity, risk = calculate_sepsis(
                infection, sofa, pao2, vent, vaso, lact, map_low, plt, inr, gcs, bili, creat, age)

            result = f"""
Phoenix Score: {phoenix}/17
ДИАГНОЗ:
   Сепсис: {"ДА" if sepsis else "НЕТ"}
   Шок: {"ДА" if shock else "НЕТ"}

СТЕПЕНЬ ТЯЖЕСТИ:
   f"{severity[0]} - {severity[1]}"
РИСК ЛЕТАЛЬНОСТИ: {risk}%
   {"НИЗКИЙ" if risk <= 25 else "СРЕДНИЙ" if risk <= 50 else "ВЫСОКИЙ"}
РЕКОМЕНДАЦИИ:"""
            if shock:
                result += """
   !!Норадреналин + антибиотики
   !!ОРИТ НЕМЕДЛЕННО!"""
            elif sepsis:
                result += """
   !!Антибиотики широкого спектра
   !!Госпитализация"""
            else:
                result += """
   !!Наблюдение
   !!Повторная оценка через 6-12ч"""
            if lact > 4:
                result += "\nКРИТИЧЕСКИЙ ЛАКТАТ!"

            self.result.delete(1.0, tk.END)
            self.result.insert(1.0, result)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проверьте ввод данных\n{e}")
    def run(self):
        self.root.mainloop()
if __name__ == "__main__":
    app = SepsisApp()
    app.run()