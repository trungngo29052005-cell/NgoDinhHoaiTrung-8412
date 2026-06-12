import hmac
import hashlib

def calculate_hmac(key, message):
    hmac_code = hmac.new(key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
    return hmac_code.hexdigest()

def main():
    key = input("Nhập khóa bí mật (Secret Key): ")
    message = input("Nhập thông điệp cần tạo mã HMAC: ")
    
    hmac_value = calculate_hmac(key, message)
    
    print("\nThông điệp:", message)
    print("Mã HMAC (SHA-256):", hmac_value)

if __name__ == "__main__":
    main()