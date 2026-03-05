from turtle import width
import tkinter as tk
from tkinter import messagebox
import os
import product_manager#==================================================================#
#------------------------------Create Frame-------------------------------
#==================================================================#
def create_scrollable_frame(parent):
    """ฟังก์ชันช่วยสร้างเฟรมที่สามารถเลื่อนได้"""
    # สร้างกรอบนอก (Container)
    container = tk.Frame(parent,)
    
    # สร้าง Canvas เพื่อให้เนื้อหาข้างในขยับได้เพราะ Frame ไม่รองรับการเลื่อนเมาส์
    canvas = tk.Canvas(container, highlightthickness=0)
    
    # สร้าง Scrollbar แนวตั้ง ไว้ทางขวามือ
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    
    # สร้างเฟรมด้านใน เอาไว้ใส่ content อีกทีนึง
    inner_frame = tk.Frame(canvas)
    
    # ฟังก์ชันสำหรับอัปเดตพื้นที่เลื่อนทุกครั้งที่ inner_frame มีการเปลี่ยนแปลงเนื้อหา
    inner_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # วาง inner_frame ลงไปใน canvas
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # ความสามารถเสริม ให้ canvas กว้างพอดีกรอบตลอดเวลา
    def configure_canvas_width(event):
        canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
    canvas.bind("<Configure>", configure_canvas_width)
    
    # ทำให้เมาส์วีลเลื่อนหน้าจอได้ โดยสามารถเลื่อนขึ้นได้เฉพาะตอนที่ยังไม่ถึงบนสุด และเลื่อนลงได้เฉพาะตอนที่ยังไม่ถึงล่างสุด
    def _on_mousewheel(event):
        # โดยปกติ
        # canvas.yview() คืนค่ามาเป็น tuple (top_fraction, bottom_fraction) เช่น (0.0, 0.5)
        # ถ้า top_fraction == 0.0 แปลว่าอยู่บนสุดแล้ว ถ้า bottom_fraction == 1.0 แปลว่าอยู่ล่างสุดแล้ว
        top, bottom = canvas.yview()
        
        # เลื่อนขึ้น (event.delta > 0)
        if event.delta > 0:
            if top > 0.0: # เลื่อนขึ้นได้เฉพาะตอนที่ยังไม่ถึงบนสุด
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        # เลื่อนลง (event.delta < 0)
        elif event.delta < 0:
            if bottom < 1.0: # เลื่อนลงได้เฉพาะตอนที่ยังไม่ถึงล่างสุด
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    # ผูกคำสั่งเลื่อนด้วยลูกกลิ้งเมาส์ เมื่อเมาส์เข้ามาในกรอบและยกเลิกเมื่อออกนอกกรอบ
    canvas.bind('<Enter>', lambda _: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind('<Leave>', lambda _: canvas.unbind_all("<MouseWheel>"))

    # จัดวางให้ Canvas อยู่ซ้าย Scrollbar อยู่ขวา
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # คืนค่า container สำหรับจัดวาง และ frame1 (inner_frame) สำหรับนำไปใส่เนื้อหาต่อ
    return container, inner_frame

def create_three_frames(parent):
    """
    ฟังก์ชันสำหรับสร้าง 3 เฟรมภายในหน้าต่างหลัก (parent)
    โดยเฟรมที่ 1 และ 2 เลื่อนได้ ส่วนเฟรมที่ 3 แบบปกติ
    """
    # สร้าง เฟรมที่ 1 (เลื่อนได้)
    # คืนค่า container สำหรับจัดวาง และ frame1 (inner_frame) สำหรับนำไปใส่เนื้อหาต่อ
    container1, frame1 = create_scrollable_frame(parent)
    container1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    load_products_to_frame(frame1) #เรียกใช้ฟังก์ชันโหลดสินค้าไปแสดงใน frame1
    
    # สร้าง เฟรมที่ 2 (เลื่อนได้)
    container2, frame2 = create_scrollable_frame(parent)
    container2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    
    # สร้าง เฟรมที่ 3 (แบบปกติ เลื่อนไม่ได้)
    frame3 = tk.Frame(parent)
    frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    
    # คืนค่า frame1, frame2, frame3 ให้เสมือนว่าเป็น Frame ปกติสำหรับใส่เนื้อหาอื่นๆ
    return frame1, frame2, frame3

#==================================================================#
#------------------------------Frame1-------------------------------
#==================================================================#
# ตัวแปร Global สำหรับเก็บค่า ID และชื่อสินค้าที่ถูกเลือกคลิกล่าสุด
current_selected_product = {"id": None, "name": None}

def load_products_to_frame(frame):
    """ฟังก์ชันสำหรับอ่านไฟล์ products.txt และสร้างปุ่มสินค้า"""
    # กำหนด path ของไฟล์ products.txt
    file_path = os.path.join(os.path.dirname(__file__), "data", "products.txt")
    
    # จัดเรียงน้ำหนัก (weight) ให้ 4 คอลัมน์ขยายตัวเท่าๆ กัน
    for col_index in range(4):
        frame.columnconfigure(col_index, weight=1)
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        button_count = 0  # ตัวนับจำนวนปุ่มที่ถูกสร้าง
        for line in lines:
            line = line.strip()
            if not line:
                continue # ข้ามบรรทัดว่าง
                
            # แยกข้อมูลด้วยคอมม่า: "001,cake,0,50.0,35.0"
            parts = line.split(",")
            if len(parts) >= 2:
                product_id = parts[0]
                product_name = parts[1]
                
                # กำหนดฟังก์ชันย่อยสำหรับการกดปุ่ม
                def on_product_click(p_id=product_id, p_name=product_name):
                    global current_selected_product
                    # เก็บค่า id และชื่อสินค้าไว้ในตัวแปร global
                    current_selected_product["id"] = p_id
                    current_selected_product["name"] = p_name
                    print(f"Stored -> ID: {p_id}, Name: {p_name}")
                    
                    # เรียกเปิดหน้าพ็อปอัพ Numpad
                    open_numpad_popup(frame)
                
                # สร้างปุ่มโดยแสดงชื่อสินค้า (product_name)
                btn = tk.Button(
                    frame, 
                    text=product_name, 
                    font=("Arial", 10),
                    height=8,
                    command=on_product_click
                )
                btn.place(relwidth=1, relheight=1)  # ให้ปุ่มขยายเต็มความกว้างและสูงของกริดคอลัมน์
                
                # คำนวณแถวและคอลัมน์จากตัวนับ (4 ปุ่มต่อแถว)
                row = int(button_count / 4)
                col = button_count % 4  # type: ignore
                
                # วางปุ่มแบบ Grid (ตาราง) โดยเว้นระยะห่างด้านนอก (padx, pady) และขยายปุ่มให้เต็มกริดตารางช่องนั้นๆ (sticky="nsew")
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                
                button_count = button_count + 1
                
    except FileNotFoundError:
        tk.Label(frame, text="⚠️ ไม่พบไฟล์ data/products.txt", fg="red").grid(row=0, column=0, columnspan=4, pady=20)
        
def open_numpad_popup(parent):
    """ฟังก์ชันเปิดหน้าต่าง Numpad (ป๊อปอัป) เพื่อกรอกจำนวนสินค้า"""
    popup = tk.Toplevel(parent)
    popup.title("Amount Products")
    popup.geometry("300x420+1000+200")  # กำหนดขนาดและตำแหน่งของหน้าต่าง
    
    # ล็อคหน้าต่างนี้ไว้ด้านหน้าสุด จนกว่าจะกดยกเลิกหรือตกลง
    popup.grab_set()
    popup.transient(parent)
    popup.focus_force()
    
    # ตัวแปรแสดงจำนวนบนหน้าจอ
    qty_var = tk.StringVar(value="0")  # เริ่มต้นที่ 0 หรือตามที่ต้องการ
    
    # จอแสดงตัวเลข
    display = tk.Label(popup, textvariable=qty_var, font=("Arial", 28, "bold"), bg="white", relief="sunken", anchor="e")
    display.pack(fill=tk.X, padx=10, pady=10, ipady=10)
    
    # เฟรมสำหรับปุ่มตัวเลข 1-9
    keypad_frame = tk.Frame(popup)
    keypad_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
    
    # จัดการน้ำหนักแถวและคอลัมน์ของแป้นพิมพ์ให้ขยายเท่าๆ กัน
    for i in range(3):
        keypad_frame.columnconfigure(i, weight=1)
    for i in range(4):
        keypad_frame.rowconfigure(i, weight=1)
        
    def btn_press(key):
        current = str(qty_var.get())
        if key == "C":
            qty_var.set("0") # รีเซ็ตกลับเป็น 0
        elif key == "<-":
            # ลบตัวเลขท้ายสุด
            length = len(current)
            new_val = current[0:length-1] if length > 0 else ""
            qty_var.set(new_val if new_val else "0")
        else:
            # พิมพ์ตัวเลขต่อท้าย
            if current == "0" or current == "1":
                # ถ้าเป็น 0 หรือ 1 (ค่าเริ่มต้น) ให้ลองพิจารณาพิมพ์ทับถ้าเดิมเป็น 0
                if current == "0":
                    qty_var.set(key)
                else:
                    qty_var.set(current + key)
            else:
                qty_var.set(current + key)

    def create_btn_command(k):
        # Closure เพื่อให้ปุ่มจำค่าตัวแปร k ของตัวเอง
        return lambda: btn_press(k)
        
    # ตำแหน่งของปุ่มบน Numpad
    buttons = [
        ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
        ('C', 3, 0), ('0', 3, 1), ('<-', 3, 2),
    ]
    
    for (text, row, col) in buttons:
        btn = tk.Button(keypad_frame, text=text, font=("Arial", 18, "bold"), command=create_btn_command(text))
        btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
    
    # ฟังก์ชันสำหรับปุ่มยืนยัน (Confirm) ตัดสต็อก
    def submit():
        qty_str = qty_var.get()
        try:
            qty_int = int(qty_str)
        except ValueError:
            qty_int = 0
            
        if qty_int <= 0:
            messagebox.showwarning("แจ้งเตือน", "กรุณาระบุจำนวนมากกว่า 0", parent=popup)
            return
            
        pid = current_selected_product["id"]
        if pid:
            success, msg = product_manager.process_sale(pid, qty_int)
            if success:
                messagebox.showinfo("สำเร็จ", msg, parent=popup)
                popup.destroy()
                # ตรงนี้สามารถใส่โค้ดให้อัปเดตตาราง (Treeview) เพิ่มเข้าไปยังตะกร้าในอนาคตได้
            else:
                messagebox.showwarning("ข้อผิดพลาด", msg, parent=popup)
        else:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบข้อมูลรหัสสินค้าที่เลือก", parent=popup)
            
    # ปุ่มยืนยันด้านล่าง
    submit_btn = tk.Button(popup, text="Confirm", command=submit, font=("Arial", 16, "bold"), bg="green", fg="white")
    submit_btn.pack(fill=tk.X, padx=10, pady=10)
    