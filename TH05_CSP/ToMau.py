import os


def is_safe(node, color_to_try, adj, color):
    # Kiểm tra xem có hàng xóm nào của 'node' đã tô màu 'color_to_try' chưa
    for neighbor in adj[node]:
        if color[neighbor] == color_to_try:
            return False
    return True


def backtrack(node, k, n, adj, color):
    # Nếu đã tô màu xong tất cả n thành phố
    if node > n:
        return True

    # Thử tô cho thành phố 'node' các màu từ 1 đến k
    for c in range(1, k + 1):
        if is_safe(node, c, adj, color):
            color[node] = c
            # Tiến hành tô màu cho thành phố tiếp theo
            if backtrack(node + 1, k, n, adj, color):
                return True
            # Nếu không thành công thì quay lui
            color[node] = 0
    return False


def solve():
    file_name = "Tomau.txt"

    if not os.path.exists(file_name):
        print(f"Không tìm thấy file {file_name}")
        return

    with open(file_name, "r") as f:
        inputdata = f.read().split()

    if not inputdata:
        return

    # n va m la hai thanh pho ke nhau
    n = int(inputdata[0])
    m = int(inputdata[1])

    # Xây dựng danh sách kề
    adj = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(m):
        if idx + 1 < len(inputdata):
            u = int(inputdata[idx])
            v = int(inputdata[idx + 1])
            adj[u].append(v)
            adj[v].append(u)
            idx += 2

    final_color = [0] * (n + 1)
    min_k = 0

    # Thử tìm số màu ít nhất bằng cách tăng k từ 1 đến n
    for k in range(1, n + 1):
        color = [0] * (n + 1)
        if backtrack(1, k, n, adj, color):
            min_k = k
            final_color = color
            break

    print(min_k)
    # Duyệt qua từng màu từ 1 đến min_k
    for color_idx in range(1, min_k + 1):
        group = []
        for i in range(1, n + 1):
            if final_color[i] == color_idx:
                group.append(str(i))

        if group:
            print(f"Màu {color_idx}: {' '.join(group)}")


solve()
