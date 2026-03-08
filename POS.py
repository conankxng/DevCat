"""
ไฟล์นี้รวมโค้ด GUI ทั้งหมดของระบบ POS
(ไม่มี Logic เฉพาะการสร้างหน้าจอ, ปุ่ม, และการแสดงผล)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import textwrap
from PIL import Image, ImageTk
from playsound import playsound
import customtkinter as ctk
import pos_logic

# ========================================================================= #
# ฟังชั่น Refresh ปุ่มสินค้า
# ========================================================================= #
def refresh_data():
    """โหลดข้อมูลใหม่จาก report และอัปเดตทุก Label บนหน้าจอ"""
    total_of_year.configure(text=str(report.show_year_sales()))

# ========================================================================= #
# ส่วนที่ 1: Numpad ที่ใช้ร่วมกันทั้งระบบ (Shared Numpad Widget)
# ========================================================================= #

def show_shared_numpad(parent_win, title, initial_value, callback):
    """
    แสดง Popup แป้นกดตัวเลข (Numpad) แบบ reusable
    พารามิเตอร์:
        parent_win   : หน้าต่างแม่ที่ Popup จะ grab focus จาก
        title        : ชื่อหัวข้อของ Popup
        initial_value: ค่าเริ่มต้นใน Display
        callback     : ฟังก์ชันที่จะถูกเรียกพร้อมค่าที่กรอก เมื่อกด "ยืนยัน"
    """
    popup = ctk.CTkToplevel(parent_win)
    popup.title(title)
    popup.geometry("300x500+550+300")
    popup.grab_set()
    popup.transient(parent_win)
    popup.focus_force()

    qty_var = ctk.StringVar(value=initial_value)

    # แสดงตัวเลขที่กำลังกรอก
    display = ctk.CTkLabel(
        popup, textvariable=qty_var,
        font=("Kanit", 28, "bold"),
        fg_color="white",
        text_color="#1e683e",
        anchor="e"
    )
    display.pack(fill=tk.X, padx=10, pady=(10, 10))

    keypad_frame = ctk.CTkFrame(popup)
    keypad_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

    for i in range(3): keypad_frame.columnconfigure(i, weight=1)
    for i in range(4): keypad_frame.rowconfigure(i, weight=1)

    def btn_press(key):
        """จัดการการกดปุ่มแต่ละปุ่มบน Numpad"""
        current = qty_var.get()
        if key == "C":
            qty_var.set("")
        elif key == "<-":
            qty_var.set(current[:-1])
        else:
            qty_var.set(current + key)

    def create_btn_command(k):
        """สร้าง command function สำหรับแต่ละปุ่ม (ป้องกัน closure bug)"""
        return lambda: btn_press(k)

    # วาง layout ปุ่ม Numpad
    buttons = [
        ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
        ('C', 3, 0), ('0', 3, 1), ('<-', 3, 2),
    ]

    for (text, row, col) in buttons:
        btn = ctk.CTkButton(
            keypad_frame, text=text,
            font=("Kanit", 25, "bold"),
            command=create_btn_command(text),
            border_color="#1e683e",
            border_width=4,
            fg_color="transparent",
            text_color="#1e683e",
            hover_color="#61bc85"
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    def submit():
        """ส่งค่าที่กรอกกลับ callback และปิด Popup"""
        val = qty_var.get()
        popup.destroy()
        callback(val)

    ctk.CTkButton(
        popup, text="ยืนยัน",
        command=submit,
        font=("Kanit", 30, "bold"),
        fg_color="green",
        text_color="white"
    ).pack(fill=tk.X, padx=10, pady=20)


# ========================================================================= #
# ส่วนที่ 2: Popup สำหรับระบุจำนวนสินค้า (Product Quantity Numpad)
# ========================================================================= #

def open_numpad_popup(parent, on_add_to_cart_cb=None):
    """
    เปิด Numpad ให้ผู้ใช้กรอกจำนวนสินค้าที่ต้องการ
    เมื่อยืนยันแล้วจะเรียก pos_logic.add_item_to_bill() เพื่อบันทึกลงตะกร้า
    พารามิเตอร์:
        parent           : หน้าต่างแม่สำหรับ Popup
        on_add_to_cart_cb: callback เพื่อ reload ตะกร้าหลังเพิ่มสินค้าสำเร็จ
    """
    def on_submit(val):
        """ตรวจสอบค่าและบันทึกสินค้าลงบิลเมื่อผู้ใช้ยืนยัน"""
        try:
            qty_int = int(val or "0")
        except ValueError:
            qty_int = 0

        if qty_int <= 0:
            messagebox.showwarning("แจ้งเตือน", "กรุณาระบุจำนวนมากกว่า 0", parent=parent)
            return

        pid = pos_logic.current_selected_product["id"]
        if not pid:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบข้อมูลรหัสสินค้าที่เลือก", parent=parent)
            return

        # ดึงราคาจาก Logic
        price = pos_logic.get_product_price(pid)
        name = pos_logic.current_selected_product["name"]

        # เพิ่มลงบิลผ่าน Logic
        success, msg = pos_logic.add_item_to_bill(pid, name, price, qty_int)
        if not success:
            messagebox.showwarning("ข้อผิดพลาด", msg, parent=parent)
            return

        messagebox.showinfo("สำเร็จ", msg, parent=parent)

        # เรียก reload ตารางฝั่ง GUI
        if on_add_to_cart_cb:
            on_add_to_cart_cb()

    show_shared_numpad(parent, "ระบุจำนวนสินค้า", "", on_submit)


# ========================================================================= #
# ส่วนที่ 3: ฟังก์ชันโหลดปุ่มสินค้า (Product Button Grid)
# ========================================================================= #

def load_products_to_frame(frame, reload_cart_cb=None, search_keyword=""):
    """
    อ่านสินค้าจาก pos_logic และสร้างปุ่มกด (Grid) ลงใน frame ซ้ายสุด
    รองรับการกรองตามคำค้นหา
    พารามิเตอร์:
        frame          : CTkScrollableFrame ที่จะวางปุ่มลงไป
        reload_cart_cb : callback ให้เรียกหลังจากเพิ่มสินค้าลงตะกร้า
        search_keyword : คำค้นหาสำหรับกรองสินค้า
    """
    # ล้างปุ่มเดิมออกก่อน (สำหรับตอนค้นหาและอัปเดต)
    for widget in frame.winfo_children():
        widget.destroy()

    # กำหนดให้มี 4 คอลัมน์โดยขยายเท่าๆ กัน
    for col_index in range(4):
        frame.columnconfigure(col_index, weight=1)

    # ดึงรายการสินค้าจาก Logic (กรองตาม keyword แล้ว)
    products = pos_logic.get_all_products_filtered(search_keyword)

    if not products:
        # ถ้าไม่มีสินค้าหรือไม่พบไฟล์
        ctk.CTkLabel(
            frame,
            text="⚠️ ไม่พบไฟล์ data/products.txt หรือไม่มีสินค้าที่ตรงกัน",
            text_color="red"
        ).grid(row=0, column=0, columnspan=4, pady=20)
        return

    for button_count, product in enumerate(products):
        product_id = product["id"]
        product_name = product["name"]

        def on_product_click(p_id=product_id, p_name=product_name):
            """บันทึกสินค้าที่คลิกลง Global State แล้วเปิด Numpad"""
            pos_logic.current_selected_product["id"] = p_id
            pos_logic.current_selected_product["name"] = p_name
            open_numpad_popup(frame, reload_cart_cb)

        # ตัดข้อความยาวให้ขึ้นบรรทัดใหม่
        wrapped_name = "\n".join(textwrap.wrap(product_name, width=10))

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

        row = button_count // 4
        col = button_count % 4
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")


# ========================================================================= #
# ส่วนที่ 4: หน้าจอหลัก POS — สร้าง Frame ทั้ง 3 ส่วน
# ========================================================================= #

def create_three_frames(parent):
    """
    สร้างและวาง Frame หลัก 3 ส่วนบนหน้าจอ POS:
        - Frame ซ้าย  (frame1): ค้นหาและรายการปุ่มสินค้า
        - Frame กลาง (frame2): ตะกร้าสินค้า (Treeview)
        - Frame ขวา  (frame3): ข้อมูลสมาชิก, สรุปยอด, ปุ่มดำเนินการ

    คืนค่า: (frame1, frame2, frame3)
    """

    # =========================================================
    # Frame ซ้าย: ค้นหาและรายการสินค้า
    # =========================================================
    left_panel = ctk.CTkFrame(parent, fg_color="transparent", width=500)
    left_panel.pack_propagate(False)
    left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=(10, 0))

    # --- แถบค้นหา ---
    search_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
    search_frame.pack(fill=tk.X, pady=5)

    search_label_bg = ctk.CTkFrame(search_frame, fg_color="transparent", corner_radius=10)
    search_label_bg.pack(padx=(5, 20))

    ctk.CTkLabel(
        search_label_bg, text="ค้นหาสินค้า",
        font=("Kanit", 30, "bold"), text_color="#1e683e"
    ).pack(padx=15, pady=5)

    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, font=("Kanit", 15))
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

    ctk.CTkButton(
        search_frame, text="X",
        font=("Kanit", 15, "bold"),
        fg_color="#1e683e", text_color="white",
        width=3, command=lambda: search_var.set("")
    ).pack(side=tk.RIGHT)

    # --- พื้นที่วางปุ่มสินค้า (Scrollable) ---
    frame1 = ctk.CTkScrollableFrame(
        left_panel,
        fg_color="#FFFFFF",
        scrollbar_fg_color="transparent",
        scrollbar_button_color="gray",
        scrollbar_button_hover_color="#1e683e",
    )
    frame1.pack(fill=tk.BOTH, expand=True, pady=(10, 15), padx=(10, 0))

    # =========================================================
    # Frame กลาง: ตะกร้าสินค้า (Treeview Table)
    # =========================================================
    frame2 = ctk.CTkFrame(parent, fg_color="white", width=820)
    frame2.pack_propagate(False)
    frame2.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 10), pady=(10, 15))

    ctk.CTkLabel(
        frame2, text="รายการสินค้า",
        font=("Kanit", 25, "bold"), text_color="#1e683e"
    ).pack(pady=10)

    # กรอบสำหรับ Treeview และ Scrollbar
    tree_frame = ctk.CTkFrame(frame2, fg_color="transparent")
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # --- ตั้งค่า Treeview ---
    columns = ("id", "name", "price", "total")
    cart_tree = ttk.Treeview(
        tree_frame, columns=columns, show="headings",
        height=15, yscrollcommand=tree_scroll.set, selectmode="browse"
    )
    tree_scroll.config(command=cart_tree.yview)

    # ปรับธีมสี Treeview ให้เข้ากับสีเขียวของร้าน
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#000000", foreground="#333333",
        rowheight=35, fieldbackground="white",
        font=("Kanit", 11), borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        font=("Kanit", 12, "bold"),
        background="#1e683e", foreground="white",
        borderwidth=0, relief="flat"
    )
    style.map('Treeview', background=[('selected', 'black')], foreground=[('selected', '#000000')])
    style.map('Treeview.Heading', background=[('active', 'black')])

    # กำหนดหัวข้อและขนาดคอลัมน์
    cart_tree.heading("id", text="รหัสสินค้า")
    cart_tree.heading("name", text="สินค้า")
    cart_tree.heading("price", text="ราคา/หน่วย")
    cart_tree.heading("total", text="ราคารวม")

    cart_tree.column("id", width=80, anchor="center")
    cart_tree.column("name", width=150, anchor="center")
    cart_tree.column("price", width=80, anchor="center")
    cart_tree.column("total", width=80, anchor="center")

    cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # =========================================================
    # Frame ขวา: สมาชิก + สรุปยอด + ปุ่มดำเนินการ
    # =========================================================
    frame3 = ctk.CTkFrame(parent, fg_color="#FFFFFF", width=600)
    frame3.pack_propagate(False)
    frame3.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 15), pady=(10, 15))

    # ======================= ส่วนสมาชิก =======================
    member_frame = ctk.CTkFrame(
        frame3, border_width=5,
        fg_color="white", border_color="#1e683e", corner_radius=10
    )
    member_frame.pack(fill=tk.X, pady=(10, 10), padx=(10, 10))

    lbl_member_status_var = ctk.StringVar(value="ลูกค้าทั่วไป")
    ctk.CTkLabel(
        member_frame, textvariable=lbl_member_status_var,
        font=("Kanit", 40, "bold"), text_color="#1e683e"
    ).pack(pady=(30, 30))

    # --- ฟังก์ชัน Reload ตะกร้า (อ่านจาก pos_logic) ---
    def reload_cart():
        """อ่านบิลจาก pos_logic และแสดงผลใน Treeview พร้อมคำนวณยอด"""
        for row in cart_tree.get_children():
            cart_tree.delete(row)

        # สลับสีแถว (Zebra striping)
        cart_tree.tag_configure('evenrow', background='#FFFFFF')
        cart_tree.tag_configure('oddrow', background='#F1F8E9')

        items = pos_logic.read_bill_lines()
        raw_total = 0.0
        for idx, item in enumerate(items):
            raw_total += item["total"]
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            cart_tree.insert(
                "", tk.END,
                values=(item["pid"], f"{item['name']} (x{item['qty']})", f"{item['price']:.2f}", f"{item['total']:.2f}"),
                tags=(tag,)
            )

        # คำนวณยอดผ่าน Logic
        totals = pos_logic.calculate_totals(raw_total)
        lbl_subtotal_var.set(f"{totals['subtotal']:,.2f} บาท")
        lbl_discount_var.set(f"-{totals['discount']:,.2f} บาท")
        lbl_vat_var.set(f"+{totals['vat']:,.2f} บาท")
        lbl_grand_total_var.set(f"{totals['grand_total']:,.2f} บาท")

    # --- Popup เปิด Numpad สำหรับกรอกเบอร์โทรศัพท์ ---
    def open_phone_numpad(parent_win, entry_widget):
        """เปิด Numpad เพื่อกรอกเบอร์โทรศัพท์ลงใน Entry Widget"""
        def on_submit(val):
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, val)
        show_shared_numpad(parent_win, "แป้นตัวเลข", entry_widget.get(), on_submit)

    # --- Popup สมัครสมาชิก ---
    def popup_register():
        """เปิดหน้าต่างกรอกข้อมูลเพื่อสมัครสมาชิกใหม่"""
        reg_pop = ctk.CTkToplevel(parent)
        reg_pop.title("ลงทะเบียนสมาชิกใหม่")
        reg_pop.geometry("400x350+700+300")
        reg_pop.grab_set()

        ctk.CTkLabel(reg_pop, text="เบอร์โทรศัพท์", font=("Kanit", 30, "bold"), text_color="#1e683e").pack(pady=5)
        ent_phone = ctk.CTkEntry(reg_pop)
        ent_phone.pack(fill="both", padx=30)
        ent_phone.bind("<Button-1>", lambda e: open_phone_numpad(reg_pop, ent_phone))

        ctk.CTkLabel(reg_pop, text="ชื่อ", font=("Kanit", 30, "bold"), text_color="#1e683e").pack(pady=5)
        ent_fname = ctk.CTkEntry(reg_pop)
        ent_fname.pack(fill="both", padx=30)

        ctk.CTkLabel(reg_pop, text="นามสกุล", font=("Kanit", 30, "bold"), text_color="#1e683e").pack(pady=5)
        ent_lname = ctk.CTkEntry(reg_pop)
        ent_lname.pack(fill="both", padx=30)

        def do_register():
            """ดึงค่าจาก Entry และส่งให้ pos_logic ลงทะเบียนสมาชิก"""
            phone = ent_phone.get().strip()
            fname = ent_fname.get().strip()
            lname = ent_lname.get().strip()

            if not phone or not fname or not lname:
                messagebox.showwarning("แจ้งเตือน", "กรุณากรอกข้อมูลให้ครบทุกช่อง", parent=reg_pop)
                return

            success, msg = pos_logic.do_register_member(phone, fname, lname)
            if success:
                messagebox.showinfo("สำเร็จ", msg, parent=reg_pop)
                reg_pop.destroy()
            else:
                messagebox.showwarning("แจ้งเตือน", msg, parent=reg_pop)

        ctk.CTkButton(
            reg_pop, text="ยืนยันสมาชิก",
            font=("Kanit", 20, "bold"),
            command=do_register,
            fg_color="#1e683e", hover_color="#003315", text_color="white"
        ).pack(pady=15)

    # --- Popup เข้าสู่ระบบสมาชิก ---
    def popup_login():
        """เปิดหน้าต่างกรอกเบอร์โทรศัพท์เพื่อ Login สมาชิก"""
        log_pop = ctk.CTkToplevel(parent)
        log_pop.title("เข้าสู่ระบบสมาชิก")
        log_pop.geometry("400x350+700+300")
        log_pop.grab_set()

        ctk.CTkLabel(log_pop, text="ใส่เบอร์โทรศัพท์", font=("Kanit", 30, "bold"), text_color="#1e683e").pack(pady=10)
        ent_phone = ctk.CTkEntry(log_pop)
        ent_phone.pack(fill="both", padx=30)
        ent_phone.bind("<Button-1>", lambda e: open_phone_numpad(log_pop, ent_phone))

        def do_login():
            """ตรวจสอบสมาชิกจาก pos_logic และอัปเดต Label แสดงสถานะ"""
            mem = pos_logic.do_login_member(ent_phone.get())
            if mem:
                pos_logic.save_member_to_state(mem)
                lbl_member_status_var.set(f"สมาชิก | {mem['first_name']} {mem['last_name']}")
                messagebox.showinfo("สำเร็จ", "ลงชื่อเข้าใช้สมาชิกสำเร็จ ได้รับส่วนลด 25%", parent=log_pop)
                log_pop.destroy()
                reload_cart()  # คำนวณเงินใหม่เพราะได้ส่วนลด
            else:
                messagebox.showerror("ไม่พบข้อมูล", "ไม่พบเบอร์โทรศัพท์นี้ในระบบ", parent=log_pop)

        ctk.CTkButton(
            log_pop, text="ตรวจสอบ",
            font=("Kanit", 20, "bold"),
            command=do_login,
            fg_color="#1e683e", hover_color="#003315", text_color="white"
        ).pack(pady=15)

    # --- ปุ่มสมัครและเข้าสู่ระบบ ---
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

    # --- ปุ่มออกจากระบบสมาชิก ---
    def logout_member():
        """ล้างข้อมูลสมาชิกจาก Global State และ reload ตะกร้า"""
        pos_logic.logout_member_state()
        lbl_member_status_var.set("ลูกค้าทั่วไป")
        reload_cart()

    ctk.CTkButton(
        frame3, text="ออกจากระบบสมาชิก",
        font=("Kanit", 18), command=logout_member,
        text_color="#FFFFFF", fg_color="#1e683e", hover_color="#003a17"
    ).pack(fill=tk.X, padx=(10, 10), pady=2)

    # ======================= ส่วนสรุปยอด =======================
    ctk.CTkLabel(
        frame3, text="สรุปยอดชำระ",
        font=("Kanit", 25, "bold"), text_color="#1e683e"
    ).pack(fill=tk.X, padx=(10, 10), pady=(20, 0))

    summary_frame = ctk.CTkFrame(
        frame3, fg_color="white",
        border_width=5, border_color="#1e683e", corner_radius=10
    )
    summary_frame.pack(fill=tk.X, padx=10, pady=5)

    # ตัวแปรแสดงผลยอดต่างๆ
    lbl_subtotal_var  = ctk.StringVar(value="0.00 บาท")
    lbl_discount_var  = ctk.StringVar(value="0.00 บาท")
    lbl_vat_var       = ctk.StringVar(value="0.00 บาท")
    lbl_grand_total_var = ctk.StringVar(value="0.00 บาท")

    ctk.CTkLabel(summary_frame, text="ราคารวม", font=("Kanit", 20)).grid(row=0, column=0, sticky="w", padx=(20, 0), pady=10)
    ctk.CTkLabel(summary_frame, textvariable=lbl_subtotal_var, font=("Kanit", 20)).grid(row=0, column=1, sticky="e", padx=(0, 20), pady=10)

    ctk.CTkLabel(summary_frame, text="ส่วนลดสมาชิก:", font=("Kanit", 20), text_color="red").grid(row=1, column=0, sticky="w", padx=(20, 0), pady=10)
    ctk.CTkLabel(summary_frame, textvariable=lbl_discount_var, font=("Kanit", 20), text_color="red").grid(row=1, column=1, sticky="e", padx=(0, 20), pady=10)

    ctk.CTkLabel(summary_frame, text="VAT 7%:", font=("Kanit", 20), text_color="orange").grid(row=2, column=0, sticky="w", padx=(20, 0), pady=10)
    ctk.CTkLabel(summary_frame, textvariable=lbl_vat_var, font=("Kanit", 20), text_color="#f98404").grid(row=2, column=1, sticky="e", padx=(0, 20), pady=10)

    ctk.CTkLabel(summary_frame, text="ราคาสุทธิ", font=("Kanit", 30, "bold"), text_color="green").grid(row=3, column=0, sticky="w", padx=(20, 0), pady=(40, 10))
    ctk.CTkLabel(summary_frame, textvariable=lbl_grand_total_var, font=("Kanit", 30, "bold"), text_color="green").grid(row=3, column=1, sticky="e", padx=(0, 20), pady=(40, 10))
    summary_frame.columnconfigure(1, weight=1)

    # เชื่อมต่อ search กับ reload ปุ่มสินค้า และ โหลดครั้งแรก
    search_var.trace_add("write", lambda *args: load_products_to_frame(frame1, reload_cart, search_var.get()))
    load_products_to_frame(frame1, reload_cart)
    reload_cart()

    # ======================= ส่วนปุ่มดำเนินการ =======================
    action_frame = ctk.CTkFrame(frame3, fg_color="transparent")
    action_frame.pack(fill=tk.X, padx=(10, 10), pady=(20, 0))

    # --- ล้างตะกร้า ---
    def clear_cart():
        """ถามยืนยันแล้วเคลียร์บิลทั้งหมดผ่าน pos_logic"""
        bill_path = pos_logic.get_bill_path()
        if not os.path.exists(bill_path):
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return
        with open(bill_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return
        confirm = messagebox.askyesno("ยืนยัน", "คุณแน่ใจหรือไม่ที่จะล้างตะกร้าทั้งหมด?")
        if confirm:
            pos_logic.clear_bill_file()
            reload_cart()
            messagebox.showinfo("สำเร็จ", "เคลียร์ตะกร้าเรียบร้อยแล้ว")

    # --- พักบิล ---
    def hold_bill_action():
        """ย้ายบิลปัจจุบันไปพัก โดยเรียก pos_logic.hold_bill()"""
        success, msg = pos_logic.hold_bill()
        if success:
            reload_cart()
            messagebox.showinfo("สำเร็จ", msg)
        else:
            messagebox.showinfo("แจ้งเตือน", msg)

    # --- เรียกคืนบิล ---
    def recall_bill_action():
        """เปิด Popup แสดงรายการบิลที่พักไว้ ให้ผู้ใช้เลือกเรียกคืน"""
        files = pos_logic.get_held_bill_files()
        if not files:
            messagebox.showinfo("แจ้งเตือน", "ไม่มีบิลที่ถูกพักไว้")
            return

        recall_pop = ctk.CTkToplevel(parent)
        recall_pop.title("เลือกบิลที่ต้องการเรียกคืน")
        recall_pop.geometry("300x300")
        recall_pop.grab_set()

        ctk.CTkLabel(recall_pop, text="รายการพักบิลทั้งหมด:", font=("Kanit", 10, "bold")).pack(pady=5)

        listbox = tk.Listbox(recall_pop, font=("Kanit", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for f in files:
            # ตัดคำว่า bill_ และ .txt ออกให้เหลือแต่วันเวลา
            display_name = f.replace("bill_", "").replace(".txt", "")
            listbox.insert(tk.END, display_name)

        def do_recall():
            """เรียกคืนบิลที่เลือกแล้ว reload ตะกร้า"""
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกบิล!", parent=recall_pop)
                return
            selected_file = files[selected[0]]
            success, msg = pos_logic.recall_bill(selected_file)
            if success:
                messagebox.showinfo("สำเร็จ", msg, parent=recall_pop)
                reload_cart()
                recall_pop.destroy()

        ctk.CTkButton(recall_pop, text="เรียกคืนบิลนี้", command=do_recall, fg_color="lightblue").pack(pady=10)

    ctk.CTkButton(action_frame, text="พักบิล", font=("Kanit", 25, "bold"),
                  command=hold_bill_action, fg_color="orange", hover_color="#9b5c00"
                  ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 5))
    ctk.CTkButton(action_frame, text="เรียกคืนบิล", font=("Kanit", 25, "bold"),
                  command=recall_bill_action, fg_color="#006b70", hover_color="#003a3a"
                  ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(5, 5))
    ctk.CTkButton(action_frame, text="ล้างตะกร้า", font=("Kanit", 25, "bold"),
                  command=clear_cart, fg_color="red", text_color="white", hover_color="#8e0000"
                  ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(5, 0))

    # --- ยืนยันชำระเงิน ---
    def confirm_checkout():
        """
        เรียก pos_logic.process_checkout() เพื่อดำเนินการชำระเงิน
        ถ้าสำเร็จ: เล่นเสียง, logout สมาชิก, reload ตะกร้า
        ถ้าไม่สำเร็จ: แสดงข้อความ error และ reload ตะกร้า
        """
        success, msg, _pdf = pos_logic.process_checkout()

        if success:
            logout_member()  # รับเงินเสร็จ เตะสมาชิกออกรอคิวต่อไป
            try:
                playsound("sound/cat.mp3", block=False)
                playsound("sound/money_pickup.mp3", block=False)
            except Exception:
                print("เล่นเสียงไม่ได้")
        else:
            messagebox.showwarning("ข้อผิดพลาด", msg)
            reload_cart()

    # --- ปุ่มแมวยืนยันรายการ ---
    cat_img_normal = ctk.CTkImage(light_image=Image.open("img/cat_normal.png"), size=(500, 150))
    cat_img_hover  = ctk.CTkImage(light_image=Image.open("img/cat_hover.png"),  size=(500, 150))

    btn_cat = ctk.CTkButton(
        frame3, text="",
        image=cat_img_normal,
        fg_color="transparent",
        hover_color="#FFFFFF",
        command=confirm_checkout
    )
    btn_cat.pack(pady=(20, 0))

    def on_enter(event):
        """เปลี่ยนรูปแมวตอน Mouse Hover"""
        btn_cat.configure(image=cat_img_hover)

    def on_leave(event):
        """กลับรูปแมวปกติตอน Mouse Leave"""
        btn_cat.configure(image=cat_img_normal)

    btn_cat.bind("<Enter>", on_enter)
    btn_cat.bind("<Leave>", on_leave)

    ctk.CTkLabel(
        frame3, text="ขอบคุณที่อุดหนุนนะ เมี๊ยววว!!",
        font=("Kanit", 40, "bold"), text_color="#1e683e"
    ).pack(pady=(30, 0))

    # ส่งเฟรมทั้ง 3 กลับเพื่อให้ผู้เรียกใช้งานต่อได้
    return frame1, frame2, frame3