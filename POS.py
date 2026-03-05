import tkinter as tk
import os
from tkinter import messagebox
import datetime

# ==========================================
# 1. การตั้งค่าตัวแปรระบบ (System Setup)
# ==========================================

# สร้างโฟลเดอร์สำหรับเก็บไฟล์บิลที่ถูกพักไว้ (Hold Bills)
HOLD_DIR = "hold_bills"
if not os.path.exists(HOLD_DIR):
    os.makedirs(HOLD_DIR)

# ตัวแปรสำหรับอ้างอิง UI เลเบลต่างๆบนหน้าจอ (เพื่อให้เราแก้ข้อความได้ทีหลัง)
vat_label_ref = None
net_label_ref = None
total_label_ref = None
cart_frame_ref = None

# ตัวแปรเก็บสถานะการทำงานของตู้ POS
current_total_sum = 0.0  # เก็บยอดรวมของราคาสินค้าในตะกร้าทั้งหมด
is_holding = False       # เก็บสถานะว่ากำลังพักบิลอยู่หรือไม่
last_pos = 0             # จดจำตำแหน่งบรรทัดล่าสุดที่อ่านไฟล์ Bill.txt (เพื่อไม่ให้อ่านของเดิมซ้ำ)
row_bill = 1             # แถวของรายการสินค้าในตะกร้า เริ่มที่ 1 เพราะแถวที่ 0 เป็นหัวตาราง

# ==========================================
# 2. ส่วนแสดงผลฝั่งซ้าย: เมนูสินค้าและการค้นหา
# ==========================================
def setup_pos_interface(p2, root):
    """สร้างหน้าอินเตอร์เฟซหลักฝั่งซ้าย สำหรับแสดงปุ่มสินค้าและช่องค้นหา"""
    
    # 1. กล่องกรอบฝั่งซ้ายสุด
    container_left = tk.Frame(p2, bg="black")
    container_left.place(x=0, y=0, width=690, height=1000)

    # 2. แถบค้นหาสินค้า
    search_frame = tk.Frame(container_left, bg="#222")
    search_frame.pack(side="top", fill="x", padx=10, pady=10)
    
    tk.Label(search_frame, text="Search:", fg="white", bg="#222", font=("Arial", 12)).pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, font=("Arial", 14))
    search_entry.pack(side="left", fill="x", expand=True, padx=5)

    # 3. สร้างพื้นที่ Canvas และ Scrollbar เพื่อให้เมนูสินค้าสามารถเลื่อนขึ้นลงได้
    canvas_menu = tk.Canvas(container_left, bg="black", highlightthickness=0)
    scrollbar_menu = tk.Scrollbar(container_left, orient="vertical", command=canvas_menu.yview)
    canvas_menu.configure(yscrollcommand=scrollbar_menu.set)
    scrollbar_menu.pack(side="right", fill="y")
    canvas_menu.pack(side="left", fill="both", expand=True)

    # 4. กล่องสำหรับวางปุ่มสินค้าด้านใน Canvas
    menu_frame = tk.Frame(canvas_menu, bg="black")
    canvas_menu.create_window((0, 0), window=menu_frame, anchor="nw")

    # 5. ตั้งค่าเพื่อให้ Canvas รู้ขนาดของเนื้อหาและเลื่อนเมาส์ได้
    menu_frame.bind("<Configure>", lambda e: canvas_menu.configure(scrollregion=canvas_menu.bbox("all")))
    
    def _on_mousewheel_menu(event):
        canvas_menu.yview_scroll(int(-1*(event.delta/120)), "units")
    
    container_left.bind("<Enter>", lambda e: canvas_menu.bind_all("<MouseWheel>", _on_mousewheel_menu))
    container_left.bind("<Leave>", lambda e: canvas_menu.unbind_all("<MouseWheel>"))

    # 6. ผูกการพิมพ์ในช่องค้นหากับฟังก์ชันปุ่ม (พิมพ์ปุ๊บ กรองผลทันที)
    search_entry.bind("<KeyRelease>", lambda e: generate_buttons(root, p2, menu_frame, search_entry.get(), canvas_menu))

    # 7. โหลดปุ่มสินค้าทั้งหมดในครั้งแรก
    generate_buttons(root, p2, menu_frame, "", canvas_menu)
    
    return menu_frame

