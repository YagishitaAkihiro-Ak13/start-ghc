import streamlit as st
import pandas as pd

def load_books(file_path):
    """
    CSVファイルを読み込み、データフレームを返す。
    エラーハンドリングを追加し、データが存在しない場合の対応を行う。
    """
    try:
        df = pd.read_csv(file_path)
        # 必要な列が存在するか確認
        required_columns = ['title', 'description']
        if not all(col in df.columns for col in required_columns):
            st.error(f"CSVファイルに必要な列が不足しています: {required_columns}")
            return pd.DataFrame()  # 空のデータフレームを返す
        return df
    except FileNotFoundError:
        st.error("CSVファイルが見つかりません。ファイルパスを確認してください。")
        return pd.DataFrame()  # 空のデータフレームを返す
    except pd.errors.ParserError:
        st.error("CSVファイルのフォーマットが不正です。")
        return pd.DataFrame()  # 空のデータフレームを返す

def show_books(df):
    """
    書籍一覧を表示する。
    データが空の場合は警告を表示する。
    """
    if df.empty:
        st.warning("表示する書籍データがありません。")
    else:
        st.dataframe(df)

# メイン処理
def main():
    st.title('OReilly Books Manager')
    file_path = 'books.csv'
    df = load_books(file_path)
    show_books(df)

if __name__ == '__main__':
    main()