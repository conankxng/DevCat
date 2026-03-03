#ฟังก์ชั่นดึงข้อมูลการขาย
import storage_product
import os
def product_sale_data():
    pass

#ฟังก์ชั่นสรุปยอดขายรวม และแสดงผลกำไร-ขาดทุน
def total_sale_Sumary():
   # ดึงข้อมูลจากสินค้าในสต้อกเพื่อเอาราคา และกำไร
    stock = storage_product.load_products() #inventory = stock 
    total_cost = 0 #ไว้รอเก็บต้นทุนรวม
    total_revenue = 0  #ไว้รอเก็บยอดขายรวม 

    

#ฟังก์ชั่นการแสดงประวัติสินค้า (ว่าสินค้าไหนทำกำไรได้มากที่สุด,น้อยที่สุด)
def product_report():
    pass
