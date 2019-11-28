global Parameter#参数T的存储空间

global v#记号流位置

global text#返回的文本

global haha#决定是否打印语法树
haha=1
def enter(x):#辅助函数入口
    global text
    text+='enter in '
    text+=x
    text+='\n'
def back(x):#辅助函数出口
    global text
    text+='exit from '
    text+=x
    text+='\n'
def call_match(x):#辅助函数符号匹配
    global text
    text+='matchtoken  '
    text+=x
    text+='\n'
def Tree_trace(x):#辅助函数输出树
    PrintSyntaxTree(x, 1);

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
    global text
    text+='Error in'+x1+x2
    raise NameError('cuouw')

def PrintSyntaxTree(x,indent):#先序遍历并打印表达式的语法树
    global text
    for i in range(indent):
        text+='\t'
    if x[0] == 'PLUS':
        text+='+\n'
    elif x[0]=='MINUS':
        text+='-\n'
    elif x[0]=='MUL':
        text+='*\n'
    elif x[0]=='DIV':
        text+='/\n'
    elif x[0]=='POWER':
        text+='**\n'
    elif x[0]=='FUNC':
        text+=x[1]+'\n'
    elif x[0]=='CONST_ID':
        text+=str(x[1])+'\n'
    elif x[0]=='T':
        text+='T\n'
    else:
        text+="Error Tree Node !\n"
    if(x[0]=='CONST_ID' or x[0]=='T'):
        return
    if(x[0]=='FUNC'):
        PrintSyntaxTree(x[2],indent+1)
    else:
        PrintSyntaxTree(x[1],indent+1)
        PrintSyntaxTree(x[2],indent+1)
def Parser(w):#语法分析入口
    global text
    global Parameter
    global v
    text=''
    v=-1
    Parameter=0
    w.append(['NONTOKEN',"NONTOKEN",0.0,'None'])
    try:
        enter('Parser')
        FetchToken(w)#获取第一个记号
        Program(w)#递归下降分析
        back('Parser')
        return text
    except:
        return text

def Program(w):
    global v
    enter('Program')
    while w[v][0]!='NONTOKEN':
        Statement(w);
        MatchToken(w,'SEMICO')
    back('Program')

def Statement(w):
    global v
    enter('Statement')
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
    back('Statement')

def OriginStatement(w):
    enter("OriginStatement");
    MatchToken (w,'ORIGIN');
    call_match("ORIGIN")
    MatchToken (w,'IS')
    call_match("IS")
    MatchToken (w,'L_BRACKET')
    call_match("L_BRACKET")
    tmp = Expression(w);

    MatchToken (w,'COMMA')
    call_match("COMMA")
    tmp = Expression(w);

    MatchToken (w,'R_BRACKET')
    call_match("R_BRACKET")
    back("OriginStatement");

def ScaleStatement(w):
    enter("ScaleStatement");
    MatchToken (w,'SCALE')
    call_match("SCALE")
    MatchToken (w,'IS');
    call_match("IS")
    MatchToken (w,'L_BRACKET')
    call_match("L_BRACKER")
    tmp = Expression(w);
	
    MatchToken (w,'COMMA');
    call_match("COMMA")
    tmp = Expression(w);
	
    MatchToken (w,'R_BRACKET');
    call_match("R_BRACKET")
    back("ScaleStatement");

def ROTStatement(w):
    enter("RotStatement");
    MatchToken (w,'ROT')
    call_match("ROT")
    MatchToken (w,'IS');
    call_match("IS")
    tmp = Expression(w);

    back("RotStatement");

def FORStaement(w):
    enter("ForStatement");
    MatchToken (w,'FOR');
    call_match("FOR");
    
    MatchToken(w,'T');
    call_match("T");
    
    MatchToken (w,'FROM');
    call_match("FROM");
    
    start_ptr = Expression(w);	# 构造参数起始表达式语法树
    
    MatchToken (w,'TO')
    call_match("TO")
    
    end_ptr = Expression(w);	#构造参数终结表达式语法树
    
    MatchToken (w,'STEP')
    call_match("STEP")
    
    step_ptr = Expression(w);	# 构造参数步长表达式语法树
    
    MatchToken (w,'DRAW');
    call_match("DRAW");
    
    MatchToken (w,'L_BRACKET');
    call_match("(");
    
    x_ptr = Expression(w);	 # 构造横坐标表达式语法树
    
    MatchToken (w,'COMMA');
    call_match(",");
    
    y_ptr = Expression(w); 	#构造纵坐标表达式语法树
    
    MatchToken (w,'R_BRACKET');
    call_match(")");
    back("ForStatement");

def Expression(w):#表达式的递归子程序
    global v
    global haha
    enter("Expression")
    left = Term(w)#分析左操作数且得到其语法树
    while (w[v][0]=='PLUS'or w[v][0]=='MINUS'):
        token_tmp=w[v][0]
        MatchToken(w,token_tmp)
        right=Term(w)#分析右操作数且得到其语法树
        left = MakeExprNode(token_tmp, left, right)
	    # 构造运算的语法树，结果为左子树
    if haha==1:
        Tree_trace(left)	#打印表达式的语法树
    back("Expression")
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
    global haha
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
        haha=0
        tmp=Expression(w)
        haha=1
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

