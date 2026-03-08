"""
ไฟล์นี้รวบรวมฟังก์ชันด้าน Logic ทั้งหมดของระบบ POS
"""
import os
import product_manager
import member_manager
import sales_logger
from datetime import datetime


# ========================================================================= #
# ตัวแปร Global สำหรับจำสถานะ
# ========================================================================= #
# จำสินค้าที่ถูกเลือกล่าสุดจากหน้าจอซ้าย
current_selected_product = {"id": None, "name": None}
# จำข้อมูลสมาชิกที่ Login อยู่ในขณะนี้
current_member_info = {"phone": None, "first_name": None, "last_name": None}


# ========================================================================= #
# ฟังก์ชันเกี่ยวกับสมาชิก (Member)
# ========================================================================= #
def do_login_member(phone):
    """
    ตรวจสอบเบอร์โทรศัพท์ในระบบสมาชิก
    """
    return member_manager.get_member(phone)

def save_member_to_state(mem):
    """
    บันทึกข้อมูลสมาชิกที่ Login สำเร็จลงใน (Global State)
    """
    global current_member_info
    current_member_info["phone"] = mem["phone"]
    current_member_info["first_name"] = mem["first_name"]
    current_member_info["last_name"] = mem["last_name"]


def logout_member_state():
    """
    ล้างข้อมูลสมาชิกออกจาก Global State
    """
    global current_member_info
    current_member_info = {"phone": None, "first_name": None, "last_name": None}


def do_register_member(phone, fname, lname):
    """
    ลงทะเบียนสมาชิกใหม่
    """
    return member_manager.register_member(phone, fname, lname)


def is_member_logged_in():
    """
    ตรวจสอบว่ามีสมาชิก Login อยู่หรือไม่
    คืนค่า True ถ้ามีสมาชิก Login อยู่
    """
    return current_member_info["phone"] is not None


# ========================================================================= #
# ฟังก์ชันเกี่ยวกับตะกร้าสินค้า
# ========================================================================= #
def get_bill_path():
    """
    คืนค่า Path เต็มของไฟล์บิลปัจจุบัน (bill.txt)
    """
    return os.path.join(os.path.dirname(__file__), "data", "bill.txt")


