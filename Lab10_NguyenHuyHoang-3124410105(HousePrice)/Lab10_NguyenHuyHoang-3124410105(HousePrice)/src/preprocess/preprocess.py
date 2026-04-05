import pandas as pd
from sklearn.preprocessing import LabelEncoder


class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}

    def clean_missing_values(self, df):
        df = df.copy()

        # Các cột chữ mà NaN nghĩa là 'Không có'
        none_cols = [
            "PoolQC",
            "MiscFeature",
            "Alley",
            "Fence",
            "FireplaceQu",
            "GarageType",
            "GarageFinish",
            "GarageQual",
            "GarageCond",
            "BsmtQual",
            "BsmtCond",
            "BsmtExposure",
            "BsmtFinType1",
            "BsmtFinType2",
            "MasVnrType",
        ]
        for col in none_cols:
            if col in df.columns:
                df[col] = df[col].fillna("None")

        # Các cột số mà NaN nghĩa là 0
        zero_cols = [
            "GarageArea",
            "GarageCars",
            "BsmtFinSF1",
            "BsmtFinSF2",
            "BsmtUnfSF",
            "TotalBsmtSF",
            "BsmtFullBath",
            "BsmtHalfBath",
            "MasVnrArea",
        ]
        for col in zero_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)

        # Điền Mode cho các cột lặt vặt
        mode_cols = [
            "MSZoning",
            "Electrical",
            "KitchenQual",
            "Exterior1st",
            "Exterior2nd",
            "SaleType",
        ]
        for col in mode_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].mode()[0])

        #  Xử lý logic đặc biệt
        if "LotFrontage" in df.columns:
            df["LotFrontage"] = df.groupby("Neighborhood")["LotFrontage"].transform(
                lambda x: x.fillna(x.median())
            )

        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype == "object":
                    df[col] = df[col].fillna("Unknown")
                else:
                    df[col] = df[col].fillna(0)

        return df

    def fit_encoders(self, df):
        """Chỉ gọi 1 lần trên tập TRAIN để học các nhãn."""
        cat_cols = df.select_dtypes(include=["object"]).columns
        for col in cat_cols:
            le = LabelEncoder()
            le.fit(df[col].astype(str))
            self.label_encoders[col] = le

    def encode_categorical(self, df):
        """Dùng encoder đã fit sẵn để transform. Train và Test dùng chung bộ này."""
        df = df.copy()
        for col, le in self.label_encoders.items():
            if col in df.columns:
                # Xử lý nhãn lạ xuất hiện trong test nhưng không có trong train
                known_labels = set(le.classes_)
                df[col] = (
                    df[col]
                    .astype(str)
                    .apply(lambda x: x if x in known_labels else "Unknown")
                )
                # Đảm bảo 'Unknown' luôn có trong classes_ của encoder
                if "Unknown" not in le.classes_:
                    import numpy as np

                    le.classes_ = np.append(le.classes_, "Unknown")
                df[col] = le.transform(df[col])
        return df

    def process(self, df, is_train=False):
        """
        is_train=True  → fit encoder mới trên tập này (chỉ dùng cho Train)
        is_train=False → dùng encoder đã fit sẵn (dùng cho Test)
        """
        print(">>> [Preprocess] Bắt đầu làm sạch dữ liệu...")
        df_cleaned = self.clean_missing_values(df)
        if is_train:
            print(">>> [Preprocess] Đang học bộ mã hóa từ tập Train...")
            self.fit_encoders(df_cleaned)
        print(">>> [Preprocess] Đang chuyển đổi dữ liệu Chữ thành Số...")
        df_encoded = self.encode_categorical(df_cleaned)
        print(">>> [Preprocess] Hoàn thành!")
        return df_encoded
