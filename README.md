# 関係と順序
- `relations.py`
    - `To`: 関係単体のクラス
    - `Relation`: 関係の集合を表すクラス
        - `multiply()`: 関係の結合
        - `add()`: 関係に要素を追加
        - `update()`: 関係から要素集合を追加
        - `inverse()`: 関係の逆関係を返す
        - `closure()`: 関係の推移閉包を求める
$$
\begin{align*}
R^\ast &= \bigcup_{n=0}^\infty R^n\\
R^+ &= \bigcup_{n=1}^\infty R^n\\
\end{align*}
$$