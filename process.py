# process.py
import re
import streamlit as st
import google.generativeai as genai

def clean_code_blocks(text):
    return re.sub(r"^```.*?\n|\n```$", "", text.strip(), flags=re.DOTALL)

def translate(source, target, code, strict):
    genai.configure(api_key=st.secrets["api_keys"]["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config={
        "temperature": 0.2 if strict else 0.7
    })

    prompt = f"""
{'You are a strict code translator.' if strict else 'Convert the following code carefully.'}

Source Language: {source}
Target Language: {target}

{'⚠️ Do not correct typos or logic.\n⚠️ Reflect the same structure and errors.' if strict else 'Preserve logic, adapt syntax, and follow best practices.'}

Code:
{code}

Only return the translated code. No explanations.
"""

    response = model.generate_content(prompt)
    output = clean_code_blocks(response.text)
    return output if output else "⚠️ Translation failed or returned empty output."

def explain(code, language):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config={
        "temperature": 0.7
    })

    prompt = f"""
You are a helpful and accurate programming assistant.

Explain the following code in simple terms. Cover what each part does, how it works, and why it’s written that way.

The explanation should be:
- Clear and easy to understand, even for beginners.
- Step-by-step and well-structured.
- Include key concepts or syntax relevant to {language}.

Only explain the code. Do not modify or re-translate it.

Language: {language}
Code:
{code}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
