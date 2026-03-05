import tkinter as tk
import product_manager

windown_A = tk.Tk()
windown_A.title("DevCat")
windown_A.geometry("800x800")

def show_strock():
    with open("data/products.txt", "r") as file:
        strock = file.read()
        return strock

tk.Label(windown_A, text=show_strock()).pack()

tk.Label(windown_A, text="storck_id").pack()

strock_id = tk.Entry(windown_A, width=20)
strock_id.pack()

tk.Label(windown_A, text="count").pack()

count_strock = tk.Entry(windown_A, width=20)
count_strock.pack()

btn = tk.Button(windown_A, text="Ok", command=lambda: product_manager.process_sale(strock_id.get(), int(count_strock.get()))) #เมื่อกดปุ่ม Ok จะเรียกใช้ฟังก์ชัน process_sale ใน product_manager โดยส่งค่า strock_id และ count_strock ที่ผู้ใช้กรอกเข้ามาเป็นพารามิเตอร์
btn.pack()

A = tk.Label(windown_A, text=count_strock.get())
A.pack()


windown_A.mainloop()