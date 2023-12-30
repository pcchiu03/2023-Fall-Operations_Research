# Created time: 2023_12_02
# Created by: Chiu Pao Chang
# Shift code: A：0、M1：1、C1：2、H：3、G：4、C2：5、N：6、M3：7、I：8

import gurobipy as gp
from gurobipy import GRB
import numpy as np

# Create a new model
model = gp.Model("team10_1")

# Set parameters
D = 7 # 排班天數
B = 9 # 班別類型數量
N = 7 # 排班人員數
# 每天值班人員
Y = np.array([[1, 0, 0, 0, 0, 0, 0],  # Mon.
              [0, 0, 1, 0, 0, 0, 0],  # Tue.
              [0, 0, 0, 0, 0, 1, 0],  # Wed.
              [0, 0, 1, 0, 0, 0, 0],  # Thr.
              [0, 0, 0, 0, 0, 0, 0],  # Fri.
              [0, 0, 0, 0, 0, 0, 0],  # Sat.
              [0, 0, 0, 1, 0, 0, 0]]) # Sun.
# 週六上 I 班人員
I = np.array([[0, 0, 0, 0, 0, 0, 0],  # Mon.
              [0, 0, 0, 0, 0, 0, 0],  # Tue.
              [0, 0, 0, 0, 0, 0, 0],  # Wed.
              [0, 0, 0, 0, 0, 0, 0],  # Thr.
              [0, 0, 0, 0, 0, 0, 0],  # Fri.
              [0, 0, 0, 1, 0, 0, 1],  # Sat.
              [0, 0, 0, 0, 0, 0, 0]]) # Sun.

# Create decision varibles
w = model.addVars(D, B, N, vtype=GRB.BINARY, name='w') 
r = model.addVars(D, N, vtype=GRB.BINARY, name='r')

# Set objective function
model.setObjective(gp.quicksum(w[d, b, n] for d in range(D) for b in range(B) for n in range(N)), GRB.MINIMIZE)

# Add constraints
# 週六：值班或休息
for d in range(D):
    if d == 5:
        for n in range(N):
            model.addConstr(I[d, n] + r[d, n] == 1, 'c1_%d_%d'%(d, n))

# 週六：上 I 班
for d in range(D):
    if d == 5:
        for n in range(N):
            model.addConstr(w[d, 8, n] == I[d, n], 'c2_%d_%d'%(d, n))

# 週六：I 班以外的班別都為零
for d in range(D):
    if d == 5:
        for b in range(B):
            if b  not in [8]:
                for n in range(N):
                    model.addConstr(w[d, b, n]== 0, 'c3_%d_%d_%d'%(d, b, n))

# 週日：休息   
for d in range(D):
    if d == 6:
        for n in range(N):
                model.addConstr(r[d, n] == 1, 'c4_%d_%d'%(d, n))

# 週日：休息   
for d in range(D):
    if d == 6:
        for b in range(B):
            for n in range(N):
                model.addConstr(w[d, b, n] == 0, 'c5_%d_%d_%d'%(d, b, n))

# 週一至週五：每天上班或休息
for d in range(D):
    if d not in [5, 6]:
        for b in range(B):
            if b not in [2, 5, 8]:
                model.addConstr(gp.quicksum(w[d, b, n] for n in range(N)) == 1, 'c6_%d_%d'%(d, b))

# 週一至週五：沒有人上 I 班
for d in range(D):
    if d not in [5, 6]:
        for b in range(B):
            if b in [8]:
                model.addConstr(gp.quicksum(w[d, b, n] for n in range(N)) == 0, 'c7_%d_%d'%(d, b))

# 週一至週五：每天一人休息
for d in range(D):
    if d not in [5, 6]:
        model.addConstr(gp.quicksum(r[d, n] for n in range(N)) == 1, 'c8_%d'%d)

# 週一至週五：每天上班或休假
for n in range(N):
    for d in range(D):
        if d not in [5, 6]:
            model.addConstr(gp.quicksum(w[d, b, n] for b in range(B) if b not in [2, 5, 8]) + r[d, n] == 1, 'c9_%d_%d'%(n, d))

