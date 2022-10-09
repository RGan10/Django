import time
from collections import OrderedDict
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'SudokuFormat.html')

def is_valid(sudoku, a, b):
    if sudoku[a][b] == 0:
        return True
    # 3x3 check
    c = 3 * (a // 3)
    d = 3 * (b // 3)
    for i in range(c, c + 3):
        for j in range(d, d + 3):
            if sudoku[a][b] == sudoku[i][j] and a != i and b != j:
                return False
    # horizontal check
    for i in range(0, 9):
        if sudoku[a][i] == sudoku[a][b]:
            if b == i:
                continue
            return False
    # verical check
    for i in range(0, 9):
        if sudoku[i][b] == sudoku[a][b]:
            if a == i:
                continue
            return False
    return True


def find_min_acceptable(zsudoku):
    final_list = []
    for i in range(0,9):
        list = []
        for j in range(0,9):
            no_of_valid = 0
            if zsudoku[i][j]!=0:
                no_of_valid= 10
                list.append(no_of_valid)
                continue
            for k in range(1,10):
                zsudoku[i][j] = k
                if is_valid(zsudoku,i,j):
                    no_of_valid+=1
                zsudoku[i][j] = 0
            list.append(no_of_valid)
        final_list.append(list)
    list = []
    for i in range(0,9):
        list.append(min(final_list[i]))
    z = min(list)
    if z == 10:
        return False
    n = list.index(z)
    m = final_list[n].index(min(final_list[n]))
    return n,m


def compute(request, sudoku, a, b):
    zzz = find_min_acceptable(sudoku)
    global glob_sudoku
    glob_sudoku = 1
    if (not zzz):
        glob_sudoku = sudoku
        return 5
    else:
        (a, b) = zzz
    for i in range(1, 10):
        sudoku[a][b] = i
        if is_valid(sudoku, a, b):
            if compute(request, sudoku, a, b) == 5:
                return 5
    sudoku[a][b]= 0

def solved(request):
    sudoku_dict = (request.GET.dict())
    sorted_dict = OrderedDict(sorted(sudoku_dict.items()))
    sudoku_list = list(dict.values(sorted_dict))
    n = 0
    sudoku= [[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]
    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku_list[n] == '':
                sudoku[i][j] = 0
            else:
                sudoku[i][j] = int(sudoku_list[n])
            n += 1
    for i in range(0, 9):
        for j in range(0, 9):
            if not is_valid(sudoku, i, j):
                return HttpResponse("Invalid Sudoku")
    compute(request,sudoku, 0, 0)
    if glob_sudoku == 1:
        return HttpResponse("Invalid Sudoku 2")
    sudoku_list = []
    key = []
    for i in range(0, 9):
        for j in range(0, 9):
            sudoku_list.append('a'+str(i)+str(j))
            sudoku_list.append(str(glob_sudoku[i][j]))
    init = iter(sudoku_list)
    sudoku_dict = dict(zip(init, init))
    return render(request, 'solved.html', sudoku_dict)
    exit()