from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
 
## 전역 변수 선언 부분 ##
#filename = ""
 
## 함수 선언 부분 ##
def func_open() :
    global filename     # 오픈한 이미지를 확대, 축소하기 위해 변수 공유
    filename = askopenfilename(parent = window, filetypes =
    (("GIF 파일", "*.gif"), ("모든 파일", "*.*")))
    photo = PhotoImage(file = filename)
    pLabel.configure(image = photo)
    pLabel.image = photo
 
def func_exit() :
    window.quit()
    window.destroy()
 
def func_zoom() :   # 확대 함수
    value = askinteger("확대배수", "확대할 배수를 입력하세요(2~8)", minvalue = 2, maxvalue = 8) # 확대할 배수 입력
    photo = PhotoImage(file = filename) # func_open에서 선택된 파일
    photo = photo.zoom(value,value) # 이미지 확대
    pLabel.configure(image = photo) # 윈도창에 나타내기
    pLabel.image = photo
 
def func_subsample() :   # 축소 함수
    value = askinteger("축소배수", "축소할 배수를 입력하세요(2~8)", minvalue = 2, maxvalue = 8) # 축소할 배수 입력
    photo = PhotoImage(file = filename) # func_open에서 선택된 파일
    photo = photo.subsample(value,value) # 이미지 축소
    pLabel.configure(image = photo) # 윈도창에 나타내기
    pLabel.image = photo
 
## 메인 코드 부분 ##
window = Tk()
window.geometry("400x400")
window.title("사진 확대, 축소하기")
 
photo = PhotoImage()
pLabel = Label(window, image = photo)
pLabel.pack(expand = 1, anchor = CENTER)
 
mainMenu = Menu(window)
window.config(menu = mainMenu)
 
fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "파일", menu = fileMenu)
fileMenu.add_command(label = "파일 열기", command = func_open)
fileMenu.add_separator()
fileMenu.add_command(label = "프로그램 종료", command = func_exit)
 
## 이미지 효과 메뉴 추가하는 부분 ##
imageMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "이미지 효과", menu = imageMenu)
imageMenu.add_command(label = "확대하기", command = func_zoom)
imageMenu.add_separator()
imageMenu.add_command(label = "축소하기", command = func_subsample)
 
 
window.mainloop()
