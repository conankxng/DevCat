import storage_product as stock
import os
#ฟังก์ชั่นดึงข้อมูลการขาย
def product_sale_data():
    sale_data = stock.SALES_FILE  # อ้างอิงไฟล์จาก storage_product
    if os.path.exists(sale_data):  # เช็คว่าไฟล์มีอยู่จริงไหม
        with open(sale_data, "r", encoding="utf-8") as cat_data:  # เปิดไฟล์เพื่ออ่าน
            content = cat_data.read().strip()  #content มีไว้เก็บ ข้อมูลที่อ่านออกมาจากไฟล์  #.strip()ตัดช่องว่างหน้า-หลัง
            if content: #ถ้าcontentไม่ว่าง ให้คืนค่าเป็น float(content)
                return float(content) 
            else: #ถ้า contentว่าง ให้คืนค่าเป็น 0.0
                return 0.0
    return 0.0

#ฟังก์ชั่นคำนวณรายจ่าย
def calculate_expenses():
    inventory = stock.load_products() # ฟังก์ชั่นสำหรับดึงข้อมูลจากไฟล์ ออกมาเก็บในรูปแบบ Dictionary
   

    total_cost = 0.0 #ตัวแปรสำหรับเก็บต้นทุนทั้งหมด
    # ต้นทุนคือ 70% ของราคาขาย ปล.ไม่อยากทำไฟล์ต้นทุนเลยเอาเป็น70%จากราคาสินค้า

    total_cost = sum(int(item['stock'])*(item['price']*0.7)) for item in inventory.val
    return total_cost

#ฟังก์ชั่นการแสดงประวัติสินค้า
def product_report():
    pass
