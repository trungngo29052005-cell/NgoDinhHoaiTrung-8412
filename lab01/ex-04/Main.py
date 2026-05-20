from QuanLySinhVien import QuanLySinhVien

# Khởi tạo đối tượng quản lý
qlsv = QuanLySinhVien()
file_path = "sinhvien.json"

while True:
    print("\n" + "="*15 + " CHƯƠNG TRÌNH QUẢN LÝ SINH VIÊN " + "="*15)
    print("1. Thêm sinh viên.")
    print("2. Cập nhật thông tin sinh viên bởi ID.")
    print("3. Xóa sinh viên bởi ID.")
    print("4. Tìm kiếm sinh viên theo tên.")
    print("5. Sắp xếp sinh viên theo điểm trung bình (GPA).")
    print("6. Sắp xếp sinh viên theo tên.")
    print("7. Hiển thị danh sách sinh viên.")
    print("8. Ghi danh sách sinh viên vào file JSON.")
    print("9. Đọc danh sách sinh viên từ file JSON.")
    print("0. Thoát chương trình.")
    print("=" * 62)
    
    choice = input("Nhập tùy chọn của bạn (0-9): ")
    
    if choice == "1":
        qlsv.themSinhVien()
    elif choice == "2":
        if qlsv.soLuongSinhVien() > 0:
            while True:
                try:
                    id_update = int(input("Nhập ID sinh viên cần cập nhật: "))
                    qlsv.updateSinhVien(id_update)
                    break
                except ValueError:
                    print("❌ Lỗi: ID phải là một số nguyên hợp lệ! Vui lòng nhập lại.")
        else:
            print("\nDanh sách sinh viên trống!")
    elif choice == "3":
        if qlsv.soLuongSinhVien() > 0:
            while True:
                try:
                    id_delete = int(input("Nhập ID sinh viên cần xóa: "))
                    qlsv.deleteById(id_delete)
                    break
                except ValueError:
                    print("❌ Lỗi: ID phải là một số nguyên hợp lệ! Vui lòng nhập lại.")
        else:
            print("\nDanh sách sinh viên trống!")
    elif choice == "4":
        if qlsv.soLuongSinhVien() > 0:
            name_search = input("Nhập tên sinh viên cần tìm: ")
            search_result = qlsv.findByName(name_search)
            if len(search_result) > 0:
                print(f"\nKết quả tìm kiếm cho từ khóa '{name_search}':")
                qlsv.showSinhVien(search_result)
            else:
                print(f"\nKhông tìm thấy sinh viên nào tên '{name_search}'!")
        else:
            print("\nDanh sách sinh viên trống!")
    elif choice == "5":
        if qlsv.soLuongSinhVien() > 0:
            qlsv.sortByDiemTB()
            print("\nĐã sắp xếp danh sách sinh viên theo Điểm TB!")
            qlsv.showSinhVien(qlsv.listSinhVien)
        else:
            print("\nDanh sách sinh viên trống!")
    elif choice == "6":
        if qlsv.soLuongSinhVien() > 0:
            qlsv.sortByName()
            print("\nĐã sắp xếp danh sách sinh viên theo Tên!")
            qlsv.showSinhVien(qlsv.listSinhVien)
        else:
            print("\nDanh sách sinh viên trống!")
    elif choice == "7":
        if qlsv.soLuongSinhVien() > 0:
            print(f"\nHiển thị danh sách gồm {qlsv.soLuongSinhVien()} sinh viên:")
            qlsv.showSinhVien(qlsv.listSinhVien)
        else:
            print("\nDanh sách sinh viên trống!")
    elif choice == "8":
        qlsv.ghiDanhSachSinhVienVaoFileJson(file_path)
    elif choice == "9":
        qlsv.docDanhSachSinhVienTuFileJson(file_path)
    elif choice == "0":
        print("\nĐã thoát chương trình. Tạm biệt!")
        break
    else:
        print("\nLựa chọn không hợp lệ! Vui lòng nhập lại số từ 0 đến 9.")