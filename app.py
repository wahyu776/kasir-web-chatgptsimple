from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Daftar barang dan harga
barang = ["Beras", "Gula", "Minyak", "Telur", "Sabun"]
harga = [10000, 5000, 15000, 20000, 3000]

# Fungsi untuk menyimpan laporan transaksi
def simpan_laporan(barang, harga, jumlah, total_harga, pembayaran, kembalian):
    with open("laporan_transaksi.txt", "a") as file:
        file.write(f"\n--- Laporan Transaksi ---\n")
        file.write(f"Tanggal: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for i in range(len(barang)):
            if jumlah[i] > 0:
                file.write(f"{barang[i]} x {jumlah[i]} - Rp {harga[i] * jumlah[i]}\n")
        
        file.write(f"\nTotal Pembayaran: Rp {total_harga}\n")
        file.write(f"Pembayaran: Rp {pembayaran}\n")
        file.write(f"Kembalian: Rp {kembalian}\n")
        file.write("------------------------\n")

# Route untuk halaman utama kasir
@app.route("/", methods=["GET", "POST"])
def index():
    total_harga = 0
    jumlah_barang = [0] * len(barang)
    
    if request.method == "POST":
        for i in range(len(barang)):
            jumlah_barang[i] = int(request.form.get(f"jumlah_{i}", 0))
            total_harga += jumlah_barang[i] * harga[i]
        
        return redirect(url_for('struk', total_harga=total_harga, jumlah_barang=jumlah_barang))
    
    return render_template("index.html", barang=barang, harga=harga)

# Route untuk halaman struk belanja
@app.route("/struk", methods=["GET", "POST"])
def struk():
    total_harga = int(request.args.get("total_harga", 0))
    jumlah_barang = list(map(int, request.args.getlist("jumlah_barang")))
    
    pembayaran = 0
    kembalian = 0  # Menyediakan nilai default untuk kembalian
    error = None
    now = datetime.datetime.now()  # Ambil waktu saat ini
    
    if request.method == "POST":
        pembayaran = int(request.form["pembayaran"])
        if pembayaran >= total_harga:
            kembalian = pembayaran - total_harga
            # Simpan laporan transaksi
            simpan_laporan(barang, harga, jumlah_barang, total_harga, pembayaran, kembalian)
            return render_template("struk.html", barang=barang, harga=harga, jumlah_barang=jumlah_barang, total_harga=total_harga, pembayaran=pembayaran, kembalian=kembalian, now=now)
        else:
            error = "Uang tidak cukup."
            return render_template("struk.html", barang=barang, harga=harga, jumlah_barang=jumlah_barang, total_harga=total_harga, error=error, now=now, kembalian=kembalian)  # Kirimkan kembalian yang default (0)
    
    return render_template("struk.html", barang=barang, harga=harga, jumlah_barang=jumlah_barang, total_harga=total_harga, now=now, kembalian=kembalian)  # Kirimkan kembalian yang default (0)

if __name__ == "__main__":
    app.run(debug=True)

