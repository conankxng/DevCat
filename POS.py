import tkinter as tk
import os

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


def total_show_price(p2):
    show_price = tk.Frame(p2, bg="white") 
    show_price.place(x=1390, y=0, width=522, height=1000)
    tk.Label(show_price, text="Total Price", font=("Arial", 20), bg="white").pack(pady=20)
    tk.Label(show_price, text="Total Price", font=("Arial", 10), fg="white", bg="red").pack(pady=20)




# --- ปรับปรุงฟังก์ชันสร้างปุ่ม ---
def generate_buttons(root, p2, target_frame):
    try:
        with open('Inventory.txt', 'r', encoding='utf-8') as f:
            for index, line in enumerate(f):
                data = [item.strip() for item in line.split(',')]
                if len(data) < 4: continue # เช็คว่ามีข้อมูลครบ (ID, Name, Qty, Price)
                
                p_name = data[1]
                p_price = data[3] # ดึงราคา (ตำแหน่งที่ 4 หรือ index 3)
                
                row_pos = index // 4
                col_pos = index % 4
                
                btn = tk.Button(
                    target_frame, 
                    text=f"{p_name}\n({p_price}฿)", # แสดงราคาบนปุ่มด้วย
                    width=21, 
                    height=10,
                    # ส่ง p_price เพิ่มเข้าไปในฟังก์ชัน
                    command=lambda n=p_name, p=p_price: open_amount_window(root, n, p, p2)
                )
                btn.grid(row=row_pos, column=col_pos, padx=5, pady=5)
    except FileNotFoundError:
        tk.Label(target_frame, text="ไม่พบไฟล์ Inventory.txt", fg="white", bg="black").grid()

# --- ปรับปรุงฟังก์ชันยืนยันค่า ---
# (หมายเหตุ: คุณต้องสร้าง cart_frame ทิ้งไว้ใน p2 เพื่อให้ฟังก์ชันนี้เรียกใช้ได้)
cart_frame_ref = None

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
        global last_pos, row_bill, cart_frame_ref
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