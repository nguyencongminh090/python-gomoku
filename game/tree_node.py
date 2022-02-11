class Tree:
    def __init__(self, node='', root=False):
        self.__child = []
        self.__node = node
        self.__root = root
        self.__cur = self.__child
        self.__past = []
        self.depth = ''
        self.val = ''
        self.note = ''

    @staticmethod
    def __rotate_lr(arr):
        out = []
        for i in arr.split():
            out.append(chr(96 + 15 - ord(i[0]) + 97) + i[1:])
        return ' '.join(out)

    @staticmethod
    def __rotate_ud(arr):
        out = []
        for i in arr.split():
            out.append(i[0] + str(16 - int(i[1:])))
        return ' '.join(out)

    def __rotate(self, arr):
        lst = [arr]
        for i in range(3):
            strg = []
            for j in lst[i].split(' '):
                x = chr(int(j[1:]) + 96)
                y = str(15 - (ord(j[0]) - 97))
                strg.append(x + y)
            strg = ' '.join(strg)
            if strg not in lst:
                lst.append(strg)
        for i in lst[:4]:
            lst.append(self.__rotate_lr(i))
        for i in lst[:4]:
            lst.append(self.__rotate_ud(i))
        return list(set(lst))

    def add_game(self, lst: list, rotate=False):
        child = [i.__node for i in self.__child]
        if not rotate:
            if lst[0] not in child:
                self.__child.append(Tree(lst[0]))
            self.__insert(lst)
        else:
            move = self.__rotate(' '.join(lst))
            for i in move:
                child = [i.__node for i in self.__child]
                lst = i.split()
                if lst[0] not in child:
                    self.__child.append(Tree(lst[0]))
                self.__insert(lst)

    def __insert(self, lst: list, it=1):
        if len(lst) >= 2:
            child = [i.__node for i in self.__child]
            if lst[it - 1] in child:
                return self.__child[child.index(lst[it - 1])].__insert(lst, it)
            if lst[it] not in child:
                self.__child.append(Tree(lst[it]))
            self.__insert(lst[1:])
        return

    def get_move(self, lst: list):
        child = [i.__node for i in self.__child]
        if len(lst) != 0 and lst[0] not in child:
            return 'Not found'
        elif len(lst) != 0:
            return self.__child[child.index(lst[0])].get_move(lst[1:])
        elif len(child) != 0:
            return child
        else:
            return 'Empty'

    def tree_level(self, level=0):
        ret = level
        for child in self.__child:
            k = child.tree_level(level=level + 1)
            if k > ret:
                ret = k
        return ret

    def goto(self, move=''):
        self.__past.append(self.__cur)
        child = [i.__node for i in self.__cur]
        if move not in child:
            self.__cur = False
            return
        self.__cur = self.__cur[child.index(move)].__child

    def add_move(self, node='', move=''):
        if not node:
            self.__child.append(Tree(move))
            return
        child = [i.__node for i in self.__cur]
        self.__cur[child.index(node)].__child.append(Tree(move))

    def get_next_move(self):
        if not self.__cur:
            return False
        return [i.__node for i in self.__cur]

    def undo(self):
        if self.__past:
            self.__cur = self.__past.pop()

    def reset_curpos(self):
        self.__cur = self.__child
        self.__past = []

    def __get_pos(self, lta):
        child = [i.__node for i in self.__child]
        if len(lta) != 0 and lta[0] not in child:
            return []
        elif len(lta) != 0:
            return self.__child[child.index(lta[0])].__get_pos(lta[1:])
        elif len(child) != 0:
            return self.__child
        else:
            return []

    def set_pos(self, lst):
        self.__cur = self.__get_pos(lst)

    def total_nodes(self):
        if self.__root:
            n = 0
        else:
            n = 1
        for child in self.__child:
            n += child.total_nodes()
        return n

    def load_txt(self, strg='', fn='', delimiter='\n', rotate=False):
        if fn:
            with open(fn) as f:
                data = f.read().split(delimiter)
        else:
            data = strg.split(delimiter)
        for i in data:
            if len(i.split()) > 0:
                if not rotate:
                    self.add_game(i.split())
                else:
                    self.add_game(i.split(), rotate=True)

    def print_tree(self, level=-1):
        k = "    " * level + str(self.__node) + "\n"
        for child in self.__child:
            k += child.print_tree(level + 1)
        return k

    def sml_search(self, lst: list):
        """
        Similar Position Search
        """
        stack = []
        mline = []  # main line
        b_list = lst[::2]
        w_list = lst[1::2]
        state = True  # True: Black, False: white
        if state:
            cur_list = b_list
        else:
            cur_list = w_list
        for i in cur_list:
            if i in [node.__node for node in self.__cur]:
                stack.append(i)

        while stack:
            if stack[0] not in [node.__node for node in self.__cur] or stack[0] not in cur_list:
                self.undo()
                mline.pop()
                state = not state
                if state:
                    cur_list = b_list
                else:
                    cur_list = w_list
                continue
            self.goto(stack[0])
            mline.append(stack[0])
            stack.remove(stack[0])
            state = not state
            if state:
                cur_list = b_list
            else:
                cur_list = w_list
            # Find next node
            empty = True
            for i in cur_list:
                if i in [node.__node for node in self.__cur]:
                    stack.insert(0, i)
                    empty = False

            if len(mline) == len(lst):
                return True, ' '.join(mline), [node.__node for node in self.__cur]
            if empty:
                mline.pop()
                self.undo()
                state = not state
        return False, '', []

    def tree_record(self):
        out = ''
        if not self.__root:
            k = '(' + self.__node
            out += k
        for child in self.__child:
            out += child.tree_record()
            out += ')'
        return out

    @staticmethod
    def read_rec_file(fn):
        game = []
        stack = []
        pos = 1
        s = ''
        with open(fn) as f:
            fn = f.read()
        while fn:
            if not stack and fn[pos - 1] == '(':
                s += fn[pos]
                pos += 1
                while fn[pos].isnumeric():
                    s += fn[pos]
                    pos += 1
                stack.append(s)
                s = ''
                fn = fn[pos:]
                pos = 1

            elif len(stack) == 1 and fn[pos - 1] == '(':
                s += fn[pos]
                pos += 1
                while fn[pos].isnumeric():
                    s += fn[pos]
                    pos += 1
                stack.append(s)
                s = ''
                fn = fn[pos:]
                pos = 1

            elif len(stack) > 1 and fn[pos - 1] == '(':
                s += fn[pos]
                pos += 1
                while fn[pos].isnumeric():
                    s += fn[pos]
                    pos += 1
                stack.append(s)
                s = ''
                fn = fn[pos:]
                pos = 1
                if fn[pos - 1] == ')':
                    game.append(' '.join(stack))

            elif fn[pos - 1] == ')':
                stack.pop()
                fn = fn[pos:]
        return '\n'.join(game)

    def save(self, fn):
        with open(fn, 'w+') as f:
            f.write(self.tree_record())

    def load(self, fn: str):
        stack = []
        pos = 1
        s = ''
        while fn:
            if not stack and fn[pos - 1] == '(':
                s += fn[pos]
                pos += 1
                while fn[pos].isnumeric():
                    s += fn[pos]
                    pos += 1
                self.add_move(move=s)
                stack.append(s)
                s = ''
                fn = fn[pos:]
                pos = 1

            elif len(stack) == 1 and fn[pos - 1] == '(':
                s += fn[pos]
                pos += 1
                while fn[pos].isnumeric():
                    s += fn[pos]
                    pos += 1
                self.add_move(node=stack[-1], move=s)
                stack.append(s)
                s = ''
                fn = fn[pos:]
                pos = 1

            elif len(stack) > 1 and fn[pos - 1] == '(':
                s += fn[pos]
                pos += 1
                while fn[pos].isnumeric():
                    s += fn[pos]
                    pos += 1
                self.goto(stack[-2])
                self.add_move(node=stack[-1], move=s)
                stack.append(s)
                s = ''
                fn = fn[pos:]
                pos = 1

            elif fn[pos - 1] == ')':
                stack.pop()
                self.undo()
                fn = fn[pos:]

    def print_all_move(self, line=''):
        out = ''
        k = ''
        if not self.__root:
            k = self.__node + ' '
        if not self.__child:
            out = line + self.__node + '\n'
            return out
        for child in self.__child:
            if k not in line:
                line += k
            out += child.print_all_move(line=line)
        return out

    def add_rotate(self):
        for i in self.print_all_move().split('\n'):
            if i:
                for j in self.__rotate(i):
                    if not self.sml_search(j.split())[0]:
                        self.add_game(j.split())

    def __str__(self, line='', n=1):
        out = ''
        k = ''
        if not self.__root:
            k = self.__node + ' '
        if not self.__child:
            out = str(n) + ': ' + line + self.__node + '\n'
            n += 1
            return out, n
        for child in self.__child:
            if k not in line:
                line += k
            a = child.__str__(line=line, n=n)
            out += a[0]
            n = a[1]
        if self.__root:
            return out
        return out, n

    def __repr__(self):
        return f'{self.__node.upper()}'
