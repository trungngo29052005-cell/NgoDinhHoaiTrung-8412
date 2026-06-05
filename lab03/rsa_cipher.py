import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from rsa_ui import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect buttons to their respective functions
        self.ui.pushButton.clicked.connect(self.call_api_encrypt)
        self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)
        self.ui.pushButton_3.clicked.connect(self.call_api_sign)
        self.ui.pushButton_4.clicked.connect(self.call_api_verify)
        
        # Thông báo để người dùng biết server cần được bật
        print("RSA Controller is running. Connect to API on port 5000.")

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            # Sử dụng POST cho đồng bộ và an toàn hơn khi tạo dữ liệu mới
            response = requests.post(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
            else:
                error_info = response.json().get('error', 'Unknown error')
                QMessageBox.critical(self, "Error", f"Failed to generate keys: {error_info}")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Cannot connect to API server: {e}")

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.textEdit.toPlainText(),
            "key_type": "public"
        }
        if not payload["message"]:
            QMessageBox.warning(self, "Input Error", "Please enter Plain Text!")
            return
            
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit_2.setText(data.get("encrypted_message", ""))
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "API Error", f"Encryption failed. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Is api.py running?\n{e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.textEdit_2.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit.setText(data.get("decrypted_message", ""))
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "API Error", f"Decryption failed. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Is api.py running?\n{e}")

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.textEdit_3.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit_4.setText(data.get("signature", ""))
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Error", f"Signing failed. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"API Error: {e}")

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.textEdit_3.toPlainText(),
            "signature": self.ui.textEdit_4.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                if data.get("is_verified"):
                    msg.setText("Verified Successfully")
                else:
                    msg.setText("Verification Failed")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Error", f"Verification failed. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"API Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())