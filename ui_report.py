"""
ไฟล์นี้รวมโค้ด GUI ของหน้า Report ทั้งหมด
"""
import customtkinter as ctk
from tkinter import ttk
import report
from PIL import Image


# =========================================================================== #
# ฟังก์ชันหลัก: สร้าง UI ของหน้า Report ทั้งหน้า
# =========================================================================== #

def create_report_ui(parent):
    """
    สร้าง UI หน้า Report ทั้งหน้าและวางลงใน parent
    โครงสร้างหน้าจอ:
    """
    # พื้นที่หลักของหน้า
    content = ctk.CTkFrame(parent, fg_color="#191919")
    content.pack(fill="both", expand=True, padx=(15, 15), pady=(15, 0))

    # =========================================================
    # ส่วนที่ 1: ฟังก์ชัน Refresh (อัปเดต Label ทุกตัวพร้อมกัน)
    # =========================================================

    def refresh_data():
        """โหลดข้อมูลใหม่จาก report และอัปเดตทุก Label บนหน้าจอ"""
        total_of_year.configure(text=str(report.show_year_sales()))
        total_of_month.configure(text=str(report.show_month_sales()))
        total_of_day.configure(text=str(report.show_day_sales()))
        total_members.configure(text=str(report.total_members()))
        income.configure(text=str(report.total_revenue()))
        expense.configure(text=str(report.total_expense()))
        render_sales_table()

    # =========================================================
    # ส่วนที่ 2: แถว Summary Cards (บนสุด)
    # =========================================================

    cards_row = ctk.CTkFrame(content, fg_color="#191919", height=80)
    cards_row.pack(fill="x", pady=(0, 20))
    cards_row.pack_propagate(False)

    # แบ่ง 5 คอลัมน์ (4 การ์ด + 1 ปุ่ม Refresh)
    for i in range(5):
        cards_row.columnconfigure(i, weight=1, uniform="card")

    # --- Helper: สร้างการ์ดสรุปยอด ---
    def make_summary_card(col, title_text, value_widget_class, value_text):
        """
        สร้าง Card แสดงข้อมูลสรุป (Title + ตัวเลข)
        คืนค่า: CTkLabel ที่แสดงตัวเลข (ใช้อัปเดตภายหลัง)
        """
        card = ctk.CTkFrame(
            cards_row, fg_color="white",
            height=130, corner_radius=15,
            border_width=5, border_color="#1e683e"
        )
        card.grid(row=0, column=col, sticky="nsew", padx=10)

        ctk.CTkLabel(
            card, text=title_text,
            font=("Kanit", 30, "bold"),
            width=40, height=40,
            corner_radius=10, text_color="#144e2d"
        ).pack(side=ctk.TOP, pady=(20, 0))

        value_lbl = ctk.CTkLabel(
            card, text=value_text,
            font=("Kanit", 50, "bold"), text_color="#144e2d"
        )
        value_lbl.pack(pady=(0, 10))
        return value_lbl

    # สร้างการ์ดทั้ง 4 ใบ
    total_of_year  = make_summary_card(0, "รายได้ปีนี้",    ctk.CTkLabel, report.show_year_sales())
    total_of_month = make_summary_card(1, "รายได้เดือนนี้", ctk.CTkLabel, report.show_month_sales())
    total_of_day   = make_summary_card(2, "รายได้วันนี้",   ctk.CTkLabel, report.show_day_sales())
    total_members  = make_summary_card(3, "สมาชิกทั้งหมด",  ctk.CTkLabel, report.total_members())

    # --- ปุ่ม Refresh (คอลัมน์ที่ 5) ---
    card_refresh = ctk.CTkFrame(cards_row, fg_color="#191919", height=130)
    card_refresh.grid(row=0, column=4, sticky="nsew", padx=(10, 0))

    refresh_img_normal = ctk.CTkImage(light_image=Image.open("img/Button_refresh_normal.png"), size=(358, 160))
    refresh_img_hover  = ctk.CTkImage(light_image=Image.open("img/Button_refresh_hover.png"),  size=(358, 160))

    refresh_btn = ctk.CTkButton(
        card_refresh, text="",
        image=refresh_img_normal,
        fg_color="transparent",
        hover_color="#191919",
        command=refresh_data
    )
    refresh_btn.pack(fill=ctk.BOTH, expand=True)
    refresh_btn.pack_propagate(False)

    def on_enter(event):
        """เปลี่ยนรูปปุ่ม Refresh ตอน Hover"""
        refresh_btn.configure(image=refresh_img_hover)

    def on_leave(event):
        """คืนรูปปุ่ม Refresh ตอน Mouse Leave"""
        refresh_btn.configure(image=refresh_img_normal)

    refresh_btn.bind("<Enter>", on_enter)
    refresh_btn.bind("<Leave>", on_leave)

    # =========================================================
    # ส่วนที่ 3: แถวกลาง — ซ้าย (ตาราง Sales) / ขวา (Income + Best Sellers)
    # =========================================================

    # --- คอลัมน์ซ้าย ---
    mid_row_left = ctk.CTkFrame(content, fg_color="#191919")
    mid_row_left.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

    # --- คอลัมน์ขวา ---
    mid_row_right = ctk.CTkFrame(content, fg_color="#191919")
    mid_row_right.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)
    mid_row_right.grid_columnconfigure(0, weight=1)
    mid_row_right.grid_rowconfigure(0, weight=1)

    # =========================================================
    # ส่วนที่ 4: ตาราง Master Sales (คอลัมน์ซ้าย)
    # =========================================================

    ctk.CTkLabel(
        mid_row_left, text="รายการบิลสินค้า",
        font=("Kanit", 25, "bold"),
        fg_color="#FFFFFF", text_color="#144e2d",
        height=40, corner_radius=10
    ).pack(fill=ctk.X, pady=(0, 15))

    chart_frame = ctk.CTkFrame(mid_row_left, fg_color="white", height=400, corner_radius=15)
    chart_frame.pack(fill=ctk.BOTH, expand=True, pady=(0, 15))

    # ตั้งค่า Style ของ Treeview (ใช้ร่วมกันทั้งตาราง Sales และ Best Sellers)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="white", foreground="#333333",
        rowheight=35, fieldbackground="white",
        font=("Kanit", 11), borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        font=("Kanit", 12, "bold"),
        background="#144e2d", foreground="#FFFFFF",
        borderwidth=0, relief="flat"
    )
    style.map("Treeview",         background=[("selected", "#E3F2FD")], foreground=[("selected", "#000000")])
    style.map("Treeview.Heading", background=[("selected", "#004f20")])

    def render_sales_table(days_filter=None):
        """
        แสดงตาราง Master Sales ภายใน chart_frame
        พารามิเตอร์:
            days_filter (int หรือ None): กรองข้อมูลย้อนหลังกี่วัน
                                         ถ้า None = แสดงทั้งหมด
        """
        # ลบ Widget เก่าออกก่อนสร้างใหม่ (ป้องกันการซ้อนทับ)
        for widget in chart_frame.winfo_children():
            widget.destroy()

        # สร้างตาราง Treeview
        columns = ("customer_type", "date_time", "items", "total")
        tree = ttk.Treeview(chart_frame, columns=columns, show="headings", height=15, selectmode="browse")

        tree.heading("customer_type", text="ประเภทลูกค้า",  anchor="w")
        tree.column ("customer_type", width=150, anchor="w")

        tree.heading("date_time",     text="วันเดือนปีเวลา", anchor="w")
        tree.column ("date_time",     width=180, anchor="w")

        tree.heading("items",         text="จำนวนไอเทม",    anchor="center")
        tree.column ("items",         width=100, anchor="center")

        tree.heading("total",         text="Total",          anchor="w")
        tree.column ("total",         width=120, anchor="w")

        # Scrollbar แนวตั้ง
        scrollbar = ttk.Scrollbar(chart_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left",  fill="both", expand=True, padx=(15, 0), pady=15)
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=15)

        # ดึงข้อมูลจาก report และแสดงผล
        sales_data = report.get_master_sales_data(days_filter)

        tree.tag_configure("evenrow", background="#FFFFFF")
        tree.tag_configure("oddrow",  background="#F8F9FA")

        for idx, data in enumerate(sales_data):
            customer_type = "Member" if "Member" in data["customer"] else "General Customer"
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            tree.insert("", "end", values=(customer_type, data["date"], data["items"], data["total"]), tags=(tag,))

    # โหลดตารางครั้งแรก (แสดงทั้งหมด)
    render_sales_table()

    # =========================================================
    # ส่วนที่ 5: กล่อง Income / Expense + Best Sellers (คอลัมน์ขวา)
    # =========================================================

    right_panel = ctk.CTkFrame(mid_row_right, fg_color="#191919", corner_radius=15)
    right_panel.grid(row=0, column=0, sticky="nsew", padx=(15, 0), pady=(0, 14))

    # กำหนดสัดส่วนความสูงของแต่ละแถว
    right_panel.grid_rowconfigure(0, weight=3)  # Income/Expense
    right_panel.grid_rowconfigure(1, weight=1)  # ปุ่มกรองเวลา
    right_panel.grid_rowconfigure(2, weight=5)  # Best Sellers
    right_panel.grid_columnconfigure(0, weight=1)
    right_panel.grid_columnconfigure(1, weight=1)

    # --- กล่อง Income ---
    in_come = ctk.CTkFrame(right_panel, fg_color="#FFFFFF", corner_radius=15, border_width=5, border_color="#1e683e")
    in_come.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=(0, 5))

    ctk.CTkLabel(in_come, text="Income", font=("Kanit", 30, "bold"), text_color="#1e683e").pack(side="top", pady=(10, 0))
    income = ctk.CTkLabel(in_come, text=report.total_revenue(), font=("Kanit", 80, "bold"), text_color="#1e683e")
    income.pack(expand=True, fill="both", padx=10, pady=(0, 10))

    # --- กล่อง Expense ---
    out_come = ctk.CTkFrame(right_panel, fg_color="#FFFFFF", corner_radius=15, border_width=5, border_color="#1e683e")
    out_come.grid(row=0, column=1, sticky="nsew", padx=5, pady=(0, 5))

    ctk.CTkLabel(out_come, text="Expense", font=("Kanit", 30, "bold"), text_color="#8e0000").pack(side="top", pady=(10, 0))
    expense = ctk.CTkLabel(out_come, text=report.total_expense(), font=("Kanit", 80, "bold"), text_color="#8e0000")
    expense.pack(expand=True, fill="both", padx=10, pady=(0, 10))

    # --- แถวปุ่มกรองช่วงเวลาของตาราง Sales ---
    filter_row = ctk.CTkFrame(right_panel, fg_color="transparent", corner_radius=15)
    filter_row.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=(0, 5))

    filter_row.rowconfigure(0, weight=1)
    for i in range(4):
        filter_row.columnconfigure(i, weight=1)

    # ปุ่มกรองทั้ง 4 ช่วง
    filter_buttons = [
        ("ทั้งหมด", None),
        ("7 วัน",   7),
        ("15 วัน",  15),
        ("1 เดือน", 30),
    ]
    for col_idx, (label, days) in enumerate(filter_buttons):
        padx = (0, 5) if col_idx == 0 else (5, 0) if col_idx == 3 else (5, 5)
        ctk.CTkButton(
            filter_row, text=label,
            font=("Kanit", 20, "bold"),
            command=lambda d=days: render_sales_table(d),
            fg_color="#1e683e", hover_color="#002c13"
        ).grid(row=0, column=col_idx, padx=padx, pady=(5, 0), sticky="nsew")

    # =========================================================
    # ส่วนที่ 6: ตาราง Best Sellers (สินค้าขายดี)
    # =========================================================

    best_sellers_frame = ctk.CTkFrame(right_panel, fg_color="white", corner_radius=15)
    best_sellers_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    ctk.CTkLabel(
        best_sellers_frame,
        text="🏆 สินค้าขายดี (Best Sellers)",
        font=("Kanit", 16, "bold"), text_color="#333333"
    ).pack(side="top", pady=(10, 5), padx=15, anchor="w")

    def render_best_sellers_table():
        """
        สร้างและแสดงตาราง Best Sellers โดยเรียงจากสินค้าที่สต็อกเหลือน้อยสุด
        (สินค้าที่ขายออกไปมาก = สต็อกเหลือน้อย)
        """
        # Frame สำหรับ Treeview + Scrollbar
        tv_frame = ctk.CTkFrame(best_sellers_frame, fg_color="transparent")
        tv_frame.pack(fill="both", expand=True, padx=10)

        # สร้างตาราง
        columns = ("rank", "id", "name")
        tree_bs = ttk.Treeview(tv_frame, columns=columns, show="headings", height=8, selectmode="none")

        tree_bs.heading("rank", text="อันดับ",   anchor="center")
        tree_bs.column ("rank", width=50,          anchor="center")

        tree_bs.heading("id",   text="รหัส",      anchor="center")
        tree_bs.column ("id",   width=60,          anchor="center")

        tree_bs.heading("name", text="ชื่อสินค้า", anchor="center")
        tree_bs.column ("name", width=150,          anchor="center")

        # Scrollbar แนวตั้ง
        scrollbar_bs = ttk.Scrollbar(tv_frame, orient="vertical", command=tree_bs.yview)
        tree_bs.configure(yscrollcommand=scrollbar_bs.set)

        tree_bs.pack(side="left",  fill="both", expand=True)
        scrollbar_bs.pack(side="right", fill="y")

        # ดึงข้อมูลสินค้าและเรียงตามสต็อกน้อยสุด
        bs_data    = report.product_report()
        sorted_bs  = sorted(bs_data, key=lambda item: item.get("stock", 0))

        tree_bs.tag_configure("evenrow", background="#FFFFFF")
        tree_bs.tag_configure("oddrow",  background="#F8F9FA")

        for idx, item in enumerate(sorted_bs):
            pid  = item.get("id",   "N/A")
            name = item.get("name", "Unknown")
            tag  = "evenrow" if idx % 2 == 0 else "oddrow"
            tree_bs.insert("", "end", values=(f"#{idx + 1}", pid, name), tags=(tag,))

    # โหลดตาราง Best Sellers ครั้งแรก
    render_best_sellers_table()
