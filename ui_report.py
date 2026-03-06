import tkinter as tk
from tkinter import ttk, messagebox
import report

#ฟังก์ชันสำหรับสร้างหน้าต่าง Reportโดยแสดงผลใน (p3)
def setup_Report_interface(parent): 

    default_font = ("Kanit", 12)  #เก็บตัวแปรฟอนต์แบบปกติ
    bold_font = ("Kanit", 14, "bold") #เก็บตัวแปรฟอนต์แบบตัวหนา


    mian_frame = tk.Frame(parent,background="#FF9EE4") #สร้างเฟรมหลักไว้นอกสุด
    revenue_frame = tk.Frame(parent, background="#FF9EE4")
    revenue_frame

