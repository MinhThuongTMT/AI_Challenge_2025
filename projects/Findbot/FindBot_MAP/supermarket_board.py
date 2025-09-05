# Updated Supermarket layout - 5 rows x 4 columns = 20 shelves
# 0 = walkway (black), 1 = product shelf, 9 = entrance/exit

# Product categories mapping - 16 shelves arranged in 4 rows x 4 columns
# Each shelf is 4 cells long x 2 cells wide, double-sided with different products
PRODUCT_CATEGORIES = {
    # ROW 1 - Đồ uống và Thực phẩm khô
    # SHELF 1 - Đồ uống
    'sua_nuoc': {
        'name': 'Sua/Nuoc uong',
        'key': '1',
        'shelf_id': 1,
        'side': 'front',
        'positions': [(3,5), (3,6), (3,7), (3,8), (4,5), (4,6), (4,7), (4,8)],
        'color': (0, 255, 255),  # Cyan
        'description': 'Ke 1 (Mat truoc): Sua tuoi, sua hop, nuoc uong'
    },
    'nuoc_ngot': {
        'name': 'Nuoc ngot',
        'key': '1b',
        'shelf_id': 1,
        'side': 'back',
        'positions': [(5,5), (5,6), (5,7), (5,8), (6,5), (6,6), (6,7), (6,8)],
        'color': (100, 255, 255),  # Light Cyan
        'description': 'Ke 1 (Mat sau): Nuoc ngot, nuoc co ga'
    },

    # SHELF 2 - Gạo và Gia vị
    'gao_nep': {
        'name': 'Gao/Nep',
        'key': '2',
        'shelf_id': 2,
        'side': 'front',
        'positions': [(3,13), (3,14), (3,15), (3,16), (4,13), (4,14), (4,15), (4,16)],
        'color': (255, 255, 0),  # Yellow
        'description': 'Ke 2 (Mat truoc): Gao, nep cac loai'
    },
    'gia_vi': {
        'name': 'Gia vi',
        'key': '2b',
        'shelf_id': 2,
        'side': 'back',
        'positions': [(5,13), (5,14), (5,15), (5,16), (6,13), (6,14), (6,15), (6,16)],
        'color': (255, 255, 150),  # Light Yellow
        'description': 'Ke 2 (Mat sau): Gia vi, nuoc mam, muoi'
    },

    # SHELF 3 - Bánh kẹo và Snack
    'banh_keo': {
        'name': 'Banh keo',
        'key': '3',
        'shelf_id': 3,
        'side': 'front',
        'positions': [(3,21), (3,22), (3,23), (3,24), (4,21), (4,22), (4,23), (4,24)],
        'color': (255, 182, 193),  # Light Pink
        'description': 'Ke 3 (Mat truoc): Banh keo cac loai'
    },
    'snack': {
        'name': 'Snack',
        'key': '3b',
        'shelf_id': 3,
        'side': 'back',
        'positions': [(5,21), (5,22), (5,23), (5,24), (6,21), (6,22), (6,23), (6,24)],
        'color': (255, 160, 180),  # Pink
        'description': 'Ke 3 (Mat sau): Snack, do an vat'
    },

    # SHELF 4 - Mì và Đồ ăn liền
    'mi_goi': {
        'name': 'Mi goi',
        'key': '4',
        'shelf_id': 4,
        'side': 'front',
        'positions': [(3,29), (3,30), (3,31), (3,32), (4,29), (4,30), (4,31), (4,32)],
        'color': (255, 165, 0),  # Orange
        'description': 'Ke 4 (Mat truoc): Mi goi cac loai'
    },
    'do_an_lien': {
        'name': 'Do an lien',
        'key': '4b',
        'shelf_id': 4,
        'side': 'back',
        'positions': [(5,29), (5,30), (5,31), (5,32), (6,29), (6,30), (6,31), (6,32)],
        'color': (255, 140, 0),  # Dark Orange
        'description': 'Ke 4 (Mat sau): Do an lien, chao an lien'
    },

    # ROW 2 - Thực phẩm tươi sống
    # SHELF 5 - Rau củ và Trái cây
    'rau_cu': {
        'name': 'Rau cu',
        'key': '5',
        'shelf_id': 5,
        'side': 'front',
        'positions': [(10,5), (10,6), (10,7), (10,8), (11,5), (11,6), (11,7), (11,8)],
        'color': (0, 255, 0),  # Green
        'description': 'Ke 5 (Mat truoc): Rau cu tuoi'
    },
    'trai_cay': {
        'name': 'Trai cay',
        'key': '5b',
        'shelf_id': 5,
        'side': 'back',
        'positions': [(12,5), (12,6), (12,7), (12,8), (13,5), (13,6), (13,7), (13,8)],
        'color': (144, 238, 144),  # Light Green
        'description': 'Ke 5 (Mat sau): Trai cay tuoi'
    },

    # SHELF 6 - Thịt và Hải sản
    'thit': {
        'name': 'Thit tuoi',
        'key': '6',
        'shelf_id': 6,
        'side': 'front',
        'positions': [(10,13), (10,14), (10,15), (10,16), (11,13), (11,14), (11,15), (11,16)],
        'color': (255, 0, 0),  # Red
        'description': 'Ke 6 (Mat truoc): Thit tuoi cac loai'
    },
    'hai_san': {
        'name': 'Hai san',
        'key': '6b',
        'shelf_id': 6,
        'side': 'back',
        'positions': [(12,13), (12,14), (12,15), (12,16), (13,13), (13,14), (13,15), (13,16)],
        'color': (250, 128, 114),  # Salmon
        'description': 'Ke 6 (Mat sau): Hai san tuoi'
    },

    # SHELF 7 - Trứng và Đồ đông lạnh
    'trung': {
        'name': 'Trung',
        'key': '7',
        'shelf_id': 7,
        'side': 'front',
        'positions': [(10,21), (10,22), (10,23), (10,24), (11,21), (11,22), (11,23), (11,24)],
        'color': (255, 222, 173),  # Navajo White
        'description': 'Ke 7 (Mat truoc): Trung ga, vit, cut'
    },
    'dong_lanh': {
        'name': 'Do dong lanh',
        'key': '7b',
        'shelf_id': 7,
        'side': 'back',
        'positions': [(12,21), (12,22), (12,23), (12,24), (13,21), (13,22), (13,23), (13,24)],
        'color': (176, 224, 230),  # Powder Blue
        'description': 'Ke 7 (Mat sau): Do dong lanh'
    },

    # SHELF 8 - Sữa và Đồ uống lạnh
    'sua_tuoi': {
        'name': 'Sua tuoi',
        'key': '8',
        'shelf_id': 8,
        'side': 'front',
        'positions': [(10,29), (10,30), (10,31), (10,32), (11,29), (11,30), (11,31), (11,32)],
        'color': (255, 250, 250),  # Snow White
        'description': 'Ke 8 (Mat truoc): Sua tuoi'
    },
    'do_uong_lanh': {
        'name': 'Do uong lanh',
        'key': '8b',
        'shelf_id': 8,
        'side': 'back',
        'positions': [(12,29), (12,30), (12,31), (12,32), (13,29), (13,30), (13,31), (13,32)],
        'color': (240, 248, 255),  # Alice Blue
        'description': 'Ke 8 (Mat sau): Do uong lanh'
    },

    # ROW 3 - Đồ dùng sinh hoạt
    # SHELF 9 - Đồ dùng nhà bếp
    'do_nha_bep': {
        'name': 'Do dung nha bep',
        'key': '9',
        'shelf_id': 9,
        'side': 'front',
        'positions': [(17,5), (17,6), (17,7), (17,8), (18,5), (18,6), (18,7), (18,8)],
        'color': (169, 169, 169),  # Dark Gray
        'description': 'Ke 9 (Mat truoc): Do dung nha bep'
    },
    'do_nau_an': {
        'name': 'Do nau an',
        'key': '9b',
        'shelf_id': 9,
        'side': 'back',
        'positions': [(19,5), (19,6), (19,7), (19,8), (20,5), (20,6), (20,7), (20,8)],
        'color': (192, 192, 192),  # Silver
        'description': 'Ke 9 (Mat sau): Dung cu nau an'
    },

    # SHELF 10 - Đồ vệ sinh
    'do_ve_sinh': {
        'name': 'Do ve sinh',
        'key': '10',
        'shelf_id': 10,
        'side': 'front',
        'positions': [(17,13), (17,14), (17,15), (17,16), (18,13), (18,14), (18,15), (18,16)],
        'color': (135, 206, 235),  # Sky Blue
        'description': 'Ke 10 (Mat truoc): Do ve sinh ca nhan'
    },
    'san_pham_tam': {
        'name': 'San pham tam',
        'key': '10b',
        'shelf_id': 10,
        'side': 'back',
        'positions': [(19,13), (19,14), (19,15), (19,16), (20,13), (20,14), (20,15), (20,16)],
        'color': (173, 216, 230),  # Light Blue
        'description': 'Ke 10 (Mat sau): San pham tam, goi'
    },

    # SHELF 11 - Đồ giặt giũ
    'do_giat': {
        'name': 'Do giat',
        'key': '11',
        'shelf_id': 11,
        'side': 'front',
        'positions': [(17,21), (17,22), (17,23), (17,24), (18,21), (18,22), (18,23), (18,24)],
        'color': (221, 160, 221),  # Plum
        'description': 'Ke 11 (Mat truoc): Bot giat, nuoc giat'
    },
    'do_tay_rua': {
        'name': 'Do tay rua',
        'key': '11b',
        'shelf_id': 11,
        'side': 'back',
        'positions': [(19,21), (19,22), (19,23), (19,24), (20,21), (20,22), (20,23), (20,24)],
        'color': (238, 130, 238),  # Violet
        'description': 'Ke 11 (Mat sau): San pham tay rua'
    },

    # SHELF 12 - Đồ gia dụng
    'do_gia_dung': {
        'name': 'Do gia dung',
        'key': '12',
        'shelf_id': 12,
        'side': 'front',
        'positions': [(17,29), (17,30), (17,31), (17,32), (18,29), (18,30), (18,31), (18,32)],
        'color': (160, 82, 45),  # Sienna
        'description': 'Ke 12 (Mat truoc): Do gia dung'
    },
    'dung_cu': {
        'name': 'Dung cu',
        'key': '12b',
        'shelf_id': 12,
        'side': 'back',
        'positions': [(19,29), (19,30), (19,31), (19,32), (20,29), (20,30), (20,31), (20,32)],
        'color': (210, 105, 30),  # Chocolate
        'description': 'Ke 12 (Mat sau): Dung cu gia dinh'
    },

    # ROW 4 - Đồ điện tử và Khác
    # SHELF 13 - Đồ điện tử
    'do_dien_tu': {
        'name': 'Do dien tu',
        'key': '13',
        'shelf_id': 13,
        'side': 'front',
        'positions': [(24,5), (24,6), (24,7), (24,8), (25,5), (25,6), (25,7), (25,8)],
        'color': (75, 0, 130),  # Indigo
        'description': 'Ke 13 (Mat truoc): Do dien tu'
    },
    'phu_kien_dt': {
        'name': 'Phu kien dien tu',
        'key': '13b',
        'shelf_id': 13,
        'side': 'back',
        'positions': [(26,5), (26,6), (26,7), (26,8), (27,5), (27,6), (27,7), (27,8)],
        'color': (138, 43, 226),  # Blue Violet
        'description': 'Ke 13 (Mat sau): Phu kien dien tu'
    },

    # SHELF 14 - Văn phòng phẩm
    'van_phong_pham': {
        'name': 'Van phong pham',
        'key': '14',
        'shelf_id': 14,
        'side': 'front',
        'positions': [(24,13), (24,14), (24,15), (24,16), (25,13), (25,14), (25,15), (25,16)],
        'color': (0, 0, 139),  # Dark Blue
        'description': 'Ke 14 (Mat truoc): Van phong pham'
    },
    'dung_cu_hoc_tap': {
        'name': 'Dung cu hoc tap',
        'key': '14b',
        'shelf_id': 14,
        'side': 'back',
        'positions': [(26,13), (26,14), (26,15), (26,16), (27,13), (27,14), (27,15), (27,16)],
        'color': (0, 0, 205),  # Medium Blue
        'description': 'Ke 14 (Mat sau): Dung cu hoc tap'
    },

    # SHELF 15 - Đồ thể thao
    'do_the_thao': {
        'name': 'Do the thao',
        'key': '15',
        'shelf_id': 15,
        'side': 'front',
        'positions': [(24,21), (24,22), (24,23), (24,24), (25,21), (25,22), (25,23), (25,24)],
        'color': (0, 100, 0),  # Dark Green
        'description': 'Ke 15 (Mat truoc): Do the thao'
    },
    'phu_kien_tt': {
        'name': 'Phu kien the thao',
        'key': '15b',
        'shelf_id': 15,
        'side': 'back',
        'positions': [(26,21), (26,22), (26,23), (26,24), (27,21), (27,22), (27,23), (27,24)],
        'color': (34, 139, 34),  # Forest Green
        'description': 'Ke 15 (Mat sau): Phu kien the thao'
    },

    # SHELF 16 - Đồ trang trí
    'do_trang_tri': {
        'name': 'Do trang tri',
        'key': '16',
        'shelf_id': 16,
        'side': 'front',
        'positions': [(24,29), (24,30), (24,31), (24,32), (25,29), (25,30), (25,31), (25,32)],
        'color': (218, 112, 214),  # Orchid
        'description': 'Ke 16 (Mat truoc): Do trang tri'
    },
    'qua_tang': {
        'name': 'Qua tang',
        'key': '16b',
        'shelf_id': 16,
        'side': 'back',
        'positions': [(26,29), (26,30), (26,31), (26,32), (27,29), (27,30), (27,31), (27,32)],
        'color': (255, 20, 147),  # Deep Pink
        'description': 'Ke 16 (Mat sau): Qua tang, do luu niem'
    }
}

# New supermarket layout - 35 columns x 28 rows
# Layout: 5 rows of shelves, each row has 4 shelves
# Each shelf: 4 cells long x 2 cells wide
# Main walkway in center: 3 cells wide
# Entrance at bottom center
supermarket_layout = [
    # Top border
    [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # First row of shelves (Shelves 1-4)
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Walkway between first and second row 
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Second row of shelves (Shelves 5-8)
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Walkway between second and third row
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Third row of shelves (Shelves 9-12)
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Walkway between third and fourth row
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Fourth row of shelves (Shelves 13-16)
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Bottom walkway with entrance
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],  # Entrance
    [7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8]   # Bottom border with entrance
]

# Helper function to get category by key
def get_category_by_key(key):
    for category, info in PRODUCT_CATEGORIES.items():
        if info['key'] == key:
            return category
    return None

# Helper function to get shelf center position
def get_shelf_center(shelf_id):
    """Get the center position of a shelf for pathfinding target"""
    for category, info in PRODUCT_CATEGORIES.items():
        if info['shelf_id'] == shelf_id:
            positions = info['positions']
            if positions:
                # Return center of the shelf (middle position)
                center_idx = len(positions) // 2
                return positions[center_idx]
    return None