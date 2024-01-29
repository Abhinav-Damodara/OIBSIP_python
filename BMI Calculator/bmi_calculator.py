import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class BMICalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")

        # Variables for user input
        self.weight_var = tk.IntVar()
        self.height_var = tk.IntVar()

        # Variables for data storage
        self.users_data = []

        # GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry widgets
        ttk.Label(self.master, text="Weight (kg):").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        ttk.Entry(self.master, textvariable=self.weight_var).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.master, text="Height (cm):").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        ttk.Entry(self.master, textvariable=self.height_var).grid(row=1, column=1, padx=10, pady=5)

        # Calculate BMI button
        ttk.Button(self.master, text="Calculate BMI", command=self.calculate_bmi).grid(row=2, column=0, columnspan=2, pady=10)

        # Display BMI result
        self.result_label = ttk.Label(self.master, text="")
        self.result_label.grid(row=3, column=0, columnspan=2)

        # Save data and show statistics button
        ttk.Button(self.master, text="Save Data & Show Statistics", command=self.save_and_show_stats).grid(row=4, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        weight = self.weight_var.get()
        height = self.height_var.get()

        if 20 <= weight <= 300 and 100 <= height <= 300:  # Height in cm now
            bmi = weight / ((height / 100) ** 2)  # Convert height to meters
            self.result_label.config(text=f"BMI: {bmi:.2f} ({self.categorize_bmi(bmi)})")
        else:
            messagebox.showerror("Input Error", "Invalid weight or height. Please enter valid values.")

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal Weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def save_and_show_stats(self):
        weight = self.weight_var.get()
        height = self.height_var.get()
        bmi = weight / ((height / 100) ** 2)
        category = self.categorize_bmi(bmi)

        # Save user data
        self.users_data.append({"Weight": weight, "Height": height, "BMI": bmi, "Category": category})

        # Display statistics
        self.show_statistics()

    def show_statistics(self):
        if self.users_data:
            weights = [data["Weight"] for data in self.users_data]
            heights = [data["Height"] for data in self.users_data]
            bmis = [data["BMI"] for data in self.users_data]

            # Remove NaN values from BMI list
            bmis = [bmi for bmi in bmis if not np.isnan(bmi)]

            if bmis:  # Check if there are non-NaN BMI values
                # Plotting
                fig, axs = plt.subplots(2, 2, figsize=(12, 6.5))  # Adjust figure size here
                axs[0, 0].hist(weights, bins=10, color='blue', edgecolor='black')
                axs[0, 0].set_title('Weight Distribution')

                axs[0, 1].hist(heights, bins=10, color='green', edgecolor='black')
                axs[0, 1].set_title('Height Distribution')

                axs[1, 0].hist(bmis, bins=10, color='orange', edgecolor='black')
                axs[1, 0].set_title('BMI Distribution')

                # Count categories
                category_counts = {
                    "Underweight": 0,
                    "Normal Weight": 0,
                    "Overweight": 0,
                    "Obese": 0
                }

                for data in self.users_data:
                    category_counts[data["Category"]] += 1

                # Convert the counts to a list
                category_counts = list(category_counts.values())

                axs[1, 1].pie(category_counts,
                            labels=['Underweight', 'Normal Weight', 'Overweight', 'Obese'],
                            autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '')
                axs[1, 1].set_title('BMI Categories Distribution')

                # Show the plot in the GUI with a scrollbar
                canvas = FigureCanvasTkAgg(fig, master=self.master)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(row=5, column=0, columnspan=2)

                # Add a vertical scrollbar
                scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=canvas_widget.yview)
                scrollbar.grid(row=5, column=2, sticky=tk.NS)
                canvas_widget.configure(yscrollcommand=scrollbar.set)

            else:
                messagebox.showinfo("No Data", "No BMI data available for statistics.")
        else:
            messagebox.showinfo("No Data", "No user data available for statistics.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
