global Parameter#参数T的存储空间

global v#记号流位置

global EX#返回的树

def FetchToken(w):#取记号流中下一个记号
    global v
    v+=1
    if(w[v][0]=='ERRTOKEN'):SyntaxErr(1,w)

def MatchToken(w,x):#匹配记号
    global v
    if (w[v][0]!=x):SyntaxErr(2,w)
    FetchToken(w)

def SyntaxErr(x,w):#语法错误处理
    global v
    if x==1:
        ErrMsg('错误记号',w[v][1])
    elif x==2:
        ErrMsg('不是预期记号',w[v][1])
   
def ErrMsg(x1,x2):#打印错误信息
    global EX
    EX.append('Error in'+x1+x2)
    raise NameError('cuouw')

def Parser(w):#语法分析入口
    global EX
    global Parameter
    global v
    EX=[]
    v=-1
    Parameter=0
    w.append(['NONTOKEN',"NONTOKEN",0.0,'None'])
    try:
        FetchToken(w)#获取第一个记号
        Program(w)#递归下降分析
        return EX
    except:
        return EX

def Program(w):
    global v
    while w[v][0]!='NONTOKEN':
        Statement(w);
        MatchToken(w,'SEMICO')

def Statement(w):
    global v
    if w[v][0]=='ORIGIN':
        OriginStatement(w)
    elif w[v][0]=='SCALE':
        ScaleStatement(w)
    elif w[v][0]=='ROT':
        ROTStatement(w)
    elif w[v][0]=='FOR':
        FORStaement(w)
    else:
        SyntaxErr(2,w)

def OriginStatement(w):
    global EX
    MatchToken (w,'ORIGIN')
    MatchToken (w,'IS')
    MatchToken (w,'L_BRACKET')
    tmp1 = Expression(w)
    MatchToken (w,'COMMA')
    tmp2 = Expression(w)
    MatchToken (w,'R_BRACKET')
    EX.append(['ORIGIN',tmp1,tmp2])

def ScaleStatement(w):
    global EX
    MatchToken (w,'SCALE')
    MatchToken (w,'IS')
    MatchToken (w,'L_BRACKET')
    tmp1 = Expression(w)
    MatchToken (w,'COMMA')
    tmp2 = Expression(w)
    MatchToken (w,'R_BRACKET')
    EX.append(['SCALE',tmp1,tmp2])

def ROTStatement(w):
    global EX
    MatchToken (w,'ROT')
    MatchToken (w,'IS')
    tmp = Expression(w)
    EX.append(['ROT',tmp])

def FORStaement(w):
    global EX
    MatchToken (w,'FOR')
    MatchToken(w,'T')
    MatchToken (w,'FROM')
    start_ptr = Expression(w)	# 构造参数起始表达式语法树
    MatchToken (w,'TO')
    end_ptr = Expression(w)	#构造参数终结表达式语法树
    MatchToken (w,'STEP')
    step_ptr = Expression(w)	# 构造参数步长表达式语法树
    MatchToken (w,'DRAW')
    MatchToken (w,'L_BRACKET')
    x_ptr = Expression(w)	 # 构造横坐标表达式语法树
    MatchToken (w,'COMMA')
    y_ptr = Expression(w)	#构造纵坐标表达式语法树
    MatchToken (w,'R_BRACKET')
    EX.append(['FOR',start_ptr,end_ptr,step_ptr,x_ptr,y_ptr])

def Expression(w):#表达式的递归子程序
    global v
    left = Term(w)#分析左操作数且得到其语法树
    while (w[v][0]=='PLUS'or w[v][0]=='MINUS'):
        token_tmp=w[v][0]
        MatchToken(w,token_tmp)
        right=Term(w)#分析右操作数且得到其语法树
        left = MakeExprNode(token_tmp, left, right)
	    # 构造运算的语法树，结果为左子树
    return left		#返回最终表达式的语法树

def Term(w):
    global v
    left = Factor(w);
    while (w[v][0]=='MUL' or w[v][0]=='DIV'):
        token_tmp = w[v][0]
        MatchToken(w,token_tmp)
        right = Factor(w);
        left = MakeExprNode(token_tmp, left, right);
    return left

def Factor(w):
    global v
    if(w[v][0] == 'PLUS'): 	# 匹配一元加运算
        MatchToken(w,'PLUS')
        right = Factor(w)#  表达式退化为仅有右操作数的表达式
    elif(w[v][0] == 'MINUS'):# 匹配一元减运算
        MatchToken(w,'MINUS')#表达式转化为二元减运算的表达式
        right = Factor(w)
        left=['CONST_ID',0.0]
        right = MakeExprNode('MINUS', left, right);
    else:
        right = Component(w)# 匹配非终结符Component
    return right;

def Component(w):
    global v
    left = Atom(w);
    if(w[v][0] == 'POWER'):
        MatchToken(w,'POWER');
        right = Component(w);	# 递归调用Component以实现POWER的右结合
        left = MakeExprNode('POWER', left, right)
    return left;

def Atom(w):
    global v
    t=w[v][:]
    if(w[v][0] == 'CONST_ID'):
        MatchToken(w,'CONST_ID')
        address=MakeExprNode('CONST_ID',t[2])
    elif w[v][0] == 'T':
        MatchToken(w,'T')
        address=MakeExprNode('T')
    elif w[v][0] == 'FUNC':
        MatchToken(w,'FUNC')
        MatchToken(w,'L_BRACKET')
        tmp=Expression(w)
        address=MakeExprNode('FUNC',t[1],tmp)
        MatchToken(w,'R_BRACKET')
    elif w[v][0] == 'L_BRACKET':
        MatchToken(w,'L_BRACKET')
        address=Expression(w)
        MatchToken(w,'R_BRACKET')
    else:
        SyntaxErr(2,w)
    return address

def MakeExprNode(opcode,*LR):
    node=[opcode,]
    if opcode=='CONST_ID':#常数节点
        node.append(LR[0])
    elif opcode =='T':#参数节点
        node.append(0)
    elif opcode=='FUNC':#函数调用节点
        node.append(LR[0])
        node.append(LR[1])
    else:#二元运算节点
        node.append(LR[0])
        node.append(LR[1])
    return node
