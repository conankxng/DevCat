import tkinter as tk
import os
from tkinter import messagebox  # ต้องเพิ่มบรรทัดนี้เพื่อใช้การแจ้งเตือน
import datetime

HOLD_DIR = "hold_bills"
if not os.path.exists(HOLD_DIR):
    os.makedirs(HOLD_DIR)



is_holding = False  # เช็คว่าตอนนี้มีการพักบิลอยู่ไหม
last_pos = 0
row_bill = 0 # ใช้ตัวแปรนับแถวแทน current_y เพื่อความสวยงามใน Grid

# --- ฝั่งที่ 1: ตั้งค่าหน้าเลือกสินค้า (ปุ่มเมนู) ---
def setup_pos_interface(p2, root):
    # 1. Container ฝั่งซ้าย
    container_left = tk.Frame(p2, bg="black")
    container_left.place(x=0, y=0, width=690, height=1000)

    canvas_menu = tk.Canvas(container_left, bg="black", highlightthickness=0)
    scrollbar_menu = tk.Scrollbar(container_left, orient="vertical", command=canvas_menu.yview)
    canvas_menu.configure(yscrollcommand=scrollbar_menu.set)

    scrollbar_menu.pack(side="right", fill="y")
    canvas_menu.pack(side="left", fill="both", expand=True)

    # Frame สำหรับวางปุ่ม
    menu_frame = tk.Frame(canvas_menu, bg="black")
    canvas_menu.create_window((0, 0), window=menu_frame, anchor="nw")

    # อัปเดตการเลื่อนเฉพาะฝั่งเมนู
    menu_frame.bind("<Configure>", lambda e: canvas_menu.configure(scrollregion=canvas_menu.bbox("all")))

    # ฟังก์ชัน Scroll wheel เฉพาะฝั่งเมนู
    def _on_mousewheel_menu(event):
        canvas_menu.yview_scroll(int(-1*(event.delta/120)), "units")
    
    # ผูกเหตุการณ์เมื่อเมาส์ "เข้า" มาในพื้นที่ฝั่งซ้ายเท่านั้น
    container_left.bind("<Enter>", lambda e: canvas_menu.bind_all("<MouseWheel>", _on_mousewheel_menu))
    container_left.bind("<Leave>", lambda e: canvas_menu.unbind_all("<MouseWheel>"))

    generate_buttons(root, p2, menu_frame)
    return menu_frame # ส่งค่ากลับไปใช้

