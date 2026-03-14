"""
=============================================================
ไฟล์ GUI ของระบบ POS 
=============================================================
"""
import tkinter as tk         
from tkinter import ttk, messagebox   
import os                             
import textwrap                     
from PIL import Image, ImageTk        
from playsound import playsound       
import customtkinter as ctk    
import pos_logic 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ==============================================================
# ส่วนที่ 1 Numpad ที่ใช้ร่วมกันทั้งระบบ (Shared Numpad Widget)
# ==============================================================
def show_shared_numpad(parent_win, title, initial_value, callback):
    """
    สร้างและแสดง Popup แป้นกดตัวเลข (Numpad) ใช้ซ้ำได้ทั้งโปรแกรม
    """
    # สร้างหน้าต่าง Popup ลอยขึ้นมา
    popup = ctk.CTkToplevel(parent_win)
    popup.title(title)
    popup.geometry("300x500+550+300")   # ขนาดหน้าต่าง (กว้างxสูง+x+y)
    popup.grab_set()                    # ล็อกให้ผู้ใช้ต้องจัดการ Popup นี้ก่อน
    popup.transient(parent_win)         # ผูก Popup ไว้กับหน้าต่างแม่
    popup.focus_force()                 # บังคับโฟกัสไปที่ Popup

    # ตัวแปรเก็บตัวเลขที่ผู้ใช้กด (แสดงผลแบบ real-time)
    qty_var = ctk.StringVar(value=initial_value)

    # Label แสดงตัวเลขที่กำลังกรอกอยู่
    display = ctk.CTkLabel(
        popup,
        textvariable=qty_var,           # ผูกกับ qty_var → อัปเดตอัตโนมัติ
        font=("Kanit", 28, "bold"),
        fg_color="white",
        text_color="#1e683e",
        anchor="e"                       # จัดข้อความชิดขวา
    )
    display.pack(fill=tk.X, padx=10, pady=(10, 10))

    # Frame สำหรับวางปุ่ม Numpad
    keypad_frame = ctk.CTkFrame(popup)
    keypad_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

    # แบ่ง 3 คอลัมน์, 4 แถว ให้อยู่เต็มพื้นที่
    for i in range(3): keypad_frame.columnconfigure(i, weight=1)
    for i in range(4): keypad_frame.rowconfigure(i, weight=1)


    def btn_press(key):
        """
        จัดการการกดปุ่มแต่ละปุ่มบน Numpad:
            C   = ล้างตัวเลขทั้งหมด
            <-  = ลบตัวเลขสุดท้าย (Backspace)
            0-9 = เพิ่มตัวเลขต่อท้าย
        """
        current = qty_var.get()          # อ่านค่าปัจจุบัน
        if key == "C":
            qty_var.set("")              # ล้างทั้งหมด
        elif key == "<-":
            qty_var.set(current[:-1])    # ลบตัวอักษรสุดท้าย
        else:
            qty_var.set(current + key)   # ต่อตัวเลขใหม่เข้าไป


    def create_btn_command(k):
        return lambda: btn_press(k)


    # กำหนด layout ของปุ่มทั้งหมด (text, แถว, คอลัมน์)
    buttons = [
        ("7", 0, 0), ("8", 0, 1), ("9", 0, 2),
        ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
        ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
        ("C", 3, 0), ("0", 3, 1), ("<-", 3, 2),
    ]

    # วนสร้างปุ่มในตาราง
    for (text, row, col) in buttons:
        btn = ctk.CTkButton(
            keypad_frame,
            text=text,
            font=("Kanit", 25, "bold"),
            command=create_btn_command(text),  # ใช้ฟังก์ชัน wrapper ป้องกัน bug
            border_color="#1e683e",
            border_width=4,
            fg_color="transparent",
            text_color="#1e683e",
            hover_color="#61bc85"
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)


    def submit():
        """ส่งค่าที่กรอกกลับไปยัง callback แล้วปิด Popup"""
        val = qty_var.get()
        popup.destroy()     # ปิด Popup ก่อน
        callback(val)       # แล้วค่อยเรียก callback ด้วยค่าที่กรอก

    # ปุ่มยืนยัน
    ctk.CTkButton(
        popup,
        text="ยืนยัน",
        command=submit,
        font=("Kanit", 30, "bold"),
        fg_color="green",
        text_color="white"
    ).pack(fill=tk.X, padx=10, pady=20)


# ==============================================================
# ส่วนที่ 2 Popup ระบุจำนวนสินค้า
# ==============================================================

