def solve_knight():
    with open("Knight.txt", "r") as f:
        data = f.read().split()
    n = int(data[0])
    start_x, start_y = int(data[1]), int(data[2])

    # Khởi tạo bàn cờ với giá trị 0 (chưa đi qua)
    board = [[-1 for _ in range(n)] for _ in range(n)]

    # Đánh dấu ô đầu tiên
    board[start_x][start_y] = 0

    # 8 hướng di chuyển của quân mã
    dx = [2, 1, -1, -2, -2, -1, 1, 2]
    dy = [1, 2, 2, 1, -1, -2, -2, -1]

    if backtrack_knight(start_x, start_y, 1, n, board, dx, dy):
        for row in board:
            print(" ".join(f"{item:2}" for item in row))
    else:
        print("Không có lời giải")


def backtrack_knight(x, y, move_i, n, board, dx, dy):
    if move_i == n * n:
        return True

    for i in range(8):
        next_x = x + dx[i]
        next_y = y + dy[i]
        if 0 <= next_x < n and 0 <= next_y < n and board[next_x][next_y] == -1:
            board[next_x][next_y] = move_i
            if backtrack_knight(next_x, next_y, move_i + 1, n, board, dx, dy):
                return True
            board[next_x][next_y] = -1  # Quay lui
    return False


solve_knight()
