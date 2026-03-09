"""
=============================================================
ไฟล์หลักของแอปพลิเคชัน DevCat
=============================================================
"""
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import POS
import ui_inventory
import ui_report

# ==============================================================
# คลาสเก็บสถานะของแอป
# ==============================================================
class AppState:
    """
    เก็บสถานะต่างๆ ของแอปพลิเคชันไว้ในที่เดียว ทำให้ฟังก์ชันอื่นๆ เข้าถึงค่าเหล่านี้ได้ง่าย
    """
    current_page = None   # เก็บว่าตอนนี้แสดงหน้าไหนอยู่
    is_animating = False  # True = กำลังโหลด (ป้องกันการกดปุ่มซ้ำระหว่างโหลด)
    loading_frame = None  # Frame ของหน้าโหลด
    progress_bar  = None  # แถบ Progress ในหน้าโหลด


# ==============================================================
# ฟังก์ชันสร้างหน้า Loading Screen
# ==============================================================
def init_loading_screen(parent):
    """
    สร้างหน้า Loading Screen และซ่อนไว้ใต้หน้าอื่น เมื่อสลับหน้า จะถูกดึงขึ้นมาแสดงชั่วคราว
    """
    # สร้าง Frame พื้นหลังสีดำสำหรับหน้าโหลด
    AppState.loading_frame = ctk.CTkFrame(
        parent,
        fg_color="#191919",  # สีพื้นหลังสีดำ
        width=1920,
        height=960
    )
    AppState.loading_frame.place(x=0, y=90)  # วางไว้ใต้ Header (Header สูง 90px)

    # สร้าง Frame ด้านในสำหรับจัดให้ข้อความและ Progress Bar อยู่กึ่งกลาง
    inner_frame = ctk.CTkFrame(AppState.loading_frame, fg_color="transparent")
    inner_frame.place(relx=0.5, rely=0.5, anchor="center")  # วางตรงกลางหน้าจอ

    # สร้างข้อความที่แสดงระหว่างรอโหลด
    ctk.CTkLabel(
        inner_frame,
        text="รอสักครู่นะเมี๊ยวว...",
        font=("Kanit", 50, "bold"),
        text_color="white"
    ).pack(pady=(0, 20))

    # สร้างแถบ Progress Bar แบบวิ่งไปมาเรื่อยๆ
    AppState.progress_bar = ctk.CTkProgressBar(
        inner_frame,
        width=500,
        mode="indeterminate",    # โหมดวิ่งไปมา (ไม่รู้เวลาสิ้นสุด)
        progress_color="#1e683e" # สี Processbar
    )
    AppState.progress_bar.pack(pady=20)


# ==============================================================
# ฟังก์ชันสลับหน้า
# ==============================================================
def switch(page):
    """
    สลับไปแสดงหน้าที่ต้องการ พร้อมแสดงหน้าโหลดระหว่างสลับ
    page = Frame ของหน้าที่ต้องการสลับไป
    """

    # ถ้ากำลังโหลดอยู่ หรือ อยู่ที่หน้านั้นแล้ว → ไม่ทำอะไร
    if AppState.is_animating or AppState.current_page == page:
        return

    # ถ้ายังไม่ได้สร้างหน้าโหลด → สลับหน้าทันทีโดยไม่มีอนิเมชัน
    if AppState.loading_frame is None:
        page.tkraise()               # ดึงหน้าที่ต้องการขึ้นมาแสดง
        AppState.current_page = page # อัปเดตสถานะหน้าปัจจุบัน
        return

    # เริ่มต้นการสลับหน้าพร้อมอนิเมชัน
    AppState.is_animating = True     # ตั้งสถานะว่ากำลังโหลด
    AppState.loading_frame.tkraise() # แสดงหน้าโหลดทับทุกหน้า
    AppState.progress_bar.start()    # เริ่มเล่นอนิเมชัน Progress Bar

    def finish_switch():
        """
        ฟังก์ชันนี้จะถูกเรียกหลังจากรอ 1.5 วินาที
        เพื่อหยุดอนิเมชันและแสดงหน้าปลายทาง
        """
        AppState.progress_bar.stop()     # หยุดอนิเมชัน Progress Bar
        page.tkraise()                   # แสดงหน้าปลายทาง
        AppState.current_page = page     # อัปเดตสถานะหน้าปัจจุบัน
        AppState.is_animating = False    # รีเซ็ตสถานะให้กดปุ่มได้อีกครั้ง

    # หน่วงเวลา 1500ms (1.5 วินาที) แล้วค่อยเรียก finish_switch
    root.after(1500, finish_switch)


# ==============================================================
# ฟังก์ชันปิดโปรแกรม
# ==============================================================
def on_closing():
    """
    ฟังก์ชันนี้จะถูกเรียกเมื่อผู้ใช้กดปุ่ม X เพื่อปิดหน้าต่าง
    ทำหน้าที่ปิดโปรแกรมทั้งหมด
    """
    root.destroy()  # ทำลายหน้าต่างหลักและปิดโปรแกรม


