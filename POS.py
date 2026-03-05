import tkinter as tk
from tkinter import ttk, messagebox
import os
import product_manager
import member_manager
import sales_logger
from datetime import datetime

# ========================================================================= #
# ส่วนที่ 1: ฟังก์ชันสำหรับสร้างกล่องแบบเลื่อนได้ (Scrollable Frame)
# ========================================================================= #
def create_scrollable_frame(parent):
    """
    ฟังก์ชันนี้ช่วยสร้าง Frame ที่สามารถใช้ลูกกลิ้งเมาส์เลื่อนขึ้นลงได้
    เหมาะสำหรับหน้าที่มีของเยอะจนล้นจอ เช่น ปุ่มสินค้า
    """
    # 1. สร้างกรอบนอกสุด (Container) เพื่อเป็นฐานหลัห
    container = tk.Frame(parent)
    
    # 2. สร้าง Canvas เพราะ Frame ปกติไม่รองรับการเลื่อน (Scroll)
    # เราจะเอาสิ่งต่างๆ ไปวาดแปะไว้บน Canvas แทน
    canvas = tk.Canvas(container, highlightthickness=0)
    
    # 3. สร้างแถบเลื่อน (Scrollbar) แนวตั้ง แล้วผูกมันเข้ากับมุมมองของ Canvas
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    
    # 4. สร้าง Frame ด้านใน (Inner Frame) เพื่อเอาไว้เก็บปุ่มสินค้าจริงๆ
    inner_frame = tk.Frame(canvas)
    
    # 5. ฟังก์ชันคอยอัปเดตขนาดพื้นที่ที่เลื่อนได้ (Scrollregion)
    # เพื่อให้รู้ว่าควรเลื่อนได้ยาวแค่ไหนเมื่อมีปุ่มเพิ่มเข้ามา
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    inner_frame.bind("<Configure>", configure_scroll_region)
    
    # 6. นำ Frame ด้านใน วางแปะลงไปบน Canvas ที่จุดมุมซ้ายบนสุด (0,0)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # 7. ทำให้ความกว้างของ Canvas ล็อคพอดีกับหน้าจอเสมอ
    def configure_canvas_width(event):
        canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
    canvas.bind("<Configure>", configure_canvas_width)
    
    # 8. ฟังก์ชันตรวจจับลูกกลิ้งเมาส์ เพื่อเลื่อนหน้าจอ
    def _on_mousewheel(event):
        # canvas.yview() คืนค่าตำแหน่งบนและล่างสุดมา (0.0 ถึง 1.0)
        top, bottom = canvas.yview()
        
        if event.delta > 0:       # หมุนลูกกลิ้งชี้ขึ้นด้านบน
            if top > 0.0:         # ถ้ายังไม่ถึงยอดสุด ให้เลื่อนขึ้น
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.delta < 0:     # หมุนลูกกลิ้งชี้ลงด้านล่าง
            if bottom < 1.0:      # ถ้ายังไม่ถึงขอบล่าง ให้เลื่อนลง
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    # 9. ผูกคำสั่งเลื่อนเมาส์เฉพาะเวลาเมาส์อยู่ในกรอบนี้เท่านั้น
    canvas.bind('<Enter>', lambda _: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind('<Leave>', lambda _: canvas.unbind_all("<MouseWheel>"))

    # 10. จัดเรียงให้ Canvas อยู่ทางซ้าย และแถบ Scrollbar แปะอยู่ทางขวาสุด
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # คืนค่า container (ไปจัดวางในเมนูหลัก) และ inner_frame (เอาไปใส่ปุ่มสินค้าข้างใน)
    return container, inner_frame


# ========================================================================= #
# ส่วนที่ 2: ฟังก์ชันหลักของหน้าจอ POS
# ========================================================================= #
# ตัวแปรวงกว้าง (Global) สำหรับจำสเตตัสสินค้าที่คลิกล่าสุด
current_selected_product = {"id": None, "name": None}
# ตัวแปรจำสถานะสมาชิกปัจจุบัน
current_member_info = {"phone": None, "first_name": None, "last_name": None}

def create_three_frames(parent):
    """
    ฟังก์ชันสำหรับแบ่งหน้าจอ POS ออกเป็น 3 ส่วนหลัก (ซ้าย: สินค้า, กลาง: ตะกร้า, ขวา: ดำเนินการ)
    """
    # ---------------------------------------------------------
    # เฟรมที่ 1: รายการสินค้า (เลื่อนได้)
    # ---------------------------------------------------------
    container1, frame1 = create_scrollable_frame(parent)
    container1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # ---------------------------------------------------------
    # เฟรมที่ 2: ตะกร้าสินค้า (แสดงผลเป็นตาราง)
    # ---------------------------------------------------------
    frame2 = tk.Frame(parent)
    frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # ป้ายหัวข้อตะกร้าสินค้า
    tk.Label(frame2, text="{ ตะกร้าสินค้า }", bg="lightgreen", font=("Arial", 12, "bold")).pack(pady=10)
    
    # กรอบสำหรับตารางและแถบเลื่อน
    tree_frame = tk.Frame(frame2)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # แถบเลื่อน (Scrollbar) ของตาราง
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    # การตั้งค่าตาราง (Treeview) เพื่อแสดงรายการสินค้าที่เลือก
    columns = ("id", "name", "price", "total")
    cart_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15, yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=cart_tree.yview)
    
    # กำหนดหัวข้อคอลัมน์ของตาราง
    cart_tree.heading("id", text="รหัสสินค้า")
    cart_tree.heading("name", text="ชื่อสินค้า")
    cart_tree.heading("price", text="ราคา/หน่วย")
    cart_tree.heading("total", text="ราคารวม")
    
    # กำหนดขนาดและการจัดตำแหน่งของแต่ละคอลัมน์
    cart_tree.column("id", width=80, anchor="center")
    cart_tree.column("name", width=150, anchor="w")
    cart_tree.column("price", width=80, anchor="e")
    cart_tree.column("total", width=80, anchor="e")
    
    # วางตารางลงบนจอ
    cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # ที่อยู่ของไฟล์บิลสินค้าเก็บพักไว้
    bill_path = os.path.join(os.path.dirname(__file__), "data", "bill.txt")
    
    # สร้าง Frame 3 ก่อนเพื่อให้ reload_cart เรียกใช้ Label ได้
    frame3 = tk.Frame(parent)
    frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # ========================== ส่วนที่ 3 บน: สมาชิก ==========================
    member_frame = tk.Frame(frame3, relief="groove", bd=2)
    member_frame.pack(fill=tk.X, pady=5)
    
    lbl_member_status_var = tk.StringVar(value="👤 ลูกค้าทั่วไป (ไม่มีส่วนลด)")
    tk.Label(member_frame, textvariable=lbl_member_status_var, font=("Arial", 11, "bold"), fg="blue").pack(pady=5)
    
    def popup_register():
        reg_pop = tk.Toplevel(parent)
        reg_pop.title("สมัครสมาชิกใหม่")
        reg_pop.geometry("300x250")
        reg_pop.grab_set()
        
        tk.Label(reg_pop, text="เบอร์โทรศัพท์:").pack(pady=5)
        ent_phone = tk.Entry(reg_pop)
        ent_phone.pack()
        
        tk.Label(reg_pop, text="ชื่อจริง:").pack(pady=5)
        ent_fname = tk.Entry(reg_pop)
        ent_fname.pack()
        
        tk.Label(reg_pop, text="นามสกุล:").pack(pady=5)
        ent_lname = tk.Entry(reg_pop)
        ent_lname.pack()
        
        def do_register():
            success, msg = member_manager.register_member(ent_phone.get(), ent_fname.get(), ent_lname.get())
            if success:
                messagebox.showinfo("สำเร็จ", msg, parent=reg_pop)
                reg_pop.destroy()
            else:
                messagebox.showwarning("แจ้งเตือน", msg, parent=reg_pop)
                
        tk.Button(reg_pop, text="ยืนยันสมัครสมาชิก", command=do_register, bg="green", fg="white").pack(pady=15)

    def popup_login():
        log_pop = tk.Toplevel(parent)
        log_pop.title("เข้าสู่ระบบสมาชิก")
        log_pop.geometry("250x150")
        log_pop.grab_set()
        
        tk.Label(log_pop, text="กรอกเบอร์โทรศัพท์:").pack(pady=10)
        ent_phone = tk.Entry(log_pop)
        ent_phone.pack()
        
        def do_login():
            global current_member_info
            mem = member_manager.get_member(ent_phone.get())
            if mem:
                current_member_info["phone"] = mem["phone"]
                current_member_info["first_name"] = mem["first_name"]
                current_member_info["last_name"] = mem["last_name"]
                lbl_member_status_var.set(f"🌟 สมาชิก: {mem['first_name']} {mem['last_name']}")
                messagebox.showinfo("สำเร็จ", "ลงชื่อเข้าใช้สมาชิกสำเร็จ ได้รับส่วนลด 25%", parent=log_pop)
                log_pop.destroy()
                reload_cart() # คำนวณเงินใหม่เพราะได้ส่วนลด
            else:
                messagebox.showerror("ไม่พบข้อมูล", "ไม่พบเบอร์โทรศัพท์นี้ในระบบ", parent=log_pop)
                
        tk.Button(log_pop, text="ตรวจสอบ", command=do_login, bg="blue", fg="white").pack(pady=10)

    btn_frame = tk.Frame(frame3)
    btn_frame.pack(fill=tk.X, pady=5)
    tk.Button(btn_frame, text="สมัครสมาชิก", command=popup_register).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
    tk.Button(btn_frame, text="ลงชื่อเข้าใช้ (รับส่วนลด 25%)", command=popup_login).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
    
    def logout_member():
        global current_member_info
        current_member_info = {"phone": None, "first_name": None, "last_name": None}
        lbl_member_status_var.set("👤 ลูกค้าทั่วไป (ไม่มีส่วนลด)")
        reload_cart()
    tk.Button(frame3, text="ออกจากระบบสมาชิก", command=logout_member, fg="red").pack(fill=tk.X, pady=2)


    # ========================== ส่วนที่ 3 กลาง: สรุปยอด ==========================
    tk.Label(frame3, text="สรุปยอดชำระ", bg="lightcoral", font=("Arial", 12, "bold")).pack(fill=tk.X, pady=10)
    
    summary_frame = tk.Frame(frame3)
    summary_frame.pack(fill=tk.X, padx=10, pady=5)
    
    lbl_subtotal_var = tk.StringVar(value="0.00 บาท")
    lbl_discount_var = tk.StringVar(value="0.00 บาท")
    lbl_vat_var = tk.StringVar(value="0.00 บาท")
    lbl_grand_total_var = tk.StringVar(value="0.00 บาท")
    
    tk.Label(summary_frame, text="รวมเงิน (Subtotal):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=2)
    tk.Label(summary_frame, textvariable=lbl_subtotal_var, font=("Arial", 10)).grid(row=0, column=1, sticky="e", pady=2)
    
    tk.Label(summary_frame, text="ส่วนลดสมาชิก (25%):", font=("Arial", 10), fg="red").grid(row=1, column=0, sticky="w", pady=2)
    tk.Label(summary_frame, textvariable=lbl_discount_var, font=("Arial", 10), fg="red").grid(row=1, column=1, sticky="e", pady=2)
    
    tk.Label(summary_frame, text="ภาษีมูลค่าเพิ่ม (VAT 7%):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=2)
    tk.Label(summary_frame, textvariable=lbl_vat_var, font=("Arial", 10)).grid(row=2, column=1, sticky="e", pady=2)
    
    tk.Label(summary_frame, text="ยอดสุทธิ (Grand Total):", font=("Arial", 14, "bold"), fg="green").grid(row=3, column=0, sticky="w", pady=10)
    tk.Label(summary_frame, textvariable=lbl_grand_total_var, font=("Arial", 14, "bold"), fg="green").grid(row=3, column=1, sticky="e", pady=10)
    summary_frame.columnconfigure(1, weight=1)
    
    
    def reload_cart():
        """ฟังก์ชันสำหรับเคลียร์ตารางอ่านบิลใหม่ และคำนวณเงิน"""
        for row in cart_tree.get_children():
            cart_tree.delete(row)
            
        total_sum = 0.0
        if os.path.exists(bill_path):
            with open(bill_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    pid, name, price, qty, total = parts
                    total_sum += float(total)
                    cart_tree.insert("", tk.END, values=(pid, f"{name} (x{qty})", price, total))

        discount = 0.0
        if current_member_info["phone"] is not None:
            discount = total_sum * 0.25 # ลด 25% สำหรับกระเป๋า
            
        after_discount = total_sum - discount
        vat = after_discount * 0.07 # ภาษี 7%
        grand_total = after_discount + vat
        
        lbl_subtotal_var.set(f"{total_sum:,.2f} บาท")
        lbl_discount_var.set(f"-{discount:,.2f} บาท")
        lbl_vat_var.set(f"+{vat:,.2f} บาท")
        lbl_grand_total_var.set(f"{grand_total:,.2f} บาท")

    # โหลดตะกร้าครั้งแรก
    load_products_to_frame(frame1, reload_cart)
    reload_cart()
    
    # ========================== ส่วนที่ 3 ล่าง: ดำเนินการ ==========================
    action_frame = tk.Frame(frame3)
    # ลบ expand=True ทิ้งเพื่อป้องกันไม่ให้ปุ่มข้างล่างโดนดันตกขอบจอ
    action_frame.pack(fill=tk.X, pady=10)
    
    def hold_bill():
        if not os.path.exists(bill_path):
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return
            
        with open(bill_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        if not lines:
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return
            
        held_dir = os.path.join(os.path.dirname(__file__), "data", "held_bills")
        os.makedirs(held_dir, exist_ok=True)
        
        # ตั้งชื่อไฟล์เป็น วัน-เดือน-ปี_ชั่วโมง-นาที-วินาที
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        held_file = os.path.join(held_dir, f"bill_{timestamp}.txt")
        
        # ย้ายข้อมูลไปไฟล์พักบิลและล้างของเดิม
        with open(held_file, "w", encoding="utf-8") as f:
            f.writelines(lines)
        open(bill_path, "w").close()
        reload_cart()
        messagebox.showinfo("สำเร็จ", f"พักบิลไว้เรียบร้อยแล้วในชื่อ:\n{timestamp}")

    def recall_bill():
        held_dir = os.path.join(os.path.dirname(__file__), "data", "held_bills")
        os.makedirs(held_dir, exist_ok=True)
        
        files = [f for f in os.listdir(held_dir) if f.endswith(".txt")]
        if not files:
            messagebox.showinfo("แจ้งเตือน", "ไม่มีบิลที่ถูกพักไว้")
            return
            
        recall_pop = tk.Toplevel(parent)
        recall_pop.title("เลือกบิลที่ต้องการเรียกคืน")
        recall_pop.geometry("300x300")
        recall_pop.grab_set()
        
        tk.Label(recall_pop, text="รายการพักบิลทั้งหมด:", font=("Arial", 10, "bold")).pack(pady=5)
        
        listbox = tk.Listbox(recall_pop, font=("Arial", 10))
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
            held_path = os.path.join(held_dir, selected_file)
            
            # อ่านข้อมูลที่พักไว้มาใส่ท้าย bill.txt ปัจจุบัน
            with open(held_path, "r", encoding="utf-8") as hf:
                held_lines = hf.readlines()
                
            with open(bill_path, "a", encoding="utf-8") as bf:
                bf.writelines(held_lines)
                
            # ลบไฟล์ที่พักทิ้ง
            os.remove(held_path)
            
            messagebox.showinfo("สำเร็จ", "เรียกบิลเรียบร้อยแล้ว เพิ่มสินค้าลงตะกร้าแล้ว", parent=recall_pop)
            reload_cart()
            recall_pop.destroy()
            
        tk.Button(recall_pop, text="เรียกคืนบิลนี้", command=do_recall, bg="lightblue").pack(pady=10)
        
    tk.Button(action_frame, text="พักบิล (Hold Bill)", command=hold_bill, bg="orange").pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)
    tk.Button(action_frame, text="เรียกบิล (Recall Bill)", command=recall_bill, bg="lightblue").pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)

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
                success_msg = f"ทำรายการสำเร็จ!\nระบบได้บันทึกยอดขายและออกใบเสร็จที่:\n{pdf_file}"
            except Exception as e:
                success_msg = f"ทำรายการสำเร็จ! แต่เกิดข้อผิดพลาดในการสร้างใบเสร็จ: {e}"
                
            messagebox.showinfo("สำเร็จ", success_msg)
            open(bill_path, 'w').close() 
            logout_member() # รับเงินเสร็จ เตะสมาชิกออกรอคิวต่อไป
        else:
            errors = "\n".join(error_msgs)
            messagebox.showwarning("ข้อผิดพลาด", f"สต๊อกไม่พอ:\n{errors}\n*ระบบเคลียร์ตะกร้าแล้ว")
            open(bill_path, 'w').close()
            reload_cart()
                
    # ปุ่มยืนยันรายการจ่ายเงิน (แพ็คให้ติดขอบล่างเสมอ ป้องกันการโดนดันตกจอ)
    tk.Button(
        frame3, 
        text="ยืนยันการทำรายการ\n(Confirm & ออกใบเสร็จ)", 
        font=("Arial", 14, "bold"), 
        bg="green", 
        fg="white", 
        command=confirm_checkout
    ).pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
    
    # ส่งเฟรมทั้ง 3 กลับเป็นก้อน
    return frame1, frame2, frame3


# ========================================================================= #
# ส่วนที่ 3: ฟังก์ชันโหลดปุ่มสินค้า
# ========================================================================= #
def load_products_to_frame(frame, reload_cart_cb=None):
    """
    ฟังก์ชันสำหรับอ่านไฟล์ products.txt และสร้างปุ่มสินค้ามาวางเรียงกันในเฟรมซ้ายสุด
    """
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
                
                # ฟังก์ชันเมื่อปุ่มสินค้าถูกคลิก
                def on_product_click(p_id=product_id, p_name=product_name):
                    global current_selected_product
                    # เซฟไว้ว่ากดอันไหนไป
                    current_selected_product["id"] = p_id
                    current_selected_product["name"] = p_name
                    # เปิดหน้า Numpad กรอกจำนวน
                    open_numpad_popup(frame, reload_cart_cb)
                
                # สร้างปุ่มสำหรับสินค้านั้นๆ
                btn = tk.Button(
                    frame, 
                    text=product_name, 
                    font=("Arial", 10),
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
        tk.Label(frame, text="⚠️ ไม่พบไฟล์ data/products.txt", fg="red").grid(row=0, column=0, columnspan=4, pady=20)
        

# ========================================================================= #
# ส่วนที่ 4: หน้าต่างกรอกจำนวนสินค้า (Numpad)
# ========================================================================= #
def open_numpad_popup(parent, on_add_to_cart_cb=None):
    """
    ป๊อปอัปให้กดตัวเลข 0-9 เพื่อระบุจำนวนที่ต้องการ
    """
    popup = tk.Toplevel(parent)
    popup.title("Amount Products")
    popup.geometry("300x420")
    
    # ล็อคความสนใจไว้ที่หน้าต่างนี้จนกว่าจะปิด
    popup.grab_set()
    popup.transient(parent)
    popup.focus_force()
    
    qty_var = tk.StringVar(value="0") # ค่าตั้งต้นบนจอ
    
    # หน้าจอแสดงตัวเลข
    display = tk.Label(popup, textvariable=qty_var, font=("Arial", 28, "bold"), bg="white", relief="sunken", anchor="e")
    display.pack(fill=tk.X, padx=10, pady=10, ipady=10)
    
    # กรอบสำหรับเรียงปุ่ม
    keypad_frame = tk.Frame(popup)
    keypad_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
    
    for i in range(3): keypad_frame.columnconfigure(i, weight=1)
    for i in range(4): keypad_frame.rowconfigure(i, weight=1)
        
    def btn_press(key):
        """ฟังก์ชันสำหรับปุ่มกดแต่ละตัวในป๊อปอัป"""
        current = str(qty_var.get())
        if key == "C":
            qty_var.set("0") # เคลียร์ค่าคืนเป็น 0
        elif key == "<-":
            # ลบปลายถอยหลังไป 1 ตัว ถ้าไม่เหลืออะไรให้เป็น 0
            if len(current) > 1:
                qty_var.set(current[:-1])
            else:
                qty_var.set("0")
        else:
            # พิมพ์ตัวเลขต่อท้าย
            if current == "0":
                qty_var.set(key) # ถ้าเป็น 0 อยู่ ให้แทนที่เลย (เช่น 0 ตามด้วย 5 = 5)
            else:
                qty_var.set(current + key)

    def create_btn_command(k):
        # สร้าง Closure คืนค่าคำสั่งที่ตรงกับตัวปุ่ม
        return lambda: btn_press(k)
        
    # ลิสต์จัดวางแผงปุ่ม
    buttons = [
        ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
        ('C', 3, 0), ('0', 3, 1), ('<-', 3, 2),
    ]
    
    # เจนเนอเรทและวางปุ่มเข้า Numpad
    for (text, row, col) in buttons:
        btn = tk.Button(keypad_frame, text=text, font=("Arial", 18, "bold"), command=create_btn_command(text))
        btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
    def submit():
        """ฟังก์ชันเมื่อกดยืนยัน เพิ่มลงตะกร้า (bill)"""
        try:
            qty_int = int(qty_var.get())
        except ValueError:
            qty_int = 0
            
        if qty_int <= 0:
            messagebox.showwarning("แจ้งเตือน", "กรุณาระบุจำนวนมากกว่า 0", parent=popup)
            return
            
        pid = current_selected_product["id"]
        if pid:
            # โหลดคลังขึ้นมาดูว่าของพอไหม
            inventory = product_manager.get_all_products()
            if pid not in inventory or inventory[pid]['stock'] < qty_int:
                messagebox.showwarning("ข้อผิดพลาด", "สินค้าในสต็อกไม่เพียงพอ!", parent=popup)
                return
                
            price = float(inventory[pid].get("price", 0.0))
            name = current_selected_product["name"]
            total_price = price * qty_int
            
            # บันทึกลงบิล
            bill_path = os.path.join(os.path.dirname(__file__), "data", "bill.txt")
            with open(bill_path, "a", encoding="utf-8") as f:
                f.write(f"{pid},{name},{price:.2f},{qty_int},{total_price:.2f}\n")
                
            messagebox.showinfo("สำเร็จ", "เพิ่มลงตะกร้าเรียบร้อยแล้ว", parent=popup)
            
            # เรียกรีโหลดตารางข้างนอก
            if on_add_to_cart_cb:
                on_add_to_cart_cb()
                
            popup.destroy()
        else:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบข้อมูลรหัสสินค้าที่เลือก", parent=popup)
            
    # ปุ่มยืนยัน
    tk.Button(popup, text="Confirm", command=submit, font=("Arial", 16, "bold"), bg="green", fg="white").pack(fill=tk.X, padx=10, pady=10)