def read_bill_lines():
    """
    อ่านบิลปัจจุบันจากไฟล์และคืนค่าเป็น list ของ dict แต่ละรายการสินค้า
    """
    bill_path = get_bill_path()
    items = []
    if os.path.exists(bill_path):
        with open(bill_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split(",") #คั่นข้อมูล ลบช่องว่าง
            if len(parts) == 5:
                pid, name, price, qty, total = parts
                items.append({
                    "pid": pid,
                    "name": name,
                    "price": float(price),
                    "qty": int(qty),
                    "total": float(total),
                })
    return items


def clear_bill_file():
    """
    ล้างไฟล์บิลให้ว่างเปล่า
    """
    open(get_bill_path(), "w").close()


def calculate_totals(raw_total):
    """
    คำนวณสรุปยอด: ส่วนลดสมาชิก, VAT, และยอดสุทธิ
    """
    discount = raw_total * 0.25 if is_member_logged_in() else 0.0 #ถ้าเป็นสมาชิกลด 25%
    after_discount = raw_total - discount
    vat = after_discount * 0.07
    grand_total = after_discount + vat
    return {
        "subtotal": raw_total,
        "discount": discount,
        "vat": vat,
        "grand_total": grand_total,
    }


def add_item_to_bill(pid, name, price, qty):
    """
    เพิ่มสินค้าลงใน bill.txt และตรวจสอบสต็อกก่อนเพิ่ม
    """
    inventory = product_manager.get_all_products()
    if pid not in inventory or inventory[pid]["stock"] < qty:
        return False, "สินค้าในสต็อกไม่เพียงพอ!"

    total_price = price * qty
    bill_path = get_bill_path()
    with open(bill_path, "a", encoding="utf-8") as f:
        f.write(f"{pid},{name},{price:.2f},{qty},{total_price:.2f}\n")
    return True, "เพิ่มลงตะกร้าเรียบร้อยแล้ว"

def get_product_price(pid):
    """
    ดึงราคาสินค้าจากคลังสินค้า
    """
    inventory = product_manager.get_all_products()
    if pid in inventory:
        return float(inventory[pid].get("price", 0.0))
    return 0.0


# ========================================================================= #
# ฟังก์ชันเกี่ยวกับการพักบิล
# ========================================================================= #
def get_hold_dir():
    """
    คืนค่า Path ของโฟลเดอร์เก็บบิลพัก
    """
    return os.path.join(os.path.dirname(__file__), "data", "hold_bills")


def hold_bill():
    """
    ย้ายบิลปัจจุบันไปพักไว้ในโฟลเดอร์ hold_bills
    """
    bill_path = get_bill_path()
    if not os.path.exists(bill_path):
        return False, "ไม่มีสินค้าในตะกร้า!"

    with open(bill_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        return False, "ไม่มีสินค้าในตะกร้า!"

    hold_dir = get_hold_dir()
    os.makedirs(hold_dir, exist_ok=True)

    # ตั้งชื่อไฟล์เป็น วัน-เดือน-ปี_ชั่วโมง-นาที
    timestamp = datetime.now().strftime("%d-%m-%Y  %H-%M")
    hold_file = os.path.join(hold_dir, f"bill_{timestamp}.txt")

    with open(hold_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    clear_bill_file()
    return True, f"พักบิลไว้เรียบร้อย\n{timestamp}"


def get_held_bill_files():
    """
    คืนค่า list ชื่อไฟล์บิลที่ถูกพักไว้ทั้งหมด
    """
    hold_dir = get_hold_dir()
    os.makedirs(hold_dir, exist_ok=True) #ตรวจสอบว่ามีโฟลเดอร์นี้อยู่ไหม ถ้าไม่มีก็สร้างขึ้นมา
    return [f for f in os.listdir(hold_dir) if f.endswith(".txt")] #เอาแค่ txt


def recall_bill(selected_file):
    """
    เรียกคืนบิลที่พักไว้ มาเพิ่มต่อใน bill.txt ปัจจุบัน แล้วลบไฟล์พักทิ้ง
    """
    hold_dir = get_hold_dir()
    hold_path = os.path.join(hold_dir, selected_file)

    with open(hold_path, "r", encoding="utf-8") as hf:
        hold_lines = hf.readlines()

    with open(get_bill_path(), "a", encoding="utf-8") as bf:
        bf.writelines(hold_lines)

    os.remove(hold_path)
    return True, "เรียกบิลเรียบร้อยแล้ว เพิ่มสินค้าลงตะกร้าแล้ว"


# ========================================================================= #
# ฟังก์ชันเกี่ยวกับการชำระเงิน
# ========================================================================= #
def process_checkout():
    """
    ดำเนินการชำระเงิน: ตัดสต็อก, บันทึกการขาย, และสร้างใบเสร็จ
    """
    bill_path = get_bill_path()

    if not os.path.exists(bill_path):
        return False, "ไม่มีสินค้าในตะกร้า!", None

    with open(bill_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        return False, "ไม่มีสินค้าในตะกร้า!", None

    all_success = True
    error_msgs = []
    receipt_items = []
    total_sum = 0.0

    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 5:
            pid, name, price, qty, total = parts
            success, msg = product_manager.process_sale(pid, int(qty))
            if not success:
                all_success = False
                error_msgs.append(f"{name}: {msg}")
            else:
                product_manager.record_sale(pid, int(qty), float(total))
                receipt_items.append({
                    "name": name,
                    "qty": int(qty),
                    "price": float(price),
                    "total": float(total),
                })
                total_sum += float(total)

    if not all_success:
        errors = "\n".join(error_msgs)
        clear_bill_file()
        return False, f"สต๊อกไม่พอ:\n{errors}\n*ระบบเคลียร์ตะกร้าแล้ว", None

    # คำนวณยอดสุดท้าย
    totals = calculate_totals(total_sum)

    # บันทึกการขายและสร้างใบเสร็จ PDF
    pdf_file = None
    try:
        pdf_file = sales_logger.record_sale(
            items=receipt_items,
            subtotal=totals["subtotal"],
            discount=totals["discount"],
            vat=totals["vat"],
            grand_total=totals["grand_total"],
            member_info=current_member_info,
        )
    except Exception as e:
        pass  # ถ้าสร้าง PDF ไม่ได้ก็ไม่เป็นไร

    clear_bill_file()
    return True, "ชำระเงินสำเร็จ", pdf_file


# ========================================================================= #
# ฟังก์ชันเกี่ยวกับสินค้า (Products)
# ========================================================================= #

def get_all_products_filtered(search_keyword=""):
    """
    อ่านรายการสินค้าทั้งหมดจากไฟล์ products.txt และกรองตามคำค้นหา
    พารามิเตอร์:
        search_keyword (str): คำที่ต้องการค้นหา (ค้นได้ทั้งชื่อและรหัสสินค้า)
    คืนค่า: list of dict (product_id, product_name)
    """
    file_path = os.path.join(os.path.dirname(__file__), "data", "products.txt")
    products = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        kw = search_keyword.strip().lower()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) >= 2:
                product_id = parts[0]
                product_name = parts[1]
                # กรองตามคำค้นหา
                if kw and kw not in product_name.lower() and kw not in product_id.lower():
                    continue
                products.append({"id": product_id, "name": product_name})

    except FileNotFoundError:
        pass  # คืนค่า list ว่างถ้าไม่มีไฟล์

    return products
