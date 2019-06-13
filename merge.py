import pandas as pd 

# book3 仙侠
# book4 玄幻
# book6 历史
# book7 都市
# book8 奇幻
# book9 武侠
# book10 游戏
# book11 科幻
# book12 二次元
# book13 军事


b1 = pd.read_csv('book3.csv')
b2 = pd.read_csv('book4.csv')
b3 = pd.read_csv('book6.csv')
b4 = pd.read_csv('book7.csv')
b5 = pd.read_csv('book8.csv')
b6 = pd.read_csv('book9.csv')
b7 = pd.read_csv('book10.csv')
b8 = pd.read_csv('book11.csv')
b9 = pd.read_csv('book12.csv')
all_book = [b1, b2, b3, b4, b5, b6, b7, b8, b9]
book = pd.concat(all_book)
my_columns = ['title', 'author', 'cate1', 'cate2', 'size', '仙草', '毒草', '粮草', '干草', '枯草', 'abstract', 'code', 'link1', 'link2']
book = book[my_columns]
book.to_csv('book.csv', index=False)