def generate_buttons(root, p2, target_frame, search_query="", canvas=None):
    """อ่านข้อมูลจาก products.txt เพื่อสร้างปุ่มสินค้า และกรองตามคำค้นหา"""
    
    # ลบปุ่มเก่าทั้งหมดก่อนสร้างใหม่
    for widget in target_frame.winfo_children():
        widget.destroy()

    try:
        with open('data/products.txt', 'r', encoding='utf-8') as f:
            display_index = 0  # ตัวแปรช่วยนับเพื่อจัดเรียงปุ่มเป็นตารางกริด
            for line in f:
                data = [item.strip() for item in line.split(',')]
                if len(data) < 4: continue
                
                p_name = data[1]
                p_stock = int(data[2])
                p_price = data[3]

                # กรองสินค้าโดยเช็คว่าคำค้นหาอยู่ในชื่อสินค้าหรือไม่ (ตัวพิมพ์เล็ก-ใหญ่ไม่มีผล)
                if search_query.lower() not in p_name.lower():
                    continue

                # จัดรูปแบบให้แถวละ 4 ปุ่ม
                row_pos = display_index // 4
                col_pos = display_index % 4

                # สร้างปุ่มสินค้า หากสต็อก <= 0 ปุ่มจะกดไม่ได้และเป็นสีเทา
                btn = tk.Button(
                    target_frame, 
                    text=f"{p_name}\n({p_price} ฿)\nStock: {p_stock}",
                    width=21, 
                    height=10,
                    state="normal" if p_stock > 0 else "disabled",
                    bg="white" if p_stock > 0 else "#cccccc",
                    command=lambda n=p_name, p=p_price: open_amount_window(root, n, p, p2)
                )
                btn.grid(row=row_pos, column=col_pos, padx=5, pady=5)
                display_index += 1

        # อัปเดตขนาดการเลื่อนหน้าจอ
        if canvas:
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

    except FileNotFoundError:
        tk.Label(target_frame, text="ไม่พบไฟล์ data/products.txt", fg="white", bg="black").grid()

# ==========================================
# 3. ส่วนแสดงผลฝั่งกลาง: ตะกร้าสินค้า
# ==========================================
def create_canvas_show_product_to_cart(p2):
    """สร้างพื้นที่แสดงรายการสินค้าที่เลือกใส่ตะกร้า (Cart)"""
    global row_bill, cart_frame_ref
    row_bill = 1 

    # 1. คอนเทนเนอร์ตรงกลาง แบ็กกราวด์สีเทาเข้ม
    container_right = tk.Frame(p2, bg="#333") 
    container_right.place(x=700, y=0, width=690, height=1000)

    # 2. ปรับให้ตะกร้าสามารถเลื่อนScrollbar ได้
    canvas_cart = tk.Canvas(container_right, bg="white", highlightthickness=0)
    scrollbar_cart = tk.Scrollbar(container_right, orient="vertical", command=canvas_cart.yview)
    canvas_cart.configure(yscrollcommand=scrollbar_cart.set)
    scrollbar_cart.pack(side="right", fill="y")
    canvas_cart.pack(side="left", fill="both", expand=True)

    # 3. พื้นที่สำหรับใส่แถวสินค้า (cart_frame_ref)
    cart_frame_ref = tk.Frame(canvas_cart, bg="white")
    canvas_cart.create_window((0, 0), window=cart_frame_ref, anchor="nw")

    # ส่วนหัวตารางของตะกร้า
    header_font = ("Arial", 16, "bold")
    header_bg = "#eeeeee" 
    tk.Label(cart_frame_ref, text="Product", font=header_font, bg=header_bg, width=24, anchor="w").grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
    tk.Label(cart_frame_ref, text="Amount", font=header_font, bg=header_bg, width=8).grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
    tk.Label(cart_frame_ref, text="Price", font=header_font, bg=header_bg, width=12, anchor="e").grid(row=0, column=2, sticky="nsew", padx=10, pady=5)

    # 4. ตั้งค่าให้เมาส์สามารถเลื่อนหน้าจอตะกร้าได้
    cart_frame_ref.bind("<Configure>", lambda e: canvas_cart.configure(scrollregion=canvas_cart.bbox("all")))
    
    def _on_mousewheel_cart(event):
        canvas_cart.yview_scroll(int(-1*(event.delta/120)), "units")
    
    container_right.bind("<Enter>", lambda e: canvas_cart.bind_all("<MouseWheel>", _on_mousewheel_cart))
    container_right.bind("<Leave>", lambda e: canvas_cart.unbind_all("<MouseWheel>"))

    return cart_frame_ref

