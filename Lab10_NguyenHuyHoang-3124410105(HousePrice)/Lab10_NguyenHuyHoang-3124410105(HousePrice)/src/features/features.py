import pandas as pd


class FeatureEngineer:
    def __init__(self):
        pass

    def create_features(self, df):
        df = df.copy()
        print(">>> [Feature Engineering] Bắt đầu tạo các biến số mới...")

        # 1. Tổng diện tích sử dụng (Yếu tố quan trọng nhất quyết định giá nhà)
        if set(["TotalBsmtSF", "1stFlrSF", "2ndFlrSF"]).issubset(df.columns):
            df["TotalSF"] = df["TotalBsmtSF"] + df["1stFlrSF"] + df["2ndFlrSF"]

        # 2. Tổng số phòng tắm (Quy đổi phòng tắm nhỏ = 0.5)
        if set(["FullBath", "HalfBath", "BsmtFullBath", "BsmtHalfBath"]).issubset(
            df.columns
        ):
            df["TotalBath"] = (
                df["FullBath"]
                + (0.5 * df["HalfBath"])
                + df["BsmtFullBath"]
                + (0.5 * df["BsmtHalfBath"])
            )

        # 3. Tuổi đời của căn nhà (Tính từ lúc xây đến lúc bán)
        if set(["YrSold", "YearBuilt"]).issubset(df.columns):
            df["HouseAge"] = df["YrSold"] - df["YearBuilt"]

        # 4. Đánh dấu nhà đã từng được cải tạo hay chưa (1 là có, 0 là không)
        if set(["YearRemodAdd", "YearBuilt"]).issubset(df.columns):
            df["IsRemodeled"] = (df["YearRemodAdd"] != df["YearBuilt"]).astype(int)

        # 5. Đánh dấu nhà có hồ bơi hay không
        if "PoolArea" in df.columns:
            df["HasPool"] = df["PoolArea"].apply(lambda x: 1 if x > 0 else 0)

        print(
            f">>> [Feature Engineering] Hoàn thành! Dữ liệu hiện có {df.shape[1]} cột."
        )
        return df
