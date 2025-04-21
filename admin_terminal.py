import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib

class AdminTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Terminal")
        self.root.geometry("800x600")
        
        # Database connections
        self.conn_main = sqlite3.connect("jewelry_marketplace.db")
        self.conn_main.row_factory = sqlite3.Row
        self.cur_main = self.conn_main.cursor()
        self.conn_hash = sqlite3.connect("hashed_passwords.db")
        self.cur_hash = self.conn_hash.cursor()
        
        # Setup style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#2E2E2E')
        self.style.configure('TLabel', background='#2E2E2E', foreground='#FFFFFF', font=('Courier', 12))
        self.style.configure('TButton', font=('Courier', 12, 'bold'), background='#4ECDC4')
        self.style.configure('TEntry', font=('Courier', 12))
        
        # Create login frame
        self.login_frame = ttk.Frame(self.root, padding=20, style='TFrame')
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.login_frame, text="Admin Terminal Login").grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(self.login_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.username_entry = ttk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=10)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.password_entry = ttk.Entry(self.login_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=10)
        
        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Bind enter key to login
        self.root.bind('<Return>', lambda event: self.login())
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        """Handle admin login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            self.cur_main.execute("SELECT * FROM Users WHERE username = ?", (username,))
            user = self.cur_main.fetchone()
            
            if user:
                self.cur_hash.execute("SELECT hashed_password FROM HashedPasswords WHERE user_id = ?", (user['id'],))
                stored_hash = self.cur_hash.fetchone()
                
                if stored_hash and stored_hash[0] == self.hash_password(password) and username == "admin":
                    messagebox.showinfo("Success", "Login successful")
                    self.show_admin_panel()
                else:
                    messagebox.showerror("Error", "Invalid credentials or not an admin user")
            else:
                messagebox.showerror("Error", "User not found")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    
    def show_admin_panel(self):
        """Show admin panel after successful login"""
        self.login_frame.destroy()
        
        admin_frame = ttk.Frame(self.root, padding=20, style='TFrame')
        admin_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(admin_frame, text="Admin Panel").grid(row=0, column=0, columnspan=2, pady=20)
        
        # Add admin functionality buttons
        ttk.Button(admin_frame, text="View All Orders", command=self.view_orders).grid(row=1, column=0, pady=10)
        ttk.Button(admin_frame, text="Update Order Status", command=self.update_order_status).grid(row=1, column=1, pady=10)
        ttk.Button(admin_frame, text="View All Users", command=self.view_users).grid(row=2, column=0, pady=10)
        ttk.Button(admin_frame, text="Logout", command=self.logout).grid(row=3, column=0, columnspan=2, pady=20)
    
    def view_orders(self):
        """View all orders"""
        orders_window = tk.Toplevel(self.root)
        orders_window.title("All Orders")
        orders_window.geometry("800x600")
        
        tree = ttk.Treeview(orders_window, columns=("ID", "User", "Date", "Total", "Status"), show="headings")
        tree.heading("ID", text="Order ID")
        tree.heading("User", text="Username")
        tree.heading("Date", text="Date")
        tree.heading("Total", text="Total")
        tree.heading("Status", text="Status")
        
        self.cur_main.execute("""
            SELECT o.id, u.username, o.order_date, o.total_amount, o.status
            FROM Orders o
            JOIN Users u ON o.user_id = u.id
            ORDER BY o.order_date DESC
        """)
        
        for row in self.cur_main.fetchall():
            tree.insert("", tk.END, values=(row['id'], row['username'], row['order_date'], f"${row['total_amount']:.2f}", row['status']))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def update_order_status(self):
        """Update order status"""
        order_id = tk.simpledialog.askinteger("Input", "Enter Order ID:")
        if not order_id:
            return
        
        self.cur_main.execute("SELECT status FROM Orders WHERE id = ?", (order_id,))
        order = self.cur_main.fetchone()
        
        if not order:
            messagebox.showerror("Error", "Order not found")
            return
        
        status_window = tk.Toplevel(self.root)
        status_window.title("Update Order Status")
        status_window.geometry("300x200")
        
        ttk.Label(status_window, text="Select New Status:").pack(pady=10)
        status_var = tk.StringVar(value=order['status'])
        status_combo = ttk.Combobox(status_window, textvariable=status_var, state="readonly")
        status_combo['values'] = ('pending', 'shipped', 'delivered')
        status_combo.pack(pady=10)
        
        def submit_status():
            try:
                new_status = status_var.get()
                self.cur_main.execute("UPDATE Orders SET status = ? WHERE id = ?", (new_status, order_id))
                self.conn_main.commit()
                messagebox.showinfo("Success", "Order status updated")
                status_window.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")
        
        ttk.Button(status_window, text="Update Status", command=submit_status).pack(pady=15)
    
    def view_users(self):
        """View all users"""
        users_window = tk.Toplevel(self.root)
        users_window.title("All Users")
        users_window.geometry("800x600")
        
        tree = ttk.Treeview(users_window, columns=("ID", "Username", "Email", "Name"), show="headings")
        tree.heading("ID", text="User ID")
        tree.heading("Username", text="Username")
        tree.heading("Email", text="Email")
        tree.heading("Name", text="Full Name")
        
        self.cur_main.execute("SELECT id, username, email, firstname, lastname FROM Users")
        for row in self.cur_main.fetchall():
            tree.insert("", tk.END, values=(row['id'], row['username'], row['email'], f"{row['firstname']} {row['lastname']}"))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def logout(self):
        """Handle logout"""
        self.root.destroy()
    
    def __del__(self):
        """Cleanup database connections"""
        self.conn_main.close()
        self.conn_hash.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminTerminal(root)
    root.mainloop()