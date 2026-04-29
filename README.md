AI Waste Classifier - Hệ thống Phân loại rác thông minh

Đồ án cuối kỳ môn: Các nền tảng phát triển phần mềm

 Thành viên thực hiện
SVTH1: Nguyễn Hà Thu – 2474802010376
SVTH2: Nguyễn Phạm Trọng Khang – [MSSV]
Giới thiệu dự án
Đây là hệ thống sử dụng Trí tuệ nhân tạo (AI) để phân loại rác từ hình ảnh.
Người dùng có thể upload ảnh, hệ thống sẽ dự đoán loại rác và lưu kết quả vào database, đồng thời hiển thị thống kê trên dashboard.
Hệ thống được xây dựng theo pipeline hoàn chỉnh:
AI Model → Backend API → Database → Dashboard → Cloud
Tính năng chính
📸 Upload ảnh và phân loại rác bằng AI
📊 Dashboard thống kê trực quan (Bar chart + Pie chart)
🗄️ Lưu lịch sử phân loại vào database
⚡ API xử lý nhanh với FastAPI
☁️ Deploy trên cloud (Railway)
🐳 Đóng gói bằng Docker
Công nghệ sử dụng
Backend
Python
FastAPI
AI / Machine Learning
TensorFlow
Keras
Model .h5 từ Teachable Machine
Database
MongoDB
MongoDB Atlas (cloud)
Frontend (Dashboard)
HTML, CSS, Bootstrap
Chart.js
DevOps
Docker
Railway (Cloud Deployment)
🌐 Demo hệ thống
📊 Dashboard:
https://ai-ph-n-lo-i-r-c-production.up.railway.app/dashboard
https://ai-ph-n-lo-i-r-c-production.up.railway.app/docs
⚙️ Cách chạy dự án (Local)
🔹 Cách 1: Dùng Docker (Khuyến khích)
docker-compose up --build
Sau đó truy cập:
http://localhost:8000/docs
http://localhost:8000/dashboard
🔹 Cách 2: Chạy thủ công
pip install -r requirements.txtuvicorn app.main:app --reload
⚠️ Lưu ý về Model AI
File model .h5 có dung lượng lớn nên không bao gồm trong file nộp
Model đầy đủ được lưu tại GitHub hoặc nguồn ngoài
👉 Khi chạy cần đặt model tại:
app/models/keras_model.h5
🗄️ Cấu trúc thư mục
WasteClassifier_AI/ ├── app/ │    ├── main.py │    ├── ai_engine.py │    ├── database.py │    └── models/ │         └── keras_model.h5 ├── requirements.txt ├── Dockerfile ├── docker-compose.yml └── README.md
🔄 Quy trình hoạt động
Người dùng upload ảnh
Backend xử lý và preprocess ảnh
AI model dự đoán loại rác
Kết quả được lưu vào MongoDB
Dashboard hiển thị thống kê
🎯 Hướng phát triển
Cải thiện độ chính xác model
Mở rộng thêm loại rác
Xây dựng frontend hoàn chỉnh (web/mobile)
Tối ưu hiệu năng và scale hệ thống
📌 Ghi chú
File nộp đã được rút gọn để đáp ứng yêu cầu dung lượng (<100MB)
Source code đầy đủ và model AI có tại GitHub
🏁 Kết luận
Hệ thống đã xây dựng thành công một pipeline AI hoàn chỉnh từ xử lý ảnh → dự đoán → lưu trữ → hiển thị → deploy cloud, có thể mở rộng thành ứng dụng thực tế trong tương lai.
