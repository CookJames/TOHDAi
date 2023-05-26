import tkinter as tk
from tkinter import ttk
import webbrowser
import pyperclip
from time import sleep
import pyautogui as gui
import sqlite3
from tkinter import messagebox

conn = sqlite3.connect('TOHDAi.db')
table_name = 'login_elem'
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS login_elem (id integer PRIMARY KEY AUTOINCREMENT, number_school0 text, password0 text,
 number_school text, password text, confidence int);''')
c.execute('select count(*) from login_elem')
count = c.fetchone()
if count[0] < 1:
    c.execute("INSERT INTO login_elem(number_school0,password0,number_school,password,confidence) VALUES('','','','','6')")
    c.execute('select count(*) from login_elem')
    count = c.fetchone() 
conn.commit()  
conn.close()

class ShortCutButton(tk.Button):   #1
    '''
    登録したurlをブラウザで開くボタンを生成
    clipwordを登録すると、登録した文字をクリップボードにコピー（任意）
    '''
    def __init__(self, title,  url, clipword=None, master=None):    #2
        if title == "blackbord":
            super().__init__(master, bg='gray10', activebackground='gray15', highlightthickness=0, bd=0, image=img_Bb, compound='top', cursor='top_left_corner', text=None, command=self.button_clicked) #3
        elif title == "COMITS2":
            super().__init__(master, bg='gray10', activebackground='gray15', highlightthickness=0, bd=0, image=img_COMITS, compound='top', cursor='top_left_corner', text=None, command=self.button_clicked) 
        elif title=="CHIPS":
            super().__init__(master, bg='gray10', activebackground='gray15', highlightthickness=0, bd=0, padx=10, image=img_CHIPS, compound='top', cursor='top_left_corner', text=None, command=self.button_clicked)    
            
        self.url = url  #4
        self.clipword = clipword    #5

    def button_clicked(self):   #6 
        conn = sqlite3.connect('TOHDAi.db')        
        c = conn.cursor()    
        if c.execute('''select trim(replace(number_school0, ' ', '_')) from login_elem'''):    
            acquire_num0 = c.fetchone()
        if c.execute('''select trim(replace(password0, ' ', '_')) from login_elem'''):    
            acquire_pass0 = c.fetchone()                
        if c.execute('''select trim(replace(number_school, ' ', '_')) from login_elem'''):    
            acquire_num = c.fetchone()
        if c.execute('''select trim(replace(password, ' ', '_')) from login_elem'''):    
            acquire_pass = c.fetchone()  
        if c.execute('''select trim(replace(confidence, ' ', '_')) from login_elem'''):    
            acquire_conf = c.fetchone()  
            acquire_conf = round(int(acquire_conf[0]) * 0.1, 2)           
        if self.clipword:
            pyperclip.copy(self.clipword)   #7

        if self.url:    
            if not acquire_num0[0] or not acquire_pass0[0] or not acquire_num[0] or not acquire_pass[0]:
                messagebox.showerror('エラー', '「SETTING」でアカウントを登録してください。')   
            else:                 
                webbrowser.open(self.url)   #8
                if self.url == "https://nuchs.blackboard.com/":
                    for tryCount in range(10):
                        try:                        
                            if gui.locateOnScreen(r'screen1.png', confidence=acquire_conf):   
                                sleep(0.2)                                                                                         
                                gui.press('tab')
                                gui.press('enter')                                
                            if gui.locateOnScreen(r'screen3.png', confidence=acquire_conf):   
                                sleep(0.3)                                                                                             
                                gui.press('tab')
                                pyperclip.copy(acquire_num0[0])
                                gui.hotkey('ctrl', 'v')
                                gui.press('tab')
                                gui.write(acquire_pass0[0])
                                gui.press('enter')
                                break
                        except gui.ImageNotFoundException:
                            sleep(1)  
                elif self.url == "https://comits2.educ.chs.nihon-u.ac.jp/uniprove_pt/UnLoginAction":                         
                    for tryCount in range(10):
                        try:
                            if gui.locateOnScreen(r'screen.png', confidence=acquire_conf):
                                sleep(0.1)
                                pyperclip.copy(acquire_num[0])
                                gui.hotkey('ctrl', 'v')
                                gui.press('tab')
                                gui.write(acquire_pass[0])
                                gui.press('enter')
                                break
                        except gui.ImageNotFoundException:
                            sleep(1)                        
                elif self.url == "https://www-as1.chs.nihon-u.ac.jp/uniasv2/UnSSOLoginControl":
                    for tryCount in range(10):
                        try:
                            if gui.locateOnScreen(r'screen2.png', confidence=acquire_conf):
                                sleep(0.1)    
                                pyperclip.copy(acquire_num[0])
                                gui.hotkey('ctrl', 'v')
                                gui.press('tab')
                                gui.write(acquire_pass[0])
                                gui.press('enter')
                                break
                        except gui.ImageNotFoundException:
                            sleep(1)                                         


if __name__ == '__main__':
    #1
    word_list = [
        ["blackbord", "https://nuchs.blackboard.com/","学習支援システム"],
        ["COMITS2", "https://comits2.educ.chs.nihon-u.ac.jp/uniprove_pt/UnLoginAction","情報掲示板"],
        ["CHIPS", "https://www-as1.chs.nihon-u.ac.jp/uniasv2/UnSSOLoginControl","履修・成績"]
    ]

    def enter_bg_Button(event):
        if event.widget == button_black:
            button_black.configure(bg='gray15')
        elif event.widget == button_comits:
            button_comits.configure(bg='gray15')
        elif event.widget == button_chips:
            button_chips.configure(bg='gray15')
        else:
            button_setting.configure(bg='gray15')                                    

    def leave_bg_Button(event): 
        if event.widget == button_black:
            button_black.configure(bg='gray10')
        elif event.widget == button_comits:
            button_comits.configure(bg='gray10')
        elif event.widget == button_chips:
            button_chips.configure(bg='gray10')
        else:
            button_setting.configure(bg='gray10')                                    

    def sub_window():            
        conn = sqlite3.connect('TOHDAi.db')
        c = conn.cursor()        
        if c.execute('''select trim(replace(number_school0, ' ', '_')) from login_elem'''):    
            acquire_num0 = c.fetchone()
        if c.execute('''select trim(replace(password0, ' ', '_')) from login_elem'''):    
            acquire_pass0 = c.fetchone()                    
        if c.execute('''select trim(replace(number_school, ' ', '_')) from login_elem'''):    
            acquire_num = c.fetchone()
        if c.execute('''select trim(replace(password, ' ', '_')) from login_elem'''):    
            acquire_pass = c.fetchone()
        if c.execute('''select trim(replace(confidence, ' ', '_')) from login_elem'''):    
            acquire_conf = c.fetchone()                       
        conn.close()                   

        def keep_login_elem():    
            getry01 = entry1_change02.get() 
            getry02 = entry2_change02.get()                                                                                       
            getry1 = entry1_change.get() 
            getry2 = entry2_change.get() 
            if not getry01 and not getry02: 
                label_error = tk.Label(frame_change02, text='ユーザー名を入力してください', foreground='red', bg='gray20')            
                label_error2 = tk.Label(frame_change02, text='パスワードを入力してください', foreground='red', bg='gray20')
                label_error.place(x=25,y=50)                     
                label_error2.place(x=25,y=120) 
                frame_change2.update()              
                frame_change2.after(2000, label_error.destroy(), label_error2.destroy())
            elif not getry01:  
                label_error = tk.Label(frame_change02, text='ユーザー名を入力してください', foreground='red', bg='gray20')                  
                label_error.place(x=25,y=50)                   
                frame_change2.update()                       
                frame_change2.after(2000, label_error.destroy())                 
            elif not getry02:   
                label_error2 = tk.Label(frame_change02, text='パスワードを入力してください', foreground='red', bg='gray20')                
                label_error2.place(x=25,y=120)     
                frame_change2.update()    
                frame_change2.after(2000, label_error2.destroy())
            elif not getry1 and not getry2: 
                label_error = tk.Label(frame_change2, text='IDを入力してください', foreground='red', bg='gray20')            
                label_error2 = tk.Label(frame_change2, text='パスワードを入力してください', foreground='red', bg='gray20')
                label_error.place(x=25,y=50)                     
                label_error2.place(x=25,y=120) 
                frame_change2.update()              
                frame_change2.after(2000, label_error.destroy(), label_error2.destroy())
            elif not getry1:  
                label_error = tk.Label(frame_change2, text='IDを入力してください', foreground='red', bg='gray20')                  
                label_error.place(x=25,y=50)                   
                frame_change2.update()                       
                frame_change2.after(2000, label_error.destroy())                 
            elif not getry2:   
                label_error2 = tk.Label(frame_change2, text='パスワードを入力してください', foreground='red', bg='gray20')                
                label_error2.place(x=25,y=120)     
                frame_change2.update()    
                frame_change2.after(2000, label_error2.destroy())                  
            else: 
                keep_login_elem_db() 
        def keep_login_elem_db():
            getry01 = entry1_change02.get() 
            getry02 = entry2_change02.get()                 
            getry1 = entry1_change.get() 
            getry2 = entry2_change.get()             
            try:
                conn = sqlite3.connect('TOHDAi.db')
                c = conn.cursor()
                c.execute("UPDATE %s SET number_school0=? WHERE id=?" % table_name,(getry01, 1))  
                c.execute("UPDATE %s SET password0=? WHERE id=?" % table_name,(getry02, 1))                 
                c.execute("UPDATE %s SET number_school=? WHERE id=?" % table_name,(getry1, 1))  
                c.execute("UPDATE %s SET password=? WHERE id=?" % table_name,(getry2, 1))                                             
                conn.commit()        
                if c.execute('''select trim(replace(number_school0, ' ', '_')) from login_elem'''):    
                    acquire_num0 = c.fetchone()
                if c.execute('''select trim(replace(password0, ' ', '_')) from login_elem'''):    
                    acquire_pass0 = c.fetchone()                   
                if c.execute('''select trim(replace(number_school, ' ', '_')) from login_elem'''):    
                    acquire_num = c.fetchone()
                if c.execute('''select trim(replace(password, ' ', '_')) from login_elem'''):    
                    acquire_pass = c.fetchone()                    
                conn.close()                                   
            except:
                messagebox.showerror('エラー', '編集内容を正常に保存できませんでした。直らなければホームページ・Twitterから気軽にお問い合わせください')                    
            if not acquire_num[0]:
                pass
            else:         
                label_before.place(x=550,y=0) 
                label_before.configure(text=f'{acquire_num[0]}さんようこそ')                                          
            frame.tkraise()         
            entry1_change02.delete(0, tk.END)
            entry2_change02.delete(0, tk.END)
            entry1_change02.insert(0, acquire_num0[0])
            entry2_change02.insert(0, acquire_pass0[0])                 
            entry1_change.delete(0, tk.END)
            entry2_change.delete(0, tk.END)
            entry1_change.insert(0, acquire_num[0])
            entry2_change.insert(0, acquire_pass[0])
        def keep_adapt_elem():
            getvar = scalevar.get()
            try:
                conn = sqlite3.connect('TOHDAi.db')
                c = conn.cursor()
                c.execute("UPDATE %s SET confidence=? WHERE id=?" % table_name,(getvar, 1))  
                conn.commit()
                if c.execute('''select trim(replace(confidence, ' ', '_')) from login_elem'''):    
                    acquire_conf = c.fetchone()                                          
                conn.close()                      
            except:
                messagebox.showerror('エラー', '編集内容を正常に保存できませんでした。直らなければホームページ・Twitterから気軽にお問い合わせください')                                                                                       
            frame.tkraise()          
            scalevar.set(int(acquire_conf[0]))        

        def change_change():            
            frame_change.tkraise()
        def change_help():
            frame_help.tkraise()        

        def pass_disp():
            getvar0 = keep_button_var02.get()            
            getvar = keep_button_var.get()            
            if getvar0 == True:
                entry2_change02.configure(show='')
            else:
                entry2_change02.configure(show='・')  
            if getvar == True:
                entry2_change.configure(show='')
            else:
                entry2_change.configure(show='・') 

        def labelvalue(event):
            getscale = scalevar.get()
            labelvaluebutton.configure(text=getscale)

        def hover_change_button(event):            
            global my_img_before2
            my_img_before2 = tk.PhotoImage(file=r"25889_2-removebg-previewh (2).png")
            change_button.configure(image=my_img_before2)                        
        def hover_change_button2(event):
            global my_img_before
            my_img_before = tk.PhotoImage(file=r"25889_2-removebg-preview.png")
            change_button.configure(image=my_img_before)
        def hover_keep_button(event):
            global my_img2
            my_img2 =  tk.PhotoImage(file=r'subscribeh.png')
            keep_button.configure(image=my_img2)    
        def hover_keep_button2(event):
            global my_img
            my_img =  tk.PhotoImage(file=r'subscribe.png')
            keep_button.configure(image=my_img)      
        def hover_help_button(event):
            global my_img_help2
            my_img_help2 = tk.PhotoImage(file=r'h.png')  
            help_button.configure(image=my_img_help2)
        def hover_help_button2(event):
            global my_img_help
            my_img_help = tk.PhotoImage(file=r'25889-removebg-preview.png')  
            help_button.configure(image=my_img_help)      
        def hover_adapt_button(event):
            global my_img_up2
            my_img_up2 = tk.PhotoImage(file=r'updateh.png')      
            adapt_button.configure(image=my_img_up2)
        def hover_adapt_button2(event):
            global my_img_up
            my_img_up = tk.PhotoImage(file=r'update.png')      
            adapt_button.configure(image=my_img_up)                       

        sub_win = tk.Toplevel()
        sub_win.resizable(0, 0)
        sub_win.geometry("700x300+620+250")   
        sub_win.configure(bg='gray10')     
        sub_win.grid_rowconfigure(0, weight=1)
        sub_win.grid_columnconfigure(0, weight=1)                 

        men = tk.Menu(sub_win, bg='black', tearoff=0) 
        sub_win.config(menu=men)        
        menu_file2 = tk.Menu(sub_win, tearoff=0, activebackground='sky blue', activeforeground='black') 
        menu_file3 = tk.Menu(sub_win, tearoff=0, activebackground='sky blue', activeforeground='black') 
        def commnad_homepage():
            webbrowser.open('http://127.0.0.1:5500/TOHDAi.html')
        def command_twitter():
            webbrowser.open('https://twitter.com/CookJam75250567')
        men.add_cascade(label='ホームページ', menu=menu_file2)
        menu_file2.add_command(label='公式ホームページ', command=commnad_homepage)        
        men.add_cascade(label='Twitter', menu=menu_file3)
        menu_file3.add_command(label='公式アカウント', command=command_twitter)                

        frame = tk.Frame(sub_win, bg='#151922')
        frame.grid(row=0, column=0, sticky="nsew")   
        frame_change = tk.Frame(sub_win, bg='gray20')
        frame_change.grid(row=0, column=0, sticky="nsew") 
        frame_change02 = tk.LabelFrame(frame_change, foreground='snow', width=300, height=200, bd=2,
                                      labelanchor='n', text='NUアカウント登録フォーム(Blackbord)', bg='gray20')            
        frame_change2 = tk.LabelFrame(frame_change, foreground='snow', width=300, height=200, bd=2,
                                      labelanchor='n', text='教育用アカウント登録フォーム', bg='gray20')
        frame_change02.place(x=35,y=20)          
        frame_change2.place(x=365,y=20)  

        frame_help = tk.Frame(sub_win, bg='gray10')  
        frame_help.grid(row=0, column=0, sticky='nsew') 
        scalevar = tk.IntVar(value=int(acquire_conf[0]))   
        s = ttk.Style()
        s.configure('TScale', background='gray10')         
        scale_ttk = ttk.Scale(frame_help, from_=0,to=10, orient='horizontal', length=300, variable=scalevar, style='TScale', command=labelvalue)
        scale_ttk.place(x=110,y=70)  
        labelvaluebutton = tk.Label(frame_help, bg='gray10', fg='snow', text=acquire_conf[0])   
        labelvaluebutton.place(x=410,y=70)   
        change_label = tk.Label(frame_help, text='confidence', fg='snow', bg='gray10', font=('normal', 10, 'bold'))
        change_label2 = tk.Label(frame_help, fg='snow', bg='gray10', justify='left', text='　ログイン時のミスを調整します。他のURL欄に入力された場合値を上げます。無反応\nの時は値を下げます。（推奨値：5～7）')        
        change_label.place(x=100,y=0)
        change_label2.place(x=100,y=20)
        labelframe_help = tk.LabelFrame(frame_help, bg='gray10', foreground='snow', width=500, height=190, bd=2, text='正しく起動しないときは')  
        labelframe_help.place(x=100,y=100)
        labelcaretitle = tk.Label(labelframe_help, fg='snow', bg='gray10', text='1 ブラウザのURL欄にフォーカスが当たっていませんか？', font=('normal', 8, 'bold'))
        labelcaretitle.place(x=5,y=0)
        labelcarebody = tk.Label(labelframe_help, fg='snow', bg='gray10', text='　同一のブラウザにて、ボタンで開くタブとは別のタブでURL欄にフォーカスが当たってい\nると正常にプログラムが働かないことがあります。URL欄のフォーカスを外す、フォーカスの\n当たっているタブもしくはブラウザごと消すと改善する場合があります。',
                                 justify='left')
        labelcarebody.place(x=0,y=20)                                        
        labelcaretitle2 = tk.Label(labelframe_help, fg='snow', bg='gray10', text='2 自動ログイン中に他の操作をしていませんか？', font=('normal', 8, 'bold'))
        labelcaretitle2.place(x=5,y=80)
        labelcarebody2 = tk.Label(labelframe_help, fg='snow', bg='gray10', text='　プログラム起動中や自動ログイン時にキーボード、マウス、パッドなどの入力によって\n正常にプログラムが働かないことがあります。自動ログイン中に他の入力をしなければ\n改善する場合があります。',
                                 justify='left')                                 
        labelcarebody2.place(x=0,y=100)
        global my_img_up
        my_img_up = tk.PhotoImage(file=r"update.png") 
        adapt_button = tk.Button(frame_help,image=my_img_up,bd=0,bg='gray10',activebackground='gray10',command=keep_adapt_elem,cursor='top_left_corner')
        adapt_button.place(x=450,y=55)
        adapt_button.bind('<Enter>', hover_adapt_button)
        adapt_button.bind('<Leave>', hover_adapt_button2)


        canvas = tk.Canvas(frame, bg="black", width=705, height=200, highlightthickness=0)
        canvas.place(x=-5, y=-5)
        global bg
        bg = tk.PhotoImage(file=r'cPBgZjE0x9iy49r1676373326_1676373585.png', width=705, height=205)
        bg = bg.subsample(1, 1)
        canvas.create_image(0, 0, image=bg, anchor=tk.NW) 

        if not acquire_num[0]:
            label_before = tk.Label(frame, text=f'{acquire_num[0]}さんようこそ', bg='#0c2934', foreground='snow')
            label_before.place(x=550,y=0) 
            label_before.place_forget()
        else:
            label_before = tk.Label(frame, text=f'{acquire_num[0]}さんようこそ', bg='#0c2934', foreground='snow')
            label_before.place(x=550,y=0)        
                
        global my_img_before
        global my_img_help
        my_img_before0 = tk.PhotoImage(file=r'25889_2-removebg-preview.png')
        my_img_before = tk.PhotoImage(file=r"25889_2-removebg-preview.png")         
        change_button = tk.Button(frame,image=my_img_before,bd=0,bg='#151922',activebackground='#151922',command=change_change,cursor='top_left_corner') 
        my_img_help = tk.PhotoImage(file=r"25889-removebg-preview.png") 
        help_button = tk.Button(frame,image=my_img_help,bd=0,bg='#151922',activebackground='#151922',command=change_help,cursor='top_left_corner')                 
        change_button.place(x=350,y=215)
        help_button.place(x=100,y=215)
        change_button.bind('<Enter>', hover_change_button)
        change_button.bind('<Leave>', hover_change_button2)
        help_button.bind('<Enter>', hover_help_button)
        help_button.bind('<Leave>', hover_help_button2)
        labelhelp = tk.Label(frame, text='困ったとき...', bg='#151922', fg='snow')
        labelsubsc = tk.Label(frame, text='アカウント登録(NU&教育用)', bg='#151922', fg='snow')
        labelhelp.place(x=190,y=200)
        labelsubsc.place(x=390,y=200)

        label1_change02 = tk.Label(frame_change02, text='ユーザー名(@以降は省略)', width=20, fg='snow', bg='gray20')        
        label2_change02 = tk.Label(frame_change02, text='パスワード', width=10, fg='snow', bg='gray20')        
        se = ttk.Style()  
        se.configure('TLabel', background='gray40', foreground='cyan')         
        entry1_change02 = ttk.Entry(frame_change02, width=30, style='TLabel')
        entry2_change02 = ttk.Entry(frame_change02, width=30, show='・', style='TLabel')
        entry1_change02.insert(0, acquire_num0[0])
        entry2_change02.insert(0, acquire_pass0[0])
        s2 = ttk.Style()
        s2.configure('TCheckbutton', background='gray40', foreground='cyan')  
        keep_button_var02 = tk.BooleanVar()        
        keep_button_chk02 = ttk.Checkbutton(frame_change02, command=pass_disp, text='パスワードを表示する', variable=keep_button_var02, onvalue=True, offvalue=False)        
        label1_change02.place(x=22,y=0)
        label2_change02.place(x=12,y=70)        
        entry1_change02.place(x=25,y=25)
        entry2_change02.place(x=25,y=95)        
        keep_button_chk02.place(x=25,y=145)

        label1_change = tk.Label(frame_change2, text='ID', width=5, fg='snow', bg='gray20')        
        label2_change = tk.Label(frame_change2, text='パスワード', width=10, fg='snow', bg='gray20')                                                      
        entry1_change = ttk.Entry(frame_change2, width=30, style='TLabel')
        entry2_change = ttk.Entry(frame_change2, width=30, show='・', style='TLabel')
        entry1_change.insert(0, acquire_num[0])
        entry2_change.insert(0, acquire_pass[0])
        global my_img       
        my_img = tk.PhotoImage(file=r"subscribe.png") 
        keep_button = tk.Button(frame_change,image=my_img,bd=0,bg='gray20',activebackground='gray20',command=keep_login_elem,cursor='top_left_corner')
        keep_button.bind('<Enter>', hover_keep_button)
        keep_button.bind('<Leave>', hover_keep_button2)
        keep_button_var = tk.BooleanVar()
        s2 = ttk.Style()
        s2.configure('TCheckbutton', background='gray20', foreground='snow')          
        keep_button_chk = ttk.Checkbutton(frame_change2, style='TCheckbutton', command=pass_disp, text='パスワードを表示する', variable=keep_button_var, onvalue=True, offvalue=False)        
        label1_change.place(x=10,y=0)
        label2_change.place(x=12,y=70)        
        entry1_change.place(x=25,y=25)
        entry2_change.place(x=25,y=95)
        keep_button.place(x=275,y=240)
        keep_button_chk.place(x=25,y=145)
        frame.tkraise()
            
    root = tk.Tk()
    root.iconbitmap(default=r'favicon.ico')
    root.geometry("320x80+1590+900")
    root.resizable(0, 0)
    root.configure(bg='gray10')
    root.title('')
    img_Bb = tk.PhotoImage(file=r"PuuptDLO3BxwF5a1676253668_1676253951.png").subsample(2, 2)
    img_Bbh = tk.PhotoImage(file=r"PuuptDLO3BxwF5a1676253668_1676253951.png").subsample(2, 2)
    img_COMITS = tk.PhotoImage(file=r"UX9jjl4t7uIoZ4Z1676254066_1676254246.png").subsample(2, 2)
    img_COMITSh = tk.PhotoImage(file=r"UX9jjl4t7uIoZ4Z1676254066_1676254246.png").subsample(2, 2)
    img_CHIPS = tk.PhotoImage(file=r"rSyWy6EskXCyvhK1676254785_1676254815.png").subsample(2, 2)
    img_CHIPSh = tk.PhotoImage(file=r"rSyWy6EskXCyvhK1676254785_1676254815.png").subsample(2, 2)
    img_setting = tk.PhotoImage(file=r"FQ4PujOaENJwbWk1676255229_1676255244-removebg-preview.png").subsample(2, 2)
    img_settingh = tk.PhotoImage(file=r"FQ4PujOaENJwbWk1676255229_1676255244-removebg-preview.png").subsample(2, 2)
    for info in word_list:
        button = ShortCutButton(*info)
        button_black = ShortCutButton("blackbord", "https://nuchs.blackboard.com/","学習支援システム")
        button_black.bind('<Enter>', enter_bg_Button)
        button_black.bind('<Leave>', leave_bg_Button)
        button_black.grid(row=0,column=0)
        button_comits = ShortCutButton("COMITS2", "https://comits2.educ.chs.nihon-u.ac.jp/uniprove_pt/UnLoginAction","情報掲示板")
        button_comits.bind('<Enter>', enter_bg_Button)
        button_comits.bind('<Leave>', leave_bg_Button)
        button_comits.grid(row=0,column=1)
        button_chips = ShortCutButton("CHIPS", "https://www-as1.chs.nihon-u.ac.jp/uniasv2/UnSSOLoginControl","履修・成績")
        button_chips.bind('<Enter>', enter_bg_Button)
        button_chips.bind('<Leave>', leave_bg_Button)
        button_chips.grid(row=0,column=2) 
        button_setting = tk.Button(root, bg='gray10', activebackground='gray15', highlightthickness=0, bd=0, padx=10, image=img_setting, compound='top', cursor='top_left_corner', text=None, command=sub_window)
        button_setting.bind('<Enter>', enter_bg_Button)
        button_setting.bind('<Leave>', leave_bg_Button)
        button_setting.grid(row=0,column=3)

    root.mainloop()


