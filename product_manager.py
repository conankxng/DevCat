import storage_product as storage

def add_product(pid,name,price,stock,cost):
    """
    ฟังก์ชันสำหรับเพิ่มสินค้า
    """
    inventory = storage.load_products() #เรียกฟังก์ชันในไฟล์เก็บข้อมูลเพื่อดึงรายการสินค้า
    
    if pid in inventory:
        return False, f'เกิดข้อผิดพลาด: รหัสสินค้า "{pid}" มีอยู่แล้ว!' #เช็คว่ารหัสสินค้าซ้ำกับที่่อยู่ในระบบไหม หาซ้ำจะหยุดทำงานและส่งค่่า False
    
    for existing_pid,product in inventory.items(): #เช็คว่ามีชื่อสินค้าซ้ำกันไหมก่อนเพิ่มสินค้า
        if product.get('name') == name:
            return False, f'เกิดข้อผิดพลาด: ชื่อสินค้า "{name}" มีอยู่แล้วในระบบ!'
    
    #เพิ่มช้อมูลลง Dictionary
    inventory[pid] = {'name':name, "price":price, "stock":stock, 'cost':cost} #หากไม่่ซ้ำก็จะทำการสร้างข้อมูลเก็บเข้าไปใน inventory โดยใช้ pid เป็นคีย์หลัก
    storage.save_products(inventory) #เมื่อเพิ่มข้อมูลในตัวแปรเสร็จ ก็สั่งบันทึกทับลงไปในไฟล์ฟังก์ชั่่น save_products
    return True, "สำเร็จ: เพิ่มสินค้าเรียบร้อยแล้ว!" #เมื่อทำงานครบทุกขั้นตอน จะส่งค่า True (สำเร็จ) พร้อมข้อความยืนยันกลับไป

def get_all_products():
    """
    ฟังก์ชันสำหรับดึงข้อมูลสินค้าทั้งหมด
    เพื่่อให้หน้าจอ GUI นำไปวนลูปแแสดงในตาราง
    """
    return storage.load_products() #ไปดึงไฟล์ออกมาเพื่อจะเอาไปแสดง

def update_product(pid,name,price,stock,cost):
    """
    ฟังก์ชันสำหรับแก้ไขข้อมูลสินค้า
    """
    inventory = storage.load_products() #อ่านไฟลฺ์แล้วดึงข้อมูลมาเก็บไว้ในตัวแปร
    
    if pid not in inventory: #เอามาเช็คเงื่อนไข ว่าไม่่มี รหัสสินค้า ข้อมูลจริงไหม
        return False, 'แจ้งเตือน: ไม่พบรหัสสินค้านี้ในระบบ!' #แล้วก็ส่งข้อมูลกลับไป
    
    for existing_pid, product in inventory.items():
        if existing_pid != pid and product.get('name') == name: #ถ้าเป็นรหัสสินค้าตัวเดิมไม่่ถือว่ามันซ้ำนะ เราจะแจ้งตรงส่วน ชื่อว่าห้ามซ้ำ
            return False, f'เกิดข้อผิดพลาด: ชื่อสินค้า "{name}" มีอยู่แล้วในระบบ!' 
    
    #ถ้ามีมาเข้าส่วนนี้ ก็คือเก็บข้อมูลใหม่ลงในตัวแปร
    inventory[pid]["name"] = name 
    inventory[pid]["price"] = price 
    inventory[pid]["stock"] = stock
    inventory[pid]["cost"] = cost
    
    storage.save_products(inventory) #แล้วทำการนำข้อมูลใหม่กลับไปเซฟลงไฟล์ txt
    return True,"สำเร็จ: แก้ไขสินค้าเรียบร้อยแล้ว!" #แล้วส่งแจ้งเตือนกลับไป

