# Sử dụng base image Python chính thức.
FROM python:3.11-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Thiết lập thư mục làm việc
WORKDIR /usr/src/app

# BƯỚC 1: Cài đặt Dependencies (Thường ít thay đổi)
# Sao chép requirements.txt (chỉ 1 file) để tận dụng Docker cache.
COPY requirements.txt .

# Cài đặt các dependencies
RUN pip install --no-cache-dir -r requirements.txt

# BƯỚC 2: Chuẩn bị Thư mục Dữ liệu SQLite
# Tạo thư mục 'instance' và thiết lập quyền ghi (777) để khắc phục lỗi 'unable to open database file'.
# Lưu ý: Lệnh này chỉ cần chạy 1 lần.
RUN mkdir -p instance && chmod -R 777 instance

# BƯỚC 3: Sao chép Mã nguồn (Thường xuyên thay đổi)
# Sao chép toàn bộ mã nguồn ứng dụng vào thư mục làm việc
COPY . .

# Định nghĩa cổng mà ứng dụng sẽ lắng nghe
EXPOSE 5000

# BƯỚC CUỐI: Lệnh chạy (Sử dụng Gunicorn trong production)
# Sử dụng Gunicorn (giả sử đã có trong requirements.txt)
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
CMD ["./setup.sh"]

# Nếu bạn muốn sử dụng lệnh chạy development từ docker-compose (đã đề xuất trước đó):
# CMD ["python", "app.py"]