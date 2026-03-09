"""
=============================================================
ไฟล์ Logic ของระบบ POS
=============================================================
"""
import os
import product_manager
import member_manager
import sales_logger
from datetime import datetime


# ==============================================================
# ตัวแปร Global สำหรับเก็บสถานะปัจจุบันของ POS
# ==============================================================
# เก็บสินค้าที่ผู้ใช้เลือกล่าสุดจากรายการด้านซ้าย
current_selected_product = {"id": None, "name": None}
# เก็บข้อมูลสมาชิกที่กำลัง Login อยู่ตอนนี้
current_member_info = {"phone": None, "first_name": None, "last_name": None}


# ==============================================================
# กลุ่มฟังก์ชัน เกี่ยวกับสมาชิก (Member)
# ==============================================================
def do_login_member(phone):
    """
    ค้นหาสมาชิกในระบบจากเบอร์โทรศัพท์
    พารามิเตอร์ phone (str) เบอร์โทรศัพท์ที่ต้องการค้นหา
    คืนค่า dict ข้อมูลสมาชิกถ้าพบ None ถ้าไม่พบในระบบ
    """
    return member_manager.get_member(phone)  # ส่งต่อให้ member_manager ค้นหา


def save_member_to_state(mem):
    """
    บันทึกข้อมูลสมาชิกที่ Login สำเร็จลงใน Global State เพื่อให้ฟังก์ชันอื่นรู้ว่าตอนนี้มีสมาชิกใช้อยู่
    พารามิเตอร์ mem (dict) ข้อมูลสมาชิกที่ได้จาก do_login_member()
    """
    global current_member_info  # บอกว่าจะแก้ไขตัวแปร global

    # คัดลอกค่าจาก dict ที่รับเข้ามาใส่ใน State
    current_member_info["phone"]      = mem["phone"]
    current_member_info["first_name"] = mem["first_name"]
    current_member_info["last_name"]  = mem["last_name"]


def logout_member_state():
    """
    ล้างข้อมูลสมาชิกออกจาก Global State
    เรียกใช้ตอนสมาชิก Logout หรือหลังชำระเงินเสร็จ
    """
    global current_member_info  # บอกว่าจะแก้ไขตัวแปร global

    # Reset ทุกค่ากลับเป็น None (ไม่มีสมาชิก Login)
    current_member_info = {"phone": None, "first_name": None, "last_name": None}


def do_register_member(phone, fname, lname):
    """
    ลงทะเบียนสมาชิกใหม่เข้าสู่ระบบ
    """
    return member_manager.register_member(phone, fname, lname)


def is_member_logged_in():
    """
    ตรวจสอบว่ามีสมาชิก Login อยู่ในขณะนี้หรือไม่
    """
    # ถ้า phone ไม่ใช่ None แสดงว่ามีสมาชิก Login อยู่
    return current_member_info["phone"] is not None


# ==============================================================
# กลุ่มฟังก์ชันเกี่ยวกับตะกร้าสินค้า
# ==============================================================
def get_bill_path():
    """
    สร้างและคืนค่า Path เต็มของไฟล์บิลปัจจุบัน (bill.txt)
    """
    # os.path.dirname(__file__) = โฟลเดอร์ที่ไฟล์นี้อยู่
    # os.path.join ต่อ path เข้าด้วยกันให้ถูกต้องทุก OS
    return os.path.join(os.path.dirname(__file__), "data", "bill.txt")


def read_bill_lines():
    """
    อ่านรายการสินค้าทั้งหมดในบิลปัจจุบันจากไฟล์
    """
    bill_path = get_bill_path()
    items = []  # เตรียม list ไว้เก็บสินค้าแต่ละรายการ

    if os.path.exists(bill_path):  # ตรวจว่าไฟล์บิลมีอยู่ไหม
        with open(bill_path, "r", encoding="utf-8") as f:
            lines = f.readlines()  # อ่านทุกบรรทัดมาเก็บใน list

        for line in lines:
            # strip() ลบช่องว่างหัวท้าย, split(",") ตัดด้วยคอมม่า
            parts = line.strip().split(",")

            if len(parts) == 5:  # แต่ละบรรทัดต้องมีพอดี 5 ส่วน
                pid, name, price, qty, total = parts  # แยกค่าออกมา

                # แปลงชนิดข้อมูลให้ถูกต้อง แล้วใส่ใน dict
                items.append({
                    "pid":   pid,
                    "name":  name,
                    "price": float(price),  # แปลง str → ทศนิยม
                    "qty":   int(qty),      # แปลง str → จำนวนเต็ม
                    "total": float(total),  # แปลง str → ทศนิยม
                })

    return items


