import heapq as hq


def heuristic(a, b):
    # Khoảng cách Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(maze, start, end):
    row, col = len(maze), len(maze[0])
    openlist = []
    hq.heappush(openlist, (0, start))

    comefrom = {}
    g = {start: 0}

    while openlist:
        currentf, current = hq.heappop(openlist)

        # Nếu đã tìm thấy đích
        if current == end:
            path = []
            while current in comefrom:
                path.append(current)
                current = comefrom[current]
            path.append(start)  # Thêm nốt điểm bắt đầu
            return path[::-1]  # Đảo ngược để có đường từ start -> end

        # VÒNG LẶP FOR PHẢI NẰM TRONG WHILE
        for dx, dy in ([-1, 0], [1, 0], [0, -1], [0, 1]):
            neighbor = (current[0] + dx, current[1] + dy)

            # Kiểm tra biên
            if 0 <= neighbor[0] < row and 0 <= neighbor[1] < col:
                # Kiểm tra vật cản
                if maze[neighbor[0]][neighbor[1]] == 1:
                    continue

                tentative_g = g[current] + 1

                if neighbor not in g or tentative_g < g[neighbor]:
                    comefrom[neighbor] = current
                    g[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, end)
                    hq.heappush(openlist, (f, neighbor))

    return None


# Chạy thử
maze = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
]
start = (0, 0)
end = (5, 5)

path = a_star(maze, start, end)
print("Path from start to end:", path)