def delete_product(pid):
    """
    ฟังก์ชันสำหรับลบสินค้า
    """
    
    inventory = storage.load_products() #โหลดข้อมูลสินค้าแล้วมาเก็บในตัวแปร
    
    if pid not in inventory:
        return False,"แจ้งเตือน: ไม่พบรหัสสินค้านี้ในระบบ!" #เช็คว่ามีรหัสสินค้าไหมถ้าไม่มี return แจ้งเตือนกลับ
    
    del inventory[pid] #ถ้ามีก็มาเข้าเงื่อนไขนี้ก็คือ คำสั่ง del คือลบข้อมูลทั้งหมด
    storage.save_products(inventory) #แล้วก็ทำการเซฟข้อมูลใหม่ลงไป
    return True,"สำเร็จ: ลบสินค้าเรียบร้อยแล้ว!" #return ค่ากลับพร้อมแจ้งเตือน

def best_seller(threshold=20):
    """
    ฟังก์ชันสำหรับเช็คสินค้าขายดี
    """
    inventory = storage.load_products() #ดึงข้อมูลในไฟล์มาเก็บใน ตัวแปร
    best_stock_items = [] #สร้างตัวแปรสำหรับเก็บข้อมูลสำหรับรายชื่อสินค้าขายดี
    
    for pid,data in inventory.items(): #วนรอบตรวจสอบข้อมูล
        if data['stock']<=threshold: #มาเข้าเงื่อนไข ตรวจสอบ stock น้อยกว่าหรือ = ตัวแปรที่กำหนดไว้
            best_stock_items.append({ #เก็บข้อมูลลงในตัวแปร ใช้append ต่อท้ายข้อมูลเก็บ ทั้งid ชื่อ จำนวนสินค้า เป็น list
                "id":pid,
                "name":data["name"],
                "stock": data["stock"]
            })
    return best_stock_items #ส่ง ข้อมูลเป็น listกลับไป

def get_low_stock_list(threshold=5):
    """
    ฟังก์ชันสำหรับเช็คสินค้าใกล้หมด
    """
    inventory = storage.load_products() #ดึงข้อมูลในไฟล์มาเก็บใน ตัวแปร
    low_stock_items = [] #สร้างตัวแปรสำหรับเก็บข้อมูลสำหรับรายชื่อสินค้าใกล้หมด
    
    for pid,data in inventory.items(): #วนรอบตรวจสอบข้อมูล
        if data['stock']<=threshold: #มาเข้าเงื่อนไข ตรวจสอบ stock น้อยกว่าหรือ = ตัวแปรที่กำหนดไว้
            low_stock_items.append({ #เก็บข้อมูลลงในตัวแปร ใช้append ต่อท้ายข้อมูลเก็บ ทั้งid ชื่อ จำนวนสินค้า เป็น list
                "id":pid,
                "name":data["name"],
                "stock": data["stock"]
            })
    return low_stock_items #ส่ง ข้อมูลเป็น listกลับไป


def search_product(query):
    """
    ค้นหาสินค้าจากชื่อหรือ ID
    คืนค่าเป็น Dictionary ของสินค้าที่ค้นพบ
    """
    inventory = storage.load_products() #ดึงข้อมูลในไฟล์มาเก็บใน ตัวแปร
    results = {} #สร้าง Dictionary ว่างเพื่อรอเก็บรายการที่ค้นพบ
    query = query.lower() #ทำให้เป็นตัวพิมพ์เล็ก
    
    for pid,data in inventory.items(): #ลูปวนตรวจสอบข้อมูล            # ใช้ .lower() เพื่อให้ค้นหาเจอแม้จะพิมพ์ตัวเล็กหรือตัวใหญ่ไม่ตรงกัน
        if query in pid.lower() or query in data['name'].lower():   # ตรวจสอบว่า query (คำค้นหา) ปรากฏอยู่ใน pid (รหัส) หรือ name (ชื่อสินค้า)
            results[pid] = data #หากพบว่าคำค้นหาตรงกับรหัสหรือชื่อสินค้าชิ้นนั้น จะนำข้อมูลสินค้านั้นมาใส่ไว้ในตัวแปร
    
    return results #แล้วก็ส่งค่ากลับไปในฟังก์ชั่น

