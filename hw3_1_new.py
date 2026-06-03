#! /usr/bin/python3
# evaluate()の中にevaluate_plus_minusを入れ、evaluateの中で掛け算割り算もやるようにした。
# make_new_tokens_without_multiply_and_devide()の中の余計なif文などを10行ほど減らした。
# エラー処理をexit(1)ではなく、次の入力に移るように変更

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
    return token, index+1
    
def read_devide(line,index): # 割り算のtokenを作成
    token = {'type':'DEVIDE'}
    return token, index+1

def tokenize(line): # 入力された字句列から各字句のtokenを作成
    tokens = [] # i番目にi番目の字句のステータスが入る（但し数字は一つの数字で一つの字句）
    index = 0 # ここで初めてindexの定義
    if line == '':
        return False
    if line[0] == '*' or line[0] == '/':
        print(line[0])
        print("The initial token unavailable.")
        return False #exit(1)
    while index < len(line):
        if line[index].isdigit(): # 数字だったら
            (token, index) = read_number(line, index)
        elif index > 0 and tokens[-1]['type'] != 'NUMBER':
            print("This syntax is not available")
            return False #exit(1)            
        elif line[index] == '+': # '+'だったら
            (token, index) = read_plus(line, index)
        elif line[index] == '-': # '-'だったら
            (token, index) = read_minus(line, index)
        elif line[index] == '*': # '*'だったら
            (token,index) = read_multiply(line,index)   
        elif line[index] == '/': # '/'だったら
            (token, index) = read_devide(line,index)     
        else: # その他だったら
            print('Invalid character found: ' + line[index])
            return False #exit(1)
        tokens.append(token)
    #print(f"tokens : {tokens}")    
    return tokens

# evaluate_multiply_and_devide()
def make_new_tokens_without_multiply_and_devide(tokens): # 掛け算や割り算の演算を施したnew_tokensを返す
    new_tokens = [{'type':'PLUS'}] # Insert a dummy '+' token、一番最初の要素にPLUSを入れて置き、一番最初の数字だけ特別扱いをしなくてよくしている。
    index = 0 # 余計な分岐を減らしたver
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if index == len(tokens)-1: # これがないと後でindex+1 をしたときにindex out of rangeになる
                new_tokens.append(tokens[index])
                index += 1
     
            elif tokens[index+1]['type'] == 'PLUS' or tokens[index+1]['type'] == 'MINUS': # 数字の次の演算子がPLUS、MINUSの時
                new_tokens.append(tokens[index])
                new_tokens.append(tokens[index+1])
                index += 2 # ここで足し算と引き算の演算子も一緒にappendして、indexも２こ進める。
                
            elif tokens[index+1]['type'] == 'MULTIPLY' or tokens[index+1]['type'] == 'DEVIDE': # 数字の次の演算子がMULTIPLY、DEVIDEの時
                tmp_list = [tokens[index]] # 掛け算、割り算の部分のtokenをリスト化
                tmp = index+1
                while tmp < len(tokens) and tokens[tmp]['type'] != 'PLUS' and tokens[tmp]['type'] != 'MINUS':
                    if tokens[tmp]['type'] == 'NUMBER' or tokens[tmp]['type'] == 'MULTIPLY' or tokens[tmp]['type'] == 'DEVIDE':
                        tmp_list.append(tokens[tmp])
                        tmp += 1                     
                index = tmp    
                new_tokens.append(evaluate_multiply_and_devide(tmp_list))
                if index != len(tokens):
                    new_tokens.append(tokens[index])
                    index += 1
                                     
        else: # 演算子はすべてindexで直接指される前にリストに入れてしまうからNUMBER以外がindexに指されることはないはず
            print('Invalid syntax3')
            return False #exit(1)                
    return new_tokens                          
                    
                    
def evaluate_multiply_and_devide(num_dev_mul_tokens): # 数字と掛け算と割り算の演算のみを含んだtokensを受け取り、その答えをtokenとして返す                   
        answer = 1
        num_dev_mul_tokens.insert(0, {'type': 'MULTIPLY'})# Insert a dummy '+' token、一番最初の要素にPLUSを入れて置き、一番最初の数字だけ特別扱いをしなくてよくしている。
        index = 1
        while index < len(num_dev_mul_tokens):
            if num_dev_mul_tokens[index]['type'] == 'NUMBER':
                if num_dev_mul_tokens[index-1]['type'] == 'MULTIPLY':
                    answer *= num_dev_mul_tokens[index]['number']
                    
                elif num_dev_mul_tokens[index-1]['type'] == 'DEVIDE':
                    answer /= num_dev_mul_tokens[index]['number']
            index += 1        
        return {'type': 'NUMBER','number':answer}            

# evaluateの中でplus,minusの関数、multiply,devideの関数を呼ぶ
def evaluate(tokens): # 入力された字句の情報が入ったリストtokensから式を計算
    new_tokens = make_new_tokens_without_multiply_and_devide(tokens)
    if new_tokens == False:
        return False
    else:
        ans = evaluate_plus_minus(new_tokens)
        if ans == False:
            return False
        else:
            return ans

def evaluate_plus_minus(new_tokens):
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
    

def test(line): # 引数の通りの計算を実行テスト
    tokens = tokenize(line)
    if tokens == False:
        return False
    actual_answer = evaluate(tokens)
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
    test("k")
    test("3***")
    test("3+*3")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('>> ', end="")
    line = input().replace(' ','')
    tokens = tokenize(line)
    if tokens == False:
        continue
    answer = evaluate(tokens)
    if answer == False:
        continue
    print("answer = %f\n" % answer)
