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
        tk.Label(frame, text=label_text, font=default_font, bg='#f0f0f0', width=15,anchor='w').pack(side='left') #สร้างป้ายชื่อ textดึงข้อมูลมาแสดง และชิดซ้าย เพื่อให้ช่องกรอกอยู่บรรทัดเดียว w ด้านซ้าย
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
        
    # def refresh_data():
    #     """
    #     ฟังก์ชัน รีเฟรช เพื่อดึงข้อมูลล่าสุดจากไฟล์มาแสดงให้เป็นปัจจุบัน
    #     """
    #     for row in tree.get_children(): # tree.get_children() มีอะไรอยู๋ในตารางบ้าง ลูปมาที่ละแถว มาเก็บในตัวแปร
    #         tree.delete(row) #แล้วก็สั่งลบข้อมูลที่ละแถว #เพื่ออัปเดทข้อมูล ก็คือพอลบเสร็จก็จะเข้าในส่วนอัปเดทข้อมูล for pid, data in products.items(): อันนี้
    
    # products = pm.get_all_products() #อ่านข้อมูลแล้วมาเก็บในตัวแปร
    
    # for pid, data in products.items(): #ทำการลูปเอาข้อมูล
    #     tree.insert('', 'end', values=(pid, data['name'], data['price'], data['stock'], data['cost'])) #tree.insert: เป็นคำสั่ง "เขียนข้อมูล" ลงไปในตาราง แล้ว values= คือระบุว่าข้อมูลควรมีอะไรบ้างและเรียงตามลำดับ
    #     #tree.insert: เป็นคำสั่ง "เขียนข้อมูล" ลงไปในตาราง แล้ว values= คือระบุว่าข้อมูลควรมีอะไรบ้างและเรียงตามลำดับ  end คือให้ต่อเป็นแถวๆไป  "" สร้างแถวใหม่ขึ้นมาเลย
        
    # update_summary() # พอ รีเฟรช ก็แสดงจำนวนยอดเงินใหม่
    # check_low_stock() # พอ รีเฟรช ก็จะดูว่ามีสินค้าไหนใกล้หมดไหม
    
    # def update_summary():
    #     """
    #     ฟังก์ชันสำหรับแสดง ยอดเงิน บนหน้า inventory
    #     """
    #     summary = pm.get_store_financial_summary() #ดึงตัวเลขสรุปผลมาเก็บไว้ในตัวแปร
    #     summary_text = (f'ต้นทุนรวม: ฿{summary['total_cost']:,.2f}  |  ' # "จัดรูปแบบข้อความ" ให้สวยงามก่อนจะเอาไปโชว์ครับ
    #                     f'รายได้ที่คาดหวัง: ฿{summary['total_revenue']:,.2f}  |  '
    #                     f'กำไรคาดหวัง: ฿{summary['total_profit']:,.2f}')
    #     ibl_summary.config(text=summary_text)   #จะทำหน้าที่เปลี่ยนข้อความเก่าให้เป็นข้อความใหม่
        
    # def check_low_stock():
    #     """
    #     ฟังก์ชันสำหรับเช็ค สินค้าใกล้หมด
    #     """
    #     low_stock_list = pm.get_low_stock_list(threshold=5) #ไปฟังก์ชันเช็คสต๊อก