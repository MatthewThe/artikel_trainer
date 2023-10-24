import streamlit as st
import streamlit.components.v1 as components

import feedparser
import requests
from bs4 import BeautifulSoup


# Define a list of German articles
german_articles = ["der", "die", "das", "den", "dem", "des"]


def main():
    st.set_page_config(layout="wide")
    
    st.title("German Article Trainer")
    
    if 'submit' not in st.session_state:
        st.session_state.submit = False
    
    col1, col2 = st.columns(2)

    with col1:
        # Text input field for the user to paste their text
        user_input_text = st.text_area("Paste your German text here:", key="input")
        
        st.button("Remove Articles and Fill In", on_click=click_submit)
        if st.session_state.submit:
            if user_input_text:
                create_form_with_holes(user_input_text)


    with col2:
        st.subheader("Train with articles from SZ.de")
        get_article_links()


def click_submit():
    st.session_state.submit = True


def create_form_with_holes(user_input_text):
    st.subheader("Fill in the Removed Articles:")
    
    for sentence in user_input_text.splitlines():
        create_text_with_holes(sentence)
    
    js = '''<script>
    let elements = window.parent.document.querySelectorAll('.artikel_input');

    elements.forEach((item) => {
        item.addEventListener("change", () => {
            answerKey = item.alt
            if (item.value.trim().toLowerCase() === answerKey.toLowerCase()) {
                item.style.color = "green";
            } else {
                item.style.color = "red";
            }
        })
    });
    </script>
    '''
    components.html(js)


def get_article_links(top_n: int = 10):
    url = "https://rss.sueddeutsche.de/rss/Topthemen"
    feed = feedparser.parse(url)
    
    for entry in feed.entries[:top_n]:
        st.button(entry.title, on_click=update_input_text, args=[entry.link])


def update_input_text(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    
    body = soup.find(itemprop="articleBody")
    
    article_text = ""
    for paragraph in body.find_all("p", attrs={'data-manual': 'paragraph'}):
        article_text += paragraph.get_text() + "\n\n"
        
    st.session_state.input = article_text
    click_submit()


def create_text_with_holes(sentence: str):
    # Split the text into words
    words = sentence.split()

    # Initialize a list to store user input for articles
    user_inputs = []
    

    # Use HTML and CSS to create an inline layout
    inline_layout = '<div style="display: flex; flex-wrap: wrap;">'

    i = 0
    for word in words:
        if word.lower() in german_articles:
            user_input = f'<input type="text" alt="{word}" style="width: 50px; height: 22px;" class="artikel_input">'
            # st.text_input(f"Fill in the article for '{word}':", key=f"input_{i}")
            i += 1
            inline_layout += f'<div style="margin-right: 5px;">{user_input}</div>'
        else:
            inline_layout += f'<div style="margin-right: 5px;">{word}</div>'

    inline_layout += '</div>'
     
    st.markdown(inline_layout, unsafe_allow_html=True)
    
    




if __name__ == "__main__":
    main()

