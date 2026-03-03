import storage_product as storage

def add_product(pid,name,price,stock):
    """
    ฟังก์ชันสำหรับเพิ่มสินค้า
    คืนค่า: (สถานะความสำเร็จ True/False, ข้อความแจ้งเตือน)
    """
    inventory = storage.load_products() #เรียกฟังก์ชันในไฟล์เก็บข้อมูลเพื่อดึงรายการสินค้า มาเก็บในตัวแปร เป็นDictionary
    
    if pid in inventory:
        return False, f'เกิดข้อผิดพลาด: รหัสสินค้า "{pid}" มีอยู่แล้ว!' #เช็คว่ารหัสสินค้าซ้ำกับที่่อยู่ในระบบไหม หาซ้ำจะหยุดทำงานและส่งค่่า False
    
    #เพิ่มช้อมูลลง Dictionary
    inventory[pid] = {'name':name, "price":price, "stock":stock} #หากไม่่ซ้ำก็จะทำการสร้างข้อมูลเก็บเข้าไปใน inventory โดยใช้ pid เป็นคีย์หลัก
    storage.save_products(inventory) #เมื่อเพิ่มข้อมูลในตัวแปรเสร็จ ก็สั่งบันทึกทับลงไปในไฟล์ฟังก์ชั่่น save_products
    return True, "สำเร็จ: เพิ่มสินค้าเรียบร้อยแล้ว!" #เมื่อทำงานครบทุกขั้นตอน จะส่งค่า True (สำเร็จ) พร้อมข้อความยืนยันกลับไป

def get_all_products():
    """
    ฟังก์ชันสำหรับดึงข้อมูลสินค้าทั้งหมด
    เพื่่อให้หน้าจอ GUI นำไปวนลูปแแสดงในตาราง
    """
    return storage.load_products() #ไปดึงไฟล์ออกมาเพื่อจะเอาไปแสดง

def update_product(pid,name,price,stock):
    """
    ฟังก์ชันสำหรับแก้ไขข้อมูลสินค้า
    คืนค่าเป็น True/False ,เพื่อแจ้งเตือน
    """
    inventory = storage.load_products()
    
    if pid not in inventory:
        return False, 'แจ้งเตือน: ไม่พบรหัสสินค้านี้ในระบบ!'
    
    inventory[pid]["name"] = name
    inventory[pid]["price"] = price
    inventory[pid]["stock"] = stock
    
    storage.save_products(inventory)
    return True,"สำเร็จ: แก้ไขสินค้าเรียบร้อยแล้ว!"

def delete_product(pid):
    """
    ฟังก์ชันสำหรับลบสินค้า
    คืนค่า: (สถานะความสำเร็จ True/False, ข้อความแจ้งเตือน)
    """
    
    inventory = storage.load_products() #โหลดข้อมูลสินค้าแล้วมาเก็บในตัวแปร
    
    if pid not in inventory:
        return False,"แจ้งเตือน: ไม่พบรหัสสินค้านี้ในระบบ!" #เช็คว่ามีรหัสสินค้าไหมถ้าไม่มี return แจ้งเตือนกลับ
    
    del inventory[pid] #ถ้ามีก็มาเข้าเงื่อนไขนี้ก็คือ คำสั่ง del คือลบข้อมูลทั้งหมด
    storage.save_products(inventory) #แล้วก็ทำการเซฟข้อมูลใหม่ลงไป
    return True,"สำเร็จ: ลบสินค้าเรียบร้อยแล้ว!" #return ค่ากลับพร้อมแจ้งเตือน


def get_low_stock_list(threshold=5):
    """
    ฟังก์ชันสำหรับเช็คสินค้าใกล้หมด
    คืนค่า: รายชื่อสินค้าที่เป็น List เพื่อให้ GUI นำไปแสดง Popup หรือ Label
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