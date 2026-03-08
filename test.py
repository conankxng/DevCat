import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

# 1. ตั้งค่าพื้นฐาน
root = tk.Tk()
root.title("Python GIF Viewer")
root.geometry("600x400")

# 2. โหลดไฟล์ GIF และดึงเฟรมออกมาเก็บไว้ใน List
gif_path = "gif/test1.gif"
img = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(img)]

# 3. สร้างตัวแปรไว้เก็บลำดับเฟรมปัจจุบัน
current_frame = 0

# 4. สร้าง Label ไว้แสดงภาพ
label = tk.Label(root)
label.pack(fill="both", expand=True)

# 5. ฟังก์ชันสำหรับเปลี่ยนภาพไปเรื่อยๆ (Animation)
def update_gif():
    global current_frame
    
    # ดึงภาพเฟรมปัจจุบันมาโชว์
    frame = frames[current_frame]
    label.configure(image=frame)
    
    # เลื่อนลำดับเฟรม (ถ้าถึงเฟรมสุดท้ายให้วนกลับไป 0)
    current_frame = (current_frame + 1) % len(frames)
    
    # สั่งให้ทำงานซ้ำทุกๆ 100 มิลลิวินาที
    root.after(100, update_gif)

# 6. เรียกใช้งานฟังก์ชันครั้งแรก
update_gif()

root.mainloop()