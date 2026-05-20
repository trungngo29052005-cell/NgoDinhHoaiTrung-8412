import json
from SinhVien import SinhVien

class QuanLySinhVien:
    def __init__(self):
        self.listSinhVien = []

    # Hàm tự động tạo ID tăng dần
    def generateId(self):
        maxId = 1
        if self.soLuongSinhVien() > 0:
            maxId = self.listSinhVien[0]._id
            for sv in self.listSinhVien:
                if maxId < sv._id:
                    maxId = sv._id
            maxId += 1
        return maxId

    # Trả về số lượng sinh viên hiện tại
    def soLuongSinhVien(self):
        return len(self.listSinhVien)

    # Chức năng 1: Thêm sinh viên (Đã sửa lỗi chống văng)
    def themSinhVien(self):
        print("\n1. Thêm sinh viên.")
        id = self.generateId()
        name = input("Nhập tên sinh viên: ")
        sex = input("Nhập giới tính sinh viên: ")
        major = input("Nhập chuyên ngành sinh viên: ")
        
        # Vòng lặp chặn lỗi nhập điểm
        while True:
            try:
                diemTB = float(input("Nhập điểm trung bình sinh viên: "))
                if 0 <= diemTB <= 10:
                    break
                print("❌ Lỗi: Điểm trung bình phải nằm trong khoảng từ 0 đến 10!")
            except ValueError:
                print("❌ Lỗi: Điểm phải là một số (Ví dụ: 7.5 hoặc 8)! Vui lòng nhập lại.")
        
        sv = SinhVien(id, name, sex, major, diemTB)
        self.xepLoaiHocLuc(sv)
        self.listSinhVien.append(sv)
        print("\nThêm sinh viên thành công!")

    # Chức năng 2: Cập nhật thông tin sinh viên (Đã sửa lỗi chống văng)
    def updateSinhVien(self, ID):
        sv = self.findByID(ID)
        if sv is not None:
            print(f"\nCập nhật thông tin sinh viên có ID = {ID}")
            name = input("Nhập tên sinh viên mới: ")
            sex = input("Nhập giới tính sinh viên mới: ")
            major = input("Nhập chuyên ngành sinh viên mới: ")
            
            # Vòng lặp chặn lỗi nhập điểm khi cập nhật
            while True:
                try:
                    diemTB = float(input("Nhập điểm trung bình sinh viên mới: "))
                    if 0 <= diemTB <= 10:
                        break
                    print("❌ Lỗi: Điểm trung bình phải nằm trong khoảng từ 0 đến 10!")
                except ValueError:
                    print("❌ Lỗi: Điểm phải là một số (Ví dụ: 7.5 hoặc 8)! Vui lòng nhập lại.")
            
            sv._name = name
            sv._sex = sex
            sv._major = major
            sv._diemTB = diemTB
            self.xepLoaiHocLuc(sv)
            print("\nCập nhật thông tin thành công!")
        else:
            print(f"\nSinh viên có ID = {ID} không tồn tại!")

    # Chức năng 3: Xóa sinh viên bởi ID
    def deleteById(self, ID):
        sv = self.findByID(ID)
        if sv is not None:
            self.listSinhVien.remove(sv)
            print(f"\nĐã xóa sinh viên có ID = {ID} thành công!")
            return True
        else:
            print(f"\nSinh viên có ID = {ID} không tồn tại!")
            return False

    # Chức năng 4: Tìm kiếm sinh viên theo tên
    def findByName(self, keyword):
        listSV = []
        if self.soLuongSinhVien() > 0:
            for sv in self.listSinhVien:
                if keyword.upper() in sv._name.upper():
                    listSV.append(sv)
        return listSV

    # Hàm bổ trợ: Tìm kiếm sinh viên theo ID cụ thể
    def findByID(self, ID):
        searchResult = None
        if self.soLuongSinhVien() > 0:
            for sv in self.listSinhVien:
                if sv._id == ID:
                    searchResult = sv
                    break
        return searchResult

    # Chức năng 5: Sắp xếp theo điểm trung bình
    def sortByDiemTB(self):
        self.listSinhVien.sort(key=lambda x: x._diemTB)

    # Chức năng 6: Sắp xếp theo tên
    def sortByName(self):
        self.listSinhVien.sort(key=lambda x: x._name)

    # Hàm tự động xếp loại học lực
    def xepLoaiHocLuc(self, sv: SinhVien):
        if sv._diemTB >= 8:
            sv._hocLuc = "Gioi"
        elif sv._diemTB >= 6.5:
            sv._hocLuc = "Kha"
        elif sv._diemTB >= 5:
            sv._hocLuc = "Trung binh"
        else:
            sv._hocLuc = "Yeu"

    # Chức năng 7: Hiển thị danh sách sinh viên
    def showSinhVien(self, listSV):
        print(f"{'ID':<5} {'Name':<20} {'Sex':<8} {'Major':<15} {'Diem TB':<10} {'Hoc Luc':<10}")
        print("-" * 70)
        for sv in listSV:
            print(f"{sv._id:<5} {sv._name:<20} {sv._sex:<8} {sv._major:<15} {sv._diemTB:<10.2f} {sv._hocLuc:<10}")
        print("-" * 70)

    # Chức năng 8: Ghi danh sách sinh viên vào file JSON
    def ghiDanhSachSinhVienVaoFileJson(self, filePath):
        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                json_data = [sv.__dict__ for sv in self.listSinhVien]
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            print(f"\nGhi dữ liệu vào file {filePath} thành công!")
        except Exception as e:
            print(f"\nLỗi khi ghi file JSON: {e}")

    # Chức năng 9: Đọc danh sách sinh viên từ file JSON
    def docDanhSachSinhVienTuFileJson(self, filePath):
        try:
            with open(filePath, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                self.listSinhVien = []
                for item in json_data:
                    sv = SinhVien(item['_id'], item['_name'], item['_sex'], item['_major'], item['_diemTB'])
                    sv._hocLuc = item['_hocLuc']
                    self.listSinhVien.append(sv)
            print(f"\nĐọc dữ liệu từ file {filePath} thành công!")
        except FileNotFoundError:
            print(f"\nFile {filePath} không tồn tại. Danh sách hiện đang trống.")
        except Exception as e:
            print(f"\nLỗi khi đọc file JSON: {e}")