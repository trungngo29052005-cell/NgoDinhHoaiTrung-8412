from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12346))
server_socket.listen(5)

print("[System] Đang khởi tạo bộ tham số DH 2048-bit...")
dh_parameters = dh.generate_parameters(generator=2, key_size=2048)
server_private_key = dh_parameters.generate_private_key()
server_public_key = server_private_key.public_key()

clients = {}  # Đổi thành dict lưu: {client_socket: (aes_key, username)}

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

def ghi_log(thong_bao):
    txt_logs.insert(tk.END, thong_bao + "\n")
    txt_logs.yview(tk.END)

def handle_client(client_socket, client_address):
    ghi_log(f"[+] Kết nối mới từ: {client_address}")
    try:
        # Trao đổi khóa DH giống bài cũ
        param_bytes = dh_parameters.parameter_bytes(serialization.Encoding.PEM, serialization.ParameterFormat.PKCS3)
        pub_bytes = server_public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
        
        client_socket.send(f"{len(param_bytes):04d}".encode())
        client_socket.send(param_bytes)
        client_socket.send(f"{len(pub_bytes):04d}".encode())
        client_socket.send(pub_bytes)
        
        client_pub_len = int(client_socket.recv(4).decode())
        client_pub_bytes = client_socket.recv(client_pub_len)
        client_public_key = serialization.load_pem_public_key(client_pub_bytes)
        
        shared_secret = server_private_key.exchange(client_public_key)
        aes_key = shared_secret[:16]
        
        # NHẬN USERNAME (Mã hóa bằng AES vừa tính xong)
        enc_username = client_socket.recv(1024)
        username = decrypt_message(aes_key, enc_username)
        
        clients[client_socket] = (aes_key, username)
        ghi_log(f"[✓] DH thành công. {username} gia nhập phòng.")
        
        for sock, (k, name) in clients.items():
            if sock != client_socket:
                sock.send(encrypt_message(k, f"[Hệ thống] {username} đã vào phòng."))

        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message: break
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            ghi_log(f"[{username}]: {decrypted_message}")
            
            for sock, (k, name) in clients.items():
                if sock != client_socket:
                    sock.send(encrypt_message(k, f"{username}: {decrypted_message}"))
    except:
        pass
            
    if client_socket in clients:
        username = clients[client_socket][1]
        del clients[client_socket]
        ghi_log(f"[-] {username} rời phòng.")
        for sock, (k, name) in clients.items():
            sock.send(encrypt_message(k, f"[Hệ thống] {username} đã rời phòng."))
    client_socket.close()

def accept_connections():
    ghi_log("[Hệ thống] DH-AES Server đang hoạt động ở port 12346...")
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

root = tk.Tk()
root.title("DH-AES Server Monitor")
txt_logs = scrolledtext.ScrolledText(root, width=55, height=20)
txt_logs.pack(padx=10, pady=10)
threading.Thread(target=accept_connections, daemon=True).start()
root.mainloop()