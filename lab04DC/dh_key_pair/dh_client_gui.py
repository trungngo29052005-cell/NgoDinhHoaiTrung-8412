from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
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
        client_socket.connect(('localhost', 12346))

        # Nhận tham số DH từ Server
        param_len = int(client_socket.recv(4).decode())
        param_bytes = client_socket.recv(param_len)
        dh_parameters = serialization.load_pem_parameters(param_bytes)

        server_pub_len = int(client_socket.recv(4).decode())
        server_pub_bytes = client_socket.recv(server_pub_len)
        server_public_key = serialization.load_pem_public_key(server_pub_bytes)

        # Tạo khóa DH Client và gửi lên
        client_private_key = dh_parameters.generate_private_key()
        client_public_key = client_private_key.public_key()
        my_pub_bytes = client_public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
        
        client_socket.send(f"{len(my_pub_bytes):04d}".encode())
        client_socket.send(my_pub_bytes)

        # Tính toán khóa AES
        shared_secret = client_private_key.exchange(server_public_key)
        aes_key = shared_secret[:16]

        # GỬI USERNAME SANG (Đã được mã hóa an toàn)
        client_socket.send(encrypt_message(aes_key, username))

        # Đổi giao diện chat
        khung_dang_nhap.pack_forget()
        khung_chat_giao_dien.pack(padx=10, pady=10)
        root.title(f"DH-AES Chat - {username}")

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
root.title("Đăng nhập phòng chat DH")
root.geometry("450x450")

khung_dang_nhap = tk.Frame(root)
khung_dang_nhap.pack(pady=150)
tk.Label(khung_dang_nhap, text="Nhập tên hiển thị DH:", font=("Helvetica", 11)).pack()
o_username = tk.Entry(khung_dang_nhap, width=25, font=("Helvetica", 11))
o_username.pack(pady=10)
tk.Button(khung_dang_nhap, text="Kết nối an toàn", command=ket_noi_server, bg="#008CBA", fg="white").pack()

khung_chat_giao_dien = tk.Frame(root)
khung_chat = scrolledtext.ScrolledText(khung_chat_giao_dien, width=50, height=18)
khung_chat.pack(pady=5)
o_nhap = tk.Entry(khung_chat_giao_dien, width=35)
o_nhap.pack(side=tk.LEFT, pady=10)
o_nhap.bind("<Return>", lambda event: gui_tin_nhan())
tk.Button(khung_chat_giao_dien, text="Gửi", command=gui_tin_nhan, width=8).pack(side=tk.RIGHT, pady=10)

root.mainloop()