# ==========================================
# 4. ส่วนแสดงผลฝั่งขวา: ราคารวมและปุ่มสั่งการ
# ==========================================
def setup_total_price_interface(p2):
    """สร้างส่วนแสดงราคาสุทธิ ภาษี และปุ่มต่างๆ (พักบิล, เคลียร์บิล, ชำระเงิน)"""
    global total_label_ref, vat_label_ref, net_label_ref
    
    show_price_frame = tk.Frame(p2, bg="white") 
    show_price_frame.place(x=1390, y=0, width=522, height=1000)
    
    # สินค้ารวมยังไม่บวกภาษี
    net_label_ref = tk.Label(show_price_frame, text="Total Price: 0.00 ฿", font=("Arial", 18), bg="#333", fg="white", width=30, height=2)
    net_label_ref.pack(pady=5)
    
    # ภาษี 7%
    vat_label_ref = tk.Label(show_price_frame, text="VAT (7%): 0.00 ฿", font=("Arial", 18), bg="#f5a623", fg="black", width=30, height=2)
    vat_label_ref.pack(pady=5)

    # ราคาสุทธิ (ต้องจ่ายทั้งหมด)
    tk.Label(show_price_frame, text="Net Amount", font=("Arial", 25, "bold"), bg="white").pack(pady=(80, 5))
    total_label_ref = tk.Label(show_price_frame, text="0.00 ฿", font=("Arial", 40, "bold"), fg="white", bg="#d0021b", width=15)
    total_label_ref.pack(pady=10)

    # ปุ่มคำสั่งเพิ่มเติม
    tk.Button(show_price_frame, text="Hold Bill", command=hold_bill, font=("Arial", 15), bg="orange", width=20).pack(pady=10)
    tk.Button(show_price_frame, text="Recall Bill", command=recall_bill, font=("Arial", 15), bg="blue", fg="white", width=20).pack(pady=5)
    tk.Button(show_price_frame, text="Clear Cart", command=clear_cart, font=("Arial", 15), bg="#777777", fg="white", width=20).pack(pady=5)
    
    # ปุ่มชำระเงินขนาดใหญ่
    btpay = tk.Button(show_price_frame, text="Payment", command=process_payment, font=("Arial", 25, "bold"), bg="green", fg="white", width=50, height=5)
    btpay.pack(side="bottom", pady=40)
    
    return show_price_frame

def update_price_labels():
    """คำนวณราคาใหม่ทุกครั้งที่มีการเปลี่ยนสินค้า และอัปเดตหน้าจอ"""
    global current_total_sum, total_label_ref, vat_label_ref, net_label_ref
    
    sub_total = current_total_sum
    vat_amount = sub_total * 0.07
    net_total = sub_total + vat_amount

    # .config() ใช้เพื่อแก้ไขข้อความของ Label นั้นๆ
    if total_label_ref: total_label_ref.config(text=f"{net_total:,.2f} ฿")
    if vat_label_ref: vat_label_ref.config(text=f"VAT (7%): {vat_amount:,.2f} ฿")
    if net_label_ref: net_label_ref.config(text=f"Total Price: {sub_total:,.2f} ฿")

