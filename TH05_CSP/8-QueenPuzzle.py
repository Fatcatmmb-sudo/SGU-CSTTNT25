import os


def backtracking_queen():
    n = 8
    diemdung = [-1] * n
    cot = [False] * n
    hangcheochinh = [False] * (2 * n - 1)
    hangcheophu = [False] * (2 * n - 1)
    solutions = []  # Luu ket qua

    def backtracking(row):
        if row == n:
            board_res = []
            for r in range(n):
                line = ["."] * n
                line[diemdung[r]] = "Q"
                board_res.append(" ".join(line))
            solutions.append(board_res)
            return

        for col in range(n):
            if (
                not cot[col]
                and not hangcheochinh[row + col]
                and not hangcheophu[row - col + n - 1]
            ):

                diemdung[row] = col
                cot[col] = hangcheochinh[row + col] = hangcheophu[row - col + n - 1] = (
                    True
                )

                backtracking(row + 1)

                # Quay lui
                cot[col] = hangcheochinh[row + col] = hangcheophu[row - col + n - 1] = (
                    False
                )

    backtracking(0)

    if solutions:
        print(f"Ket qua")
        for row in solutions[0]:
            print(row)
    else:
        print("Khong tim thay ket qua")


backtracking_queen()
