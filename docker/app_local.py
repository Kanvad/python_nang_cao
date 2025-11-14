from flask import Flask, url_for
from database import db
from models import User, Product, CartItem, Order, OrderItem # Import TẤT CẢ các models
from flask_login import LoginManager
from routes import main
import os
import random
import click # Import click

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key'
# Đảm bảo đường dẫn tuyệt đối CHÍNH XÁC: /usr/src/app/instance/site.db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/app/instance/site.db' # <--- DOCKER: Đã BỎ COMMENT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./instance/site.db' # <--- LOCAL: ĐÃ BỎ COMMENT
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# *** THÊM CẤU HÌNH SERVER_NAME ĐỂ TẠO URL TRONG CLI ***
# Đây là tên máy chủ mà Flask sẽ sử dụng khi không có request thực tế.
app.config['SERVER_NAME'] = 'localhost:5000'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'

@login_manager.user_loader
def load_user(user_id):
    # Dùng .get() của Flask-SQLAlchemy cho tính tương thích
    return User.query.get(int(user_id))

app.register_blueprint(main)

# Định nghĩa các lệnh CLI
@app.cli.command('create-db')
def create_db_command():
    """Kiểm tra và tạo các bảng database nếu chúng chưa tồn tại (KHÔNG XÓA DỮ LIỆU)."""
    with app.app_context():
        # *** Bổ sung: Đảm bảo thư mục instance tồn tại ***
        instance_path = os.path.join(app.root_path, 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
            print(f"Đã tạo thư mục instance tại: {instance_path}")

        db.create_all() 
        print('Đã kiểm tra và tạo (nếu cần) cơ sở dữ liệu.')

@app.cli.command('seed-db')
def seed_db_command():
    """Add sample products to the database."""
    with app.app_context():
        if not Product.query.first(): # Chỉ thêm nếu chưa có sản phẩm nào
            print("Đang thêm sản phẩm mẫu theo thứ tự...")
            product_names = [
                'Áo thun cơ bản', 'Quần jean slim-fit', 'Giày sneakers trắng', 'Đồng hồ đeo tay',
                'Mũ lưỡi trai', 'Kính râm thời trang', 'Túi xách da', 'Váy maxi hoa',
                'Sơ mi công sở', 'Áo khoác bomber', 'Khuyên tai bạc', 'Dây chuyền vàng',
                'Nước hoa cao cấp', 'Son môi lì', 'Sách khoa học', 'Balo du lịch',
                'Bàn phím cơ', 'Chuột gaming', 'Tai nghe bluetooth', 'Đèn bàn LED',
            ]
            product_descriptions = [
                'Sản phẩm chất lượng cao, bền đẹp.',
                'Thiết kế hiện đại, phù hợp mọi phong cách.',
                'Thoải mái khi sử dụng, tiện lợi hàng ngày.',
                'Sự lựa chọn hoàn hảo cho bạn.',
                'Phong cách trẻ trung, năng động.',
                'Bảo vệ mắt tối ưu, phong cách sành điệu.',
                'Sang trọng và tiện dụng.',
                'Thoáng mát và nữ tính.',
                'Lịch sự và chuyên nghiệp.',
                'Ấm áp và cá tính.',
                'Phụ kiện lấp lánh cho mọi dịp.',
                'Điểm nhấn tinh tế cho trang phục.',
                'Mùi hương quyến rũ, lưu hương lâu.',
                'Màu sắc tươi tắn, giữ màu tốt.',
                'Kiến thức bổ ích, bìa cứng.',
                'Rộng rãi, chống nước.',
                'Gõ êm ái, đèn nền RGB.',
                'Độ chính xác cao, ôm tay.',
                'Âm thanh sống động, kết nối ổn định.',
                'Tiết kiệm điện, ánh sáng dịu nhẹ.',
            ]

            # Lấy danh sách tên file ảnh trong static/images
            instance_path = os.path.join(app.root_path, 'instance')
            if not os.path.exists(instance_path):
                os.makedirs(instance_path)

            image_files = [f for f in os.listdir(os.path.join(app.root_path, 'static', 'images')) if os.path.isfile(os.path.join(app.root_path, 'static', 'images', f))]
            image_files.sort()

            num_products_to_create = 20

            if len(product_names) < num_products_to_create:
                product_names = (product_names * (num_products_to_create // len(product_names) + 1))[:num_products_to_create]
            if len(product_descriptions) < num_products_to_create:
                product_descriptions = (product_descriptions * (num_products_to_create // len(product_descriptions) + 1))[:num_products_to_create]
            if len(image_files) < num_products_to_create:
                print(f"Cảnh báo: Chỉ có {len(image_files)} ảnh trong static/images. Nên có ít nhất {num_products_to_create} ảnh để tránh lặp lại nhiều. Sẽ lặp lại ảnh có sẵn.")
                image_files = (image_files * (num_products_to_create // len(image_files) + 1))[:num_products_to_create]

            for i in range(num_products_to_create):
                name = product_names[i]
                description = product_descriptions[i]
                price = random.randint(5, 200) * 10000

                with app.test_request_context():
                    image_url_for_db = url_for('static', filename=f'images/{image_files[i]}')
                
                new_product = Product(name=name, description=description, price=float(price), image_url=image_url_for_db)

                db.session.add(new_product)
            db.session.commit()
            print(f"Đã thêm {num_products_to_create} sản phẩm mẫu theo thứ tự.")
        else:
            print("Cơ sở dữ liệu đã có sản phẩm, bỏ qua việc thêm sản phẩm mẫu.")


if __name__ == '__main__':
    # Đặt debug=True để nhận lỗi trực tiếp trong trình duyệt khi phát triển
    # Bỏ host='0.0.0.0' để mặc định lắng nghe trên localhost
    app.run(port=5000, debug=True)