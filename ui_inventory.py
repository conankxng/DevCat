import tkinter as tk
from tkinter import ttk, messagebox #ttk คือ widget  messagebox คือหน้าต่างแจ้งเตือนpopup
import product_manager as pm


def setup_inventory_interface(parent):
    """
    ฟังก์ชันหลักสำหรับหน้า GUI คลังสินค้า
    """
    default_font = ("Tahoma", 12)  #เก็บตัวแปรฟอนต์ภาษาไทย
    header_font = ("Tahoma", 14, "bold") #เก็บตัวแปรฟอนต์ภาษาไทยแบบตัวหนา
    
    form_frame = tk.Frame(parent,bg="#f0f0f0",padx=20,pady=20) #กล่อง Frame parentพารามิตเตอร์ที่จะเอา Frame ไปว่างใน Main
    form_frame.place(relwidth=0.3,relheight=1) #.place() ปรับตำแหน่งอิสระ กว้าง 30 สูง 100%
    
    tk.Label(form_frame, text='ระบบจัดการคลังสินค้า (Inventory)', font=header_font,bg='#f0f0f0').pack(pady=20) #สร้างText บอกผู้ใช้ ให้มันแสดงใน form_frame .packให้แสดง padyเว้นระยะห่างส่วนบน 20
    
    def create_input(label_text):
        """
        ฟังก์ชันสร้างช่องกรอกข้อมูล
        """
        frame = tk.Frame(form_frame,bg='#f0f0f0') #สร้างแถวมาอยู่ใน form_frame 
        frame.pack(fill='x',pady=8) #วางแถวนี้ลงบนหน้าจอ และให้ขยายเต็มความกว้าง และเว้นคนสูง 8
        tk.Label(frame, text=label_text, font=default_font, bg='#f0f0f0', width=15,anchor='w').pack(side='left') #สร้างป้ายชื่อ textดึงข้อมูลมาแสดง และชิดซ้าย เพื่อให้ช่องกรอกอยู่บรรทัดเดียว
        entry = tk.Entry(frame, font=default_font) #สร้างช่องไว้สำหรับป้อนข้อมูล
        entry.pack(side='left',fill='x',expand=True) #างช่องกรอกไว้ต่อจากป้ายชื่อ และสั่งให้มันยืดขยายตัว (expand=True) ให้เต็มพื้นที่ที่เหลือในแถวนั้น
        return entry #ส่งค่ากลับไปในฟังก์ชัน
    
    entry_pid = create_input('รหัสสินค้า (ID):') #ส่งค่าไปในฟังก์ชันเพื่อใช้เลือก
    entry_name = create_input('ชื่อสินค้า:')
    entry_price = create_input('ราคาขาย:')
    entry_stock = create_input('จำนวนสต๊อก:')
    entry_cost = create_input('ต้นทุน:')
    
    def clear_form():
        entry_pid.config(state='normal') #คำสั่งให้ปลดล็อค รหัสสิินค้าถึงจะเข้าไปลบข้างในได้
        entry_pid.delete(0, tk.END) #คำสั่งลบข้อความออกจากช่องกรอก 0คือตั้งแต่ตัวแรก end ถึงตัวสุดท้าย
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_stock.delete(0, tk.END)
        entry_cost.delete(0, tk.END)