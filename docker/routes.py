from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Product, CartItem, Order, OrderItem
from database import db
from datetime import datetime

main = Blueprint('main', __name__)

# Trang chủ
@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Đăng ký
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Tên người dùng đã tồn tại!', 'danger')
            return redirect(url_for('main.register'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email đã được sử dụng!', 'danger')
            return redirect(url_for('main.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Tài khoản đã được tạo thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

# Đăng nhập
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Chào mừng trở lại, {user.username}!', 'success')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Tên người dùng hoặc mật khẩu không đúng.', 'danger')
    return render_template('login.html')

# Đăng xuất
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất.', 'info')
    return redirect(url_for('main.index'))

# Trang danh sách sản phẩm
@main.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

# Chi tiết sản phẩm
@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# Thêm sản phẩm vào giỏ hàng
@main.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))

    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()
    flash(f'Đã thêm "{product.name}" vào giỏ hàng của bạn.', 'success')
    return redirect(url_for('main.cart'))

# Xem giỏ hàng
@main.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

# Cập nhật số lượng sản phẩm trong giỏ hàng
@main.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Bạn không có quyền chỉnh sửa mục này.', 'danger')
        return redirect(url_for('main.cart'))

    quantity = int(request.form.get('quantity'))
    if quantity <= 0:
        db.session.delete(item)
        flash('Sản phẩm đã được xóa khỏi giỏ hàng.', 'info')
    else:
        item.quantity = quantity
        flash('Số lượng sản phẩm đã được cập nhật.', 'success')
    db.session.commit()
    return redirect(url_for('main.cart'))

# Xóa sản phẩm khỏi giỏ hàng
@main.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Bạn không có quyền xóa mục này.', 'danger')
        return redirect(url_for('main.cart'))

    db.session.delete(item)
    db.session.commit()
    flash('Sản phẩm đã được xóa khỏi giỏ hàng.', 'info')
    return redirect(url_for('main.cart'))


# Thanh toán
@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Giỏ hàng của bạn đang trống.', 'warning')
        return redirect(url_for('main.index'))

    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Đây là nơi bạn sẽ tích hợp logic xử lý thanh toán thực tế (ví dụ: cổng thanh toán)
        # Hiện tại, chúng ta sẽ tạo một đơn hàng giả định.

        new_order = Order(user_id=current_user.id, total_amount=total_amount, status='Completed')
        db.session.add(new_order)
        db.session.flush() # Để có ID đơn hàng trước khi commit

        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product.id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            db.session.delete(item) # Xóa khỏi giỏ hàng sau khi tạo đơn hàng

        db.session.commit()
        flash('Đơn hàng của bạn đã được đặt thành công!', 'success')
        return redirect(url_for('main.index')) # Hoặc trang xác nhận đơn hàng

    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)