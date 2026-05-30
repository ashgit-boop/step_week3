#! /usr/bin/python3

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

def tokenize(line): # 入力された字句列から各字句のステータスを作成
    tokens = [] # i番目にi番目の字句のステータスが入る（但し数字は一つの数字で一つの字句）
    index = 0 # ここで初めてindexの定義
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
        else: # その他だったら
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    #print(f"tokens : {tokens}")    
    return tokens

    
def make_new_tokens_without_multiply_and_devide(tokens): # 掛け算や割り算の演算を施したnew_tokensを返す
    new_tokens = [{'type':'PLUS'}] # Insert a dummy '+' token、一番最初の要素にPLUSを入れて置き、一番最初の数字だけ特別扱いをしなくてよくしている。
    index = 0
    while index < len(tokens):
        #print(new_tokens)
        if tokens[index]['type'] == 'NUMBER':
            if index == len(tokens)-1:
                if tokens[index]['type'] == 'NUMBER':
                    new_tokens.append(tokens[index])
                    index += 1
                else:
                    print('Invalid syntax1')
                    exit(1)          
            elif tokens[index+1]['type'] == 'PLUS' or tokens[index+1]['type'] == 'MINUS':
                new_tokens.append(tokens[index])
                index += 1
                
            elif tokens[index+1]['type'] == 'MULTIPLY' or tokens[index+1]['type'] == 'DEVIDE':
                tmp_list = [tokens[index]]
                tmp = index+1
                while tmp < len(tokens) and tokens[tmp]['type'] != 'PLUS' and tokens[tmp]['type'] != 'MINUS':
                    if tokens[tmp]['type'] == 'NUMBER' or tokens[tmp]['type'] == 'MULTIPLY' or tokens[tmp]['type'] == 'DEVIDE':
                        tmp_list.append(tokens[tmp])
                        tmp += 1
                    else:
                        #print(tmp_list)
                        #print(tokens[tmp])
                        #print('Invalid syntax2')
                        exit(1) 
                new_tokens.append(evaluate_multiply_and_devide(tmp_list))
                index = tmp
                
        elif tokens[index]['type'] == 'PLUS' or tokens[index]['type'] == 'MINUS':
            new_tokens.append(tokens[index])
            index += 1
        
        else:
            print('Invalid syntax3')
            exit(1)       
    #print(f"new_tokens : {new_tokens}")         
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
                print('Invalid syntax4')
                exit(1)
        index += 1
    return answer


def test(line): # 引数の通りの計算を実行テスト
    tokens = tokenize(line)
    actual_answer = evaluate(make_new_tokens_without_multiply_and_devide(tokens))
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
    print("==== Test finished! ====\n")

run_test()

while True:
    print('>> ', end="")
    line = input().replace(' ','')
    tokens = tokenize(line)
    new_tokens = make_new_tokens_without_multiply_and_devide(tokens)
    answer = evaluate(new_tokens)
    print("answer = %f\n" % answer)