def clear_bill_file():
    """
    ล้างไฟล์บิลให้ว่างเปล่า (ไม่ลบไฟล์ แค่ลบเนื้อหาข้างใน)
    ใช้หลังชำระเงินเสร็จหรือล้างตะกร้า
    """
    # เปิดไฟล์ด้วยโหมด "w" (write) แล้วปิดทันที → เนื้อหาถูกล้าง
    open(get_bill_path(), "w").close()


def calculate_totals(raw_total):
    """
    คำนวณสรุปยอดทั้งหมด ได้แก่ ส่วนลดสมาชิก, VAT, และยอดสุทธิ
    คืนค่า
        dict ที่มี 4 กุญแจ:
        subtotal   = ยอดก่อนลด
        discount   = ส่วนลด (25% สำหรับสมาชิก, 0 สำหรับทั่วไป)
        vat        = ภาษีมูลค่าเพิ่ม 7%
        grand_total = ยอดสุทธิที่ต้องจ่าย
    """
    # ถ้ามีสมาชิก Login อยู่ → ลด 25%, ถ้าไม่มี → ไม่ลด
    discount = raw_total * 0.25 if is_member_logged_in() else 0.0

    after_discount = raw_total - discount   # ยอดหลังหักส่วนลด
    vat = after_discount * 0.07             # คิด VAT 7% จากยอดหลังลด
    grand_total = after_discount + vat      # ยอดสุทธิ = หลังลด + VAT

    return {
        "subtotal":    raw_total,
        "discount":    discount,
        "vat":         vat,
        "grand_total": grand_total,
    }


def add_item_to_bill(pid, name, price, qty):
    """
    เพิ่มสินค้าลงในไฟล์บิล (bill.txt) พร้อมตรวจสอบสต็อกก่อน
    """
    inventory = product_manager.get_all_products()  # ดึงข้อมูลสินค้าทั้งหมด

    # ตรวจสอบว่าสินค้ามีในระบบ และสต็อกเพียงพอ
    if pid not in inventory or inventory[pid]["stock"] < qty:
        return False, "สินค้าในสต็อกไม่เพียงพอ!"

    total_price = price * qty  # คำนวณราคารวมของรายการนี้

    bill_path = get_bill_path()
    with open(bill_path, "a", encoding="utf-8") as f:
        # โหมด "a" (append) = เขียนต่อท้ายไฟล์ ไม่ลบของเดิม
        # :.2f = แสดงทศนิยม 2 ตำแหน่ง เช่น 10.00
        f.write(f"{pid},{name},{price:.2f},{qty},{total_price:.2f}\n")

    return True, "เพิ่มลงตะกร้าเรียบร้อยแล้ว"


def get_product_price(pid):
    """
    ดึงราคาของสินค้าจากคลังสินค้าตาม ID ที่ระบุ
    คืนค่า
        float ราคาสินค้า ถ้าพบ
        0.0 ถ้าไม่พบสินค้านั้นในระบบ
    """
    inventory = product_manager.get_all_products()  # ดึงสินค้าทั้งหมด

    if pid in inventory:
        # .get("price", 0.0) = ดึงค่า "price", ถ้าไม่มีให้ใช้ค่าเริ่มต้น 0.0
        return float(inventory[pid].get("price", 0.0))

    return 0.0  # ไม่พบสินค้า


