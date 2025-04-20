import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

@st.cache_data
def load_books(file_path):
    """
    CSVファイルを読み込み、データフレームを返す。
    エラーハンドリングを追加し、データが存在しない場合の対応を行う。
    """
    try:
        df = pd.read_csv(file_path)
        required_columns = ['title', 'description']
        if not all(col in df.columns for col in required_columns):
            st.error(f"CSVファイルに必要な列が不足しています: {required_columns}")
            return pd.DataFrame()
        if 'comments' not in df.columns:
            df['comments'] = ''  # コメント列がない場合は追加
        return df
    except FileNotFoundError:
        st.error("CSVファイルが見つかりません。ファイルパスを確認してください。")
        return pd.DataFrame()
    except pd.errors.ParserError:
        st.error("CSVファイルのフォーマットが不正です。")
        return pd.DataFrame()

@st.cache_data
def get_tfidf_matrix(texts):
    """
    TF-IDFベクトルを生成し、キャッシュする。
    """
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(texts)

def show_books(df):
    """
    書籍一覧を表示する。
    データが空の場合は警告を表示する。
    """
    if df.empty:
        st.warning("表示する書籍データがありません。")
    else:
        st.dataframe(df)

def filter_books(df):
    """
    書籍をタイトルでフィルタリングする。
    """
    title_filter = st.text_input('タイトル検索')
    if title_filter:
        filtered = df[df['title'].str.contains(title_filter, case=False, na=False)]
        st.dataframe(filtered)
        return filtered.index.tolist()
    else:
        st.dataframe(df)
        return []

def similarity_search(df, selected_books):
    """
    選択された書籍との類似度を計算し、可視化する。
    """
    if df.empty:
        st.warning("類似度計算を行うデータがありません。")
        return

    texts = df['title'] + ' ' + df['description']
    matrix = get_tfidf_matrix(texts)

    if selected_books:
        avg_vector = matrix[selected_books].mean(axis=0)
        similarities = cosine_similarity(avg_vector, matrix)
        df['similarity'] = similarities[0]

        # 類似度を可視化
        plt.figure(figsize=(10, 6))
        plt.bar(df.index, df['similarity'], color='skyblue')
        plt.xlabel('Book Index')
        plt.ylabel('Similarity')
        plt.title('Book Similarity')
        st.pyplot()
    else:
        st.warning("書籍を選択してください。")

def add_comment(df):
    """
    書籍にコメントを追加する。
    """
    if df.empty:
        st.warning("コメントを追加するデータがありません。")
        return

    book_id = st.number_input('Book ID', min_value=0, max_value=len(df) - 1, step=1)
    comment = st.text_area('Comment')
    if st.button('Submit'):
        if 'comments' not in df.columns:
            df['comments'] = ''
        df.at[book_id, 'comments'] = comment
        df.to_csv('books.csv', index=False)
        st.success("コメントが追加されました。")

def main():
    st.title('OReilly Books Manager')
    file_path = '.\\resources\\books.csv'
    df = load_books(file_path)

    if not df.empty:
        show_books(df)
        selected_books = filter_books(df)
        similarity_search(df, selected_books)
        add_comment(df)

if __name__ == '__main__':
    main()