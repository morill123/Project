import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, simpledialog, Toplevel, Label
import requests

class ProductManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Management System")
        self.root.geometry('700x500')  #
        self.font = tkfont.Font(family="Helvetica", size=14)
        self.create_login_frame()
        self.inventory_update_job = None
        self.product_update_job = None

    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=100, pady=100)

        tk.Label(self.login_frame, text="Username:", font=self.font).grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame, font=self.font, width=30)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password:", font=self.font).grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show='*', font=self.font, width=30)
        self.password_entry.grid(row=1, column=1)

        login_button = tk.Button(self.login_frame, text="Log in", font=self.font, command=self.login)
        login_button.grid(row=2, column=1, sticky=tk.W+tk.E)

    def clear_frame(self):
        # Cancel any existing jobs for updating product or inventory
        if self.product_update_job is not None:
            self.root.after_cancel(self.product_update_job)
            self.product_update_job = None
        if self.inventory_update_job is not None:
            self.root.after_cancel(self.inventory_update_job)
            self.inventory_update_job = None

        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Send a login request to the proxy server
        data = {'username': username, 'password': password}
        try:
            response = requests.post('http://localhost:12345/login', json=data)
            login_result = response.json()  # Parse the response content in JSON format

            if login_result.get('success', False):
                print("Login successful!")
                self.clear_frame()
                self.create_main_menu()
            else:
                print("Login failed!")
                messagebox.showerror("Error", login_result.get('message', 'Wrong username or password'))
        except requests.RequestException as e:
            print(f"Error: {e}")


    def create_main_menu(self):
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack(padx=10, pady=10)

        product_management_button = tk.Button(self.main_menu_frame, text="Product Management", width=30, height=5,command=self.create_product_management)
        product_management_button.grid(row=0, column=0, padx=5, pady=5)

        order_management_button = tk.Button(self.main_menu_frame, text="Order Management", width=30, height=5,command=self.create_order_management)
        order_management_button.grid(row=1, column=0, padx=5, pady=5)

        inventory_management_button = tk.Button(self.main_menu_frame, text="Inventory Management", width=30, height=5,command=self.create_inventory_management)
        inventory_management_button.grid(row=2, column=0, padx=5, pady=5)

        exit_button = tk.Button(self.main_menu_frame, text="Exit", width=30, height=5,command=lambda: self.close_gui(self.root))
        exit_button.grid(row=3, column=0, padx=5, pady=5)

    def close_gui(self, root):
        root.destroy()

    def create_product_management(self):

        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        search_product_button = tk.Button(frame, text="Search Product", width=30, height=4, command=self.show_search_product_frame)
        search_product_button.grid(row=0, column=0, padx=5, pady=5)

        view_all_products_button = tk.Button(frame, text="View All Products", width=30, height=4, command=self.view_all_products)
        view_all_products_button.grid(row=1, column=0, padx=5, pady=5)

        add_product_button = tk.Button(frame, text="Add Product", width=30, height=4, command=self.add_product)
        add_product_button.grid(row=2, column=0, padx=5, pady=5)

        delete_product_button = tk.Button(frame, text="Delete Product", width=30, height=4, command=self.delete_product)
        delete_product_button.grid(row=3, column=0, padx=5, pady=5)

        return_button = tk.Button(frame, text="Return", width=30, height=4,
                                  command=lambda: [self.clear_frame(), self.create_main_menu()])
        return_button.grid(row=4, column=0, padx=5, pady=5)

    def add_product(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Create entry fields for product details

        tk.Label(frame, text="Name:", font=self.font).grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(frame, font=self.font, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Price:", font=self.font).grid(row=1, column=0, padx=5, pady=5)
        price_entry = tk.Entry(frame, font=self.font, width=30)
        price_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Quantity:", font=self.font).grid(row=2, column=0, padx=5, pady=5)
        quantity_entry = tk.Entry(frame, font=self.font, width=30)
        quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Supplier_id:", font=self.font).grid(row=3, column=0, padx=5, pady=5)
        supplier_entry = tk.Entry(frame, font=self.font, width=30)
        supplier_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Region_id:", font=self.font).grid(row=4, column=0, padx=5, pady=5)
        region_entry = tk.Entry(frame, font=self.font, width=30)
        region_entry.grid(row=4, column=1, padx=5, pady=5)

        # Add button to add the product
        add_button = tk.Button(frame, text="Add Product", font=self.font,
                               command=lambda: self.submit_product(name_entry.get(), price_entry.get(),
                                                                   quantity_entry.get(), supplier_entry.get(),
                                                                   region_entry.get()))
        add_button.grid(row=5, columnspan=2, padx=5, pady=5)

        # Return button
        return_button = tk.Button(frame, text="Return", font=self.font,
                                  command=lambda: [self.clear_frame(), self.create_product_management()])
        return_button.grid(row=6, columnspan=2, padx=5, pady=5)

    def submit_product(self, name, price, quantity, supplier_id, region_id):
        # Send a POST request to add the product
        data = {
            "name": name,
            "price": float(price),
            "quantity": int(quantity),
            "supplier_id": int(supplier_id),
            "region_id": int(region_id)}
        response = requests.post("http://localhost:12345/products", json=data)

        if response.status_code == 201:
            self.add_success = True
            messagebox.showinfo("Success", "Product added successfully")

        else:
            messagebox.showerror("Error", "Failed to add product")

    def refresh_product(self):
        if self.results_text.winfo_exists():
            response = requests.get("http://localhost:12345/products/all")
            self.results_text.delete('1.0', tk.END)
            if response.status_code == 200:
                products = response.json()
                for product in products:
                    line = f"Product ID: {product['id']}, Name: {product['name']}, Price: {product['price']}\n"
                    self.results_text.insert(tk.END, line)
                # Cancel the existing job first if it exists
                if self.product_update_job is not None:
                    self.root.after_cancel(self.product_update_job)
                self.product_update_job = self.root.after(10000, self.refresh_product)
            else:
                messagebox.showerror("Error", "Failed to retrieve products")
        else:
            if self.product_update_job is not None:
                self.root.after_cancel(self.product_update_job)
                self.product_update_job = None


    def delete_product(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Create entry field for product ID
        tk.Label(frame, text="Product ID:", font=self.font).grid(row=0, column=0, padx=5, pady=5)
        product_id_entry = tk.Entry(frame, font=self.font, width=30)
        product_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Add button to delete the product
        delete_button = tk.Button(frame, text="Delete Product", font=self.font,
                                  command=lambda: self.submit_delete_product(product_id_entry.get()))
        delete_button.grid(row=1, columnspan=2, padx=5, pady=5)

        # Return button
        return_button = tk.Button(frame, text="Return", font=self.font,
                                  command=lambda: [self.clear_frame(), self.create_product_management()])
        return_button.grid(row=2, columnspan=2, padx=5, pady=5)

        # Text widget to display all products
        self.results_text = tk.Text(self.root, height=15)
        self.results_text.pack(padx=10, pady=10, fill='both', expand=True)

        self.refresh_product()

    def submit_delete_product(self, product_id):
        # Send a DELETE request to delete the product
        response = requests.delete(f"http://localhost:12345/products/{product_id}")

        if response.status_code == 200:
            self.delete_success = True
            messagebox.showinfo("Success", "Product deleted successfully")
            self.delete_product()
        elif response.status_code == 401:
            messagebox.showerror("Error", "There's no product with id " + product_id);
        else:
            messagebox.showerror("Error", "Failed to delete product")

    def clear_search_results(self):
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()

    def search_product(self):
        # Clear the current results
        self.results_text.delete('1.0', tk.END)

        product_id = self.product_id_entry.get()
        if product_id:
            response = requests.get(f"http://localhost:12345/products/{product_id}")
            if response.status_code == 200:
                product = response.json()
                # Display product details in the text widget
                self.display_product_details_in_text(product)
            elif response.status_code == 404:
                messagebox.showerror("Error", "Product not found")
            else:
                messagebox.showerror("Error", "Failed to retrieve product details")
        else:
            messagebox.showinfo("Search Error", "Please enter a Product ID to search.")

    def display_product_details_in_text(self, product):
        details = f"Product Name: {product['name']}\n" \
                  f"Price: ${product['price']}\n" \
                  f"Quantity: {product['quantity']}\n" \
                  f"Supplier ID: {product['supplierid']}\n" \
                  f"Region ID: {product['regionid']}\n"
        self.results_text.insert(tk.END, details)

    def display_product_details(self, product):
        details_frame = tk.Frame(self.search_results_frame)
        details_frame.pack(fill='x', pady=20)
        details_font = ('Helvetica', 14)
        tk.Label(details_frame, text="Product Name: " + product['name'], font=details_font).pack()
        tk.Label(details_frame, text="Price: $" + str(product['price']), font=details_font).pack()
        tk.Label(details_frame, text="Quantity: " + str(product['quantity']), font=details_font).pack()
        tk.Label(details_frame, text="Supplier ID: " + str(product['supplierid']), font=details_font).pack()
        tk.Label(details_frame, text="Region ID: " + str(product['regionid']), font=details_font).pack()

    def show_search_product_frame(self):
        self.clear_frame()
        search_frame = tk.Frame(self.root)
        search_frame.pack(padx=10, pady=10, fill='x')

        # Entry label and entry field for product ID
        tk.Label(search_frame, text="Enter Product ID:", font=self.font).grid(row=0, column=0, padx=5, pady=5,
                                                                              sticky='e')
        self.product_id_entry = tk.Entry(search_frame, font=self.font)
        self.product_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        # Search button
        search_button = tk.Button(search_frame, text="Search", font=self.font, command=self.search_product)
        search_button.grid(row=0, column=2, padx=5, pady=5)

        # Return button
        return_button = tk.Button(search_frame, text="Return", font=self.font, command=self.create_product_management)
        return_button.grid(row=0, column=3, padx=5, pady=5)

        # Set up the frame for results display with a scrollbar
        results_frame = tk.Frame(self.root)
        results_frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.results_text = tk.Text(results_frame, height=15)
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_text['yscrollcommand'] = scrollbar.set


    def view_all_products(self):
        self.clear_frame()
        self.isdelete = False
        # 将请求发送到代理服务器
        response = requests.get("http://localhost:12345/products/all")
        if response.status_code == 200:
            products = response.json()
            if products:
                self.display_all_products(products)
            else:
                messagebox.showinfo("Info", "No products found")
                self.create_product_management()
        else:
            messagebox.showerror("Error", "Failed to retrieve products")
            self.create_product_management()

    def display_all_products(self, products):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        Label(frame, text="All Products", font=('Helvetica', 18, 'bold')).grid(row=0, columnspan=4)
        headers = ["Product ID", "Name", "Price", "Quantity", "Supplier ID", "Region ID"]
        for i, header in enumerate(headers):
            Label(frame, text=header, font=('Helvetica', 16, 'bold')).grid(row=1, column=i)

        for index, product in enumerate(products):
            Label(frame, text=product['id'], font=('Helvetica', 14)).grid(row=index + 2, column=0)
            Label(frame, text=product['name'], font=('Helvetica', 14)).grid(row=index + 2, column=1)
            Label(frame, text=f"${product['price']}", font=('Helvetica', 14)).grid(row=index + 2, column=2)
            Label(frame, text=product['quantity'], font=('Helvetica', 14)).grid(row=index + 2, column=3)
            Label(frame, text=product['supplierid'], font=('Helvetica', 14)).grid(row=index + 2, column=4)
            Label(frame, text=product['regionid'], font=('Helvetica', 14)).grid(row=index + 2, column=5)

        if (self.isdelete == False):
            return_button = tk.Button(frame, text="Return", width=20, height=2,
                                      command=lambda: [self.clear_frame(), self.create_product_management()])
            return_button.grid(row=len(products) + 3, columnspan=6)

    def create_order_management(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        search_order_button = tk.Button(frame, text="Search Order", width=30, height=5, command=self.create_order_place)
        search_order_button.grid(row=0, column=0, padx=5, pady=5)

        view_all_orders_button = tk.Button(frame, text="View All Orders", width=30, height=5,
                                           command=self.view_all_orders)
        view_all_orders_button.grid(row=1, column=0, padx=5, pady=5)

        edit_order_button = tk.Button(frame, text="Edit Order", width=30, height=5, command=self.edit_order)
        edit_order_button.grid(row=2, column=0, padx=5, pady=5)

        return_button = tk.Button(frame, text="Return", width=30, height=5,
                                  command=lambda: [self.clear_frame(), self.create_main_menu()])
        return_button.grid(row=3, column=0, padx=5, pady=5)

    def view_all_orders(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        self.root.geometry('800x500')
        frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.orders_text = tk.Text(frame, wrap='word', height=30)
        self.orders_text.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(frame, command=self.orders_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.orders_text['yscrollcommand'] = scrollbar.set

        self.refresh_all_orders()

        return_button = tk.Button(frame, text="Return",
                                  command=lambda: [self.clear_frame(), self.create_order_management()])
        return_button.pack(pady=10)

    def refresh_all_orders(self):
        response = requests.get("http://localhost:12345/orders/all")
        if response.status_code == 200:
            orders = response.json()
            if self.orders_text.winfo_exists():
                self.orders_text.delete('1.0', tk.END)
                if orders:
                    self.display_all_orders(orders)
                else:
                    self.orders_text.insert(tk.END, "No orders found")
            else:
                return
        else:
            if self.orders_text.winfo_exists():
                self.orders_text.insert(tk.END, "Failed to retrieve orders")
            else:
                return

        self.root.after(5000, self.refresh_all_orders)

    def display_all_orders(self, orders):
        self.orders_text.delete('1.0', tk.END)
        self.orders_text.insert(tk.END, "All Orders:\n\n")

        # Headers
        header_format = "{:<10} {:<20} {:<20} {:<30} {:<20}\n"
        headers = header_format.format("Order ID", "Customer Name", "Region Name", "Date", "Status")
        self.orders_text.insert(tk.END, headers + "\n")

        # Display each order
        for order in orders:
            order_details = header_format.format(
                order['id'],
                order['customername'],
                order['regionname'],
                order['date'],
                order['status']
            )
            self.orders_text.insert(tk.END, order_details + "\n")

    def return_to_main_menu(self):
        self.clear_frame()
        self.create_main_menu()

    def create_order_place(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill='both', expand=True)

        search_frame = tk.Frame(frame)
        search_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        tk.Label(search_frame, text="Order ID:", font=('Arial', 12)).grid(row=0, column=0, sticky="w")
        order_id_entry = tk.Entry(search_frame, font=('Arial', 12))
        order_id_entry.grid(row=0, column=1, sticky="w")

        search_button = tk.Button(search_frame, text="Search Order",
                                  command=lambda: self.search_order(order_id_entry.get()))
        search_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        status_frame = tk.Frame(frame)
        status_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        new_status_label = tk.Label(status_frame, text="New Status:", font=('Arial', 12))
        new_status_label.grid(row=0, column=0, sticky="w")

        new_status_entry = tk.Entry(status_frame, font=('Arial', 12))
        new_status_entry.grid(row=0, column=1, sticky="w")

        update_status_button = tk.Button(status_frame, text="Update Order Status",
                                         command=lambda: self.update_order_status(order_id_entry.get(),
                                                                                  new_status_entry.get()))
        update_status_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        return_button = tk.Button(status_frame, text="Return", command=self.create_order_management)
        return_button.grid(row=0, column=3, padx=5, pady=10, sticky="w")

        results_frame = tk.Frame(frame)
        results_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.results_text = tk.Text(results_frame, height=15, wrap='word')
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_text['yscrollcommand'] = scrollbar.set

    def search_and_refresh_order(self):
        # Saves the currently entered order ID
        self.current_order_id = self.order_id_entry.get()
        self.search_order(self.current_order_id)
        self.refresh_order()

    def refresh_order(self):
        if self.results_text.winfo_exists():
            self.search_order(self.current_order_id)
            self.root.after(10000, self.refresh_order)
        else:
            # If the results_text component is destroyed, cancel the timed task
            if self.order_update_job is not None:
                self.root.after_cancel(self.order_update_job)
                self.order_update_job = None

    def search_order(self, order_id):
        if order_id:
            response = requests.get(f"http://localhost:12345/orders/{order_id}")
            if response.status_code == 200:
                order = response.json()
                if order:
                    self.display_order_details(order)
                else:
                    messagebox.showinfo("Notice", "No order found with this ID")
            else:
                messagebox.showerror("Error", "Failed to retrieve order")
        else:
            messagebox.showinfo("Notice", "Please enter an Order ID")

    def display_order_details(self, order):
        self.results_text.delete('1.0', tk.END)

        details = f"Order ID: {order.get('id')}\nCustomer Name: {order.get('customername')}\nRegion: {order.get('regionname')}\nStatus: {order.get('status')}\n"

        self.results_text.insert(tk.END, details)

    def update_order_status(self, order_id, new_status):
        if order_id and new_status:
            response = requests.put(f"http://localhost:12345/orders/{order_id}/status", json={"status": new_status})
            if response.status_code == 200:
                messagebox.showinfo("Success", "Order status updated successfully")
                self.create_order_management()
            else:
                messagebox.showerror("Error", "Failed to update order status: " + response.text)
        else:
            if not order_id:
                messagebox.showerror("Error", "Order ID is required")
            if not new_status:
                messagebox.showerror("Error", "New status is required")

    def edit_order(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Section to update order status
        tk.Label(frame, text="Order ID:", font=self.font).grid(row=0, column=0)
        order_id_entry = tk.Entry(frame, font=self.font)
        order_id_entry.grid(row=0, column=1)

        tk.Label(frame, text="New Status:", font=self.font).grid(row=1, column=0)
        new_status_entry = tk.Entry(frame, font=self.font)
        new_status_entry.grid(row=1, column=1)

        update_button = tk.Button(frame, text="Update Order Status",
                                  command=lambda: self.update_order_status(order_id_entry.get(),
                                                                           new_status_entry.get()))
        update_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        delete_button = tk.Button(frame, text="Delete Order", command=lambda: self.delete_order(order_id_entry.get()))
        delete_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(frame, text="Customer ID:", font=self.font).grid(row=4, column=0)
        customer_id_entry = tk.Entry(frame, font=self.font)
        customer_id_entry.grid(row=4, column=1)

        tk.Label(frame, text="Region ID:", font=self.font).grid(row=5, column=0)
        region_id_entry = tk.Entry(frame, font=self.font)
        region_id_entry.grid(row=5, column=1)

        tk.Label(frame, text="Order Date (YYYY-MM-DD):", font=self.font).grid(row=6, column=0)
        order_date_entry = tk.Entry(frame, font=self.font)
        order_date_entry.grid(row=6, column=1)

        add_button = tk.Button(frame, text="Add New Order",
                               command=lambda: self.add_order(customer_id_entry.get(), region_id_entry.get(),
                                                              order_date_entry.get()))
        add_button.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        return_button = tk.Button(frame, text="Return", command=self.create_order_management)
        return_button.grid(row=8, column=1, padx=5, pady=10, sticky="ew")

    def update_order_status(self, order_id, new_status):
        if order_id and new_status:
            response = requests.put(f"http://localhost:12345/orders/{order_id}/status", json={"status": new_status})
            if response.status_code == 200:
                messagebox.showinfo("Success", "Order status updated successfully")
            else:
                messagebox.showerror("Error", response.json().get("error", "Failed to update order status"))
        else:
            messagebox.showerror("Error", "Order ID and new status are required")

    def delete_order(self, order_id):
        if order_id:
            response = requests.delete(f"http://localhost:12345/orders/{order_id}")
            if response.status_code == 200:
                # If deletion was successful, inform the user.
                messagebox.showinfo("Success", "Order deleted successfully")
            elif response.status_code == 404:
                # If the server responds with a 404 status, it means the order ID was not found.
                messagebox.showerror("Error", "No order found with the given ID")
            else:
                error_message = response.json().get('error', 'Unknown error occurred while trying to delete the order')
                messagebox.showerror("Error", error_message)
        else:
            messagebox.showerror("Error", "Order ID is required to delete an order.")

    def add_order(self, customer_id, region_id, date):
        if customer_id and region_id and date:
            data = {'customer_id': customer_id, 'region_id': region_id, 'date': date}
            response = requests.post("http://localhost:5001/orders", json=data)
            if response.status_code == 201:
                messagebox.showinfo("Success", "Order added successfully")
            else:
                messagebox.showerror("Error", "Failed to add order.")
        else:
            messagebox.showerror("Error", "All fields are required")

    def display_order_edit_form(self, order):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        Label(frame, text="Edit Order Status", font=self.font).grid(row=0, column=0, padx=10, pady=5)
        status_entry = tk.Entry(frame, font=self.font)
        status_entry.insert(0, order['status'])
        status_entry.grid(row=0, column=1, padx=10, pady=5)

        update_button = tk.Button(frame, text="Update Order",
                                  command=lambda: self.update_order(order['id'], status_entry.get()))
        update_button.grid(row=1, column=1, padx=10, pady=20)

    def update_order(self, order_id, status):
        response = requests.put(f"http://localhost:12345/orders/{order_id}", json={"status": status})
        if response.status_code == 200:
            messagebox.showinfo("Success", "Order updated successfully")
        else:
            messagebox.showerror("Error", "Failed to update order")

    def create_inventory_management(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        search_inventory_button = tk.Button(frame, text="Search Inventory", width=30, height=5, command=self.search_inventory)
        search_inventory_button.grid(row=0, column=0, padx=5, pady=5)

        view_all_inventory_button = tk.Button(frame, text="View All Inventorys", width=30, height=5,command=self.view_all_inventory)
        view_all_inventory_button.grid(row=1, column=0, padx=5, pady=5)

        edit_inventory_button = tk.Button(frame, text="Edit Inventory", width=30, height=5, command=self.edit_inventory)
        edit_inventory_button.grid(row=2, column=0, padx=5, pady=5)

        return_button = tk.Button(frame, text="Return", width=30, height=5,command=lambda: [self.clear_frame(), self.create_main_menu()])
        return_button.grid(row=3, column=0, padx=5, pady=5)

    #This method now holds a frame of search results as a member variable of the class
    def search_inventory(self):
        self.clear_frame()
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10, fill='x')

        tk.Label(input_frame, text="Enter Inventory ID:").grid(row=0, column=0)
        search_entry = tk.Entry(input_frame)
        search_entry.grid(row=0, column=1)

        search_button = tk.Button(input_frame, text="Search",command = lambda: self.validate_and_search(search_entry.get()))
        search_button.grid(row=0, column=2, padx=10)

        self.results_text = tk.Text(self.root, height=15)
        self.results_text.pack(padx=10, pady=10, fill='both', expand=True)

        return_button = tk.Button(input_frame, text="Return", command=self.create_inventory_management)
        return_button.grid(row=0, column=3, padx=10)

        self.populate_all_inventory()

    def validate_and_search(self, input_text):
        if input_text.isdigit():
            inventory_id = int(input_text)
            self.search_inventory_by_id(input_text)
        else:
            messagebox.showerror("Error", "Please enter a valid integer.")

    def populate_all_inventory(self):
        if self.results_text.winfo_exists():
            response = requests.get("http://localhost:12345/inventory/all")
            self.results_text.delete('1.0', tk.END)
            if response.status_code == 200:
                inventory_items = response.json()
                for item in inventory_items:
                    line = f"Inventory ID: {item['inventoryid']}, Product ID: {item['productid']}, " \
                           f"Quantity: {item['quantity']}, Region ID: {item['regionid']}, " \
                           f"Min Quantity: {item['minquantity']}\n"
                    self.results_text.insert(tk.END, line)
                # Save the after job ID so we can cancel it if we leave this page
                self.inventory_update_job = self.root.after(10000, self.populate_all_inventory)
            else:
                messagebox.showerror("Error", "Failed to retrieve inventory")
        else:
            # Cancel the after job since the widget doesn't exist anymore
            if self.inventory_update_job is not None:
                self.root.after_cancel(self.inventory_update_job)
                self.inventory_update_job = None

    def search_inventory_by_id(self, inventory_id):
        if not inventory_id.strip():
            messagebox.showinfo("Info", "Please enter an Inventory ID to search.")
            return
        if inventory_id.strip():
            response = requests.get(f"http://localhost:12345/inventory/{inventory_id}")
            if response.status_code == 200:
                inventory_item = response.json()
                if inventory_item:
                    self.show_search_results(inventory_item)
                else:
                    messagebox.showinfo("Search Result", "No inventory found for the provided ID")
            else:
                self.results_text.insert(tk.END, "Failed to retrieve inventory for the provided ID\n")

    def show_search_results(self, inventory_item):
        self.clear_frame()
        results_frame = tk.Frame(self.root)
        results_frame.pack(padx=10, pady=10, fill='both', expand=True)

        results_text = tk.Text(results_frame, height=15)
        results_text.pack(padx=10, pady=10, fill='both', expand=True)

        for key, value in inventory_item.items():
            results_text.insert(tk.END, "{}: {}\n".format(key.capitalize(), value))

        scrollbar = tk.Scrollbar(results_frame, command=results_text.yview)
        scrollbar.pack(side='right', fill='y')
        results_text['yscrollcommand'] = scrollbar.set

        return_button = tk.Button(results_frame, text="Return", command=lambda: self.search_inventory())
        return_button.pack(pady=10)

    def view_all_inventory(self):
        response = requests.get("http://localhost:12345/inventory/all")

        if response.status_code == 200:
            inventory_items = response.json()
            if inventory_items:
                self.display_all_inventory(inventory_items)
            else:
                messagebox.showinfo("Info", "No inventory found")
                self.create_inventory_management()
        else:
            messagebox.showerror("Error", "Failed to retrieve inventory")
            self.create_inventory_management()

    def display_all_inventory(self, inventory_items):
        self.clear_frame()

        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Inventory", font=('Helvetica', 18, 'bold')).grid(row=0, columnspan=4)

        # Headers
        headers = ["Inventory ID", "Product ID", "Quantity", "Region ID", "Min Quantity"]
        for i, header in enumerate(headers):
            tk.Label(frame, text=header, font=('Helvetica', 16, 'bold')).grid(row=1, column=i)

        # Display each inventory item
        for index, item in enumerate(inventory_items):
            for col, key in enumerate(headers):
                tk.Label(frame, text=item[key.replace(" ", "").lower()], font=('Helvetica', 14)).grid(row=index + 2,
                                                                                                      column=col)
        return_button = tk.Button(frame, text="Return", width=20, height=2,command=lambda: [self.clear_frame(), self.create_inventory_management()])
        return_button.grid(row=len(inventory_items) + 3, columnspan=4)

    def edit_inventory(self):
        self.clear_frame()

        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10, fill='x')

        tk.Label(input_frame, text="Enter Inventory ID:").grid(row=0, column=0)
        self.search_entry = tk.Entry(input_frame)  # Make search_entry accessible to other methods
        self.search_entry.grid(row=0, column=1)

        search_button = tk.Button(input_frame, text="Edit",command=lambda: self.validate_and_search_edit(self.search_entry.get()))
        search_button.grid(row=0, column=2, padx=10)

        add_button = tk.Button(input_frame, text="Add", command=self.create_add_inventory_form)
        add_button.grid(row=0, column=3, padx=10)

        return_button = tk.Button(input_frame, text="Return", command=self.create_inventory_management)
        return_button.grid(row=0, column=4, padx=10)

        self.results_text = tk.Text(self.root, height=15)
        self.results_text.pack(padx=10, pady=10, fill='both', expand=True)

        self.populate_all_inventory()

    def validate_and_search_edit(self, input_text):
        if input_text.isdigit():
            inventory_id = int(input_text)
            self.prepare_edit_inventory(input_text)
        else:
            messagebox.showerror("Error", "Please enter a valid integer.")

    def create_add_inventory_form(self):
        self.clear_frame()

        add_frame = tk.Frame(self.root)
        add_frame.pack(padx=10, pady=10, fill='x')

        labels = ["productid", "quantity", "regionid", "minquantity"]
        entries = {}

        for index, label in enumerate(labels):
            tk.Label(add_frame, text=label).grid(row=index, column=0)
            entry = tk.Entry(add_frame)
            entry.grid(row=index, column=1)
            entries[label] = entry

        submit_button = tk.Button(add_frame, text="Submit",
                                  command=lambda: self.submit_new_inventory(entries))
        submit_button.grid(row=len(labels), column=0, columnspan=2)

        return_button = tk.Button(add_frame, text="Return", command=self.edit_inventory)
        return_button.grid(row=len(labels) + 1, column=0, columnspan=2)

    def submit_new_inventory(self, entries):
        new_inventory_data = {label.lower().replace(" ", ""): entry.get() for label, entry in entries.items()}

        response = requests.post("http://localhost:12345/inventory/add", json=new_inventory_data)
        if response.status_code == 200:
            messagebox.showinfo("Success", "New inventory added successfully.")
            self.edit_inventory()  # Refresh the form or go back to the inventory management
        else:
            messagebox.showerror("Error", "Failed to add new inventory.")

    def prepare_edit_inventory(self, inventory_id):
        if not inventory_id.strip():
            messagebox.showinfo("Info", "Please enter an Inventory ID to edit.")
            return

        response = requests.get(f"http://localhost:12345/inventory/{inventory_id}")
        if response.status_code == 200:
            inventory_item = response.json()
            if inventory_item:
                self.show_edit_inventory_form(inventory_item)
            else:
                messagebox.showinfo("Info", "No inventory found for the provided ID")
        else:
            messagebox.showerror("Error", "Failed to retrieve inventory for the provided ID")

    def show_edit_inventory_form(self, inventory_item):
        self.clear_frame()

        edit_frame = tk.Frame(self.root)
        edit_frame.pack(padx=10, pady=10, fill='x')

        labels = ["Inventory ID", "Product ID", "Quantity", "Region ID", "Min Quantity"]
        self.entries = {}

        for index, label in enumerate(labels):
            tk.Label(edit_frame, text=label).grid(row=index, column=0)
            entry = tk.Entry(edit_frame)
            entry.grid(row=index, column=1)
            entry.insert(0, inventory_item.get(label.lower().replace(" ", "")))
            self.entries[label] = entry

        edit_button = tk.Button(edit_frame, text="Submit Edit",
                                command=lambda: self.submit_edit_inventory(inventory_item["inventoryid"]))
        edit_button.grid(row=len(labels), column=0, columnspan=2)

        delete_button = tk.Button(edit_frame, text="Delete",
                                  command=lambda: self.delete_inventory(inventory_item["inventoryid"]))
        delete_button.grid(row=len(labels) + 2, column=0, columnspan=2)

        return_button = tk.Button(edit_frame, text="Return", command=self.edit_inventory)
        return_button.grid(row=len(labels) + 1, column=0, columnspan=2)

    def delete_inventory(self, inventory_id):
        response = requests.delete(f"http://localhost:12345/inventory/{inventory_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Inventory item deleted successfully.")
            self.edit_inventory()  # Refresh the edit form or return to inventory management
        else:
            messagebox.showerror("Error", "Failed to delete inventory item.")

    def submit_edit_inventory(self, inventory_id):
        updated_inventory = {key.lower().replace(" ", ""): entry.get() for key, entry in self.entries.items()}

        response = requests.put(f"http://localhost:12345/inventory/{inventory_id}", json=updated_inventory)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Inventory updated successfully.")
            self.edit_inventory()  # Refresh the edit form
        else:
            messagebox.showerror("Error", "Failed to update inventory.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductManagementApp(root)
    root.mainloop()
