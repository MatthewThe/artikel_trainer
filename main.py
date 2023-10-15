import streamlit as st
import streamlit.components.v1 as components

# Define a list of German articles
german_articles = ["der", "die", "das", "den", "dem", "des"]

def main():
    st.title("German Article Trainer")

    # Text input field for the user to paste their text
    user_input_text = st.text_area("Paste your German text here:")

    if st.button("Remove Articles and Fill In"):
        if user_input_text:
            # Split the text into words
            words = user_input_text.split()

            # Initialize a list to store user input for articles
            user_inputs = []

            st.subheader("Fill in the Removed Articles:")

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
if __name__ == "__main__":
    main()

