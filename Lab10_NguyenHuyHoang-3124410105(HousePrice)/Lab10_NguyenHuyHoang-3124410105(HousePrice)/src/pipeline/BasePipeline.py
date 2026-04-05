import numpy as np
import pandas as pd
import joblib
import os
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_absolute_error


class BasePipeline:
    def __init__(self, model_name, model_instance, n_splits=5):
        self.model_name = model_name
        self.model_instance = model_instance
        self.n_splits = n_splits
        self.models = []
        self.oof_predictions = None

    def fit_predict_kfold(self, X, y, test_data=None):
        print(f" PIPELINE: {self.model_name} ({self.n_splits} Folds)")

        kf = KFold(n_splits=self.n_splits, shuffle=True, random_state=42)
        X_arr = X.values if isinstance(X, pd.DataFrame) else X
        y_arr = y.values if isinstance(y, pd.Series) else y

        self.oof_predictions = np.zeros(len(X_arr))
        test_predictions = []
        fold_scores = []

        save_dir = f"experiments/data/processed"
        os.makedirs(save_dir, exist_ok=True)

        for fold, (train_idx, val_idx) in enumerate(kf.split(X_arr)):
            print(f"\n--- Đang huấn luyện {self.model_name} - Fold {fold} ---")

            X_train, y_train = X_arr[train_idx], y_arr[train_idx]
            X_val, y_val = X_arr[val_idx], y_arr[val_idx]

            from sklearn.base import clone

            model = clone(self.model_instance)

            model.fit(X_train, y_train)
            self.models.append(model)

            val_preds = model.predict(X_val)
            self.oof_predictions[val_idx] = val_preds

            r2 = r2_score(y_val, val_preds)
            mae = mean_absolute_error(y_val, val_preds)
            fold_scores.append(r2)
            print(f"> Điểm Fold {fold}: R2 = {r2:.4f} | MAE = {mae:.2f}")

            model_path = os.path.join(save_dir, f"{self.model_name}_Fold{fold}.pkl")
            joblib.dump(model, model_path)

            if test_data is not None:
                test_preds = model.predict(test_data)
                test_predictions.append(test_preds)

        mean_r2 = np.mean(fold_scores)
        self.fold_scores_mean = mean_r2
        print("=" * 60)
        print(f"Điểm R2 Trung bình 5 Folds: {mean_r2:.4f}")
        print("=" * 60)

        final_test_preds = (
            np.mean(test_predictions, axis=0) if test_data is not None else None
        )
        return self.oof_predictions, final_test_preds
