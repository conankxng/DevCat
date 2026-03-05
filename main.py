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
root.geometry("1920x1080")

#สร้างปุ่มเมนู
tk.Button(root, text="Inventory", command=lambda: switch(p1), font=50, padx=300, pady=30).grid(row=0, column=0)
tk.Button(root, text="POS", command=lambda: switch(p2), font=50, padx=300, pady=30).grid(row=0, column=1)
tk.Button(root, text="Dashboard", command=lambda: switch(p3), font=50, padx=300, pady=30).grid(row=0, column=2)
#สร้างหน้า
# Inventory = p1
p1 = tk.Frame(root, bg='red') #สร้างหน้าเข้าไปใน root และเปลี่ยนสี Bg
p1.place(x=0, y=90, width=1920, height=1000) #วางแบบกำหนดค่าเองคือ แกน x และ y พร้อมกำหนดขนาด



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
ส่วนของ เบนโตะ Dashboard
"""
p3 = tk.Frame(root, bg='blue') #สร้างหน้าเข้าไปใน root และเปลี่ยนสี Bg
p3.place(x=0, y=90, width=1920, height=1000) #วางแบบกำหนดค่าเองคือ แกน x และ y พร้อมกำหนดขนาด
"""
กัญญ์กณิษฐ์ เชื้อฉลาด  681310001
"""



#เริ่มต้นให้หน้า 1 อยู่บนสุด
switch(p1)


# สมมติว่า root คือชื่อตัวแปรหน้าต่างหลักของคุณ
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()



