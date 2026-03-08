import product_manager
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
    if os.path.exists(cost_data):
        total_costs_list = [] # เปลี่ยนชื่อให้สื่อความหมายว่าเป็น "ต้นทุนรวม"
        with open(cost_data, 'r', encoding='utf-8') as f:
            lines = f.readlines() 
            for line in lines:
                line = line.strip()
                if line: 
                    try:
                        parts = line.split(',')
                        # ดึงค่าตามที่คุณต้องการ:
                        # parts[-1] คือ ต้นทุนต่อหน่วย (Cost per unit)
                        # parts[-3] คือ จำนวน (Quantity)
                        unit_cost = float(parts[-1].strip())
                        quantity = float(parts[-3].strip())
                        
                        # นำมาคูณกันตามโจทย์
                        line_total_cost = unit_cost * quantity
                        
                        total_costs_list.append(line_total_cost)
                    except (ValueError, IndexError):
                        # ถ้าแปลงเลขไม่ได้ หรือ index ไม่ครบ ให้ใส่ 0.0
                        total_costs_list.append(0.0)
        return total_costs_list
    return []

#ฟังก์ชั่นแสดงรายจ่ายรวมทั้งหมด
def total_expense():
    expense = product_cost_data()
    return sum(expense) #sumเพื่อรวม

#ฟังก์ชั่นที่แสดงว่าสินค้าขายดี
def product_report():
    inventory = manage.best_seller(threshold=20) # เรียกใช้ฟังก์ชันจาก product_manager 
    return inventory


# #ฟังก์ชันค้นหาประวัติจากขายแบบ Custom ผ่านวัน/เดือน/ปี ปล.จริงๆให้ใส่เปน ปี เดือน วัน
# def search_sale_history_custom(year,month,day):
#     # เป็น แปลงint เพื่อให้จัดรูปแบบวันที่ให้เปน YYYY-MM-DD เรียงแบบนี้เพือให้ตรงกับไฟล์ sale.txt
#     search_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}" #เกบวันที่
#     #d = แสดงเป็นตัวเลขจำนวนเต็ม #ใช้ :04d :02d :02d เพื่อกำหนดจำนวนอักษรให้ตรงตามล็อค ใส่0 เพื่อเติมในเดือนที่เป็นเลขตัวเดียว

#     sale_data = stock.SALES_FILE
#     results = [] #ใช้เก็บเนื้อหาที่ค้นเจอ
    
#     if os.path.exists(sale_data): #ตรวจสอบว่าไฟล์sale_data มีอยู่จริงไหม
#         with open(sale_data,'r',encoding='utf-8') as f:
#             lines = f.readlines() #อ่านไฟล์ในบรรทัด
#             for line in lines: #ลูปให้อ่านแต่ละบรรทัด
#                 line = line.strip() #ตัดช่องว่างหน้า-หลัง
#                 if line:
#                     if line.startswith(search_date): #ถ้าบรรทัดนั้นขึ้นต้นด้วยวันในsearch_date 
#                         results.append(line)  #ให้เก็บผลลัพนั้นลงใน results เปน line
#     return results

