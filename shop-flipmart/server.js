// ------------------------------
// Import thư viện
// ------------------------------
const express = require("express");
const bodyParser = require("body-parser");
const sqlite3 = require("sqlite3").verbose();
const path = require("path");

// ------------------------------
// Cấu hình cơ bản
// ------------------------------
const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname)); // cho phép truy cập file tĩnh như HTML, CSS, JS

// ------------------------------
// Kết nối CSDL SQLite
// ------------------------------
const dbPath = path.join(__dirname, "thoitrang.db");
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error("❌ Lỗi kết nối database:", err.message);
  } else {
    console.log("✅ Kết nối SQLite thành công:", dbPath);
  }
});

// ------------------------------
// Route chính
// ------------------------------

// Trang đăng nhập (sign-in)
app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "sign-in.html"));
});

// ------------------------------
// Xử lý đăng nhập
// ------------------------------
app.post("/login", (req, res) => {
  const { mail, password } = req.body;

  const query = `SELECT * FROM users WHERE mail = ? AND password = ?`;
  db.get(query, [mail, password], (err, user) => {
    if (err) {
      console.error("Lỗi truy vấn:", err.message);
      return res
        .status(500)
        .send(`<script>alert("Lỗi máy chủ!"); window.location.href='/login';</script>`);
    }

    if (!user) {
      return res.send(
        `<script>alert("Sai email hoặc mật khẩu!"); window.location.href='/login';</script>`
      );
    }

    // Nếu đúng -> chuyển hướng tới trang home.html
    res.send(
      `<script>alert("Đăng nhập thành công, chào ${user.name}!"); window.location.href='/home.html';</script>`
    );
  });
});

// ------------------------------
// Xử lý đăng ký tài khoản mới
// ------------------------------
app.post("/register", (req, res) => {
  const { name, mail, password, confirm_password } = req.body;

  if (password !== confirm_password) {
    return res.send(
      `<script>alert("Mật khẩu xác nhận không khớp!"); window.location.href='/login';</script>`
    );
  }

  const checkQuery = `SELECT mail FROM users WHERE mail = ?`;
  db.get(checkQuery, [mail], (err, row) => {
    if (err) {
      console.error("Lỗi truy vấn:", err.message);
      return res
        .status(500)
        .send(`<script>alert("Lỗi máy chủ!"); window.location.href='/login';</script>`);
    }

    if (row) {
      return res.send(
        `<script>alert("Email đã tồn tại! Vui lòng dùng email khác."); window.location.href='/login';</script>`
      );
    }

    const insertQuery = `INSERT INTO users (name, mail, password) VALUES (?, ?, ?)`;
    db.run(insertQuery, [name, mail, password], (err) => {
      if (err) {
        console.error("Lỗi thêm user:", err.message);
        return res.send(
          `<script>alert("Đăng ký thất bại!"); window.location.href='/login';</script>`
        );
      }
      res.send(
        `<script>alert("Đăng ký thành công! Hãy đăng nhập."); window.location.href='/login';</script>`
      );
    });
  });
});

// ------------------------------
// Khởi động server
// ------------------------------
app.listen(port, () => {
  console.log(`🚀 Server đang chạy tại: http://localhost:${port}/login`);
});
