import sqlite3
import streamlit as st

# データベース接続を開く
conn = sqlite3.connect('board.db')
c = conn.cursor()

# テーブルがなければ作成
c.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, created_at DATETIME)''')

# 投稿をデータベースに保存する関数
def save_post(content):
    c.execute("INSERT INTO posts (content, created_at) VALUES (?, datetime('now'))", (content,))
    conn.commit()

# 投稿を削除する関数
def delete_post(post_id):
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()

# 新しい投稿を受け付けるフォーム
with st.form("post_form"):
    post_text = st.text_area("投稿内容を入力してください")
    submitted = st.form_submit_button("投稿")
    if submitted and post_text:
        save_post(post_text)
        st.success("投稿されました。")

# 投稿と削除ボタンを表示
c.execute("SELECT id, content FROM posts ORDER BY created_at DESC")
posts = c.fetchall()
for post in posts:
    post_id, post_content = post
    st.write(post_content)
    
    if st.button("削除", key=post_id):  # 各投稿に一意のキーを割り当てる
        delete_post(post_id)
        st.experimental_rerun()  # 投稿を削除した後、ページを再読み込みする
