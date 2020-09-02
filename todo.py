#!/bin/python3
import sys
from shutil import copyfile

course = sys.argv[2]

BASE = "/home/carter/sft/todo/"

if sys.argv[1] == "new":
    name = sys.argv[3]
    date = sys.argv[4]
    with open(BASE + 'todo.rec', 'r') as rec:
        reclines = rec.readlines()
    
    num = 0
    for line in reclines:
        fields = line.strip().split(',')
        if len(fields) > 1 and fields[1] == course:
            num += 1

    reclines += [f"0,{course},{name},{date},{num}\n"]

    with open(BASE + 'todo.rec', 'w') as rec:
        rec.writelines(reclines)

if sys.argv[1] == "done":
    num = int(sys.argv[3])

    with open(BASE + 'todo.rec', 'r') as rec:
        reclines = rec.readlines()
    
    for i, line in enumerate(reclines):
        fields = line.strip().split(',')
        if fields[4] == str(num) and fields[1] == course:
            fields[0]="1"
        reclines[i] = ','.join(fields) + "\n"

    with open(BASE + 'todo.rec', 'w') as rec:
        rec.writelines(reclines)

#template make

copyfile(BASE + 'temp.html', BASE + 'todo.html')

with open(BASE + 'todo.html', 'r') as todo:
    todocont = todo.read()
    
with open(BASE + 'todo.rec', 'r') as rec:
    reclines = rec.readlines()


# reclines += [f"0,{course},{name},{date},{num}\n"]
nums = [0,0,0,0,0]
for line in reclines:
    fields = line.strip().split(',')
    todomarker = f"<!--todo {fields[1]}-->\n"
    donemarker = f"<!--done {fields[1]}-->\n"
    task = f"<div class=\"task\"><span class=\"num\">{fields[4]}</span>{fields[2]}<br><i>{fields[3]}</i></div>\n"
    space = " " * 16
    task += space
    if fields[0] == "0":
        nums[int(fields[1])] += 1
        todocont = todocont.replace(todomarker, todomarker+task)

    if fields[0] == "1":
        todocont = todocont.replace(donemarker, donemarker+task)

for i, n in enumerate(nums):
    todomarker = f"<!--todo {i}-->\n"
    blank = f"<div class=\"task\"><span class=\"num\" style=\"float:none;\">All Done!</span></div>\n"
    if n == 0:
        todocont = todocont.replace(todomarker, todomarker+blank)
   
with open(BASE + 'todo.html', 'w') as todo:
    todo.write( todocont )
