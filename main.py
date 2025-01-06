import os
import random
import pandas as pd
import streamlit as st
from app.langflow_helper.langflow_wrapper import LangFlow_Helper

def get_graph(df):
    numeric_cols = [col for col in df.columns if df[col].dtype != 'object'] 
    categorical_cols = [col for col in df.columns if df[col].dtype == 'object'] 
    
    print("numercia_cols: ", numeric_cols)
    print("cat_cols: ", categorical_cols)
    
    bar_x = random.choice(categorical_cols)
    bar_y = random.choice(numeric_cols)
    
    print("bar_x: ", bar_x)
    print("bar_y: ", bar_y)
    
    categorical_cols.remove(bar_x)
    numeric_cols.remove(bar_y)
    
    line_x = random.choice(categorical_cols)
    line_y = random.choice(numeric_cols)
    
    
    print("line_x: ", line_x)
    print("line_y: ", line_y)

    st.title(f"{str(bar_x)} VS {str(bar_y)}")
    st.bar_chart(data=df, x=bar_x, y=bar_y, x_label=str(bar_x), y_label=str(bar_y))
    
    df_agg = df.groupby(line_x)[line_y].mean().reset_index()

    st.title(f"{str(line_x)} VS {str(line_y)}")
    st.line_chart(data=df_agg, x=line_x, y=line_y, x_label=str(line_x), y_label=f"{line_y}")
    
    
    

def login():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # If already authenticated, skip the login page
    if st.session_state["authenticated"]:
        return True

    st.title("🔒 Login")
    st.markdown("Please enter your credentials to proceed.")

    # Input fields for login
    username = st.text_input("📧 Email", placeholder="Enter your email", key="login_username")
    password = st.text_input("🔑 Password", placeholder="Enter your password", type="password", key="login_password")

    # Login button
    if st.button("🔓 Login"):
        if username == "admin@gmail.com" and password == "Admin@123":
            st.session_state["authenticated"] = True  
        else:
            st.error("❌ Invalid credentials. Please try again.")

    return False

def main():
    st.title("📄 CSV File Processor")
    st.markdown("Upload a CSV file and select the type of post you'd like to generate insights for.")

    uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"], help="Ensure the file is in CSV format.")

    file_path = None
    if uploaded_file is not None:
        temp_dir = "data"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ File uploaded successfully!")
        df = pd.read_csv(file_path)
    
    post_type = st.selectbox(
        "🎨 Select a post type:",
        ("--Select--", "Carousel", "Reels", "Static Images"),
        help="Choose the type of post you want insights for."
    )

    
    langflow = LangFlow_Helper(query=post_type, file_path=file_path)

    if st.button("🚀 Submit"):
        with st.spinner(text=f"Generating analysis for {post_type}..."):
            if file_path:
                response = langflow.get_response()
                st.text_area("📝 Response:", response, height=200)
                get_graph(df=df)
            else:
                st.error("Please upload a CSV file before submitting.")

    if st.button("🔒 Logout"):
        langflow.delete_data()
        if file_path:
            os.remove(file_path)
        st.session_state["authenticated"] = False
        login()
        st.rerun()

if __name__ == "__main__":
    if login():
        main()
        