def open_numpad_popup(parent, on_add_to_cart_cb=None):
    """
    เปิด Numpad ให้ผู้ใช้กรอกจำนวนสินค้าที่ต้องการซื้อ
    """

    def on_submit(val):
        """
        ฟังก์ชันนี้ถูกเรียกเมื่อผู้ใช้กดยืนยันใน Numpad
        ทำหน้าที่ตรวจสอบค่า แล้วเพิ่มสินค้าลงบิล
        """
        # แปลงค่าที่กรอกเป็นตัวเลข ถ้ากรอกผิดหรือว่างให้ใช้ 0
        try:
            qty_int = int(val or "0")
        except ValueError:
            qty_int = 0

        # ตรวจสอบว่ากรอกจำนวนมากกว่า 0
        if qty_int <= 0:
            messagebox.showwarning("แจ้งเตือน", "กรุณาระบุจำนวนมากกว่า 0", parent=parent)
            return

        # ดึงรหัสสินค้าที่เลือกไว้จาก Global State
        pid = pos_logic.current_selected_product["id"]
        if not pid:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบข้อมูลรหัสสินค้าที่เลือก", parent=parent)
            return

        # ดึงราคาและชื่อสินค้าจาก Logic
        price = pos_logic.get_product_price(pid)
        name  = pos_logic.current_selected_product["name"]

        # เพิ่มสินค้าลงบิล → คืน (success, ข้อความ)
        success, msg = pos_logic.add_item_to_bill(pid, name, price, qty_int)
        if not success:
            messagebox.showwarning("ข้อผิดพลาด", msg, parent=parent)
            return

        messagebox.showinfo("สำเร็จ", msg, parent=parent)

        # เรียก callback เพื่อ reload ตาราง Treeview ฝั่ง GUI
        if on_add_to_cart_cb:
            on_add_to_cart_cb()

    # เปิด Numpad โดยใช้ฟังก์ชัน shared
    show_shared_numpad(parent, "ระบุจำนวนสินค้า", "", on_submit)


# ==============================================================
# ส่วนที่ 3 โหลดปุ่มสินค้า
# ==============================================================

def load_products_to_frame(frame, reload_cart_cb=None, search_keyword=""):
    """
    อ่านรายการสินค้าจาก pos_logic และสร้างปุ่มกด (Grid) ลงใน frame
    รองรับการกรองตามคำค้นหา
    """
    # ล้างปุ่มเดิมออกก่อนทุกครั้ง (ใช้ตอนค้นหาหรืออัปเดต)
    for widget in frame.winfo_children():
        widget.destroy()

    # แบ่งปุ่มเป็น 4 คอลัมน์เท่าๆ กัน
    for col_index in range(4):
        frame.columnconfigure(col_index, weight=1)

    # ดึงรายการสินค้าจาก Logic (กรองตาม keyword แล้ว)
    products = pos_logic.get_all_products_filtered(search_keyword)

    # ถ้าไม่มีสินค้าเลย → แสดงข้อความแจ้งเตือน
    if not products:
        ctk.CTkLabel(
            frame,
            text="⚠️ ไม่พบไฟล์ data/products.txt หรือไม่มีสินค้าที่ตรงกัน",
            text_color="red"
        ).grid(row=0, column=0, columnspan=4, pady=20)
        return

    # วนสร้างปุ่มสินค้าทีละตัว
    for button_count, product in enumerate(products):
        product_id   = product["id"]
        product_name = product["name"]

        def on_product_click(p_id=product_id, p_name=product_name):
            """
            เมื่อกดปุ่มสินค้า:
            1. บันทึกสินค้าที่เลือกลง Global State
            2. เปิด Numpad ให้กรอกจำนวน
            """
            pos_logic.current_selected_product["id"]   = p_id
            pos_logic.current_selected_product["name"] = p_name
            open_numpad_popup(frame, reload_cart_cb)

        # ตัดชื่อสินค้าที่ยาวให้ขึ้นบรรทัดใหม่ (กว้างสูงสุด 10 ตัวอักษรต่อบรรทัด)
        wrapped_name = "\n".join(textwrap.wrap(product_name, width=10))

        # สร้างปุ่มสินค้า
        btn = ctk.CTkButton(
            frame,
            text=wrapped_name,
            font=("Kanit", 20, "bold"),
            height=100,
            text_color="#1e683e",
            fg_color="#FFFFFF",
            hover_color="#74c494",
            border_color="#1e683e",
            border_width=3,
            command=on_product_click,
            anchor="center"
        )

        # คำนวณตำแหน่งแถวและคอลัมน์ (4 ปุ่มต่อแถว)
        row = button_count // 4   # หารเอาแถว (0, 0, 0, 0, 1, 1)
        col = button_count % 4    # เหลือเอาคอลัมน์ (0, 1, 2, 3, 0, 1)
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")