# ==========================================
# 5. ป็อปอัปและการเพิ่มสินค้า
# ==========================================
def open_amount_window(root, product_name, p_price, p2):
    """เปิดหน้าจอเล็กเพื่อรับค่าจำนวนสินค้า แล้วบวกเข้าไปในบิล"""
    global cart_frame_ref
    window_select = tk.Toplevel(root) 
    window_select.title("DevCat - ใส่ปริมาณ")
    window_select.geometry("350x220+750+300")
    
    tk.Label(window_select, text=product_name, font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(window_select, text=f"ราคา/ชิ้น: {p_price} ฿", font=("Arial", 12)).pack()
    
    # ช่องกรอกจำนวน
    count_product = tk.Entry(window_select, font=("Arial", 16), justify="center", width=10)
    count_product.pack(pady=10)
    count_product.focus() # ให้คอร์เซอร์กระพริบที่ช่องนี้อัตโนมัติ

    def confirm_value():
        global last_pos, row_bill, current_total_sum
        raw_value = count_product.get()
        # เช็คให้แน่ใจว่าค่าที่พิมพ์มาเป็นตัวเลขที่ถูกต้อง
        if not raw_value.isdigit() or int(raw_value) <= 0: return 
        
        file_name = "Bill.txt"
        
        # 1. เขียนสินค้าลงไฟล์บิล
        with open(file_name, "a", encoding="utf-8") as o:
            o.write(product_name + "\n")
            o.write(raw_value + "\n")
            o.write(p_price + "\n")

        # 2. อ่านไฟล์บิล และวาดสินค้าชิ้นใหม่ลงตะกร้า
        with open(file_name, 'r', encoding='utf-8') as f:
            f.seek(last_pos) # อ่านข้ามส่วนเก่า ไปเริ่มอ่านของใหม่ทันที
            new_data = [line.strip() for line in f.readlines() if line.strip()]
            
            # วนลูปอ่านชุดละ 3 บรรทัด (ชื่อ, จำนวน, ราคา)
            for i in range(0, len(new_data), 3):
                if i + 2 < len(new_data):
                    name = new_data[i]
                    amount = new_data[i+1]
                    price = new_data[i+2]
                    
                    total_item_price = float(price) * int(amount)
                    current_total_sum += total_item_price
                    update_price_labels()

                    # วาดรายการสินค้าใหม่เรียงลง Grid ต่อท้าย
                    if cart_frame_ref:
                        tk.Label(cart_frame_ref, text=name, font=("Arial", 14), bg="white", fg="black", anchor="w").grid(row=row_bill, column=0, sticky="w", padx=10, pady=5)
                        tk.Label(cart_frame_ref, text=amount, font=("Arial", 14), bg="white", fg="black").grid(row=row_bill, column=1, padx=10, pady=5)
                        tk.Label(cart_frame_ref, text=f"{total_item_price:.2f}", font=("Arial", 14), bg="white", fg="green", anchor="e").grid(row=row_bill, column=2, sticky="e", padx=10, pady=5)
                        row_bill += 1
            
            last_pos = f.tell() # เซฟตำแหน่งล่าสุดเอาไว้
            
        window_select.destroy() # ปิดหน้าต่างลง
        
    tk.Button(window_select, text="ยืนยัน (Confirm)", command=confirm_value, font=("Arial", 12), bg="#4caf50", fg="white", width=15).pack(pady=5)
    
    # กด Enter เพื่อยืนยันได้เลย
    window_select.bind('<Return>', lambda event: confirm_value())

# ==========================================
# 6. ฟังก์ชันจัดการระบบและฐานข้อมูล
# ==========================================
def get_pid_by_name(name):
    """ค้นหาไอดี (PID) ของสินค้าผ่านชื่อ"""
    try:
        with open('data/products.txt', 'r', encoding='utf-8') as f:
            for line in f:
                data = line.strip().split(',')
                if data[1] == name: return data[0]
    except FileNotFoundError: pass
    return None

def process_sale(pid, quantity):
    """ฟังก์ชันตัดสต็อกเมื่อทำการขายสำเร็จ"""
    file_path = 'data/products.txt'
    if not os.path.exists(file_path): return

    updated_data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = [item.strip() for item in line.split(',')]
            if data[0] == pid:
                try:
                    new_stock = int(data[2]) - int(quantity)
                    data[2] = str(max(new_stock, 0)) # ป้องกันสต็อกติดลบ
                except (ValueError, IndexError): pass
            updated_data.append(",".join(data))

    # เซฟกลับทับไฟล์เดิม
    with open(file_path, 'w', encoding='utf-8') as f:
         f.write("\n".join(updated_data) + "\n")

def process_payment():
    """ฟังก์ชันชำระเงิน ตัดบิล ตัดชำระ สร้างใบเสร็จลูกค้า และล้างข้อมูลหน้าจอ"""
    global current_total_sum, row_bill, last_pos
    temp_bill_file = "Bill.txt"
    
    if not os.path.exists(temp_bill_file):
        messagebox.showwarning("DevCat", "ไม่มีรายการสินค้าให้ชำระเงิน")
        return

    try:
        now = datetime.datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
        file_name_timestamp = now.strftime("%Y%m%d_%H%M%S")
        customer_bill_name = f"Customer_Bill_{file_name_timestamp}.txt"
        
        sub_total = current_total_sum
        vat_amount = sub_total * 0.07
        net_total = sub_total + vat_amount

        # อ่านข้อมูลสินค้าจากตะกร้า
        with open(temp_bill_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        # เริ่มสร้างไฟล์ใบเสร็จลูกค้า Customer_Bill
        with open(customer_bill_name, 'w', encoding='utf-8') as f_out:
            f_out.write("==============================\n")
            f_out.write("       Store: DevCat         \n")
            f_out.write(f"  Date: {timestamp_str}\n")
            f_out.write("==============================\n")
            f_out.write(f"{'Item':<15} {'Qty':<5} {'Total':>8}\n")
            f_out.write("------------------------------\n")

            for i in range(0, len(lines), 3):
                name = lines[i]
                qty = lines[i+1]
                price = lines[i+2]
                item_total = float(price) * int(qty)
                
                f_out.write(f"{name[:15]:<15} {qty:<5} {item_total:>8.2f}\n")
                f_out.write(f"  (@{price})\n")

                # ตัดสต็อกทีละบรรทัด
                target_pid = get_pid_by_name(name)
                if target_pid: process_sale(target_pid, qty)

            f_out.write("------------------------------\n")
            f_out.write(f"Sub-total:            {sub_total:>8.2f} ฿\n")
            f_out.write(f"VAT (7%):             {vat_amount:>8.2f} ฿\n")
            f_out.write(f"Net Amount:           {net_total:>8.2f} ฿\n")
            f_out.write("==============================\n")

        # ลบไฟล์บิลเทมพ์เพลตทิ้ง และรีเซ็ตตัวแปร
        os.remove(temp_bill_file)
        messagebox.showinfo("DevCat", "ชำระเงินและตัดสต็อกเสร็จสิ้น!")

        current_total_sum = 0.0
        row_bill = 1
        last_pos = 0
        update_price_labels()

        # ล้างคอมโพเนนท์ออกจากตะกร้าบนหน้าจอ
        if cart_frame_ref:
            for widget in cart_frame_ref.winfo_children():
                if int(widget.grid_info().get("row", 0)) > 0:
                    widget.destroy()
        
    except Exception as e:
        messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")

# ==========================================
# 7. ฟังก์ชันพักบิลและคืนบิล (Hold & Recall)
# ==========================================
def hold_bill():
    """ย้ายบิลปัจจุบันไปเก็บไว้ในโฟลเดอร์ hold_bills ชั่วคราว"""
    global current_total_sum, row_bill, last_pos
    source_file = "Bill.txt"

    if os.path.exists(source_file):
        file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        hold_file_path = os.path.join(HOLD_DIR, f"Bill_{file_timestamp}.txt")
        
        # ย้ายๆไฟล์จากหลักเป็นพัก
        os.rename(source_file, hold_file_path) 
        
        # รีเซ็ตหน้าจอรถเข็นให้ว่าง
        current_total_sum = 0.0
        row_bill = 1
        last_pos = 0
        update_price_labels() 
        
        if cart_frame_ref:
            for widget in cart_frame_ref.winfo_children():
                if int(widget.grid_info().get("row", 0)) > 0:
                    widget.destroy()
        
        messagebox.showinfo("Hold Bill", "บันทึกและพักบิลเรียบร้อยแล้ว")
    else:
        messagebox.showwarning("Hold Bill", "ไม่มีรายการให้พัก")

def recall_bill():
    """เปิดหน้าต่างรายการบิลที่โดนพักไว้ และเลือกเพื่อนำกลับมาใส่ตะกร้า"""
    # ถ้าของใหม่ค้างอยู่ ห้ามซ้อน
    if os.path.exists("Bill.txt") or current_total_sum > 0:
        messagebox.showwarning("Recall Bill", "กรุณาจัดการบิลปัจจุบันก่อนเรียกคืนบิลอื่น")
        return

    files = [f for f in os.listdir(HOLD_DIR) if f.endswith('.txt')]
    if not files:
        messagebox.showwarning("Recall Bill", "ไม่มีบิลที่พักไว้")
        return

    # สร้างหน้าต่างเลือกบิล
    recall_window = tk.Toplevel()
    recall_window.title("เลือกบิลที่ต้องการเรียกคืน")
    recall_window.geometry("400x400")

    tk.Label(recall_window, text="รายการบิลที่พักไว้", font=("Arial", 14, "bold")).pack(pady=10)
    lb = tk.Listbox(recall_window, font=("Arial", 12), width=35)
    lb.pack(padx=20, pady=10, expand=True, fill="both")

    for f in files:
        # ตัดนามสกุลไฟล์ให้ดูสวยขึ้นเวลาโชว์
        display_name = f.replace("Bill_", "").replace(".txt", "")
        lb.insert("end", display_name)

    def select_and_recall():
        selection = lb.curselection()
        if selection:
            filename = files[selection[0]]
            full_path = os.path.join(HOLD_DIR, filename)
            
            # ดึงกลับมาเป็นบิลหลักทำงานต่อ
            os.rename(full_path, "Bill.txt")
            refresh_cart_display()
            recall_window.destroy()
            messagebox.showinfo("Success", "เรียกคืนบิลสำเร็จ")

    tk.Button(recall_window, text="ยืนยัน", command=select_and_recall, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

def refresh_cart_display():
    """ฟังก์ชันแฝงที่ทำหน้าที่โหลด Bill.txt ที่ถูก Recall เพื่อมาจัดเรียงบนหน้าจอตะกร้าใหม่แบบเต็มรูปแบบ"""
    global current_total_sum, row_bill, last_pos
    file_name = "Bill.txt"
    
    if os.path.exists(file_name):
        current_total_sum = 0.0
        row_bill = 1
        
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
            for i in range(0, len(lines), 3):
                name = lines[i]
                amount = lines[i+1]
                price = lines[i+2]
                
                total_item_price = float(price) * int(amount)
                current_total_sum += total_item_price
                
                if cart_frame_ref:
                    tk.Label(cart_frame_ref, text=name, font=("Arial", 14), bg="white", fg="black", anchor="w").grid(row=row_bill, column=0, sticky="w", padx=10, pady=5)
                    tk.Label(cart_frame_ref, text=amount, font=("Arial", 14), bg="white", fg="black").grid(row=row_bill, column=1, padx=10, pady=5)
                    tk.Label(cart_frame_ref, text=f"{total_item_price:.2f}", font=("Arial", 14), bg="white", fg="green", anchor="e").grid(row=row_bill, column=2, sticky="e", padx=10, pady=5)
                row_bill += 1
            
            update_price_labels()
            last_pos = f.tell()

# ==========================================
# 8. ฟังก์ชันการล้างบิลและการปิดหน้าต่าง
# ==========================================
def clear_cart():
    """ลบทิ้งรายการสินค้าจากทั้งในไฟล์บิลและบนหน้าจอทั้งหมด"""
    global current_total_sum, row_bill, last_pos
    file_name = "Bill.txt"
    
    if not os.path.exists(file_name) and current_total_sum == 0:
        messagebox.showwarning("Clear Cart", "ไม่มีรายการสินค้าในรถเข็น")
        return

    confirm = messagebox.askyesno("Confirm Clear", "คุณต้องการล้างรายการทั้งหมดในตะกร้าใช่หรือไม่?")
    if confirm:
        if os.path.exists(file_name):
            os.remove(file_name)
        
        current_total_sum = 0.0
        row_bill = 1
        last_pos = 0
        update_price_labels()
        
        if cart_frame_ref:
            # ลบทุกไอเทมออก ยกเว้นแถวที่ 0 (หัวตาราง)
            for widget in cart_frame_ref.winfo_children():
                if int(widget.grid_info().get("row", 0)) > 0:
                    widget.destroy()
        
        messagebox.showinfo("Clear Cart", "ล้างตะกร้าเรียบร้อยแล้ว")

def on_closing(root):
    """เมื่อกดกากบาทปิดโปรแกรม จะล้างไฟล์บิลค้างทิ้ง เพื่อเริ่มต้นใหม่ในครั้งถัดไป"""
    file_name = "Bill.txt"
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
        except:
            pass
    root.destroy()