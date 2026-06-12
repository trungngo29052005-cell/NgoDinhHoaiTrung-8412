import sys
import os
# Đảm bảo Qt tìm thấy các plugin nền tảng để hiển thị cửa sổ
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'../platforms'
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from ui.ecc import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect buttons to functions based on the provided UI layout
        self.ui.pushButton.clicked.connect(self.call_api_sign)
        self.ui.pushButton_2.clicked.connect(self.call_api_verify)
        print("ECC UI initialized successfully.")
        
        # Thêm nút Tạo Key trực tiếp vào giao diện (tương tự RSA)
        self.btn_gen_keys = QPushButton("Generate Keys", self.ui.centralwidget)
        self.btn_gen_keys.setGeometry(350, 440, 100, 30)
        self.btn_gen_keys.clicked.connect(self.call_api_gen_keys)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
            else:
                error_info = response.json().get('error', 'Unknown error')
                QMessageBox.critical(self, "Error", f"Failed to generate keys: {error_info}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"API Error: {e}")

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/ecc/sign"
        payload = {
            "message": self.ui.textEdit.toPlainText()
        }
        if not payload["message"]:
            QMessageBox.warning(self, "Input Error", "Please enter a message to sign!")
            return
            
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit_2.setText(data.get("signature", ""))
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                error_info = response.json().get('error', 'Signing failed')
                QMessageBox.critical(self, "Error", f"Error: {error_info}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"API Error: {e}")

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"
        payload = {
            "message": self.ui.textEdit.toPlainText(),
            "signature": self.ui.textEdit_2.toPlainText()
        }
        if not payload["message"] or not payload["signature"]:
            QMessageBox.warning(self, "Input Error", "Message and Signature are required!")
            return

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get("is_verified"):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verification Failed")
                    msg.exec_()
            else:
                error_info = response.json().get('error', 'Verification failed')
                QMessageBox.critical(self, "Error", f"Error: {error_info}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"API Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())