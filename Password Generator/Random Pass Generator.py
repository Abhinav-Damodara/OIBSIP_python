import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip

class PasswordGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator")

        self.length_label = ttk.Label(master, text="Password Length:")
        self.length_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)

        self.length_entry = ttk.Entry(master, width=5)
        self.length_entry.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)
        self.length_entry.insert(tk.END, "12")  # default length

        self.complexity_label = ttk.Label(master, text="Password Complexity:")
        self.complexity_label.grid(row=1, column=0, pady=10, padx=10, sticky=tk.W)

        self.complexity_var = tk.StringVar()
        self.complexity_var.set("Medium")

        self.complexity_combobox = ttk.Combobox(master, values=["Low", "Medium", "High"], textvariable=self.complexity_var)
        self.complexity_combobox.grid(row=1, column=1, pady=10, padx=10, sticky=tk.W)
        self.complexity_combobox.set("Medium")

        self.include_rules_var = tk.BooleanVar()
        self.include_rules_checkbox = ttk.Checkbutton(master, text="Include Security Rules", variable=self.include_rules_var)
        self.include_rules_checkbox.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W)

        self.generate_button = ttk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W + tk.E)

        self.password_entry = ttk.Entry(master, show="*", state="readonly", width=20)
        self.password_entry.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W + tk.E)

        self.copy_button = ttk.Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W + tk.E)

    def generate_password(self):
        length = int(self.length_entry.get())
        complexity = self.complexity_var.get()
        include_rules = self.include_rules_var.get()

        if complexity == "Low":
            chars = string.ascii_letters + string.digits
        elif complexity == "Medium":
            chars = string.ascii_letters + string.digits + string.punctuation
        else:
            chars = string.ascii_letters + string.digits + string.punctuation + string.ascii_letters.upper()

        if include_rules:
            chars = self.remove_confusing_chars(chars)

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_entry.config(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(tk.END, password)
        self.password_entry.config(state="readonly")

    def remove_confusing_chars(self, chars):
        # Remove visually confusing characters like 'l', 'I', 'O', '0', '1'
        confusing_chars = "lIO01"
        return ''.join(c for c in chars if c not in confusing_chars)

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            print("Password copied to clipboard")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()