import cv2
import numpy as np
import serial
import time
from cvzone.HandTrackingModule import HandDetector

# 1. Hubungkan ke Arduino (Sesuaikan 'COM4' dengan port Arduino-mu!)
try:
    arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)
    time.sleep(2) # Tunggu sirkuit Arduino siap setelah reset otomatis
    print("Berhasil terhubung ke Arduino!")
except:
    print("Gagal terhubung! Periksa nomor Port COM Arduino di device manager.")
    exit()

# 2. Inisialisasi Detektor Tangan dari cvzone
detector = HandDetector(detectionCon=0.7, maxHands=1)

# Buka Kamera (0 biasanya webcam bawaan laptop)
cap = cv2.VideoCapture(0)

# Set ukuran frame kamera agar presisi dengan kanvas programmu
lebar_cam, tinggi_cam = 480, 300
cap.set(cv2.CAP_PROP_FRAME_WIDTH, lebar_cam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, tinggi_cam)

# Variabel pembatas (debounce) agar perintah tidak terkirim terus-menerus
last_command = ""
cooldown_time = 0.5  # Detik jeda antar pengiriman data
last_cmd_time = time.time()

def kirim_perintah(cmd, log_msg):
    global last_command, last_cmd_time
    current_time = time.time()
    if cmd != last_command or (current_time - last_cmd_time > cooldown_time):
        print(log_msg)
        arduino.write(cmd.encode())
        last_command = cmd
        last_cmd_time = current_time

while True:
    success, img = cap.read()
    if not success:
        print("Gagal membaca kamera")
        break

    # Balik gambar kamera (seperti cermin)
    img = cv2.flip(img, 1)
    
    # Deteksi tangan
    hands, img = detector.findHands(img, draw=True)
    
    # Koordinat ujung jari telunjuk awal (di luar layar)
    index_x, index_y = -1, -1

    # Jika tangan terdeteksi
    if hands:
        hand1 = hands[0]
        lmList = hand1["lmList"] # Daftar 21 titik koordinat tangan
        
        # Titik nomor 8 adalah UJUNG JARI TELUNJUK
        index_x, index_y = lmList[8][0], lmList[8][1]
        
        # Gambar lingkaran penanda di ujung jari telunjuk kamu
        cv2.circle(img, (index_x, index_y), 10, (255, 0, 0), cv2.FILLED)

    # --- LOGIKA DETEKSI JARI DI ATAS BUTTON (POSISI SUDAH DITUKAR) ---
    if 100 <= index_y <= 170:
        # SEKARANG KOTAK PERTAMA (X: 30-150) ADALAH MERAH
        if 30 <= index_x <= 150:
            kirim_perintah('M', "Telunjuk menunjuk MERAH -> LED Merah Aktif (Pin 11)")
            
        # SEKARANG KOTAK KEDUA (X: 180-300) ADALAH KUNING
        elif 180 <= index_x <= 300:
            kirim_perintah('K', "Telunjuk menunjuk KUNING -> LED Kuning Aktif (Pin 12)")
            
        # KOTAK KETIGA (X: 330-450) TETAP HIJAU
        elif 330 <= index_x <= 450:
            kirim_perintah('H', "Telunjuk menunjuk HIJAU -> LED Hijau Aktif (Pin 13)")

    # Tombol OFF (X: 190-290, Y: 210-260)
    elif 210 <= index_y <= 260 and 190 <= index_x <= 290:
        kirim_perintah('O', "Telunjuk menunjuk OFF -> Semua LED Padam")

    # --- RENDER ELEMENT VISUAL UI (WARNA DAN KATA-KATA SUDAH DITUKAR) ---
    # Kotak Pertama (Sekarang: Warna MERAH murni, teks MERAH)
    cv2.rectangle(img, (30, 100), (150, 170), (0, 0, 255), -1)
    cv2.putText(img, "MERAH", (55, 142), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Kotak Kedua (Sekarang: Warna KUNING murni, teks KUNING)
    cv2.rectangle(img, (180, 100), (300, 170), (0, 255, 255), -1)
    cv2.putText(img, "KUNING", (205, 142), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    # Kotak Ketiga (Tetap: Warna Hijau, teks HIJAU)
    cv2.rectangle(img, (330, 100), (450, 170), (0, 200, 0), -1)
    cv2.putText(img, "HIJAU", (360, 142), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Render Tombol OFF
    cv2.rectangle(img, (190, 210), (290, 260), (80, 80, 80), -1)
    cv2.putText(img, "OFF", (223, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Header Teks Judul
    cv2.putText(img, "Sistem Kontrol LED via Jari Telunjuk (cvzone)", (30, 50), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Tampilkan output kamera langsung ke jendela utama
    cv2.imshow("Kontrol 3 LED Arduino", img)
    
    # Tekan tombol 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()