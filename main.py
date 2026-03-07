import tkinter as tk
import POS
import os
from tkinter import messagebox  # ต้องเพิ่มบรรทัดนี้เพื่อใช้การแจ้งเตือน
import customtkinter as ctk
from PIL import Image

class AppState:
    current_page = None
    is_animating = False
    loading_frame = None
    progress_bar = None

def init_loading_screen(parent):
    AppState.loading_frame = ctk.CTkFrame(parent, fg_color="#191919", width=1920, height=960)
    AppState.loading_frame.place(x=0, y=90)
    
    inner_frame = ctk.CTkFrame(AppState.loading_frame, fg_color="transparent")
    inner_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    lbl = ctk.CTkLabel(inner_frame, text="กำลังเตรียมข้อมูล...", font=("Kanit", 50, "bold"), text_color="white")
    lbl.pack(pady=(0, 20))
    
    AppState.progress_bar = ctk.CTkProgressBar(inner_frame, width=500, mode="indeterminate", progress_color="#1e683e")
    AppState.progress_bar.pack(pady=20)

#ฟังก์ชันสลับหน้าตอนโหลดข้อมูล
def switch(page):
    if AppState.is_animating or AppState.current_page == page:
        return
        
    if AppState.loading_frame is None:
        page.tkraise()
        AppState.current_page = page
        return

    AppState.is_animating = True
    AppState.loading_frame.tkraise()
    AppState.progress_bar.start()
    
    def finish_switch():
        AppState.progress_bar.stop()
        page.tkraise()
        AppState.current_page = page
        AppState.is_animating = False
        
    root.after(1500, finish_switch)

def on_closing():
    root.destroy()

root = tk.Tk()
root.title("DevCat")
root.geometry("1920x1080")

header = ctk.CTkFrame(root, height=90, fg_color="#FFFFFF")
header.pack(fill=ctk.X)
# 1. ตั้งค่าให้ header กระจายน้ำหนักทั้งแนวตั้ง (Row) และแนวนอน (Column)
header.grid_rowconfigure(0, weight=1, minsize=80)    # ทำให้แถวที่ 0 ขยายความสูงได้
header.grid_columnconfigure(0, weight=1) # แบ่ง 3 คอลัมน์เท่าๆ กัน
header.grid_columnconfigure(1, weight=1)
header.grid_columnconfigure(2, weight=1)

in_header_left = ctk.CTkFrame(header, fg_color="#FFFFFF") #สร้างเฟรมย่อยใน header เพื่อแยกส่วนซ้ายและขวา
in_header_left.grid(row=0, column=0, sticky="nsew")

try:
    raw_img_logo = Image.open("img/Logo_devcat.png")
    # แนะนำให้ตั้ง size ให้เท่ากับขนาดของ left_panel หรือใหญ่พอที่จะคลุมพื้นที่
    image_logo = ctk.CTkImage(light_image=raw_img_logo, dark_image=raw_img_logo, size=(200, 50)) 
    img_logo = ctk.CTkLabel(in_header_left, image=image_logo, text="") 
    img_logo.place(x=20, y=20) 
except Exception as e:
    print(f"Error loading logo: {e}")
    ctk.CTkLabel(in_header_left, text="DevCat Logo", font=("Kanit", 20, "bold")).place(x=20, y=20)

in_header_right = ctk.CTkFrame(header, fg_color="#FFFFFF") #สร้างเฟรมย่อยใน header เพื่อแยกส่วนซ้ายและขวา
in_header_right.grid(row=0, column=1 , sticky="nsew")
in_header_right.grid_columnconfigure(0, weight=1)
in_header_right.grid_columnconfigure(1, weight=1)
in_header_right.grid_columnconfigure(2, weight=1)

ctk.CTkButton(in_header_right, text="Inventory", 
              command=lambda: switch(p1), 
              font=("Kanit", 30, "bold"),
              height=70,
              fg_color="#FFFFFF",
              hover_color="#fffbee",
              text_color="#1e683e",
              border_width=2,
              border_color="#1e683e",
              corner_radius=10).grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

ctk.CTkButton(in_header_right, text="POS", 
              command=lambda: switch(p2), 
              font=("Kanit", 30, "bold"),
              height=70,
              fg_color="#FFFFFF",
              hover_color="#fffbee",
              text_color="#1e683e",
              border_width=2,
              border_color="#1e683e",
              corner_radius=10).grid(row=0, column=1, sticky="nsew", padx=10, pady=(10, 5))

ctk.CTkButton(in_header_right, text="Dashboard", 
              command=lambda: switch(p3), 
              font=("Kanit", 30, "bold"), 
              height=70, 
              fg_color="#FFFFFF",
              hover_color="#fffbee",
              text_color="#1e683e",
              border_width=2,
              border_color="#1e683e",
              corner_radius=10).grid(row=0, column=2, sticky="nsew", padx=10, pady=(10, 5))

main = tk.Frame(root, bg='red') #สร้างหน้าเข้าไปใน root และเปลี่ยนสี Bg
main.place(x=0, y=90, width=1920, height=960) #วางแบบกำหนดค่าเองคือ แกน x และ y พร้อมกำหนดขนาด

"""
ส่วนของ เนส Inventory
"""
# Inventory = p1
p1 = tk.Frame(root, bg='red') #สร้างหน้าเข้าไปใน root และเปลี่ยนสี Bg
p1.place(x=0, y=90, width=1920, height=960) #วางแบบกำหนดค่าเองคือ แกน x และ y พร้อมกำหนดขนาด
import ui_inventory #ดึงข้อมูลมา
ui_inventory.setup_inventory_interface(p1) #เรียกดึง GUI ของ inventory มาแสดงในส่วนของ P1 พารามิตเตอร์
"""
อนุพงค์ พลจันทึก 681310024
"""


"""
ส่วนของ อุ้ม POS
"""
p2 = tk.Frame(root, bg="#191919") #สร้างหน้าเข้าไปใน root และเปลี่ยนสี Bg
p2.place(x=0, y=90, width=1920, height=960) #วางแบบกำหนดค่าเองคือ แกน x และ y พร้อมกำหนดขนาด

POS.create_three_frames(p2) # เรียกใช้ฟังก์ชันสร้าง 3 เฟรมใน POS เพื่อเตรียมพื้นที่สำหรับแสดงข้อมูลต่างๆ

"""
อภิรักษ์ ธรรมแก้ว 681310025
"""


"""
ส่วนของ เบนโตะ Dashboard
"""
p3 = tk.Frame(root, bg='blue') #สร้างหน้าเข้าไปใน root และเปลี่ยนสี Bg
p3.place(x=0, y=90, width=1920, height=960) #วางแบบกำหนดค่าเองคือ แกน x และ y พร้อมกำหนดขนาด
import ui_report
ui_report.create_report_ui(p3) #เรียกใช้ฟังก์ชันสร้าง UI
"""
กัญญ์กณิษฐ์ เชื้อฉลาด  681310001
"""



# สร้างหน้าโหลดให้เรียบร้อยก่อนโชว์หน้าแรก
init_loading_screen(root)

#เริ่มต้นให้หน้า 1 อยู่บนสุด
switch(main)


# สมมติว่า root คือชื่อตัวแปรหน้าต่างหลักของคุณ
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()