def process_sale(pid,quantity):
    """
    ฟังก์ชันสำหรับตัดสต็อกสินค้าเมื่อมีการขาย
    """
    inventory = storage.load_products() #เรียกใช้ฟังก์ชันจากไฟล์ เพื่อดึงข้อมูล
    if pid in inventory: #ตรวจสอบข้อมูลรหัสสินค้า
        current_stock = inventory[pid]['stock']
        if inventory[pid]['stock']>=quantity: #ตรวจสอบว่าจำนวนสินค้าในคลัง มีเพียงพอ ต่อการขายครั้งนี้หรือไม่
            inventory[pid]['stock']-=quantity #หากข้อมูลถูกต้องและสินค้าพอ ระบบจะทำการ ลบจำนวน สินค้าออกจากสต็อกในตัวแปร
            storage.save_products(inventory) #สั่งบันทึกข้อมูลที่ถูกหักสต็อกแล้วทับลงในไฟล์
            return True,'ตัดสต๊อกสำเร็จ!' 
        return False, f"สินค้าในสต๊อกไม่่เพียงพอ!\n(ปัจจุบันเหลืออยู่เพียง {current_stock} ชิ้น)" #ตรวจสอบแล้วของน้อยกว่าคนที่ต้องการซื้อแจ้งเตือน
    return False,'ไม่พบสินค้า!' #ถ้ากรอก รหัสสินค้าผิดก็จะส่่งแจ้งเตือนกลับไป

def record_sale(pid,quantity,total_price):
    """
    บันทีกประวัติการขาย พร้อมอัพลง Data
    """
    import datetime #ดึงโมดูลเวลามาใช้
    inventory = storage.load_products()
    
    # คำนวณกำไร = (ราคาขายรวม - (ต้นทุนต่อชิ้น * จำนวนที่ขาย))
    cost_price = inventory[pid]['cost'] * quantity
    profit = total_price-cost_price
    
    with open(storage.SALES_FILE,'a', encoding='utf-8') as f: #เปิดไฟล์ แล้วก็ทำการเขียนข้อมูลลงไปโดยใช้ a คือการเขียนต่่อท้าย ข้อมูลเดิมที่มีอยู๋ ทำให้ประวัติไม่หาย
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #แสดงเวลาประวัติการขายเพื่อให้รู้ประวัติเวลา
        f.write(f'{timestamp}, ID:{pid},Name:{inventory[pid]["name"]} Qty: {quantity}, Total: {total_price}, Profit: {profit}\n') #เก็บข้อมูลประวัติ เวลา จำนวนที่ขาย ราคาทั้งหมด กำไรที่ได้
    return True

def get_store_financial_summary():
    """
    สรุปต้นทุนรวมทั้งหมด ยอดขายรวมที่คาดหวัง และกำไรที่่ควรจะได้จากสินค้าที่มีอยู่
    """
    inventory = storage.load_products()
    
    total_inventory_cost = 0 #ตัวแปรสำหรับรวม "ต้นทุนทั้งหมด" ของสินค้าที่มีอยู่ในร้าน
    total_expected_revenue = 0 #ตัวแปรสำหรับรวม "รายได้ทั้งหมด" ที่คาดว่าจะได้รับหากขายสินค้าในร้านได้จนหมด
    
    for pid, data in inventory.items(): #วนรูปข้อมูลจากไฟล์
        item_total_cost = data['cost'] * data['stock'] #เอา ราคาต้นทุนต่อชิ้น คูณกับ จำนวนที่เหลือในสต็อก
        item_expected_revenue = data['price'] * data['stock'] #เอา ราคาขายต่อชิ้น คูณกับ จำนวนที่เหลือในสต็อก
        
        total_inventory_cost += item_total_cost # เอาราคาต้นทุนของสินค้าทั้งหมดมารวมกันทั้งสต๊อก
        total_expected_revenue += item_expected_revenue #เอาราคากลางของสินค้ามารวมกันทั้งสต๊อก
    
    total_potential_profit = total_expected_revenue - total_inventory_cost #"รายได้คาดหวังทั้งหมด" ลบด้วย "ต้นทุนทั้งหมด" ผลลัพธ์ที่ได้คือ "กำไรสุทธิที่จะได้รับหากขายสินค้าที่มีอยู่ตอนนี้จนหมด"
    
    return {
        "total_cost": total_inventory_cost, #ราคาต้นทุน
        "total_revenue": total_expected_revenue, #ราคากลางสินค้า
        "potential_profit": total_potential_profit #กำไรสุทธิ คาดการ
    }        
        