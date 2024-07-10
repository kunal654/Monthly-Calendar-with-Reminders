import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Calendar with Reminders")

        self.reminders = {}

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.create_widgets()
        self.display_calendar(self.current_year, self.current_month)

    def create_widgets(self):
        self.calendar_frame = ttk.Frame(self.root)
        self.calendar_frame.grid(row=0, column=0, padx=10, pady=10)

        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.add_reminder_frame = ttk.Frame(self.root)
        self.add_reminder_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.month_label = ttk.Label(self.control_frame, text="", font=("Arial", 16))
        self.month_label.pack(side="top", pady=5)

        self.prev_button = ttk.Button(self.control_frame, text="<<", command=self.prev_month)
        self.prev_button.pack(side="left")

        self.next_button = ttk.Button(self.control_frame, text=">>", command=self.next_month)
        self.next_button.pack(side="right")

        self.reminder_label = ttk.Label(self.add_reminder_frame, text="Add Reminder:")
        self.reminder_label.grid(row=0, column=0, padx=5, pady=5)

        self.day_entry = ttk.Entry(self.add_reminder_frame, width=3)
        self.day_entry.grid(row=0, column=1, padx=5, pady=5)
        self.day_entry.insert(0, "Day")

        self.reminder_entry = ttk.Entry(self.add_reminder_frame, width=30)
        self.reminder_entry.grid(row=0, column=2, padx=5, pady=5)
        self.reminder_entry.insert(0, "Reminder")

        self.add_button = ttk.Button(self.add_reminder_frame, text="Add", command=self.add_reminder)
        self.add_button.grid(row=0, column=3, padx=5, pady=5)

    def display_calendar(self, year, month):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.Calendar()
        days = cal.itermonthdays(year, month)

        self.month_label.config(text=f"{calendar.month_name[month]} {year}")

        day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day_label in enumerate(day_labels):
            ttk.Label(self.calendar_frame, text=day_label).grid(row=0, column=i, padx=5, pady=5)

        row = 1
        col = 0
        for day in days:
            if day == 0:
                ttk.Label(self.calendar_frame, text="").grid(row=row, column=col, padx=5, pady=5)
            else:
                day_btn = ttk.Button(self.calendar_frame, text=str(day), command=lambda d=day: self.show_reminders(d))
                day_btn.grid(row=row, column=col, padx=5, pady=5)
                if day in self.reminders:
                    day_btn.config(style="Reminder.TButton")

            col += 1
            if col == 7:
                col = 0
                row += 1

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.display_calendar(self.current_year, self.current_month)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.display_calendar(self.current_year, self.current_month)

    def add_reminder(self):
        day = int(self.day_entry.get())
        reminder = self.reminder_entry.get()

        if day < 1 or day > calendar.monthrange(self.current_year, self.current_month)[1]:
            messagebox.showerror("Invalid Day", "Please enter a valid day for the selected month.")
            return

        if day not in self.reminders:
            self.reminders[day] = []
        self.reminders[day].append(reminder)

        self.day_entry.delete(0, tk.END)
        self.reminder_entry.delete(0, tk.END)

        self.display_calendar(self.current_year, self.current_month)

    def show_reminders(self, day):
        if day in self.reminders:
            reminders = "\n".join(self.reminders[day])
        else:
            reminders = "No reminders for this day."

        messagebox.showinfo(f"Reminders for {day} {calendar.month_name[self.current_month]} {self.current_year}", reminders)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
