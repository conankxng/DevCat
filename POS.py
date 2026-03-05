from turtle import width
import tkinter as tk
import os

#==================================================================#
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
def load_products_to_frame(frame):
    """ฟังก์ชันสำหรับอ่านไฟล์ products.txt และสร้างปุ่มสินค้า"""
    # กำหนด path ของไฟล์ products.txt
    file_path = os.path.join(os.path.dirname(__file__), "data", "products.txt")
    
    # จัดเรียงน้ำหนัก (weight) ให้ 4 คอลัมน์ขยายตัวเท่าๆ กัน
    for col_index in range(4):
        frame.columnconfigure(col_index, weight=1)
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        button_count: int = 0  # ตัวนับจำนวนปุ่มที่ถูกสร้าง
        for line in lines:
            line = line.strip()
            if not line:
                continue # ข้ามบรรทัดว่าง
                
            # แยกข้อมูลด้วยคอมม่า: "001,cake,0,50.0,35.0"
            parts = line.split(",")
            if len(parts) >= 2:
                product_id = parts[0]
                product_name = parts[1]
                
                # กำหนดฟังก์ชันย่อย (closure) เพื่อแนบไปกับคำสั่งผูกปุ่ม
                def make_cmd(name=product_name):
                    return lambda: print(f"เลือกสินค้า: {name}")
                
                # สร้างปุ่มโดยแสดงชื่อสินค้า (product_name)
                btn = tk.Button(
                    frame, 
                    text=product_name, 
                    font=("Arial", 10),
                    height=8,
                    command=make_cmd()
                )
                btn.place(relwidth=1, relheight=1)  # ให้ปุ่มขยายเต็มความกว้างและสูงของกริดคอลัมน์
                
                # คำนวณแถวและคอลัมน์จากตัวนับ (4 ปุ่มต่อแถว)
                row = button_count // 4
                col = button_count % 4
                
                # วางปุ่มแบบ Grid (ตาราง) โดยเว้นระยะห่างด้านนอก (padx, pady) และขยายปุ่มให้เต็มกริดตารางช่องนั้นๆ (sticky="nsew")
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                
                button_count += 1
        
