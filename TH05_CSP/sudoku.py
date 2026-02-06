import sys


def solve():
    # 1. Đọc tệp tin Sudoku.txt
    try:
        with open("Sudoku.txt", "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("File not found")
        return

    # 2. Tạo bảng board (chuyển chuỗi thành list để có thể chỉnh sửa)
    board = []
    for line in lines:
        board.append(list(line))

    if len(board) != 9:
        print("Dữ liệu bảng không hợp lệ (phải đủ 9 dòng)")
        return

    # 3. Hàm kiểm tra tính hợp lệ
    def valid(r, c, val):
        # Kiểm tra hàng và cột
        for i in range(9):
            if board[r][i] == val or board[i][c] == val:
                return False

        # Kiểm tra lưới ô vuông con 3x3
        start_r, start_c = 3 * (r // 3), 3 * (c // 3)
        for i in range(start_r, start_r + 3):
            for j in range(start_c, start_c + 3):
                if board[i][j] == val:
                    return False
        return True

    # 4. Thuật toán Quay lui (Backtracking)
    def backtrack():
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for val in "123456789":
                        if valid(r, c, val):
                            board[r][c] = val
                            if backtrack():
                                return True
                            board[r][c] = "."  # Quay lui
                    return False
        return True

    # 5. Thực thi và in kết quả
    if backtrack():
        for row in board:
            # Theo yêu cầu đề bài: in không dấu cách (hoặc dùng "".join)
            print("".join(row))
    else:
        print("IMPOSSIBLE")


# Gọi hàm thực thi
if __name__ == "__main__":
    solve()
