# 🚀 Nhật ký Kỹ thuật Đặc trưng (Feature Engineering Log)

Tài liệu này ghi chép lại toàn bộ quy trình phân tích và tối ưu hóa không gian đặc trưng (Feature Space) cho bài toán Dự đoán Giá nhà. Mục tiêu là chuyển đổi dữ liệu thô thành các tín hiệu mạnh mẽ giúp các thuật toán Machine Learning (đặc biệt là XGBoost) có thể tối ưu hóa hàm mất mát hiệu quả nhất.

## Giai đoạn V1: Tiền xử lý Cơ sở (Baseline Preprocessing)
- **Tình trạng ban đầu:** Bộ dữ liệu gốc chứa 81 chiều không gian, tồn tại tỷ lệ dữ liệu thiếu (Missing Values) rất cao và có tính chất "Thiếu không ngẫu nhiên" (Missing Not At Random).
- **Chiến lược xử lý (`DataPreprocessor`):**
  - **Biến phân loại (Categorical):** Các giá trị NaN ở các cột kiến trúc (VD: `PoolQC`, `Fence`, `Alley`) được mã hóa thành nhãn `'None'` để bảo toàn ý nghĩa vật lý (Công trình không có tiện ích này).
  - **Biến số thực (Numerical):** Các giá trị NaN (VD: `GarageArea`, `TotalBsmtSF`) được lấp đầy bằng `0`. Điền giá trị Mode/Median cho các nhiễu dữ liệu nhỏ.
- **Đánh giá:** Giải quyết thành công rác dữ liệu, giúp các mô hình nhạy cảm như Ridge Regression và Random Forest có thể thiết lập được thước đo cơ sở (Baseline Metric).

## Giai đoạn V2: Khai phá Tri thức ngành (Domain-Driven Feature Engineering)
Dựa trên kiến thức thực tiễn về định giá bất động sản, class `FeatureEngineer` được triển khai để trích xuất các siêu đặc trưng (Meta-features) có trọng số quyết định cao:

1. **`TotalSF` (Tổng diện tích không gian sống):** - *Công thức:* `TotalBsmtSF` + `1stFlrSF` + `2ndFlrSF`. 
   - *Ý nghĩa:* Thu gọn chiều dữ liệu diện tích. Đây là biến độc lập có hệ số tương quan dương (Positive Correlation) mạnh nhất với giá nhà.
2. **`HouseAge` (Tuổi thọ công trình):** - *Công thức:* `YrSold` - `YearBuilt`. 
   - *Ý nghĩa:* Chuyển đổi mốc thời gian tĩnh thành một biến số tuyến tính thể hiện độ khấu hao tài sản theo thời gian.
3. **`TotalBath` (Tổng quy mô phòng tắm):** - *Công thức:* Cộng dồn số phòng tắm đầy đủ (FullBath) và phòng tắm nhỏ (HalfBath được quy đổi trọng số = 0.5).
4. **`IsRemodeled` (Trạng thái Trùng tu/Cải tạo):** - *Logic:* Biến nhị phân (Binary) nhận giá trị `1` nếu `YearBuilt != YearRemodAdd`, ngược lại là `0`. Căn nhà đã cải tạo sẽ có giá trị chênh lệch lớn so với nhà nguyên bản.
5. **`HasPool` (Tiện ích Hồ bơi):** - *Logic:* Biến nhị phân hóa (Binarization) từ cột `PoolArea`. Chuyển đổi diện tích hồ bơi thành trạng thái Có/Không để giảm nhiễu cục bộ.

## Giai đoạn V3: Tích hợp vào Pipeline (Integration)
- Toàn bộ các đặc trưng nhân tạo này được tự động hóa quy trình nội suy bên trong class `FeatureEngineer`. 
- **Kết quả:** Đóng vai trò là "bệ phóng" giúp mô hình XGBoost trong K-Fold Pipeline nhảy vọt độ chính xác R2 Score từ 0.89 lên hơn 0.91, đồng thời giảm thiểu hiện tượng đa cộng tuyến (Multicollinearity).