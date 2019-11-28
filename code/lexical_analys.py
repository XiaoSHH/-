import math

#定义符号表
Tokens=[]
Tokens.append(['CONST_ID',"PI",3.1415926,'None'])#0
Tokens.append(['CONST_ID',"E",2.71828,'None'])#1
Tokens.append(['T',"T",0.0,'None'])#2
Tokens.append(['FUNC',"SIN",0.0,'sin'])#3
Tokens.append(['FUNC',"COS",0.0,'cos'])#4
Tokens.append(['FUNC',"TAN",0.0,'tan'])#5
Tokens.append(['FUNC',"LN",0.0,'log'])#6
Tokens.append(['FUNC',"EXP",0.0,'exp'])#7
Tokens.append(['FUNC',"SQRT",0.0,'sqrt'])#8
Tokens.append(['ORIGIN',"ORIGIN",0.0,'None'])#9
Tokens.append(['SCALE',"SCALE",0.0,'None'])#10
Tokens.append(['ROT',"ROT",0.0,'None'])#11
Tokens.append(['IS',"IS",0.0,'None'])#12
Tokens.append(['FOR',"FOR",0.0,'None'])#13
Tokens.append(['FROM',"FROM",0.0,'None'])#14
Tokens.append(['TO',"TO",0.0,'None'])#15
Tokens.append(['STEP',"STEP",0.0,'None'])#16
Tokens.append(['DRAW',"DRAW",0.0,'None'])#17
Tokens.append(['SEMICO',";",0.0,'None'])#18
Tokens.append(['L_BRACKET',"(",0.0,'None'])#19
Tokens.append(['R_BRACKET',")",0.0,'None'])#20
Tokens.append(['COMMA',",",0.0,'None'])#21
Tokens.append(['PLUS',"+",0.0,'None'])#22
Tokens.append(['MINUS',"-",0.0,'None'])#23
Tokens.append(['MUL',"*",0.0,'None'])#24
Tokens.append(['DIV',"/",0.0,'None'])#25
Tokens.append(['POWER',"**",0.0,'None'])#26
Tokens.append(['CONST_ID','None',0.0,'None'])#27
Tokens.append(['ERRTOKEN',"ERRTOKEN",0.0,'None'])#28
#符号表定义完成
def id_la(w):#识别符号
    w=w.upper()#转换为大写
    x=[]
    i=0
    try:
        while i<len(w)-1:
            if w[i].isalpha():#字母开头
                if w[i]=='P':
                    if w[i+1]=='I':
                        x.append(Tokens[0])
                        i+=1
                    else:
                        Tokens[28][1]=w[i]+w[i+1]
                        x.append(Tokens[28])
                        break
                
                elif w[i]=='E':
                    if(w[i+1]=='X'and w[i+2]=='P'):
                        i+=2
                        x.append(Tokens[7])
                    else:
                        x.append(Tokens[1])
                elif w[i]=='T':
                    if(w[i+1]=='A'and w[i+2]=='N'):
                        i+=2
                        x.append(Tokens[5])
                    elif(w[i+1]=='O'):
                        i+=1
                        x.append(Tokens[15])
                    else:
                        x.append(Tokens[2])
                elif w[i]=='S':
                    if(w[i+1]=='I'and w[i+2]=='N'):
                        i+=2
                        x.append(Tokens[3])
                    elif(w[i+1]=='Q'and w[i+2]=='R' and w[i+3]=='T'):
                        i+=3
                        x.append(Tokens[8])
                    elif(w[i+1]=='C' and w[i+2]=='A' and w[i+3]=='L'and w[i+4]=='E'):
                        i+=4
                        x.append(Tokens[10])
                    elif(w[i+1]=='T'and w[i+2]=='E' and w[i+3]=='P'):
                        i+=3
                        x.append(Tokens[16])
                    else:
                        Tokens[28][1]=w[i]+w[i+1]
                        x.append(Tokens[28])
                        break
                elif w[i]=='C':
                    if(w[i+1]=='O'and w[i+2]=='S'):
                        i+=2
                        x.append(Tokens[4])
                    else:
                        Tokens[28][1]=w[i]+w[i+1]+w[i+2]
                        x.append(Tokens[28])
                        break
                elif w[i]=='L':
                    if w[i+1]=='N':
                        i+=1
                        x.append(Tokens[6])
                    else:
                        Tokens[28][1]=w[i]+w[i+1]
                        x.append(Tokens[28])
                        break
                elif w[i]=='O':
                    if w[i+1]=='R' and w[i+2]=='I' and w[i+3]=='G'and w[i+4]=='I'and w[i+5]=='N':
                        i+=5
                        x.append(Tokens[9])
                    else:
                        Tokens[28][1]=w[i]+w[i+1]
                        x.append(Tokens[28])
                        break
                elif w[i]=='R':
                    if w[i+1]=='O' and w[i+2]=='T':
                        i+=2
                        x.append(Tokens[11])
                    else:
                        Tokens[28][1]=w[i]+w[i+1]
                        x.append(Tokens[28])
                        break
                elif w[i]=='I':
                    if w[i+1]=='S':
                        i+=1
                        x.append(Tokens[12])
                    else:
                        Tokens[28][1]=w[i]+w[i+1]
                        x.append(Tokens[28])
                        break
                elif w[i]=='F':
                    if(w[i+1]=='O'and w[i+2]=='R'):
                        i+=2
                        x.append(Tokens[13])
                    elif(w[i+1]=='R'and w[i+2]=='O' and w[i+3]=='M'):
                        i+=3
                        x.append(Tokens[14])
                    else:
                        Tokens[28][1]=w[i]+w[i+1]
                        x.append(Tokens[28])
                        break
                elif w[i]=='D':
                    if w[i+1]=='R' and w[i+2]=='A' and w[i+3]=='W':
                        i+=3
                        x.append(Tokens[17])
                    else:
                        Tokens[28][1]=w[i]+w[i+1]
                        x.append(Tokens[28])
                        break
                else:
                    Tokens[28][1]=w[i]
                    x.append(Tokens[28])
                    break            
            elif w[i].isdigit():#数字常量
                num=''
                while(w[i].isdigit() or w[i]=='.'):
                    num+=w[i]
                    i+=1
                Tokens[27][2]=float(num)
                x.append(Tokens[27][:])
                i-=1
            else:#符号
                if w[i]==';':
                    x.append(Tokens[18])
                elif w[i]=='(':
                    x.append(Tokens[19])
                elif w[i]==')':
                    x.append(Tokens[20])
                elif w[i]==',':
                    x.append(Tokens[21])
                elif w[i]=='+':
                    x.append(Tokens[22])
                elif w[i]=='-':
                    x.append(Tokens[23])
                elif w[i]=='*'and w[i+1]=='*':
                    x.append(Tokens[26])
                    i+=1
                elif w[i]=='*':
                    x.append(Tokens[24])
                elif w[i]=='/':
                    x.append(Tokens[25])
                else:
                    Tokens[28][1]=w[i]
                    x.append(Tokens[28])
                    break
            i+=1
    except TypeError:
        Tokens[28][1]='TypeError'
        x.append(Tokens[28])
    except IndexError:
        Tokens[28][1]='IndexError'
        x.append(Tokens[28])
    except ValueError:
        Tokens[28][2]='ValueError'
        x.append(Tokens[28])
    return x
def lexical_analys(w):
    #滤掉无用成分
    i=0
    while(i<len(w)-2):
        if((w[i]=='-'and w[i+1]=='-')or( w[i]=='/' and w[i+1]=='/')):
            if(i<len(w)-2):
                for j in range(i,len(w)-2):
                    if(w[j]=='\n'):
                        w=w[:i]+w[j+1:]
                        break
                    if(j==len(w)-3):
                        w=w[:i]
        else:i+=1
    i=0
    while(i<len(w)-1):
        if(w[i]==' 'or w[i]=='\t' or w[i]=='\n' or w[i]=='\r'):
            if(i!=len(w)-1):
                w=w[:i]+w[i+1:]
            else:
                w=w[:i]
        else:
            i+=1
    x=id_la(w)#识别字符
    #过滤完成
    return x
