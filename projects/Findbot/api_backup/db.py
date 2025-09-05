import sqlite3

def init_database():
    conn = sqlite3.connect('Findbot.db')
    cursor = conn.cursor()

    # 1. Tạo bảng nếu chưa tồn tại
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Shelves (
        shelf_id INTEGER PRIMARY KEY,
        location TEXT,
        max_capacity INTEGER
    )   
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Goods (
        good_ID INTEGER PRIMARY KEY,
        name TEXT,
        x INTEGER,
        y INTEGER,
        shelf_id INTEGER,
        FOREIGN KEY (shelf_id) REFERENCES Shelves(shelf_id)
    )
    """)

    # 2. Chỉ thêm dữ liệu mẫu nếu bảng Shelves hoặc Goods đang rỗng
    cursor.execute("SELECT COUNT(*) FROM Shelves")
    shelf_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Goods")
    goods_count = cursor.fetchone()[0]

    if shelf_count == 0 and goods_count == 0:
        # 3. Khởi tạo kệ (ví dụ 4 kệ, mỗi kệ tối đa 5 sản phẩm)
        max_capacity = 5
        num_shelves = 10
        for shelf_id in range(1, num_shelves + 1):
            cursor.execute(
                "INSERT INTO Shelves (shelf_id, location, max_capacity) VALUES (?, ?, ?)",
                (shelf_id, f"Kệ số {shelf_id}", max_capacity)
            )
    
        # 4. Danh sách sản phẩm mẫu
        product_names = [
            "Trái cây", "Rau củ", "Gạo", "Cà phê", "Trà", "Sữa", "Nước uống", "Giải khát",
            "Thịt", "Cá", "Hải sản", "Giấy", "Áo quần", "Giày dép", "Sách vở",
            "Hộp (thực phẩm đóng hộp)", "Gia vị", "Lạnh (thực phẩm đông lạnh)", 
            "Chế biến sẵn", "Đồ ăn vặt"
        ]
    
        # 5. Thêm sản phẩm, đảm bảo không trùng tọa độ và đúng sức chứa kệ
        for idx, name in enumerate(product_names):
            shelf_id = (idx // max_capacity) + 1  # Chia đều vào các kệ
            x = idx % max_capacity                # x: 0-4 trong mỗi kệ
            y = shelf_id                         # y: số kệ (hoặc có thể là idx // max_capacity)
            cursor.execute(
                "INSERT INTO Goods (name, x, y, shelf_id) VALUES (?, ?, ?, ?)",
                (name, x, y, shelf_id)
            )
    
        conn.commit()
    
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!")