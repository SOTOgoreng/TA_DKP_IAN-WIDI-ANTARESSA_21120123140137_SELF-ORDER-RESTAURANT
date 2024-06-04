import tkinter as tk
from tkinter import messagebox


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_price(self):
        raise NotImplementedError("Subclasses should implement this method")

class FoodItem(MenuItem):
    def get_price(self):
        return self.price

class DrinkItem(MenuItem):
    def get_price(self):
        return self.price

class FoodOrderApp:
    def __init__(self, dasar):
        self.dasar = dasar
        self.dasar.title("Menu Makanan")
        self.dasar.configure(bg="#00008b")

        self.menu = {
            "Nasi Goreng": FoodItem("Nasi Goreng", 15000),
            "Mie Goreng": FoodItem("Mie Goreng", 13000),
            "Ayam Goreng": FoodItem("Ayam Goreng", 20000),
            "Sate Ayam": FoodItem("Sate Ayam", 25000),
            "Teh Manis": DrinkItem("Teh Manis", 5000),
            "Es Jeruk": DrinkItem("Es Jeruk", 7000)
        }

        self.__create_widgets()
        self.__order_history = []

    def __create_widgets(self):
        title1 = tk.Label(self.dasar, text= "Warung Ahuy", font=("Arial", 20, "bold"), bg="#f0f0f0")
        title1.pack(pady=10)
        title2 = tk.Label(self.dasar, text="Pilih Menu", font=("Arial", 18, "bold"), bg="#f0f0f0")
        title2.pack(pady=10)

        menu_frame = tk.Frame(self.dasar, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        menu_frame.pack(pady=10, padx=10, fill=tk.X)

        self.menu_vars = {}
        for item, menu_item in self.menu.items():
            item_frame = tk.Frame(menu_frame, bg="#ffffff")
            item_frame.pack(anchor=tk.W, pady=5)

            item_label = tk.Label(item_frame, text=f"{item} - Rp {menu_item.get_price()}", font=("Arial", 12, "bold"), bg="#ffffff")
            item_label.pack(side=tk.LEFT, padx=10)

            var = tk.StringVar(value='0')
            spin = tk.Spinbox(item_frame, from_=0, to=100, width=3, textvariable=var, font=("Arial", 12))
            spin.pack(side=tk.RIGHT, padx=10)
            self.menu_vars[item] = var

        table_number_frame = tk.Frame(self.dasar, bg="#f0f0f0")
        table_number_frame.pack(pady=10)

        tk.Label(table_number_frame, text="Nomor Meja:", font=("Arial", 14), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.table_number_var = tk.StringVar()
        vcmd = (self.dasar.register(self.validate_table_number), '%P')
        tk.Entry(table_number_frame, textvariable=self.table_number_var, font=("Arial", 12), validate='key', validatecommand=vcmd).pack(side=tk.RIGHT, padx=5)

        button_frame = tk.Frame(self.dasar, bg="#f0f0f0")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Pesan dan Proses", command=self.calculate_and_process_order, font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Lihat Riwayat", command=self.show_history, font=("Arial", 12), bg="#ff0000", fg="white").pack(side=tk.RIGHT, padx=10)

        self.total_label = tk.Label(self.dasar, text="Total: Rp 0", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.total_label.pack(pady=10)

    def validate_table_number(self, P):
        return P.isdigit() or P == ""

    def calculate_and_process_order(self):
        total = 0
        order = {}
        for item, var in self.menu_vars.items():
            count = int(var.get())
            if count > 0:
                price = self.menu[item].get_price()
                total += price * count
                order[item] = (count, price)

        table_number = self.table_number_var.get().strip()
        if not table_number:
            messagebox.showwarning("No Meja Kosong", "Silakan masukkan nomor meja Anda.")
            return

        if total == 0:
            messagebox.showwarning("Pesanan Kosong", "Anda belum memilih menu.")
        else:
            self.total_label.config(text=f"Total: Rp {total}")
            detailed_order = "\n".join([f"{item}: {count} x Rp {price} = Rp {count * price}" for item, (count, price) in order.items()])
            messagebox.showinfo("Silahkan Pergi Kekasir, Total Pesanan Anda", f"Total yang harus dibayar: Rp {total}\nNomor Meja: {table_number}\n\nRincian Pesanan:\n{detailed_order}")
            self.__order_history.append((table_number, total, order))
            self.__clear_current_order()

    def __clear_current_order(self):
        for var in self.menu_vars.values():
            var.set('0')
        self.table_number_var.set('')
        self.total_label.config(text="Total:Rp 0")
    def show_history(self):
        if not self.__order_history:
            messagebox.showinfo("Riwayat Kosong", "Belum ada order yang diproses.")
            return

        history_message = ""
        for index, (table_number, total, order) in enumerate(self.__order_history, start=1):
            history_message += f"Order {index} (Meja {table_number}):\n"
            for item, (count, price) in order.items():
                history_message += f"  {item}: {count} x Rp {price} = Rp {count * price}\n"
            history_message += f"Total: Rp {total}\n\n"

        messagebox.showinfo("Riwayat Order", history_message)

    def set_menu(self, new_menu):
        self.menu = new_menu
        self.__create_widgets()

    def get_menu(self):
        return self.menu

if __name__ == "__main__":
    dasar = tk.Tk()
    app = FoodOrderApp(dasar)
    dasar.mainloop()