# ==============================================================
# ส่วนที่ 4 หน้าจอหลัก POS — สร้าง Frame ทั้ง 3 ส่วน
# ==============================================================

def create_three_frames(parent):
    """
    สร้างและวาง Frame หลัก 3 ส่วนบนหน้าจอ POS ดังนี้:
        Frame ซ้าย  (frame1) — ค้นหาและปุ่มสินค้า
        Frame กลาง (frame2) — ตะกร้าสินค้า (Treeview)
        Frame ขวา  (frame3) — สมาชิก, สรุปยอด, ปุ่มดำเนินการ
    """

    # ==========================================================
    # Frame ซ้าย ค้นหาและรายการปุ่มสินค้า
    # ==========================================================
    left_panel = ctk.CTkFrame(parent, fg_color="transparent", width=500)
    left_panel.pack_propagate(False)  # ล็อคขนาด ไม่ให้ขยายตาม Widget ข้างใน
    left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=(10, 0))

    # แถบค้นหาสินค้า
    search_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
    search_frame.pack(fill=tk.X, pady=5)

    # พื้นหลังปุ่ม Label "ค้นหาสินค้า"
    search_label_bg = ctk.CTkFrame(search_frame, fg_color="transparent", corner_radius=10)
    search_label_bg.pack(padx=(5, 20))

    ctk.CTkLabel(
        search_label_bg,
        text="ค้นหาสินค้า",
        font=("Kanit", 30, "bold"),
        text_color="#1e683e"
    ).pack(padx=15, pady=5)

    # ตัวแปรเก็บคำค้นหา (เชื่อมกับ Entry)
    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, font=("Kanit", 15))
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

    # ปุ่ม X ล้างคำค้นหา
    ctk.CTkButton(
        search_frame,
        text="X",
        font=("Kanit", 15, "bold"),
        fg_color="#1e683e",
        text_color="white",
        width=3,
        command=lambda: search_var.set("")   # ล้าง search_var ให้ว่าง
    ).pack(side=tk.RIGHT)

    # พื้นที่วางปุ่มสินค้า (เลื่อนขึ้นลงได้)
    frame1 = ctk.CTkScrollableFrame(
        left_panel,
        fg_color="#FFFFFF",
        scrollbar_fg_color="transparent",
        scrollbar_button_color="gray",
        scrollbar_button_hover_color="#1e683e",
    )
    frame1.pack(fill=tk.BOTH, expand=True, pady=(10, 15), padx=(10, 0))


    # ==========================================================
    # Frame กลาง ตะกร้าสินค้า
    # ==========================================================
    frame2 = ctk.CTkFrame(parent, fg_color="white", width=820)
    frame2.pack_propagate(False)  # ล็อคความกว้าง
    frame2.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 10), pady=(10, 15))

    ctk.CTkLabel(
        frame2,
        text="รายการสินค้า",
        font=("Kanit", 25, "bold"),
        text_color="#1e683e"
    ).pack(pady=10)

    # Frame ห่อ Treeview + Scrollbar
    tree_frame = ctk.CTkFrame(frame2, fg_color="transparent")
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Scrollbar สำหรับตาราง
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # สร้างตาราง Treeview (ตะกร้าสินค้า)
    columns = ("id", "name", "price", "total")
    cart_tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings",                     # ซ่อน tree column แสดงแค่หัวคอลัมน์
        height=15,
        yscrollcommand=tree_scroll.set,      # เชื่อม Scrollbar กับตาราง
        selectmode="browse"                  # เลือกได้ทีละ 1 แถว
    )
    tree_scroll.config(command=cart_tree.yview)

    # ปรับสไตล์ตาราง
    style = ttk.Style()
    style.theme_use("clam")  # theme "clam" รองรับการปรับแต่งสีได้
    style.configure(
        "Treeview",
        background="#000000",
        foreground="#333333",
        rowheight=35,
        fieldbackground="white",
        font=("Kanit", 11),
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",              # ส่วนหัวตาราง
        font=("Kanit", 12, "bold"),
        background="#1e683e",
        foreground="white",
        borderwidth=0,
        relief="flat"
    )
    # map() = กำหนดสีตามสถานะ (เช่น ตอนถูก Select)
    style.map("Treeview",         background=[("selected", "black")],  foreground=[("selected", "#000000")])
    style.map("Treeview.Heading", background=[("active",   "black")])

    # กำหนดหัวคอลัมน์และความกว้าง
    cart_tree.heading("id",    text="รหัสสินค้า")
    cart_tree.heading("name",  text="สินค้า")
    cart_tree.heading("price", text="ราคา/หน่วย")
    cart_tree.heading("total", text="ราคารวม")

    cart_tree.column("id",    width=80,  anchor="center")
    cart_tree.column("name",  width=150, anchor="center")
    cart_tree.column("price", width=80,  anchor="center")
    cart_tree.column("total", width=80,  anchor="center")

    cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    # ==========================================================
    # Frame ขวา สมาชิก + สรุปยอด + ปุ่มดำเนินการ
    # ==========================================================
    frame3 = ctk.CTkFrame(parent, fg_color="#FFFFFF", width=600)
    frame3.pack_propagate(False)
    frame3.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 15), pady=(10, 15))


    # กล่องแสดงสถานะสมาชิก
    member_frame = ctk.CTkFrame(
        frame3,
        border_width=5,
        fg_color="white",
        border_color="#1e683e",
        corner_radius=10
    )
    member_frame.pack(fill=tk.X, pady=(10, 10), padx=(10, 10))

    # ตัวแปรข้อความแสดงสถานะ (จะเปลี่ยนเมื่อ Login/Logout)
    lbl_member_status_var = ctk.StringVar(value="ลูกค้าทั่วไป")
    ctk.CTkLabel(
        member_frame,
        textvariable=lbl_member_status_var,
        font=("Kanit", 40, "bold"),
        text_color="#1e683e"
    ).pack(pady=(30, 30))


    # ----------------------------------------------------------
    # ฟังก์ชัน Reload ตะกร้าสินค้า
    # ----------------------------------------------------------
    def reload_cart():
        """
        อ่านบิลปัจจุบันจาก pos_logic แล้วแสดงผลใน Treeview
        พร้อมคำนวณและอัปเดตยอดเงินทั้งหมด
        """
        # ลบแถวเก่าทั้งหมดออกก่อน
        for row in cart_tree.get_children():
            cart_tree.delete(row)

        # กำหนดสีสลับแถว (Zebra striping) เพื่อให้อ่านง่าย
        cart_tree.tag_configure("evenrow", background="#FFFFFF")   # แถวคู่ - ขาว
        cart_tree.tag_configure("oddrow",  background="#F1F8E9")   # แถวคี่ - เขียวอ่อน

        # อ่านรายการสินค้าจากไฟล์บิล
        items = pos_logic.read_bill_lines()
        raw_total = 0.0

        for idx, item in enumerate(items):
            raw_total += item["total"]  # รวมยอดก่อนคิดส่วนลด

            tag = "evenrow" if idx % 2 == 0 else "oddrow"  # สลับสีแถว
            cart_tree.insert(
                "", tk.END,
                values=(
                    item["pid"],
                    f"{item['name']} (x{item['qty']})",  # แสดงชื่อ + จำนวน
                    f"{item['price']:.2f}",              # ราคาต่อหน่วย ทศนิยม 2 ตำแหน่ง
                    f"{item['total']:.2f}"               # ราคารวม
                ),
                tags=(tag,)
            )

        # คำนวณยอดสุทธิผ่าน Logic (ส่วนลด + VAT)
        totals = pos_logic.calculate_totals(raw_total)

        # อัปเดต Label แสดงยอดเงิน
        lbl_subtotal_var.set(f"{totals['subtotal']:,.2f} บาท")
        lbl_discount_var.set(f"-{totals['discount']:,.2f} บาท")
        lbl_vat_var.set(f"+{totals['vat']:,.2f} บาท")
        lbl_grand_total_var.set(f"{totals['grand_total']:,.2f} บาท")


    # ----------------------------------------------------------
    # ฟังก์ชัน เปิด Numpad สำหรับกรอกเบอร์โทรศัพท์
    # ----------------------------------------------------------
    def open_phone_numpad(parent_win, entry_widget):
        """
        เปิด Numpad ให้ผู้ใช้กดตัวเลขเพื่อกรอกเบอร์โทรศัพท์
        แล้วนำค่าที่ได้ใส่ลงใน Entry Widget ที่ระบุ
        """
        def on_submit(val):
            entry_widget.delete(0, tk.END)   # ลบข้อมูลเก่าใน Entry
            entry_widget.insert(0, val)      # ใส่ค่าใหม่ที่กรอกจาก Numpad

        show_shared_numpad(parent_win, "แป้นตัวเลข", entry_widget.get(), on_submit)


    # ----------------------------------------------------------
    # ฟังก์ชัน Popup สมัครสมาชิก
    # ----------------------------------------------------------
    def popup_register():
        """เปิดหน้าต่าง Popup สำหรับกรอกข้อมูลสมัครสมาชิกใหม่"""
        reg_pop = ctk.CTkToplevel(parent)
        reg_pop.title("ลงทะเบียนสมาชิกใหม่")
        reg_pop.geometry("400x350+700+300")
        reg_pop.grab_set()  # ล็อกให้จัดการ Popup นี้ก่อน

        ctk.CTkLabel(reg_pop, text="เบอร์โทรศัพท์", font=("Kanit", 30, "bold"), text_color="#1e683e").pack(pady=5)
        ent_phone = ctk.CTkEntry(reg_pop)
        ent_phone.pack(fill="both", padx=30)
        # เมื่อกดที่ช่องเบอร์โทร → เปิด Numpad
        ent_phone.bind("<Button-1>", lambda e: open_phone_numpad(reg_pop, ent_phone))

        ctk.CTkLabel(reg_pop, text="ชื่อ",     font=("Kanit", 30, "bold"), text_color="#1e683e").pack(pady=5)
        ent_fname = ctk.CTkEntry(reg_pop)
        ent_fname.pack(fill="both", padx=30)

        ctk.CTkLabel(reg_pop, text="นามสกุล", font=("Kanit", 30, "bold"), text_color="#1e683e").pack(pady=5)
        ent_lname = ctk.CTkEntry(reg_pop)
        ent_lname.pack(fill="both", padx=30)

        def do_register():
            """ดึงค่าจาก Entry ทั้งหมด แล้วส่งให้ pos_logic ลงทะเบียน"""
            phone = ent_phone.get().strip()  # .strip() ลบช่องว่างหัวท้าย
            fname = ent_fname.get().strip()
            lname = ent_lname.get().strip()

            # ตรวจสอบว่ากรอกครบทุกช่อง
            if not phone or not fname or not lname:
                messagebox.showwarning("แจ้งเตือน", "กรุณากรอกข้อมูลให้ครบทุกช่อง", parent=reg_pop)
                return

            # ส่งให้ Logic ลงทะเบียน → คืน (success, ข้อความ)
            success, msg = pos_logic.do_register_member(phone, fname, lname)
            if success:
                messagebox.showinfo("สำเร็จ",      msg, parent=reg_pop)
                reg_pop.destroy()  # ปิด Popup เมื่อสมัครสำเร็จ
            else:
                messagebox.showwarning("แจ้งเตือน", msg, parent=reg_pop)

        ctk.CTkButton(
            reg_pop, text="ยืนยันสมาชิก",
            font=("Kanit", 20, "bold"),
            command=do_register,
            fg_color="#1e683e", hover_color="#003315", text_color="white"
        ).pack(pady=15)


    # ----------------------------------------------------------
    # ฟังก์ชัน Popup เข้าสู่ระบบสมาชิก
    # ----------------------------------------------------------
    def popup_login():
        """เปิดหน้าต่าง Popup ให้กรอกเบอร์โทรศัพท์เพื่อ Login สมาชิก"""
        log_pop = ctk.CTkToplevel(parent)
        log_pop.title("เข้าสู่ระบบสมาชิก")
        log_pop.geometry("400x350+700+300")
        log_pop.grab_set()

        ctk.CTkLabel(log_pop, text="ใส่เบอร์โทรศัพท์", font=("Kanit", 30, "bold"), text_color="#1e683e").pack(pady=10)
        ent_phone = ctk.CTkEntry(log_pop)
        ent_phone.pack(fill="both", padx=30)
        ent_phone.bind("<Button-1>", lambda e: open_phone_numpad(log_pop, ent_phone))

        def do_login():
            """ค้นหาสมาชิกจากเบอร์ที่กรอก และอัปเดตสถานะถ้าพบ"""
            mem = pos_logic.do_login_member(ent_phone.get())  # ค้นหาสมาชิก

            if mem:
                pos_logic.save_member_to_state(mem)           # บันทึกลง Global State
                lbl_member_status_var.set(f"สมาชิก | {mem['first_name']} {mem['last_name']}")
                messagebox.showinfo("สำเร็จ", "ลงชื่อเข้าใช้สมาชิกสำเร็จ ได้รับส่วนลด 25%", parent=log_pop)
                log_pop.destroy()
                reload_cart()   # โหลดตะกร้าใหม่ เพราะได้ส่วนลด 25% แล้ว
            else:
                messagebox.showerror("ไม่พบข้อมูล", "ไม่พบเบอร์โทรศัพท์นี้ในระบบ", parent=log_pop)

        ctk.CTkButton(
            log_pop, text="ตรวจสอบ",
            font=("Kanit", 20, "bold"),
            command=do_login,
            fg_color="#1e683e", hover_color="#003315", text_color="white"
        ).pack(pady=15)


    # ปุ่ม "สมัครสมาชิก" และ "เข้าสู่ระบบ" 
    btn_frame = ctk.CTkFrame(frame3, fg_color="transparent")
    btn_frame.pack(fill=tk.X, padx=(10, 10))

    ctk.CTkButton(
        btn_frame, text="สมัครสมาชิก",
        font=("Kanit", 25), command=popup_register,
        fg_color="#1e683e", hover_color="#003a17"
    ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

    ctk.CTkButton(
        btn_frame, text="เข้าสู่ระบบ",
        font=("Kanit", 25), command=popup_login,
        fg_color="#1e683e", hover_color="#003a17"
    ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))


    # ----------------------------------------------------------
    # ฟังก์ชัน ออกจากระบบสมาชิก
    # ----------------------------------------------------------
    def logout_member():
        """ล้างข้อมูลสมาชิกออกจาก Global State แล้ว reload ตะกร้า"""
        pos_logic.logout_member_state()                # ล้างข้อมูลใน Logic
        lbl_member_status_var.set("ลูกค้าทั่วไป")    # คืนค่าร Label
        reload_cart()                                  # คำนวณยอดใหม่ (ไม่มีส่วนลดแล้ว)

    ctk.CTkButton(
        frame3, text="ออกจากระบบสมาชิก",
        font=("Kanit", 18), command=logout_member,
        text_color="#FFFFFF", fg_color="#1e683e", hover_color="#003a17"
    ).pack(fill=tk.X, padx=(10, 10), pady=2)


    # ==========================================================
    # ส่วนสรุปยอดชำระ
    # ==========================================================
    ctk.CTkLabel(
        frame3, text="สรุปยอดชำระ",
        font=("Kanit", 25, "bold"), text_color="#1e683e"
    ).pack(fill=tk.X, padx=(10, 10), pady=(20, 0))

    summary_frame = ctk.CTkFrame(
        frame3, fg_color="white",
        border_width=5, border_color="#1e683e", corner_radius=10
    )
    summary_frame.pack(fill=tk.X, padx=10, pady=5)

    # ตัวแปร StringVar สำหรับแสดงยอดเงินแต่ละส่วน (อัปเดตได้โดยไม่ต้องสร้าง Widget ใหม่)
    lbl_subtotal_var    = ctk.StringVar(value="0.00 บาท")   # ยอดก่อนลด
    lbl_discount_var    = ctk.StringVar(value="0.00 บาท")   # ส่วนลดสมาชิก
    lbl_vat_var         = ctk.StringVar(value="0.00 บาท")   # VAT
    lbl_grand_total_var = ctk.StringVar(value="0.00 บาท")   # ยอดสุทธิ

    # แถวที่ 0 ราคารวม
    ctk.CTkLabel(summary_frame, text="ราคารวม",        font=("Kanit", 20)).grid(row=0, column=0, sticky="w", padx=(20, 0), pady=10)
    ctk.CTkLabel(summary_frame, textvariable=lbl_subtotal_var, font=("Kanit", 20)).grid(row=0, column=1, sticky="e", padx=(0, 20), pady=10)

    # แถวที่ 1 ส่วนลดสมาชิก (สีแดง)
    ctk.CTkLabel(summary_frame, text="ส่วนลดสมาชิก:",  font=("Kanit", 20), text_color="red").grid(row=1, column=0, sticky="w", padx=(20, 0), pady=10)
    ctk.CTkLabel(summary_frame, textvariable=lbl_discount_var, font=("Kanit", 20), text_color="red").grid(row=1, column=1, sticky="e", padx=(0, 20), pady=10)

    # แถวที่ 2 VAT 7% (สีส้ม)
    ctk.CTkLabel(summary_frame, text="VAT 7%:",         font=("Kanit", 20), text_color="orange").grid(row=2, column=0, sticky="w", padx=(20, 0), pady=10)
    ctk.CTkLabel(summary_frame, textvariable=lbl_vat_var, font=("Kanit", 20), text_color="#f98404").grid(row=2, column=1, sticky="e", padx=(0, 20), pady=10)

    # แถวที่ 3 ราคาสุทธิ (ใหญ่กว่า, สีเขียว)
    ctk.CTkLabel(summary_frame, text="ราคาสุทธิ",      font=("Kanit", 30, "bold"), text_color="green").grid(row=3, column=0, sticky="w", padx=(20, 0), pady=(40, 10))
    ctk.CTkLabel(summary_frame, textvariable=lbl_grand_total_var, font=("Kanit", 30, "bold"), text_color="green").grid(row=3, column=1, sticky="e", padx=(0, 20), pady=(40, 10))

    summary_frame.columnconfigure(1, weight=1)  # คอลัมน์ขวาขยายเต็มพื้นที่

    # เชื่อมการค้นหากับฟังก์ชันโหลดปุ่มสินค้า
    # trace_add("write") = เรียกฟังก์ชันทุกครั้งที่ search_var เปลี่ยนแปลง
    search_var.trace_add("write", lambda *args: load_products_to_frame(frame1, reload_cart, search_var.get()))

    # โหลดปุ่มสินค้าและตะกร้าครั้งแรก
    load_products_to_frame(frame1, reload_cart)
    reload_cart()


    # ==========================================================
    # ส่วนปุ่มดำเนินการ (ล้างตะกร้า, พักบิล, เรียกคืนบิล)
    # ==========================================================
    action_frame = ctk.CTkFrame(frame3, fg_color="transparent")
    action_frame.pack(fill=tk.X, padx=(10, 10), pady=(20, 0))


    # ----------------------------------------------------------
    # ฟังก์ชัน ล้างตะกร้า
    # ----------------------------------------------------------
    def clear_cart():
        """ถามยืนยันก่อน แล้วเคลียร์บิลทั้งหมดผ่าน pos_logic"""
        bill_path = pos_logic.get_bill_path()

        # ตรวจสอบว่ามีบิลอยู่ไหม
        if not os.path.exists(bill_path):
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return

        with open(bill_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return

        # ถามยืนยันก่อนล้าง
        confirm = messagebox.askyesno("ยืนยัน", "คุณแน่ใจหรือไม่ที่จะล้างตะกร้าทั้งหมด?")
        if confirm:
            pos_logic.clear_bill_file()  # ล้างไฟล์บิล
            reload_cart()                # โหลดตะกร้าใหม่ (จะว่างเปล่า)
            messagebox.showinfo("สำเร็จ", "เคลียร์ตะกร้าเรียบร้อยแล้ว")


    # ----------------------------------------------------------
    # ฟังก์ชัน พักบิล
    # ----------------------------------------------------------
    def hold_bill_action():
        """บันทึกบิลปัจจุบันไว้ชั่วคราว แล้วล้างตะกร้า (ผ่าน pos_logic)"""
        success, msg = pos_logic.hold_bill()
        if success:
            reload_cart()                         # ล้างตะกร้าหลังพัก
            messagebox.showinfo("สำเร็จ", msg)
        else:
            messagebox.showinfo("แจ้งเตือน", msg)


    # ----------------------------------------------------------
    # ฟังก์ชัน เรียกคืนบิล
    # ----------------------------------------------------------
    def recall_bill_action():
        """
        เปิด Popup แสดงรายการบิลที่พักไว้ทั้งหมด
        ให้ผู้ใช้เลือกแล้วเรียกคืนมาใส่ตะกร้าปัจจุบัน
        """
        files = pos_logic.get_held_bill_files()

        if not files:
            messagebox.showinfo("แจ้งเตือน", "ไม่มีบิลที่ถูกพักไว้")
            return

        # สร้าง Popup แสดงรายการบิลพัก
        recall_pop = ctk.CTkToplevel(parent)
        recall_pop.title("เลือกบิลที่ต้องการเรียกคืน")
        recall_pop.geometry("300x500+700+350")
        recall_pop.grab_set()

        ctk.CTkLabel(recall_pop, text="รายการพักบิลทั้งหมด", font=("Kanit", 20, "bold")).pack(pady=5)

        # Listbox แสดงชื่อบิลพัก
        listbox = tk.Listbox(recall_pop, font=("Kanit", 12))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for f in files:
            # ตัด bill_ หน้า และ .txt ท้ายออก ให้เหลือแค่วันเวลา เช่น 09-03-2026  21-00
            display_name = f.replace("bill_", "").replace(".txt", "")
            listbox.insert(tk.END, display_name)

        def do_recall():
            """เรียกคืนบิลที่ผู้ใช้เลือกจาก Listbox"""
            selected = listbox.curselection()  # ดึง index ที่เลือก เป็น tuple เช่น (2,)
            if not selected:
                messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกบิล!", parent=recall_pop)
                return

            selected_file = files[selected[0]]  # เอาชื่อไฟล์จริงตาม index ที่เลือก
            success, msg = pos_logic.recall_bill(selected_file)
            if success:
                messagebox.showinfo("สำเร็จ", msg, parent=recall_pop)
                reload_cart()          # โหลดตะกร้าใหม่
                recall_pop.destroy()   # ปิด Popup

        ctk.CTkButton(
            recall_pop, text="เรียกคืนบิลนี้",
            font=("Kanit", 20, "bold"),
            fg_color= "#1e683e",
            hover_color="#084622",
            command=do_recall,
        ).pack(pady=20)


    # สร้างปุ่มดำเนินการทั้ง 3 ปุ่ม
    ctk.CTkButton(
        action_frame, text="พักบิล",
        font=("Kanit", 25, "bold"),
        command=hold_bill_action,
        fg_color="orange", hover_color="#9b5c00"
    ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 5))

    ctk.CTkButton(
        action_frame, text="เรียกคืนบิล",
        font=("Kanit", 25, "bold"),
        command=recall_bill_action,
        fg_color="#006b70", hover_color="#003a3a"
    ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(5, 5))

    ctk.CTkButton(
        action_frame, text="ล้างตะกร้า",
        font=("Kanit", 25, "bold"),
        command=clear_cart,
        fg_color="red", text_color="white", hover_color="#8e0000"
    ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(5, 0))


    # ----------------------------------------------------------
    # ฟังก์ชัน ยืนยันชำระเงิน
    # ----------------------------------------------------------
    def confirm_checkout():
        """
        เรียก pos_logic.process_checkout() เพื่อดำเนินการชำระเงิน:
            ถ้าสำเร็จ  → เล่นเสียง, logout สมาชิก, ล้างตะกร้า
            ถ้าไม่สำเร็จ → แสดงข้อความ Error และ reload ตะกร้า
        """
        success, msg, _pdf = pos_logic.process_checkout()
        # _pdf = ชื่อไฟล์ PDF ใบเสร็จ (ไม่ใช้ในฟังก์ชันนี้ จึงใส่ _ นำหน้า)

        if success:
            logout_member()  # Logout สมาชิกหลังชำระเงินเสร็จ รอลูกค้าคนต่อไป
            try:
                playsound(os.path.join(BASE_DIR, "sound", "cat.mp3"),          block=False)  # เล่นเสียงแมวร้อง
                playsound(os.path.join(BASE_DIR, "sound", "money_pickup.mp3"), block=False)  # เล่นเสียงรับเงิน
            except Exception:
                print("เล่นเสียงไม่ได้")  # ถ้าไฟล์เสียงไม่มีก็ไม่ Error
        else:
            messagebox.showwarning("ข้อผิดพลาด", msg)
            reload_cart()  # โหลดตะกร้าใหม่ (อาจถูกล้างหลังสต็อกไม่พอ)


    # ปุ่มรูปแมวสำหรับยืนยันชำระเงิน
    # โหลดรูปแมว 2 แบบ: ปกติ และตอน Hover
    cat_img_normal = ctk.CTkImage(light_image=Image.open(os.path.join(BASE_DIR, "img", "cat_normal.png")), size=(500, 150))
    cat_img_hover  = ctk.CTkImage(light_image=Image.open(os.path.join(BASE_DIR, "img", "cat_hover.png")),  size=(500, 150))

    btn_cat = ctk.CTkButton(
        frame3,
        text="",                    # ไม่มีข้อความ ใช้รูปแทน
        image=cat_img_normal,
        fg_color="transparent",
        hover_color="#FFFFFF",
        command=confirm_checkout    # กดแล้วชำระเงิน
    )
    btn_cat.pack(pady=(20, 0))

    def on_enter(event):
        """เปลี่ยนรูปแมวเป็นแบบ Hover เมื่อเมาส์เข้ามา"""
        btn_cat.configure(image=cat_img_hover)

    def on_leave(event):
        """คืนรูปแมวปกติเมื่อเมาส์ออกไป"""
        btn_cat.configure(image=cat_img_normal)

    btn_cat.bind("<Enter>", on_enter)  # เมาส์เข้า
    btn_cat.bind("<Leave>", on_leave)  # เมาส์ออก

    # ข้อความขอบคุณด้านล่าง
    ctk.CTkLabel(
        frame3,
        text="ขอบคุณที่อุดหนุนนะ เมี๊ยววว!!",
        font=("Kanit", 40, "bold"),
        text_color="#1e683e"
    ).pack(pady=(30, 0))

    # ส่ง Frame ทั้ง 3 กลับให้ผู้เรียก (main.py) ใช้งานต่อได้
    return frame1, frame2, frame3