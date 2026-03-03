#ฟังก์ชั่นดึงข้อมูลการขาย

import storage_product as stock
import os
def product_sale_data():
    sale_data = stock.SALES_FILE  # อ้างอิงไฟล์จาก storage_product
    if os.path.exists(sale_data):  # เช็คว่าไฟล์มีอยู่จริงไหม
        with open(sale_data, "r", encoding="utf-8") as cat_data:  # เปิดไฟล์เพื่ออ่าน
            content = cat_data.read().strip()  #อ่านข้อมูล #.strip()ตัดช่องว่างหน้า-หลัง
            if content: 
                return float(content)
            else:
                return 0.0
    return 0.0

#ฟังก์ชั่นสรุปยอดขายรวม