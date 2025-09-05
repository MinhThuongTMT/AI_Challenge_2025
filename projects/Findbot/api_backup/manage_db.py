import sqlite3
import json
from datetime import datetime
from tabulate import tabulate

# Connect to the existing database
conn = sqlite3.connect('Findbot.db')
cursor = conn.cursor()

# Create necessary tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Shelves (
        shelf_id INTEGER PRIMARY KEY,
        location TEXT,
        max_capacity INTEGER
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Product (
        product_id INTEGER PRIMARY KEY,
        name TEXT,
        x INTEGER,
        y INTEGER,
        shelf_id INTEGER,
        FOREIGN KEY (shelf_id) REFERENCES Shelves(shelf_id)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Findbot (
        findbot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER
    )
""")

# In-memory storage for the last deleted item
last_deleted = None

# Initialize database with sample data
def init_database():
    cursor.execute("SELECT COUNT(*) FROM Shelves")
    shelf_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Product")
    product_count = cursor.fetchone()[0]

    if shelf_count == 0 and product_count == 0:
        max_capacity = 5
        num_shelves = 10
        for shelf_id in range(1, num_shelves + 1):
            cursor.execute(
                "INSERT INTO Shelves (shelf_id, location, max_capacity) VALUES (?, ?, ?)",
                (shelf_id, f"Kệ số {shelf_id}", max_capacity)
            )
        
        product_names = [
            "Trái cây", "Rau củ", "Gạo", "Cà phê", "Trà", "Sữa", "Nước uống", "Giải khát",
            "Thịt", "Cá", "Hải sản", "Giấy", "Áo quần", "Giày dép", "Sách vở",
            "Hộp (thực phẩm đóng hộp)", "Gia vị", "Lạnh (thực phẩm đông lạnh)", 
            "Chế biến sẵn", "Đồ ăn vặt"
        ]
        
        for idx, name in enumerate(product_names):
            shelf_id = (idx // max_capacity) + 1
            x = idx % max_capacity
            y = shelf_id
            cursor.execute(
                "INSERT INTO Product (name, x, y, shelf_id) VALUES (?, ?, ?, ?)",
                (name, x, y, shelf_id)
            )
        
        conn.commit()
    return {"status": "Database initialized successfully"}

# Find product
def find_product(product_name: str):
    cursor.execute("SELECT * FROM Product WHERE name = ?", (product_name,))
    product = cursor.fetchone()
    if product:
        return {"status": "success", "data": {
            "product_id": product[0], "name": product[1], "x": product[2], "y": product[3], "shelf_id": product[4]
        }}
    return {"status": "error", "message": "Product not found"}

# Update product location
def update_product_location(product_name: str, new_shelf_id: int, new_x: int, new_y: int):
    cursor.execute("SELECT shelf_id FROM Product WHERE name = ?", (product_name,))
    current_shelf = cursor.fetchone()
    if not current_shelf:
        return {"status": "error", "message": "Product not found"}
    
    current_shelf_id = current_shelf[0]
    cursor.execute("SELECT max_capacity FROM Shelves WHERE shelf_id = ?", (new_shelf_id,))
    shelf = cursor.fetchone()
    if not shelf:
        return {"status": "error", "message": "Shelf not found"}
    
    max_capacity = shelf[0]
    cursor.execute("SELECT COUNT(*) FROM Product WHERE shelf_id = ?", (new_shelf_id,))
    current_count = cursor.fetchone()[0]
    if current_count >= max_capacity and new_shelf_id != current_shelf_id:
        return {"status": "error", "message": f"Shelf {new_shelf_id} has reached max capacity of {max_capacity}"}
    
    cursor.execute("SELECT * FROM Product WHERE shelf_id = ? AND x = ? AND y = ? AND name != ?",
                   (new_shelf_id, new_x, new_y, product_name))
    if cursor.fetchone():
        return {"status": "error", "message": f"Coordinates (x={new_x}, y={new_y}) on shelf {new_shelf_id} are occupied"}
    
    cursor.execute("UPDATE Product SET shelf_id = ?, x = ?, y = ? WHERE name = ?", 
                   (new_shelf_id, new_x, new_y, product_name))
    conn.commit()
    return {"status": "success", "message": "Product location updated successfully"}

# Update product name
def update_product_name(product_name: str, new_name: str, location: int):
    cursor.execute("SELECT * FROM Product WHERE name = ?", (product_name,))
    if not cursor.fetchone():
        return {"status": "error", "message": "Product not found"}
    
    cursor.execute("UPDATE Product SET name = ? WHERE name = ?", (new_name, product_name))
    conn.commit()
    return {"status": "success", "message": "Product name updated successfully"}

# Add findbot
def add_findbot(findbot_name: str, location_id: int):
    cursor.execute("INSERT INTO Findbot (location_id) VALUES (?)", (location_id,))
    conn.commit()
    return {"status": "success", "message": "Findbot added successfully", "findbot_id": cursor.lastrowid}

# Update findbot location
def update_findbot_location(findbot_id: int, new_location_id: int):
    cursor.execute("SELECT * FROM Findbot WHERE findbot_id = ?", (findbot_id,))
    if not cursor.fetchone():
        return {"status": "error", "message": "Findbot not found"}
    
    cursor.execute("UPDATE Findbot SET location_id = ? WHERE findbot_id = ?", (new_location_id, findbot_id))
    conn.commit()
    return {"status": "success", "message": "Findbot location updated successfully"}

# Generate report and create JSON
def generate_report():
    cursor.execute("SELECT * FROM Shelves")
    shelves = cursor.fetchall()
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM Findbot")
    findbots = cursor.fetchall()

    report = {
        "shelves": [{"shelf_id": sh[0], "location": sh[1], "max_capacity": sh[2]} for sh in shelves],
        "products": [{"product_id": p[0], "name": p[1], "x": p[2], "y": p[3], "shelf_id": p[4]} for p in products],
        "findbots": [{"findbot_id": fb[0], "location_id": fb[1]} for fb in findbots]
    }

    with open('report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
    return {"status": "success", "message": "Report generated successfully"}

# Delete product with in-memory undo
def delete_product(product_id: int):
    global last_deleted
    cursor.execute("SELECT * FROM Product WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()
    if product:
        last_deleted = product  # Store the deleted item in memory
        cursor.execute("DELETE FROM Product WHERE product_id = ?", (product_id,))
        conn.commit()
        return {"status": "success", "message": "Product deleted successfully"}
    return {"status": "error", "message": "Product not found"}

# Undo delete using in-memory storage
def undo_delete():
    global last_deleted
    if last_deleted:
        cursor.execute("INSERT INTO Product (product_id, name, x, y, shelf_id) VALUES (?, ?, ?, ?, ?)",
                       (last_deleted[0], last_deleted[1], last_deleted[2], last_deleted[3], last_deleted[4]))
        conn.commit()
        result = {"status": "success", "message": "Product restored successfully"}
        last_deleted = None  # Clear the memory after undo
        return result
    return {"status": "error", "message": "No product to restore"}

def view_product_status():
    cursor.execute("SELECT name, x, y, shelf_id FROM Product")
    products = cursor.fetchall()
    if products:
        status_list = [{"tên sản phẩm": p[0], "tọa độ x": p[1], "tọa độ y": p[2], "kệ hiện tại lưu trữ": p[3]} for p in products]
        return {"status": "success", "data": status_list}
    return {"status": "error", "message": "No products found"}

# Main function for testing
def main():
    init_database()
    while True:
        print("\n=== QUẢN LÝ KHO HÀNG ===")
        print("1. Tìm sản phẩm")
        print("2. Cập nhật location sản phẩm")
        print("3. Cập nhật tên sản phẩm")
        print("4. Thêm findbot")
        print("5. Cập nhật location findbot")
        print("6. Tạo báo cáo")
        print("7. Xóa sản phẩm")
        print("8. Hoàn tác xóa sản phẩm")
        print("9. Xem trạng thái hiện tại của hàng hóa")
        print("0. Thoát")
        print("======================")
        
        choice = input("Chọn thao tác (0-9): ")
        if choice == "1":
            product_name = input("Nhập tên sản phẩm: ")
            result = find_product(product_name)
            print(result)
        elif choice == "2":
            product_name = input("Nhập tên sản phẩm: ")
            new_shelf_id = int(input("Nhập shelf_id mới: "))
            new_x = int(input("Nhập tọa độ x mới: "))
            new_y = int(input("Nhập tọa độ y mới: "))
            result = update_product_location(product_name, new_shelf_id, new_x, new_y)
            print(result)
        elif choice == "3":
            product_name = input("Nhập tên sản phẩm hiện tại: ")
            new_name = input("Nhập tên mới: ")
            location = int(input("Nhập location (shelf_id): "))
            result = update_product_name(product_name, new_name, location)
            print(result)
        elif choice == "4":
            findbot_name = input("Nhập tên findbot: ")
            location_id = int(input("Nhập location_id: "))
            result = add_findbot(findbot_name, location_id)
            print(result)
        elif choice == "5":
            findbot_id = int(input("Nhập findbot_id: "))
            new_location_id = int(input("Nhập location_id mới: "))
            result = update_findbot_location(findbot_id, new_location_id)
            print(result)
        elif choice == "6":
            result = generate_report()
            print(result)
        elif choice == "7":
            product_id = int(input("Nhập product_id để xóa: "))
            result = delete_product(product_id)
            print(result)
        elif choice == "8":
            result = undo_delete()
            print(result)
        elif choice == "9":
            result = view_product_status()
            if result["status"] == "success":
                table_data = [[p["tên sản phẩm"], p["tọa độ x"], p["tọa độ y"], p["kệ hiện tại lưu trữ"]] for p in result["data"]]
                print(tabulate(table_data, headers=["Tên sản phẩm", "Tọa độ x", "Tọa độ y", "Kệ hiện tại lưu trữ"], tablefmt="grid"))
            else:
                print(result["message"])
        elif choice == "0":
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
    conn.close()