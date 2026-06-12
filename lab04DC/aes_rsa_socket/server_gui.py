from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
server_key = RSA.generate(2048)
clients = {}  # Đổi thành dict để lưu: {client_socket: (aes_key, username)}

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
    ghi_log(f"[+] Có kết nối mới từ: {client_address}")
    try:
        # Bắt tay mã hóa giống cũ
        client_socket.send(server_key.publickey().export_key(format='PEM'))
        client_received_key = RSA.import_key(client_socket.recv(2048))
        aes_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(client_received_key)
        client_socket.send(cipher_rsa.encrypt(aes_key))
        
        # NHẬN USERNAME (Đã được mã hóa AES)
        enc_username = client_socket.recv(1024)
        username = decrypt_message(aes_key, enc_username)
        
        clients[client_socket] = (aes_key, username)
        ghi_log(f"[✓] {username} ({client_address[1]}) đã gia nhập phòng chat.")
        
        # Thông báo cho người khác biết
        for sock, (key, name) in clients.items():
            if sock != client_socket:
                sock.send(encrypt_message(key, f"[Hệ thống] {username} đã vào phòng."))

        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message: break
                
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            ghi_log(f"[{username}]: {decrypted_message}")
            
            # Gửi tin nhắn kèm theo Username của người gửi
            for sock, (key, name) in clients.items():
                if sock != client_socket:
                    encrypted = encrypt_message(key, f"{username}: {decrypted_message}")
                    sock.send(encrypted)
    except:
        pass
            
    if client_socket in clients:
        username = clients[client_socket][1]
        del clients[client_socket]
        ghi_log(f"[-] {username} đã rời phòng.")
        for sock, (key, name) in clients.items():
            sock.send(encrypt_message(key, f"[Hệ thống] {username} đã rời phòng."))
    client_socket.close()

def accept_connections():
    ghi_log("[Hệ thống] RSA-AES Server đang chạy ở port 12345...")
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

root = tk.Tk()
root.title("RSA-AES Server Monitor")
txt_logs = scrolledtext.ScrolledText(root, width=55, height=20)
txt_logs.pack(padx=10, pady=10)
threading.Thread(target=accept_connections, daemon=True).start()
root.mainloop()