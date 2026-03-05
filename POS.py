import tkinter as tk
from tkinter import ttk, messagebox
import os
import product_manager

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
    
    def reload_cart():
        """ฟังก์ชันสำหรับเคลียร์ตารางและอ่านบิลใหม่จากไฟล์ bill.txt"""
        # เคลียร์ข้อมูลเก่าทิ้งทั้งหมดก่อน
        for row in cart_tree.get_children():
            cart_tree.delete(row)
            
        # ถ้ามีไฟล์บิลอยู่ ให้ดึงข้อมูลมาเรียงใส่ตะกร้า
        if os.path.exists(bill_path):
            with open(bill_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            # แบ่งบรรทัดและแยกคอมม่า
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    pid, name, price, qty, total = parts
                    # เอามาใส่เข้าตารางตะกร้า
                    cart_tree.insert("", tk.END, values=(pid, f"{name} (x{qty})", price, total))

    # โหลดปุ่มสินค้าสู่เฟรมแรำ พร้อมส่งตัว reload_cart เพื่อให้อัพเดตตะกร้าเวลาเลือกของได้
    load_products_to_frame(frame1, reload_cart)
    # โหลดข้อมูลตะกร้าเตรียมไว้
    reload_cart()
    
    # ---------------------------------------------------------
    # เฟรมที่ 3: ปุ่มดำเนินการ (ยืนยัน/ตัดบิล)
    # ---------------------------------------------------------
    frame3 = tk.Frame(parent)
    frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    tk.Label(frame3, text="ดำเนินการ", bg="lightcoral", font=("Arial", 12, "bold")).pack(pady=10)
    
    def confirm_checkout():
        """ฟังก์ชันสำหรับเมื่อกดปุ่ม Confirm (ยืนยันบิล)"""
        # เช็คให้ชัวร์ว่ามีสินค้าในตะกร้าไหม
        if not os.path.exists(bill_path):
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return
            
        with open(bill_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        if not lines:
            messagebox.showinfo("แจ้งเตือน", "ไม่มีสินค้าในตะกร้า!")
            return
            
        # สถานะการตัดสต๊อก
        all_success = True
        error_msgs = []
        
        # วนลูปอ่านทุกบรรทัดและสั่งตัดสต๊อก (process_sale) ใน product_manager
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 5:
                pid, name, price, qty, total = parts
                success, msg = product_manager.process_sale(pid, int(qty))
                if not success:
                    # ถ้าของไม่พอ จะถูกบันทึกไว้ในข้อผิดพลาด
                    all_success = False
                    error_msgs.append(f"{name}: {msg}")
                    
        # ถ้าผ่านหมด ล้างตะกร้าให้เลย
        if all_success:
            messagebox.showinfo("สำเร็จ", "ตัดสต๊อกสินค้าทั้งหมดเรียบร้อยแล้ว!")
            open(bill_path, 'w').close() # ลบข้อความในระบบบิลทิ้งให้ว่าง
            reload_cart()
        else:
            # ถ้ามีสินค้าบางรายการที่ตัดไม่ได้ แจ้งเตือนและล้างบิลเหมือนกัน
            errors = "\n".join(error_msgs)
            messagebox.showwarning("ข้อผิดพลาดบางรายการ", f"ตัดสต๊อกไม่สำเร็จบางรายการ:\n{errors}\n*ระบบได้ล้างตะกร้าแล้ว กรุณาเพิ่มเฉพาะสินค้าที่ติดปัญหาใหม่ถ้าต้องการ")
            open(bill_path, 'w').close()
            reload_cart()
            
    # ปุ่มยืนยันรายการจ่ายเงิน
    tk.Button(
        frame3, 
        text="ยืนยันการทำรายการ\n(Confirm & ตัดสต็อก)", 
        font=("Arial", 14, "bold"), 
        bg="green", 
        fg="white", 
        command=confirm_checkout
    ).pack(fill=tk.X, padx=10, pady=10)
    
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