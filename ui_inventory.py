import tkinter as tk
from tkinter import ttk, messagebox #ttk คือ widget  messagebox คือหน้าต่างแจ้งเตือนpopup
import product_manager as pm

def setup_inventory_interface(parent):
    """
    ฟังก์ชันหลักสำหรับหน้า GUI คลังสินค้า
    """
    default_font = ("Kanit", 12)  #เก็บตัวแปรฟอนต์ภาษาไทย
    header_font = ("Kanit", 14, "bold") #เก็บตัวแปรฟอนต์ภาษาไทยแบบตัวหนา
    
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
        
    def refresh_data():
        """
        ฟังก์ชัน รีเฟรช เพื่อดึงข้อมูลล่าสุดจากไฟล์มาแสดงให้เป็นปัจจุบัน
        """
        for row in tree.get_children(): # tree.get_children() มีอะไรอยู๋ในตารางบ้าง ลูปมาที่ละแถว มาเก็บในตัวแปร
            tree.delete(row) #แล้วก็สั่งลบข้อมูลที่ละแถว #เพื่ออัปเดทข้อมูล ก็คือพอลบเสร็จก็จะเข้าในส่วนอัปเดทข้อมูล for pid, data in products.items(): อันนี้
        
        products = pm.get_all_products() #อ่านข้อมูลล่าสุดแล้วมาเก็บในตัวแปร
        for pid, data in products.items(): #ทำการลูปเอาข้อมูลใส่ตาราง
            tree.insert('', 'end', values=(pid, data['name'], data['price'], data['stock'], data['cost']))
        
        entry_search.delete(0,tk.END) #เคลียร์ช่องคนหาเมื่อกดรีเฟรช
        update_summary() # พอ รีเฟรช ก็แสดงจำนวนยอดเงินใหม่
        check_low_stock() # พอ รีเฟรช ก็จะดูว่ามีสินค้าไหนใกล้หมดไหม
    

    
    def update_summary():
        """
        ฟังก์ชันสำหรับแสดง ยอดเงิน บนหน้า inventory
        """
        summary = pm.get_store_financial_summary() #ดึงตัวเลขสรุปผลมาเก็บไว้ในตัวแปร
        summary_text = (f'ต้นทุนรวม: ฿{summary['total_cost']:,.2f}  |  ' # "จัดรูปแบบข้อความ" ให้สวยงามก่อนจะเอาไปโชว์ครับ
                        f'รายได้ที่คาดหวัง: ฿{summary['total_revenue']:,.2f}  |  '
                        f'กำไรคาดหวัง: ฿{summary['potential_profit']:,.2f}')
        lbl_summary.config(text=summary_text)   #จะทำหน้าที่เปลี่ยนข้อความเก่าให้เป็นข้อความใหม่
        
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
                details += f'- รหัส: {item['id']} | ชื่อ: {item['name']} | เหลือ: {item['stock']} ชิ้น\n' #เอาข้อความที่ใกล้หมดไปต่อที่หัวข้อคือตัวแปร
                
            messagebox.showwarning('เตือนสินค้าใกล้หมด!', details) #คำเด้งหน้าจอแจ้งเตือนขึ้นแล้วก็เรียกเนื้อหาขึ้นมา
        
        if low_stock_list:
            #config เปลี่ยนคุณสมบัติป้ายชื่อ #cursor='hand2': เมื่อผู้ใช้ลากเมาส์ไปวางทับข้อความนี้ ลูกศรเมาส์จะเปลี่ยนเป็น "รูปมือจิ้ม" เหมือนเวลาเราจะกดลิงก์ในเว็บ เพื่อสื่อให้ผู้ใช้รู้ว่า "ป้ายนี้กดได้นะ"
            lbl_alert.config(text = f'⚠️ แจ้งเตือน: มีสินค้าใกล้หมดสต๊อก {len(low_stock_list)} รายการ! คลิกเพื่อดู',fg='red',cursor='hand2') #ดึงจำนวนรายการมาแสดงโชว์ข้อความให้ผู้ใช้ 
            lbl_alert.bind('<Button-1>',show_low_stock_details) #ทำเหตุการณ์ ให้คลิก แล้วก็แสดงให้ popup ขึ้นมา
        else:                                                                       #cursor="arrow" คือการสั่งให้ "สัญลักษณ์ของเมาส์" กลับมาเป็น "รูปศรปกติ"
            lbl_alert.config(text="✅ สถานะสต็อก: ปกติ", fg="green", cursor="arrow") #ถ้าไม่มีสินค้าใกล้หมดก็จะเข้าเงื่อนไขนี้ 
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
        
        # เรียกใช้ฟังก์ชันจาก product_manager
        success, msg = pm.add_product(pid, name, price, stock, cost) #success: จะได้รับค่าเป็น True (ถ้าบันทึกสำเร็จ) หรือ False (ถ้าล้มเหลว เช่น รหัสสินค้าซ้ำ)
        if success:                                                  #msg: จะได้รับ "ข้อความสรุป" เช่น 'เพิ่มสินค้าสำเร็จ!' หรือ 'รหัสสินค้านี้มีอยู่แล้ว!' เพื่อเอาไปโชว์ให้ผู้ใช้เห็น
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
        for row in tree.get_children(): #มันจะสั่งลบทันที ก่อนที่จะเริ่มแสดงผลการค้นหาครับ เพื่อเป็นการ 'ล้างกระดาน' ข้อมูลเก่าทั้งหมดออกไปก่อน
            tree.delete(row)
        
        for pid, data in results.items():
            tree.insert('','end',values=(pid, data["name"], data["price"], data["stock"], data["cost"])) #เป็นคำสั่ง "เขียนข้อมูล" ลงไปในตาราง แล้ว values= คือระบุว่าข้อมูลควรมีอะไรบ้างและเรียงตามลำดับ  end คือให้ต่อเป็นแถวๆไป  "" สร้างแถวใหม่ขึ้นมาเลย
        
    def on_tree_select(event):
        """
        ฟังก์ชันสำหรับคลิกแถวของข้อมูลเพื่อจะ แก้ไข หรือ ลบ 
        """
        try:                               #selection() นี่แหละคือตัวที่ทำหน้าที่บอกโปรแกรมว่า "ตอนนี้ผู้ใช้กำลังสนใจ (คลิก) แถวไหนอยู่"
            selected = tree.selection()[0] #ให้ไปดูว่าผู้ใช้เลือกแถวไหน [0]คือกรณีเผลอเลือกหลายแถวก็จะให้เลือกแถวที่คลิกล่าสุด
            values = tree.item(selected, "values") #ไปดึงข้อมูลจากแถวนั้นออกมาเก็บไว้ในตัวแปร
            
            clear_form() #เครียร์ฟร์อมเพื่อจะเอาข้อมูลใหม่ไปแสดง
            entry_pid.insert(0, values[0]) #แสดงช้อมูลลงไปในฟร์อม # values[0] = รหัสสินค้า (PID)
            entry_pid.config(state="disabled") # ล็อกการแก้ไขรหัสสินค้า เพื่อป้องกัน Bug 
            entry_name.insert(0, values[1])    # values[1] = ชื่อสินค้า (Name)
            entry_price.insert(0, values[2])   # values[2] = ราคา (Price)
            entry_stock.insert(0, values[3])   # values[3] = สต็อก (Stock)
            entry_cost.insert(0, values[4])    # values[4] = ต้นทุน (Cost)
        except IndexError: #คือการบอกคอมพิวเตอร์ว่า "ถ้าหาไม่เจอ ก็ไม่ต้องทำอะไรนะ นิ่งไว้ โปรแกรมไม่ต้องค้าง"
            pass
    
    # ==========================
    # ปุ่มในมุมฟอร์มฝั่งซ้าย
    # ==========================
    btn_frame = tk.Frame(form_frame,bg='#f0f0f0')
    btn_frame.pack(fill='x', pady=20)
    
    btn_add = tk.Button(btn_frame, text='เพิ่มสินค้า', font=default_font, bg='#4CAF50', command=add_item)
    btn_add.pack(side='left', padx=5, fill='x', expand=True)
    
    btn_update = tk.Button(btn_frame, text="แก้ไข", font=default_font, bg="#2196F3", fg="white", command=update_item)
    btn_update.pack(side="left", padx=5, fill="x", expand=True)
    
    btn_delete = tk.Button(btn_frame, text="ลบ", font=default_font, bg="#f44336", fg="white", command=delete_item)
    btn_delete.pack(side="left", padx=5, fill="x", expand=True)
    
    btn_clear = tk.Button(form_frame, text="เคลียร์ข้อมูลในช่อง", font=default_font, command=clear_form)
    btn_clear.pack(fill="x", pady=5)

    # ==========================
    # เฟรมขวา สำหรับแสดงรายการ และ ยอดสรุป
    # ==========================
    data_frame = tk.Frame(parent, bg='#ffffff', padx=20,pady=20)
    data_frame.place(relx=0.3, relwidth=0.7, relheight=1) #.place ทำให้เป็นเปอร์เซ็น
    
    # กรอบสำหรับสรุปการเงิน และ แจ้งเตือนของใกล้หมด (ส่วนบนขวา)
    dash_frame = tk.Frame(data_frame, bg='#e0f7fa', pady=10,padx=15,relief='ridge',bd=2) #relief='ridge',bd=2 สร้างขอบนูนแล้วปรับเส้นหนา 2
    dash_frame.pack(fill='x', pady=(0, 15)) #ด้านบน 0 ด้านล่าง 15
    
    lbl_summary = tk.Label(dash_frame, text='สรุปการเงิน: --',font=default_font,bg="#e0f7fa")
    lbl_summary.pack(side='left')
    
    lbl_alert = tk.Label(dash_frame, text="สถานะสต็อก: ปกติ", font=default_font, bg="#e0f7fa", fg="green")
    lbl_alert.pack(side="right")
    
    # กรอบสำหรับค้นหา
    search_frame = tk.Frame(data_frame, bg="#ffffff")
    search_frame.pack(fill="x", pady=5)
    # ==========================
    # เฟรม ค้นหาสินค้า
    # ==========================
    # กรอบสำหรับค้นหา
    search_frame = tk.Frame(data_frame, bg="#ffffff")
    search_frame.pack(fill="x", pady=5)
    
    tk.Label(search_frame,text='ค้นหา (ชื่อ / รหัส):', font=default_font,bg='#ffffff').pack(side='left')
    entry_search = tk.Entry(search_frame,font=default_font,width=30) #สร้างช่องกรอกข้อมูล
    entry_search.pack(side='left',padx=10)
    entry_search.bind('<Return>',lambda event: search_item()) #.bind นำเหตุการณ์  <Return> ปุ่ม ถ้าผู้ใช้กรอกช้อมูลแล้วกดปุ่ม ก็จะส่งไปให้ฟังก์ชันทำงาน
    tk.Button(search_frame, text='ค้นหา',font=default_font,bg='#ffc107', command=search_item).pack(side='left',padx=5)
    tk.Button(search_frame, text='รีเฟรชข้อมูล', font=default_font, command=refresh_data).pack(side='left', padx=5)
    
    # ==========================
    # ตารางสินค้า (Treeview)
    # ==========================
    
    columns = ('PID', 'Name', 'Price', 'Stock', 'Cost') #สร้างชื่อตอลัมขึ้นมาแล้วก็เก็บในตัวแปร
    tree = ttk.Treeview(data_frame, columns=columns, show='headings', height=20) #สร้างตาราง เอาคอลัมที่กำหนดมาแสดง สั่งให้แสดงเฉพาะหัวตาราง
    
    # จัดการแสดงผลฟอนต์ไทยใน Treeview
    style = ttk.Style() #เรียก .Style() มาตกแต่งให้ทั้งหมดเหมือนกัน
    style.configure("Treeview.Heading", font=header_font) #กำหนดให้หัวตาราง ตัวใหญ่และเด่นทำให้รอมันคือคอลัมอะไร
    style.configure("Treeview", font=default_font, rowheight=30)
    
    # กำหนดหัวตาราง
    tree.heading("PID", text="รหัสสินค้า") #กำหนดให้ตรงตามที่ลำเคยสร้างตัวแปรคอลัมว่ามันจะไปอยู่ส่วนไหน
    tree.heading("Name", text="ชื่อสินค้า")
    tree.heading("Price", text="ราคาขาย (บาท)")
    tree.heading("Stock", text="สต็อกคงเหลือ")
    tree.heading("Cost", text="ต้นทุน (บาท)")
    
    # กำหนดความกว้างคอลัมน์                          # Center (กลาง)  W (ซ้าย) E (ขวา)
    tree.column("PID", width=100, anchor="center") #กำหนดข้อความคอลัม width คือ ขนาดความกว้างที่กำหนดว่าส่วนนี้ของผมไม่ต้องมายุ่ง 
    tree.column("Name", width=350, anchor="w")
    tree.column("Price", width=120, anchor="e")
    tree.column("Stock", width=120, anchor="center")
    tree.column("Cost", width=120, anchor="e")
    
    # ผูก Event เวลากดเลือกแถว
    tree.bind("<<TreeviewSelect>>", on_tree_select) # เหตุการณ์กระทำ เมื่อมีการกระทำ การคลิกแถว จะทำการ เรียกฟังก์ชัน
    
    # เพิ่ม Scrollbar ให้ตาราง                                                       #คือการผูกการทำงานของแถบเลื่อนเข้ากับมุมมองแนวตั้งของตาราง
    scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=tree.yview) #เมื่อมีคนมาเลื่อนในส่วน data_frame ทำให้เลื่อนจากบนลงล่าง 
    tree.configure(yscrollcommand=scrollbar.set) #เมื่อข้อมูลของ tree มันเยอะเกินหน้าจอ จะทำการสั่งให้เลื่อนสกอบาร์ได้
    
    tree.pack(side="left", fill="both", expand=True) #ให้ตารางอยู่ฝั่งซ้าย ให้ตารางเต็มพื้นที่ สั่งให้เต็มพื้นที่ขนาด
    scrollbar.pack(side="right", fill="y") #สั่งให้อยู่ฝั่งขวา พร้อมให้มันยาวลงมาเป็นแกนYเท่านั้น
    
    # ดึงข้อมูลมาแสดงครั้งแรก
    refresh_data()