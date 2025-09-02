import os
import re
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_google_genai import ChatGoogleGenerativeAI

# -----------------------------
# Load API key and DB connection
# -----------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_NAME = "atliq_tshirts"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# -----------------------------
# Initialize LLM
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=API_KEY,
    temperature=0.2
)

# -----------------------------
# Database schema for LLM (with revenue instructions)
# -----------------------------
SCHEMA = """
You are an expert SQL generator. The database schema is:

Table: t_shirts
- t_shirt_id (INT, PK)
- brand (VARCHAR)
- size (VARCHAR)
- color (VARCHAR)
- price (DECIMAL)
- stock_quantity (INT)

Table: discounts
- t_shirt_id (INT, FK to t_shirts)
- pct_discount (DECIMAL)

Instructions:
- Always use correct table and column names.
- Write valid MySQL queries only.
- If the question asks about revenue **after discounts**, calculate:
      revenue = price * stock_quantity * (1 - pct_discount/100)
- Always join t_shirts and discounts when needed.
- Return SQL only, no explanations.
"""

# -----------------------------
# Size mapping
# -----------------------------
SIZE_MAPPING = {
    "extra small": "XS",
    "xs": "XS",
    "small": "S",
    "s": "S",
    "medium": "M",
    "m": "M",
    "large": "L",
    "l": "L",
    "extra large": "XL",
    "xl": "XL"
}

def normalize_sizes(question):
    """Replace natural size words with exact DB values"""
    question_lower = question.lower()
    for word, val in SIZE_MAPPING.items():
        if word in question_lower:
            question = re.sub(word, val, question, flags=re.IGNORECASE)
    return question

# -----------------------------
# SQL generation & cleaning
# -----------------------------
def clean_sql(sql_text):
    """Remove Markdown fences from LLM output"""
    match = re.search(r"```(?:sql)?\s*(.*?)\s*```", sql_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return sql_text.strip()

def get_sql_query(question):
    question = normalize_sizes(question)  # normalize sizes first
    prompt = SCHEMA + f"\n\nQuestion: {question}"
    response = llm.predict(prompt)
    sql_query = clean_sql(response)
    return sql_query

# -----------------------------
# Execute SQL
# -----------------------------
def execute_sql(sql_query):
    try:
        df = pd.read_sql(sql_query, engine)
        return df
    except Exception as e:
        return f"Error executing SQL: {e}"

# -----------------------------
# Generate human-readable answer
# -----------------------------
def generate_answer(question, sql_result):
    if isinstance(sql_result, pd.DataFrame):
        if sql_result.empty:
            summary = "No results"
        else:
            # If single numeric value, show that; otherwise show first few rows
            if sql_result.shape[1] == 1 and sql_result.shape[0] == 1:
                summary = sql_result.iloc[0, 0]
            else:
                summary = sql_result.head(5).to_dict(orient="records")
    else:
        summary = str(sql_result)
    prompt = f"Generate a human-readable answer for the question: '{question}' using the result: {summary}"
    response = llm.predict(prompt)
    return response

# -----------------------------
# Streamlit interface
# -----------------------------
st.title("Inventory Q&A")

question = st.text_input("Ask a question:")

if question:
    with st.spinner("Generating answer..."):
        sql_query = get_sql_query(question)
        result = execute_sql(sql_query)
        answer_text = generate_answer(question, result)
        st.write(answer_text)
