import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import psutil
import threading
import time
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NMSProcessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NMSProcess")
        self.islem_id = None
        self.izleme_aktif = threading.Event()
        self.loglar = []
        self.tema = "light"
        
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        logo = Image.open("logo.png")
        logo = logo.resize((281, 281), Image.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.frame, image=self.logo_img)
        logo_label.pack(pady=10)
        
        self.islem_listesi = ttk.Combobox(self.frame, state="readonly")
        self.islem_listesi.pack(pady=10)
        
        yenile_butonu = tk.Button(self.frame, text="İşlem Listesini Yenile", command=self.yenile_islemler)
        yenile_butonu.pack(pady=5)
        
        tema_label = tk.Label(self.frame, text="Tema Seçimi:")
        tema_label.pack(pady=5)
        self.tema_listesi = ttk.Combobox(self.frame, values=["light", "dark"], state="readonly")
        self.tema_listesi.set("light")
        self.tema_listesi.pack(pady=5)
        self.tema_listesi.bind("<<ComboboxSelected>>", self.tema_degistir)
        
        self.islem_detaylari = tk.Label(self.frame, text="")
        self.islem_detaylari.pack(pady=5)
        
        izlemeyi_baslat_butonu = tk.Button(self.frame, text="İzlemeyi Başlat", command=self.izlemeyi_baslat)
        izlemeyi_baslat_butonu.pack(pady=5)
        
        izlemeyi_durdur_butonu = tk.Button(self.frame, text="İzlemeyi Durdur", command=self.izlemeyi_durdur)
        izlemeyi_durdur_butonu.pack(pady=5)
        
        logu_kaydet_butonu = tk.Button(self.frame, text="Logu Kaydet", command=self.logu_kaydet)
        logu_kaydet_butonu.pack(pady=5)
        
        logu_ac_butonu = tk.Button(self.frame, text="Kayıtlı Log Dosyasını Aç", command=self.logu_ac)
        logu_ac_butonu.pack(pady=5)
        
        log_frame = tk.Frame(self.frame)
        log_frame.pack(pady=10, fill=tk.BOTH, expand=1)
        
        self.log_ekrani = tk.Text(log_frame, height=30, width=100)
        self.log_ekrani.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_ekrani.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_ekrani.configure(yscrollcommand=log_scrollbar.set)
        
        self.telif_hakki_label = tk.Label(self.frame, text="NMSHacking tarafından kodlandı.", fg="grey")
        self.telif_hakki_label.pack(side=tk.BOTTOM, pady=10)

        self.durum_cubugu = tk.Label(self.frame, text="Durum: Hazır", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.durum_cubugu.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.yenile_islemler()
        self.otomatik_yenile()
        
        self.fig, self.ax = plt.subplots()
        self.canvas_grafik = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_grafik.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.fig.autofmt_xdate()
        
        self.cpu_kullanim = []
        self.bellek_kullanim = []
        self.zaman = []
        
        self.root.protocol("WM_DELETE_WINDOW", self.pencereyi_kapat)

    def yenile_islemler(self):
        islemler = [f"{p.pid} - {p.name()}" for p in psutil.process_iter(['pid', 'name'])]
        self.islem_listesi['values'] = islemler
        self.durum_cubugu.config(text="Durum: İşlem listesi yenilendi")
        
    def otomatik_yenile(self):
        self.yenile_islemler()
        self.root.after(60000, self.otomatik_yenile)

    def tema_degistir(self, event):
        self.tema = self.tema_listesi.get()
        if self.tema == "dark":
            self.root.config(bg="black")
            self.frame.config(bg="black")
            self.log_ekrani.config(bg="black", fg="white")
            self.durum_cubugu.config(bg="black", fg="white")
            self.telif_hakki_label.config(bg="black", fg="grey")
        else:
            self.root.config(bg="white")
            self.frame.config(bg="white")
            self.log_ekrani.config(bg="white", fg="black")
            self.durum_cubugu.config(bg="white", fg="black")
            self.telif_hakki_label.config(bg="white", fg="grey")
    
    def izlemeyi_baslat(self):
        secim = self.islem_listesi.get()
        if not secim:
            messagebox.showwarning("Uyarı", "Lütfen bir işlem seçin!")
            return
        self.islem_id = int(secim.split(" - ")[0])
        self.izleme_aktif.set()
        self.loglar.clear()
        self.log_ekrani.delete(1.0, tk.END)
        self.izleme_thread = threading.Thread(target=self.islem_izle)
        self.izleme_thread.start()
        self.durum_cubugu.config(text="Durum: İzleme başlatıldı")
        messagebox.showinfo("Bilgi", "İzleme başlatıldı.")
        
        self.islem_detaylari.config(text=f"İzlenen İşlem: PID {self.islem_id}")

    def izlemeyi_durdur(self):
        self.izleme_aktif.clear()
        if hasattr(self, 'izleme_thread'):
            self.izleme_thread.join()
        self.durum_cubugu.config(text="Durum: İzleme durduruldu")
        messagebox.showinfo("Bilgi", "İzleme durduruldu.")
        self.islem_detaylari.config(text="")

    def logu_kaydet(self):
        if not self.loglar:
            messagebox.showwarning("Uyarı", "Kaydedilecek bir log yok.")
            return
        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if dosya_yolu:
            with open(dosya_yolu, 'w') as f:
                for log in self.loglar:
                    f.write(log + "\n")
            self.durum_cubugu.config(text="Durum: Log başarıyla kaydedildi")
            messagebox.showinfo("Bilgi", "Log başarıyla kaydedildi.")

    def logu_ac(self):
        dosya_yolu = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if dosya_yolu:
            with open(dosya_yolu, 'r') as f:
                log_icerigi = f.read()
                self.log_ekrani.delete(1.0, tk.END)
                self.log_ekrani.insert(tk.END, log_icerigi)
            self.durum_cubugu.config(text="Durum: Log dosyası açıldı")

    def islem_izle(self):
        while self.izleme_aktif.is_set():
            try:
                p = psutil.Process(self.islem_id)
                with p.oneshot():
                    cpu = p.cpu_percent(interval=1)
                    mem = p.memory_info().rss / (1024 * 1024)
                    io_counters = p.io_counters()
                    io_read = io_counters.read_bytes / (1024 * 1024)
                    io_write = io_counters.write_bytes / (1024 * 1024)
                    net_io_counters = psutil.net_io_counters()
                    net_io_sent = net_io_counters.bytes_sent / (1024 * 1024)
                    net_io_recv = net_io_counters.bytes_recv / (1024 * 1024)
                    zaman = time.strftime("%Y-%m-%d %H:%M:%S")
                    log = (f"[{zaman}] CPU: {cpu}%, Memory: {mem:.2f}MB, "
                           f"Read: {io_read:.2f}MB, Write: {io_write:.2f}MB, "
                           f"Sent: {net_io_sent:.2f}MB, Received: {net_io_recv:.2f}MB")
                    self.loglar.append(log)
                    self.log_ekrani.insert(tk.END, log + "\n")
                    self.log_ekrani.see(tk.END)
                    self.cpu_kullanim.append(cpu)
                    self.bellek_kullanim.append(mem)
                    self.zaman.append(zaman)
                    self.grafik_guncelle()
            except psutil.NoSuchProcess:
                self.loglar.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] İşlem sonlandırıldı.")
                break

    def grafik_guncelle(self):
        self.ax.clear()
        self.ax.plot(self.zaman, self.cpu_kullanim, label="CPU Kullanımı (%)")
        self.ax.plot(self.zaman, self.bellek_kullanim, label="Bellek Kullanımı (MB)")
        self.ax.legend()
        self.ax.set_xticks([]) 
        self.canvas_grafik.draw()

    def pencereyi_kapat(self):
        self.izleme_aktif.clear()
        if hasattr(self, 'izleme_thread'):
            self.izleme_thread.join()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1366x768")
    app = NMSProcessApp(root)
    root.mainloop()

