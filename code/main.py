from tkinter import *           # 导入 Tkinter 库
import lexical_analys
import parser_analys
import semantic_analys
import tkinter.messagebox
import math
root = Tk()                     # 创建窗口对象
root.title("我的编译器")          #定义窗口标题
root.geometry('900x600')        #定义窗口大小
global back
global byBack
global text
global canvas
global Parameer
byBack=1
def word():#进行词法分析
    global back
    global text
    w=text.get(1.0,END)
    back=w[:]
    x=lexical_analys.lexical_analys(w)
    text.delete(1.0,END)
    text.insert(INSERT,'类别\t\t')
    text.insert(INSERT,'原始输入\t\t')
    text.insert(INSERT,'值\t\t')
    text.insert(INSERT,'函数地址\t\t\n')
    for i in x:
        text.insert(INSERT,i[0])
        text.insert(INSERT,'\t\t')
        text.insert(INSERT,i[1])
        text.insert(INSERT,'\t\t')
        text.insert(INSERT,i[2])
        text.insert(INSERT,'\t\t')
        text.insert(INSERT,i[3])
        text.insert(INSERT,'\t\t\n')
def pa():
    global back
    global text
    w=text.get(1.0,END)
    back=w[:]
    x=lexical_analys.lexical_analys(w)
    t=parser_analys.Parser(x)
    text.delete(1.0,END)
    text.insert(INSERT,t)

def semantic():
    global back
    global byBack
    global text
    global canvas
    global Parameer
    w=text.get(1.0,END)
    back=w[:]
    byBack=0
    text.pack_forget()
    canvas =Canvas(root,width=900,height=600,bg='white')
    canvas.pack(expand=YES,fill=BOTH)
    x=lexical_analys.lexical_analys(w)
    EX=semantic_analys.Parser(x)
    Parameer=0
    Ox=0
    Oy=0
    Sx=1
    Sy=1
    R=0
    try:
        for i in EX:
            if i[0]=='ORIGIN':
                Ox=GetExprValue(i[1])
                Oy=GetExprValue(i[2])
            elif i[0]=='ROT':
                R=GetExprValue(i[1])
            elif i[0]=='SCALE':
                Sx=GetExprValue(i[1])
                Sy=GetExprValue(i[2])
            elif i[0]=='FOR':
                Parameer=GetExprValue(i[1])
                end=GetExprValue(i[2])
                step=GetExprValue(i[3])
                while(Parameer<end):
                    x=GetExprValue(i[4])
                    y=GetExprValue(i[5])
                    x*=Sx
                    y*=Sy
                    x,y=x*math.cos(R)+y*math.sin(R),y*math.cos(R)-x*math.sin(R)
                    x+=Ox
                    y+=Oy
                    canvas.create_line(x,y,x+1,y+1,width=1,fill='red')
                    Parameer+=step
            else:
                tkinter.messagebox.showinfo("编译错误","非法语句"+i[0])
                return
    except :
        tkinter.messagebox.showinfo("编译错误","非法表达式")
def ba():
    global back
    global byBack
    global text
    global canvas
    if byBack==1:
        text.delete(1.0,END)
        text.insert(INSERT,back)
    else:
        canvas.pack_forget()
        text = Text(root,width=900,height=600)#创建文本框
        text.pack()                #显示文本框
        text.insert(INSERT,back)
        byBack=1

def GetExprValue(x):
    global Parameer
    if x[0]=='PLUS':
        return GetExprValue(x[1])+GetExprValue(x[2])
    elif x[0]=='MINUS':
        return GetExprValue(x[1])-GetExprValue(x[2])
    elif x[0]=='MUL':
        return GetExprValue(x[1])*GetExprValue(x[2])
    elif x[0]=='DIV':
        return GetExprValue(x[1])/GetExprValue(x[2])
    elif x[0]=='POWER':
        return GetExprValue(x[1])**GetExprValue(x[2])
    elif x[0]=='FUNC':
        if x[1]=='SIN':
            return math.sin(GetExprValue(x[2]))
        elif x[1]=='COS':
            return math.cos(GetExprValue(x[2]))
        elif x[1]=='TAN':
            return math.tan(GetExprValue(x[2]))
        elif x[1]=='LN':
            return math.log(GetExprValue(x[2]))
        elif x[1]=='EXP':
            return math.exp(GetExprValue(x[2]))
        elif x[1]=='SQRT':
            return math.sqrt(GetExprValue(x[2]))
    elif x[0]=='CONST_ID':
        return x[1]
    elif x[0]=='T':
        return Parameer
    else:
        print('jinlai')
        print(x[0])
        raise NameError('cuouw')

menubar = Menu(root)            # 创建一个导航菜单
#创建菜单词法，然后将其加入到顶级的菜单栏中
menubar.add_command(label=" 词 ", command=word)
#创建菜单语法，然后将其加入到顶级的菜单栏中
menubar.add_command(label=" 语 ", command=pa)
#创建菜单语义，然后将其加入到顶级的菜单栏中
menubar.add_command(label=" 义 ", command=semantic)
#创建菜单back，然后将其加入到顶级的菜单栏中
menubar.add_command(label=" back ", command=ba)

root.config(menu=menubar)       #显示菜单

text = Text(root,width=900,height=600)#创建文本框
text.pack()                #显示文本框


root.mainloop() #进入消息循环
