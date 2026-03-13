import streamlit as st
import google.generativeai as genai

# 1. Setup Page Config
st.set_page_config(page_title="University Competitor Finder", page_icon="🎓")

st.title("🎓 University Competitor Analyst (Gemini Edition)")
st.markdown("Enter a university to identify 10 competitor schools based on rankings, tuition, and proximity.")

# 2. Sidebar for API Key
with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", type="password")
    st.info("Get your free key at [aistudio.google.com](https://aistudio.google.com/)")

# 3. User Inputs
col1, col2 = st.columns(2)
with col1:
    uni_name = st.text_input("University Name", placeholder="e.g. Baylor University")
with col2:
    uni_type = st.selectbox("University Type", ["Public", "Private", "Private-Faith Based"])

# 4. Generate Button
if st.button("Generate Competitor List"):
    if not gemini_api_key:
        st.error("Please add your Gemini API key in the sidebar.")
    elif not uni_name:
        st.warning("Please enter a university name.")
    else:
        try:
            # Configure Gemini
            genai.configure(api_key=gemini_api_key)
            
            # Initialize the model (Gemini 1.5 Flash is fast and efficient)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # The exact prompt requested
            analyst_prompt = f"""
            You are an analyst who looks at recruiting trends for a university to identify competitor markets and identify competitor schools. 
            The target school is: {uni_name} (Type: {uni_type}).

            Using publicly available data such as Niche rankings, US News and come up with 10 schools for a partner schools. 
            Use IPEDS data to understand trends of schools around you and see how they are comparing to identify potential "blue sky" 
            ideas of schools and markets that can be competitor. 

            For each of the 10 competitors, analyze the following comparables:
            - Tuition (estimated)
            - Geographic proximity (Region/Distance)
            - Acceptance rate 
            - Rankings (Niche/US News)
            
            Format the output as a clean Markdown table.
            """

            with st.spinner(f"Gemini is analyzing markets for {uni_name}..."):
                # Call Gemini API
                response = model.generate_content(analyst_prompt)
                
                st.subheader(f"Competitor Analysis for {uni_name}")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
