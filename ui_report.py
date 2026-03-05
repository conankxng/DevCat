import tkinter as tk
from tkinter import ttk, messagebox #ttk คือ widget  messagebox คือหน้าต่างแจ้งเตือนpopup
import product_manager as pm

def financial_summary(): 
    try: 
        revenue = report.total_revenue() 
        expense = report.total_expense() 
        profit = revenue - expense
    