# --- ฝั่งที่ 2: ตั้งค่าหน้าแสดงรายการสินค้า (รถเข็น) ---
def create_canvas_show_product_to_cart(p2):
    global row_bill
    # กำหนดให้เริ่มที่แถว 1 เพราะแถว 0 จะเอาไว้ทำหัวตาราง
    row_bill = 1 

    # 1. Container ฝั่งขวา (เหมือนเดิม)
    container_right = tk.Frame(p2, bg="#333") 
    container_right.place(x=700, y=0, width=690, height=1000)

    # 2. Canvas และ Scrollbar (เหมือนเดิม)
    canvas_cart = tk.Canvas(container_right, bg="white", highlightthickness=0)
    scrollbar_cart = tk.Scrollbar(container_right, orient="vertical", command=canvas_cart.yview)
    canvas_cart.configure(yscrollcommand=scrollbar_cart.set)
    scrollbar_cart.pack(side="right", fill="y")
    canvas_cart.pack(side="left", fill="both", expand=True)

    # 3. Frame สำหรับวางรายการสินค้า
    cart_grid_frame = tk.Frame(canvas_cart, bg="white")
    canvas_cart.create_window((0, 0), window=cart_grid_frame, anchor="nw")


    header_font = ("Arial", 16, "bold")
    header_bg = "#eeeeee" # สีพื้นหลังเทาอ่อนให้ดูเป็นหัวข้อ

    tk.Label(cart_grid_frame, text="Product", font=header_font, bg=header_bg, width=24, anchor="w").grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
    tk.Label(cart_grid_frame, text="Amount", font=header_font, bg=header_bg, width=8).grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
    tk.Label(cart_grid_frame, text="Price", font=header_font, bg=header_bg, width=12, anchor="e").grid(row=0, column=2, sticky="nsew", padx=10, pady=5)
    # -------------------------------------------

    # 4. อัปเดตการเลื่อนและ Bind Mousewheel (เหมือนเดิม)
    cart_grid_frame.bind("<Configure>", lambda e: canvas_cart.configure(scrollregion=canvas_cart.bbox("all")))
    
    def _on_mousewheel_cart(event):
        canvas_cart.yview_scroll(int(-1*(event.delta/120)), "units")
    
    container_right.bind("<Enter>", lambda e: canvas_cart.bind_all("<MouseWheel>", _on_mousewheel_cart))
    container_right.bind("<Leave>", lambda e: canvas_cart.unbind_all("<MouseWheel>"))

    return cart_grid_frame

    # ฟังก์ชัน Scroll wheel เฉพาะฝั่งรถเข็น
    def _on_mousewheel_cart(event):
        canvas_cart.yview_scroll(int(-1*(event.delta/120)), "units")
    
    # ผูกเหตุการณ์เมื่อเมาส์ "เข้า" มาในพื้นที่ฝั่งขวาเท่านั้น
    container_right.bind("<Enter>", lambda e: canvas_cart.bind_all("<MouseWheel>", _on_mousewheel_cart))
    container_right.bind("<Leave>", lambda e: canvas_cart.unbind_all("<MouseWheel>"))

    return cart_grid_frame # ส่งค่า Frame นี้ออกไปเพื่อให้ open_amount_window รู้ว่าต้องวาดที่ไหน
    # ตรงนี้สำคัญ: ตอนสร้าง window ใน canvas ให้ใช้ anchor="nw" (North-West)
    # เพื่อให้ Frame ไปแปะที่มุมบนซ้ายสุดของ Canvas พอดี
    canvas_cart.create_window((0, 0), window=cart_grid_frame, anchor="nw")

# เพิ่มตัวแปรเก็บปุ่มทั้งหมดเพื่อให้ง่ายต่อการค้นหา (วางไว้ด้านบนของไฟล์)
all_products = [] 

def setup_pos_interface(p2, root):
    # 1. สร้าง Container ฝั่งซ้าย
    container_left = tk.Frame(p2, bg="black")
    container_left.place(x=0, y=0, width=690, height=1000)

    # 2. สร้างส่วน Search (ทำแค่ครั้งเดียวตรงนี้)
    search_frame = tk.Frame(container_left, bg="#222")
    search_frame.pack(side="top", fill="x", padx=10, pady=10)
    
    tk.Label(search_frame, text="Search:", fg="white", bg="#222", font=("Arial", 12)).pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, font=("Arial", 14))
    search_entry.pack(side="left", fill="x", expand=True, padx=5)

    # 3. สร้าง Canvas และ Scrollbar สำหรับรายการสินค้า
    canvas_menu = tk.Canvas(container_left, bg="black", highlightthickness=0)
    scrollbar_menu = tk.Scrollbar(container_left, orient="vertical", command=canvas_menu.yview)
    canvas_menu.configure(yscrollcommand=scrollbar_menu.set)
    scrollbar_menu.pack(side="right", fill="y")
    canvas_menu.pack(side="left", fill="both", expand=True)

    # 4. สร้าง Frame สำหรับวางปุ่มสินค้าด้านใน Canvas
    menu_frame = tk.Frame(canvas_menu, bg="black")
    canvas_menu.create_window((0, 0), window=menu_frame, anchor="nw")

    # 5. ตั้งค่าการ Scroll
    menu_frame.bind("<Configure>", lambda e: canvas_menu.configure(scrollregion=canvas_menu.bbox("all")))
    
    def _on_mousewheel_menu(event):
        canvas_menu.yview_scroll(int(-1*(event.delta/120)), "units")
    
    container_left.bind("<Enter>", lambda e: canvas_menu.bind_all("<MouseWheel>", _on_mousewheel_menu))
    container_left.bind("<Leave>", lambda e: canvas_menu.unbind_all("<MouseWheel>"))

    # 6. เชื่อมระบบ Search เข้ากับปุ่ม (ส่ง canvas_menu ไปด้วยเพื่อให้ Scroll ทำงาน)
    search_entry.bind("<KeyRelease>", lambda e: generate_buttons(root, p2, menu_frame, search_entry.get(), canvas_menu))

    # 7. โหลดปุ่มครั้งแรก
    generate_buttons(root, p2, menu_frame, "", canvas_menu)
    
    return menu_frame

