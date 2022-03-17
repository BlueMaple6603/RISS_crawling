import tkinter
from tkinter import ttk

window = tkinter.Tk()
window.title("RISS 검색기")
window.geometry('700x300')
window.resizable(False, False)


#name1 = tkinter.StringVar()
#label1 = ttk.Label(window, text="주소0")
#label1.grid(column=0, row=0)
#textbox1 = ttk.Entry(window, width=100, textvariable=name1)
#textbox1.grid(column=0, row=1)

#name2 = tkinter.StringVar()
#label2 = ttk.Label(window, text="주소1")
#label2.grid(column=0, row=2)
#textbox2 = ttk.Entry(window, width=100, textvariable=name2)
#textbox2.grid(column=0, row=3)
def input_value():
    def buttonClicked():


    name3 = tkinter.StringVar()
    label3 = ttk.Label(window, text="csv파일명")
    label3.grid(column=0, row=4)
    textbox3 = ttk.Entry(window, width=100, textvariable=name3)
    textbox3.grid(column=0, row=5)

    name4 = tkinter.StringVar()
    label4 = ttk.Label(window, text="페이지수")
    label4.grid(column=0, row=6)
    textbox4 = ttk.Entry(window, width=100, textvariable=name4)
    textbox4.grid(column=0, row=7)

    button = ttk.Button(window, text="실행", command=buttonClicked)
    button.grid(column=0, row=9)

    window.mainloop()