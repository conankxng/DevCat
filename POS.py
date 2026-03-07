import tkinter as tk
from tkinter import ttk, messagebox
import os
import product_manager
import member_manager
import sales_logger
from datetime import datetime
from PIL import Image, ImageTk
from playsound import playsound 
import customtkinter as ctk

# ========================================================================= #
# ส่วนที่ 1.5: แป้นกดตัวเลข (Numpad) ที่ใช้ร่วมกัน
# ========================================================================= #
def show_shared_numpad(parent_win, title, initial_value, callback):
    popup = ctk.CTkToplevel(parent_win)
    popup.title(title)
    popup.geometry("300x500")
    popup.grab_set()
    popup.transient(parent_win)
    popup.focus_force()
    
    qty_var = ctk.StringVar(value=initial_value)
    
    display = ctk.CTkLabel(popup, textvariable=qty_var, font=("Kanit", 28, "bold"), fg_color="white", anchor="e")
    display.pack(fill=tk.X, padx=10, pady=(10, 10))
    
    keypad_frame = ctk.CTkFrame(popup)
    keypad_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
    
    for i in range(3): keypad_frame.columnconfigure(i, weight=1)
    for i in range(4): keypad_frame.rowconfigure(i, weight=1)
        
    def btn_press(key):
        current = qty_var.get()
        if key == "C":
            qty_var.set("")
        elif key == "<-":
            qty_var.set(current[:-1])
        else:
            qty_var.set(current + key)

    def create_btn_command(k):
        return lambda: btn_press(k)
        
    buttons = [
        ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
        ('C', 3, 0), ('0', 3, 1), ('<-', 3, 2),
    ]
    
    for (text, row, col) in buttons:
        btn = ctk.CTkButton(keypad_frame, text=text, font=("Kanit", 18, "bold"), command=create_btn_command(text))
        btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
    def submit():
        val = qty_var.get()
        popup.destroy()
        callback(val)
        
    ctk.CTkButton(popup, text="ยืนยัน", command=submit, font=("Kanit", 16, "bold"), fg_color="green", text_color="white").pack(fill=tk.X, padx=10, pady=10)


# ========================================================================= #
# ส่วนที่ 2: ฟังก์ชันหลักของหน้าจอ POS
# ========================================================================= #
# ตัวแปรวงกว้าง (Global) สำหรับจำสเตตัสสินค้าที่คลิกล่าสุด
current_selected_product = {"id": None, "name": None}
# ตัวแปรจำสถานะสมาชิกปัจจุบัน
current_member_info = {"phone": None, "first_name": None, "last_name": None}