# ฟังก์ชันกรองปุ่ม
def filter_buttons(query, target_frame, root, p2):
    # ลบปุ่มเก่าออกให้หมดก่อน
    for widget in target_frame.winfo_children():
        widget.destroy()
    
    # สร้างปุ่มใหม่ตามคำค้นหา
    generate_buttons(root, p2, target_frame, search_query=query)

# --- ปรับปรุงฟังก์ชันสร้างปุ่ม ---
def generate_buttons(root, p2, target_frame, search_query="", canvas=None):
    # ลบปุ่มเก่าออกก่อนสร้างใหม่ (สำคัญมาก)
    for widget in target_frame.winfo_children():
        widget.destroy()

    try:
        with open('Inventory.txt', 'r', encoding='utf-8') as f:
            display_index = 0  # ใช้ตัวนับนี้เพื่อวาง Grid ให้เรียงกันสวยงาม
            for line in f:
                data = [item.strip() for item in line.split(',')]
                if len(data) < 4: continue
                
                p_name = data[1]
                p_price = data[3]

                # --- ส่วนเช็คการค้นหา ---
                # ถ้าพิมพ์ค้นหา แล้วชื่อสินค้าไม่มีคำนั้น ให้ข้ามไป (ตัวเล็กตัวใหญ่ไม่มีผล)
                if search_query.lower() not in p_name.lower():
                    continue

                # คำนวณตำแหน่ง Grid (4 คอลัมน์)
                row_pos = display_index // 4
                col_pos = display_index % 4
                
                btn = tk.Button(
                    target_frame, 
                    text=f"{p_name}\n({p_price}฿)", 
                    width=21, 
                    height=10,
                    command=lambda n=p_name, p=p_price: open_amount_window(root, n, p, p2)
                )
                btn.grid(row=row_pos, column=col_pos, padx=5, pady=5)
                display_index += 1

        # --- ส่วนสำคัญ: อัปเดตการเลื่อนหน้าจอ ---
        if canvas:
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

    except FileNotFoundError:
        tk.Label(target_frame, text="ไม่พบไฟล์ Inventory.txt", fg="white", bg="black").grid()
# --- ปรับปรุงฟังก์ชันยืนยันค่า ---
# (หมายเหตุ: คุณต้องสร้าง cart_frame ทิ้งไว้ใน p2 เพื่อให้ฟังก์ชันนี้เรียกใช้ได้)
cart_frame_ref = None

# สร้างตัวแปรเก็บ Label ราคาไว้เพื่ออัปเดตภายหลัง
total_label_ref = None 
current_total_sum = 0.0

