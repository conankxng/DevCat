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
    
    tk.Label(form_frame, text='ระบบจัดการคลังสินค้า (Inventory)', font=header_font,bg='#f0f0f0').pack(pady=20)