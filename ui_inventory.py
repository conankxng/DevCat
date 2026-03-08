import tkinter as tk
from tkinter import ttk, messagebox #ttk คือ widget  messagebox คือหน้าต่างแจ้งเตือนpopup
import customtkinter as ctk
import product_manager as pm

def setup_inventory_interface(parent):
    """
    ฟังก์ชันหลักสำหรับหน้า GUI คลังสินค้า
    """
    default_font = ("Kanit", 15)  #เก็บตัวแปรฟอนต์ภาษาไทย
    
    form_frame = ctk.CTkFrame(parent,fg_color="white",corner_radius=15) #กล่อง Frame parentพารามิตเตอร์ที่จะเอา Frame ไปว่างใน Main กำหนดโค้งมน 15
    form_frame.place(relheight=0.96, relwidth=0.28, relx=0.01, rely=0.02) #.place() ปรับตำแหน่งอิสระ 
    
    ctk.CTkLabel(
        form_frame, 
        text='ระบบจัดการคลังสินค้า', 
        font=("Kanit", 25, "bold"), 
        text_color="#1e683e"
    ).pack(pady=(20, 20))    
    
    def create_input(label_text):
        """
        ฟังก์ชันสร้างช่องกรอกข้อมูล
        """
        frame = ctk.CTkFrame(form_frame,fg_color="transparent") #สร้างแถวมาอยู่ใน form_frame  #transparent โปร่งใส่
        frame.pack(fill='x', pady=8, padx=10)  #วางแถวนี้ลงบนหน้าจอ และให้ขยายเต็มความกว้าง และเว้นคนสูง 8
        
        ctk.CTkLabel(frame, text=label_text,  font=("Kanit", 18, "bold"), width=120, anchor='w', text_color="#1e683e").pack(side='left') #สร้างป้ายชื่อ textดึงข้อมูลมาแสดง และชิดซ้าย เพื่อให้ช่องกรอกอยู่บรรทัดเดียว w ด้านซ้าย
        
        entry = ctk.CTkEntry(
            frame, 
            font=("Kanit", 18,), 
            height=35, # ทำให้กล่องสูงขึ้นเพื่อให้คลิกง่าย
            fg_color="white", # สีพื้นหลังช่องกรอก
            border_color="#1e683e", #สีกรอบ
            text_color="black", # สีตัวอักษรตอนพิมพ์
            border_width=2, #ความหน้าของเส้นกรอบ
        )
        entry.pack(side='left', fill='x', expand=True) #Xยืดความกว้างออกไปทางขวา จนเต็มพื้นที่ True ถ้าหน้าต่างขยายใหญ่ขึ้น ให้ช่องกรอกนี้ยืดตามไปด้วย 
        return entry
    
    entry_pid = create_input('รหัสสินค้า (ID):') #ส่งค่าไปในฟังก์ชันเพื่อใช้เลือก
    entry_name = create_input('ชื่อสินค้า:')
    entry_price = create_input('ราคาขาย:')
    entry_stock = create_input('จำนวนสต๊อก:')
    entry_cost = create_input('ต้นทุน:')
    
    def clear_form():
        entry_pid.configure(state='normal') #คำสั่งให้ปลดล็อค รหัสสิินค้าถึงจะเข้าไปลบข้างในได้
        entry_pid.delete(0, tk.END) #คำสั่งลบข้อความออกจากช่องกรอก 0คือตั้งแต่ตัวแรก end ถึงตัวสุดท้าย
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_stock.delete(0, tk.END)
        entry_cost.delete(0, tk.END)
        
    def refresh_data():
        """
        ฟังก์ชัน รีเฟรช เพื่อดึงข้อมูลล่าสุดจากไฟล์มาแสดงให้เป็นปัจจุบัน
        """
        for row in tree.get_children(): # tree.get_children() มีอะไรอยู๋ในตารางบ้าง ลูปมาที่ละแถว มาเก็บในตัวแปร
            tree.delete(row) #แล้วก็สั่งลบข้อมูลที่ละแถว #เพื่ออัปเดทข้อมูล ก็คือพอลบเสร็จก็จะเข้าในส่วนอัปเดทข้อมูล for pid, data in products.items(): อันนี้
        
        products = pm.get_all_products() #อ่านข้อมูลล่าสุดแล้วมาเก็บในตัวแปร
        for pid, data in products.items(): #ทำการลูปเอาข้อมูลใส่ตาราง
            tree.insert('', 'end', values=(pid, f'{data["name"]}', f'{data["price"]:,.2f}', data['stock'], f'{data["cost"]:,.2f}'))
        
        entry_search.delete(0,tk.END) #เคลียร์ช่องคนหาเมื่อกดรีเฟรช
        update_summary() # พอ รีเฟรช ก็แสดงจำนวนยอดเงินใหม่
        check_low_stock() # พอ รีเฟรช ก็จะดูว่ามีสินค้าไหนใกล้หมดไหม
    

    
    def update_summary():
        """
        ฟังก์ชันสำหรับอัปเดตตัวเลขในกล่องการ์ดทั้ง 3 ใบ
        """
        summary = pm.get_store_financial_summary() 
        
        lbl_cost_val.configure(text=f"ต้นทุนรวม: ฿ {summary['total_cost']:,.2f}")
        lbl_rev_val.configure(text=f"รายได้ที่คาดหวัง: ฿ {summary['total_revenue']:,.2f}")
        
        # ถ้าร้านมีกำไร (เลขเป็นบวก) ให้สีตัวอักษรเป็นสีเขียว
        if summary['potential_profit'] >= 0:
            lbl_profit_val.configure(text=f"กำไรที่คาดหวัง: ฿ {summary['potential_profit']:,.2f}", text_color="green")
        else:
            lbl_profit_val.configure(text=f"กำไรที่คาดหวัง: ฿ {summary['potential_profit']:,.2f}", text_color="red")

    def check_low_stock():
        """
        ฟังก์ชันสำหรับเช็ค สินค้าใกล้หมด
        """
        low_stock_list = pm.get_low_stock_list(threshold=5) #ไปฟังก์ชันเช็คสต๊อก
    
        def show_low_stock_details(event):
            """
            ฟังก์ชันสำหรับเมื่อคลิกจะแจ้งเตือนสินค้าที่ใกล้หมด
            """
            if not low_stock_list: #ถ้าไม่มีสินค้าใกล้หมดก็จะจบการทำงาน ไม่แสดงอะไร
                return
            
            details = 'รายการสินค้าที่ใกล้หมดสต๊อก:\n\n' #หัวข้อของข้อความ
            for item in low_stock_list: #ลูปสินค้าที่ใกล้หมด
                details += f"- รหัส: {item['id']} | ชื่อ: {item['name']} | เหลือ: {item['stock']} ชิ้น\n" #เอาข้อความที่ใกล้หมดไปต่อที่หัวข้อคือตัวแปร
                
            messagebox.showwarning('เตือนสินค้าใกล้หมด!', details) #คำเด้งหน้าจอแจ้งเตือนขึ้นแล้วก็เรียกเนื้อหาขึ้นมา
        
        if low_stock_list:
            #cursor='hand2'เมื่อไปชี้จะเป็นรูปมือว่ากดได้
            lbl_alert.configure(text = f'⚠️ แจ้งเตือน: มีสินค้าใกล้หมดสต๊อก {len(low_stock_list)} รายการ! คลิกเพื่อดู',text_color='red',cursor='hand2') #ดึงจำนวนรายการมาแสดงโชว์ข้อความให้ผู้ใช้ 
            lbl_alert.unbind('<Button-1>') # ลบ event เก่าออกก่อนเสมอเพื่อป้องกันการแจ้งเตือนเด้งซ้อนกันหลายรอบ
            lbl_alert.bind('<Button-1>',show_low_stock_details) #ทำเหตุการณ์ ให้คลิก แล้วก็แสดงให้ popup ขึ้นมา
        else:                                                                       #cursor="arrow" คือการสั่งให้ "สัญลักษณ์ของเมาส์" กลับมาเป็น "รูปศรปกติ"
            lbl_alert.configure(text="✅ สถานะสต็อก: ปกติ", text_color="green", cursor="arrow") #ถ้าไม่มีสินค้าใกล้หมดก็จะเข้าเงื่อนไขนี้ 
            lbl_alert.unbind('<Button-1>') #.unbind ยกเลิกการคลิกของผู้ใช้
    
    def add_item():
        """
        ฟังก์ชันสำหรับนำสินค้าเข้า Data
        """
        pid = entry_pid.get().strip() #ดึงข้อมูลจากผู้ใช้ที่พิมพ์ข้อมูล และตัดช่องว่างออกให้หมด
        name = entry_name.get().strip()
        price = entry_price.get().strip()
        stock = entry_stock.get().strip()
        cost = entry_cost.get().strip()
        
        if not pid or not name or not price or not stock or not cost: #เช็คว่าผู้ใช้พิมพ์ครบทุกช่องไหม not ถ้าไม่มีแสดง Flast ถ้ามีแสดง True
            messagebox.showwarning("เตือน!", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return
        
        try:
            price = float(price)
            stock = int(stock)
            cost = float(cost)
        except ValueError: #ตรวจสอบข้อมูลว่าเป็นแบบที่เรากำหนดไหม ถ้าไม่ใช้ก็แสดงข้อมูลแจ้งเตือน
            messagebox.showwarning('เตือน!', 'ราคา, ต้นทุน ต้องเป็นตัวเลข \nและ สต๊อกต้องเป็นจำนวนเต็ม')
            return
        
        # เรียกใช้ฟังก์ชันจาก product_manager
        success, msg = pm.add_product(pid, name, price, stock, cost) #success: จะได้รับค่าเป็น True กับ Flase
        if success:                                                  #msg: จะได้รับ ค่าข้อความที่ ส่งมา
            messagebox.showinfo('สำเร็จ', msg)
            clear_form()    # ล้างข้อความในช่องกรอกให้ว่างเหมือนเดิม
            refresh_data()  # อัปเดตตารางให้สินค้าใหม่โผล่ขึ้นมาทันที
        else:
            messagebox.showerror('ผิดพลาด', msg)
        
    def update_item():
        """
        ฟังก์ชันสำหรับ อัปเดท Data ข้อมูลเดิม
        """
        pid = entry_pid.get().strip() #ดึงข้อมูลจากผู้ใช้ที่พิมพ์ข้อมูล และตัดช่องว่างออกให้หมด
        name = entry_name.get().strip()
        price = entry_price.get().strip()
        stock = entry_stock.get().strip()
        cost = entry_cost.get().strip()
        
        if not pid: #เช็คว่ามีการเลือกรหัสสินไหมหรือช่องว่างเปล่าถ้าว่างทำการแจ้งเตือน
            messagebox.showwarning('เตือน!', 'กรุณาเลือกรหัสสินค้าเพื่อแก้ไขข้อมูล')
            return
        
        if not name: #เช็คว่ามีการลบชื่อไหมหรือช่องว่างเปล่าถ้าว่างทำการแจ้งเตือน
            messagebox.showwarning('เตือน!', 'ช่องชื่อสินค้าว่างเปล่า')
            return
        
        try:
            price = float(price)
            stock = int(stock)
            cost = float(cost)
        except ValueError: #เช็คข้อมูลว่ากรอกตามที่เรากำหนดไหม
            messagebox.showwarning("เตือน!", "รูปแบบตัวเลขไม่ถูกต้อง")
            return
        
        success, msg =pm.update_product(pid, name, price, stock, cost) #ตัวแปรแสดงค่า True False แล้วข้อความ
        if success: #เช็คค่า
            messagebox.showinfo('สำเร็จ', msg)
            clear_form()    # ล้างข้อความในช่องกรอกให้ว่างเหมือนเดิม
            refresh_data()  # อัปเดตตารางให้สินค้าใหม่โผล่ขึ้นมาทันที
        else:
            messagebox.showerror('ผิดพลาด', msg)
            
    def delete_item():
        """
        ฟังก์ชันลบสินค้าใน Data
        """
        pid = entry_pid.get().strip()
        if not pid: #เช็คว่ามีการเลือกรหัสสินไหมหรือช่องว่างเปล่าถ้าว่างทำการแจ้งเตือน
            messagebox.showwarning('เตือน!', "กรุณาเลือกรหัสสินค้าเพื่อลบ")
            return
            
        confirm = messagebox.askyesno('ยืนยัน', f'คุณต้องการลบสินค้ารหัส: {pid} ใช่หรือไม่?') #askyesno สร้าง 2 ตัวเลือกว่าจะลบหรือไม่ จะส่ง True False
        if confirm: #ถ้า True เข้าเงื่อนไข
            success, msg = pm.delete_product(pid) #ตัวแปรแสดงค่า True False แล้วข้อความ
            if success:  #ถ้า True เข้าเงื่อนไข
                messagebox.showinfo('สำเร็จ', msg)
                clear_form()    # ล้างข้อความในช่องกรอกให้ว่างเหมือนเดิม
                refresh_data()  # อัปเดตตารางให้สินค้าใหม่โผล่ขึ้นมาทันที
            else:
                messagebox.showerror('ผิดพลาด',msg)
    
    def search_item():
        """
        ฟังก์ชันสำหรับค้นหาสินค้า
        """
        query = entry_search.get().strip() #หยิบข้อความที่ผู้ใช้พิมพ์มาเก็บไว้ในตัวแปร 
        if not query:
            refresh_data() # ถ้าไม่ได้พิมพ์อะไร ให้รีเฟรชโชว์ทั้งหมด
            return
        
        results = pm.search_product(query) #โปรแกรมจะส่ง query ไปให้ฟังก์ชัน ให้ช่วยหาว่ามีสินค้าตัวไหนที่มีชื่อกับรหัสเหมือนอันนี้บ้าง
        # เคลียร์ตารางเดิมทิ้ง
        for row in tree.get_children(): #มันจะสั่งลบทันที ก่อนที่จะเริ่มแสดงผลการค้นหาครับ เพื่อเป็นการ ล้างกระดาน ข้อมูลเก่าทั้งหมดออกไปก่อน
            tree.delete(row)
        
        for pid, data in results.items():
            tree.insert('','end',values=(pid, data["name"], f'{data["price"]:,.2f}', data["stock"], f'{data["cost"]:,.2f}')) #เป็นคำสั่ง เขียนข้อมูล ลงไปในตาราง แล้ว end คือให้ต่อเป็นแถวๆไป  "" สร้างแถวใหม่ขึ้นมาเลย
        
    def on_tree_select(event):
        """
        ฟังก์ชันสำหรับคลิกแถวของข้อมูลเพื่อจะ แก้ไข หรือ ลบ 
        """
        try:                               #selection() คือผู้ใช้กำลังคลิกอันไหน
            selected = tree.selection()[0] #ให้ไปดูว่าผู้ใช้เลือกแถวไหน [0]คือกรณีเผลอเลือกหลายแถวก็จะให้เลือกแถวที่คลิกล่าสุด
            values = tree.item(selected, "values") #ไปดึงข้อมูลจากแถวนั้นออกมาเก็บไว้ในตัวแปร
            
            clear_form() #เครียร์ฟร์อมเพื่อจะเอาข้อมูลใหม่ไปแสดง
            entry_pid.insert(0, values[0]) #แสดงช้อมูลลงไปในฟร์อม # values[0] = รหัสสินค้า (PID)
            entry_pid.configure(state="disabled") # ล็อกการแก้ไขรหัสสินค้า เพื่อป้องกัน Bug 
            entry_name.insert(0, str(values[1]).strip())    # values[1] = ชื่อสินค้า (Name) (ตัดช่องว่างข้างหน้าออกตอนดึงข้อมูลมา)
            # ตัดลูกน้ำ ออกจากราคาและต้นทุนก่อนนำไปวางในช่องกรอก เพื่อให้ฟังก์ชัน update ทำงานได้ต่อ
            entry_price.insert(0, str(values[2]).replace(',', ''))   # values[2] = ราคา (Price)
            entry_stock.insert(0, values[3])   # values[3] = สต็อก (Stock)
            entry_cost.insert(0, str(values[4]).replace(',', ''))    # values[4] = ต้นทุน (Cost)
        except IndexError: #คือการบอกคอมพิวเตอร์ว่า "ถ้าหาไม่เจอ ก็ไม่ต้องทำอะไรนะ นิ่งไว้ โปรแกรมไม่ต้องค้าง"
            pass
    
    # ==========================
    # ปุ่มในมุมฟอร์มฝั่งซ้าย
    # ==========================
    btn_frame = ctk.CTkFrame(form_frame,fg_color="transparent")
    btn_frame.pack(fill='x', pady=20,padx=10)
    
    btn_add = ctk.CTkButton(
        btn_frame, text='➕ เพิ่มสินค้าใหม่', font=("Kanit", 16, "bold"), height=50, # เพิ่มความสูงและทำตัวหนา
        fg_color="#1e683e", hover_color="#003a17", #เมาส์ไปชี้เพื่อเปลี่ยนสี
        command=add_item
    )
    btn_add.pack(fill='x', pady=(0, 10)) #xยืดความกว้างออกไปทางขวา
    
    sub_action_frame = ctk.CTkFrame(btn_frame, fg_color="transparent") #เว้นระยะ
    sub_action_frame.pack(fill="x")
    
    btn_update = ctk.CTkButton(
        sub_action_frame, text="✏️ แก้ไข", font=("Kanit", 16, "bold"), height=50,
        fg_color="#2196F3", hover_color="#0d47a1", text_color="white",
        command=update_item
    )
    btn_update.pack(side="left", fill="x", expand=True, padx=(0, 5))
    
    btn_delete = ctk.CTkButton(
        sub_action_frame, text="🗑️ ลบ", font=("Kanit", 16, "bold"), height=50, 
        fg_color="#f44336", hover_color="#b71c1c", text_color="white",
        command=delete_item
    )
    btn_delete.pack(side="left", fill="x", expand=True, padx=(5, 0))
    
    btn_clear = ctk.CTkButton(
        form_frame, text="🧹 เคลียร์ข้อมูลในช่อง", font=("Kanit", 16, "bold"), height=50, 
        fg_color="transparent", border_color="#1e683e", border_width=2, text_color="#1e683e",
        hover_color="#f0f0f0",
        command=clear_form
    )
    btn_clear.pack(fill="x", pady=(15, 5), padx=10)

    # ==========================
    # เฟรมขวา สำหรับแสดงรายการ และ ยอดสรุป
    # ==========================
    data_frame = ctk.CTkFrame(parent, fg_color="#F8F9FA", corner_radius=15)
    data_frame.place(relwidth=0.68, relheight=0.96, relx=0.3, rely=0.02) #กำหนดขนาด จากอันที่กำหนดไว้ไม่ให้ทับกัน
    
    # กรอบสำหรับสรุปการเงิน และ แจ้งเตือนของใกล้หมด (ส่วนบนขวา)
    dash_frame = ctk.CTkFrame(data_frame, fg_color="#E8F5E9", border_color="#1e683e", border_width=2, corner_radius=10)
    dash_frame.pack(fill='x', pady=20, padx=20) 
    
    #สร้างกล่องที่ 1
    lbl_cost_val = ctk.CTkLabel(dash_frame, text="฿ 0.00", font=("Kanit", 16, "bold"), text_color="#f98404")
    lbl_cost_val.pack(side="left", padx=15, pady=10)
    
    # สร้างกล่องที่ 2
    lbl_rev_val = ctk.CTkLabel(dash_frame, text="฿ 0.00", font=("Kanit", 16, "bold"), text_color="#1565C0")
    lbl_rev_val.pack(side="left", padx=15, pady=10)
    
    # สร้างกล่องที่ 3
    lbl_profit_val = ctk.CTkLabel(dash_frame, text="฿ 0.00", font=("Kanit", 16, "bold"), text_color="#2E7D32")
    lbl_profit_val.pack(side="left", padx=15, pady=10)
    
    lbl_alert = ctk.CTkLabel(
        dash_frame, text="✅ สถานะสต็อก: ปกติ", 
        font=("Kanit", 16, "bold"), text_color="green" # เดี๋ยวสีแดงเราไปแก้ใน check_low_stock อีกที
    )
    lbl_alert.pack(side="right", padx=15, pady=10)
    

    # ==========================
    # เฟรม ค้นหาสินค้า
    # ==========================
    # กรอบสำหรับค้นหา
    search_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
    search_frame.pack(fill="x", padx=20, pady=(0, 10))
    
    ctk.CTkLabel(search_frame, text='🔍 ค้นหา (ชื่อ/รหัส):', font=default_font, text_color="#1e683e").pack(side='left', padx=(0, 10))
    
    entry_search = ctk.CTkEntry(
        search_frame, font=default_font, width=250, height=35,
        border_color="#1e683e", border_width=2
    )
    entry_search.pack(side='left', padx=10)
    entry_search.bind('<Return>', lambda event: search_item()) #.bind นำเหตุการณ์  <Return> ปุ่ม ถ้าผู้ใช้กรอกช้อมูลแล้วกดปุ่ม ก็จะส่งไปให้ฟังก์ชันทำงาน
    
    btn_search = ctk.CTkButton(
        search_frame, text='ค้นหา', font=default_font, 
        fg_color="#1e683e", hover_color="#003a17", text_color="white", width=100,
        command=search_item
    )
    btn_search.pack(side='left', padx=5)
    
    btn_refresh = ctk.CTkButton(
        search_frame, text='🔄 รีเฟรชข้อมูล', font=default_font, 
        fg_color="transparent", border_color="#1e683e", border_width=2, text_color="#1e683e", hover_color="#f0f0f0", width=120,
        command=refresh_data
    )
    btn_refresh.pack(side='left', padx=5)
    
    # ==========================
    # ตารางสินค้า (Treeview)
    # ==========================
    tree_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    columns = ('PID', 'Name', 'Price', 'Stock', 'Cost') #สร้างชื่อตอลัมขึ้นมาแล้วก็เก็บในตัวแปร
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20, selectmode="browse")  #สร้างตาราง เอาคอลัมที่กำหนดมาแสดง สั่งให้แสดงเฉพาะหัวตาราง #browseเลือกได้ทีละแถวเดียวเท่านั้น
    

    style = ttk.Style() 
    style.theme_use("clam")  # ลบขอบตารางแบบยุคเก่าออก
    
    style.configure("Treeview", 
                    background="white",
                    foreground="#333333",
                    rowheight=35,            # ความสูงแต่ละแถว
                    fieldbackground="white",
                    font=("Kanit", 12),
                    borderwidth=0) #เอาเส้นขอบออก
                    
    style.configure("Treeview.Heading", 
                    font=("Kanit", 14, "bold"), 
                    background="#1e683e",  # สีเขียวเข้มของร้าน
                    foreground="white",
                    borderwidth=0,
                    relief="flat") #ผิวเฟรมกับปุ่ม เรียบไปกับจอ
                    
    # map เปลี่ยนสีเวลาคลิกเลือกรายการ 
    style.map('Treeview', background=[('selected', '#C8E6C9')], foreground=[('selected', '#000000')])
    style.map('Treeview.Heading', background=[('active', '#144e2d')]) #เมื่อเอาเมาส์ไปชี้หัวตารางจะเปลี่ยนเป็นสีนี้
    
    # กำหนดหัวตาราง
    tree.heading("PID", text="รหัสสินค้า", anchor="center") #กำหนดให้ตรงตามที่ลำเคยสร้างตัวแปรคอลัมว่ามันจะไปอยู่ส่วนไหน
    tree.heading("Name", text="ชื่อสินค้า", anchor="center")
    tree.heading("Price", text="ราคาขาย (บาท)", anchor="e")
    tree.heading("Stock", text="สต็อกคงเหลือ", anchor="center")
    tree.heading("Cost", text="ต้นทุน (บาท)", anchor="e")
    
    # กำหนดความกว้างคอลัมน์                          # Center (กลาง)  W (ซ้าย) E (ขวา)
    tree.column("PID", width=100, anchor="center") #กำหนดข้อความคอลัม width คือ ขนาดความกว้างที่กำหนดว่าส่วนนี้ของผมไม่ต้องมายุ่ง 
    tree.column("Name", width=350, anchor="center")
    tree.column("Price", width=120, anchor="e")
    tree.column("Stock", width=120, anchor="center")
    tree.column("Cost", width=120, anchor="e")
    
    # ผูก Event เวลากดเลือกแถว
    tree.bind("<<TreeviewSelect>>", on_tree_select) # เหตุการณ์กระทำ เมื่อมีการกระทำ การคลิกแถว จะทำการ เรียกฟังก์ชัน
    
    # เพิ่ม Scrollbar ให้ตาราง                                                       #คือการผูกการทำงานของแถบเลื่อนเข้ากับมุมมองแนวตั้งของตาราง
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)  #เมื่อมีคนมาเลื่อนในส่วน tree_frame ทำให้เลื่อนจากบนลงล่าง 
    tree.configure(yscrollcommand=scrollbar.set)  #เมื่อข้อมูลของ tree มันเยอะเกินหน้าจอ จะทำการสั่งให้เลื่อนสกอบาร์ได้
    
    tree.pack(side="left", fill="both", expand=True) #ให้ตารางอยู่ฝั่งซ้าย ให้ตารางเต็มพื้นที่ สั่งให้เต็มพื้นที่ขนาด
    scrollbar.pack(side="right", fill="y") #สั่งให้อยู่ฝั่งขวา พร้อมให้มันยาวลงมาเป็นแกนYเท่านั้น
    
    # ดึงข้อมูลมาแสดงครั้งแรก
    refresh_data()
    