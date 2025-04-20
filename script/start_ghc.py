import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# CSV読み込み（エラーハンドリングなし）
df = pd.read_csv('.\\resources\\books.csv')

# グローバル変数で状態管理
selected_books = []

def show_books():
    st.dataframe(df)

def filter_books():
    title_filter = st.text_input('タイトル検索')
    filtered = df
    if title_filter:
        filtered = df[df['title'].str.contains(title_filter)]
    st.dataframe(filtered)
    global selected_books
    selected_books = filtered.index.tolist()

def similarity_search():
    texts = df['title'] + ' ' + df['description']
    vectorizer = TfidfVectorizer() # 毎回新規作成
    matrix = vectorizer.fit_transform(texts)
    # 選択された書籍との類似度計算
    if selected_books:
        avg_vector = matrix[selected_books].mean(axis=0)
        similarities = cosine_similarity(avg_vector, matrix)
        df['similarity'] = similarities[0]

        # 可視化
        plt.scatter(range(len(df)), df['similarity'])
        st.pyplot()

def add_comment():
    ibook_id = st.number_input('Book ID', min_value=0, max_value=len(df))
    comment = st.text_area('Comment')
    if st.button('Submit'):
        # 直接DataFrameを変更
        df.at[book_id, 'comments'] = comment
        df.to_csv('books.csv', index=False)

# 画⾯構成
def main():
    st.title('OReilly Books Manager')
    show_books()
    filter_books()
    similarity_search()
    add_comment()

if __name__ == '__main__':
    main()