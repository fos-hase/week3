# This file is used to evaluate the correctness of your code.
# You cannot modify or delete this file. If you do, we cannot evaluate your code correctly.
# このファイルはあなたのコードの自動評価用です。
# このファイルを変更したり、削除したりしてははいけません。もし変更した場合、あなたのコードを正しく評価できません。

# Even you can modify this file, you cannot cheat. We will evaluate your code with different test cases.
# このファイルを変更して不正に得点を得ることはできません。本番採点は別途行います。

import subprocess
from pathlib import Path
import json
import ctypes
import subprocess
from typing import List, Any
import sys
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from math import sqrt

def compile_c_code(file: str):
    subprocess.run(["gcc", "-shared", "-o", "libtest.so", "-fPIC", file])

def run_only_func(file: str, func: str, test_cases: List[List[Any]], arg_types: List[Any], res_type: Any):
    py_func = globals()[func]
    compile_c_code(file)
    lib = ctypes.CDLL("./libtest.so")
    c_func = getattr(lib, func)
    c_func.argtypes = arg_types
    c_func.restype = res_type

    for case in test_cases:
        c_args = []
        for arg, arg_type in zip(case, arg_types):
            if arg_type == ctypes.c_char:
                c_args.append( ctypes.c_char(arg.encode('utf-8')))
            else:
                c_args.append(arg)

        py_result = py_func(*case)
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(c_func, *c_args)
                c_result = future.result(timeout=1)
        except TimeoutError:
            print(f"> [!CAUTION]\n > {file}: Failed")
            print(f"> Time out on case {case}\n")
            return False

        if py_result == c_result:
            pass
        else:
            print(f"> [!CAUTION]\n > {file}: Failed")
            print(f"> on case {case}: Python result {py_result}, C result {c_result}\n")
            return False
    print(f"{file}: OK")
    return True

## test cases
test_cases = {"is_prime":[[2147483647]]}
arg_types = {"is_prime":[ctypes.c_int]}
res_types = {"is_prime":ctypes.c_int}

def is_prime(n):
    if n == 1:
        return 0
    sqrtn = int(sqrt(n))
    for d in range(2, sqrtn):
        if n % d == 0:
            return 0
    return 1

## 

def run_job(cmd):
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return ret.stdout.decode(('UTF-8'))

def print_codeblock(s):
    print("```")
    print(s)
    print("```")

if __name__ == "__main__":
    print("# Running test cases...")
    with open(".eval/test_case.json", "r") as f:
        cases = json.load(f)

    for case in cases:
        file = case["file"]
        func = case["func"]
        echo = case["echo"]
        ans = case["ans"]
        
        if not Path(file).exists():
            print("Error. File `{}` not found.".format(file))
            continue
        print("## Testing `{}`...".format(file))   
        run_job("rm -rf a.out")

        if func == "main":
            msg = run_job("gcc {}".format(file))
            if Path("a.out").exists():
                print("Compiled successfully.")
            else:
                print("Compile failed.")
                print_codeblock(msg)
                continue  
            if echo == "":
                msg = run_job("./a.out")
            else:
                process = subprocess.run(['./a.out'], input=echo, text=True, capture_output=True)
                msg = process.stdout
            if ans == "python":
                py_func = globals()[func]
                ans = py_func()
            if msg == ans:
                print(f"{file}: OK")
            else:
                print(f"> [!CAUTION]\n > {file}: Failed")
                print("your output:")
                print_codeblock(msg)
                print("ideal output:")
                print_codeblock(ans)
                continue
        else:
            run_only_func(file, func, test_cases[func], arg_types[func], res_types[func])
    if Path("a.out").exists():
        run_job("rm -rf a.out")

# This file is used to evaluate the correctness of your code.
# You cannot modify or delete this file. If you do, we cannot evaluate your code correctly.
# このファイルはあなたのコードの自動評価用です。
# このファイルを変更したり、削除したりしてははいけません。もし変更した場合、あなたのコードを正しく評価できません。

# Even you can modify this file, you cannot cheat. We will evaluate your code with different test cases.
# このファイルを変更して不正に得点を得ることはできません。本番採点は別途行います。