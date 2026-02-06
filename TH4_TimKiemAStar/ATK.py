import heapq as hq


def get_moves(x, y, board_size, visited):
    directions = [
        (2, 1),
        (2, -1),
        (-2, 1),
        (-2, -1),
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
    ]
    moves = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < board_size and 0 <= ny < board_size and not visited[nx][ny]:
            moves.append((nx, ny))
    return moves


def solve_knight_tour(board_size, start_pos):
    # Khởi tạo bàn cờ
    visited = [[False for _ in range(board_size)] for _ in range(board_size)]
    path = []

    def backtrack(curr_x, curr_y, step_count):
        visited[curr_x][curr_y] = True
        path.append((curr_x, curr_y))

        # Nếu đã đi hết 64 ô
        if step_count == board_size * board_size:
            return True

        # Lấy các nước đi tiếp theo
        neighbors = get_moves(curr_x, curr_y, board_size, visited)

        # TRI THỨC AKT (Heuristic Warnsdorff):
        # Sắp xếp các ô láng giềng theo số lượng nước đi tiếp theo của chúng (ưu tiên ít nhất)
        ranked_neighbors = []
        for nx, ny in neighbors:
            # Tính bậc (degree) - số lối thoát từ ô láng giềng này
            degree = len(get_moves(nx, ny, board_size, visited))
            ranked_neighbors.append((degree, nx, ny))

        # Sắp xếp theo degree tăng dần
        ranked_neighbors.sort()

        # Thử đi vào các ô có degree thấp nhất trước
        for _, nx, ny in ranked_neighbors:
            if backtrack(nx, ny, step_count + 1):
                return True

        # Nếu không đi tiếp được, quay lui
        visited[curr_x][curr_y] = False
        path.pop()
        return False

    if backtrack(start_pos[0], start_pos[1], 1):
        return path
    return None


# Chạy thử
size = 8
start = (0, 0)
result = solve_knight_tour(size, start)

if result:
    print(f"Thành công! Đường đi dài: {len(result)}")
    # In ra dạng ma trận cho đẹp
    board = [[0] * size for _ in range(size)]
    for i, (r, c) in enumerate(result):
        board[r][c] = i + 1
    for row in board:
        print(" ".join(f"{col:2d}" for col in row))
else:
    print("Không tìm thấy lời giải.")
