import customtkinter as ctk
from tkinter import ttk
import report

# ==========================================
# พื้นที่เนื้อหาหลัก (เว้นขอบซ้ายขวา)
# ==========================================
def create_report_ui(parent):
    content = ctk.CTkFrame(parent, fg_color="red")
    content.pack(fill="both", expand=True, padx=40, pady=20)

    def refresh_data():
        total_of_year.configure(text=str(report.show_year_sales()))
        total_of_month.configure(text=str(report.show_month_sales()))
        total_of_day.configure(text=str(report.show_day_sales()))
        total_members.configure(text=str(report.total_members()))
        render_sales_table()

    # --- 2. แถวของการ์ด 4 ใบ (Summary Cards) ---
    cards_row = ctk.CTkFrame(content, fg_color="black")
    cards_row.pack(fill="x", pady=(0, 20))

    # แบ่งคัดเป็น 4 คอลัมน์เท่าๆ กัน
    for i in range(5):
        cards_row.columnconfigure(i, weight=1, uniform="card")
        
    # สีไอคอน (สมมุติ)
    card_colors = ["#E0F2FE", "#F3E8FF", "#FFEDD5", "#FCE7F3"]

    # การ์ดใบที่ 1
    card_1 = ctk.CTkFrame(cards_row, fg_color="white", height=130, corner_radius=15)
    card_1.grid(row=0, column=0, sticky="nsew", padx=(10))
    label1 = ctk.CTkLabel(card_1, text="รายได้ปีนี้", font=("Kanit", 15, "bold"), width=40, height=40, corner_radius=10)
    label1.pack(side=ctk.TOP, pady=(10, 0))
    total_of_year = ctk.CTkLabel(card_1, text=report.show_year_sales(), font=ctk.CTkFont(size=16, weight="bold"))
    total_of_year.pack(side=ctk.BOTTOM, pady=(0, 10))

    # การ์ดใบที่ 2
    card_2 = ctk.CTkFrame(cards_row, fg_color="white", height=130, corner_radius=15)
    card_2.grid(row=0, column=1, sticky="nsew", padx=(10))
    label2 = ctk.CTkLabel(card_2, text="รายได้เดือนนี้", font=("Kanit", 15, "bold"), width=40, height=40, corner_radius=10)
    label2.pack(side=ctk.TOP, pady=(10, 0))
    total_of_month = ctk.CTkLabel(card_2, text=report.show_month_sales(), font=ctk.CTkFont(size=16, weight="bold"))
    total_of_month.pack(side=ctk.BOTTOM, pady=(0, 10))

    # การ์ดใบที่ 3
    card_3 = ctk.CTkFrame(cards_row, fg_color="white", height=130, corner_radius=15)
    card_3.grid(row=0, column=2, sticky="nsew", padx=(10))
    label3 = ctk.CTkLabel(card_3, text="รายได้วันนี้", font=("Kanit", 15, "bold"), width=40, height=40, corner_radius=10)
    label3.pack(side=ctk.TOP, pady=(10, 0))
    total_of_day = ctk.CTkLabel(card_3, text=report.show_day_sales(), font=ctk.CTkFont(size=16, weight="bold"))
    total_of_day.pack(side=ctk.BOTTOM, pady=(0, 10))

    # การ์ดใบที่ 4
    card_4 = ctk.CTkFrame(cards_row, fg_color="white", height=130, corner_radius=15)
    card_4.grid(row=0, column=3, sticky="nsew", padx=(10, 0))
    label4 = ctk.CTkLabel(card_4, text="สมาชิกทั้งหมด", font=("Kanit", 15, "bold"), width=40, height=40, corner_radius=10)
    label4.pack(side=ctk.TOP, pady=(10, 0))
    total_members = ctk.CTkLabel(card_4, text=report.total_members(), font=ctk.CTkFont(size=16, weight="bold"))
    total_members.pack(side=ctk.BOTTOM, pady=(0, 10))

    card_5 = ctk.CTkFrame(cards_row, fg_color="white", height=130, corner_radius=15)
    card_5.grid(row=0, column=4, sticky="nsew", padx=(10, 0))
    refresh_btn = ctk.CTkButton(card_5, text="🔄 รีเฟรชข้อมูล", font=("Kanit", 14, "bold"), command=refresh_data)
    refresh_btn.pack(fill=ctk.BOTH, expand=True)

    # --- 3. แถวตรงกลาง (Chart กับ ก้อนขวา 2 อัน) ---
    mid_row_left = ctk.CTkFrame(content, fg_color="green")
    mid_row_left.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, pady=(0, 20))
    
    mid_row_right = ctk.CTkFrame(content, fg_color="yellow")
    mid_row_right.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, pady=(0, 20))
    mid_row_right.grid_columnconfigure(0, weight=1)
    mid_row_right.grid_rowconfigure(0, weight=1)


    # 3.1 Frame กราฟ (ซ้าย) สีขาว (ใช้เป็นตารางแสดงข้อมูล Master Sales)
    chart_frame = ctk.CTkFrame(mid_row_left, fg_color="white", height=400, corner_radius=15)
    chart_frame.pack(fill=ctk.BOTH, expand=True, pady=(0, 20))

    # ปรับแต่งสไตล์ของ Treeview ให้เข้ากับแอป (Modern Look)
    style = ttk.Style()
    style.theme_use("clam") # ใช้ clam theme เพื่อเอาขอบแบบ Windows 98 ออก
    
    style.configure("Treeview", 
                    background="white",
                    foreground="#333333",
                    rowheight=35,
                    fieldbackground="white",
                    font=("Kanit", 11),
                    borderwidth=0) # ลบขอบตาราง
    
    style.configure("Treeview.Heading", 
                    font=("Kanit", 12, "bold"), 
                    background="#F8F9FA", 
                    foreground="#495057",
                    borderwidth=0,
                    relief="flat") # ทำให้หัวตารางแบนเรียบ
                    
    style.map('Treeview', background=[('selected', '#E3F2FD')], foreground=[('selected', '#000000')])
    style.map('Treeview.Heading', background=[('active', '#E9ECEF')])

    def render_sales_table(days_filter=None):
        # เคลียร์ข้อมูลเก่าที่อาจซ้อนใน chart_frame (ถ้ามี Treeview เก่าอยู่ให้ลบออกก่อน)
        for widget in chart_frame.winfo_children():
            widget.destroy()

        # สร้าง Treeview (ตาราง) แบบไม่มีเส้นขอบ
        columns = ("customer_type", "date_time", "items", "total")
        tree = ttk.Treeview(chart_frame, columns=columns, show="headings", height=15, selectmode="browse")
        
        # ปรับความกว้างและหัวข้อคอลัมน์
        tree.heading("customer_type", text="ประเภทลูกค้า", anchor="w")
        tree.column("customer_type", width=150, anchor="w")

        tree.heading("date_time", text="วันเดือนปีเวลา", anchor="w")
        tree.column("date_time", width=180, anchor="w")

        tree.heading("items", text="จำนวนไอเทม", anchor="center")
        tree.column("items", width=100, anchor="center")

        tree.heading("total", text="Total", anchor="w")
        tree.column("total", width=120, anchor="w")

        # สร้าง Scrollbar สำหรับเลื่อนตารางขึ้น-ลง
        scrollbar = ttk.Scrollbar(chart_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # จัดวางตัว Treeview และ Scrollbar ลงใน Frame
        tree.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=15)
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=15)

        # ดึงข้อมูลมาจาก report
        sales_data = report.get_master_sales_data(days_filter)
        
        # ใส่ tag เพื่อสลับสีแถว (Zebra striping)
        tree.tag_configure('evenrow', background='#FFFFFF')
        tree.tag_configure('oddrow', background='#F8F9FA')
        
        for idx, data in enumerate(sales_data):
            # ประเภทลูกค้า
            customer_type = "Member" if "Member" in data["customer"] else "General Customer"
            
            # ยัดข้อมูลลงแถวของ Treeview พร้อมกำหนด tag สลับสี
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=(customer_type, data["date"], data["items"], data["total"]), tags=(tag,))

    # เรียกใช้งานแสดงตารางครั้งแรก
    render_sales_table()