def process_payment():
    global current_total_sum, row_bill, last_pos, cart_frame_ref, total_label_ref
    file_name = "Bill.txt"
    
    if os.path.exists(file_name):
        try:
            # 1. ลบไฟล์ Bill.txt
            os.remove(file_name)
            
            # 2. แจ้งเตือนผู้ใช้
            messagebox.showinfo("DevCat", "ชำระเงินเสร็จสิ้น!")

            # 3. รีเซ็ตตัวแปรทางบัญชีให้เป็น 0
            current_total_sum = 0.0
            row_bill = 1  # เริ่มนับแถวใหม่ (เว้นแถว 0 ที่เป็น Header)
            last_pos = 0  # รีเซ็ตตำแหน่งการอ่านไฟล์

            # 4. อัปเดตตัวเลขราคารวมบนหน้าจอให้เป็น 0.00
            if total_label_ref:
                total_label_ref.config(text="0.00 ฿")

            # 5. ล้างรายการสินค้าในรถเข็น (ลบ Widget ลูกทั้งหมดใน cart_frame_ref)
            if cart_frame_ref:
                for widget in cart_frame_ref.winfo_children():
                    # ตรวจสอบเพื่อไม่ให้ลบ Header (Product, Amount, Price) 
                    # ถ้าคุณใช้ grid(row=0) สำหรับ Header เราจะลบเฉพาะ row > 0
                    info = widget.grid_info()
                    if int(info.get("row", 0)) > 0:
                        widget.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")
    else:
        messagebox.showwarning("DevCat", "ไม่มีรายการสินค้าให้ชำระเงิน")

def setup_total_price_interface(p2):
    global total_label_ref
    show_price_frame = tk.Frame(p2, bg="white") 
    show_price_frame.place(x=1390, y=0, width=522, height=1000)
    
    tk.Label(show_price_frame, text="Total Price", font=("Arial", 25, "bold"), bg="white").pack(pady=20)
    
    # สร้าง Label เปล่ารอไว้ และเก็บ Reference ไว้ในตัวแปร global
    total_label_ref = tk.Label(show_price_frame, text="0.00 ฿", font=("Arial", 40), fg="white", bg="red", width=15)
    total_label_ref.pack(pady=20)
    
    # tk.Label(show_price_frame, text="Vat 7% : 0.00 ฿", font=("Arial", 25, "bold"), bg="white").pack(pady=20)
    
    # เพิ่มปุ่ม Hold
    bthold = tk.Button(show_price_frame, text="Hold Bill", command=hold_bill, font=("Arial", 15), bg="orange", fg="black", width=20, height=2)
    bthold.pack(pady=10)

    # เพิ่มปุ่ม Recall
    btrecall = tk.Button(show_price_frame, text="Recall Bill", command=recall_bill, font=("Arial", 15), bg="blue", fg="white", width=20, height=2)
    btrecall.pack(pady=10)
    
    # ปุ่ม Clear Cart (เพิ่มใหม่)
    tk.Button(show_price_frame, text="Clear Cart", command=clear_cart, font=("Arial", 15), bg="#777777", fg="white", width=20, height=2).pack(pady=5)
    
    btpay = tk.Button(show_price_frame, text="Payment", command=lambda: process_payment(), font=50, bg="green", fg="white", width=50, height=10)
    btpay.pack(pady=(300, 0)) # ใช้ pady เพื่อดันจากข้างบนลงมา 200 พิกเซล
    
    return show_price_frame

