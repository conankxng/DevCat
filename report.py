import storage_product as stock
import product_manager as manage
import os

#ฟังก์ชั่นดึงข้อมูลการขาย
def product_sale_data():
    sale_data = stock.SALES_FILE  # อ้างอิงไฟล์จาก storage_product
    if os.path.exists(sale_data):  # เช็คว่าไฟล์มีอยู่จริงไหม
        with open(sale_data, 'r', encoding='utf-8') as cat_data:  # เปิดไฟล์เพื่ออ่าน
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

    for pid,item in inventory.item():# วนลูปผ่านสินค้าทั้งหมดใน inventory
        stock_a = int(item['stock']) #แปลงเป็น int
        sale_price = float (item['price']) #แปลงราคาขายเป็น float
    
    # cost = 



#ฟังก์ชั่นการแสดงประวัติสินค้า
def product_report():
    invemtory = stock.load_products() #ฟังก์ชั่นสำหรับดึงข้อมูลจากไฟล์ ออกมาเก็บในรูปแบบ Dictionary
    good_product = []
    not_good_product = []
    for pid,item in inventory.item(): #วนลูปผ่านสินค้าทั้งหมดใน inventory
        item = {'name': data['name'],'stock': data['stock']} #Dictionary

        #สร้างเงื่อนไขว่าอันไหนเป็น สินค้าที่ดี และ เป็นสินค้าที่ไม่ดี
        if data['stock']<50 :
            good_product.append(item) #เก็บข้อมูลไป list ไปเก็บไว้ในตัวแปร good_product
        else :
            not_good_product.append(item) #เก็บข้อมูลไป list ไปเก็บไว้ในตัวแปร not_good_product
    return (good_product,not_good_product)
        
