import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from caesar import Ui_call_api_decrypt_2
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_call_api_decrypt_2()
        self.ui.setupUi(self)
        self.ui.call_api_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.call_api_decrypt.clicked.connect(self.call_api_decrypt)
        # In ra thông báo để xác nhận App đã sẵn sàng
        print("App is running. Please make sure api.py is started on port 5000.")

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        key_text = self.ui.textEdit_2.toPlainText().strip()
        if not key_text:
            QMessageBox.warning(self, "Input Error", "Please enter a Key (number)!")
            return

        payload = {
            "plain_text": self.ui.textEdit.toPlainText(),
            "key": key_text
        }
        print(f"Encrypting: {payload}")
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # Lấy kết quả từ API (tương thích cả lab02 và lab03)
                cipher_result = data.get("encrypted_message") or data.get("encrypted_text", "")
                print(f"Result: {cipher_result}")
                
                self.ui.textEdit_3.setText(cipher_result)
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(f"Encrypted Successfully!\nResult: {cipher_result}")
                msg.exec_()
            else:
                error_msg = response.json().get('error', 'Unknown error')
                QMessageBox.critical(self, "API Error", f"Server Error: {error_msg}")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Connection Error", "API is NOT running! Please run 'python api.py' first.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def call_api_decrypt(self):
        # Để Decrypt hoạt động khi textEdit_3 là ReadOnly, 
        # bạn phải gán kết quả encrypt vào đó trước hoặc bỏ ReadOnly tạm thời.
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        key_text = self.ui.textEdit_2.toPlainText().strip()
        if not key_text:
            QMessageBox.warning(self, "Input Error", "Please enter a Key (number)!")
            return

        payload = {
            "cipher_text": self.ui.textEdit_3.toPlainText(),
            "key": key_text
        }
        print(f"Sending to API (Decrypt): {payload}")
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                plain_result = data.get("decrypted_message", "")
                print(f"Received from API: {plain_result}")
                self.ui.textEdit.setText(plain_result)
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                error_msg = response.json().get('error', 'Unknown error')
                QMessageBox.critical(self, "API Error", f"Server Error: {error_msg}")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Connection Error", "Cannot connect to API. Please run api.py first!")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())