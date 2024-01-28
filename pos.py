import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
from decimal import Decimal

class QuickPOS:
    def __init__(self, master):
        self.master = master
        master.title("QuickPOS")
        master.attributes('-zoomed', True)

        # Создаем фрейм для центрирования
        center_frame = ttk.Frame(master)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label_title = ttk.Label(center_frame, text="QuickPOS", font=("Arial", 24))
        self.label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.label_barcode = ttk.Label(center_frame, text="Barcode:")
        self.label_barcode.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_barcode = ttk.Entry(center_frame)
        self.entry_barcode.grid(row=1, column=1, padx=10, pady=10)
        self.entry_barcode.bind('<Return>', self.scan_product)  # Привязываем функцию к событию нажатия клавиши Enter

        self.product_listbox = tk.Listbox(center_frame, font=("Arial", 16), width=40, height=10)
        self.product_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.total_label = ttk.Label(center_frame, text="Total: 0")
        self.total_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.confirm_button = ttk.Button(center_frame, text="Accept Sale", command=self.confirm_purchase)
        self.confirm_button.grid(row=4, column=0, pady=10, padx=5)

        self.cancel_button = ttk.Button(center_frame, text="Cancel", command=self.cancel_purchase)
        self.cancel_button.grid(row=4, column=1, pady=10, padx=5)

        self.history_button = ttk.Button(center_frame, text="Sale History", command=self.show_sales_history)
        self.history_button.grid(row=5, column=0, columnspan=2, pady=10, padx=5)

        self.total_amount = Decimal('0')
        self.products = []
        self.load_products()

    def load_products(self):
        try:
            with open('products.json', 'r') as file:
                self.products = json.load(file)
        except FileNotFoundError:
            print("Ошибка: файл 'products.json' не найден.")
        except json.JSONDecodeError:
            print("Ошибка: не удалось прочитать данные из файла 'products.json'.")
        else:
            print("Данные из файла 'products.json' успешно загружены.")

    def save_products(self):
        try:
            with open('products.json', 'w') as file:
                json.dump(self.products, file, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    def scan_product(self, event=None):
        barcode = self.entry_barcode.get()
        for product in self.products:
            if product.get('barcode') == barcode:
                self.product_listbox.insert(tk.END, f"{product.get('name')} - Price: {product.get('price')}AZN")
                self.total_amount += Decimal(str(product.get('price')))
                self.total_label.config(text=f"Total: {self.total_amount}")
                self.entry_barcode.delete(0, 'end')
                break
        else:
            self.entry_barcode.delete(0, 'end')

    def confirm_purchase(self):
        purchase_data = {
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_amount": str(self.total_amount),
            "purchased_items": [self.product_listbox.get(idx) for idx in range(self.product_listbox.size())]
        }
        with open('history.json', 'a') as file:
            json.dump(purchase_data, file, indent=2)
            file.write('\n')

        self.product_listbox.delete(0, tk.END)
        self.total_amount = Decimal('0')
        self.total_label.config(text="Total: 0")

    def cancel_purchase(self):
        self.product_listbox.delete(0, tk.END)
        self.total_amount = Decimal('0')
        self.total_label.config(text="Total: 0")

    def show_sales_history(self):
        try:
            with open('history.json', 'r') as file:
                history_data = json.load(file)
                sorted_history = sorted(history_data, key=lambda x: datetime.strptime(x['date_time'], "%Y-%m-%d %H:%M:%S"))
                for item in sorted_history:
                    print(f"Date/Time: {item['date_time']}, Total: {item['total_amount']}, Porducts: {item['purchased_items']}")
        except FileNotFoundError:
            print("Ошибка: файл 'history.json' не найден.")
        except json.JSONDecodeError:
            print("Ошибка: не удалось прочитать данные из файла 'history.json'.")
        else:
            print("История продаж успешно загружена.")

    def __del__(self):
        self.save_products()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuickPOS(root)
    root.mainloop()
