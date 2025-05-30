import streamlit as st
from process import translate, explain

st.set_page_config(page_title="Code Alchemy", page_icon="🕵️‍♂️", layout="wide")
st.title("🕵️‍♂️ Code Alchemy: Your AI-Powered Code Conjurer")
st.markdown("### Transform any snippet into the language of your choice. No magic wand needed.")
st.caption("Watch code morph like never before — powered by cutting-edge AI.")

languages = [
    "🐍 Python", "🔨 JavaScript", "🔵 TypeScript", "☕ Java", "🔣 C", "🢨 C++", "🪟 C#", 
    "🐹 Go", "🦀 Rust", "🍏 Swift", "📱 Kotlin", "🌯 Dart", "💎 Ruby", "🧬 Perl",
    "🌐 HTML", "🎨 CSS", "🢾 JSON", "💻 Bash", "👚 Shell", "⚡ PowerShell",
    "🧮 SQL", "📊 R", "🔬 MATLAB", "📐 Julia", "🔗 GraphQL", "📄 YAML", 
    "🐳 Dockerfile", "🧱 Makefile", "⚙️ Assembly", "📦 Protobuf", 
    "🐢 Haskell", "📜 Scala", "🐉 Lua"
]

def clean_lang(label):
    return label.split(" ", 1)[1].lower()

# Initialize session state vars for persistence
if "translated_code" not in st.session_state:
    st.session_state.translated_code = ""
if "explanation" not in st.session_state:
    st.session_state.explanation = ""

col1, col2 = st.columns(2)

with col1:
    slang_label = st.selectbox("Choose the source language:", languages, index=0)

with col2:
    tlang_label = st.selectbox("Choose the target language:", languages, index=1)


slang = clean_lang(slang_label)
tlang = clean_lang(tlang_label)
col1,col2=st.columns(2)
with col1:
    
    input_text = st.text_area("Paste your code here...", height=200)
with col2:
    if input_text.strip():
        st.markdown("#### 📟 Input Preview:")
        st.code(input_text, language=slang)
col1,col2=st.columns(2)
with col1:
    strict_mode = st.checkbox("Strict mode (preserve typos and logic as-is)", value=True)
with col2:
    view_mode = st.radio("View Output As:", ["Code Only", "Side-by-Side"], horizontal=True)
st.divider()
st.markdown("### Ready to turn your code into pure gold? ✨ Hit Translate and watch the magic!")

# Buttons container
col_buttons = st.container()
with col_buttons:
    if st.button("✨ Translate"):
            if not input_text.strip():
                st.warning("Please enter some code to translate.")
            elif slang == tlang:
                st.info("Source and target language are the same.")
            else:
                with st.spinner("Summoning Gemini spirits... ✨"):
                    try:
                        st.session_state.translated_code = translate(slang, tlang, input_text, strict_mode)
                        st.session_state.explanation = ""  # Clear old explanation on new translate
                        st.success("🧪 Alchemy Complete! Your code has been transmuted.")
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

st.markdown("---")

if st.session_state.translated_code:
    if view_mode == "Side-by-Side":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📞 Original")
            st.code(input_text, language=slang)
        with col2:
            st.markdown("### 🔮 Translated")
            st.code(st.session_state.translated_code, language=tlang)
    else:
        st.markdown("### 🔮 Translated Code")
        st.code(st.session_state.translated_code, language=tlang)

    st.download_button(
        "💾 Download", 
        st.session_state.translated_code, 
        file_name=f"translated.{tlang}", 
        mime="text/plain"
    )
    explain_disabled = not bool(st.session_state.translated_code)
    if st.button("🔍 Explain Translated Code", disabled=explain_disabled):
            with st.spinner("Casting an explanation spell... 🪄"):
                try:
                    st.session_state.explanation = explain(st.session_state.translated_code, tlang)
                except Exception as e:
                    st.error(f"Explanation failed: {e}")
if st.session_state.explanation:
    st.markdown("---")
    st.markdown("### 📖 Code Explanation")
    st.write(st.session_state.explanation)

if st.button("Clear All"):
    st.session_state.translated_code = ""
    st.session_state.explanation = ""
