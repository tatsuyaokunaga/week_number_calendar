import sys 
import tkinter as tk 
import datetime as dt
import calendar as cl
import jpholiday

class Desktop_Calendar():
    
    def __init__(self, btn, label1, label2, label3):
        self.btn = btn
        self.label1 = label1
        self.label2 = label2
        self.label3 = label3
#         self.label4 = label4
        # 月曜日:1～日曜日:7
        self.iso_target_day_weeknum = 1
        self.date = dt.datetime.now().date()
        self.year = self.date.year 
        self.month = self.date.month 
        self.day = self.date.day 
        self.wd = 0
        self.cal = [""]*40 
        self.m_desc = ["January", "February", "March", 
                        "April", "May", "June", 
                        "July", "August", "September",
                        "October", "November","December"]


    # 引数の日付から次の「1週目とする基準の曜日」の日付を取得する
    def _get_next_target_day(self, date):  
        days_ahead = self.iso_target_day_weeknum - int(date.strftime("%u"))  # 月曜日:1～日曜日:7
        if days_ahead <= 0: 
            days_ahead += 7
        return date + dt.timedelta(days_ahead)

    # ウィークナンバーを取得する
    def _get_weeknum(self):
        # 引数の日付が「1週目とする基準の曜日」と同じ場合、元旦から引数の日付でウィークナンバーを取得
        if int(self.date.strftime("%u")) == self.iso_target_day_weeknum: # 月曜日
            next_target_date = self._get_next_target_day(self.date)
            # １週間後に年を越し、かつ元旦だった場合は同年の週番号になる
            if next_target_date.year == self.date.year+1 and next_target_date == dt.datetime(next_target_date.year, 1, 1).date():
                new_years_date = dt.datetime(self.date.year, 1, 1).date()
                return str(self.date.year) + str((next_target_date - new_years_date).days // 7+1).zfill(2)
            # １週間後に年を越し、かつ元旦ではない場合は翌年の週番号になる
            elif next_target_date.year == self.date.year+1 and next_target_date != dt.datetime(next_target_date.year, 1, 1).date():
                new_years_date = dt.datetime(next_target_date.year, 1, 1).date()
                return str(next_target_date.year) + str((next_target_date - new_years_date).days // 7 +1).zfill(2)
            else:
                new_years_date = dt.datetime(next_target_date.year, 1, 1).date()
                if int(new_years_date.strftime("%u")) == self.iso_target_day_weeknum: 
                    return str(self.date.year) + str((next_target_date - new_years_date).days // 7).zfill(2)
                else:
                    return str(self.date.year) +str((next_target_date - new_years_date).days // 7+1).zfill(2)
                
    
    def _generate_calendar(self): 
#         self.cal = [""]*40 
        for i in range( len(self.cal) ): 
            self.cal[i] = ""
        date = dt.date( self.year, self.month, 1 ) 
        wd = date.weekday() # 月曜日 0 〜　日曜日 6
        if wd > 5: # 日曜日
            wd = wd - 7 
        cal_max = cl.monthrange( self.year, self.month )[1] 
        for i in range( cal_max ): 
            day = str( i + 1 ) 
            idx = i + wd + 1 
            self.cal[idx] = day

    # 祝日表示
    def _get_holiday(self, day_str):
        if day_str == '':
            return None
        result = jpholiday.is_holiday_name(
            dt.date(int(self.label3["text"]), int(self.m_desc.index(self.label2["text"])) + 1, int(day_str)))
        return result


    def _set_calendar(self):
        for i in range(len(self.cal)):
            day_str = self.cal[i]
            self.btn[i]["text"] = day_str
            # 祝日表示↓↓↓
            # 月曜日のウィジェットに週IDを追加
#             self.date = dt.date(self.year,self.month,int(day_str))
            if day_str != '' and i % 7 == 1:
                self.date = dt.date(self.year,self.month,int(day_str))
                wk_idnx = self._get_weeknum() # 週番号
                if self._get_holiday(day_str) is not None:
                    fg = "#FF0000"
                    self.btn[i]["text"] = day_str + " " +                                      self._get_holiday(day_str)+ "\n" + wk_idnx
                else:
                    fg = "#000000"
                    self.btn[i]["text"] = day_str + " " + wk_idnx

            elif day_str != '' and self._get_holiday(day_str) is not None:
                self.date = dt.date(self.year,self.month,int(day_str))
                fg = "#FF0000"
                self.btn[i]["text"] = day_str + " " + self._get_holiday(day_str)
            elif i % 7 == 0:# sunday
                fg = "#FF0000"
            elif i % 7 == 6: # saturday
                fg = "#0000A0"
            else:
                fg = "#000000"
            self.btn[i]["fg"] = fg
            # 祝日表示↑↑↑

    def prev_next(self, num):
        self.month = self.month + num
        if self.month > 12:
            self.year = self.year + 1
            self.month = 1
        elif self.month < 1:
            self.year=  self.year  - 1
            self.month = 12
        self.label1["text"] = str(self.month)
        self.label2["text"] = self.m_desc[self.month - 1]
        self.label3["text"] = str(self.year)
        self._generate_calendar()
        self._set_calendar()


def btn_click():
    return 


root = tk.Tk()
root.title(u"week number calendar")
root.geometry("755x530+100+100")
root["bg"] = "#EEEEE8"

label1 = tk.Label(font=("Meiryo UI",28),anchor=tk.CENTER, width=2)
label1["bg"] = "#EEEEE8" 
label1.place(x=50, y=3) 

label2 = tk.Label(font=("Meiryo UI",12),anchor=tk.W, width=10)
label2["bg"] = "#EEEEE5" 
label2.place(x=120, y=8) 

label3 = tk.Label(font=("Meiryo UI",14),anchor=tk.W, width=10)
label3["bg"] = "#EEEEE8" 
label3.place(x=120, y=25) 

label4 = [""]*7 
week_list = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday" ] 
for i in range( 7 ): 
    label4[i] = tk.Label(text=week_list[i], font=("Meiryo UI",10), anchor=tk.CENTER, width=10)
    label4[i]["bg"] = "#EEEEE8" 
    label4[i].place(x=30+103*i, y=55) 

btn = [""]*42 
for i in range( 6 ): 
    for j in range( 7 ): 
        fg = "#000000" 
        if j == 0: 
            bg = "#FFF0F0" 
            fg = "#FF0000" 
        elif j == 6: 
            bg = "#F6F0FF" 
            fg = "#0000A0" 
        else: 
            bg = "#FFFFFF"  
        btn[j + 7 * i] = tk.Button(root, font=("Meiryo UI",11), 
                                   anchor=tk.NW, bg=bg, fg=fg, relief='flat', command=btn_click) 
        x2 = 20 + 100 * j 
        y2 = 75 + i * 70 
        btn[j + 7 * i].place(x = x2, y = y2, width=95, height=65)

# クラスをインスタンス化
my_cal= Desktop_Calendar(btn, label1, label2, label3)
        
# prev button
btn_prev = tk.Button(root, text="prev", font=("Meiryo UI",11), bg="#D0D0D0", relief='flat', command=lambda:my_cal.prev_next(-1) )
btn_prev.place(x=600, y=10, width=60, height=30)
# next button
btn_next = tk.Button(root, text="next", font=("Meiryo UI",11), bg="#D0D0D0", relief='flat', command=lambda:my_cal.prev_next(1) )
btn_next.place(x=680, y=10, width=60, height=30)

my_cal.prev_next( 0 ) 
root.mainloop()