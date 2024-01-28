import json
import tkinter as tk
from tkinter import ttk

class QuickPOS_DB:
    def __init__(self, master):
        self.master = master
        master.title("QuickPOS")
        master.geometry("800x500")  # Устанавливаем размер окна

        center_frame = ttk.Frame(master)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label_title = ttk.Label(center_frame, text="QuickPOS", font=("Arial", 24))
        self.label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.label_name = ttk.Label(center_frame, text="Name:")
        self.label_name.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_name = ttk.Entry(center_frame)
        self.entry_name.grid(row=1, column=1, padx=10, pady=5)

        self.label_price = ttk.Label(center_frame, text="Price:")
        self.label_price.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_price = ttk.Entry(center_frame)
        self.entry_price.grid(row=2, column=1, padx=10, pady=5)

        self.label_barcode = ttk.Label(center_frame, text="Barcode:")
        self.label_barcode.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_barcode = ttk.Entry(center_frame)
        self.entry_barcode.grid(row=3, column=1, padx=10, pady=5)

        self.label_cost_price = ttk.Label(center_frame, text="Buy Price:")
        self.label_cost_price.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_cost_price = ttk.Entry(center_frame)
        self.entry_cost_price.grid(row=4, column=1, padx=10, pady=5)

        self.add_product_button = ttk.Button(center_frame, text="Add to Database", command=self.add_product)
        self.add_product_button.grid(row=5, column=0, columnspan=2, pady=10)

    def add_product(self):
        name = self.entry_name.get()
        price = self.entry_price.get()
        barcode = self.entry_barcode.get()
        cost_price = self.entry_cost_price.get()

        if name and price and barcode and cost_price:
            try:
                price = float(price)
                cost_price = float(cost_price)
                with open('products.json', 'r') as file:
                    products = json.load(file)
                products.append({"barcode": barcode, "name": name, "price": price, "cost_price": cost_price})
                with open('products.json', 'w') as file:
                    json.dump(products, file, indent=2)
                print(f"Продукт {name} успешно добавлен в базу данных.")
            except Exception as e:
                print(f"Ошибка при добавлении продукта: {e}")
        else:
            print("Пожалуйста, заполните все поля.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuickPOS_DB(root)
    root.mainloop()
