import storage_product as stock
import product_manager as manage
from datetime import datetime #นำเข้าเพื่อดึงปีและเดือนปัจจุบัน
import os 

#ฟังก์ชั่นแสดงข้อมูลการขาย
def product_sale_data():
    sale_data = stock.SALES_FILE 
    if os.path.exists(sale_data): #เช็คว่าไฟล์มีอยู่จริงไหม
        sales = [] #สร้างลิสต์ว่าง ไว้เก็บข้อมูลยอดขายที่ดึงออกมาจากไฟล์ SALES_FILE  ทีละบรรทัด
        with open(sale_data,'r',encoding='utf-8') as f: #เปิดไฟล์เพื่ออ่านเป็นภาษาไทย
            lines= f.readlines() #อ่าน f ทีละบรรทัด
            for line in lines: #วนลูปเพื่ออ่านข้อมูลทีละบรรทัด
                line = line.strip() #.strip เพื่อตัดช่องว่างหัว-ท้าย
                if line: 
                    try:
                        parts = line.split(',') #แยกส่วนข้อมูลแต่ละพาร์ท ตามลูกน้ำ
                        # total_str คือข้อมูลยอดขายที่อยู่ใน SALES_FILE 
                        total_str = [item for item in parts if "Total:" in item] # หาค่าที่ขึ้นต้นด้วย "Total:"
                        if total_str:
                            #แปลงข้อมูลเป็น float #เข้าถึงค่าภายในด้วย index เพื่อเอายอดขาย #ใช้split()เพื่อเอาโคล่อนออก
                            total_value = float(total_str[0].split(':')[1].strip()) 
                            sales.append(total_value) #.append เพื่อเพิ่มtotal_valueเข้าไปเก็บเพิ่มในlist
                        else : 
                            # ถ้า total_str ไม่มีค่า "Total:" .ให้ใส่ 0.0 ลงไปแทน
                            sales.append(0.0)
                    except :
                        sales.append(0.0) #ถ้าเกิดerror ระหว่างการแปลงค่า ให้ใส่ 0.0 ลงไปแทน
        return sales
    return []

#ฟังก์ชั่นแสดงรายรับรวมทั้งหมด
def total_revenue():
    revenue = product_sale_data()
    return sum(revenue) #sumเพื่อรวมยอดขาย

#ฟังก์ชันแสดงรายจ่าย หรือ ต้นทุน
def product_cost_data():
    cost_data = stock.FILE_NAME 
    if os.path.exists(cost_data): #เช็คว่าไฟล์มีอยู่จริงไหม
        costs = [] #สร้างลิสต์ว่าง ไว้เก็บข้อมูลรายจ่ายที่ดึงออกมาจากไฟล์ FILE_NAME  ทีละบรรทัด
        with open(cost_data,'r',encoding='utf-8') as f: #เปิดไฟล์เพื่ออ่าน เป็นภาษาไทย
            lines= f.readlines() 
            for line in lines: #วนลูปเพื่ออ่านข้อมูลทีละบรรทัด
                line = line.strip() #.strip เพื่อตัดช่องว่างหัว-ท้าย
                if line: 
                    try:
                        parts = line.split(',') #แยกส่วนข้อมูลแต่ละพาร์ท ตามลูกน้ำ
                        # cost_value คือข้อมูลต้นทุนที่อยู่ใน FILE_NAME โดยคอลั่มท้ายสุดคือต้นทุน
                        cost_value = float(parts[-1].strip()) #ตัดช่องว่างหัวท้าย
                        costs.append(cost_value) #เก็บcost_valueไปไว้ในcost
                    except :
                        costs.append(0.0) #ถ้าเกิดerror ระหว่างการแปลงค่า ให้ใส่ 0.0 ลงไปแทน
        return costs
    return []

#ฟังก์ชั่นแสดงรายจ่ายรวมทั้งหมด
def total_expense():
    expense = product_cost_data()
    return sum(expense) #sumเพื่อรวม

#ฟังก์ชั่นที่แสดงว่าสินค้าขายดี
def product_report(): 
    inventory = manage.best_seller() # เรียกใช้ฟังก์ชันจาก product_manager 
    return inventory


#ฟังก์ชันค้นหาประวัติจากขายแบบ Custom ผ่านวัน/เดือน/ปี 
def search_sale_history_custom(year,month,day):
    # เป็น แปลงint เพื่อให้จัดรูปแบบวันที่ให้เปน YYYY-MM-DD เรียงแบบนี้เพือให้ตรงกับไฟล์ sale.txt
    search_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}" #เกบวันที่
    #d = แสดงเป็นตัวเลขจำนวนเต็ม #ใช้ :04d :02d :02d เพื่อกำหนดจำนวนอักษรให้ตรงตามล็อค ใส่0 เพื่อเติมในเดือนที่เป็นเลขตัวเดียว

    sale_data = stock.SALES_FILE
    results = [] #ใช้เก็บเนื้อหาที่ค้นเจอ
    
    if os.path.exists(sale_data): #ตรวจสอบว่าไฟล์sale_data มีอยู่จริงไหม
        with open(sale_data,'r',encoding='utf-8') as f:
            lines = f.readlines() #อ่านไฟล์ในบรรทัด
            for line in lines: #ลูปให้อ่านแต่ละบรรทัด
                line = line.strip() #ตัดช่องว่างหน้า-หลัง
                if line:
                    if line.startswith(search_date): #ถ้าบรรทัดนั้นขึ้นต้นด้วยsearch_date 
                        results.append(line)  #ให้เก็บผลลัพนั้นลงใน results เปน line
    return results

#ฟังก์ชันค้นหาประวัติจากขายโดยระบุแค่ วัน
import os
from datetime import datetime

import os
from datetime import datetime

def show_today_sales():
    # 1. ดึงข้อมูลวัน/เดือน/ปี จากระบบ
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d") # ใช้สำหรับค้นหาในไฟล์ (เช่น 2026-03-07)
    month_str = now.strftime("%Y-%m") 
    year_str = now.strftime("%Y")
    
    # ดึงเฉพาะ "วัน" ออกมา (เลือกใช้อย่างใดอย่างหนึ่งตามงานของคุณ)
    today_day_num = now.day              # แบบตัวเลข (เช่น 7)
    
    sale_data = stock.SALES_FILE
    results = []
    total_sales_count = 0

    # พิมพ์หัวข้อโชว์วันที่และ "วัน" เฉพาะเจาะจง
    print(f"--- รายงานการขายประจำวันที่ {today_day_num} (Full: {today_str}) ---")

    if os.path.exists(sale_data):
        with open(sale_data, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 2. ตรวจสอบว่าบรรทัดนั้นขึ้นต้นด้วยวันที่ของวันนี้หรือไม่
                if line.startswith(year_str):
                    results.append(line)
                    print(line)  
                    total_sales_count += 1
    
    # 3. สรุปผล
    if total_sales_count == 0:
        print(f"วันที่ {today_day_num} นี้ยังไม่มีรายการขาย")
    else:
        print(f"---------------------------------------")
        print(f"สรุป: วันนี้พบทั้งหมด {total_sales_count} รายการ")

    return results

# เรียกใช้งานฟังก์ชัน
show_today_sales()

# print(search_sale_history_day())