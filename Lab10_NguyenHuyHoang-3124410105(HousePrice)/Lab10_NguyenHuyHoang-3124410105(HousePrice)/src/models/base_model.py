from abc import ABC, abstractmethod
import joblib
from sklearn.metrics import r2_score, mean_absolute_error


class BaseModel(ABC):
    def __init__(self, name):
        self.name = name
        self.model = None

    @abstractmethod
    def build_model(self, params):
        pass

    def train(self, X_train, y_train):
        print(f">>> [Model] Đang huấn luyện thuật toán {self.name}...")
        self.model.fit(X_train, y_train)
        print(f">>> [Model] Huấn luyện {self.name} hoàn tất!")

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        predictions = self.predict(X_test)
        r2 = r2_score(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        print(
            f">>> [Evaluate] Kết quả {self.name}: R2 = {r2:.4f} | MAE = {mae:.2f} USD"
        )
        return r2, mae

    def save_model(self, path):
        joblib.dump(self.model, path)
        print(f">>> [Experiment] Đã lưu mô hình {self.name} thành công!")

    def load_model(self, path):
        self.model = joblib.load(path)
        print(f">>> [Experiment] Đã nạp lại mô hình {self.name} từ file cứng!")
