"""
ไฟล์หลักของ Application DevCat
"""
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import POS
import ui_inventory
import ui_report


# =========================================================================== #
# ส่วน State การทำงานของแอป
# =========================================================================== #
class AppState:
    """เก็บสถานะการทำงานของแอปพลิเคชัน (หน้าปัจจุบัน, สถานะ Animation)"""
    current_page = None   # Frame ที่แสดงอยู่ตอนนี้
    is_animating = False  # True ขณะกำลังเล่น Loading Animation (ป้องกันการกดซ้ำ)
    loading_frame = None  # Frame ของ Loading Screen
    progress_bar  = None  # Progress Bar ใน Loading Screen


# =========================================================================== #
# ส่วนฟังก์ชันหลัก
# =========================================================================== #
def init_loading_screen(parent):
    """
    สร้าง Loading Screen ซ่อนอยู่ใต้หน้าอื่นๆ และจะ raise ขึ้นมาตอนสลับหน้า
    """
    AppState.loading_frame = ctk.CTkFrame(parent, fg_color="#191919", width=1920, height=960)
    AppState.loading_frame.place(x=0, y=90)

    # จัดให้อยู่กึ่งกลางหน้าจอ
    inner_frame = ctk.CTkFrame(AppState.loading_frame, fg_color="transparent")
    inner_frame.place(relx=0.5, rely=0.5, anchor="center")

    #สร้างข้อความแสดงโหลด
    ctk.CTkLabel(
        inner_frame, text="รอสักครู่นะเมี๊ยวว...",
        font=("Kanit", 50, "bold"), text_color="white"
    ).pack(pady=(0, 20))

    #สร้างแถบ process 
    AppState.progress_bar = ctk.CTkProgressBar(
        inner_frame, width=500,
        mode="indeterminate", progress_color="#1e683e" #โหมดที่ทำให้แถบวิ่งไปมาเรื่อย ๆ
    )
    AppState.progress_bar.pack(pady=20)


def switch(page):
    """
    สลับไปยัง page ที่ระบุ พร้อมแสดงหน้า Loading Screen
    """
    if AppState.is_animating or AppState.current_page == page: #ถ้ากำลังอยู่ในการโหลดหน้า หรือ อยู่ที่หน้าปัจุบันอยู่แล้ว ให้คืนค่าโดยไม่ต้องทำอะไร
        return

    if AppState.loading_frame is None: #ถ้าไม่มีการโหลดหน้า
        page.tkraise() #ให้ดึงหน้าเป้าหมายหรือตัวแปร page มาแสดง
        AppState.current_page = page #ให้ไปยังหน้าที่ตัวแปร page รับเข้ามา
        return

    AppState.is_animating = True #เริ่มการทำงานโดยที่ประกาศว่ากำลังทำงาน
    AppState.loading_frame.tkraise() #ดึงหน้าโหลดมาแสดงทับทุกหน้า
    AppState.progress_bar.start() #ดึงใช้แถบสถานะที่สร้างไว้

    def finish_switch():
        """หยุด Animation และแสดงหน้าปลายทาง"""
        AppState.progress_bar.stop() #หยุดการทำงานของแถบสถานะ
        page.tkraise() #ดุงหน้าตัวแปร page มาแสดงแทนหน้าโหลด
        AppState.current_page = page #ให้ไปยังหน้าที่ตัวแปร page รับเข้ามา
        AppState.is_animating = False #คืนค่า่หน้าโหลดเพื่อให้ทำอย่างอื่นได้

    root.after(1500, finish_switch) #หน่วงเวลา


def on_closing():
    """จัดการเมื่อผู้ใช้กดปุ่มปิดหน้าต่าง"""
    root.destroy()


# =========================================================================== #
# ส่วน Root Window
# =========================================================================== #
root = tk.Tk()
root.title("DevCat")
root.geometry("1920x1080")
root.protocol("WM_DELETE_WINDOW", on_closing)


# =========================================================================== #
# Header
# =========================================================================== #
header = ctk.CTkFrame(root, height=90, fg_color="#FFFFFF")
header.pack(fill=ctk.X)

# แบ่ง Header เป็น 3 ส่วน
header.grid_rowconfigure(0, weight=1, minsize=80) #ล็อคความสูง
header.grid_columnconfigure(0, weight=1)
header.grid_columnconfigure(1, weight=1)
header.grid_columnconfigure(2, weight=1)

#ฝั่งซ้าย โลโก้
header_left = ctk.CTkFrame(header, fg_color="#FFFFFF")
header_left.grid(row=0, column=0, sticky="nsew")


raw_logo = Image.open("img/Logo_devcat.png")
image_logo = ctk.CTkImage(light_image=raw_logo, dark_image=raw_logo, size=(200, 50))
ctk.CTkButton(
    header_left, image=image_logo, text="",
    fg_color="transparent", hover_color="#eeeeee",
    width=200, height=50,
    command=lambda: switch(page_main)
).place(x=20, y=10)
    
