import os
from datetime import datetime
from fpdf import FPDF

# ตั้งค่า Path สำหรับเก็บข้อมูล
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SALES_FILE = os.path.join(DATA_DIR, "master_sales.txt")
RECEIPTS_DIR = os.path.join(DATA_DIR, "receipts")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RECEIPTS_DIR, exist_ok=True)
    if not os.path.exists(SALES_FILE):
        open(SALES_FILE, 'w', encoding='utf-8').close()

def record_sale(items, subtotal, discount, vat, grand_total, member_info):
    """
    บันทึกยอดขายลงไฟล์ master_sales.txt และสร้างใบเสร็จ PDF
    items: list of dict -> [{"name": "cake", "qty": 2, "price": 50, "total": 100}, ...]
    member_info: dict -> {"phone": "080...", "first_name": "John", ...} หรือ ไม่มีคือ None
    """
    ensure_dirs()
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    # 1. บันทึกลง text file (master_sales.txt)
    member_name = "General Customer"
    if member_info and member_info.get("phone"):
        member_name = f"Member: {member_info['first_name']} {member_info['last_name']} ({member_info['phone']})"
        
    log_line = f"[{timestamp_str}] Total: {grand_total:.2f} THB | {member_name} | Items: {len(items)}\n"
    with open(SALES_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)
        
    # 2. สร้าง PDF Receipt ด้วย fpdf2
    pdf = FPDF()
    pdf.add_page()
    
    # เพิ่มฟอนต์ภาษาไทย (อิงจากระบบ Windows ถ้าไม่มีจะใช้ฟอนต์ Arial ซึ่งอาจไม่รองรับไทย)
    font_path = "C:\\Windows\\Fonts\\tahoma.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Tahoma", "", font_path)
        pdf.set_font("Tahoma", size=16)
    else:
        pdf.set_font("Helvetica", size=16)
        
    pdf.cell(200, 10, txt="DevCat POS - ใบเสร็จรับเงิน (Receipt)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(pdf.font_family, size=12)
    pdf.cell(200, 10, txt=f"วันที่ / Date: {timestamp_str}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, txt=f"ลูกค้า / Customer: {member_name}", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(200, 10, txt="----------------------------------------------------------------------", align="C", new_x="LMARGIN", new_y="NEXT")
    
    # หัวตาราง
    pdf.set_font(pdf.font_family, style="B", size=10)
    pdf.cell(80, 8, "รายการ (Item)", border=0)
    pdf.cell(30, 8, "จำนวน (Qty)", border=0, align="C")
    pdf.cell(40, 8, "ราคาต่อหน่วย (Unit Price)", border=0, align="R")
    pdf.cell(40, 8, "ราคารวม (Total)", border=0, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(pdf.font_family, size=10)
    
    # รายการสินค้า
    for item in items:
        pdf.cell(80, 8, str(item['name']))
        pdf.cell(30, 8, str(item['qty']), align="C")
        pdf.cell(40, 8, f"{float(item['price']):.2f}", align="R")
        pdf.cell(40, 8, f"{float(item['total']):.2f}", align="R", new_x="LMARGIN", new_y="NEXT")
        
    pdf.cell(200, 10, txt="----------------------------------------------------------------------", align="C", new_x="LMARGIN", new_y="NEXT")
    
    # สรุปยอด
    pdf.cell(150, 8, "รวมเป็นเงิน (Subtotal):", align="R")
    pdf.cell(40, 8, f"{subtotal:.2f}", align="R", new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(150, 8, "ส่วนลดสมาชิก 25% (Discount):", align="R")
    pdf.cell(40, 8, f"-{discount:.2f}", align="R", new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(150, 8, "ภาษีมูลค่าเพิ่ม 7% (VAT):", align="R")
    pdf.cell(40, 8, f"{vat:.2f}", align="R", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font(pdf.font_family, style="B", size=12)
    pdf.cell(150, 10, "ยอดชำระสุทธิ (Grand Total):", align="R")
    pdf.cell(40, 10, f"{grand_total:.2f} THB", align="R", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font(pdf.font_family, size=10)
    pdf.cell(200, 20, txt="*** ขอบคุณที่ใช้บริการ / Thank you ***", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf_filename = os.path.join(RECEIPTS_DIR, f"receipt_{file_timestamp}.pdf")
    pdf.output(pdf_filename)
    
    return pdf_filename
