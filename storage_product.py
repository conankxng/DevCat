import os

DATA_DIR = "data"  # ชื่อโฟเดอร์ที่จะเก็บข้อมูลสต๊อกสินค้า
os.makedirs(DATA_DIR, exist_ok=True)  # exist_ok=True จะไม่เกิด error ถ้ามีโฟลเดอร์อออยู่แล้ว


# สร้างไฟล์ลิงค์ไปในโฟเดอร์ขของ Data แล้วทำการสร้างไฟล์ (os.path.join) คือสำหรับเส้นทางไฟล์ เพราะ Windows กับ Mac \ / มันต่างกัน
FILE_NAME = os.path.join(DATA_DIR, "products.txt")
SALES_FILE = os.path.join(DATA_DIR, "sales.txt")


def load_products():
    """
    ฟังก์ชั่นสำหรับดึงข้อมูลจากไฟล์ ออกมาเก็บในรูปแบบ Dictionary
    """
    inventory = {} #สำหรับเก็บข้อมูลสินค้า
    if os.path.exists(FILE_NAME): #สำหรับเช็คว่าไฟล์มีอยู่ไหม
        with open(FILE_NAME,'r', encoding="utf-8") as f: #อ่านข้อมูลไฟล์เปิดแค่อ่านเฉยๆ
            for line in f: #วนลูปไฟล์ที่เปิดอ่านที่ละบรรทัด
                parts = line.strip().split(",") #แยกข้อมูล strip()ลบช่องว่างและลบ\n split(",") แยกข้อมูลตามเครืี่องหมาย , แล้วก็เก็บเข้าตัวแปรเป็น list
                if len(parts) == 5: # เช็คข้อมูลว่ามีครบ 5 ช่องไหม
                    pid, name, stock, price, cost = parts # การเอาค่าใน list มาใส่ตัวแปรที่ละตัว
                    inventory[pid] = {  #เก็บข้อมูลลง Dictionary
                        "name":name,
                        "stock":int(stock),
                        "price":float(price),
                        "cost":float(cost)
                    }
    return inventory

def save_products(inventory):
    """
    ฟังก์ชั่นสำหรับบันทึกข้อมูลสินค้า ระบบ(Dictionary) และเขียนทับลงไฟล์เดิม
    """
    with open(FILE_NAME, "w", encoding="utf-8") as f: #เปิดไฟล์ แล้วก็เขียนทับไฟล์เดิมทั้งหมด
        for pid, data in inventory.items(): #วนลูปข้อมูล pid คือ Idสินค้าก็คือ key | ส่วนData ก็คือข้อมูลที่กำหนดไว้
            f.write(f"{pid},{data['name']},{data['stock']},{data['price']},{data['cost']}\n") #เขียนทับไฟล์ด้วยข้อมูลดั้งนี้