# เพิ่ม p_price เข้ามาเป็น parameter
def open_amount_window(root, product_name, p_price, p2):
    global cart_frame_ref
    window_select = tk.Toplevel(root) 
    window_select.title("DevCat")
    window_select.geometry("400x200+750+300")
    
    tk.Label(window_select, text= product_name, font=20).pack(pady=5)
    tk.Label(window_select, text= p_price).pack()
    
    count_product = tk.Entry(window_select)
    count_product.pack(pady=5)

    def confirm_value():
        global last_pos, row_bill, cart_frame_ref, current_total_sum, total_label_ref
        raw_value = count_product.get()
        if not raw_value: return 
        
        file_name = "Bill.txt"
        # บันทึก 3 อย่าง: ชื่อ, จำนวน, ราคา
        with open(file_name, "a", encoding="utf-8") as o:
            o.write(product_name + "\n")
            o.write(raw_value + "\n")
            o.write(p_price + "\n") # เพิ่มการบันทึกราคาลงไฟล์ Bill

        with open(file_name, 'r', encoding='utf-8') as f:
            f.seek(last_pos)
            # อ่านข้อมูลที่เพิ่งเขียน (คราวนี้จะมาทีละ 3 บรรทัด)
            new_data = [line.strip() for line in f.readlines() if line.strip()]
            
            # วนลูปทีละ 3 ค่า (ชื่อ, จำนวน, ราคา)
            for i in range(0, len(new_data), 3):
                if i + 2 < len(new_data):
                    name = new_data[i]
                    amount = new_data[i+1]
                    price = new_data[i+2]
                    
                    # คำนวณราคารวม (ถ้าต้องการ)
                    total_item_price = float(price) * int(amount)

                    # คำนวณราคารวมสะสม
                    item_total = float(price) * int(amount)
                    current_total_sum += item_total
                    
                    # อัปเดตตัวเลขบนหน้าจอทันที
                    if total_label_ref:
                        total_label_ref.config(text=f"{current_total_sum:,.2f} ฿")

                    # --- แสดงผล 3 คอลัมน์ ---
                    # Col 0: ชื่อสินค้า
                    tk.Label(cart_frame_ref, text = name, font=("Arial", 16), bg="red", width=20, height=2, anchor="w").grid(row=row_bill, column=0, sticky="w", padx=10, pady=5)
                    
                    # Col 1: จำนวน
                    tk.Label(cart_frame_ref, text = amount, font=("Arial", 16), bg="red", width=8, height=2).grid(row=row_bill, column=1, padx=10, pady=5)
                    
                    # Col 2: ราคา (แสดงราคารวมของรายการนั้น)
                    tk.Label(cart_frame_ref, text = f"{total_item_price:.2f}", font=("Arial", 16), bg="red", fg="green", width=13, height=2, anchor="e").grid(row=row_bill, column=2, sticky="e", padx=10, pady=5)
                    
                    row_bill += 1
            
            last_pos = f.tell()
        window_select.destroy()
    tk.Button(window_select, text="Confirm", command=confirm_value, width=10).pack(pady=10)
    

def hold_bill():
    global current_total_sum, row_bill, last_pos
    source_file = "Bill.txt"

    if os.path.exists(source_file):
        # สร้างชื่อไฟล์จาก วันที่และเวลาปัจจุบัน
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        hold_file_path = os.path.join(HOLD_DIR, f"Bill_{file_timestamp}.txt")

        os.rename(source_file, hold_file_path) # ย้ายไฟล์ไปที่โฟลเดอร์ hold
        
        # ล้างหน้าจอรถเข็น
        current_total_sum = 0.0
        row_bill = 1
        last_pos = 0
        total_label_ref.config(text="0.00 ฿")
        for widget in cart_frame_ref.winfo_children():
            if int(widget.grid_info().get("row", 0)) > 0:
                widget.destroy()
        
        messagebox.showinfo("Hold Bill", f"พักบิลเรียบร้อยแล้วเมื่อ:\n{timestamp}")
    else:
        messagebox.showwarning("Hold Bill", "ไม่มีรายการให้พัก")

