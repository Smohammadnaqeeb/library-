import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from lib2 import Library, Admin, Student, Faculty, User

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.library = Library()
        self.current_user = None
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.show_login()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Login", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text="Username:").pack()
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack()
        tk.Label(self.main_frame, text="Password:").pack()
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack()
        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            user = self.library.login(username, password)
            if user:
                self.current_user = user
                if isinstance(user, Admin):
                    self.show_admin_dashboard()
                else:
                    self.show_user_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        tk.Button(self.main_frame, text="Login", command=do_login).pack(pady=5)
        tk.Button(self.main_frame, text="Register", command=self.show_register).pack()
        
    def show_register(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Register", font=("Arial", 16)).pack(pady=10)
        fields = ["Full Name", "Email", "Username", "Password", "Role (Student/Faculty/Admin)"]
        entries = {}
        for field in fields:
            tk.Label(self.main_frame, text=field+":").pack()
            ent = tk.Entry(self.main_frame, show="*" if "Password" in field else None)
            ent.pack()
            entries[field] = ent
        def do_register():
            name = entries["Full Name"].get().strip()
            email = entries["Email"].get().strip()
            username = entries["Username"].get().strip()
            password = entries["Password"].get().strip()
            role = entries["Role (Student/Faculty/Admin)"].get().strip().lower()
            if role not in ("student", "faculty", "admin"):
                messagebox.showerror("Error", "Role must be Student, Faculty, or Admin.")
                return
            try:
                user = self.library.register_user(name, email, username, password, role)
                messagebox.showinfo("Success", f"Registered {user.name} as {user.role}.")
                self.show_login()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(self.main_frame, text="Register", command=do_register).pack(pady=5)
        tk.Button(self.main_frame, text="Back to Login", command=self.show_login).pack()

    def show_admin_dashboard(self):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"Admin Dashboard - {self.current_user.name}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.main_frame, text="Add Book", command=self.add_book).pack(fill=tk.X)
        tk.Button(self.main_frame, text="View All Books", command=self.view_books).pack(fill=tk.X)
        tk.Button(self.main_frame, text="View All Transactions", command=self.view_transactions).pack(fill=tk.X)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(fill=tk.X, pady=10)

    def show_user_dashboard(self):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"User Dashboard - {self.current_user.name} ({self.current_user.role})", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.main_frame, text="View/Search Books", command=self.view_books).pack(fill=tk.X)
        tk.Button(self.main_frame, text="Borrow Book", command=self.borrow_book).pack(fill=tk.X)
        tk.Button(self.main_frame, text="Return Book", command=self.return_book).pack(fill=tk.X)
        tk.Button(self.main_frame, text="View My Transactions", command=self.view_my_transactions).pack(fill=tk.X)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(fill=tk.X, pady=10)

    def add_book(self):
        win = tk.Toplevel(self.root)
        win.title("Add Book")
        fields = ["Title", "Author", "ISBN", "Total Copies"]
        entries = {}
        for field in fields:
            tk.Label(win, text=field+":").pack()
            ent = tk.Entry(win)
            ent.pack()
            entries[field] = ent
        def do_add():
            try:
                title = entries["Title"].get().strip()
                author = entries["Author"].get().strip()
                isbn = entries["ISBN"].get().strip()
                total = int(entries["Total Copies"].get().strip())
                book = self.library.add_book(title, author, isbn, total)
                messagebox.showinfo("Success", f"Added book: {book.title}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(win, text="Add", command=do_add).pack(pady=5)

    def view_books(self):
        win = tk.Toplevel(self.root)
        win.title("Books")
        books = self.library.view_books()
        tree = ttk.Treeview(win, columns=("ID", "Title", "Author", "ISBN", "Available", "Total"), show="headings")
        for col in ("ID", "Title", "Author", "ISBN", "Available", "Total"):
            tree.heading(col, text=col)
        for b in books:
            tree.insert("", tk.END, values=(b.book_id, b.title, b.author, b.isbn, b.available_copies, b.total_copies))
        tree.pack(fill=tk.BOTH, expand=True)
        tk.Button(win, text="Close", command=win.destroy).pack()

    def view_transactions(self):
        win = tk.Toplevel(self.root)
        win.title("All Transactions")
        txns = self.library.list_all_transactions()
        tree = ttk.Treeview(win, columns=("TxnID", "UserID", "BookID", "Borrowed", "Due", "Returned", "Fine", "Status"), show="headings")
        for col in ("TxnID", "UserID", "BookID", "Borrowed", "Due", "Returned", "Fine", "Status"):
            tree.heading(col, text=col)
        for t in txns:
            tree.insert("", tk.END, values=(t.transaction_id, t.user_id, t.book_id, t.borrow_date.strftime("%Y-%m-%d"), t.due_date.strftime("%Y-%m-%d"), t.return_date.strftime("%Y-%m-%d") if t.return_date else "", t.fine_amount, t.status))
        tree.pack(fill=tk.BOTH, expand=True)
        tk.Button(win, text="Close", command=win.destroy).pack()

    def borrow_book(self):
        win = tk.Toplevel(self.root)
        win.title("Borrow Book")
        tk.Label(win, text="Enter Book ID to borrow:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()
        def do_borrow():
            book_id = book_id_entry.get().strip()
            try:
                txn = self.library.borrow_book(self.current_user, book_id)
                messagebox.showinfo("Success", f"Borrowed. Due: {txn.due_date.strftime('%Y-%m-%d')}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(win, text="Borrow", command=do_borrow).pack(pady=5)

    def return_book(self):
        win = tk.Toplevel(self.root)
        win.title("Return Book")
        tk.Label(win, text="Enter Book ID to return:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()
        def do_return():
            book_id = book_id_entry.get().strip()
            try:
                txn = self.library.return_book(self.current_user, book_id)
                msg = f"Returned. Fine: {txn.fine_amount}" if txn.fine_amount > 0 else "Returned successfully."
                messagebox.showinfo("Return", msg)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(win, text="Return", command=do_return).pack(pady=5)

    def view_my_transactions(self):
        win = tk.Toplevel(self.root)
        win.title("My Transactions")
        txns = self.library.list_transactions_for_user(self.current_user)
        tree = ttk.Treeview(win, columns=("TxnID", "BookID", "Borrowed", "Due", "Returned", "Fine", "Status"), show="headings")
        for col in ("TxnID", "BookID", "Borrowed", "Due", "Returned", "Fine", "Status"):
            tree.heading(col, text=col)
        for t in txns:
            tree.insert("", tk.END, values=(t.transaction_id, t.book_id, t.borrow_date.strftime("%Y-%m-%d"), t.due_date.strftime("%Y-%m-%d"), t.return_date.strftime("%Y-%m-%d") if t.return_date else "", t.fine_amount, t.status))
        tree.pack(fill=tk.BOTH, expand=True)
        tk.Button(win, text="Close", command=win.destroy).pack()

    def logout(self):
        self.current_user = None
        self.show_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
