#encoding: utf-8
from itertools import combinations_with_replacement as cwr
from itertools import product
from tqdm.auto import tqdm
import pandas as pd
tqdm.pandas(desc="Calculating...")

def calculate(rows):
    numbers = rows["numbers"]
    symbols = rows["symbols"]
    length = len(symbols)
    formula_list = list()
    for i in range(length):
        formula_list.append(numbers[i])
        formula_list.append(symbols[i])
    formula_list.append(numbers[length])
    print(formula_list)
    formula = "".join(formula_list)
    return eval(formula)

def main():
    numbers = list()
    goal = int(input("Enter goal number: "))
    while True:
        print(f"Numbers: {numbers}")
        v = input(" Enter number to use: ")
        if v.isdigit():
            numbers.append(v)
        else:
            break
    
    print(numbers, goal)
    comb = list(cwr(numbers, len(numbers)))

    symbols = ["+", "-", "*", "/"]
    symbols_comb = list(cwr(symbols, len(numbers) - 1))
    # print(symbols_comb)

    formulalist = list(product(comb, symbols_comb))
    # print(formulalist[:5])
    formula_df = pd.DataFrame(formulalist, columns=["numbers", "symbols"])
    formula_df["result"] = formula_df.progress_apply(calculate, axis=1)
    formula_df["correct"] = formula_df["result"] == goal
    print(formula_df[formula_df["correct"]].drop_duplicates())

if __name__ == "__main__":
    main()