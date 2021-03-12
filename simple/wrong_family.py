"""У Вас есть список семейных уз отцов и их сыновей.
Каждый элемент этого списка имеет еще два элемента.
Первым является имя отца, вторым - имя сына.
Все имена в этой семье являются уникальными.
Проверьте, достоверно ли семейное древо,
нет ли там посторонних и все ли связи являются естественными.

Входные данные: list of lists. Каждый элемент имеет две строки.
В списке есть как минимум один элемент.

Выходные данные: bool. Достоверно ли семейное древо.
"""
from typing import List
from collections import defaultdict


class TreeNode:
    def __init__(self, name: str):
        self.name = name
        self.children = list()
        self.parent = None

    def add_child(self, child: 'TreeNode') -> None:
        if child is self:
            raise TreeNodeException
        child.add_parent(self)
        self.children.append(child)

    def add_parent(self, parent: 'TreeNode') -> None:
        if self.parent and self.parent is not parent or parent is self:
            raise TreeNodeException
        if parent in self.__get_all_childs():
            raise TreeNodeException('Loops...')
        self.parent = parent

    def __get_all_childs(self):
        child_list = self.children
        for child in self.children:
            if child.children:
                child_list.extend(child.__get_all_childs())
        return child_list

    def get_all_childs(self):
        print('Get all children for', self.name)
        for x in self.__get_all_childs():
            print(x.name)

    def get_root(self):
        cur_parent = self
        while cur_parent:
            if not cur_parent.parent:
                break
            cur_parent = cur_parent.parent
        return cur_parent

    def get_all_names(self):
        root = self.get_root()
        return {x.name for x in root.__get_all_childs()} | {root.name}


class TreeNodeException(Exception):
    pass


def is_family(tree: List[List[str]]) -> bool:
    # build dict
    parent_to_children_map = defaultdict(list)
    for pair in tree:
        parent_to_children_map[pair[0]].append(pair[1])
    # print(parent_to_children_map)
    person_names = {x
                    for c in parent_to_children_map.values()
                    for x in c} | set(parent_to_children_map.keys())
    # print(person_names)
    persons_dict = {name: TreeNode(name) for name in person_names}
    for parent_name, child_name in tree:
        try:
            persons_dict.get(parent_name).add_child(
                persons_dict.get(child_name))
        except TreeNodeException:
            return False
    if list(persons_dict.values())[0].get_all_names() == person_names:
        return True
    else:
        return False


if __name__ == "__main__":
    # These "asserts" using only for self-checking and
    # not necessary for auto-testing
    assert is_family([['Logan', 'Mike']]) == True, 'One father, one son'
    assert is_family([['Logan', 'Mike'], ['Logan',
                                          'Jack']]) == True, 'Two sons'
    assert is_family([['Logan', 'Mike'], ['Logan', 'Jack'],
                      ['Mike', 'Alexander']]) == True, 'Grandfather'
    assert is_family([['Logan', 'Mike'], ['Logan', 'Jack'], ['Mike', 'Logan']
                      ]) == False, 'Can you be a father to your father?'
    assert is_family([['Logan', 'Mike'], ['Logan', 'Jack'], ['Mike', 'Jack']
                      ]) == False, 'Can you be a father to your brother?'
    assert is_family([
        ['Logan', 'William'], ['Logan', 'Jack'], ['Mike', 'Alexander']
    ]) == False, 'Looks like Mike is stranger in Logan\'s family'
    assert is_family([
        ['Jack', 'Mike'],
        ['Logan', 'Mike'],
        ['Logan', 'Jack'],
    ]) == False, 'Two fathers'
    print("Looks like you know everything. It is time for 'Check'!")
