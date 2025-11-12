from flask import Flask
from database import db
from models import User, Product # Import Product để có thể thêm dữ liệu mẫu
from flask_login import LoginManager
from routes import main
import os

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
    db.create_all()
    # Kiểm tra xem có sản phẩm nào chưa, nếu chưa thì thêm vào
    if not Product.query.first():
        print("Adding sample products...")
        sample_products = [
            Product(name='Áo thun cơ bản', description='Áo thun cotton mềm mại, thoáng mát.', price=150000, image_url='https://via.placeholder.com/200?text=Ao+Thun'),
            Product(name='Quần jean slim-fit', description='Quần jean phong cách hiện đại, ôm dáng.', price=450000, image_url='https://via.placeholder.com/200?text=Quan+Jean'),
            Product(name='Giày sneakers trắng', description='Giày thể thao năng động, dễ phối đồ.', price=700000, image_url='https://via.placeholder.com/200?text=Giay+Sneakers'),
            Product(name='Đồng hồ đeo tay', description='Đồng hồ cơ sang trọng, mặt kính sapphire.', price=1200000, image_url='https://via.placeholder.com/200?text=Dong+Ho'),
            Product(name='Mũ lưỡi trai', description='Mũ lưỡi trai phong cách thể thao.', price=80000, image_url='https://via.placeholder.com/200?text=Mu+Luoi+Trai')
        ]
        for product in sample_products:
            db.session.add(product)
        db.session.commit()
        print("Sample products added.")

if __name__ == '__main__':
    app.run(debug=True)