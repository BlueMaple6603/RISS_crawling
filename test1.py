from tkinter import *

def pressed():
    label.configure(text="버튼을 누름")
def confirm():
    in_text = "입력 내용 : " + input_text.get()
    label.configure(text=in_text)

window = Tk()
window.title("tkinter 테스트")
window.geometry('320x240')

label = Label(window, text="라벨테스트", font=("돋음", 10))
label.grid(column=0, row=0)

button = Button(window, text="버튼테스트", bg="blue", fg="white", command=pressed)
button.grid(column=0, row=1)

input_text = Entry(window, width=30)
input_text.grid(column=0, row=2)

button = Button(window, text="확인", command=confirm)
button.grid(column=1, row=2)

window.mainloop()
