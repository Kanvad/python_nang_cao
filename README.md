# My Flask E-commerce Website

Một trang web thương mại điện tử đơn giản được xây dựng với Flask. Dự án này minh họa các chức năng cơ bản của một cửa hàng trực tuyến, bao gồm xác thực người dùng, hiển thị sản phẩm, giỏ hàng và quy trình thanh toán mô phỏng.

![home](/preview/home.png)

## 🚀 Giới thiệu dự án

Dự án này là một trang web thương mại điện tử được xây dựng bằng Python và framework Flask. Nó sử dụng SQLite làm cơ sở dữ liệu và tích hợp các chức năng cần thiết cho một cửa hàng trực tuyến, là một ví dụ tuyệt vời cho những ai muốn tìm hiểu về phát triển web với Flask.

### ✨ Các tính năng chính

-   **Xác thực người dùng:** Đăng ký, đăng nhập, và đăng xuất với mật khẩu được mã hóa an toàn.
-   **Danh sách sản phẩm:** Duyệt qua danh sách các sản phẩm có sẵn.
-   **Chi tiết sản phẩm:** Xem thông tin chi tiết cho từng sản phẩm.
-   **Giỏ hàng:** Thêm sản phẩm vào giỏ, cập nhật số lượng, và xóa mặt hàng.
-   **Thanh toán:** Một quy trình thanh toán được mô phỏng để "đặt hàng".
-   **Thiết kế đáp ứng:** Giao diện cơ bản đáp ứng sử dụng Bootstrap 5.

### 📸 Hình ảnh xem trước

![home](/preview/home.png)
| Đăng nhập | Đăng ký |
| :---: | :---: |
| ![login](/preview/login.png) | ![register](/preview/register.png) |
| **Trang sản phẩm** | **Thanh toán** |
| ![product](/preview/product.png) | ![checkout](/preview/checkout.png) |


## 🛠️ Công nghệ sử dụng

-   **Backend:** Python 3, Flask
-   **Cơ sở dữ liệu:** SQLite (quản lý bởi Flask-SQLAlchemy)
-   **Xác thực người dùng:** Flask-Login, Werkzeug (để mã hóa mật khẩu)
-   **Frontend:** HTML5, CSS3, Bootstrap 5
-   **Templating:** Jinja2

## ⚙️ Bắt đầu

Để chạy dự án này trên máy cục bộ của bạn, hãy làm theo các bước dưới đây.

### Yêu cầu

-   [Python 3.8+](https://www.python.org/downloads/)
-   [Pip](https://pip.pypa.io/en/stable/installation/) (thường đi kèm với Python)

### Cài đặt

1.  **Clone repository về máy của bạn:**
    ```sh
    git clone https://github.com/Kanvad/python_nang_cao.git
    cd python_nang_cao
    ```

2.  **Tạo và kích hoạt môi trường ảo:**
    -   Trên Windows:
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   Trên macOS/Linux:
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Cài đặt các thư viện cần thiết:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Chạy ứng dụng:**
    ```sh
    python app.py
    ```
    Ứng dụng sẽ chạy tại `http://127.0.0.1:5000`. Lần đầu tiên chạy, cơ sở dữ liệu và 20 sản phẩm mẫu sẽ được tự động tạo.

## 📂 Cấu trúc dự án

```
.
├── app.py              # File chính của ứng dụng Flask, khởi tạo và chạy server
├── database.py         # Cấu hình và khởi tạo đối tượng SQLAlchemy
├── models.py           # Định nghĩa các model (bảng) cho cơ sở dữ liệu
├── routes.py           # Định nghĩa các route (đường dẫn) và logic xử lý
├── test.py             # File để thử nghiệm các chức năng (tùy chọn)
├── requirements.txt    # Danh sách các thư viện Python cần thiết
├── .gitignore          # Các file và thư mục được Git bỏ qua
├── static/             # Chứa các file tĩnh (CSS, JS, hình ảnh)
├── templates/          # Chứa các template HTML (giao diện)
└── instance/           # Chứa file cơ sở dữ liệu SQLite (site.db)
```

## 📄 Giấy phép

Dự án này được cấp phép theo Giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.
