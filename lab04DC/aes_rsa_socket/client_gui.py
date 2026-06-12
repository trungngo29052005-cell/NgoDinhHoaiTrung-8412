from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

def ket_noi_server():
    global aes_key, client_socket
    username = o_username.get().strip()
    if not username:
        messagebox.showwarning("Chú ý", "Vui lòng nhập tên hiển thị!")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        # Thực hiện bắt tay mật mã
        client_key = RSA.generate(2048)
        server_public_key = RSA.import_key(client_socket.recv(2048))
        client_socket.send(client_key.publickey().export_key(format='PEM'))
        encrypted_aes_key = client_socket.recv(2048)

        cipher_rsa = PKCS1_OAEP.new(client_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)

        # GỬI USERNAME LÊN SERVER (Mã hóa bằng AES)
        client_socket.send(encrypt_message(aes_key, username))

        # Chuyển đổi giao diện sang phòng chat
        khung_dang_nhap.pack_forget()
        khung_chat_giao_dien.pack(padx=10, pady=10)
        root.title(f"Secure Chat - {username}")

        threading.Thread(target=nhan_tin_nhan, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể kết nối Server: {e}")

def gui_tin_nhan():
    tin_nhan = o_nhap.get()
    if not tin_nhan.strip(): return
    khung_chat.insert(tk.END, f"Bạn: {tin_nhan}\n")
    khung_chat.yview(tk.END)
    client_socket.send(encrypt_message(aes_key, tin_nhan))
    o_nhap.delete(0, tk.END)

def nhan_tin_nhan():
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message: break
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            khung_chat.insert(tk.END, decrypted_message + "\n")
            khung_chat.yview(tk.END)
        except:
            break

# --- GIAO DIỆN GUI CLIENT ---
root = tk.Tk()
root.title("Đăng nhập phòng chat")
root.geometry("450x450")

# 1. Khung đăng nhập tên ban đầu
khung_dang_nhap = tk.Frame(root)
khung_dang_nhap.pack(pady=150)
tk.Label(khung_dang_nhap, text="Nhập tên của bạn:", font=("Helvetica", 11)).pack()
o_username = tk.Entry(khung_dang_nhap, width=25, font=("Helvetica", 11))
o_username.pack(pady=10)
tk.Button(khung_dang_nhap, text="Vào Chat", command=ket_noi_server, bg="#4CAF50", fg="white").pack()

# 2. Khung chat ẩn ban đầu
khung_chat_giao_dien = tk.Frame(root)
khung_chat = scrolledtext.ScrolledText(khung_chat_giao_dien, width=50, height=18)
khung_chat.pack(pady=5)
o_nhap = tk.Entry(khung_chat_giao_dien, width=35)
o_nhap.pack(side=tk.LEFT, pady=10)
o_nhap.bind("<Return>", lambda event: gui_tin_nhan())
tk.Button(khung_chat_giao_dien, text="Gửi", command=gui_tin_nhan, width=8).pack(side=tk.RIGHT, pady=10)

root.mainloop()