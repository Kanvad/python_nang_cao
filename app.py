from flask import Flask, url_for
from database import db
from models import User, Product # Import Product để có thể thêm dữ liệu mẫu
from flask_login import LoginManager
from routes import main
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key' # Thay đổi khóa bí mật này!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login' # Trang đăng nhập nếu người dùng chưa đăng nhập
login_manager.login_message_category = 'info'
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(main)

# Tạo cơ sở dữ liệu và thêm dữ liệu mẫu (chỉ chạy lần đầu)
with app.app_context():
    # db.drop_all() # Xóa cơ sở dữ liệu
    db.create_all()

    if not Product.query.first():
        print("Đang thêm 20 sản phẩm mẫu...")
        product_names = [
            'Áo thun cơ bản', 'Quần jean slim-fit', 'Giày sneakers trắng', 'Đồng hồ đeo tay',
            'Mũ lưỡi trai', 'Kính râm thời trang', 'Túi xách da', 'Váy maxi hoa',
            'Sơ mi công sở', 'Áo khoác bomber', 'Khuyên tai bạc', 'Dây chuyền vàng',
            'Nước hoa cao cấp', 'Son môi lì', 'Sách khoa học', 'Balo du lịch',
            'Bàn phím cơ', 'Chuột gaming', 'Tai nghe bluetooth', 'Đèn bàn LED'
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
            'Tiết kiệm điện, ánh sáng dịu nhẹ.'
        ]

        # Lấy danh sách tên file ảnh trong static/images
        image_files = [f for f in os.listdir(app.static_folder + '/images') if os.path.isfile(os.path.join(app.static_folder + '/images', f))]
        image_files.sort() # Sắp xếp ảnh theo thứ tự tên file để dễ quản lý

        num_products_to_create = 20 # Số lượng sản phẩm muốn tạo
        for i in range(num_products_to_create):
            # Lấy tên và mô tả theo thứ tự vòng lặp
            name = product_names[i]
            description = product_descriptions[i]
            price = random.randint(5, 200) * 10000 # Giá vẫn ngẫu nhiên

            # SỬ DỤNG CHUỖI ĐƯỜNG DẪN TƯƠNG ĐỐI
            image_url_for_db = f'/static/images/{image_files[i]}' 
            new_product = Product(name=f'{name}', description=description, price=float(price), image_url=image_url_for_db)
            
            db.session.add(new_product)
        db.session.commit()
        print(f"Đã thêm {num_products_to_create} sản phẩm mẫu theo thứ tự.")

if __name__ == '__main__':
    app.run(debug=True)