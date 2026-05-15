input_str = input("Nhập X, Y: ")
# Tách chuỗi nhập vào bằng dấu phẩy và chuyển thành số nguyên
dimensions = [int(x) for x in input_str.split(',')]
rowNum = dimensions[0]
colNum = dimensions[1]

# Tạo một danh sách đa chiều (ma trận) chứa toàn số 0
multilist = [[0 for col in range(colNum)] for row in range(rowNum)]

# Duyệt qua từng hàng và từng cột để tính giá trị
for row in range(rowNum):
    for col in range(colNum):
        multilist[row][col] = row * col

print(multilist)