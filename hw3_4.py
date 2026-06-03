#! /usr/bin/python3
# hw3_1.pyの変更点を引き継ぎしました。

def read_number(line, index): # 入力の数字の部分を読む
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.': # while文を抜けて小数点が見つかったら
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit(): # 小数点以下の数字の個数を考えて、decimalで各桁を調整
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index): # 足し算のtokenを作成
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index): # 引き算のtokenを作成
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiply(line,index): # 掛け算のtokenを作成
    token = {'type':'MULTIPLY'}
    return token, index+  1
    
def read_devide(line,index): # 割り算のtokenを作成
    token = {'type':'DEVIDE'}
    return token, index + 1

def read_abs(line,index):
    token = {'type':'ABS'}
    return token,index + 3

def read_int(line,index):
    token = {'type':'INT'}
    return token,index + 3

def read_round(line,index):
    token = {'type':'ROUND'}
    return token,index + 5


def tokenize(line): # 入力された(括弧のない)字句列から各字句のtokenを作成、非対応の構文の時にはエラーを出す。
    tokens = [] # i番目にi番目の字句のステータスが入る（但し数字は一つの数字で一つの字句）
    index = 0 # ここで初めてindexの定義
    #print(line)
    if line == '':
        return False
    if line[0] == '*' or line[0] == '/':
        #print(line[0])
        print(f"The initial token unavailable : {line}")
        return False #exit(1)
    #print(line[0])
    #print(line)
    while index < len(line):
        if line[index].isdigit(): # 数字だったら
            (token, index) = read_number(line, index)
        elif line[index] == '+': # '+'だったら
            (token, index) = read_plus(line, index)
        elif line[index] == '-': # '-'だったら
            (token, index) = read_minus(line, index)
        elif line[index] == '*': # '*'だったら
            (token,index) = read_multiply(line,index)   
        elif line[index] == '/': # '/'だったら
            (token, index) = read_devide(line,index)
        elif index <= len(line)-3 and line[index:index+3] == 'abs':
            (token,index) = read_abs(line,index)
        elif index <= len(line)-3 and line[index:index+3] == 'int':
            (token,index) = read_int(line,index)
        elif index <= len(line)-5 and line[index:index+5] == 'round':
            (token,index) = read_round(line,index)                       
        else: # その他だったら
            print('Invalid character found: ' + line[index])
            return False #exit(1)
        tokens.append(token)
    #print(f"tokens : {tokens}")    
    return tokens

    
        
def make_new_tokens_without_multiply_and_devide(tokens): # 掛け算や割り算の演算を施したnew_tokensを返す
    new_tokens = [{'type':'PLUS'}] # Insert a dummy '+' token、一番最初の要素にPLUSを入れて置き、一番最初の数字だけ特別扱いをしなくてよくしている。
    index = 0
    #print(tokens)
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if index == len(tokens)-1: # 最後のtokenを指しているとき
                new_tokens.append(tokens[index])
                index += 1
 
            elif tokens[index+1]['type'] == 'PLUS' or tokens[index+1]['type'] == 'MINUS': # 一個後ろが+か-の時
                new_tokens.append(tokens[index])
                index += 1
                
            elif tokens[index+1]['type'] == 'MULTIPLY' or tokens[index+1]['type'] == 'DEVIDE': # 一個後ろが*か/の時
                tmp_list = [tokens[index]] # 掛け算や割り算のみから成る式の部分のtokenを抽出してリストにする
                tmp = index+1 # tmp_listに入れるtokenのtokensの中でのindexを示す
                while tmp < len(tokens) and tokens[tmp]['type'] != 'PLUS' and tokens[tmp]['type'] != 'MINUS':
                    if tokens[tmp]['type'] == 'NUMBER' or tokens[tmp]['type'] == 'MULTIPLY' or tokens[tmp]['type'] == 'DEVIDE':
                        tmp_list.append(tokens[tmp])
                        tmp += 1
                new_tokens.append(evaluate_multiply_and_devide(tmp_list)) # 割り算掛け算のみの部分を計算してnew_tokensに追加
                index = tmp
                
        elif tokens[index]['type'] == 'PLUS' or tokens[index]['type'] == 'MINUS':
            new_tokens.append(tokens[index])
            index += 1
        
        else:
            #print(f"tokens:{tokens}")
            print('Invalid syntax3')
            return False #exit(1)       
    #print(f"new_tokens : {new_tokens}")         
    return new_tokens                          
                    
                    
                    
