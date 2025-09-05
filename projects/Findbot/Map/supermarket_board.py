# Updated Supermarket layout - 5 rows x 4 columns = 20 shelves (46x35 map)
# 0 = walkway (black), 1 = product shelf, 9 = entrance/exit

# Product categories mapping - 20 shelves arranged in 5 rows x 4 columns
# Each shelf is 7 cells long x 4 cells wide, optimized for 46-width map
PRODUCT_CATEGORIES = {
    'ao': {
        'name': 'ao',
        'key': '1',
        'shelf_id': 1,
        'positions': [(3, 4), (3, 5), (3, 6), (3, 7), 
                      (4, 4), (4, 5), (4, 6), (4, 7)],  # 7x4 shelf (adjusted for 46-width map)
        'color': (0, 150, 255),  # Blue - Hàng 1 Cặp 1
        'description': '1A'  # Example description
    },
    'quan':{
        'name': 'quan',
        'key': '2',
        'shelf_id': 2,
        'positions': [(5, 4), (5, 5), (5, 6), (5, 7), 
                      (6, 4), (6, 5), (6, 6), (6, 7)],  # 7x4 shelf (adjusted for 46-width map)
        'color': (0, 150, 255),  # Blue - Hàng 1 Cặp 1
        'description': '1B'  # Example description
    },
    'gaolut': {
        'name': 'gaolut',
        'key': '3',
        'shelf_id': 3,
        'positions': [(3, 12), (3, 13), (3, 14), (3, 15), 
                      (4, 12), (4, 13), (4, 14), (4, 15)],  # 7x4 shelf
        'color': (255, 200, 0),  # Gold - Hàng 1 Cặp 2
        'description': '2A'
    },
    'gaonep':{
        'name': 'gaonep',
        'key': '4',
        'shelf_id': 4,
        'positions': [(5, 12), (5, 13), (5, 14), (5, 15),
                      (6, 12), (6, 13), (6, 14), (6, 15)],  # 7x4 shelf
        'color': (255, 200, 0),  # Gold - Hàng 1 Cặp 2
        'description': '2B'
    },
    'banhkeo': {
        'name': 'banhkeo',
        'key': '5',
        'shelf_id': 5,
        'positions': [(3, 20), (3, 21), (3, 22), (3, 23), 
                      (4, 20), (4, 21), (4, 22), (4, 23)],  # 7x4 shelf (shifted left)
        'color': (255, 100, 150),  # Pink - Hàng 1 Cặp 3
        'description': '3A'
    },
    'dochoi': {
        'name': 'dochoi',
        'key': '6',
        'shelf_id': 6,
        'positions': [(5, 20), (5, 21), (5, 22), (5, 23),
                      (6, 20), (6, 21), (6, 22), (6, 23)],  # 7x4 shelf (shifted left)
        'color': (255, 100, 150),  # Pink - Hàng 1 Cặp 3
        'description': '3B'
    },
    'mi': {
        'name': 'mi',
        'key': '7',
        'shelf_id': 7,
        'positions': [(3, 28), (3, 29), (3, 30), (3, 31), 
                      (4, 28), (4, 29), (4, 30), (4, 31)],  # 7x4 shelf (shifted left)
        'color': (255, 120, 0),  # Orange - Hàng 1 Cặp 4
        'description': '4A'
    },
    'migoi': {
        'name': 'migoi',
        'key': '8',
        'shelf_id': 8,
        'positions': [(5, 28), (5, 29), (5, 30), (5, 31),
                      (6, 28), (6, 29), (6, 30), (6, 31)],  # 7x4 shelf (shifted left)
        'color': (255, 120, 0),  # Orange - Hàng 1 Cặp 4
        'description': '4B'
    },    

    'botgiat': {
        'name': 'botgiat',
        'key': '9',
        'shelf_id': 9,
        'positions': [(10, 4), (10, 5), (10, 6), (10, 7),
                      (11, 4), (11, 5), (11, 6), (11, 7)],  # Row 2, Shelf 1 (8 cells, cols 4-7)
        'color': (50, 200, 50),  # Green - Hàng 2 Cặp 1
        'description': '5A'
    },
    'xabong': {
        'name': 'xabong',
        'key': '10',
        'shelf_id': 10,
        'positions': [(12, 4), (12, 5), (12, 6), (12, 7),
                      (13, 4), (13, 5), (13, 6), (13, 7)],  # Row 2, Shelf 1 (8 cells, cols 4-7)
        'color': (50, 200, 50),  # Green - Hàng 2 Cặp 1
        'description': '5B'
    },
    'thitbo': {
        'name': 'thitbo',
        'key': '11',
        'shelf_id': 11,
        'positions': [(10, 12), (10, 13), (10, 14), (10, 15),
                      (11, 12), (11, 13), (11, 14), (11, 15)],  # Row 2, Shelf 2 (8 cells, cols 12-15)
        'color': (220, 50, 50),  # Red - Hàng 2 Cặp 2
        'description': '6A'
    },
    'thitga': {
        'name': 'thitga',
        'key': '12',
        'shelf_id': 12,
        'positions': [(12, 12), (12, 13), (12, 14), (12, 15),
                      (13, 12), (13, 13), (13, 14), (13, 15)],  # Row 2, Shelf 2 (8 cells, cols 12-15)
        'color': (220, 50, 50),  # Red - Hàng 2 Cặp 2
        'description': '6B'
    },    
    'thitheo': {
        'name': 'thitheo',
        'key': '13',
        'shelf_id': 13,
        'positions': [(10, 20), (10, 21), (10, 22), (10, 23),
                      (11, 20), (11, 21), (11, 22), (11, 23)],  # Row 2, Shelf 3 (8 cells, cols 20-23)
        'color': (50, 100, 200),  # Blue - Hàng 2 Cặp 3
        'description': '7A'
    },
    'cahoi': {
        'name': 'cahoi',
        'key': '14',
        'shelf_id': 14,
        'positions': [(12, 20), (12, 21), (12, 22), (12, 23),
                      (13, 20), (13, 21), (13, 22), (13, 23)],  # Row 2, Shelf 3 (8 cells, cols 20-23)
        'color': (50, 100, 200),  # Blue - Hàng 2 Cặp 3
        'description': '7B'
    },    
    'cathu': {
        'name': 'cathu',
        'key': '14',
        'shelf_id': 14,
        'positions': [(12, 20), (12, 21), (12, 22), (12, 23),
                      (13, 20), (13, 21), (13, 22), (13, 23)],  # Same as 'cahoi'
        'color': (50, 100, 200),  # Blue - Hàng 2 Cặp 3
        'description': '7B'
    },      
    'caphe': {
        'name': 'caphe',
        'key': '15',
        'shelf_id': 15,
        'positions': [(10, 28), (10, 29), (10, 30), (10, 31),
                      (11, 28), (11, 29), (11, 30), (11, 31)],  # Row 2, Shelf 4 (8 cells, cols 28-31)
        'color': (100, 200, 200),  # Light Blue - Hàng 2 Cặp 4
        'description': '8A'
    },
    'giavi': {
        'name': 'giavi',
        'key': '16',
        'shelf_id': 16,
        'positions': [(12, 28), (12, 29), (12, 30), (12, 31),
                      (13, 28), (13, 29), (13, 30), (13, 31)],  # Row 2, Shelf 4 (8 cells, cols 28-31)
        'color': (100, 200, 200),  # Light Blue - Hàng 2 Cặp 4
        'description': '8B'
    },
    'dogiadung': {
        'name': 'dogiadung',
        'key': '17',
        'shelf_id': 17,
        'positions': [(17, 4), (17, 5), (17, 6), (17, 7),
                      (18, 4), (18, 5), (18, 6), (18, 7)],  # Row 3, Shelf 1 (8 cells, cols 4-7)
        'color': (150, 50, 200),  # Purple - Hàng 3 Cặp 1
        'description': '9A'
    },
    'noi': {
        'name': 'noi',
        'key': '18',
        'shelf_id': 18,
        'positions': [(19, 4), (19, 5), (19, 6), (19, 7),
                      (20, 4), (20, 5), (20, 6), (20, 7)],  # Row 3, Shelf 1 (8 cells, cols 4-7)
        'color': (150, 50, 200),  # Purple - Hàng 3 Cặp 1
        'description': '9B'
    },
    'chao': {
        'name': 'chao',
        'key': '18',
        'shelf_id': 18,
        'positions': [(19, 4), (19, 5), (19, 6), (19, 7),
                      (20, 4), (20, 5), (20, 6), (20, 7)],  # Same as 'noi'
        'color': (150, 50, 200),  # Purple - Hàng 3 Cặp 1
        'description': '9B'
    },
    'bep': {
        'name': 'bep',
        'key': '19',
        'shelf_id': 19,
        'positions': [(17, 12), (17, 13), (17, 14), (17, 15),
                      (18, 12), (18, 13), (18, 14), (18, 15)],  # Row 3, Shelf 2 (8 cells, cols 12-15)
        'color': (200, 50, 100),  # Deep Pink - Hàng 3 Cặp 2
        'description': '10A'
    },
    'congcu': {
        'name': 'congcu',
        'key': '20',
        'shelf_id': 20,
        'positions': [(19, 12), (19, 13), (19, 14), (19, 15),
                      (20, 12), (20, 13), (20, 14), (20, 15)],  # Row 3, Shelf 2 (8 cells, cols 12-15)
        'color': (200, 50, 100),  # Deep Pink - Hàng 3 Cặp 2
        'description': '10B'
    },
    'mypham': {
        'name': 'mypham',
        'key': '21',
        'shelf_id': 21,
        'positions': [(17, 20), (17, 21), (17, 22), (17, 23),
                      (18, 20), (18, 21), (18, 22), (18, 23)],  # Row 3, Shelf 3 (8 cells, cols 20-23)
        'color': (220, 220, 220),  # Light Gray - Hàng 3 Cặp 3
        'description': '11A'
    },
    'phukien': {
        'name': 'phukien',
        'key': '22',
        'shelf_id': 22,
        'positions': [(19, 20), (19, 21), (19, 22), (19, 23),
                      (20, 20), (20, 21), (20, 22), (20, 23)],  # Row 3, Shelf 3 (8 cells, cols 20-23)
        'color': (220, 220, 220),  # Light Gray - Hàng 3 Cặp 3
        'description': '11B'
    },
    'traicay': {
        'name': 'traicay',
        'key': '23',
        'shelf_id': 23,
        'positions': [(17, 28), (17, 29), (17, 30), (17, 31),
                      (18, 28), (18, 29), (18, 30), (18, 31)],  # Row 3, Shelf 4 (8 cells, cols 28-31)
        'color': (255, 150, 180),  # Light Pink - Hàng 3 Cặp 4
        'description': '12A'
    },
    'traitao': {
        'name': 'traitao',
        'key': '24',
        'shelf_id': 24,
        'positions': [(19, 28), (19, 29), (19, 30), (19, 31),
                      (20, 28), (20, 29), (20, 30), (20, 31)],  # Row 3, Shelf 4 (8 cells, cols 28-31)
        'color': (255, 150, 180),  # Light Pink - Hàng 3 Cặp 4
        'description': '12B'
    },
    'cha': {
        'name': 'cha',
        'key': '25',
        'shelf_id': 25,
        'positions': [(24, 4), (24, 5), (24, 6), (24, 7),
                    (25, 4), (25, 5), (25, 6), (25, 7)],  # Row 4, Shelf 1 (8 cells, cols 4-7)
        'color': (100, 180, 100),  # Spring Green - Hàng 4 Cặp 1
        'description': '13A'
    },    
    'xucxich': {
        'name': 'xucxich',
        'key': '26',
        'shelf_id': 26,
        'positions': [(26, 4), (26, 5), (26, 6), (26, 7),
                      (27, 4), (27, 5), (27, 6), (27, 7)],  # Row 4, Shelf 2 (8 cells, cols 4-7)
        'color': (100, 180, 100),  # Spring Green - Hàng 4 Cặp 1
        'description': '13B'
    },
    'trung': {
        'name': 'trung',
        'key': '27',
        'shelf_id': 27,
        'positions': [(24, 12), (24, 13), (24, 14), (24, 15),
                      (25, 12), (25, 13), (25, 14), (25, 15)],  # Row 4, Shelf 3 (8 cells, cols 12-15)
        'color': (80, 80, 80),  # Dark Gray - Hàng 4 Cặp 2
        'description': '14A'
    },

    'suatuoi': {
        'name': 'suatuoi',
        'key': '28',
        'shelf_id': 28,
        'positions': [(26, 12), (26, 13), (26, 14), (26, 15),
                      (27, 12), (27, 13), (27, 14), (27, 15)],  # Row 4, Shelf 3 (8 cells, cols 12-15)
        'color': (80, 80, 80),  # Dark Gray - Hàng 4 Cặp 2
        'description': '14B'
    },    
    'suabot': {
        'name': 'suabot',
        'key': '29',
        'shelf_id': 29,
        'positions': [(24, 20), (24, 21), (24, 22), (24, 23),
                      (25, 20), (25, 21), (25, 22), (25, 23)],  # Row 4, Shelf 4 (8 cells, cols 20-23)
        'color': (150, 100, 60),  # Brown - Hàng 4 Cặp 3
        'description': '15A'
    },
    'douong': {
        'name': 'douong',
        'key': '30',
        'shelf_id': 30,
        'positions': [(26, 20), (26, 21), (26, 22), (26, 23),
                      (27, 20), (27, 21), (27, 22), (27, 23)],  # Row 4, Shelf 4 (8 cells, cols 20-23)
        'color': (150, 100, 60),  # Brown - Hàng 4 Cặp 3
        'description': '15B'
    },    
    'trangsuc': {
        'name': 'trangsuc',
        'key': '31',
        'shelf_id': 31,
        'positions': [
            (24, 28), (24, 29), (24, 30), (24, 31),
            (25, 28), (25, 29), (25, 30), (25, 31),
            (26, 28), (26, 29), (26, 30), (26, 31),
            (27, 28), (27, 29), (27, 30), (27, 31)
        ],  # 4x4 = 16 cells, cols 28-31
        'color': (255, 215, 0),  # Gold - Kệ 31 màu riêng
        'description': '16'
    },        
    'dodonghop': {
        'name': 'dodonghop',
        'key': '32',
        'shelf_id': 32,
        'positions': [(3, 36), (3, 37), (3, 38), (3, 39),
                      (4, 36), (4, 37), (4, 38), (4, 39)],  # Row 5, Shelf 1
        'color': (255, 80, 80),  # Red Orange - Hàng 5 Cặp 1
        'description': '17A'
    },
    'dohop': {
        'name': 'dohop',
        'key': '32',
        'shelf_id': 32,
        'positions': [(3, 36), (3, 37), (3, 38), (3, 39),
                      (4, 36), (4, 37), (4, 38), (4, 39)],  # Row 5, Shelf 1
        'color': (255, 80, 80),  # Red Orange - Hàng 5 Cặp 1
        'description': '17A'
    },
    'dau': {
        'name': 'dau',
        'key': '33',
        'shelf_id': 33,
        'positions': [(5, 36), (5, 37), (5, 38), (5, 39),
                      (6, 36), (6, 37), (6, 38), (6, 39)],  # Row 5, Shelf 1
        'color': (255, 80, 80),  # Red Orange - Hàng 5 Cặp 1
        'description': '17B'
    },
    'carot': {
        'name': 'carot',
        'key': '34',
        'shelf_id': 34,
        'positions': [(10, 36), (10, 37), (10, 38), (10, 39),
                      (11, 36), (11, 37), (11, 38), (11, 39)],  # Row 5, Shelf 2
        'color': (60, 180, 60),  # Forest Green - Hàng 5 Cặp 2
        'description': '18A'
    },
    'khoaitay': {
        'name': 'khoaitay',
        'key': '34',
        'shelf_id': 34,
        'positions': [(10, 36), (10, 37), (10, 38), (10, 39),
                      (11, 36), (11, 37), (11, 38), (11, 39)],  # Row 5, Shelf 2
        'color': (60, 180, 60),  # Forest Green - Hàng 5 Cặp 2
        'description': '18A'
    },
    'rau': {
        'name': 'rau',
        'key': '35',
        'shelf_id': 35,
        'positions': [(12, 36), (12, 37), (12, 38), (12, 39),
                      (13, 36), (13, 37), (13, 38), (13, 39)],  # Row 5, Shelf 2
        'color': (60, 180, 60),  # Forest Green - Hàng 5 Cặp 2
        'description': '18B'
    },
    'raucu': {
        'name': 'raucu',
        'key': '35',
        'shelf_id': 35,
        'positions': [(12, 36), (12, 37), (12, 38), (12, 39),
                      (13, 36), (13, 37), (13, 38), (13, 39)],  # Row 5, Shelf 2
        'color': (60, 180, 60),  # Forest Green - Hàng 
        'description': '18B'
    },
    'giay': {
        'name': 'giay',
        'key': '36',
        'shelf_id': 36,
        'positions': [(17, 36), (17, 37), (17, 38), (17, 39),
                      (18, 36), (18, 37), (18, 38), (18, 39)],  # Row 5, Shelf 3
        'color': (200, 150, 0),  # Gold - Hàng 5 Cặp 3
        'description': '19A'
    },
    'dep': { 
        'name': 'dep',
        'key': '37',
        'shelf_id': 37,
        'positions': [(19, 36), (19, 37), (19, 38), (19, 39),
                      (20, 36), (20, 37), (20, 38), (20, 39)],  # Row 5, Shelf 3
        'color': (200, 150, 0),  # Gold - Hàng 5 Cặp 3
        'description': '19B'
    },
    'sach': {
        'name': 'sach',
        'key': '38',
        'shelf_id': 38,
        'positions': [(24, 36), (24, 37), (24, 38), (24, 39),
                      (25, 36), (25, 37), (25, 38), (25, 39),
                      (26, 36), (26, 37), (26, 38), (26, 39),
                      (27, 36), (27, 37), (27, 38), (27, 39)],  # Row 5, Shelf 4
        'color': (80, 50, 20),  # Dark Brown - Kệ 38 màu riêng
        'description': '20'
    },
}

