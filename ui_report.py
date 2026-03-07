import customtkinter as ctk

# ==========================================
# พื้นที่เนื้อหาหลัก (เว้นขอบซ้ายขวา)
# ==========================================
def create_report_ui(parent):
    content = ctk.CTkFrame(parent, fg_color="red")
    content.pack(fill="both", expand=True, padx=40, pady=20)

    # --- 2. แถวของการ์ด 4 ใบ (Summary Cards) ---
    cards_row = ctk.CTkFrame(content, fg_color="black")
    cards_row.pack(fill="x", pady=(0, 20))

    # แบ่งคัดเป็น 4 คอลัมน์เท่าๆ กัน
    for i in range(4):
        cards_row.columnconfigure(i, weight=1, uniform="card")
        
    # สีไอคอน (สมมุติ)
    card_colors = ["#E0F2FE", "#F3E8FF", "#FFEDD5", "#FCE7F3"]

    for i in range(4):
        # สร้าง Frame เปล่าๆ สีขาว แทนการ์ด 4 ใบ (เพิ่ม corner_radius ให้ขอบมน)
        card = ctk.CTkFrame(cards_row, fg_color="white", height=130, corner_radius=15)
        card.grid(row=0, column=i, sticky="nsew", padx=(0 if i==0 else 10, 0 if i==3 else 10))
        
        # ใส่สี่เหลี่ยมสีๆ ไว้มุมซ้ายบนแทนตำแหน่ง Icon
        icon_mock = ctk.CTkFrame(card, fg_color=card_colors[i], width=40, height=40, corner_radius=10)
        icon_mock.place(x=20, y=20)

    # --- 3. แถวตรงกลาง (Chart กับ ก้อนขวา 2 อัน) ---
    mid_row_left = ctk.CTkFrame(content, fg_color="green")
    mid_row_left.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, pady=(0, 20))

    mid_row_right = ctk.CTkFrame(content, fg_color="yellow")
    mid_row_right.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, pady=(0, 20))

    # 3.1 Frame กราฟ (ซ้าย) สีขาว
    chart_frame = ctk.CTkFrame(mid_row_left, fg_color="white", height=400, corner_radius=15)
    chart_frame.pack(fill=ctk.BOTH, expand=True)

    # Frame บนขวา (Best Sellers) สีขาว
    best_sellers = ctk.CTkFrame(mid_row_right, fg_color="black", corner_radius=15)
    best_sellers.pack(fill=ctk.BOTH, expand=True)

    # 3.2 Frame ฝั่งขวา 
    scroll = ctk.CTkScrollableFrame(mid_row_right, fg_color="green", corner_radius=15)
    scroll.pack(fill=ctk.BOTH, expand=True)

