#!/bin/sh

# Dừng server phát triển và chạy các lệnh Flask CLI
flask create-db

# Lệnh 'flask seed-db' sẽ thêm dữ liệu mẫu
flask seed-db

# Chạy ứng dụng Flask bằng server phát triển
# Lệnh này sẽ thay thế 'python app.py' trong docker-compose.yml
exec python app.py