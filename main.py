import tkinter as tk
import POS
import os
from tkinter import messagebox  # ต้องเพิ่มบรรทัดนี้เพื่อใช้การแจ้งเตือน

#ฟังก์ชันสลับหน้า
def switch(page):
    page.tkraise()

def on_closing():
    root.destroy()

root = tk.Tk()
root.title("DevCat")
# วิธีที่ 2: ดึงค่าขนาดหน้าจอผู้ใช้มาคำนวณ (Responsive)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#root.geometry("1920x1080")
# ตั้งค่าให้เล็กลงกว่าหน้าจอผู้ใช้เล็กน้อย (เช่น 90% ของหน้าจอ) เพื่อไม่ให้ล้น
root.geometry(f"{int(screen_width*0.9)}x{int(screen_height*0.9)}")




#สร้างปุ่มเมนู
tk.Button(root, text="Inventory", command=lambda: switch(p1), font=("Kanit", 18)).grid(row=0, column=0)
tk.Button(root, text="POS", command=lambda: switch(p2), font=("Kanit", 18)).grid(row=0, column=1)
tk.Button(root, text="Report", command=lambda: switch(p3), font=("Kanit", 18)).grid(row=0, column=2)
#สร้างหน้า



"""
ส่วนของ เนส Inventory
"""
# Inventory = p1
p1 = tk.Frame(root, bg='red') #สร้างหน้าเข้าไปใน root และเปลี่ยนสี Bg
p1.place(x=0, y=90, width=1920, height=1000) #วางแบบกำหนดค่าเองคือ แกน x และ y พร้อมกำหนดขนาด
import ui_inventory #ดึงข้อมูลมา
ui_inventory.setup_inventory_interface(p1) #เรียกดึง GUI ของ inventory มาแสดงในส่วนของ P1 พารามิตเตอร์
"""
อนุพงค์ พลจันทึก 681310024
"""


"""
ส่วนของ อุ้ม POS
"""
p2 = tk.Frame(root, bg='green') #สร้างหน้าเข้าไปใน root และเปลี่ยนสี Bg
p2.place(x=0, y=90, width=1920, height=1000) #วางแบบกำหนดค่าเองคือ แกน x และ y พร้อมกำหนดขนาด

POS.create_three_frames(p2) #เรียกใช้ฟังก์ชันสร้าง 3 เฟรมใน POS เพื่อเตรียมพื้นที่สำหรับแสดงข้อมูลต่างๆ
"""
อภิรักษ์ ธรรมแก้ว 681310025
"""


"""
ส่วนของ เบนโตะ Report
"""
p3 = tk.Frame(root, bg='blue') #สร้างหน้าเข้าไปใน root และเปลี่ยนสี Bg
p3.place(x=0, y=90, width=1920, height=1000) #วางแบบกำหนดค่าเองคือ แกน x และ y พร้อมกำหนดขนาด
import ui_report
ui_report.setup_Report_interface(p3)
"""
กัญญ์กณิษฐ์ เชื้อฉลาด  681310001
"""



#เริ่มต้นให้หน้า 1 อยู่บนสุด
switch(p1)


# สมมติว่า root คือชื่อตัวแปรหน้าต่างหลักของคุณ
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()