#ฟังก์ชันค้นหาประวัติจากขายโดยระบุแค่วัน
def show_day_sales():

    # ดึงข้อมูลวัน/เดือน/ปี จากระบบ
    now = datetime.now()

    day_sales = now.strftime("%Y-%m-%d") #.srtftime คือเพื่อดึงเฉพาะตัวเลขในวันที่ให้กลายเป็นสตริงเพื่อใช้ในการค้หา
    sale_data = stock.SALES_FILE
    total_sales = 0.0

    if os.path.exists(sale_data): #ตรวจสอบว่าไฟล์ sale_data ว่ามีอยู่จริงบ่
        with open(sale_data, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip() #ตัดช่องว่างหน้า-หลัง
                #สร้างเงื่อนไขตรวจสอบว่าบรรทัดนั้นขึ้นต้นด้วยวันที่หรือไม่
                if line.startswith(day_sales):
                    try:
                        parts = line.split(',')
                        for part in parts:
                            if "Total:" in part:
                                total_value = float(part.split(':')[1].strip())
                                total_sales += total_value
                                break
                    except:
                        pass
    return f"{total_sales:.2f}"


#ฟังก์ชันค้นหาประวัติจากขายโดยระบุแค่เดือน
def show_month_sales():
    # ดึงข้อมูลวัน/เดือน/ปี จากระบบ
    now = datetime.now() #ตัวแปรเก็บdatetimeแล้วใช้เมดธอด.now
    #.srtftime คือเพื่อดึงเฉพาะตัวเลขในเดือนให้กลายเป็นสตริงเพื่อใช้ในการค้หา
    month_sales = now.strftime("%Y-%m")
    sale_data = stock.SALES_FILE
    total_sales = 0.0

    if os.path.exists(sale_data): #ตรวจสอบว่าไฟล์ sale_data ว่ามีอยู่จริงบ่
        with open(sale_data, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip() #ตัดช่องว่างหน้า-หลัง
                #สร้างเงื่อนไขตรวจสอบว่าบรรทัดนั้นขึ้นต้นด้วยเดือนหรือไม่
                if line.startswith(month_sales):
                    try:
                        parts = line.split(',')
                        for part in parts:
                            if "Total:" in part:
                                total_value = float(part.split(':')[1].strip())
                                total_sales += total_value
                                break
                    except:
                        pass
    return f"{total_sales:.2f}"

#ฟังก์ชันค้นหาประวัติจากขายโดยระบุแค่ปี
def show_year_sales():
    #ดึงข้อมูลวัน/เดือน/ปี จากระบบ
    now = datetime.now()
    #.srtftime คือเพื่อดึงเฉพาะตัวเลขในปีให้กลายเป็นสตริงเพื่อใช้ในการค้หา
    year_sales = now.strftime("%Y")
    sale_data = stock.SALES_FILE
    total_sales = 0.0

    if os.path.exists(sale_data): #ตรวจสอบว่าไฟล์ sale_data ว่ามีอยู่จริงบ่
        with open(sale_data, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip() #ตัดช่องว่างหน้า-หลัง
                #สร้างเงื่อนไขตรวจสอบว่าบรรทัดนั้นขึ้นต้นด้วยปีหรือไม่
                if line.startswith(year_sales):
                    try:
                        parts = line.split(',')
                        for part in parts:
                            if "Total:" in part:
                                total_value = float(part.split(':')[1].strip())
                                total_sales += total_value
                                break
                    except:
                        pass
    return f"{total_sales:.2f}"

#ฟังก์ชันแสดงจำนวนสมาชิกทั้งหมด
def total_members():
    member_file = os.path.join(stock.DATA_DIR, "members.txt")
    count = 0
    if os.path.exists(member_file):
        with open(member_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    count += 1
    return count

# ฟังก์ชันดึงข้อมูลจาก master_sales.txt เพื่อไปแสดงในตาราง
def get_master_sales_data(days_filter=None):
    master_file = os.path.join(stock.DATA_DIR, "master_sales.txt")
    sales_list = []
    
    now = datetime.now()
    
    if os.path.exists(master_file):
        with open(master_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # ตัวอย่างบรรทัด: [2026-03-05 22:45:10] Total: 7490.00 THB | General Customer | Items: 2
                    try:
                        # แยกส่วนวันที่และเวลาออกจากข้อความที่เหลือ
                        date_part, rest = line.split('] ', 1)
                        date_str = date_part.replace('[', '').strip()
                        
                        if days_filter is not None:
                            try:
                                # แปลงจาก string เป็น datetime เพื่อคำนวณระยะห่าง
                                row_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                                if (now - row_date).days > days_filter:
                                    continue
                            except ValueError:
                                pass
                        
                        # แยกข้อมูลที่เหลือด้วย "|"
                        parts = [p.strip() for p in rest.split('|')]
                        
                        # ดึงข้อมูลแต่ละส่วน
                        total_str = parts[0].replace('Total:', '').strip()
                        customer_str = parts[1].strip()
                        items_str = parts[2].replace('Items:', '').strip()
                        
                        sales_list.append({
                            "date": date_str,
                            "customer": customer_str,
                            "items": items_str,
                            "total": total_str
                        })
                    except Exception as e:
                        pass
    return sales_list

# a = search_sale_history_custom("2026","03","05") #ทดสอบฟังก์ชันค้นหาประวัติจากขายแบบ Custom ผ่านวัน/เดือน/ปี
# print(a)
# y = show_year_sales()
# m = show_month_sales()
# d = show_day_sales()

# print(f"{y=}, {m=}, {d=}")
# a = total_revenue()
# print(a)
'''
print(show_day_sales())
print(show_month_sales())
print(show_year_sales())
'''