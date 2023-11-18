import tkinter as tk
from PIL import Image, ImageTk
import os
import pickle
# Base class for medicines
class Medicine(object):
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
        self.quantity = 0

    # Display details method (to be overridden by derived classes)
    def display_details(self):
        return f"Name: {self.name}\nStock: {self.stock}\nPrice: ${self.price}"

# Derived class representing pharmacy items
class PharmacyItem(Medicine):
    def __init__(self, name, price, stock, description):
        super().__init__(name, price, stock)
        self.description = description

    # Override the display_details method to include additional information
    def display_details(self):
        # Call the base class method
        base_details = super().display_details()
        return f"{base_details}\nDescription: {self.description}"

# Pharmacy Management System class
class PharmacyManagementSystem(object):
    def __init__(self, master):
        self.master = master
        master.title("Pharmacy Management System")

        # Get the directory of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Combine the script directory with the image file names
        menu_image_path = os.path.join(current_directory, "medmenu.jpg")
        charge_image_path = os.path.join(current_directory, "medcharge.jpg")

        # Open the images using the constructed paths
        self.menu_wallpaper_image = Image.open(menu_image_path)
        self.menu_wallpaper_image = self.menu_wallpaper_image.resize((800, 600))
        self.menu_wallpaper_photo = ImageTk.PhotoImage(self.menu_wallpaper_image)

        self.charge_wallpaper_image = Image.open(charge_image_path)
        self.charge_wallpaper_image = self.charge_wallpaper_image.resize((800, 600))
        self.charge_wallpaper_photo = ImageTk.PhotoImage(self.charge_wallpaper_image)

        self.frames = {}
        self.products = {
            'Paracetamol': PharmacyItem('Paracetamol', 10, 10, 'Relieves pain and reduces fever'),
            'Chlorpheniramine': PharmacyItem('Chlorpheniramine', 5, 5, 'Manages upper respiratory allergies'),
            'Semicon': PharmacyItem('Semicon', 15, 15, 'Antiflatulence drug'),
            'Piperazine': PharmacyItem('Piperazine', 8, 20, 'Expels worms from the body'),
            'Betadine': PharmacyItem('Betadine', 12, 25, 'External disinfectant with iodine'),
            'Simethicone': PharmacyItem('Simethicone', 7, 12, 'Relieves bloating and flatulence'),
            'Oral Rehydration Salts': PharmacyItem('Oral Rehydration Salts', 18, 30, 'Compensates for fluid loss'),
            'Dimenhydrinate': PharmacyItem('Dimenhydrinate', 9, 18, 'Prevents nausea and dizziness'),
            'Normal saline solution': PharmacyItem('Normal saline solution', 14, 22, 'Sterile solution for external use'),
            'Calamine Lotion': PharmacyItem('Calamine Lotion', 6, 8, 'Relieves mild skin irritation'),
        }
        self.product_labels_stock = {}
        self.product_labels_charging = {}
        self.total_cost = 0  # Initialize total_cost to 0
        self.order_list = []
        self.load_data()  # Move load_data after initializing products
        self.show_main_menu()

    def load_data(self):
        try:
            with open("pharmacy_data.pkl", "rb") as file:
                saved_data = pickle.load(file)
                saved_products = saved_data.get("products", {})
                saved_order_list = saved_data.get("order_list", [])
                saved_total_cost = saved_data.get("total_cost", 0)

                for product_name, product in self.products.items():
                    # Update product quantities only in the "Product In Stock" GUI
                    if product_name in saved_products:
                        product.stock = saved_products[product_name].stock
                        self.update_product_labels(product)

                # Reset charging-related attributes to zero
                self.order_list = []
                self.total_cost = 0

                # Update the GUI for charging
                for product in saved_order_list:
                    self.add_to_charging(product)

        except FileNotFoundError:
            print("No saved data found. Starting with default data.")


    def save_data(self):
        data_to_save = {
            "products": self.products,
            "order_list": self.order_list,
            "total_cost": self.total_cost,
        }

        with open("pharmacy_data.pkl", "wb") as file:
            pickle.dump(data_to_save, file)


    def show_main_menu(self):
        self.clear_screen()
        frame = tk.Frame(self.master)
        frame.pack()
        self.frames["main_menu"] = frame

        # Use Label to display the menu image as a background for the main menu
        background_label = tk.Label(frame, image=self.menu_wallpaper_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.product_in_stock_button = tk.Button(frame, text="Product In Stock", command=self.show_product_in_stock)
        self.product_in_stock_button.pack()

        self.charging_button = tk.Button(frame, text="Charging", command=self.show_charging)
        self.charging_button.pack()

    
    def show_product_in_stock(self):
        self.clear_screen()
        frame = tk.Frame(self.master)
        frame.pack()
        self.frames["product_in_stock"] = frame

        # Use Label to display the product in stock image as a background
        product_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "medproduct.jpg")
        product_wallpaper_image = Image.open(product_image_path)
        product_wallpaper_image = product_wallpaper_image.resize((800, 600))
        self.product_wallpaper_photo = ImageTk.PhotoImage(product_wallpaper_image)

        background_label = tk.Label(frame, image=self.product_wallpaper_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        back_button = tk.Button(frame, text="Back", command=self.show_main_menu)
        back_button.grid(row=0, column=0)

        for i, (product_name, product) in enumerate(self.products.items()):
            label_text = f"{product.name} - {product.stock} - Cost: ${product.price}"
            label = tk.Label(frame, text=label_text)
            label.grid(row=i + 1, column=0)
            self.product_labels_stock[product.name] = label  # Store label reference

            plus_button = tk.Button(frame, text="+", command=lambda p=product: self.add_stock(p))
            plus_button.grid(row=i + 1, column=1)

            minus_button = tk.Button(frame, text="-", command=lambda p=product: self.subtract_stock(p))
            minus_button.grid(row=i + 1, column=2)

            # Create a button to show details for the specific medicine
            details_button = tk.Button(frame, text=f"Details - {product.name}", command=lambda p=product: self.show_medicine_details(p))
            details_button.grid(row=i + 1, column=3)



    def show_medicine_details(self, product):
        details_window = tk.Toplevel(self.master)
        details_window.title(f"Details - {product.name}")

        # Display details of the selected medicine
        details_label = tk.Label(details_window, text=f"Name: {product.name}\nStock: {product.stock}\nPrice: ${product.price}")
        if product.name == 'Paracetamol':
            additional_info = "Paracetamol can relieve pain from many different causes, such as headaches and pain from osteoarthritis. It is also used to reduce fever."
            additional_info_label = tk.Label(details_window, text=additional_info)
            additional_info_label.pack()
        if product.name == 'Chlorpheniramine':
            additional_info = "Chlorpheniramine is a histamine-H1 receptor antagonist indicated for the management of symptoms associated with upper respiratory allergies."
            additional_info_label = tk.Label(details_window, text=additional_info)
            additional_info_label.pack()
        if product.name == 'Semicon':
            additional_info = "Semicon (Simethicone) is an antiflatulence drug. Simethicone is a non-toxic surface-active substance that is not absorbed by the mucous membranes. It acts as a foam suppressant by removing gases in the stomach and intestine through decreasing the surface tension of gas bubbles."
            additional_info_label = tk.Label(details_window, text=additional_info)
            additional_info_label.pack()
        if product.name == 'Piperazine':
            additional_info = "Piperazine has a mechanism of action that causes paralysis-like symptoms in the worm's muscles. The worms are then expelled from the body through the feces."
            additional_info_label = tk.Label(details_window, text=additional_info)
            additional_info_label.pack()
        if product.name == 'Betadine':
            additional_info = "Betadine is an external disinfectant (Topical Antiseptic) that contains iodine. It is effective in killing bacteria, fungi, viruses, and protozoa."
            additional_info_label = tk.Label(details_window, text=additional_info)
            additional_info_label.pack()
        if product.name == 'Simethicone':
            additional_info = "Simethicone is a medicine used to relieve bloating and flatulence caused by gases in the stomach and intestines, such as hydrogen gas (Hydrogen), methane gas (Methane), etc."
            additional_info_label = tk.Label(details_window, text=additional_info)
            additional_info_label.pack()
        if product.name == 'Oral Rehydration Salts':
            additional_info = "Oral Rehydration Salts (ORS) are used to compensate for fluid loss from vomiting or diarrhea. They are specifically formulated to help restore electrolytes and fluids in the body during periods of dehydration."
            additional_info_label = tk.Label(details_window, text=additional_info)
            additional_info_label.pack()
        if product.name == 'Dimenhydrinate':
            additional_info = "Dimenhydrinate is an anti-allergic drug that has the effect of preventing nausea, vomiting, and dizziness. It is commonly known by its generic name, dimenhydrinate. Dimenhydrinate is used to treat nausea and vomiting associated with various conditions."
            additional_info_label = tk.Label(details_window, text=additional_info)
            additional_info_label.pack()
        if product.name == 'Normal saline solution':
            additional_info = "Normal Saline Solution (NSS) is a sterile solution for external use, clear, and colorless. It is suitable for douching, washing, and general cleaning of all types that can be used with saline. Indications for use include using it as a douche for rinsing the nasal cavity."
            additional_info_label = tk.Label(details_window, text=additional_info)
            additional_info_label.pack()
        if product.name == 'Calamine Lotion':
            additional_info = "Calamine Lotion is an ointment used to relieve mild skin irritation, such as itching, pain, skin discomfort, rashes, allergic rashes to plant toxins, hives, and allergies to chemicals and cosmetics. It is commonly applied topically to soothe and calm the skin."
            additional_info_label = tk.Label(details_window, text=additional_info)
            additional_info_label.pack()
    
    def show_charging(self):
        self.clear_screen()
        frame = tk.Frame(self.master)
        frame.pack()
        self.frames["charging"] = frame

        # Use Label to display the charge image as a background for the charging page
        background_label = tk.Label(frame, image=self.charge_wallpaper_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        back_button = tk.Button(frame, text="Back", command=self.reset_charging_and_show_main_menu)
        back_button.grid(row=0, column=0)

        bill_button = tk.Button(frame, text="Add Bill", command=self.generate_bill)
        bill_button.grid(row=1, column=0, pady=10)  # Adjust the placement if needed

        # Reset quantities to 0 when entering the charging GUI
        for product in self.products.values():
            product.quantity = 0

        # Check if there are items in the charging list before resetting
        if not self.order_list:
            self.order_list = []
            self.total_cost = 0

        for i, (product_name, product) in enumerate(self.products.items()):
            label_text = f"{product.name} - {product.quantity} - Cost: ${product.price}"
            label = tk.Label(frame, text=label_text)
            label.grid(row=i + 2, column=0)  # Adjust the starting row if needed
            self.product_labels_charging[product.name] = label  # Store label reference

            plus_button = tk.Button(frame, text="+", command=lambda p=product: self.add_to_charging(p))
            plus_button.grid(row=i + 2, column=1)

            minus_button = tk.Button(frame, text="-", command=lambda p=product: self.subtract_from_charging(p))
            minus_button.grid(row=i + 2, column=2)


    def reset_charging_and_show_main_menu(self):
        # Reset quantities to 0 when leaving the charging GUI
        for product in self.products.values():
            product.quantity = 0

        # Save data before clearing the screen
        self.save_data()

        # Show the main menu
        self.show_main_menu()

    def generate_bill(self):
        # Update stock in "Product In Stock" GUI before displaying the billing window
        for product in self.order_list:
            self.update_stock_in_product_in_stock(product)

        bill_window = tk.Toplevel(self.master)
        bill_window.title("Bill")
        bill_window.geometry("200x200")

        total_cost_label = tk.Label(bill_window, text=f"Total Cost: ${self.total_cost}")
        total_cost_label.pack()

        for i, product in enumerate(self.order_list):
            label_text = f"{product.name} - {product.quantity} - ${product.price}"
            label = tk.Label(bill_window, text=label_text)
            label.pack()

        # Reset quantities and total cost after generating the bill
        self.order_list = []
        self.total_cost = 0

        # Save data after resetting quantities and total cost
        self.save_data()



    def add_to_charging(self, product):
        if product.stock > 0:
            product.quantity += 1
            product.stock -= 1
            self.update_product_labels(product)
            self.order_list.append(product)
            self.total_cost += product.price
            self.update_stock_in_product_in_stock(product)  # Update stock in "Product In Stock" GUI
            print(f"{product.name} added to charging. Current total cost: {self.total_cost}")
        else:
            print(f"No more {product.name} in stock.")

    def update_stock_in_product_in_stock(self, product):
        # Check if the product is displayed in the "Product In Stock" GUI
        if product.name in self.product_labels_stock:
            # Update the label text to reflect the new stock
            label_text_stock = f"{product.name} - {product.stock} - Cost: ${product.price}"
            self.product_labels_stock[product.name].config(text=label_text_stock)


    def subtract_from_charging(self, product):
        if product.quantity > 0:
            product.quantity -= 1
            product.stock += 1
            self.update_product_labels(product)
            self.update_stock_in_product_in_stock(product)  # Update stock in "Product In Stock" GUI

            if product in self.order_list:
                self.order_list.remove(product)
                self.total_cost -= product.price
            print(f"{product.name} removed from charging. Current total cost: {self.total_cost}")
        else:
            print(f"No {product.name} in charging.")


    def add_stock(self, product):
        if product.name in self.products:
            product.stock += 1
            self.update_product_labels(product)
            print(f"One unit of {product.name} added to stock. Current stock: {product.stock}")
        else:
            print(f"{product.name} not found in stock.")

    # Inside the PharmacyManagementSystem class

    

    def subtract_stock(self, product):
        try:
            if product.name in self.products:
                if product.stock > 0:
                    product.stock -= 1
                    self.update_product_labels(product)
                    print(f"One unit of {product.name} subtracted from stock. Current stock: {product.stock}")
                else:
                    raise ValueError(f"No more {product.name} in stock.")
            else:
                raise KeyError(f"{product.name} not found in stock.")
        except KeyError as e:
            self.show_error_message(f"Error: {e}")
        except ValueError as e:
            self.show_error_message(f"Error: {e}")

    def show_error_message(self, message):
        error_window = tk.Toplevel(self.master)
        error_window.title("Error")
        
        error_label = tk.Label(error_window, text=message)
        error_label.pack()

        ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack()



    def update_product_labels(self, product):
        if product.name in self.product_labels_stock:
            label_text_stock = f"{product.name} - {product.stock} - Cost: ${product.price}"
            self.product_labels_stock[product.name].config(text=label_text_stock)

        if product.name in self.product_labels_charging:
            label_text_charging = f"{product.name} - {product.quantity} - Cost: ${product.price}"
            self.product_labels_charging[product.name].config(text=label_text_charging)

    def clear_screen(self):
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
            else:
                widget.pack_forget()
        self.save_data()

root = tk.Tk()
my_gui = PharmacyManagementSystem(root)
root.mainloop()
