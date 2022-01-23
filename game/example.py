from tree import *


dt = Tree(root=True)
with open('Exam.txt') as f:
    f = f.read().split('\n')
    for i in f:
        # Add games to Tree
        dt.add_game(i.split(' '))


# Get next move from position
print(dt.get_move(['h3']))

# Get next move from Root -> return List
print(dt.get_next_move())

# Go to child node (h3)
dt.goto('h3')

# Get next move from child node (h3) -> return List
print(dt.get_next_move())

# Go to child node (e8)
dt.goto('e8')

# Get next move from child node (e8)
print(dt.get_next_move())

# Undo 1 move, from position
print('Before:', dt.get_next_move())
dt.undo()
print('Undo:', dt.get_next_move())
# --------------------------------------------
dt.undo()
print(dt.get_next_move())

# Add 1 move to parent node, Ex: Add c5 to h3 => c5 is child of h3
dt.add_move('h3', 'c5')
dt.goto('h3')
print(dt.get_next_move())
