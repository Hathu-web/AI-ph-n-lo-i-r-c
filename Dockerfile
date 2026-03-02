# Sử dụng Python phiên bản gọn nhẹ
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép danh sách thư viện và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Lệnh để chạy API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]