# ==============================================================
# สร้างหน้าต่างหลัก
# ==============================================================
root = tk.Tk()
root.title("DevCat")           # ชื่อที่แสดงบน Title Bar
root.geometry("1920x1080")     # กำหนดขนาดหน้าต่าง (กว้าง x สูง)
root.protocol("WM_DELETE_WINDOW", on_closing)  # เชื่อมปุ่มปิดกับฟังก์ชัน on_closing


# ==============================================================
# สร้าง Header
# ==============================================================
header = ctk.CTkFrame(root, height=90, fg_color="#FFFFFF")
header.pack(fill=ctk.X)  # ยืดให้เต็มความกว้างของหน้าต่าง

# แบ่ง Header เป็น 3 คอลัมน์: ซ้าย | กลาง | ขวา
header.grid_rowconfigure(0, weight=1, minsize=80)  # กำหนดความสูงขั้นต่ำ
header.grid_columnconfigure(0, weight=1)  # คอลัมน์ซ้าย
header.grid_columnconfigure(1, weight=1)  # คอลัมน์กลาง
header.grid_columnconfigure(2, weight=1)  # คอลัมน์ขวา

# ส่วนซ้าย โลโก้
header_left = ctk.CTkFrame(header, fg_color="#FFFFFF")
header_left.grid(row=0, column=0, sticky="nsew")  # วางในคอลัมน์ซ้าย ยืดเต็มพื้นที่

# โหลดรูปโลโก้และสร้างปุ่มโลโก้ (กดแล้วไปหน้า Main)
raw_logo = Image.open("img/Logo_devcat.png")
image_logo = ctk.CTkImage(light_image=raw_logo, dark_image=raw_logo, size=(200, 50))
ctk.CTkButton(
    header_left,
    image=image_logo,
    text="",                        # ไม่แสดงข้อความ มีแค่รูป
    fg_color="transparent",         # พื้นหลังโปร่งใส
    hover_color="#eeeeee",          # สีเมื่อเอาเมาส์ไปวาง
    width=200,
    height=50,
    command=lambda: switch(page_main)  # กดแล้วกลับหน้าหลัก
).place(x=20, y=10)

# ส่วนกลาง ปุ่มเมนูหลัก
header_center = ctk.CTkFrame(header, fg_color="#FFFFFF")
header_center.grid(row=0, column=1, sticky="nsew")
header_center.grid_columnconfigure(0, weight=1)  # Inventory
header_center.grid_columnconfigure(1, weight=1)  # POS
header_center.grid_columnconfigure(2, weight=1)  # Report

# กำหนดสไตล์ของปุ่มเมนู (เก็บไว้ใน dict เพื่อใช้ซ้ำ)
NAV_BTN_STYLE = dict(
    font=("Kanit", 30, "bold"),
    height=70,
    fg_color="#FFFFFF",
    hover_color="#eeeeee",
    text_color="#1e683e",
    border_width=2,
    border_color="#1e683e",
    corner_radius=10
)

# กำหนดตำแหน่ง layout ของปุ่มเมนู (เก็บไว้ใน dict เพื่อใช้ซ้ำ)
NAV_BTN_GRID = dict(sticky="nsew", padx=10, pady=(10, 5))

# สร้างปุ่มเมนูทั้ง 3 ปุ่มในส่วนกลาง
ctk.CTkButton(header_center, text="Inventory", command=lambda: switch(page_inventory), **NAV_BTN_STYLE).grid(row=0, column=0, **NAV_BTN_GRID)
ctk.CTkButton(header_center, text="POS",       command=lambda: switch(page_pos),       **NAV_BTN_STYLE).grid(row=0, column=1, **NAV_BTN_GRID)
ctk.CTkButton(header_center, text="Report",    command=lambda: switch(page_report),    **NAV_BTN_STYLE).grid(row=0, column=2, **NAV_BTN_GRID)

# ส่วนขวา ปุ่ม Members และ Exit 
header_right = ctk.CTkFrame(header, fg_color="#FFFFFF")
header_right.grid(row=0, column=2, sticky="nsew")
header_right.grid_columnconfigure(0, weight=1)  # Members
header_right.grid_columnconfigure(1, weight=1)  # Exit

# สร้างปุ่ม Members และ Exit
ctk.CTkButton(header_right, text="Members", command=lambda: switch(page_members), **NAV_BTN_STYLE).grid(row=0, column=0, **NAV_BTN_GRID)
ctk.CTkButton(header_right, text="Exit",    command=root.destroy,                 **NAV_BTN_STYLE).grid(row=0, column=1, **NAV_BTN_GRID)


