# 🛠️ Nhật ký Tái cấu trúc Mã nguồn (Refactoring Notes)

Dự án Dự đoán Giá nhà (House Prices) ban đầu được viết gộp chung trong một file Jupyter Notebook duy nhất, gây khó khăn cho việc quản lý và nâng cấp. Để đáp ứng tiêu chuẩn của một dự án Machine Learning thực tế, nhóm đã tiến hành tái cấu trúc (Refactoring) toàn bộ hệ thống theo chuẩn Lập trình hướng đối tượng (OOP) và bám sát quy trình làm việc của các chuyên gia Data Science.

## Giai đoạn 1: Modularization (Chia để trị - Tách file OOP)
- Phân rã Notebook khổng lồ ban đầu thành các module độc lập đặt trong thư mục `src/`:
  - `src/preprocess/preprocess.py`: Chuyên xử lý dữ liệu thiếu (Missing Values) và mã hóa (Encoding).
  - `src/features/features.py`: Chuyên tạo đặc trưng mới (Feature Engineering - TotalSF, HouseAge...).
  - `src/models/`: Chứa các thuật toán được bọc trong class (`base_model.py`, `xgboost_model.py`).
- **Ưu điểm:** Tuân thủ nguyên lý SOLID. Code gọn gàng, file nào hỏng sửa file đó mà không làm sập toàn hệ thống.

## Giai đoạn 2: Đổi chiến lược - Dùng Notebook làm "Nhạc trưởng"
- Xóa bỏ các file chạy Terminal rườm rà (`train.py`, `predict.py`).
- Triển khai chiến lược Orchestrator thông qua các file Notebook:
  - `version1_EDA_Baseline.ipynb`: Phân tích dữ liệu và chạy thuật toán cơ bản.
  - `version2_Model_Tuning.ipynb`: Cải tiến đặc trưng và so sánh các thuật toán (Ridge, RF, XGBoost).
  - `version3_KFold_Pipeline.ipynb`: Phiên bản chốt hạ với kiến trúc tối ưu nhất.
- **Ưu điểm:** Giúp việc báo cáo đồ án trực quan hơn, thầy cô có thể chạy từng ô (cell) và xem biểu đồ ngay lập tức.

## Giai đoạn 3: Nâng cấp Validation với K-Fold Pipeline
- **Vấn đề:** Đánh giá bằng phương pháp Train/Test Split (70/30) truyền thống ở V1 và V2 dễ bị sai lệch do yếu tố ngẫu nhiên khi chia tập Test, dễ gây hiện tượng quá khớp (Overfitting).
- **Giải pháp:** Xây dựng file `src/pipeline/BasePipeline.py` áp dụng **Stratified K-Fold Cross Validation (5 Folds)**.
- **Kết quả:** - Đánh giá mô hình khách quan và toàn diện hơn trên toàn bộ dữ liệu.
  - Hệ thống tự động đóng băng (Persistence) 5 mô hình thành các file `.pkl` lưu tại `experiments/data/processed/` để tái sử dụng sau này (Ensemble).

## Giai đoạn 4: Quản lý Log và Báo cáo tự động
- Tự động hóa việc tạo thư mục `reports/` để lưu trữ biểu đồ trực quan (EDA, Missing Values, K-Fold Performance) và xuất thẳng file `submission.csv` sẵn sàng nộp lên Kaggle.