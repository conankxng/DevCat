import os

MEMBER_FILE = os.path.join(os.path.dirname(__file__), "data", "members.txt")

def ensure_file_exists():
    """สร้างไฟล์ถ้ายังไม่มี"""
    os.makedirs(os.path.dirname(MEMBER_FILE), exist_ok=True)
    if not os.path.exists(MEMBER_FILE):
        open(MEMBER_FILE, 'w', encoding='utf-8').close()

def register_member(phone, first_name, last_name):
    """
    ลงทะเบียนสมาชิกใหม่
    Return: (Success(bool), Message(str))
    """
    ensure_file_exists()
    
    # ตรวจสอบว่าเบอร์ซ้ำไหม
    with open(MEMBER_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 3 and parts[0] == phone:
                return False, "เบอร์โทรศัพท์นี้เป็นสมาชิกอยู่แล้ว"
                
    # บันทึกสมาชิกใหม่
    with open(MEMBER_FILE, "a", encoding="utf-8") as f:
        f.write(f"{phone},{first_name},{last_name}\n")
        
    return True, "สมัครสมาชิกสำเร็จ"

def get_member(phone):
    """
    ดึงข้อมูลสมาชิกด้วยเบอร์โทร
    Return: Dictionary ข้อมูล หรือ None ถ้าไม่พบ
    """
    ensure_file_exists()
    with open(MEMBER_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 3 and parts[0] == phone:
                return {
                    "phone": parts[0],
                    "first_name": parts[1],
                    "last_name": parts[2]
                }
    return None
