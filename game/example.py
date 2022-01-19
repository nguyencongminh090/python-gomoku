from tree import *


dt = Tree(root=True)
with open('Exam.txt') as f:
    f = f.read().split('\n')
    for i in f:
        dt.add(i.split(' '))


print(dt.get_move(['h3']))
print(dt.get_next_move())
print(dt.get_next_move('h3'))
print(dt.get_next_move('e8'))
dt.undo()
print(dt.get_next_move())