# 週一至週四：值班隔天上 N 班
for d in range(D):
    if d not in [4, 5, 6]:
        for n in range(N):
            model.addConstr(w[d + 1, 6, n] == Y[d, n], 'c10_%d_%d'%(d, n))
# 先不算週日狀況（第二週週一的值班），因為陣列會 out of range
'''
# 週日：值班隔天上 N 班
for d in range(D):
    if d in [6]:
        for n in range(N):
            model.addConstr(w[d + 1, 6, n] == Y[d, n], 'c _%d_%d'%(d, n))
'''

# 週一至週五：人員 7 只上 M3 班
for d in range(D):
    if d not in [5, 6]:
        for n in range(N):
            if n == 6:
                model.addConstr(w[d, 7, n] + r[d, n] == 1, 'c11_%d_%d'%(d, n))

# 週一至週五：人員 2 休假
for d in range(D):
    if d not in [5, 6]:
        for n in range(N):
            if n == 1:
                model.addConstr(r[d, n] == 1, 'c12_%d_%d'%(d, n))

# 週一：人員 5 上 N 班
model.addConstr(w[0, 6, 4]== 1, 'c13')

# 週一至週五：判斷各自的班別、上 N 班、休假的狀況
for d in range(D):
    if d not in [5, 6]:
        # 人員 1
        model.addConstr(w[d, 0, 0] + w[d, 6, 0] + r[d, 0] == 1, 'c14_%d'%d)
        # 人員 2
        model.addConstr(w[d, 1, 1] + w[d, 6, 1] + r[d, 1] == 1, 'c15_%d'%d)
        # 人員 3
        #model.addConstr(w[d, 2, 2] + w[d, 6, 2] + r[d, 2] == 1, 'c _%d'%d)
        # 人員 4
        model.addConstr(w[d, 3, 3] + w[d, 6, 3] + r[d, 3] == 1, 'c16_%d'%d) 
        # 人員 5
        model.addConstr(w[d, 4, 4] + w[d, 6, 4] + r[d, 4] == 1, 'c17_%d'%d) 
        # 人員 6
        #model.addConstr(w[d, 5, 5] + w[d, 6, 5] + r[d, 5] == 1, 'c _%d'%d) 
        
# 週一至週三、週五：人員 6 上 C2 班的狀況（代替當天上 N 班該人的班別）
model.addConstr(w[0, 6, 4] == w[0, 4, 5], 'c18')
model.addConstr(w[1, 6, 0] == w[1, 0, 5], 'c19') 
model.addConstr(w[2, 6, 2] == w[2, 1, 5], 'c20') 
model.addConstr(w[4, 6, 2] == w[4, 1, 5], 'c21') 


# Update the model
model.update()

# Optimize the model
model.optimize()

# Create .lp file
model.write("team10_1.lp")

# Print the solution
if model.status == GRB.OPTIMAL:
    print("Optimal solution found!")
    print("Number of variables: ", model.numVars)
    print("Number of constraints: ", model.numConstrs)
    print("Objective value: ", model.objVal)
    for v in model.getVars():
        print("%s = %.4f"%(v.varName, v.x))
else:
    print("No solution found.")



print("\n\n")
# 印出班表的數值設定
On_Duty = model.getAttr("x", w)
Day_Off = model.getAttr("x", r)
days_of_week = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]
shift_names = ["A", "M1", "C1", "H", "G", "C2", "N", "M3", "I"]

# 印出星期的欄位
for day in days_of_week:
    print(day.ljust(8), end=" ")
print("\n")

# 印出班表
for n in range(N):
    for d in range(D):
        for b in range(B):
            for i, shift_name in enumerate(shift_names):
                if b == i and On_Duty[d, b, n] == 1:
                    print(shift_name.ljust(8), end=" ")
        if Day_Off[d, n] == 1:
            print("X".ljust(8), end=" ")
    print("\n")