#ตรงกลาง ปุ่มเมนูหลัก
header_center = ctk.CTkFrame(header, fg_color="#FFFFFF")
header_center.grid(row=0, column=1, sticky="nsew")
header_center.grid_columnconfigure(0, weight=1)
header_center.grid_columnconfigure(1, weight=1)
header_center.grid_columnconfigure(2, weight=1)

#สไตล์ปุ่ม
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
#แม่แบบการจัดวาง layout แบบ grid
NAV_BTN_GRID = dict(sticky="nsew", padx=10, pady=(10, 5))

#สร้างปุ่มรายการหลัก
ctk.CTkButton(header_center, text="Inventory", command=lambda: switch(page_inventory), **NAV_BTN_STYLE).grid(row=0, column=0, **NAV_BTN_GRID)
ctk.CTkButton(header_center, text="POS",       command=lambda: switch(page_pos),       **NAV_BTN_STYLE).grid(row=0, column=1, **NAV_BTN_GRID)
ctk.CTkButton(header_center, text="Report",    command=lambda: switch(page_report),    **NAV_BTN_STYLE).grid(row=0, column=2, **NAV_BTN_GRID)

#ฝั่งขวา ส่วน About
header_right = ctk.CTkFrame(header, fg_color="#FFFFFF")
header_right.grid(row=0, column=2, sticky="nsew")
header_right.grid_columnconfigure(0, weight=1)
header_right.grid_columnconfigure(1, weight=1)

#สร้างปุ่ม About
ctk.CTkButton(header_right, text="Members", command=lambda: switch(page_members), **NAV_BTN_STYLE).grid(row=0, column=0, **NAV_BTN_GRID)
ctk.CTkButton(header_right, text="Exit",    command=root.destroy,                 **NAV_BTN_STYLE).grid(row=0, column=1, **NAV_BTN_GRID)


# =========================================================================== #
# สร้าง Page ทั้งหมด (ซ้อนกันอยู่ที่ตำแหน่งเดียวกัน)
# =========================================================================== #
# ขนาดและตำแหน่งมาตรฐานของทุก Page .place
PAGE_CONFIG = dict(x=0, y=90, width=1920, height=960)

#หน้า Main
page_main = tk.Frame(root, bg="#191919")
page_main.place(**PAGE_CONFIG)

#แยก gif เป็น เฟรม ๆ
gif_frames_main = [
    ImageTk.PhotoImage(frame.copy())
    for frame in ImageSequence.Iterator(Image.open("gif/main.gif"))
]

current_frame_index = 0
gif_label = tk.Label(page_main)
gif_label.pack(fill="both", expand=True)

def update_gif():
    """วนเล่น GIF ทุก 100ms เรียกตัวเองซ้ำผ่าน root.after()"""
    global current_frame_index
    gif_label.configure(image=gif_frames_main[current_frame_index])
    current_frame_index = (current_frame_index + 1) % len(gif_frames_main)
    root.after(100, update_gif)

update_gif()


#หน้า Members
page_members = tk.Frame(root, bg="#191919")
page_members.place(**PAGE_CONFIG)

#แยก gif เป็น เฟรม ๆ
gif_frames_menbers = [
    ImageTk.PhotoImage(frame.copy())
    for frame in ImageSequence.Iterator(Image.open("gif/members.gif"))
]

members_frame_index = 0
members_gif_label = tk.Label(page_members)
members_gif_label.pack(fill="both", expand=True)

def update_members_gif():
    """วนเล่น GIF บนหน้า Members ทุก 100ms"""
    global members_frame_index
    members_gif_label.configure(image=gif_frames_menbers[members_frame_index])
    members_frame_index = (members_frame_index + 1) % len(gif_frames_menbers)
    root.after(100, update_members_gif)

update_members_gif()


#หน้า Inventory (p1)
# อนุพงค์ พลจันทึก 681310024
page_inventory = tk.Frame(root, bg="#191919")
page_inventory.place(**PAGE_CONFIG)
ui_inventory.setup_inventory_interface(page_inventory)


#หน้า POS (p2)
# อภิรักษ์ ธรรมแก้ว 681310025
page_pos = tk.Frame(root, bg="#191919")
page_pos.place(**PAGE_CONFIG)
POS.create_three_frames(page_pos)


#หน้า Report (p3)
# กัญญ์กณิษฐ์ เชื้อฉลาด 681310001
page_report = tk.Frame(root, bg="#191919")
page_report.place(**PAGE_CONFIG)
ui_report.create_report_ui(page_report)


# =========================================================================== #
# ส่วนเริ่มต้นโปรแกรม
# =========================================================================== #
# สร้าง Loading Screen แล้วแสดงหน้า Main เป็นหน้าแรก
init_loading_screen(root)
switch(page_main)

root.mainloop()
