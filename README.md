# STEP_Week3_HomeWork
STEP_WEEK3_HomeWork

## HomeWork1 (hw3_1.py)
### Objective:
Make a calculator which supports multiplication and division.
### Functions:
  - def tokenize (line) : Make tokens of numbers or operators from line(string input).
    - def read_numbers (line,index) : Make a token of a number. Return the token and index with 1 added.
    - def read_plus (line,index) : Make a token of plus operator. Return the token and index with 1 added.
    - def read_minus (line,index) : Make a token of minus operator. Return the token and index with 1 added.
    - def read_multiply (line,index) : Make a token of multipulation operator. Return the token and index with 1 added.
    - def read_devide (line,index) : Make a operator of division operator. Return the token and index with 1 added.
    <br>
  - def make_new_tokens_without_multiply_and_devide (tokens) : Make new 'tokens' (list of tokens) without multipulation and devision operators.
    - def evaluate_multiply_and_devide (num_dev_mul_tokens) : From num_dev_mul_tokens (list of tokens of only numbers, multipulation operators and division operators), calculate and return the answer. Add the answer to the list made in make_new_tokens_without_multiply_and_devide.  
      <br>
  - def evaluate (new_tokens) : Do addition and subtraction in new_tokens.  
    (In new_tokens, because make_new_tokens_without_multiply_and_devide is executed earlier, neither multipulation no devision operator is contained.)  
    <br>
  - def test (line) : Test the functions for line.  
   <br>  
  - def run_test() : Show the answers of the tests.  

   
## Homework3 (hw3_3.py)
### Objective:
Make a calculator which supports parentheses by expanding the code made in hw3_1.py.




## HomeWork4 (hw3_4.py)
### Objective:
Make a calculator which supports functions such as abs(), int() and round() by expanding the code in hw3_3.py.
