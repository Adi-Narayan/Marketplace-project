import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import hashlib
import datetime
import os
import re
from tkinter.scrolledtext import ScrolledText
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

class JewelryMarketplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jewelry Marketplace")
        self.root.geometry("1200x900")
        
        # Load environment variables for Twilio
        load_dotenv()
        self.twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        self.twilio_from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        # Create gradient background
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.create_gradient()
        
        # Initialize database
        self.create_database()
        
        # Initialize user state
        self.current_user = None
        self.cart = []
        
        # Setup custom style for vibrant UI
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.setup_styles()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create frames for different sections
        self.login_frame = ttk.Frame(self.notebook)
        self.register_frame = ttk.Frame(self.notebook)
        self.products_frame = ttk.Frame(self.notebook)
        self.sets_frame = ttk.Frame(self.notebook)
        self.cart_frame = ttk.Frame(self.notebook)
        self.orders_frame = ttk.Frame(self.notebook)
        self.profile_frame = ttk.Frame(self.notebook)
        self.admin_frame = ttk.Frame(self.notebook)
        
        # Add frames to notebook
        self.notebook.add(self.login_frame, text="Login")
        self.notebook.add(self.register_frame, text="Register")
        
        # Setup each frame
        self.setup_login_frame()
        self.setup_register_frame()
        self.setup_products_frame()
        self.setup_sets_frame()
        self.setup_cart_frame()
        self.setup_orders_frame()
        self.setup_profile_frame()
        self.setup_admin_frame()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome to Jewelry Marketplace")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, style='Status.TLabel')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind window resize to update gradient
        self.root.bind('<Configure>', self.create_gradient)

    def create_gradient(self, event=None):
        """Create a gradient background"""
        self.canvas.delete("gradient")
        width = self.canvas.winfo_width() or self.root.winfo_width()
        height = self.canvas.winfo_height() or self.root.winfo_height()
        
        # Gradient colors
        color1 = "#4ECDC4"  # Teal
        color2 = "#FF6B6B"  # Coral
        
        # Create gradient
        for i in range(height):
            r1, g1, b1 = [int(x) for x in self.canvas.winfo_rgb(color1)]
            r2, g2, b2 = [int(x) for x in self.canvas.winfo_rgb(color2)]
            r = int(r1 + (r2 - r1) * i / height)
            g = int(g1 + (g2 - g1) * i / height)
            b = int(b1 + (b2 - b1) * i / height)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color, tags="gradient")

    def setup_styles(self):
        """Setup custom styles for vibrant UI"""
        self.style.configure('TNotebook', background='#FFFFFF', tabmargins=5)
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 12), padding=[10, 5], background='#E0E0E0')
        self.style.map('TNotebook.Tab', background=[('selected', '#4ECDC4')])
        
        self.style.configure('TFrame', background='#FFFFFF')
        self.style.configure('TLabel', background='#FFFFFF', font=('Segoe UI', 11))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=10)
        self.style.map('TButton', 
                      background=[('active', '#FF6B6B'), ('!active', '#4ECDC4')],
                      foreground=[('active', '#FFFFFF'), ('!active', '#FFFFFF')])
        
        self.style.configure('TEntry', padding=5, font=('Segoe UI', 11))
        self.style.configure('TCombobox', padding=5, font=('Segoe UI', 11))
        self.style.configure('Treeview', font=('Segoe UI', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 11, 'bold'))
        
        self.style.configure('Status.TLabel', background='#333333', foreground='#FFFFFF', 
                           font=('Segoe UI', 10), padding=5)

    def create_database(self):
        """Create the database if it doesn't exist and initialize tables"""
        db_exists = os.path.exists("jewelry_marketplace.db")
        self.conn = sqlite3.connect("jewelry_marketplace.db")
        self.cur = self.conn.cursor()
        
        if not db_exists:
            with open("schema.sql", "r") as schema_file:
                schema = schema_file.read()
                self.cur.executescript(schema)
            
            with open("sample_data.sql", "r") as data_file:
                sample_data = data_file.read()
                self.cur.executescript(sample_data)
            
            self.conn.commit()
            print("Database created and initialized with sample data.")

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def send_sms(self, to_number, message):
        """Send SMS using Twilio"""
        try:
            message = self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_from_number,
                to=to_number
            )
            print(f"SMS sent successfully: {message.sid}")
        except TwilioRestException as e:
            print(f"Failed to send SMS: {e}")
            messagebox.showerror("Error", "Failed to send SMS notification")

    def setup_login_frame(self):
        """Setup the login frame"""
        frame = ttk.Frame(self.login_frame, padding=30, style='TFrame')
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Login to Jewelry Marketplace", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.username_entry = ttk.Entry(frame, width=40)
        self.username_entry.grid(row=1, column=1, pady=10)
        
        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.password_entry = ttk.Entry(frame, width=40, show="*")
        self.password_entry.grid(row=2, column=1, pady=10)
        
        ttk.Button(frame, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Label(frame, text="Don't have an account?").grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Register", command=lambda: self.notebook.select(1)).grid(row=5, column=0, columnspan=2)

    def setup_register_frame(self):
        """Setup the register frame with phone number validation"""
        frame = ttk.Frame(self.register_frame, padding=10, style='TFrame')  # Reduced padding from 30 to 10
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Register New Account", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        fields = [
            ("Username:", "reg_username"), 
            ("Password:", "reg_password"),
            ("Confirm Password:", "reg_confirm_password"),
            ("Email:", "reg_email"),
            ("First Name:", "reg_firstname"),
            ("Last Name:", "reg_lastname"),
            ("Address:", "reg_address"),
            ("Phone (10 digits):", "reg_phone")
        ]
        
        for i, (label, attr) in enumerate(fields):
            ttk.Label(frame, text=label).grid(row=i+1, column=0, sticky=tk.W, pady=5)
            if "password" in attr:
                entry = ttk.Entry(frame, width=40, show="*")
            else:
                entry = ttk.Entry(frame, width=40)
            entry.grid(row=i+1, column=1, pady=5)
            setattr(self, attr, entry)
        
        ttk.Button(frame, text="Register", command=self.register).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="Already have an account?").grid(row=len(fields)+2, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Login", command=lambda: self.notebook.select(0)).grid(row=len(fields)+3, column=0, columnspan=2, pady=5)

    def setup_products_frame(self):
        """Setup the products frame"""
        filter_frame = ttk.Frame(self.products_frame, padding=15, style='TFrame')
        filter_frame.pack(fill=tk.X)
        
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT, padx=10)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var, state="readonly", width=20)
        self.category_combo.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(filter_frame, text="Price Range:").pack(side=tk.LEFT, padx=10)
        self.min_price_var = tk.StringVar(value="0")
        ttk.Entry(filter_frame, textvariable=self.min_price_var, width=10).pack(side=tk.LEFT)
        ttk.Label(filter_frame, text="-").pack(side=tk.LEFT)
        self.max_price_var = tk.StringVar(value="10000")
        ttk.Entry(filter_frame, textvariable=self.max_price_var, width=10).pack(side=tk.LEFT)
        
        ttk.Button(filter_frame, text="Apply Filters", command=self.load_products).pack(side=tk.LEFT, padx=15)
        ttk.Button(filter_frame, text="Clear Filters", command=self.clear_product_filters).pack(side=tk.LEFT)
        
        list_frame = ttk.Frame(self.products_frame, padding=15, style='TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Name", "Description", "Price", "Stock", "Category")
        self.products_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.products_tree.heading(col, text=col)
            width = 120 if col != "Description" else 350
            self.products_tree.column(col, width=width)
        
        self.products_tree.bind("<Double-1>", self.view_product_details)
        
        y_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=y_scroll.set)
        
        x_scroll = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.products_tree.xview)
        self.products_tree.configure(xscrollcommand=x_scroll.set)
        
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        action_frame = ttk.Frame(self.products_frame, padding=15, style='TFrame')
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Add to Cart", command=self.add_product_to_cart).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="View Reviews", command=self.view_product_reviews).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="Add Review", command=self.add_product_review).pack(side=tk.LEFT, padx=10)
        
        self.load_categories()

    def setup_sets_frame(self):
        """Setup the sets frame"""
        filter_frame = ttk.Frame(self.sets_frame, padding=15, style='TFrame')
        filter_frame.pack(fill=tk.X)
        
        ttk.Label(filter_frame, text="Price Range:").pack(side=tk.LEFT, padx=10)
        self.set_min_price_var = tk.StringVar(value="0")
        ttk.Entry(filter_frame, textvariable=self.set_min_price_var, width=10).pack(side=tk.LEFT)
        ttk.Label(filter_frame, text="-").pack(side=tk.LEFT)
        self.set_max_price_var = tk.StringVar(value="10000")
        ttk.Entry(filter_frame, textvariable=self.set_max_price_var, width=10).pack(side=tk.LEFT)
        
        ttk.Button(filter_frame, text="Apply Filters", command=self.load_sets).pack(side=tk.LEFT, padx=15)
        ttk.Button(filter_frame, text="Clear Filters", command=self.clear_set_filters).pack(side=tk.LEFT)
        
        list_frame = ttk.Frame(self.sets_frame, padding=15, style='TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Name", "Description", "Price", "Stock")
        self.sets_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.sets_tree.heading(col, text=col)
            width = 120 if col != "Description" else 350
            self.sets_tree.column(col, width=width)
        
        self.sets_tree.bind("<Double-1>", self.view_set_details)
        
        y_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.sets_tree.yview)
        self.sets_tree.configure(yscrollcommand=y_scroll.set)
        
        x_scroll = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.sets_tree.xview)
        self.sets_tree.configure(xscrollcommand=x_scroll.set)
        
        self.sets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        action_frame = ttk.Frame(self.sets_frame, padding=15, style='TFrame')
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Add to Cart", command=self.add_set_to_cart).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="View Set Items", command=self.view_set_items).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="View Reviews", command=self.view_set_reviews).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="Add Review", command=self.add_set_review).pack(side=tk.LEFT, padx=10)

    def setup_cart_frame(self):
        """Setup the cart frame"""
        list_frame = ttk.Frame(self.cart_frame, padding=15, style='TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Type", "ID", "Name", "Price", "Quantity")
        self.cart_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=120)
        
        y_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=y_scroll.set)
        
        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        action_frame = ttk.Frame(self.cart_frame, padding=15, style='TFrame')
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Remove Item", command=self.remove_from_cart).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="Update Quantity", command=self.update_cart_quantity).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="Clear Cart", command=self.clear_cart).pack(side=tk.LEFT, padx=10)
        
        self.total_var = tk.StringVar(value="Total: $0.00")
        ttk.Label(action_frame, textvariable=self.total_var, font=("Segoe UI", 12, "bold")).pack(side=tk.RIGHT, padx=30)
        
        checkout_frame = ttk.Frame(self.cart_frame, padding=15, style='TFrame')
        checkout_frame.pack(fill=tk.X)
        
        ttk.Label(checkout_frame, text="Payment Method:").pack(side=tk.LEFT, padx=10)
        self.payment_method_var = tk.StringVar(value="credit card")
        payment_method_combo = ttk.Combobox(checkout_frame, textvariable=self.payment_method_var, state="readonly", width=20)
        payment_method_combo['values'] = ('credit card', 'PayPal')
        payment_method_combo.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(checkout_frame, text="Checkout", command=self.checkout).pack(side=tk.LEFT, padx=15)

    def setup_orders_frame(self):
        """Setup the orders frame"""
        list_frame = ttk.Frame(self.orders_frame, padding=15, style='TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Date", "Total", "Status")
        self.orders_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=150)
        
        self.orders_tree.bind("<Double-1>", self.view_order_details)
        
        y_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=y_scroll.set)
        
        self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        action_frame = ttk.Frame(self.orders_frame, padding=15, style='TFrame')
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Refresh Orders", command=self.load_orders).pack(side=tk.LEFT, padx=10)

    def setup_profile_frame(self):
        """Setup the profile frame"""
        frame = ttk.Frame(self.profile_frame, padding=30, style='TFrame')
        frame.pack(expand=True)
        
        ttk.Label(frame, text="User Profile", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        fields = [
            ("Username:", "profile_username", False),
            ("Email:", "profile_email", True),
            ("First Name:", "profile_firstname", True),
            ("Last Name:", "profile_lastname", True),
            ("Address:", "profile_address", True),
            ("Phone:", "profile_phone", True)
        ]
        
        for i, (label, attr, editable) in enumerate(fields):
            ttk.Label(frame, text=label).grid(row=i+1, column=0, sticky=tk.W, pady=10)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=i+1, column=1, pady=10)
            if not editable:
                entry.configure(state='disabled')
            setattr(self, attr, entry)
        
        ttk.Label(frame, text="New Password:").grid(row=len(fields)+1, column=0, sticky=tk.W, pady=10)
        self.profile_password = ttk.Entry(frame, width=40, show="*")
        self.profile_password.grid(row=len(fields)+1, column=1, pady=10)
        
        ttk.Label(frame, text="Confirm Password:").grid(row=len(fields)+2, column=0, sticky=tk.W, pady=10)
        self.profile_confirm_password = ttk.Entry(frame, width=40, show="*")
        self.profile_confirm_password.grid(row=len(fields)+2, column=1, pady=10)
        
        ttk.Button(frame, text="Update Profile", command=self.update_profile).grid(row=len(fields)+3, column=0, columnspan=2, pady=20)

    def setup_admin_frame(self):
        """Setup the admin frame"""
        frame = ttk.Frame(self.admin_frame, padding=30, style='TFrame')
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Admin Panel", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(frame, text="Manage Products", font=("Segoe UI", 14)).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Add Product", command=self.add_product).grid(row=2, column=0, pady=10, padx=10)
        ttk.Button(frame, text="Update Product", command=self.update_product).grid(row=2, column=1, pady=10, padx=10)
        ttk.Button(frame, text="Delete Product", command=self.delete_product).grid(row=3, column=0, pady=10, padx=10)
        
        ttk.Label(frame, text="Manage Sets", font=("Segoe UI", 14)).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Add Set", command=self.add_set).grid(row=5, column=0, pady=10, padx=10)
        ttk.Button(frame, text="Update Set", command=self.update_set).grid(row=5, column=1, pady=10, padx=10)
        ttk.Button(frame, text="Delete Set", command=self.delete_set).grid(row=6, column=0, pady=10, padx=10)
        
        ttk.Label(frame, text="Manage Orders", font=("Segoe UI", 14)).grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Update Order Status", command=self.update_order_status).grid(row=8, column=0, pady=10, padx=10)

    def login(self):
        """Handle user login"""
        username = self.username_entry.get()
        password = self.hash_password(self.password_entry.get())
        
        self.cur.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
        user = self.cur.fetchone()
        
        if user:
            self.current_user = user
            self.notebook.add(self.products_frame, text="Products")
            self.notebook.add(self.sets_frame, text="Sets")
            self.notebook.add(self.cart_frame, text="Cart")
            self.notebook.add(self.orders_frame, text="Orders")
            self.notebook.add(self.profile_frame, text="Profile")
            
            if username == "admin":
                self.notebook.add(self.admin_frame, text="Admin")
            
            self.notebook.forget(self.login_frame)
            self.notebook.forget(self.register_frame)
            self.status_var.set(f"Welcome, {user[4]} {user[5]}")
            self.load_products()
            self.load_sets()
            self.load_orders()
            self.load_profile()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        """Handle user registration with SMS notification"""
        username = self.reg_username.get()
        password = self.reg_password.get()
        confirm_password = self.reg_confirm_password.get()
        email = self.reg_email.get()
        firstname = self.reg_firstname.get()
        lastname = self.reg_lastname.get()
        address = self.reg_address.get()
        phone = self.reg_phone.get()
        
        # Validation
        if not all([username, password, email, firstname, lastname, address, phone]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Phone number validation: must be exactly 10 digits
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showerror("Error", "Phone number must be exactly 10 digits")
            return
        
        full_phone = f"+91{phone}"
        
        try:
            hashed_password = self.hash_password(password)
            self.cur.execute("""
                INSERT INTO Users (username, password, email, firstname, lastname, address, phone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, hashed_password, email, firstname, lastname, address, full_phone))
            self.conn.commit()
            
            # Send SMS notification
            sms_message = f"Welcome to Jewelry Marketplace, {firstname}! Your account has been successfully created."
            self.send_sms(full_phone, sms_message)
            
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.notebook.select(0)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or email already exists")

    def load_categories(self):
        """Load categories for product filtering"""
        self.cur.execute("SELECT name FROM Categories")
        categories = ["All"] + [row[0] for row in self.cur.fetchall()]
        self.category_combo['values'] = categories
        self.category_combo.set("All")

    def load_products(self):
        """Load products based on filters"""
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        query = """
            SELECT p.id, p.name, p.description, p.price, p.stock_quantity, c.name
            FROM Products p
            JOIN Categories c ON p.category_id = c.id
            WHERE p.price BETWEEN ? AND ?
        """
        params = [float(self.min_price_var.get()), float(self.max_price_var.get())]
        
        if self.category_var.get() != "All":
            query += " AND c.name = ?"
            params.append(self.category_var.get())
        
        self.cur.execute(query, params)
        for row in self.cur.fetchall():
            self.products_tree.insert("", tk.END, values=row)

    def clear_product_filters(self):
        """Clear product filters"""
        self.category_var.set("All")
        self.min_price_var.set("0")
        self.max_price_var.set("10000")
        self.load_products()

    def view_product_details(self, event):
        """View product details on double-click"""
        selected = self.products_tree.selection()
        if selected:
            item = self.products_tree.item(selected[0])
            product_id = item['values'][0]
            
            self.cur.execute("SELECT * FROM Products WHERE id = ?", (product_id,))
            product = self.cur.fetchone()
            
            details = f"Name: {product[1]}\nDescription: {product[2]}\nPrice: ${product[3]:.2f}\nStock: {product[4]}"
            messagebox.showinfo("Product Details", details)

    def add_product_to_cart(self):
        """Add selected product to cart"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product")
            return
        
        item = self.products_tree.item(selected[0])
        product_id = item['values'][0]
        
        quantity = simpledialog.askinteger("Quantity", "Enter quantity:", minvalue=1, maxvalue=int(item['values'][4]))
        if quantity:
            self.cart.append({
                'type': 'product',
                'id': product_id,
                'name': item['values'][1],
                'price': float(item['values'][3]),
                'quantity': quantity
            })
            self.update_cart_display()
            messagebox.showinfo("Success", "Product added to cart")

    def view_product_reviews(self):
        """View reviews for selected product"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product")
            return
        
        product_id = self.products_tree.item(selected[0])['values'][0]
        
        self.cur.execute("""
            SELECT u.username, r.rating, r.comment, r.created_at
            FROM Reviews r
            JOIN Users u ON r.user_id = u.id
            WHERE r.product_id = ?
        """, (product_id,))
        
        reviews = self.cur.fetchall()
        if not reviews:
            messagebox.showinfo("Reviews", "No reviews for this product")
            return
        
        review_text = ""
        for review in reviews:
            review_text += f"User: {review[0]}\nRating: {review[1]}/5\nComment: {review[2]}\nDate: {review[3]}\n\n"
        
        review_window = tk.Toplevel(self.root)
        review_window.title("Product Reviews")
        review_window.geometry("500x400")
        
        text_area = ScrolledText(review_window, wrap=tk.WORD, width=60, height=20)
        text_area.pack(padx=15, pady=15)
        text_area.insert(tk.END, review_text)
        text_area.configure(state='disabled')

    def add_product_review(self):
        """Add a review for selected product"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login to add a review")
            return
        
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product")
            return
        
        product_id = self.products_tree.item(selected[0])['values'][0]
        
        review_window = tk.Toplevel(self.root)
        review_window.title("Add Review")
        review_window.geometry("400x300")
        
        ttk.Label(review_window, text="Rating (1-5):").pack(pady=10)
        rating_var = tk.StringVar()
        rating_combo = ttk.Combobox(review_window, textvariable=rating_var, values=[1,2,3,4,5], state="readonly")
        rating_combo.pack(pady=10)
        
        ttk.Label(review_window, text="Comment:").pack(pady=10)
        comment_text = ScrolledText(review_window, wrap=tk.WORD, width=40, height=10)
        comment_text.pack(pady=10)
        
        def submit_review():
            rating = rating_var.get()
            comment = comment_text.get("1.0", tk.END).strip()
            
            if not rating:
                messagebox.showerror("Error", "Please select a rating")
                return
            
            self.cur.execute("""
                INSERT INTO Reviews (user_id, product_id, rating, comment)
                VALUES (?, ?, ?, ?)
            """, (self.current_user[0], product_id, int(rating), comment))
            self.conn.commit()
            messagebox.showinfo("Success", "Review submitted")
            review_window.destroy()
        
        ttk.Button(review_window, text="Submit Review", command=submit_review).pack(pady=15)

    def load_sets(self):
        """Load sets based on filters"""
        for item in self.sets_tree.get_children():
            self.sets_tree.delete(item)
        
        query = """
            SELECT id, name, description, price, stock_quantity
            FROM Sets
            WHERE price BETWEEN ? AND ?
        """
        params = [float(self.set_min_price_var.get()), float(self.set_max_price_var.get())]
        
        self.cur.execute(query, params)
        for row in self.cur.fetchall():
            self.sets_tree.insert("", tk.END, values=row)

    def clear_set_filters(self):
        """Clear set filters"""
        self.set_min_price_var.set("0")
        self.set_max_price_var.set("10000")
        self.load_sets()

    def view_set_details(self, event):
        """View set details on double-click"""
        selected = self.sets_tree.selection()
        if selected:
            item = self.sets_tree.item(selected[0])
            set_id = item['values'][0]
            
            self.cur.execute("SELECT * FROM Sets WHERE id = ?", (set_id,))
            set_info = self.cur.fetchone()
            
            details = f"Name: {set_info[1]}\nDescription: {set_info[2]}\nPrice: ${set_info[3]:.2f}\nStock: {set_info[4]}"
            messagebox.showinfo("Set Details", details)

    def add_set_to_cart(self):
        """Add selected set to cart"""
        selected = self.sets_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a set")
            return
        
        item = self.sets_tree.item(selected[0])
        set_id = item['values'][0]
        
        quantity = simpledialog.askinteger("Quantity", "Enter quantity:", minvalue=1, maxvalue=int(item['values'][4]))
        if quantity:
            self.cart.append({
                'type': 'set',
                'id': set_id,
                'name': item['values'][1],
                'price': float(item['values'][3]),
                'quantity': quantity
            })
            self.update_cart_display()
            messagebox.showinfo("Success", "Set added to cart")

    def view_set_items(self):
        """View items in selected set"""
        selected = self.sets_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a set")
            return
        
        set_id = self.sets_tree.item(selected[0])['values'][0]
        
        self.cur.execute("""
            SELECT p.name, p.description, p.price
            FROM Set_Items si
            JOIN Products p ON si.product_id = p.id
            WHERE si.set_id = ?
        """, (set_id,))
        
        items = self.cur.fetchall()
        if not items:
            messagebox.showinfo("Set Items", "No items in this set")
            return
        
        items_text = ""
        for item in items:
            items_text += f"Name: {item[0]}\nDescription: {item[1]}\nPrice: ${item[2]:.2f}\n\n"
        
        items_window = tk.Toplevel(self.root)
        items_window.title("Set Items")
        items_window.geometry("500x400")
        
        text_area = ScrolledText(items_window, wrap=tk.WORD, width=60, height=20)
        text_area.pack(padx=15, pady=15)
        text_area.insert(tk.END, items_text)
        text_area.configure(state='disabled')

    def view_set_reviews(self):
        """View reviews for selected set"""
        selected = self.sets_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a set")
            return
        
        set_id = self.sets_tree.item(selected[0])['values'][0]
        
        self.cur.execute("""
            SELECT u.username, r.rating, r.comment, r.created_at
            FROM Reviews r
            JOIN Users u ON r.user_id = u.id
            WHERE r.set_id = ?
        """, (set_id,))
        
        reviews = self.cur.fetchall()
        if not reviews:
            messagebox.showinfo("Reviews", "No reviews for this set")
            return
        
        review_text = ""
        for review in reviews:
            review_text += f"User: {review[0]}\nRating: {review[1]}/5\nComment: {review[2]}\nDate: {review[3]}\n\n"
        
        review_window = tk.Toplevel(self.root)
        review_window.title("Set Reviews")
        review_window.geometry("500x400")
        
        text_area = ScrolledText(review_window, wrap=tk.WORD, width=60, height=20)
        text_area.pack(padx=15, pady=15)
        text_area.insert(tk.END, review_text)
        text_area.configure(state='disabled')

    def add_set_review(self):
        """Add a review for selected set"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login to add a review")
            return
        
        selected = self.sets_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a set")
            return
        
        set_id = self.sets_tree.item(selected[0])['values'][0]
        
        review_window = tk.Toplevel(self.root)
        review_window.title("Add Review")
        review_window.geometry("400x300")
        
        ttk.Label(review_window, text="Rating (1-5):").pack(pady=10)
        rating_var = tk.StringVar()
        rating_combo = ttk.Combobox(review_window, textvariable=rating_var, values=[1,2,3,4,5], state="readonly")
        rating_combo.pack(pady=10)
        
        ttk.Label(review_window, text="Comment:").pack(pady=10)
        comment_text = ScrolledText(review_window, wrap=tk.WORD, width=40, height=10)
        comment_text.pack(pady=10)
        
        def submit_review():
            rating = rating_var.get()
            comment = comment_text.get("1.0", tk.END).strip()
            
            if not rating:
                messagebox.showerror("Error", "Please select a rating")
                return
            
            self.cur.execute("""
                INSERT INTO Reviews (user_id, set_id, rating, comment)
                VALUES (?, ?, ?, ?)
            """, (self.current_user[0], set_id, int(rating), comment))
            self.conn.commit()
            messagebox.showinfo("Success", "Review submitted")
            review_window.destroy()
        
        ttk.Button(review_window, text="Submit Review", command=submit_review).pack(pady=15)

    def update_cart_display(self):
        """Update cart display"""
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        total = 0
        for item in self.cart:
            self.cart_tree.insert("", tk.END, values=(
                item['type'].capitalize(),
                item['id'],
                item['name'],
                f"${item['price']:.2f}",
                item['quantity']
            ))
            total += item['price'] * item['quantity']
        
        self.total_var.set(f"Total: ${total:.2f}")

    def remove_from_cart(self):
        """Remove selected item from cart"""
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item")
            return
        
        index = self.cart_tree.index(selected[0])
        self.cart.pop(index)
        self.update_cart_display()

    def update_cart_quantity(self):
        """Update quantity of selected cart item"""
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item")
            return
        
        index = self.cart_tree.index(selected[0])
        item = self.cart[index]
        
        quantity = simpledialog.askinteger("Quantity", "Enter new quantity:", minvalue=1)
        if quantity:
            self.cart[index]['quantity'] = quantity
            self.update_cart_display()

    def clear_cart(self):
        """Clear all items from cart"""
        if messagebox.askyesno("Confirm", "Clear all items from cart?"):
            self.cart = []
            self.update_cart_display()

    def checkout(self):
        """Process checkout"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login to checkout")
            return
        
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty")
            return
        
        total = sum(item['price'] * item['quantity'] for item in self.cart)
        
        self.cur.execute("""
            INSERT INTO Orders (user_id, total_amount, status)
            VALUES (?, ?, ?)
        """, (self.current_user[0], total, 'pending'))
        order_id = self.cur.lastrowid
        
        for item in self.cart:
            if item['type'] == 'product':
                self.cur.execute("""
                    INSERT INTO Order_Items (order_id, product_id, quantity, unit_price)
                    VALUES (?, ?, ?, ?)
                """, (order_id, item['id'], item['quantity'], item['price']))
                
                self.cur.execute("""
                    UPDATE Products
                    SET stock_quantity = stock_quantity - ?
                    WHERE id = ?
                """, (item['quantity'], item['id']))
                
            else:
                self.cur.execute("""
                    INSERT INTO Order_Items (order_id, set_id, quantity, unit_price)
                    VALUES (?, ?, ?, ?)
                """, (order_id, item['id'], item['quantity'], item['price']))
                
                self.cur.execute("""
                    UPDATE Sets
                    SET stock_quantity = stock_quantity - ?
                    WHERE id = ?
                """, (item['quantity'], item['id']))
        
        transaction_id = f"TRANS_{order_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.cur.execute("""
            INSERT INTO Payments (order_id, amount, payment_method, payment_status, transaction_id)
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, total, self.payment_method_var.get(), 'completed', transaction_id))
        
        self.conn.commit()
        
        self.cart = []
        self.update_cart_display()
        self.load_products()
        self.load_sets()
        self.load_orders()
        
        messagebox.showinfo("Success", f"Order placed successfully! Order ID: {order_id}")

    def load_orders(self):
        """Load user orders"""
        if not self.current_user:
            return
        
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        self.cur.execute("""
            SELECT id, order_date, total_amount, status
            FROM Orders
            WHERE user_id = ?
            ORDER BY order_date DESC
        """, (self.current_user[0],))
        
        for row in self.cur.fetchall():
            self.orders_tree.insert("", tk.END, values=(
                row[0],
                row[1],
                f"${row[2]:.2f}",
                row[3].capitalize()
            ))

    def view_order_details(self, event):
        """View order details on double-click"""
        selected = self.orders_tree.selection()
        if not selected:
            return
        
        order_id = self.orders_tree.item(selected[0])['values'][0]
        
        self.cur.execute("""
            SELECT oi.quantity, oi.unit_price,
                   COALESCE(p.name, s.name) as item_name,
                   CASE WHEN p.id IS NOT NULL THEN 'product' ELSE 'set' END as item_type
            FROM Order_Items oi
            LEFT JOIN Products p ON oi.product_id = p.id
            LEFT JOIN Sets s ON oi.set_id = s.id
            WHERE oi.order_id = ?
        """, (order_id,))
        
        items = self.cur.fetchall()
        
        details = f"Order ID: {order_id}\n\nItems:\n"
        total = 0
        for item in items:
            subtotal = item[0] * item[1]
            total += subtotal
            details += f"{item[3].capitalize()}: {item[2]}\n"
            details += f"Quantity: {item[0]}\n"
            details += f"Unit Price: ${item[1]:.2f}\n"
            details += f"Subtotal: ${subtotal:.2f}\n\n"
        
        details += f"Total: ${total:.2f}"
        
        self.cur.execute("SELECT status, order_date FROM Orders WHERE id = ?", (order_id,))
        order = self.cur.fetchone()
        details += f"\nStatus: {order[0].capitalize()}"
        details += f"\nOrder Date: {order[1]}"
        
        order_window = tk.Toplevel(self.root)
        order_window.title("Order Details")
        order_window.geometry("500x400")
        
        text_area = ScrolledText(order_window, wrap=tk.WORD, width=60, height=20)
        text_area.pack(padx=15, pady=15)
        text_area.insert(tk.END, details)
        text_area.configure(state='disabled')

    def load_profile(self):
        """Load user profile information"""
        if not self.current_user:
            return
        
        self.profile_username.delete(0, tk.END)
        self.profile_username.insert(0, self.current_user[1])
        
        self.profile_email.delete(0, tk.END)
        self.profile_email.insert(0, self.current_user[3])
        
        self.profile_firstname.delete(0, tk.END)
        self.profile_firstname.insert(0, self.current_user[4])
        
        self.profile_lastname.delete(0, tk.END)
        self.profile_lastname.insert(0, self.current_user[5])
        
        self.profile_address.delete(0, tk.END)
        self.profile_address.insert(0, self.current_user[6])
        
        self.profile_phone.delete(0, tk.END)
        self.profile_phone.insert(0, self.current_user[7])

    def update_profile(self):
        """Update user profile"""
        if not self.current_user:
            return
        
        email = self.profile_email.get()
        firstname = self.profile_firstname.get()
        lastname = self.profile_lastname.get()
        address = self.profile_address.get()
        phone = self.profile_phone.get()
        password = self.profile_password.get()
        confirm_password = self.profile_confirm_password.get()
        
        if not all([email, firstname, lastname, address, phone]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        if password and password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Validate phone number format
        phone_digits = phone.replace('+91', '') if phone.startswith('+91') else phone
        if not (phone_digits.isdigit() and len(phone_digits) == 10):
            messagebox.showerror("Error", "Phone number must be exactly 10 digits")
            return
        
        full_phone = f"+91{phone_digits}"
        
        try:
            update_query = """
                UPDATE Users
                SET email = ?, firstname = ?, lastname = ?, address = ?, phone = ?
                WHERE id = ?
            """
            params = [email, firstname, lastname, address, full_phone, self.current_user[0]]
            
            if password:
                update_query = """
                    UPDATE Users
                    SET email = ?, firstname = ?, lastname = ?, address = ?, phone = ?, password = ?
                    WHERE id = ?
                """
                params = [email, firstname, lastname, address, full_phone, self.hash_password(password), self.current_user[0]]
            
            self.cur.execute(update_query, params)
            self.conn.commit()
            
            self.cur.execute("SELECT * FROM Users WHERE id = ?", (self.current_user[0],))
            self.current_user = self.cur.fetchone()
            
            messagebox.showinfo("Success", "Profile updated successfully")
            self.profile_password.delete(0, tk.END)
            self.profile_confirm_password.delete(0, tk.END)
            self.status_var.set(f"Welcome, {self.current_user[4]} {self.current_user[5]}")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists")

    def add_product(self):
        """Add new product (admin)"""
        if not self.current_user or self.current_user[1] != "admin":
            return
        
        product_window = tk.Toplevel(self.root)
        product_window.title("Add Product")
        product_window.geometry("400x500")
        
        fields = [
            ("Name:", "name"),
            ("Description:", "description"),
            ("Price:", "price"),
            ("Stock Quantity:", "stock"),
            ("Category:", "category")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(product_window, text=label).grid(row=i, column=0, sticky=tk.W, pady=10)
            if key == "description":
                entry = ScrolledText(product_window, wrap=tk.WORD, width=30, height=5)
                entry.grid(row=i, column=1, pady=10)
            elif key == "category":
                entry = ttk.Combobox(product_window, width=27)
                self.cur.execute("SELECT name FROM Categories")
                entry['values'] = [row[0] for row in self.cur.fetchall()]
                entry.grid(row=i, column=1, pady=10)
            else:
                entry = ttk.Entry(product_window, width=30)
                entry.grid(row=i, column=1, pady=10)
            entries[key] = entry
        
        def submit_product():
            name = entries['name'].get()
            description = entries['description'].get("1.0", tk.END).strip()
            price = entries['price'].get()
            stock = entries['stock'].get()
            category = entries['category'].get()
            
            if not all([name, price, stock, category]):
                messagebox.showerror("Error", "All fields except description are required")
                return
            
            try:
                price = float(price)
                stock = int(stock)
                
                self.cur.execute("SELECT id FROM Categories WHERE name = ?", (category,))
                category_id = self.cur.fetchone()
                if not category_id:
                    messagebox.showerror("Error", "Invalid category")
                    return
                
                self.cur.execute("""
                    INSERT INTO Products (name, description, price, stock_quantity, category_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, description, price, stock, category_id[0]))
                self.conn.commit()
                
                messagebox.showinfo("Success", "Product added successfully")
                self.load_products()
                product_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Price must be a number and stock must be an integer")
        
        ttk.Button(product_window, text="Add Product", command=submit_product).grid(row=len(fields), column=0, columnspan=2, pady=15)

    def update_product(self):
        """Update existing product (admin)"""
        if not self.current_user or self.current_user[1] != "admin":
            return
        
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product")
            return
        
        product_id = self.products_tree.item(selected[0])['values'][0]
        
        product_window = tk.Toplevel(self.root)
        product_window.title("Update Product")
        product_window.geometry("400x500")
        
        self.cur.execute("SELECT name, description, price, stock_quantity, category_id FROM Products WHERE id = ?", (product_id,))
        product = self.cur.fetchone()
        
        fields = [
            ("Name:", "name", product[0]),
            ("Description:", "description", product[1]),
            ("Price:", "price", str(product[2])),
            ("Stock Quantity:", "stock", str(product[3]))
        ]
        
        entries = {}
        for i, (label, key, value) in enumerate(fields):
            ttk.Label(product_window, text=label).grid(row=i, column=0, sticky=tk.W, pady=10)
            if key == "description":
                entry = ScrolledText(product_window, wrap=tk.WORD, width=30, height=5)
                entry.insert("1.0", value)
                entry.grid(row=i, column=1, pady=10)
            else:
                entry = ttk.Entry(product_window, width=30)
                entry.insert(0, value)
                entry.grid(row=i, column=1, pady=10)
            entries[key] = entry
        
        ttk.Label(product_window, text="Category:").grid(row=len(fields), column=0, sticky=tk.W, pady=10)
        category_combo = ttk.Combobox(product_window, width=27)
        self.cur.execute("SELECT name FROM Categories")
        categories = [row[0] for row in self.cur.fetchall()]
        category_combo['values'] = categories
        self.cur.execute("SELECT name FROM Categories WHERE id = ?", (product[4],))
        category_combo.set(self.cur.fetchone()[0])
        category_combo.grid(row=len(fields), column=1, pady=10)
        entries['category'] = category_combo
        
        def submit_update():
            name = entries['name'].get()
            description = entries['description'].get("1.0", tk.END).strip()
            price = entries['price'].get()
            stock = entries['stock'].get()
            category = entries['category'].get()
            
            if not all([name, price, stock, category]):
                messagebox.showerror("Error", "All fields except description are required")
                return
            
            try:
                price = float(price)
                stock = int(stock)
                
                self.cur.execute("SELECT id FROM Categories WHERE name = ?", (category,))
                category_id = self.cur.fetchone()
                if not category_id:
                    messagebox.showerror("Error", "Invalid category")
                    return
                
                self.cur.execute("""
                    UPDATE Products
                    SET name = ?, description = ?, price = ?, stock_quantity = ?, category_id = ?
                    WHERE id = ?
                """, (name, description, price, stock, category_id[0], product_id))
                self.conn.commit()
                
                messagebox.showinfo("Success", "Product updated successfully")
                self.load_products()
                product_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Price must be a number and stock must be an integer")
        
        ttk.Button(product_window, text="Update Product", command=submit_update).grid(row=len(fields)+1, column=0, columnspan=2, pady=15)

    def delete_product(self):
        """Delete selected product (admin)"""
        if not self.current_user or self.current_user[1] != "admin":
            return
        
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product")
            return
        
        product_id = self.products_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            try:
                self.cur.execute("DELETE FROM Products WHERE id = ?", (product_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Product deleted successfully")
                self.load_products()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Cannot delete product with existing orders or set items")

    def add_set(self):
        """Add new set (admin)"""
        if not self.current_user or self.current_user[1] != "admin":
            return
        
        set_window = tk.Toplevel(self.root)
        set_window.title("Add Set")
        set_window.geometry("600x600")
        
        fields = [
            ("Name:", "name"),
            ("Description:", "description"),
            ("Price:", "price"),
            ("Stock Quantity:", "stock")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(set_window, text=label).grid(row=i, column=0, sticky=tk.W, pady=10)
            if key == "description":
                entry = ScrolledText(set_window, wrap=tk.WORD, width=40, height=5)
                entry.grid(row=i, column=1, pady=10)
            else:
                entry = ttk.Entry(set_window, width=40)
                entry.grid(row=i, column=1, pady=10)
            entries[key] = entry
        
        ttk.Label(set_window, text="Select Products:").grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        products_frame = ttk.Frame(set_window)
        products_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        
        self.cur.execute("SELECT id, name FROM Products")
        products = self.cur.fetchall()
        
        selected_products = []
        for i, (pid, name) in enumerate(products):
            var = tk.BooleanVar()
            ttk.Checkbutton(products_frame, text=name, variable=var).grid(row=i//2, column=i%2, sticky=tk.W, padx=10)
            selected_products.append((pid, var))
        
        def submit_set():
            name = entries['name'].get()
            description = entries['description'].get("1.0", tk.END).strip()
            price = entries['price'].get()
            stock = entries['stock'].get()
            
            if not all([name, price, stock]):
                messagebox.showerror("Error", "Name, price, and stock quantity are required")
                return
            
            try:
                price = float(price)
                stock = int(stock)
                
                self.cur.execute("""
                    INSERT INTO Sets (name, description, price, stock_quantity)
                    VALUES (?, ?, ?, ?)
                """, (name, description, price, stock))
                set_id = self.cur.lastrowid
                
                for pid, var in selected_products:
                    if var.get():
                        self.cur.execute("""
                            INSERT INTO Set_Items (set_id, product_id)
                            VALUES (?, ?)
                        """, (set_id, pid))
                
                self.conn.commit()
                messagebox.showinfo("Success", "Set added successfully")
                self.load_sets()
                set_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Price must be a number and stock must be an integer")
        
        ttk.Button(set_window, text="Add Set", command=submit_set).grid(row=len(fields)+2, column=0, columnspan=2, pady=15)

    def update_set(self):
        """Update existing set (admin)"""
        if not self.current_user or self.current_user[1] != "admin":
            return
        
        selected = self.sets_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a set")
            return
        
        set_id = self.sets_tree.item(selected[0])['values'][0]
        
        set_window = tk.Toplevel(self.root)
        set_window.title("Update Set")
        set_window.geometry("600x600")
        
        self.cur.execute("SELECT name, description, price, stock_quantity FROM Sets WHERE id = ?", (set_id,))
        set_info = self.cur.fetchone()
        
        fields = [
            ("Name:", "name", set_info[0]),
            ("Description:", "description", set_info[1]),
            ("Price:", "price", str(set_info[2])),
            ("Stock Quantity:", "stock", str(set_info[3]))
        ]
        
        entries = {}
        for i, (label, key, value) in enumerate(fields):
            ttk.Label(set_window, text=label).grid(row=i, column=0, sticky=tk.W, pady=10)
            if key == "description":
                entry = ScrolledText(set_window, wrap=tk.WORD, width=40, height=5)
                entry.insert("1.0", value)
                entry.grid(row=i, column=1, pady=10)
            else:
                entry = ttk.Entry(set_window, width=40)
                entry.insert(0, value)
                entry.grid(row=i, column=1, pady=10)
            entries[key] = entry
        
        ttk.Label(set_window, text="Select Products:").grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        products_frame = ttk.Frame(set_window)
        products_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        
        self.cur.execute("SELECT id, name FROM Products")
        products = self.cur.fetchall()
        
        self.cur.execute("SELECT product_id FROM Set_Items WHERE set_id = ?", (set_id,))
        current_product_ids = set(row[0] for row in self.cur.fetchall())
        
        selected_products = []
        for i, (pid, name) in enumerate(products):
            var = tk.BooleanVar(value=pid in current_product_ids)
            ttk.Checkbutton(products_frame, text=name, variable=var).grid(row=i//2, column=i%2, sticky=tk.W, padx=10)
            selected_products.append((pid, var))
        
        def submit_update():
            name = entries['name'].get()
            description = entries['description'].get("1.0", tk.END).strip()
            price = entries['price'].get()
            stock = entries['stock'].get()
            
            if not all([name, price, stock]):
                messagebox.showerror("Error", "Name, price, and stock quantity are required")
                return
            
            try:
                price = float(price)
                stock = int(stock)
                
                self.cur.execute("""
                    UPDATE Sets
                    SET name = ?, description = ?, price = ?, stock_quantity = ?
                    WHERE id = ?
                """, (name, description, price, stock, set_id))
                
                self.cur.execute("DELETE FROM Set_Items WHERE set_id = ?", (set_id,))
                
                for pid, var in selected_products:
                    if var.get():
                        self.cur.execute("""
                            INSERT INTO Set_Items (set_id, product_id)
                            VALUES (?, ?)
                        """, (set_id, pid))
                
                self.conn.commit()
                messagebox.showinfo("Success", "Set updated successfully")
                self.load_sets()
                set_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Price must be a number and stock must be an integer")
        
        ttk.Button(set_window, text="Update Set", command=submit_update).grid(row=len(fields)+2, column=0, columnspan=2, pady=15)

    def delete_set(self):
        """Delete selected set (admin)"""
        if not self.current_user or self.current_user[1] != "admin":
            return
        
        selected = self.sets_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a set")
            return
        
        set_id = self.sets_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this set?"):
            try:
                self.cur.execute("DELETE FROM Set_Items WHERE set_id = ?", (set_id,))
                self.cur.execute("DELETE FROM Sets WHERE id = ?", (set_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Set deleted successfully")
                self.load_sets()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Cannot delete set with existing orders")

    def update_order_status(self):
        """Update order status (admin)"""
        if not self.current_user or self.current_user[1] != "admin":
            return
        
        order_id = simpledialog.askinteger("Order ID", "Enter Order ID:")
        if not order_id:
            return
        
        self.cur.execute("SELECT status FROM Orders WHERE id = ?", (order_id,))
        order = self.cur.fetchone()
        if not order:
            messagebox.showerror("Error", "Order not found")
            return
        
        status_window = tk.Toplevel(self.root)
        status_window.title("Update Order Status")
        status_window.geometry("300x200")
        
        ttk.Label(status_window, text="Select New Status:").pack(pady=10)
        status_var = tk.StringVar(value=order[0])
        status_combo = ttk.Combobox(status_window, textvariable=status_var, state="readonly")
        status_combo['values'] = ('pending', 'shipped', 'delivered')
        status_combo.pack(pady=10)
        
        def submit_status():
            new_status = status_var.get()
            self.cur.execute("UPDATE Orders SET status = ? WHERE id = ?", (new_status, order_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Order status updated")
            self.load_orders()
            status_window.destroy()
        
        ttk.Button(status_window, text="Update Status", command=submit_status).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = JewelryMarketplaceApp(root)
    root.mainloop()