def recall_bill():
    global current_total_sum, row_bill, last_pos, cart_frame_ref
    
    # ตรวจสอบก่อนว่าปัจจุบันมีบิลค้างหน้าจอไหม
    if os.path.exists("Bill.txt") or current_total_sum > 0:
        messagebox.showwarning("Recall Bill", "กรุณาจัดการบิลปัจจุบันก่อนเรียกคืนบิลอื่น")
        return

    # ดึงรายชื่อไฟล์ในโฟลเดอร์ hold
    files = [f for f in os.listdir(HOLD_DIR) if f.endswith('.txt')]
    if not files:
        messagebox.showwarning("Recall Bill", "ไม่มีบิลที่พักไว้")
        return

    # สร้างหน้าต่างเลือกบิล
    recall_window = tk.Toplevel()
    recall_window.title("Choice Bill to Recall")
    recall_window.geometry("400x400")

    tk.Label(recall_window, text="Bill Hold", font=("Arial", 14, "bold")).pack(pady=10)

    # สร้าง Listbox แสดงรายการ
    lb = tk.Listbox(recall_window, font=("Arial", 12), width=40)
    lb.pack(padx=20, pady=10, expand=True, fill="both")

    # แปลงชื่อไฟล์กลับเป็นวันเวลาให้อ่านง่าย
    for f in files:
        # สมมติชื่อไฟล์คือ Bill_20231027_143005.txt
        display_name = f.replace("Bill_", "").replace(".txt", "")
        lb.insert("end", display_name)

    def select_and_recall():
        global current_total_sum, row_bill, last_pos
        selection = lb.curselection()
        if selection:
            filename = files[selection[0]]
            full_path = os.path.join(HOLD_DIR, filename)
            
            # ย้ายกลับมาเป็น Bill.txt
            os.rename(full_path, "Bill.txt")
            
            # วาดหน้าจอใหม่
            refresh_cart_display()
            recall_window.destroy()
            messagebox.showinfo("Success", "เรียกคืนบิลสำเร็จ")

    tk.Button(recall_window, text="OK", command=select_and_recall, 
              bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

# ฟังก์ชันช่วยวาดหน้าจอใหม่หลังจากเรียกคืนบิล
def refresh_cart_display():
    global current_total_sum, row_bill, last_pos
    file_name = "Bill.txt"
    
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
            for i in range(0, len(lines), 3):
                name = lines[i]
                amount = lines[i+1]
                price = lines[i+2]
                
                total_item_price = float(price) * int(amount)
                current_total_sum += total_item_price
                
                # วาดลง Grid (Copy logic จาก confirm_value มา)
                tk.Label(cart_frame_ref, text=name, font=("Arial", 16), bg="red", width=20, height=2, anchor="w").grid(row=row_bill, column=0, sticky="w", padx=10, pady=5)
                tk.Label(cart_frame_ref, text=amount, font=("Arial", 16), bg="red", width=8, height=2).grid(row=row_bill, column=1, padx=10, pady=5)
                tk.Label(cart_frame_ref, text=f"{total_item_price:.2f}", font=("Arial", 16), bg="red", fg="green", width=13, height=2, anchor="e").grid(row=row_bill, column=2, sticky="e", padx=10, pady=5)
                
                row_bill += 1
            
            total_label_ref.config(text=f"{current_total_sum:,.2f} ฿")
            last_pos = f.tell()

def clear_cart():
    global current_total_sum, row_bill, last_pos, cart_frame_ref, total_label_ref
    file_name = "Bill.txt"
    
    # ถามเพื่อความแน่ใจก่อนลบ
    if not os.path.exists(file_name) and current_total_sum == 0:
        messagebox.showwarning("Clear Cart", "ไม่มีรายการสินค้าในรถเข็น")
        return

    confirm = messagebox.askyesno("Confirm Clear", "คุณต้องการล้างรายการทั้งหมดในรถเข็นใช่หรือไม่?")
    
    if confirm:
        try:
            # 1. ลบไฟล์ทิ้ง
            if os.path.exists(file_name):
                os.remove(file_name)
            
            # 2. รีเซ็ตตัวแปร
            current_total_sum = 0.0
            row_bill = 1
            last_pos = 0
            
            # 3. ล้างหน้าจอ UI
            if total_label_ref:
                total_label_ref.config(text="0.00 ฿")
            
            if cart_frame_ref:
                for widget in cart_frame_ref.winfo_children():
                    info = widget.grid_info()
                    if int(info.get("row", 0)) > 0:
                        widget.destroy()
            
            messagebox.showinfo("Clear Cart", "ล้างรถเข็นเรียบร้อยแล้ว")
            
        except Exception as e:
            messagebox.showerror("Error", f"ไม่สามารถล้างรถเข็นได้: {e}")

def on_closing(root):
    file_name = "Bill.txt"
    # ถ้ามีไฟล์ Bill.txt ค้างอยู่ ให้ลบทิ้งก่อนปิด
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
        except Exception as e:
            print(f"Error deleting file on close: {e}")
    
    # ปิดหน้าต่างโปรแกรม
    root.destroy()