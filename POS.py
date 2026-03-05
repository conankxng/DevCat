import tkinter as tk

def create_frames(parent):
    """
    ฟังก์ชันสำหรับสร้าง 3 เฟรมภายในหน้าต่างหลัก (parent)
    """
    # สร้าง เฟรมที่ 1
    frame1 = tk.Frame(parent, bg="lightblue", width=200, height=200)
    # จัดเรียงเฟรมที่ 1 ไว้ด้านซ้าย ให้ขยายเต็มพื้นที่เมื่อมีการย่อ/ขยายหน้าต่าง
    frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # สร้าง เฟรมที่ 2
    frame2 = tk.Frame(parent, bg="lightgreen", width=200, height=200)
    # จัดเรียงเฟรมที่ 2 ถัดมา
    frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # สร้าง เฟรมที่ 3
    frame3 = tk.Frame(parent, bg="lightcoral", width=200, height=200)
    # จัดเรียงเฟรมที่ 3 ด้านขวาสุด
    frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # คืนค่าเฟรมทั้ง 3 ออกไปเผื่อนำไปใช้งานต่อ (เช่น ใส่ปุ่มหรือตารางเพิ่มเติม)
    return frame1, frame2, frame3