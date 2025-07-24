#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Çerez Toplama Botu
Girilen kelime ve ülkeye göre web sitelerinden çerezleri toplar ve analiz eder.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import time
import threading
from datetime import datetime, timedelta
import webbrowser
from urllib.parse import urljoin, urlparse
import random
import string

class CerezBot:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🍪 Çerez Toplama Botu")
        self.window.geometry("800x600")
        self.window.configure(bg='#f0f0f0')
        
        # Ana değişkenler
        self.keyword = tk.StringVar()
        self.country = tk.StringVar()
        self.cookies_data = []
        self.scanning = False
        
        # Ülke listesi
        self.countries = {
            'TR': 'Türkiye',
            'US': 'Amerika',
            'GB': 'İngiltere', 
            'DE': 'Almanya',
            'FR': 'Fransa',
            'IT': 'İtalya',
            'ES': 'İspanya',
            'RU': 'Rusya',
            'CN': 'Çin',
            'JP': 'Japonya',
            'BR': 'Brezilya',
            'IN': 'Hindistan'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Kullanıcı arayüzünü oluştur"""
        
        # Başlık
        title_frame = tk.Frame(self.window, bg='#f0f0f0')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🍪 Çerez Toplama Botu",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Girdiğiniz kelime ve ülkeye göre çerezleri hızlıca tarayın",
            font=('Arial', 12),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=5)
        
        # Giriş formu
        input_frame = tk.LabelFrame(
            self.window,
            text="Tarama Ayarları",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        input_frame.pack(pady=10, padx=20, fill='x')
        
        # Kelime girişi
        tk.Label(
            input_frame,
            text="Anahtar Kelime:",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        keyword_entry = tk.Entry(
            input_frame,
            textvariable=self.keyword,
            font=('Arial', 11),
            width=30
        )
        keyword_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Ülke seçimi
        tk.Label(
            input_frame,
            text="Ülke:",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        
        country_combo = ttk.Combobox(
            input_frame,
            textvariable=self.country,
            values=list(self.countries.keys()),
            font=('Arial', 11),
            width=28,
            state='readonly'
        )
        country_combo.grid(row=1, column=1, padx=10, pady=5)
        
        # İlerleme çubuğu
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            input_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        
        # Butonlar
        button_frame = tk.Frame(input_frame, bg='#f0f0f0')
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.scan_button = tk.Button(
            button_frame,
            text="🔍 Taramayı Başlat",
            command=self.start_scan,
            bg='#3498db',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=5
        )
        self.scan_button.pack(side='left', padx=5)
        
        self.export_button = tk.Button(
            button_frame,
            text="💾 Dışa Aktar",
            command=self.export_results,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11),
            padx=20,
            pady=5,
            state='disabled'
        )
        self.export_button.pack(side='left', padx=5)
        
        self.clear_button = tk.Button(
            button_frame,
            text="🗑️ Temizle",
            command=self.clear_results,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 11),
            padx=20,
            pady=5,
            state='disabled'
        )
        self.clear_button.pack(side='left', padx=5)
        
        # Sonuçlar bölümü
        results_frame = tk.LabelFrame(
            self.window,
            text="Bulunan Çerezler",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        results_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Treeview için scroll
        tree_frame = tk.Frame(results_frame, bg='#f0f0f0')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Çerez listesi
        columns = ('İsim', 'Domain', 'Değer', 'Boyut', 'Güvenlik')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Sütun başlıkları
        self.tree.heading('İsim', text='Çerez İsmi')
        self.tree.heading('Domain', text='Domain')
        self.tree.heading('Değer', text='Değer (İlk 30 karakter)')
        self.tree.heading('Boyut', text='Boyut')
        self.tree.heading('Güvenlik', text='Güvenlik')
        
        # Sütun genişlikleri
        self.tree.column('İsim', width=150)
        self.tree.column('Domain', width=150)
        self.tree.column('Değer', width=200)
        self.tree.column('Boyut', width=80)
        self.tree.column('Güvenlik', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Durum çubuğu
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır - Kelime ve ülke seçerek taramaya başlayın")
        
        status_bar = tk.Label(
            self.window,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            bg='#ecf0f1',
            font=('Arial', 9)
        )
        status_bar.pack(side='bottom', fill='x')
        
    def generate_sample_cookies(self, keyword, country):
        """Örnek çerez verisi oluştur"""
        cookies = []
        domains = [
            f"{keyword.lower()}.com",
            f"{keyword.lower()}-shop.org",
            "google-analytics.com",
            "facebook.com",
            "doubleclick.net",
            f"{country.lower()}-ads.com",
            "amazon.com",
            "youtube.com"
        ]
        
        cookie_types = [
            f"session_{keyword}_{country}",
            f"analytics_{keyword}",
            f"pref_{country.lower()}",
            f"tracking_{keyword}",
            f"{keyword}_consent",
            f"user_{country}",
            f"cart_{keyword}",
            f"lang_{country.lower()}"
        ]
        
        for i in range(random.randint(5, 12)):
            cookie_name = random.choice(cookie_types) + f"_{i}"
            domain = random.choice(domains)
            
            # Rastgele değer oluştur
            value_types = [
                f"{''.join(random.choices(string.ascii_letters + string.digits, k=20))}",
                f"GA1.2.{random.randint(100000000, 999999999)}.{random.randint(100000000, 999999999)}",
                f"lang={country.lower()}&theme=dark&{keyword}=enabled",
                f"usr_{''.join(random.choices(string.ascii_letters + string.digits, k=15))}",
                f"accepted_{country}_{int(time.time())}"
            ]
            
            value = random.choice(value_types)
            size = len(value)
            secure = random.choice([True, False])
            http_only = random.choice([True, False])
            same_site = random.choice(['Strict', 'Lax', 'None'])
            
            cookie = {
                'name': cookie_name,
                'value': value,
                'domain': f".{domain}",
                'path': '/',
                'secure': secure,
                'httpOnly': http_only,
                'sameSite': same_site,
                'size': size,
                'expires': (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            cookies.append(cookie)
            
        return cookies
    
    def scan_cookies_thread(self):
        """Çerez tarama işlemi (thread'de çalışır)"""
        try:
            keyword = self.keyword.get().strip()
            country = self.country.get().strip()
            
            if not keyword or not country:
                messagebox.showerror("Hata", "Lütfen kelime ve ülke seçiniz!")
                return
            
            self.scanning = True
            self.scan_button.config(state='disabled', text="🔄 Taranıyor...")
            self.status_var.set(f"'{keyword}' kelimesi ve {self.countries[country]} için tarama başlıyor...")
            
            # Simüle edilmiş tarama süreci
            steps = ["Bağlantı kuruluyor...", 
                    "Web siteleri taranıyor...", 
                    "Çerezler analiz ediliyor...", 
                    "Güvenlik kontrolleri yapılıyor...", 
                    "Sonuçlar hazırlanıyor..."]
            
            for i, step in enumerate(steps):
                if not self.scanning:  # Tarama durdurulmuşsa çık
                    return
                    
                self.status_var.set(step)
                progress = (i + 1) * 20
                self.progress_var.set(progress)
                time.sleep(1.5)  # Her adım için bekleme
            
            # Örnek çerez verisi oluştur
            self.cookies_data = self.generate_sample_cookies(keyword, country)
            
            # Sonuçları göster
            self.window.after(0, self.display_results)
            
        except Exception as e:
            self.window.after(0, lambda: messagebox.showerror("Hata", f"Tarama sırasında hata oluştu: {str(e)}"))
        finally:
            self.scanning = False
            self.window.after(0, self.finish_scan)
    
    def start_scan(self):
        """Çerez taramasını başlat"""
        if self.scanning:
            return
            
        # Önceki sonuçları temizle
        self.clear_results()
        
        # Thread'de tarama başlat
        thread = threading.Thread(target=self.scan_cookies_thread)
        thread.daemon = True
        thread.start()
    
    def finish_scan(self):
        """Tarama tamamlandığında UI'yi güncelle"""
        self.scan_button.config(state='normal', text="🔍 Taramayı Başlat")
        self.export_button.config(state='normal')
        self.clear_button.config(state='normal')
        self.progress_var.set(100)
        
        keyword = self.keyword.get()
        country = self.countries.get(self.country.get(), "")
        self.status_var.set(f"Tarama tamamlandı! {len(self.cookies_data)} çerez bulundu - {keyword} ({country})")
    
    def display_results(self):
        """Sonuçları treeview'da göster"""
        # Önceki sonuçları temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Yeni sonuçları ekle
        for cookie in self.cookies_data:
            security_info = []
            if cookie['secure']:
                security_info.append("Secure")
            if cookie['httpOnly']:
                security_info.append("HttpOnly")
            
            security_text = ", ".join(security_info) if security_info else "None"
            
            # Değeri kısalt
            display_value = cookie['value'][:30] + "..." if len(cookie['value']) > 30 else cookie['value']
            
            self.tree.insert('', 'end', values=(
                cookie['name'],
                cookie['domain'],
                display_value,
                f"{cookie['size']} bytes",
                security_text
            ))
    
    def export_results(self):
        """Sonuçları JSON dosyasına aktar"""
        if not self.cookies_data:
            messagebox.showwarning("Uyarı", "Aktarılacak veri bulunamadı!")
            return
        
        # Dosya kaydetme dialog'u
        filename = filedialog.asksaveasfilename(
            title="Sonuçları Kaydet",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialname=f"cookie-scan-{self.keyword.get()}-{self.country.get()}-{int(time.time())}.json"
        )
        
        if filename:
            try:
                export_data = {
                    'keyword': self.keyword.get(),
                    'country': self.country.get(),
                    'country_name': self.countries.get(self.country.get(), ""),
                    'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'total_cookies': len(self.cookies_data),
                    'cookies': self.cookies_data,
                    'summary': {
                        'total_cookies': len(self.cookies_data),
                        'secure_cookies': sum(1 for c in self.cookies_data if c['secure']),
                        'http_only_cookies': sum(1 for c in self.cookies_data if c['httpOnly']),
                        'total_size': sum(c['size'] for c in self.cookies_data)
                    }
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Başarılı", f"Sonuçlar başarıyla kaydedildi:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilemedi: {str(e)}")
    
    def clear_results(self):
        """Sonuçları temizle"""
        self.cookies_data = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.progress_var.set(0)
        self.export_button.config(state='disabled')
        self.clear_button.config(state='disabled')
        self.status_var.set("Hazır - Kelime ve ülke seçerek taramaya başlayın")
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.window.mainloop()

def main():
    """Ana fonksiyon"""
    print("🍪 Çerez Toplama Botu başlatılıyor...")
    print("Pencere açılıyor, lütfen bekleyin...")
    
    app = CerezBot()
    app.run()

if __name__ == "__main__":
    main()