# ==============================================================
# กลุ่มฟังก์ชันเกี่ยวกับการพักบิล (Hold / Recall Bill)
# ==============================================================
def get_hold_dir():
    """
    สร้างและคืนค่า Path ของโฟลเดอร์ที่ใช้เก็บบิลพัก
    คืนค่า
        str เส้นทางไปยังโฟลเดอร์ data/hold_bills/
    """
    return os.path.join(os.path.dirname(__file__), "data", "hold_bills")


def hold_bill():
    """
    พักบิลปัจจุบัน บันทึกบิลลงไฟล์ใหม่ในโฟลเดอร์ hold_bills แล้วล้างตะกร้า
    """
    bill_path = get_bill_path()

    # ตรวจสอบว่าไฟล์บิลมีอยู่ไหม
    if not os.path.exists(bill_path):
        return False, "ไม่มีสินค้าในตะกร้า!"

    # อ่านรายการสินค้าในบิลปัจจุบัน
    with open(bill_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # ตรวจสอบว่าบิลมีสินค้าอยู่จริงหรือเปล่า
    if not lines:
        return False, "ไม่มีสินค้าในตะกร้า!"

    hold_dir = get_hold_dir()
    os.makedirs(hold_dir, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี

    # ตั้งชื่อไฟล์บิลพักตามวันและเวลาปัจจุบัน เช่น bill_09-03-2026  20-30.txt
    timestamp = datetime.now().strftime("%d-%m-%Y  %H-%M")
    hold_file = os.path.join(hold_dir, f"bill_{timestamp}.txt")

    # เขียนรายการสินค้าทั้งหมดลงไฟล์พัก
    with open(hold_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    clear_bill_file()  # ล้างตะกร้าของปัจจุบัน
    return True, f"พักบิลไว้เรียบร้อย\n{timestamp}"


def get_held_bill_files():
    """
    ดึงรายชื่อไฟล์บิลที่ถูกพักไว้ทั้งหมดในโฟลเดอร์ hold_bills
    """
    hold_dir = get_hold_dir()
    os.makedirs(hold_dir, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี

    # os.listdir() = ดึงชื่อไฟล์ทั้งหมดในโฟลเดอร์
    # กรองเอาเฉพาะไฟล์ที่ลงท้ายด้วย .txt
    return [f for f in os.listdir(hold_dir) if f.endswith(".txt")]


def recall_bill(selected_file):
    """
    เรียกคืนบิลที่พักไว้ โดยนำรายการมาต่อท้ายบิลปัจจุบัน แล้วลบไฟล์พักทิ้ง
    """
    hold_dir = get_hold_dir()
    hold_path = os.path.join(hold_dir, selected_file)  # สร้าง Path เต็มของไฟล์พัก

    # อ่านรายการสินค้าจากไฟล์บิลพัก
    with open(hold_path, "r", encoding="utf-8") as hf:
        hold_lines = hf.readlines()

    # เขียนต่อท้ายบิลปัจจุบัน (โหมด "a" = append)
    with open(get_bill_path(), "a", encoding="utf-8") as bf:
        bf.writelines(hold_lines)

    os.remove(hold_path)  # ลบไฟล์พักออก เพราะเรียกคืนแล้ว
    return True, "เรียกบิลเรียบร้อยแล้ว เพิ่มสินค้าลงตะกร้าแล้ว"


# ==============================================================
# กลุ่มฟังก์ชันเกี่ยวกับการชำระเงิน
# ==============================================================

def process_checkout():
    """
    ดำเนินการชำระเงิน ทำหน้าที่ทั้งหมดดังนี้:
    1. ตรวจสอบว่าตะกร้ามีสินค้า
    2. ตัดสต็อกสินค้าแต่ละรายการ
    3. คำนวณยอดสุทธิ (ส่วนลด + VAT)
    4. บันทึกการขายและสร้างใบเสร็จ PDF
    5. ล้างไฟล์บิล
    """
    bill_path = get_bill_path()

    # ตรวจสอบว่าไฟล์บิลมีอยู่ไหม
    if not os.path.exists(bill_path):
        return False, "ไม่มีสินค้าในตะกร้า!", None

    # อ่านรายการสินค้าทั้งหมดในบิล
    with open(bill_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # ตรวจสอบว่าบิลมีสินค้าจริงไหม
    if not lines:
        return False, "ไม่มีสินค้าในตะกร้า!", None

    # ตัวแปรสำหรับสรุปผลการชำระเงิน
    all_success   = True   # True = ทุกรายการตัดสต็อกสำเร็จ
    error_msgs    = []     # เก็บข้อความ Error ของแต่ละรายการ
    receipt_items = []     # เก็บรายการสินค้าสำหรับสร้างใบเสร็จ
    total_sum     = 0.0    # ยอดรวมก่อนคิดส่วนลด

    # วนลูปตรวจสอบและตัดสต็อกสินค้าทุกรายการในบิล
    for line in lines:
        parts = line.strip().split(",")  # แยกข้อมูลแต่ละช่องออกมา

        if len(parts) == 5:
            pid, name, price, qty, total = parts

            # ส่งคำสั่งตัดสต็อก → คืนค่า (success, message)
            success, msg = product_manager.process_sale(pid, int(qty))

            if not success:
                # ตัดสต็อกไม่สำเร็จ → บันทึก Error ไว้
                all_success = False
                error_msgs.append(f"{name}: {msg}")
            else:
                # ตัดสต็อกสำเร็จ → บันทึกข้อมูลขายและเก็บไว้สร้างใบเสร็จ
                product_manager.record_sale(pid, int(qty), float(total))
                receipt_items.append({
                    "name":  name,
                    "qty":   int(qty),
                    "price": float(price),
                    "total": float(total),
                })
                total_sum += float(total)  # บวกยอดสะสม

    # ถ้ามีรายการใดตัดสต็อกไม่ได้ → แจ้ง Error และล้างตะกร้า
    if not all_success:
        errors = "\n".join(error_msgs)  # รวม Error ทุกรายการเป็นข้อความเดียว
        clear_bill_file()
        return False, f"สต๊อกไม่พอ:\n{errors}\n*ระบบเคลียร์ตะกร้าแล้ว", None

    # คำนวณยอดสุทธิ (ส่วนลด + VAT)
    totals = calculate_totals(total_sum)

    # บันทึกการขายและพยายามสร้างใบเสร็จ PDF
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
    except Exception:
        pass  # ถ้าสร้าง PDF ไม่ได้ก็ไม่เป็นไร โปรแกรมยังทำงานต่อได้

    clear_bill_file()  # ล้างบิลหลังชำระเงินเสร็จ
    return True, "ชำระเงินสำเร็จ", pdf_file


# ==============================================================
# กลุ่มฟังก์ชันเกี่ยวกับสินค้า
# ==============================================================

def get_all_products_filtered(search_keyword=""):
    """
    ดึงรายการสินค้าทั้งหมด และกรองตามคำค้นหา (ถ้ามี)
    คืนค่า
        list of dict แต่ละตัวมี {"id": รหัส, "name": ชื่อ}
    """
    file_path = os.path.join(os.path.dirname(__file__), "data", "products.txt")
    products = []  # เตรียม list ไว้เก็บสินค้าที่ผ่านการกรอง

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()  # อ่านทุกบรรทัดในไฟล์สินค้า

        # แปลงคำค้นหาเป็นตัวพิมพ์เล็กเพื่อค้นหาแบบ case-insensitive
        kw = search_keyword.strip().lower()

        for line in lines:
            line = line.strip()  # ลบช่องว่างหัวท้าย
            if not line:
                continue  # ข้ามบรรทัดว่าง

            parts = line.split(",")  # แยกข้อมูลตามคอมม่า

            if len(parts) >= 2:  # ต้องมีอย่างน้อย รหัส และ ชื่อ
                product_id   = parts[0]
                product_name = parts[1]

                # ถ้ามีคำค้นหา และคำนั้นไม่อยู่ในชื่อหรือรหัส → ข้ามไป
                if kw and kw not in product_name.lower() and kw not in product_id.lower():
                    continue

                products.append({"id": product_id, "name": product_name})

    except FileNotFoundError:
        pass  # ถ้าไม่มีไฟล์ products.txt ก็คืน list ว่างแทน

    return products
