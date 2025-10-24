import numpy as np

def retrieve_problem():
    num_vars = int(input("Enter number of variables: "))
    num_const = int(input("Enter number of constraints: "))

    tableau_rows = num_const + 1
    tableau_cols = num_vars + num_const + 2
    tableau = np.zeros((tableau_rows, tableau_cols))

    for i in range(num_vars):
        tableau[-1][i] = -1 * float(input(f"Enter objective function x{i} co-efficient: "))
    tableau[-1][tableau_cols - 2] = 1
    
    for i in range(num_const):
        print(f"-----CONSTRAINT {i+1}------")
        for x in range(num_vars):
            tableau[i][x] = float(input(f"x{x} coefficient: "))

        tableau[i][x + i + 1] = 1
        tableau[i][-1] = float(input("<= "))
    
    return tableau, num_vars, num_const

def display_tableau(tableau):
    print(tableau)

def find_pivot(tableau):
    i_pivot_col = np.argmin(tableau[-1])
    pivot_col = tableau[:, i_pivot_col]

    dup_last_col = tableau[:, -1]
    pivot_row = float('inf')

    for i in range(len(dup_last_col)):
        if dup_last_col[i] < 0 or pivot_col[i] < 0:
            continue
        elif pivot_col[i] != 0:
            if dup_last_col[i] / pivot_col[i] < pivot_row:
                i_pivot_row = i
                pivot_row = dup_last_col[i] / pivot_col[i]

    print(f"Pivot value: {tableau[i_pivot_row][i_pivot_col]}")

    return i_pivot_row, i_pivot_col

def elem_row_oper(tableau, pivot_row, pivot_col):
    if tableau[pivot_row][pivot_col] != 1:
        tableau[pivot_row, :] = tableau[pivot_row, :] / tableau[pivot_row][pivot_col]

    for i in range(len(tableau)):
        if i == pivot_row:
            continue
        elif tableau[i][pivot_col] != 0:
            const = (-1 * tableau[i][pivot_col]) / tableau[pivot_row][pivot_col]
            tableau[i, :] = tableau[i, :] + (const * tableau[pivot_row, :])
    
    return tableau


def simplex_method():
    tableau, num_vars, _ = retrieve_problem()
    print("\n---- STD FORM ----")
    display_tableau(tableau)

    iter = 0
    old_tableaus = []
    old_tableaus.append(tableau.copy())

    while np.min(tableau[-1, :]) < 0:
        iter += 1
        pivot_row, pivot_col = find_pivot(tableau)
        tableau = elem_row_oper(tableau, pivot_row, pivot_col)
        print(f"\n--------- ITER {iter} ----------")
        display_tableau(tableau)
        if np.all(np.isin(tableau, old_tableaus)):
            print("REPEATING TABLEAUS! INFINITE LOOP")
            break
        else:
            old_tableaus.append(tableau.copy())

    print(f"Maximum value: {tableau[-1][-1]}")
    for i in range(num_vars):
        if tableau[-1][i] == 0:
            x_val_row = np.argmax(tableau[:, i])
            print(f"x{i} = {tableau[x_val_row][-1]}")
        else:
            print(f"x{i} = 0.0")
    

simplex_method()