# Frame บนขวา (Best Sellers)
    best_sellers = ctk.CTkFrame(mid_row_right, fg_color="black", corner_radius=15)
    best_sellers.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
    
    # ให้แถวที่ 0 (Income/Expense) สูงขึ้น (ปรับเลข 2 หรือ 3 ตามความสูงที่พอใจ)
    best_sellers.grid_rowconfigure(0, weight=3)  

    # แถวที่ 1 (สีแดง)
    best_sellers.grid_rowconfigure(1, weight=1)  

    # แถวที่ 2 (สีเขียว) ให้สูงที่สุดเพื่อโชว์รายการเยอะๆ
    best_sellers.grid_rowconfigure(2, weight=5)  

    # ตั้งค่า Column ให้แบ่งครึ่งเท่ากัน (สำหรับ Income และ Expense)
    best_sellers.grid_columnconfigure(0, weight=1)
    best_sellers.grid_columnconfigure(1, weight=1)

    # --- ส่วนของ Income ---
    in_come = ctk.CTkFrame(best_sellers, fg_color="white", corner_radius=15)
    in_come.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    lbl_inc_title = ctk.CTkLabel(in_come, text="Income", font=("Kanit", 25, "bold"), text_color="gray")
    lbl_inc_title.pack(side="top", pady=(0, 0))

    income = ctk.CTkLabel(in_come, text=report.total_revenue(), font=("Kanit", 80, "bold"), text_color="green")
    income.pack(expand=True, fill="both", padx=10, pady=(0, 0))

    # --- ส่วนของ Expense ---
    out_come = ctk.CTkFrame(best_sellers, fg_color="#2b2b2b", corner_radius=15) # เปลี่ยนจากดำสนิทให้ดูมีมิติ
    out_come.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    lbl_exp_title = ctk.CTkLabel(out_come, text="Expense", font=("Kanit", 25, "bold"), text_color="lightgray")
    lbl_exp_title.pack(side="top", pady=(0, 0))

    expense = ctk.CTkLabel(out_come, text=report.total_expense(), font=("Kanit", 80, "bold"), text_color="red")
    expense.pack(expand=True, fill="both", padx=10, pady=(0, 0))

    # --- ส่วนของ Custom (ปุ่ม) ---
    in_out_come_custom = ctk.CTkFrame(best_sellers, fg_color="transparent", corner_radius=15)
    in_out_come_custom.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=(0, 5))

    # 1. สำคัญ: ต้องกำหนดให้ Row 0 ภายในเฟรมนี้ขยายตัวด้วย
    in_out_come_custom.rowconfigure(0, weight=1) 

    # 2. กำหนดให้ทั้ง 4 Column มีน้ำหนักเท่ากัน (คุณทำไว้แล้ว ดีมากครับ)
    for i in range(4):
        in_out_come_custom.columnconfigure(i, weight=1)

    # 3. ตรวจสอบว่าปุ่มทุกปุ่มมี sticky="nsew" (เพื่อให้ปุ่มยืดไปแตะขอบ Grid)
    btn_all = ctk.CTkButton(in_out_come_custom, text="ทั้งหมด", font=("Kanit", 12), command=lambda: render_sales_table(None))
    btn_all.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

    btn_7 = ctk.CTkButton(in_out_come_custom, text="7 วัน", font=("Kanit", 12), command=lambda: render_sales_table(7))
    btn_7.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")

    btn_15 = ctk.CTkButton(in_out_come_custom, text="15 วัน", font=("Kanit", 12), command=lambda: render_sales_table(15))
    btn_15.grid(row=0, column=2, padx=2, pady=2, sticky="nsew")

    btn_30 = ctk.CTkButton(in_out_come_custom, text="1 เดือน", font=("Kanit", 12), command=lambda: render_sales_table(30))
    btn_30.grid(row=0, column=3, padx=2, pady=2, sticky="nsew")

    # 3.2 Frame ขวาล่าง (Best Sellers Table)
    best_sellers_frame = ctk.CTkFrame(best_sellers, fg_color="white", corner_radius=15)
    best_sellers_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    
    # เพิ่ม Label ชื่อตาราง
    lbl_bs_title = ctk.CTkLabel(best_sellers_frame, text="🏆 สินค้าขายดี (Best Sellers)", font=("Kanit", 16, "bold"), text_color="#333333")
    lbl_bs_title.pack(side="top", pady=(10, 5), padx=15, anchor="w")

    def render_best_sellers_table():
        # สร้าง Frame เปล่าๆ สำหรับยัด Treeview กะ Scrollbar
        tv_frame = ctk.CTkFrame(best_sellers_frame, fg_color="transparent")
        tv_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # สร้าง Treeview (ตาราง) แบบไม่มีเส้นขอบ (ใช้ style เดิมที่เซ็ตไว้)
        columns = ("rank", "id", "name")
        tree_bs = ttk.Treeview(tv_frame, columns=columns, show="headings", height=8, selectmode="none")
        
        # ปรับความกว้างและหัวข้อคอลัมน์
        tree_bs.heading("rank", text="อันดับ", anchor="center")
        tree_bs.column("rank", width=50, anchor="center")

        tree_bs.heading("id", text="รหัส", anchor="center")
        tree_bs.column("id", width=60, anchor="center")

        tree_bs.heading("name", text="ชื่อสินค้า", anchor="center")
        tree_bs.column("name", width=150, anchor="center")

        # สร้าง Scrollbar สำหรับเลื่อนตารางขึ้น-ลง
        scrollbar_bs = ttk.Scrollbar(tv_frame, orient="vertical", command=tree_bs.yview)
        tree_bs.configure(yscrollcommand=scrollbar_bs.set)

        # จัดวางตัว Treeview และ Scrollbar ลงใน Frame
        tree_bs.pack(side="left", fill="both", expand=True)
        scrollbar_bs.pack(side="right", fill="y")

        # ดึงข้อมูลมาจาก report (คืนค่ามาเป็น list of dict)
        bs_data = report.product_report()
        
        # เรียงตาม stock คงเหลือน้อยที่สุด
        sorted_bs = sorted(bs_data, key=lambda item: item.get('stock', 0))
        
        # ใส่ tag เพื่อสลับสีแถว (Zebra striping)
        tree_bs.tag_configure('evenrow', background='#FFFFFF')
        tree_bs.tag_configure('oddrow', background='#F8F9FA')
        
        for idx, item in enumerate(sorted_bs):
            # ยัดข้อมูลลงแถวของ Treeview พร้อมกำหนด tag สลับสี
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            pid = item.get('id', 'N/A')
            name = item.get('name', 'Unknown')
            tree_bs.insert("", "end", values=(f"#{idx + 1}", pid, name), tags=(tag,))

    # เรียกใช้งานแสดงตารางสินค้าขายดี
    render_best_sellers_table()