def evaluate_multiply_and_devide(num_dev_mul_tokens): # 数字と掛け算と割り算の演算のみを含んだtokensを受け取り、その答えをtokenとして返す                   
        answer = 1
        num_dev_mul_tokens.insert(0, {'type': 'MULTIPLY'})# Insert a dummy '+' token、一番最初の要素にMULTIPLYを入れて置き、一番最初の数字だけ特別扱いをしなくてよくしている。
        index = 1
        while index < len(num_dev_mul_tokens):
            if num_dev_mul_tokens[index]['type'] == 'NUMBER':
                if num_dev_mul_tokens[index-1]['type'] == 'MULTIPLY':
                    answer *= num_dev_mul_tokens[index]['number']
                    
                elif num_dev_mul_tokens[index-1]['type'] == 'DEVIDE':
                    answer /= num_dev_mul_tokens[index]['number']
            index += 1        
        return {'type': 'NUMBER','number':answer}            

def evaluate(new_tokens): # 入力された字句の情報が入ったリストtokensから式を計算
    answer = 0
    #tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token、一番最初の要素にPLUSを入れて置き、一番最初の数字だけ特別扱いをしなくてよくしている。
    index = 1
    while index < len(new_tokens):
        if new_tokens[index]['type'] == 'NUMBER': 
            if new_tokens[index - 1]['type'] == 'PLUS':
                answer += new_tokens[index]['number']
            elif new_tokens[index - 1]['type'] == 'MINUS':
                answer -= new_tokens[index]['number']
            else:
                #print(new_tokens)
                print('Invalid syntax4')
                return False #exit(1)
        index += 1
    return answer


def parentheses_match_check(line): # ()括弧が閉じられているかのエラーチェック
    if line.count(')') != line.count('('):
        print("Parentheses do not match")
        return False #exit(1)
    return True

def is_parentheses(line): # lineの中に括弧が入っているかをboolで返す。
    if '(' and ')' in line:
        return True
    else:
        return False

def remake_line(tmp_ans,line,left,right):# lineの中のleft番未満の文字列 + tmp_ans + lineの中のright+1番以上の文字列を返す
        #print(remade_line)
    return line[:left] + str(tmp_ans) + line[right+1:]
  
def make_new_tokens_without_funcs(tokens): # abs,int,roundなどの関数を計算し消したtokensを作る
    new_tokens = []
    i = 0
    if tokens == []:
        print("Invalid syntax5")
        return False #exit(1)
    while i < (len(tokens)):
        if tokens[i]['type'] == 'ABS' and i != len(tokens)-1 and tokens[i+1]['type'] == 'NUMBER':
            new_tokens.append({'type':'NUMBER','number':abs(tokens[i+1]['number'])})
            i += 2
            
        elif tokens[i]['type'] == 'ROUND' and i != len(tokens)-1 and tokens[i+1]['type'] == 'NUMBER':
            new_tokens.append({'type':'NUMBER','number':round(tokens[i+1]['number'])})
            i += 2
        
        elif tokens[i]['type'] == 'INT' and i != len(tokens)-1 and tokens[i+1]['type'] == 'NUMBER':
            new_tokens.append({'type':'NUMBER','number':int(tokens[i+1]['number'])})  
            i += 2
        else:
            new_tokens.append(tokens[i])
            i += 1    
            
    return new_tokens        
              
                   
            
