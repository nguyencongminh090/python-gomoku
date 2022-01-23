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

    def add_game(self, lst: list):
        child = [i.__node for i in self.__child]
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
        return 'Not found' if len(lst) != 0 and lst[0] not in child else \
            self.__child[child.index(lst[0])].get_move(lst[1:]) \
            if len(lst) != 0 else child if len(child) != 0 else 'Empty'

    def tree_level(self, sta=True, level=0):
        ret = level
        for child in self.__child:
            k = child.tree_level(sta=False, level=level+1)
            if k > ret:
                ret = k
        return ret

    def goto(self, move=''):
        self.__past.append(self.__cur)
        child = [i.__node for i in self.__cur]        
        self.__cur = self.__cur[child.index(move)].__child

    def add_move(self, node='', move=''):
        if not node:
            self.__child.append(Tree(move))
            return
        child = [i.__node for i in self.__cur]
        self.__cur[child.index(node)].__child.append(Tree(move))
        return
        
    def get_next_move(self):   
        return [i.__node for i  in self.__cur]
        
    def undo(self):
        try:
            self.__cur = self.__past.pop()
        except:
            print('Empty')
            return 'Empty'

    def reset_curpos(self):
        self.__cur = self.__child
        self.__past = []
        
    def total_nodes(self):
        if self.__root:
            n = 0
        else:
            n = 1 
        for child in self.__child:
            n += child.total_nodes()
        return n
        
    def __str__(self, level=-1):
        k = "    "*level+str(self.__node)+"\n"
        for child in self.__child:
            k += child.__str__(level+1)
        return k

    def __repr__(self):
        return f'{self.__node.upper()}'