supermarket_layout = [
    [3] * 44,  # Empty row for top wall
    [3] + [0] * 42 + [3],
    # First row (top) now has a continuous top wall across walkable segments and walls at both ends
    [3] + [1] * 4 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 5 + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [1] * 4 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 5 + [3],
    # Walkway between first and second row (with left and right walls)
    [3] + [0] * 42 + [3],
    # Second row of shelves (Shelves 9-16) - add left wall
    [3] + [1] * 4 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 5 + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [1] * 4 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 5 + [3],
    # Main central walkway (with left and right walls)
    [3] + [0] * 42 + [3],
    # Third row of shelves (Shelves 17-24) - add left wall
    [3] + [1] * 4 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 5 + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [1] * 4 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 5 + [3],
    # Walkway between third and fourth row (with left and right walls)
    [3] + [0] * 42 + [3],
    # Fourth row of shelves (Shelves 25-31) - add left wall
    [3] + [1] * 4 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 5 + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] + [0] + [1] * 2 + [1] * 4 + [1] * 2 + [0] + [3],
    [3] + [1] * 4 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 3 + [0] + [1] * 5 + [3],   
    # Walkway between fourth and fifth row (with left and right walls)
    [3] + [0] + [1] * 7 + [0] + [1] * 7 + [0] + [1] * 7 + [0] + [1] * 7 +  [0] + [1] * 8 + [0] + [3],
    [3] + [0] + [1] * 7 + [0] + [1] * 7 + [0] + [1] * 7 + [0] + [1] * 7 +  [0] + [1] * 8 + [0] + [3],

 
    # Bottom walkway with entrance - shifted 2 cells to the right, with left and right walls
    [3] + [0] * 19 + [9] * 4 + [0] * 19 + [3],
    [3] * 44,      
    [3] + [0] * 42 + [3],
    [3] + [0] * 42 + [3],
    [3] + [0] * 42 + [3],
    # Bottom border with entrance aligned to the shift and width

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
