import storage_product as stock
import os 

best_seller_limit = 50 #สินค้าขายดีต้องมีเกณฑ์ขายเหลือในสต้อกแค่ 50ชิ้นลงไป

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
    return sum(revenue) #sumเพื่อรวม

#ฟังก์ชันแสดงจ่ายรวมทั้งหมด
def product_cost_data():
    cost_data = stock.FILE_NAME 
    if os.path.exists(cost_data): #เช็คว่าไฟล์มีอยู่จริงไหม
        costs = [] #สร้างลิสต์ว่าง ไว้เก็บข้อมูลยอดขายที่ดึงออกมาจากไฟล์ FILE_NAME  ทีละบรรทัด
        with open(cost_data,'r',encoding='utf-8') as f: #เปิดไฟล์เพื่ออ่านเป็นภาษาไทย
            lines= f.readlines() #อ่าน f ทีละบรรทัด
            for line in lines: #วนลูปเพื่ออ่านข้อมูลทีละบรรทัด
                line = line.strip() #.strip เพื่อตัดช่องว่างหัว-ท้าย
                if line: 
                    try:
                        parts = line.split(',') #แยกส่วนข้อมูลแต่ละพาร์ท ตามลูกน้ำ
                        # cost_value คือข้อมูลต้นทุนที่อยู่ใน FILE_NAME โดยคอลั่มท้ายสุดคือต้นทุน
                        cost_value = float(parts[-1].strip()) #ตัดช่องว่างหัวท้าย
                        costs.append(cost_value)
                    except :
                        costs.append(0.0) #ถ้าเกิดerror ระหว่างการแปลงค่า ให้ใส่ 0.0 ลงไปแทน
        return costs
    return []

#ฟังก์ชั่นแสดงรายจ่ายรวมทั้งหมด
def total_expense():
    expense = product_cost_data()
    return sum(expense) #sumเพื่อรวม

#ฟังก์ชั่นที่แสดงว่าสินค้าขายดี และ สินค้าใดที่ขายไม่ดี
def product_report():
    inventory = stock.load_products() #ฟังก์ชั่นดึงข้อมูลจาก storage_product
    good_product = []
    not_good_product = []
    for pid,data in inventory.items(): #วนลูปผ่านสินค้าทั้งหมดใน inventory
        item = {'name': data['name'],'stock': data['stock']} #Dictionary

        #สร้างเงื่อนไขว่าอันไหนเป็น สินค้าที่ดี และ เป็นสินค้าที่ไม่ดี
        # 
        if  int(data['stock']) < best_seller_limit :
            good_product.append(item) #เก็บข้อมูลไป list ไปเก็บไว้ในตัวแปร good_product
        else :
            not_good_product.append(item) #เก็บข้อมูลไป list ไปเก็บไว้ในตัวแปร not_good_product
    return (good_product,not_good_product)


#ฟังก์ชันค้นหาประวัติจากขาย ผ่าน วัน/เดือน/ปี 
def search_sale_history():
    pass

print(product_sale_data())
print(total_revenue())
print(product_cost_data())
print(total_expense())