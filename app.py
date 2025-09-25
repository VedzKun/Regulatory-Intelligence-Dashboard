import streamlit as st
import pandas as pd
import os

# --- Page Setup ---
st.set_page_config(page_title="Customs Regulatory Dashboard", layout="wide")

# --- App Title and Description ---
st.title("Customs Regulatory Intelligence Dashboard 📋")
st.markdown("""
    This dashboard provides easy access to relevant Customs acts, notifications,
    and circulars by searching through an automatically collected dataset.
""")
st.markdown("---")

# --- Data Loading ---
@st.cache_data
def load_data(file_path):
    """Loads the scraped data from a CSV file."""
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"Data file '{file_path}' not found. Please run the data collector script first.")
        return pd.DataFrame()

# Assuming the scraper created 'dgft_public_notices.csv'
file_path = 'dgft_public_notices.csv'
df = load_data(file_path)

if not df.empty:
    st.success(f"Successfully loaded {len(df)} records from {file_path}")

    # --- Search and Filter UI ---
    st.subheader("Search and Filter")
    
    # Text input for searching
    search_query = st.text_input("Enter keywords to search (e.g., 're-export', 'FTP', 'SEZ')", "")
    
    # Checkboxes for filtering specific requirements
    st.markdown("##### Filter by specific issues:")
    col1, col2, col3 = st.columns(3)
    with col1:
        rejection_of_exported_material = st.checkbox("Rejection of Exported Material")
    with col2:
        import_of_foc_material = st.checkbox("Import of FOC Material")
    with col3:
        igcr_compliance = st.checkbox("IGCR Compliance")

    # --- Filtering Logic ---
    filtered_df = df.copy()

    # Filter based on search query
    if search_query:
        filtered_df = filtered_df[
            filtered_df['Title'].str.contains(search_query, case=False, na=False)
        ]

    # Filter based on checkboxes (this is a simplified example)
    # A real-world app would use a more sophisticated method like RAG
    if rejection_of_exported_material:
        filtered_df = filtered_df[
            filtered_df['Title'].str.contains('export|rejection|customs duty', case=False, na=False)
        ]

    if import_of_foc_material:
        filtered_df = filtered_df[
            filtered_df['Title'].str.contains('import|FOC|duty', case=False, na=False)
        ]

    if igcr_compliance:
        filtered_df = filtered_df[
            filtered_df['Title'].str.contains('IGCR|concessional|duty', case=False, na=False)
        ]
        
    # --- Display Results ---
    st.markdown("---")
    st.subheader("Search Results")
    
    if filtered_df.empty:
        st.info("No matching records found. Please try a different query.")
    else:
        st.dataframe(filtered_df, use_container_width=True)

    # --- Stakeholder Training Module ---
    st.markdown("---")
    st.subheader("Visual Compliance Trackers & Training")
    st.info("This section would be for flowcharts, timelines, and other visual aids for stakeholder training on Customs law updates.")