def create_three_frames(parent, bg_img1=None, bg_img2=None, bg_img3=None):
    """
    ฟังก์ชันสำหรับแบ่งหน้าจอ POS ออกเป็น 3 ส่วนหลัก (ซ้าย: สินค้า, กลาง: ตะกร้า, ขวา: ดำเนินการ)
    """
    def add_background_image(widget, image_path):
        if not image_path or not os.path.exists(image_path):
            return
        try:
            original_img = Image.open(image_path)
        except Exception:
            return
            
        bg_label = ctk.CTkLabel(widget)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()
        
        widget._bg_size = (0, 0)
        
        def on_resize(event):
            if event.widget == widget:
                w, h = event.width, event.height
                if w < 10 or h < 10: return
                if abs(w - widget._bg_size[0]) > 5 or abs(h - widget._bg_size[1]) > 5:
                    widget._bg_size = (w, h)
                    resized = original_img.resize((w, h), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(resized)
                    bg_label.config(image=photo)
                    bg_label.image = photo
                    
        widget.bind("<Configure>", on_resize, add='+')

# ---------------------------------------------------------
    # เฟรมที่ 1: ค้นหาและรายการสินค้า (เลื่อนได้)
    # ---------------------------------------------------------
    left_panel = ctk.CTkFrame(parent, fg_color="transparent")
    left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # --- 2. ส่วนค้นหา (ทำให้โปร่งใสด้วย) ---
    search_frame = ctk.CTkFrame(left_panel, fg_color="transparent") # ตั้งเป็น transparent
    search_frame.pack(fill=tk.X, pady=5)
    
    ctk.CTkLabel(search_frame, text="ค้นหาสินค้า", font=("Kanit", 12, "bold")).pack(side=tk.LEFT)
    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, font=("Kanit", 12))
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    ctk.CTkButton(search_frame, text="X", font=("Kanit", 10, "bold"), fg_color="red", text_color="white", width=3, command=lambda: search_var.set("")).pack(side=tk.RIGHT)
    
    # --- 3. ส่วนรายการสินค้า (Scrollable) ---
    frame1 = ctk.CTkScrollableFrame(left_panel)
    frame1.pack(fill=tk.BOTH, expand=True)

    # --- 4. บังคับลำดับแกน Z ---
    # img1.lower() # ส่งรูปภาพไปอยู่ชั้นล่างสุดของ left_panel


    
    # ---------------------------------------------------------
    # เฟรมที่ 2: ตะกร้าสินค้า (แสดงผลเป็นตาราง)
    # ---------------------------------------------------------
    frame2 = ctk.CTkFrame(parent)
    frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    add_background_image(frame2, bg_img2)
    
    # ป้ายหัวข้อตะกร้าสินค้า
    ctk.CTkLabel(frame2, text="รายการสินค้า", font=("Kanit", 12, "bold")).pack(pady=10)
    
    # กรอบสำหรับตารางและแถบเลื่อน
    tree_frame = ctk.CTkFrame(frame2)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # แถบเลื่อน (Scrollbar) ของตาราง
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    # การตั้งค่าตาราง (Treeview) เพื่อแสดงรายการสินค้าที่เลือก
    columns = ("id", "name", "price", "total")
    cart_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15, yscrollcommand=tree_scroll.set, selectmode="browse")
    tree_scroll.config(command=cart_tree.yview)
    
    #ปรับแต่งตารางให้สวยงาม (Modern Look)
    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure("Treeview", 
                    background="white",
                    foreground="#333333",
                    rowheight=35,
                    fieldbackground="white",
                    font=("Kanit", 11),
                    borderwidth=0)
                    
    style.configure("Treeview.Heading", 
                    font=("Kanit", 12, "bold"), 
                    background="#F8F9FA", 
                    foreground="#495057",
                    borderwidth=0,
                    relief="flat")
                    
    style.map('Treeview', background=[('selected', '#E3F2FD')], foreground=[('selected', '#000000')])
    style.map('Treeview.Heading', background=[('active', '#E9ECEF')])
    
    # กำหนดหัวข้อคอลัมน์ของตาราง
    cart_tree.heading("id", text="รหัสสินค้า")
    cart_tree.heading("name", text="สินค้า")
    cart_tree.heading("price", text="ราคา/หน่วย")
    cart_tree.heading("total", text="ราคารวม")
    
    # กำหนดขนาดและการจัดตำแหน่งของแต่ละคอลัมน์
    cart_tree.column("id", width=80, anchor="center")
    cart_tree.column("name", width=150, anchor="center")
    cart_tree.column("price", width=80, anchor="center")
    cart_tree.column("total", width=80, anchor="center")
    
    # วางตารางลงบนจอ
    cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # ที่อยู่ของไฟล์บิลสินค้าเก็บพักไว้
    bill_path = os.path.join(os.path.dirname(__file__), "data", "bill.txt")
    
    # สร้าง Frame 3 ก่อนเพื่อให้ reload_cart เรียกใช้ Label ได้
    frame3 = ctk.CTkFrame(parent)
    frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    add_background_image(frame3, bg_img3)
    
    # ========================== ส่วนที่ 3 บน: สมาชิก ==========================
    member_frame = ctk.CTkFrame(frame3, border_width=2)
    member_frame.pack(fill=tk.X, pady=5)
    
    lbl_member_status_var = ctk.StringVar(value="ลูกค้าทั่วไป")
    ctk.CTkLabel(member_frame, textvariable=lbl_member_status_var, font=("Kanit", 11, "bold"), text_color="blue").pack(pady=5)
    
    
    def open_phone_numpad(parent_win, entry_widget):
        def on_submit(val):
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, val)
        show_shared_numpad(parent_win, "แป้นตัวเลข", entry_widget.get(), on_submit)
    
    
    
    def popup_register():
        reg_pop = ctk.CTkToplevel(parent)
        reg_pop.title("ลงทะเบียนสมาชิกใหม่")
        reg_pop.geometry("300x250")
        reg_pop.grab_set()
        
        ctk.CTkLabel(reg_pop, text="เบอร์โทรศัพท์:").pack(pady=5)
        ent_phone = ctk.CTkEntry(reg_pop)
        ent_phone.pack()
        ent_phone.bind("<Button-1>", lambda e: open_phone_numpad(reg_pop, ent_phone))
        
        ctk.CTkLabel(reg_pop, text="ชื่อ:").pack(pady=5)
        ent_fname = ctk.CTkEntry(reg_pop)
        ent_fname.pack()
        
        ctk.CTkLabel(reg_pop, text="นามสกุล:").pack(pady=5)
        ent_lname = ctk.CTkEntry(reg_pop)
        ent_lname.pack()
        
        def do_register():
            success, msg = member_manager.register_member(ent_phone.get(), ent_fname.get(), ent_lname.get())
            if success:
                messagebox.showinfo("สำเร็จ", msg, parent=reg_pop)
                reg_pop.destroy()
            else:
                messagebox.showwarning("แจ้งเตือน", msg, parent=reg_pop)
                
        ctk.CTkButton(reg_pop, text="ยืนยันสมาชิก", command=do_register, fg_color="green", text_color="white").pack(pady=15)

    def popup_login():
        log_pop = ctk.CTkToplevel(parent)
        log_pop.title("เข้าสู่ระบบสมาชิก")
        log_pop.geometry("250x150")
        log_pop.grab_set()
        
        ctk.CTkLabel(log_pop, text="ใส่เบอร์โทรศัพท์").pack(pady=10)
        ent_phone = ctk.CTkEntry(log_pop)
        ent_phone.pack()
        ent_phone.bind("<Button-1>", lambda e: open_phone_numpad(log_pop, ent_phone))
        
        def do_login():
            global current_member_info
            mem = member_manager.get_member(ent_phone.get())
            if mem:
                current_member_info["phone"] = mem["phone"]
                current_member_info["first_name"] = mem["first_name"]
                current_member_info["last_name"] = mem["last_name"]
                lbl_member_status_var.set(f"สมาชิก | {mem['first_name']} {mem['last_name']}")
                messagebox.showinfo("สำเร็จ", "ลงชื่อเข้าใช้สมาชิกสำเร็จ ได้รับส่วนลด 25%", parent=log_pop)
                log_pop.destroy()
                reload_cart() # คำนวณเงินใหม่เพราะได้ส่วนลด
            else:
                messagebox.showerror("ไม่พบข้อมูล", "ไม่พบเบอร์โทรศัพท์นี้ในระบบ", parent=log_pop)
                
        ctk.CTkButton(log_pop, text="ตรวจสอบ", command=do_login, fg_color="blue", text_color="white").pack(pady=10)

    btn_frame = ctk.CTkFrame(frame3)
    btn_frame.pack(fill=tk.X, pady=5)
    ctk.CTkButton(btn_frame, text="สมัครสมาชิก", font=("Kanit", 12), command=popup_register).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
    ctk.CTkButton(btn_frame, text="เข้าสู่ระบบ", font=("Kanit", 12), command=popup_login).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
    
    def logout_member():
        global current_member_info
        current_member_info = {"phone": None, "first_name": None, "last_name": None}
        lbl_member_status_var.set("ลูกค้าทั่วไป")
        reload_cart()
    ctk.CTkButton(frame3, text="ออกจากระบบสมาชิก", font=("Kanit", 12), command=logout_member, text_color="red").pack(fill=tk.X, pady=2)


    # ========================== ส่วนที่ 3 กลาง: สรุปยอด ==========================
    ctk.CTkLabel(frame3, text="สรุปยอดชำระ", fg_color="lightcoral", font=("Kanit", 12, "bold")).pack(fill=tk.X, pady=10)
    
    summary_frame = ctk.CTkFrame(frame3)
    summary_frame.pack(fill=tk.X, padx=10, pady=5)
    
    lbl_subtotal_var = ctk.StringVar(value="0.00 บาท")
    lbl_discount_var = ctk.StringVar(value="0.00 บาท")
    lbl_vat_var = ctk.StringVar(value="0.00 บาท")
    lbl_grand_total_var = ctk.StringVar(value="0.00 บาท")
    
    ctk.CTkLabel(summary_frame, text="ราคารวม:", font=("Kanit", 10)).grid(row=0, column=0, sticky="w", pady=2)
    ctk.CTkLabel(summary_frame, textvariable=lbl_subtotal_var, font=("Kanit", 10)).grid(row=0, column=1, sticky="e", pady=2)
    
    ctk.CTkLabel(summary_frame, text="ส่วนลดสมาชิก:", font=("Kanit", 10), text_color="red").grid(row=1, column=0, sticky="w", pady=2)
    ctk.CTkLabel(summary_frame, textvariable=lbl_discount_var, font=("Kanit", 10), text_color="red").grid(row=1, column=1, sticky="e", pady=2)
    
    ctk.CTkLabel(summary_frame, text="VAT 7%:", font=("Kanit", 10)).grid(row=2, column=0, sticky="w", pady=2)
    ctk.CTkLabel(summary_frame, textvariable=lbl_vat_var, font=("Kanit", 10)).grid(row=2, column=1, sticky="e", pady=2)
    
    ctk.CTkLabel(summary_frame, text="ราคาสุทธิ:", font=("Kanit", 14, "bold"), text_color="green").grid(row=3, column=0, sticky="w", pady=10)
    ctk.CTkLabel(summary_frame, textvariable=lbl_grand_total_var, font=("Kanit", 14, "bold"), text_color="green").grid(row=3, column=1, sticky="e", pady=10)
    summary_frame.columnconfigure(1, weight=1)
    
    
    def reload_cart():
        """ฟังก์ชันสำหรับเคลียร์ตารางอ่านบิลใหม่ และคำนวณเงิน"""
        for row in cart_tree.get_children():
            cart_tree.delete(row)
            
        # ใส่ tag เพื่อสลับสีแถว (Zebra striping)
        cart_tree.tag_configure('evenrow', background='#FFFFFF')
        cart_tree.tag_configure('oddrow', background='#F8F9FA')
            
        total_sum = 0.0
        if os.path.exists(bill_path):
            with open(bill_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for idx, line in enumerate(lines):
                parts = line.strip().split(",")
                if len(parts) == 5:
                    pid, name, price, qty, total = parts
                    total_sum += float(total)
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                    cart_tree.insert("", tk.END, values=(pid, f"{name} (x{qty})", price, total), tags=(tag,))

        discount = 0.0
        if current_member_info["phone"] is not None:
            discount = total_sum * 0.25 # ลด 25%
            
        after_discount = total_sum - discount
        vat = after_discount * 0.07 # ภาษี 7%
        grand_total = after_discount + vat
        
        lbl_subtotal_var.set(f"{total_sum:,.2f} บาท")
        lbl_discount_var.set(f"-{discount:,.2f} บาท")
        lbl_vat_var.set(f"+{vat:,.2f} บาท")
        lbl_grand_total_var.set(f"{grand_total:,.2f} บาท")

    # โหลดตะกร้าครั้งแรก
    search_var.trace_add("write", lambda *args: load_products_to_frame(frame1, reload_cart, search_var.get()))
    load_products_to_frame(frame1, reload_cart)
    reload_cart()
    
    # ========================== ส่วนที่ 3 ล่าง: ดำเนินการ ==========================
    action_frame = ctk.CTkFrame(frame3)
    # ลบ expand=True ทิ้งเพื่อป้องกันไม่ให้ปุ่มข้างล่างโดนดันตกขอบจอ
    action_frame.pack(fill=tk.X, pady=10)
    
    def clear_cart():
        if os.path.exists(bill_path):
            with open(bill_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if not lines:
                messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
                return
                
            confirm = messagebox.askyesno("ยืนยัน", "คุณแน่ใจหรือไม่ที่จะล้างตะกร้าทั้งหมด?")
            if confirm:
                open(bill_path, "w").close()
                reload_cart()
                messagebox.showinfo("สำเร็จ", "เคลียร์ตะกร้าเรียบร้อยแล้ว")
    
    def hold_bill():
        if not os.path.exists(bill_path):
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return
            
        with open(bill_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        if not lines:
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return
            
        hold_dir = os.path.join(os.path.dirname(__file__), "data", "hold_bills")
        os.makedirs(hold_dir, exist_ok=True)
        
        # ตั้งชื่อไฟล์เป็น วัน-เดือน-ปี_ชั่วโมง-นาที-วินาที
        timestamp = datetime.now().strftime("%d-%m-%Y  %H-%M")
        hold_file = os.path.join(hold_dir, f"bill_{timestamp}.txt")
        
        # ย้ายข้อมูลไปไฟล์พักบิลและล้างของเดิม
        with open(hold_file, "w", encoding="utf-8") as f:
            f.writelines(lines)
        open(bill_path, "w").close()
        reload_cart()
        messagebox.showinfo("สำเร็จ", f"พักบิลไว้เรียบร้อย\n{timestamp}")

    def recall_bill():
        hold_dir = os.path.join(os.path.dirname(__file__), "data", "hold_bills")
        os.makedirs(hold_dir, exist_ok=True)
        
        files = [f for f in os.listdir(hold_dir) if f.endswith(".txt")]
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
            # ตัดคำว่า bill_ และ .txt ออกให้เหลือแต่วันเวลาเพื่อความสวยงาม
            display_name = f.replace("bill_", "").replace(".txt", "")
            listbox.insert(tk.END, display_name)
            
        def do_recall():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกบิล!", parent=recall_pop)
                return
                
            selected_file = files[selected[0]]
            hold_path = os.path.join(hold_dir, selected_file)
            
            # อ่านข้อมูลที่พักไว้มาใส่ท้าย bill.txt ปัจจุบัน
            with open(hold_path, "r", encoding="utf-8") as hf:
                hold_lines = hf.readlines()
                
            with open(bill_path, "a", encoding="utf-8") as bf:
                bf.writelines(hold_lines)
                
            # ลบไฟล์ที่พักทิ้ง
            os.remove(hold_path)
            
            messagebox.showinfo("สำเร็จ", "เรียกบิลเรียบร้อยแล้ว เพิ่มสินค้าลงตะกร้าแล้ว", parent=recall_pop)
            reload_cart()
            recall_pop.destroy()
            
        ctk.CTkButton(recall_pop, text="เรียกคืนบิลนี้", command=do_recall, fg_color="lightblue").pack(pady=10)
        
    ctk.CTkButton(action_frame, text="พักบิล", font=("Kanit", 12, "bold"), command=hold_bill, fg_color="orange").pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)
    ctk.CTkButton(action_frame, text="เรียกคืนบิล", font=("Kanit", 12, "bold"), command=recall_bill, fg_color="lightblue").pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)
    ctk.CTkButton(action_frame, text="ล้างตะกร้า", font=("Kanit", 12, "bold"), command=clear_cart, fg_color="red", text_color="white").pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)

    def confirm_checkout():
        """ยืนยันการทำรายการแบบเต็มรูปแบบ"""
        if not os.path.exists(bill_path):
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return
            
        with open(bill_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        if not lines:
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return
            
        all_success = True
        error_msgs = []
        
        # บันทึก items สำหรับใบเสร็จ
        receipt_items = []
        total_sum = 0.0
        
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 5:
                pid, name, price, qty, total = parts
                success, msg = product_manager.process_sale(pid, int(qty))
                if not success:
                    all_success = False
                    error_msgs.append(f"{name}: {msg}")
                else:
                    product_manager.record_sale(pid, int(qty), float(total))
                    receipt_items.append({
                        "name": name,
                        "qty": int(qty),
                        "price": float(price),
                        "total": float(total)
                    })
                    total_sum += float(total)
                    
        if all_success:
            # คำนวณสรุปยอดแบบเดียวกับตอน reload_cart
            discount = 0.0
            if current_member_info["phone"] is not None:
                discount = total_sum * 0.25
            after_discount = total_sum - discount
            vat = after_discount * 0.07
            grand_total = after_discount + vat
            
            # บันทึกลง Master Sales และปริ้น PDF
            try:
                pdf_file = sales_logger.record_sale(
                    items=receipt_items, 
                    subtotal=total_sum, 
                    discount=discount, 
                    vat=vat, 
                    grand_total=grand_total, 
                    member_info=current_member_info
                )

            except Exception as e:
                pass

                

            open(bill_path, 'w').close() 
            logout_member() # รับเงินเสร็จ เตะสมาชิกออกรอคิวต่อไป
        else:
            errors = "\n".join(error_msgs)
            messagebox.showwarning("ข้อผิดพลาด", f"สต๊อกไม่พอ:\n{errors}\n*ระบบเคลียร์ตะกร้าแล้ว")
            open(bill_path, 'w').close()
            reload_cart()
        try:
            # เล่นเสียง (ใส่ Path ไฟล์เสียงของคุณ)
            # block=False เพื่อให้เสียงเล่นไปโดยไม่ทำให้หน้าจอโปรแกรมค้าง
            playsound("sound/cat.mp3", block=False)
        except Exception as e:
            print(f"เล่นเสียงไม่ได้")
                
    try:
        img = Image.open("img/cat_btn.png")
        cat_button_img = ctk.CTkImage(img, size=(170, 130))
    except:
        cat_button_img = None
        print("ไม่พบรูปภาพ")         

    # ปุ่มยืนยันรายการจ่ายเงิน (แพ็คให้ติดขอบล่างเสมอ ป้องกันการโดนดันตกจอ)
    btn_cat = ctk.CTkButton(
        frame3, 
        text="",
        image=cat_button_img if "cat_button_img" in locals() else None,
        hover_color="#f0f2f5",
        fg_color="transparent",
        command=confirm_checkout
    )
        
    btn_cat.pack()
    
    # ส่งเฟรมทั้ง 3 กลับเป็นก้อน
    return frame1, frame2, frame3


# ========================================================================= #
# ส่วนที่ 3: ฟังก์ชันโหลดปุ่มสินค้า
# ========================================================================= #
def load_products_to_frame(frame, reload_cart_cb=None, search_keyword=""):
    """
    ฟังก์ชันสำหรับอ่านไฟล์ products.txt และสร้างปุ่มสินค้ามาวางเรียงกันในเฟรมซ้ายสุด (และค้นหาได้)
    """
    # ล้างปุ่มเดิมออกก่อน (สำหรับตอนค้นหาและอัปเดต)
    for widget in frame.winfo_children():
        widget.destroy()

    file_path = os.path.join(os.path.dirname(__file__), "data", "products.txt")
    
    # สั่งให้จัดตารางเรียงน้ำหนัก 4 คอลัมน์ให้ขยายตัวเท่าๆ กัน
    for col_index in range(4):
        frame.columnconfigure(col_index, weight=1)
        
    try:
        # เปิดไฟล์สินค้าออกมาอ่าน
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        button_count = 0  # ตัวนับเพื่อคอยขึ้นคอลัมน์ใหม่เรื่อยๆ
        for line in lines:
            line = line.strip()
            if not line:
                continue # ข้ามบรรทัดว่าง
                
            # แยกข้อมูล เช่น "001,cake,0,50.0,35.0"
            parts = line.split(",")
            if len(parts) >= 2:
                product_id = parts[0]
                product_name = parts[1]
                
                # กรองสินค้าจากคำค้นหา (หาได้ทั้งรหัสและชื่อ)
                kw = search_keyword.strip().lower()
                if kw and kw not in product_name.lower() and kw not in product_id.lower():
                    continue

                # ฟังก์ชันเมื่อปุ่มสินค้าถูกคลิก
                def on_product_click(p_id=product_id, p_name=product_name):
                    global current_selected_product
                    # เซฟไว้ว่ากดอันไหนไป
                    current_selected_product["id"] = p_id
                    current_selected_product["name"] = p_name
                    # เปิดหน้า Numpad กรอกจำนวน
                    open_numpad_popup(frame, reload_cart_cb)
                
                # สร้างปุ่มสำหรับสินค้านั้นๆ
                btn = ctk.CTkButton(
                    frame, 
                    text=product_name, 
                    font=("Kanit", 10),
                    height=8,
                    command=on_product_click
                )
                btn.place(relwidth=1, relheight=1)
                
                # คำนวณเลขตารางช่อง (เช่น ชิ้นที่ 5 -> แถว 1 คอลัมน์ 1)
                row = int(button_count / 4)
                col = button_count % 4
                
                # วางลงบนตารางแบบสมมาตร
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                button_count = button_count + 1
                
    except FileNotFoundError:
        ctk.CTkLabel(frame, text="⚠️ ไม่พบไฟล์ data/products.txt", text_color="red").grid(row=0, column=0, columnspan=4, pady=20)
        

# ========================================================================= #
# ส่วนที่ 4: หน้าต่างกรอกจำนวนสินค้า (Numpad)
# ========================================================================= #
def open_numpad_popup(parent, on_add_to_cart_cb=None):
    """
    ป๊อปอัปให้กดตัวเลข 0-9 เพื่อระบุจำนวนที่ต้องการ
    """
    def on_submit(val):
        try:
            qty_int = int(val or "0")
        except ValueError:
            qty_int = 0
            
        if qty_int <= 0:
            messagebox.showwarning("แจ้งเตือน", "กรุณาระบุจำนวนมากกว่า 0", parent=parent)
            return
            
        pid = current_selected_product["id"]
        if pid:
            # โหลดคลังขึ้นมาดูว่าของพอไหม
            inventory = product_manager.get_all_products()
            if pid not in inventory or inventory[pid]['stock'] < qty_int:
                messagebox.showwarning("ข้อผิดพลาด", "สินค้าในสต็อกไม่เพียงพอ!", parent=parent)
                return
                
            price = float(inventory[pid].get("price", 0.0))
            name = current_selected_product["name"]
            total_price = price * qty_int
            
            # บันทึกลงบิล
            bill_path = os.path.join(os.path.dirname(__file__), "data", "bill.txt")
            with open(bill_path, "a", encoding="utf-8") as f:
                f.write(f"{pid},{name},{price:.2f},{qty_int},{total_price:.2f}\n")
                
            messagebox.showinfo("สำเร็จ", "เพิ่มลงตะกร้าเรียบร้อยแล้ว", parent=parent)
            
            # เรียกรีโหลดตารางข้างนอก
            if on_add_to_cart_cb:
                on_add_to_cart_cb()
        else:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบข้อมูลรหัสสินค้าที่เลือก", parent=parent)

    show_shared_numpad(parent, "ระบุจำนวนสินค้า", "", on_submit)