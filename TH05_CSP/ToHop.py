import os


def backtrack(start, n, k, a, current, result):
    if len(current) == k:
        result.append(" ".join(current))
        return

    # Duyệt qua các phần tử từ start đến n
    for i in range(start, n):
        current.append(a[i])
        # Truyền tất cả biến cần thiết vào hàm đệ quy tiếp theo
        backtrack(i + 1, n, k, a, current, result)
        current.pop()  # Quay lui


def solve():
    file_name = "Tohop.txt"
    if not os.path.exists(file_name):
        print(f"Không tìm thấy file {file_name}")
        return

    with open(file_name, "r") as f:
        all_data = f.read().split()

    if not all_data:
        return

    # N là tổng số phần tử, K là số phần tử cần lấy
    n = int(all_data[0])
    k = int(all_data[1])

    # bắt đầu từ vị trí index 2 trong all_data
    a = all_data[2 : 2 + n]

    result = []
    current = []

    # Gọi hàm backtrack và truyền tham số vào
    backtrack(0, n, k, a, current, result)

    print(len(result))
    for res in result:
        print(res)


solve()