# ==============================================================
# สร้างหน้าต่างๆ ทั้งหมด (ซ้อนกันในตำแหน่งเดียวกัน)
# ==============================================================
# กำหนดขนาดและตำแหน่งมาตรฐานสำหรับทุกหน้า
# y=90 เพราะต้องเว้นที่ให้ Header (สูง 90px)
PAGE_CONFIG = dict(x=0, y=90, width=1920, height=960)


# หน้า Main 
page_main = tk.Frame(root, bg="#191919")
page_main.place(**PAGE_CONFIG)

# โหลด GIF และแยกแต่ละเฟรมออกมาเก็บในลิสต์
gif_frames_main = [
    ImageTk.PhotoImage(frame.copy())
    for frame in ImageSequence.Iterator(Image.open("gif/main.gif"))
]

# ตัวแปรสำหรับติดตามว่าตอนนี้แสดงเฟรมที่เท่าไหร่
current_frame_index = 0

# Label สำหรับแสดง GIF
gif_label = tk.Label(page_main)
gif_label.pack(fill="both", expand=True)  # ยืดให้เต็มพื้นที่หน้า


def update_gif():
    """
    อัปเดตเฟรม GIF ในหน้า Main ทุก 100ms
    ฟังก์ชันนี้จะเรียกตัวเองซ้ำเรื่อยๆ ทำให้ GIF วนลูปไปเรื่อยๆ
    """
    global current_frame_index  # บอกว่าใช้ตัวแปร current_frame_index ที่อยู่นอกฟังก์ชัน

    # อัปเดต Label ให้แสดงเฟรมปัจจุบัน
    gif_label.configure(image=gif_frames_main[current_frame_index])

    # เลื่อนไปเฟรมถัดไป (ถ้าถึงเฟรมสุดท้ายแล้วให้วนกลับเฟรม 0)
    current_frame_index = (current_frame_index + 1) % len(gif_frames_main)

    # เรียกฟังก์ชันนี้อีกครั้งหลังจาก 100ms (= 10 เฟรมต่อวินาที)
    root.after(100, update_gif)


update_gif()  # เริ่มเล่น GIF


# หน้า Members
page_members = tk.Frame(root, bg="#191919")
page_members.place(**PAGE_CONFIG)

# โหลด GIF ของหน้า Members และแยกแต่ละเฟรม
gif_frames_menbers = [
    ImageTk.PhotoImage(frame.copy())
    for frame in ImageSequence.Iterator(Image.open("gif/members.gif"))
]

# ตัวแปรสำหรับติดตามเฟรมปัจจุบันของหน้า Members
members_frame_index = 0

# Label สำหรับแสดง GIF ของหน้า Members
members_gif_label = tk.Label(page_members)
members_gif_label.pack(fill="both", expand=True)


def update_members_gif():
    """
    อัปเดตเฟรม GIF ในหน้า Members ทุก 100ms
    ทำงานเหมือน update_gif() แต่ใช้กับหน้า Members
    """
    global members_frame_index  # บอกว่าใช้ตัวแปร members_frame_index ที่อยู่นอกฟังก์ชัน

    # อัปเดต Label ให้แสดงเฟรมปัจจุบัน
    members_gif_label.configure(image=gif_frames_menbers[members_frame_index])

    # เลื่อนไปเฟรมถัดไป (ถ้าถึงเฟรมสุดท้ายแล้วให้วนกลับเฟรม 0)
    members_frame_index = (members_frame_index + 1) % len(gif_frames_menbers)

    # เรียกฟังก์ชันนี้อีกครั้งหลังจาก 100ms
    root.after(100, update_members_gif)


update_members_gif()  # เริ่มเล่น GIF


# หน้า Inventory (คลังสินค้า)
# อนุพงค์ พลจันทึก 681310024
page_inventory = tk.Frame(root, bg="#191919")
page_inventory.place(**PAGE_CONFIG)
ui_inventory.setup_inventory_interface(page_inventory)  # เรียกฟังก์ชันใน ui_inventory.py มาสร้าง UI


# หน้า POS (ขายสินค้า)
# อภิรักษ์ ธรรมแก้ว 681310025
page_pos = tk.Frame(root, bg="#191919")
page_pos.place(**PAGE_CONFIG)
POS.create_three_frames(page_pos)  # เรียกฟังก์ชันใน POS.py มาสร้าง UI


# หน้า Report (รายงาน) 
# กัญญ์กณิษฐ์ เชื้อฉลาด 681310001
page_report = tk.Frame(root, bg="#191919")
page_report.place(**PAGE_CONFIG)
ui_report.create_report_ui(page_report)  # เรียกฟังก์ชันใน ui_report.py มาสร้าง UI


# ==============================================================
# เริ่มต้นโปรแกรม
# ==============================================================
init_loading_screen(root)  # สร้างหน้าโหลด
switch(page_main)           # แสดงหน้า Main เป็นหน้าแรก

root.mainloop()  # เริ่มวนลูปรอรับ Event จากผู้ใช้ (ค้างอยู่ตรงนี้จนกว่าจะปิดโปรแกรม)
