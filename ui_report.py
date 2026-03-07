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

    def render_sales_table():
        # เคลียร์ข้อมูลเก่าที่อาจซ้อนใน chart_frame (ถ้ามี Treeview เก่าอยู่ให้ลบออกก่อน)
        for widget in chart_frame.winfo_children():
            widget.destroy()

        # Создать Treeview (ตาราง) แบบไม่มีเส้นขอบ
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
        sales_data = report.get_master_sales_data()
        
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

    # Frame บนขวา (Best Sellers) สีขาว
    best_sellers = ctk.CTkFrame(mid_row_right, fg_color="black", corner_radius=15)
    best_sellers.pack(fill=ctk.BOTH, expand=True, padx=(20, 0))

    # 3.2 Frame ฝั่งขวา 
    scroll = ctk.CTkScrollableFrame(mid_row_right, fg_color="green", corner_radius=15)
    scroll.pack(fill=ctk.BOTH, expand=True, pady=(0, 20), padx=(20, 0))

