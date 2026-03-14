"""
=============================================================
ไฟล์ GUI ของหน้า Report
=============================================================
"""
import customtkinter as ctk
from tkinter import ttk
import report
from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ==============================================================
# ฟังก์ชันหลัก สร้าง UI ของหน้า Report ทั้งหน้า
# ==============================================================
def create_report_ui(parent):
    # Frame หลักของหน้า Report
    content = ctk.CTkFrame(parent, fg_color="#191919")
    content.pack(fill="both", expand=True, padx=(15, 15), pady=(15, 0))
    # fill="both" = ยืดเต็มทั้งกว้างและสูง, expand=True = ใช้พื้นที่เหลือทั้งหมด

    # ==============================================================
    # ฟังก์ชันภายใน Refresh ข้อมูลทั้งหน้า
    # ==============================================================
    def refresh_data():
        """
        โหลดข้อมูลใหม่จากโมดูล report แล้วอัปเดต Label ทุกตัว
        เรียกใช้เมื่อกดปุ่ม Refresh
        """
        total_of_year.configure(text=str(report.show_year_sales()))    # อัปเดตรายได้ปีนี้
        total_of_month.configure(text=str(report.show_month_sales()))  # อัปเดตรายได้เดือนนี้
        total_of_day.configure(text=str(report.show_day_sales()))      # อัปเดตรายได้วันนี้
        total_members.configure(text=str(report.total_members()))      # อัปเดตจำนวนสมาชิก
        income.configure(text=str(report.total_revenue()))             # อัปเดตยอด Income
        expense.configure(text=str(report.total_expense()))            # อัปเดตยอด Expense
        render_sales_table()                                           # โหลดตารางใหม่


    # ==============================================================
    # ส่วนที่ 1 แถว Summary Cards (บนสุดของหน้า)
    # ==============================================================
    cards_row = ctk.CTkFrame(content, fg_color="#191919", height=80)
    cards_row.pack(fill="x", pady=(0, 20))   # fill="x" = ยืดตามแนวนอน
    cards_row.pack_propagate(False)           # ล็อคความสูงของ cards_row ไม่ให้ปรับตาม Widget ข้างใน

    # แบ่ง cards_row เป็น 5 คอลัมน์เท่าๆ กัน
    for i in range(5):
        cards_row.columnconfigure(i, weight=1, uniform="card")
        # uniform="card" = บังคับให้ทุกคอลัมน์มีความกว้างเท่ากัน


    # ฟังก์ชันช่วย สร้างการ์ดสรุปยอด
    def make_summary_card(col, title_text, value_widget_class, value_text):
        # สร้างกรอบการ์ดสีขาวมีขอบสีเขียว
        card = ctk.CTkFrame(
            cards_row,
            fg_color="white",
            height=130,
            corner_radius=15,
            border_width=5,
            border_color="#1e683e"
        )
        card.grid(row=0, column=col, sticky="nsew", padx=10)  # วางการ์ดในคอลัมน์ที่กำหนด

        # Label หัวข้อการ์ด
        ctk.CTkLabel(
            card,
            text=title_text,
            font=("Kanit", 30, "bold"),
            width=40, height=40,
            corner_radius=10,
            text_color="#144e2d"
        ).pack(side=ctk.TOP, pady=(20, 0))  # side=TOP = วางไว้ด้านบน

        # Label แสดงตัวเลข
        value_lbl = ctk.CTkLabel(
            card,
            text=value_text,
            font=("Kanit", 50, "bold"),
            text_color="#144e2d"
        )
        value_lbl.pack(pady=(0, 10))

        return value_lbl  # คืนค่า Label เพื่อให้ refresh_data() อัปเดตได้


    # สร้างการ์ด 4 ใบ และเก็บ Label ตัวเลขไว้สำหรับอัปเดต
    total_of_year  = make_summary_card(0, "รายได้ปีนี้",    ctk.CTkLabel, report.show_year_sales())
    total_of_month = make_summary_card(1, "รายได้เดือนนี้", ctk.CTkLabel, report.show_month_sales())
    total_of_day   = make_summary_card(2, "รายได้วันนี้",   ctk.CTkLabel, report.show_day_sales())
    total_members  = make_summary_card(3, "สมาชิกทั้งหมด",  ctk.CTkLabel, report.total_members())


    # ปุ่ม Refresh
    card_refresh = ctk.CTkFrame(cards_row, fg_color="#191919", height=130)
    card_refresh.grid(row=0, column=4, sticky="nsew", padx=(10, 0))

    # โหลดรูปปุ่ม Refresh 2 แบบ (ปกติ / ตอน Hover เมาส์)
    refresh_img_normal = ctk.CTkImage(light_image=Image.open(os.path.join(BASE_DIR, "img", "Button_refresh_normal.png")), size=(358, 160))
    refresh_img_hover  = ctk.CTkImage(light_image=Image.open(os.path.join(BASE_DIR, "img", "Button_refresh_hover.png")),  size=(358, 160))

    # สร้างปุ่ม Refresh (ใช้รูปแทนข้อความ)
    refresh_btn = ctk.CTkButton(
        card_refresh,
        text="",                      # ไม่แสดงข้อความ
        image=refresh_img_normal,     # รูปเริ่มต้น
        fg_color="transparent",       # พื้นหลังโปร่งใส
        hover_color="#191919",        # สีตอน Hover
        command=refresh_data          # เรียก refresh_data() เมื่อกด
    )
    refresh_btn.pack(fill=ctk.BOTH, expand=True)
    refresh_btn.pack_propagate(False)

    def on_enter(event):
        """เปลี่ยนรูปปุ่มเป็นแบบ Hover เมื่อเมาส์วางอยู่บนปุ่ม"""
        refresh_btn.configure(image=refresh_img_hover)

    def on_leave(event):
        """คืนรูปปุ่มเป็นแบบปกติเมื่อเมาส์ออกจากปุ่ม"""
        refresh_btn.configure(image=refresh_img_normal)

    # เชื่อม Event เมาส์เข้า/ออกกับฟังก์ชันเปลี่ยนรูป
    refresh_btn.bind("<Enter>", on_enter)  # เมาส์เข้า
    refresh_btn.bind("<Leave>", on_leave)  # เมาส์ออก


    # ==============================================================
    # ส่วนที่ 2 แถวกลาง แบ่งซ้าย/ขวา
    # ==============================================================

    # Frame คอลัมน์ซ้าย (ตาราง Master Sales)
    mid_row_left = ctk.CTkFrame(content, fg_color="#191919")
    mid_row_left.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)  # วางทางซ้าย ยืดเต็มพื้นที่

    # Frame คอลัมน์ขวา (Income, Expense, Best Sellers)
    mid_row_right = ctk.CTkFrame(content, fg_color="#191919")
    mid_row_right.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)  # วางทางขวา ยืดเต็มพื้นที่
    mid_row_right.grid_columnconfigure(0, weight=1)
    mid_row_right.grid_rowconfigure(0, weight=1)


    # ==============================================================
    # ส่วนที่ 3 ตาราง Master Sales (คอลัมน์ซ้าย)
    # ==============================================================

    # หัวข้อตาราง
    ctk.CTkLabel(
        mid_row_left,
        text="รายการบิลสินค้า",
        font=("Kanit", 25, "bold"),
        fg_color="#FFFFFF",
        text_color="#144e2d",
        height=40,
        corner_radius=10
    ).pack(fill=ctk.X, pady=(0, 15))  # ยืดเต็มความกว้าง

    # Frame ที่ Treeview จะถูกวางลงไป
    chart_frame = ctk.CTkFrame(mid_row_left, fg_color="white", height=400, corner_radius=15)
    chart_frame.pack(fill=ctk.BOTH, expand=True, pady=(0, 15))

    # ตั้งค่า Style ของตาราง Treeview 
    # ใช้ร่วมกันระหว่างตาราง Sales และตาราง Best Sellers
    style = ttk.Style()
    style.theme_use("clam")  # เลือก theme "clam" ที่รองรับการปรับแต่งสีได้
    style.configure(
        "Treeview",
        background="white",
        foreground="#333333",
        rowheight=35,           # ความสูงแต่ละแถว
        fieldbackground="white",
        font=("Kanit", 11),
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",     # ส่วนหัวตาราง
        font=("Kanit", 12, "bold"),
        background="#144e2d",
        foreground="#FFFFFF",
        borderwidth=0,
        relief="flat"
    )
    # map() = กำหนด Style ตามสถานะ เช่น ตอนถูก Select
    style.map("Treeview",         background=[("selected", "#E3F2FD")], foreground=[("selected", "#000000")])
    style.map("Treeview.Heading", background=[("selected", "#004f20")])


    def render_sales_table(days_filter=None):
        """
        สร้างและแสดงตาราง Master Sales ใน chart_frame
        ถ้าเรียกซ้ำจะลบตารางเก่าออกก่อนแล้วสร้างใหม่
        """
        # ลบ Widget เก่าใน chart_frame ออกก่อน (ป้องกันการซ้อนทับ)
        for widget in chart_frame.winfo_children():
            widget.destroy()

        # กำหนดคอลัมน์ของตาราง
        columns = ("customer_type", "date_time", "items", "total")
        tree = ttk.Treeview(
            chart_frame,
            columns=columns,
            show="headings",   # ซ่อนคอลัมน์ต้นไม้ แสดงแค่หัวคอลัมน์
            height=15,
            selectmode="browse" # เลือกได้ทีละ 1 แถว
        )

        # กำหนดหัวคอลัมน์และความกว้าง
        tree.heading("customer_type", text="ประเภทลูกค้า",  anchor="w")
        tree.column ("customer_type", width=150,             anchor="w")

        tree.heading("date_time",     text="วันเดือนปีเวลา", anchor="w")
        tree.column ("date_time",     width=180,             anchor="w")

        tree.heading("items",         text="จำนวนไอเทม",    anchor="center")
        tree.column ("items",         width=100,             anchor="center")

        tree.heading("total",         text="Total",          anchor="w")
        tree.column ("total",         width=120,             anchor="w")

        # Scrollbar แนวตั้งสำหรับตาราง
        scrollbar = ttk.Scrollbar(chart_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)  # เชื่อม Scrollbar กับตาราง

        tree.pack(side="left",  fill="both", expand=True, padx=(15, 0), pady=15)
        scrollbar.pack(side="right", fill="y",            padx=(0, 15), pady=15)

        # ดึงข้อมูลจาก report โดยกรองตาม days_filter
        sales_data = report.get_master_sales_data(days_filter)

        # กำหนดสีสลับแถวเพื่อให้อ่านง่าย
        tree.tag_configure("evenrow", background="#FFFFFF")
        tree.tag_configure("oddrow",  background="#F8F9FA")

        for idx, data in enumerate(sales_data):
            # ตรวจว่าเป็น Member หรือ General Customer
            customer_type = "Member" if "Member" in data["customer"] else "General Customer"

            tag = "evenrow" if idx % 2 == 0 else "oddrow"

            # แทรกแถวข้อมูลลงตาราง ("" = ไม่มี Parent end = ต่อท้ายสุด)
            tree.insert("", "end", values=(customer_type, data["date"], data["items"], data["total"]), tags=(tag,))


    # โหลดตารางครั้งแรกเมื่อเข้าหน้านี้ (แสดงทั้งหมด)
    render_sales_table()


    # ==============================================================
    # ส่วนที่ 4 กล่อง Income / Expense + Best Sellers (คอลัมน์ขวา)
    # ==============================================================

    # Frame หลักของคอลัมน์ขวา
    right_panel = ctk.CTkFrame(mid_row_right, fg_color="#191919", corner_radius=15)
    right_panel.grid(row=0, column=0, sticky="nsew", padx=(15, 0), pady=(0, 14))

    # กำหนดสัดส่วนความสูงของแต่ละแถวใน right_panel
    right_panel.grid_rowconfigure(0, weight=3)  # แถว 0: Income/Expense (สูงกว่า)
    right_panel.grid_rowconfigure(1, weight=1)  # แถว 1: ปุ่มกรองเวลา
    right_panel.grid_rowconfigure(2, weight=5)  # แถว 2: Best Sellers (สูงสุด)
    right_panel.grid_columnconfigure(0, weight=1)  # คอลัมน์ซ้าย (Income / ปุ่มกรอง)
    right_panel.grid_columnconfigure(1, weight=1)  # คอลัมน์ขวา (Expense / ปุ่มกรอง)


    # กล่อง Income (รายได้)
    in_come = ctk.CTkFrame(right_panel, fg_color="#FFFFFF", corner_radius=15, border_width=5, border_color="#1e683e")
    in_come.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=(0, 5))

    ctk.CTkLabel(in_come, text="Income", font=("Kanit", 30, "bold"), text_color="#1e683e").pack(side="top", pady=(10, 0))
    income = ctk.CTkLabel(in_come, text=report.total_revenue(), font=("Kanit", 80, "bold"), text_color="#1e683e")
    income.pack(expand=True, fill="both", padx=10, pady=(0, 10))
    # income เก็บ Label ไว้เพื่อให้ refresh_data() อัปเดตตัวเลขได้


    # กล่อง Expense (ค่าใช้จ่าย) 
    out_come = ctk.CTkFrame(right_panel, fg_color="#FFFFFF", corner_radius=15, border_width=5, border_color="#1e683e")
    out_come.grid(row=0, column=1, sticky="nsew", padx=5, pady=(0, 5))

    ctk.CTkLabel(out_come, text="Expense", font=("Kanit", 30, "bold"), text_color="#8e0000").pack(side="top", pady=(10, 0))
    expense = ctk.CTkLabel(out_come, text=report.total_expense(), font=("Kanit", 80, "bold"), text_color="#8e0000")
    expense.pack(expand=True, fill="both", padx=10, pady=(0, 10))
    # expense เก็บ Label ไว้เพื่อให้ refresh_data() อัปเดตตัวเลขได้


    # แถวปุ่มกรองช่วงเวลา
    filter_row = ctk.CTkFrame(right_panel, fg_color="transparent", corner_radius=15)
    filter_row.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=(0, 5))
    # columnspan=2 = ยืดให้ครอบคลุมทั้ง 2 คอลัมน์

    filter_row.rowconfigure(0, weight=1)
    for i in range(4):
        filter_row.columnconfigure(i, weight=1)  # แบ่ง 4 คอลัมน์เท่าๆ กัน

    # รายชื่อปุ่มกรอง (text, จำนวนวัน)
    filter_buttons = [
        ("ทั้งหมด", None),  # None = ไม่กรอง แสดงทั้งหมด
        ("7 วัน",   7),
        ("15 วัน",  15),
        ("1 เดือน", 30),
    ]

    for col_idx, (label, days) in enumerate(filter_buttons):
        padx = (0, 5) if col_idx == 0 else (5, 0) if col_idx == 3 else (5, 5)

        ctk.CTkButton(
            filter_row,
            text=label,
            font=("Kanit", 20, "bold"),
            command=lambda d=days: render_sales_table(d),
            fg_color="#1e683e",
            hover_color="#002c13"
        ).grid(row=0, column=col_idx, padx=padx, pady=(5, 0), sticky="nsew")


    # ==============================================================
    # ส่วนที่ 5 ตาราง Best Sellers (สินค้าขายดี)
    # ==============================================================

    # Frame หลักสำหรับ Best Sellers
    best_sellers_frame = ctk.CTkFrame(right_panel, fg_color="white", corner_radius=15)
    best_sellers_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    # columnspan=2 = ยืดให้ครอบคลุมทั้ง 2 คอลัมน์

    # หัวข้อ Best Sellers
    ctk.CTkLabel(
        best_sellers_frame,
        text="🏆 สินค้าขายดี (Best Sellers)",
        font=("Kanit", 16, "bold"),
        text_color="#333333"
    ).pack(side="top", pady=(10, 5), padx=15, anchor="w")  # anchor="w" = จัดชิดซ้าย


    def render_best_sellers_table():
        """
        สร้างตาราง Best Sellers ที่เรียงสินค้าจากสต็อกเหลือน้อยสุด
        สินค้าที่สต็อกเหลือน้อย = สินค้าที่ขายออกไปมากที่สุด (ขายดี)
        """
        # Frame ห่อ Treeview + Scrollbar ให้อยู่ด้วยกัน
        tv_frame = ctk.CTkFrame(best_sellers_frame, fg_color="transparent")
        tv_frame.pack(fill="both", expand=True, padx=10)

        # กำหนดคอลัมน์ของตาราง
        columns = ("rank", "id", "name")
        tree_bs = ttk.Treeview(
            tv_frame,
            columns=columns,
            show="headings",    # ซ่อน tree column แสดงแค่หัวคอลัมน์
            height=8,
            selectmode="none"   # ไม่ให้ Select แถวได้
        )

        # กำหนดหัวคอลัมน์และความกว้าง
        tree_bs.heading("rank", text="อันดับ",    anchor="center")
        tree_bs.column ("rank", width=50,          anchor="center")

        tree_bs.heading("id",   text="รหัส",       anchor="center")
        tree_bs.column ("id",   width=60,          anchor="center")

        tree_bs.heading("name", text="ชื่อสินค้า", anchor="center")
        tree_bs.column ("name", width=150,         anchor="center")

        # Scrollbar แนวตั้ง
        scrollbar_bs = ttk.Scrollbar(tv_frame, orient="vertical", command=tree_bs.yview)
        tree_bs.configure(yscrollcommand=scrollbar_bs.set)  # เชื่อม Scrollbar กับตาราง

        tree_bs.pack(side="left",  fill="both", expand=True)
        scrollbar_bs.pack(side="right", fill="y")

        # ดึงข้อมูลสินค้าทั้งหมด จาก report
        bs_data   = report.product_report()

        sorted_bs = sorted(bs_data, key=lambda item: item.get("stock", 0))

        # กำหนดสีสลับแถว
        tree_bs.tag_configure("evenrow", background="#FFFFFF")
        tree_bs.tag_configure("oddrow",  background="#F8F9FA")

        for idx, item in enumerate(sorted_bs):
            pid  = item.get("id",   "N/A")      # รหัสสินค้า (ถ้าไม่มีใช้ "N/A")
            name = item.get("name", "Unknown")   # ชื่อสินค้า (ถ้าไม่มีใช้ "Unknown")
            tag  = "evenrow" if idx % 2 == 0 else "oddrow"

            tree_bs.insert("", "end", values=(f"#{idx + 1}", pid, name), tags=(tag,))


    # โหลดตาราง Best Sellers เมื่อเข้าหน้านี้ครั้งแรก
    render_best_sellers_table()
