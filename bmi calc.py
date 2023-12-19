import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_bmi():
    weight = float(weight_entry.get())
    height = float(height_entry.get()) / 100
    bmi = weight / (height ** 2)
    bmi_label.config(text=f"BMI: {bmi:.2f}", font=("Helvetica", 14, "bold"))
    save_to_database(weight, height, bmi)
    update_bmi_trend_plot()

def save_to_database(weight, height, bmi):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS bmi_records (timestamp TEXT, weight REAL, height REAL, bmi REAL)")
    cursor.execute("INSERT INTO bmi_records VALUES (?, ?, ?, ?)", (timestamp, weight, height, bmi))
    conn.commit()
    conn.close()

def view_historical_data():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bmi_records ORDER BY timestamp DESC")
    records = cursor.fetchall()
    conn.close()

    historical_data_window = tk.Toplevel(root)
    historical_data_window.title("Historical BMI Data")
    historical_data_window.geometry("600x400")
    historical_data_window.configure(bg="#ffcc66")

    tree = ttk.Treeview(historical_data_window, columns=("Timestamp", "Weight", "Height", "BMI"), show="headings", height=10)
    tree.heading("Timestamp", text="Timestamp", anchor=tk.CENTER)
    tree.heading("Weight", text="Weight", anchor=tk.CENTER)
    tree.heading("Height", text="Height", anchor=tk.CENTER)
    tree.heading("BMI", text="BMI", anchor=tk.CENTER)

    for record in records:
        tree.insert("", "end", values=record)

    tree.pack(expand=True, fill="both", padx=20, pady=20)

def update_bmi_trend_plot():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, bmi FROM bmi_records ORDER BY timestamp")
    records = cursor.fetchall()
    conn.close()

    timestamps, bmis = zip(*records)

    plt.figure(figsize=(6, 4))
    plt.plot(timestamps, bmis, marker='o', linestyle='-', color='#008080')
    plt.title("BMI Trend Over Time", fontsize=14, fontweight='bold', color='#008080')
    plt.xlabel("Timestamp", fontsize=12, fontweight='bold', color='#008080')
    plt.ylabel("BMI", fontsize=12, fontweight='bold', color='#008080')
    plt.xticks(rotation=45)

    canvas = FigureCanvasTkAgg(plt.gcf(), master=bmi_trend_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("800x600")
root.configure(bg="#b3e0ff")

calculator_label = tk.Label(root, text="BMI Calculator", font=("Helvetica", 24, "bold"), bg="#b3e0ff", pady=10)
calculator_label.pack()

weight_label = tk.Label(root, text="Weight (kg):", font=("Helvetica", 14), bg="#b3e0ff")
weight_label.pack()
weight_entry = tk.Entry(root, font=("Helvetica", 14))
weight_entry.pack(pady=5)

height_label = tk.Label(root, text="Height (cm):", font=("Helvetica", 14), bg="#b3e0ff")
height_label.pack()
height_entry = tk.Entry(root, font=("Helvetica", 14))
height_entry.pack(pady=5)

calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi, font=("Helvetica", 14, "bold"), bg='#008080', fg='white')
calculate_button.pack(pady=10)

bmi_label = tk.Label(root, text="BMI: ", font=("Helvetica", 18, "bold"), bg="#b3e0ff")
bmi_label.pack(pady=10)

bmi_trend_frame = tk.Frame(root, bg="#b3e0ff", borderwidth=2, relief="solid", padx=20, pady=20)
bmi_trend_frame.pack(pady=20)

view_data_button = tk.Button(root, text="View Historical Data", command=view_historical_data, font=("Helvetica", 14, "bold"), bg='#ffcc66', fg='white')
view_data_button.pack(pady=10)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="BMI Calculator", menu=file_menu)
file_menu.add_command(label="View Historical Data", command=view_historical_data)

root.mainloop()
