import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def buat_tabel_transaksi():
    conn = sqlite3.connect('keuangan.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jenis TEXT,
            jumlah REAL
        )
    ''')
    conn.commit()
    conn.close()

def tambah_transaksi():
    jenis = jenis_var.get()
    jumlah = jumlah_var.get()
    conn = sqlite3.connect('keuangan.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transaksi (jenis, jumlah) VALUES (?, ?)', (jenis, jumlah))
    conn.commit()
    conn.close()
    refresh_data()
    update_grafik()

def reset_data():
    conn = sqlite3.connect('keuangan.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transaksi')
    conn.commit()
    conn.close()
    refresh_data()
    update_grafik()

def hitung_statistik():
    conn = sqlite3.connect('keuangan.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(jumlah) FROM transaksi WHERE jenis="pemasukan"')
    total_pemasukan = cursor.fetchone()[0] or 0
    cursor.execute('SELECT SUM(jumlah) FROM transaksi WHERE jenis="pengeluaran"')
    total_pengeluaran = cursor.fetchone()[0] or 0
    saldo = total_pemasukan - total_pengeluaran
    conn.close()
    return total_pemasukan, total_pengeluaran, saldo

def refresh_data():
    conn = sqlite3.connect('keuangan.db')
    cursor = conn.cursor()
    cursor.execute('SELECT jenis, jumlah FROM transaksi')
    transaksi_data = cursor.fetchall()
    conn.close()
    transaksi_listbox.delete(0, tk.END)
    for data in transaksi_data:
        transaksi_listbox.insert(tk.END, f"{data[0]}: {data[1]:.2f}")

def update_grafik():
    total_pemasukan, total_pengeluaran, saldo = hitung_statistik()

    # Hapus grafik sebelum membuat yang baru
    for widget in grafik_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots()
    categories = ['Pemasukan', 'Pengeluaran', 'Saldo']
    values = [total_pemasukan, total_pengeluaran, saldo]
    ax.bar(categories, values)
    ax.set_ylabel('Jumlah')
    ax.set_title('Statistik Keuangan')

    canvas = FigureCanvasTkAgg(fig, master=grafik_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()

app = tk.Tk()
app.title("Aplikasi Keuangan")

jenis_var = tk.StringVar()
jumlah_var = tk.DoubleVar()

jenis_label = tk.Label(app, text="Jenis (pemasukan/pengeluaran):")
jenis_label.pack()

jenis_entry = tk.Entry(app, textvariable=jenis_var)
jenis_entry.pack()

jumlah_label = tk.Label(app, text="Jumlah:")
jumlah_label.pack()

jumlah_entry = tk.Entry(app, textvariable=jumlah_var)
jumlah_entry.pack()

tambah_button = tk.Button(app, text="Tambah Transaksi", command=tambah_transaksi)
tambah_button.pack()

reset_button = tk.Button(app, text="Reset Data", command=reset_data)
reset_button.pack()

transaksi_listbox = tk.Listbox(app)
transaksi_listbox.pack()

grafik_frame = tk.Frame(app)
grafik_frame.pack()

buat_tabel_transaksi()
refresh_data()
update_grafik()

app.mainloop()
