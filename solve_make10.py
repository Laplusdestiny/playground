# encoding: utf-8
from itertools import permutations, product, combinations
from itertools import combinations_with_replacement as cwr
from tqdm.auto import tqdm
import pandas as pd
from logging import basicConfig
from logging import info, INFO
from logging import debug, DEBUG

tqdm.pandas(desc="Calculating...")
basicConfig(
    filename="solve_make10.log",
    level=INFO,
    format='%(asctime)s : %(levelname)s - %(filename)s - %(message)s'
)


def make_formula(numbers, symbols, parenthese=None) -> str:
    length = len(symbols)
    formula_list = list()

    if parenthese is None:
        for i in range(length):
            formula_list.append(numbers[i])
            formula_list.append(symbols[i])
        formula_list.append(numbers[length])
        formula = "".join(formula_list)
    else:
        parenthese_close = False
        for i in range(length):
            if parenthese[0] == i:
                formula_list.append("(")
            formula_list.append(numbers[i])
            if parenthese[1] == i:
                formula_list.append(")")
                parenthese_close = True
            formula_list.append(symbols[i])
        formula_list.append(numbers[length])
        if parenthese_close is False:
            formula_list.append(")")
        formula = "".join(formula_list)
    debug(formula)
    return formula


def parse_formula(row):
    if "parentheses" in row.index:
        return make_formula(row["numbers"], row["symbols"], row["parentheses"])
    else:
        return make_formula(row["numbers"], row["symbols"])


def calculate(rows):
    numbers = rows["numbers"]
    symbols = rows["symbols"]
    formula = make_formula(numbers, symbols)

    try:
        result = eval(formula)
        return result
    except SyntaxError:
        return None


def calculate_with_parentheses(rows):
    numbers = rows["numbers"]
    symbols = rows["symbols"]
    parenthese = rows["parentheses"]
    formula = make_formula(numbers, symbols, parenthese)

    try:
        result = eval(formula)
        return result
    except SyntaxError:
        return None


def orderd(numbers, goal):
    comb = list(permutations(numbers, len(numbers)))

    symbols = ["+", "-", "*", "/"]
    symbols_comb = list(cwr(symbols, len(numbers) - 1))

    formulalist = list(product(comb, symbols_comb))
    info(
        f"numbers: {len(comb)} | symbols: {len(symbols_comb)} | formula: {len(formulalist)}")
    formula_df = pd.DataFrame(formulalist, columns=["numbers", "symbols"])
    formula_df["formula"] = formula_df.apply(parse_formula, axis=1)
    formula_df["result"] = formula_df.progress_apply(calculate, axis=1)
    formula_df["correct"] = formula_df["result"] == goal
    formula_df.to_csv("ordered.csv", index=False)
    info(f"[Ordered] {formula_df['correct'].value_counts()}")
    return formula_df[formula_df["correct"]].reset_index(drop=True)


def unordered(numbers, goal):
    comb = list(permutations(numbers, len(numbers)))

    symbols = ["+", "-", "*", "/"]
    symbols_comb = list(cwr(symbols, len(numbers) - 1))

    parentheses = list(combinations(range(len(numbers) + 1), 2))
    # parentheses = [i for i in parentheses if i[1] - i[0] != 1]

    formulalist = list(product(comb, symbols_comb, parentheses))
    info(f"numbers: {len(comb)} | symbols: {len(symbols_comb)} | parentheses: {len(parentheses)}| formula: {len(formulalist)}")
    formula_df = pd.DataFrame(formulalist, columns=[
                              "numbers", "symbols", "parentheses"])
    formula_df["formula"] = formula_df.apply(parse_formula, axis=1)
    formula_df["result"] = formula_df.progress_apply(
        calculate_with_parentheses, axis=1)
    formula_df["correct"] = formula_df["result"] == goal
    formula_df.to_csv("unordered.csv", index=False)
    info(f"[Unordered] {formula_df['correct'].value_counts()}")
    return formula_df[formula_df["correct"]].reset_index(drop=True)


def get_numbers():
    numbers = list()
    goal = int(input("Enter goal number: "))
    while True:
        print(f"Numbers: {numbers}")
        v = input(" Enter number to use: ")
        if v.isdigit():
            numbers.append(v)
        else:
            break

    info(f"Numers: {numbers} -> Goal: {goal}")
    return numbers, goal


def main():
    numbers, goal = get_numbers()
    result = orderd(numbers, goal)

    if len(result) == 0:
        result = unordered(numbers, goal)

    print(result)


if __name__ == "__main__":
    main()
