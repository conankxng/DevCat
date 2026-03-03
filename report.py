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

#ฟังก์ชันสำหรับคำนวณรายจ่ายรวมทั้งหมด
def calculate_expenses():
    inventory = stock.load_products() #ฟังก์ชั่นดึงข้อมูลจากไฟล์
    total_cost = 0.0 # ตัวแปรสำหรับเก็บต้นทุนทั้งหมด
    #วนลูปสินค้าall
    for pid,data in inventory.item():
        #ดึงจำนวนสินค้าและราคาต้นทุนต่อชิ่้น
        stock_product = int(data['stock']) #จำนวนสินค้าในสต้อก และแปลงเปน int
        cost_price = float(data['cost']) #ราคาต้นทุนต่อชิ้น และแปลงข้อมูลเปน float

        #คำนวนต้นทุนทั้งหมดของสินค้า
        #product_cost = ต้นทุนสินค้าall
        product_cost = stock_product*cost_price #จำนวนสินค้า*ราคาต้นทุนต่อชิ้น

        #บวกเข้ากับtotal_cost ที่ใช้เก็บต้นทุนทั้งหมด
        total_cost = total_cost + product_cost
#คืนค่าต้นทุนรวมall
    return total_cost



#ฟังก์ชั่นการแสดงประวัติสินค้า
def product_report():
    inventory = stock.load_products() #ฟังก์ชั่นดึงข้อมูลจากไฟล์ 
    good_product = []
    not_good_product = []
    for pid,item in inventory.item(): #วนลูปผ่านสินค้าทั้งหมดใน inventory
        item = {'name': data['name'],'stock': data['stock']} #Dictionary

        #สร้างเงื่อนไขว่าอันไหนเป็น สินค้าที่ดี และ เป็นสินค้าที่ไม่ดี
        if data ['stock']<50 :
            good_product.append(item) #เก็บข้อมูลไป list ไปเก็บไว้ในตัวแปร good_product
        else :
            not_good_product.append(item) #เก็บข้อมูลไป list ไปเก็บไว้ในตัวแปร not_good_product
    return (good_product,not_good_product)
        
