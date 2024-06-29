from typing import Iterator, NamedTuple


class To(NamedTuple):
    """
    一つの要素関係を表すクラス
    """
    f: str
    t: str

    def __str__(self)->str:
        return f"({self.f}, {self.t})"

class Relation:
    """
    関係を表すクラス
    """
    def __init__(self, label:str, relations:set[To]|None)->None:
        if relations is None:
            self.relations:set[To] = set()
        else:
            self.relations = relations
        self.label:str=label

    def __iter__(self) -> Iterator[To]:
        return iter(self.relations)

    def add(self, e:To) -> None:
        self.relations.add(e)

    def addAll(self, es:set[To]) -> None:
        self.relations.update(es)

    def __len__(self) -> int:
        return len(self.relations)

    def __str__(self) -> str:
        rs = ', '.join([str(e) for e in self.relations])
        return f"{self.label}:{{{rs}}}"
    
    def __eq__(self, value: 'Relation') -> bool:
        return self.relations == value.relations

    def isEmpty(self) -> bool:
        return len(self.relations) == 0
    
    def copy(self)->'Relation':
        return Relation(self.label,self.relations.copy())

    @staticmethod
    def multiply(A:'Relation', B:'Relation',label:str|None=None)->'Relation':
        """
        関係の結合$B\u2218 A$を求める
        """
        if label is None:
            label = f"{B.label}\u2218{A.label}"
        new_relations = Relation(label,None)
        for a_to in A:
            for b_to in B:
                if a_to.t == b_to.f:
                    new_relations.add(To(a_to.f,b_to.t))
        return new_relations

    def inverse(self)->'Relation':
        """
        関係の逆関係を求める
        """
        new_relations = Relation(f"{self.label}^{{-1}}",None)
        for (a,b) in self.relations:
            new_relations.add(To(b,a))
        return new_relations
    
    def closure(self, max = 5, reflective:bool=True) -> tuple[list['Relation'], 'Relation']:
        """
        R^0からR^nまでを生成し、それぞれをリストの要素として返す
        また、Kleene閉包を返す

        max:最大のn
        reflective:反射閉包を生成するかどうか
            true: reflective transitive closure
            false: transitive closure
        """
        L: list['Relation'] = list()
        Closure=Relation(fr'{self.label}^*',None)
        #アルファベットの抽出し、R^0を生成
        A:set[To] = set()
        for (a,b) in self.relations:
            A.add(To(a,a))
            A.add(To(b,b))
        L.append(Relation(f'{self.label}^0',A))
        if reflective:
            Closure.addAll(A)
        #R^1
        L.append(Relation(f'{self.label}^1',self.relations))
        Closure.addAll(self.relations)
        #R^2以降
        Current = self.copy()
        i = 2
        while i <= max:
            C  = Relation.multiply(Current, self)
            C.label = f'{self.label}^{i}'
            if C.isEmpty():#空集合の場合は終了
                break
            if C in L:#既に生成されたものと同じ場合は終了
                break
            L.append(C)
            Closure.addAll(C.relations)
            Current = C.copy()
            i += 1
        return L, Closure

    @staticmethod
    def converter(s:set[tuple[str,str]]) -> set[To]:
        """
        tupleの集合をToの集合に変換する
        """
        relations = set()
        for (a,b) in s:
            relations.add(To(a,b))
        return relations
    
if __name__ == "__main__":
    A = Relation("A",Relation.converter({("a","b"),("b","c")}))
    B = Relation("B",Relation.converter({("b","c"),("c","d"),("b","a")}))
    R = Relation('R',Relation.converter({('a','a'),('a','b'),('b','d'),('c','d'),('d','b')}))
    # L, C =R.closure(max=5)
    # for a in L:
    #     print(a)
    # print(C)
    print(B.inverse())