def return_answer(line): # 与えられたlineから答えを返す
    if not parentheses_match_check(line) :
        return False
    if is_parentheses(line): # 与えられた式に括弧が入っているか
        #print("ans")
        ret = return_new_line_without_parentheses_and_indexes(line) # lineの（）の中の字句列、左括弧のindex、右括弧のindexが返る
        #print(ret[0])
        if ret == False:
            return False
        tmp_ans = return_answer(ret[0])# 括弧内の計算結果が返ってくる
        #print(tmp_ans)
        if tmp_ans == False:
            return False
        remade_line = remake_line(tmp_ans,line,ret[1],ret[2]) # 括弧部分をその括弧内の計算結果に変えたlineを返す
        #print(remade_line)
        return return_answer(remade_line)
              
    tokens = tokenize(line)
    if tokens == False:
        return False
    new_tokens_without_funcs = make_new_tokens_without_funcs(tokens)
    #print(new_tokens_without_funcs)
    new_tokens_without_multiply_and_devide = make_new_tokens_without_multiply_and_devide(new_tokens_without_funcs)
    if new_tokens_without_multiply_and_devide == False:
        return False
    #print(f"new_tokens_without_multiply_and_devide:{new_tokens_without_multiply_and_devide}")
    return evaluate(new_tokens_without_multiply_and_devide)



def return_new_line_without_parentheses_and_indexes(line):# 与えられたlineの（）の中の字句列、左括弧のindex、右括弧のindexを返す
    """
    # これだと括弧の対応がなっていない
    left = 0
    right = len(line)-1
    
    while line[left] != '(':
        left += 1
    while line[right] != ')':
        right -= 1
    
    if right - left <= 0:
        print("Invalid Syntax6")
        exit(1)
        """
    stack = []    
    for i,ch in enumerate(line):
        if ch == '(':
            stack.append(i)
        elif ch == ')':
            if stack == []:
                print("Parentheses don't match")
                return False #exit(1)     
            else:
                left = stack.pop()
                right = i
                return line[left+1:right] ,left, right  
    #print("Parentheses not found")
    #exit(1)            


def main(line): # line答えを返す
    return return_answer(line)
    
    
def test(line): # 引数の通りの計算を実行テスト
    actual_answer = return_answer(line) #evaluate(make_new_tokens_without_multiply_and_devide(tokens))
    #tokens = tokenize(line)
    if actual_answer == False:
        return False
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test(): # テスト実行表示
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1+2+3+4")
    test("10-2-3")
    test("2*3*4")
    test("100/2/5")
    test("1+2*3-4")
    test("10/2+3*4")
    test("2*3+4*5")
    test("100/10-2*3")
    test("0+0")
    test("0*100")
    test("100+0")
    test("0.0+1.5")
    test("1")
    test("123456789")
    test("99999999+1")
    test("1.23456789+9.87654321")
    test("1")
    test("123")
    test("1+2")
    test("5-3")
    test("4*7")
    test("20/5")
    test("2+3*4")
    test("10-2*3")
    test("8/2+5")
    test("18/3*2")
    test("(2+3)*4")
    test("(2+3)*4")
    test("10/(2+3)")
    test("(8-5)*7")
    test("100/(4*5)")
    test("((3+4)*7)")
    test("(2*(3+4))")
    test("(10-(2+3))")
    test("(8/(2+2))")
    test("((1+2)*(3+4))")
    test("((1+2)*(3+4))")
    test("(2+(3*(4+5)))")
    test("(((1+1)+1)+1)")
    test("((2+3)*(4+(5*6)))")
    test("((((((((1+2))))))))")
    test("(((((2+3)*(4+5)))))")
    
    
    test("abs(int(round(1.55)+abs(int(2.3+4))))")
    test("round(abs(int(3.7+round(1.2))))")
    test("int(abs(round(3.5)+round(2.5)))")
    test("abs(int(round(abs(int(5.9)))))")
    test("1+abs(2)*3")
    test("int(8.9)/2")
    test("abs(78)+9*4+round(3.45)*int(3.33)")
    test("round(1.4)+round(1.6)")
    test("abs(3)+int(4.9)*round(2.2)")
    test("+1")
    test("1/3*3") # stringで途中で持つと0.9999....になってしまう（情報が落ちる）
    test("*2")
    test("/3")
    test("1++2")
    test("abs()")
    test("int()")
    test("round()")
    test("(1+2")
    test("1+2)")
    test("abc")
    print("==== Test finished! ====\n")

    
run_test()
while True:
    print('>> ', end="")
    line = input().replace(' ','')        
    ans = main(line)
    if ans == False:
        continue
    else:
        print(ans)
        

    