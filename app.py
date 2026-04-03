import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="IMTEX Product Explorer 2026",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a clean, text-focused industrial look
st.markdown("""
    <style>
    .main {
        background-color: #f4f7f9;
    }
    .stCard {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        background-color: white;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 15px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 250px;
    }
    .stCard:hover {
        border-color: #1f77b4;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    .product-title {
        color: #1a1a1a;
        font-size: 1.2rem;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 8px;
    }
    .category-badge {
        background-color: #f0f2f6;
        color: #475569;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: inline-block;
        margin-bottom: 12px;
    }
    .exhibitor-name {
        color: #1f77b4;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .description-text {
        font-size: 0.9rem;
        color: #4b5563;
        line-height: 1.5;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
    }
    </style>
    """, unsafe_allow_html=True)

# Cache data loading for performance
@st.cache_data
def load_data():
    df = pd.read_csv('imtex_products_final.csv')
    df['Description'] = df['Description'].fillna('Detailed specifications available in the full catalog.')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading database: {e}")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Search & Filters")
search_query = st.sidebar.text_input("Global Search", placeholder="Search products or exhibitors...")

st.sidebar.divider()
all_categories = sorted(df['Category'].unique().tolist())
selected_categories = st.sidebar.multiselect("Industrial Category", all_categories)

all_exhibitors = sorted(df['Exhibitor Name'].unique().tolist())
selected_exhibitors = st.sidebar.multiselect("Exhibitor Name", all_exhibitors)

# --- FILTER LOGIC ---
filtered_df = df.copy()

if search_query:
    query = search_query.lower()
    mask = (
        filtered_df['Product Name'].str.lower().str.contains(query, na=False) |
        filtered_df['Description'].str.lower().str.contains(query, na=False) |
        filtered_df['Exhibitor Name'].str.lower().str.contains(query, na=False)
    )
    filtered_df = filtered_df[mask]

if selected_categories:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]

if selected_exhibitors:
    filtered_df = filtered_df[filtered_df['Exhibitor Name'].isin(selected_exhibitors)]

# --- MAIN UI ---
st.title("🏗️ IMTEX 2026: The Ultimate Product Index")
st.markdown(f"Accessing **{len(filtered_df):,}** products from **{df['Exhibitor Name'].nunique()}** global exhibitors.")

if len(filtered_df) == 0:
    st.warning("No matches found. Please adjust your search terms.")
else:
    # Display results in a clean grid
    cols_per_row = 3
    display_limit = 99  # Increased limit now that images are gone
    
    # Process rows in chunks
    for i in range(0, min(len(filtered_df), display_limit), cols_per_row):
        cols = st.columns(cols_per_row)
        batch = filtered_df.iloc[i : i + cols_per_row]
        
        for j, (idx, row) in enumerate(batch.iterrows()):
            with cols[j]:
                st.markdown(f"""
                    <div class="stCard">
                        <div>
                            <div class="category-badge">{row['Category']}</div>
                            <div class="product-title">{row['Product Name']}</div>
                            <div class="exhibitor-name">Exhibitor: {row['Exhibitor Name']}</div>
                            <div class="description-text">{row['Description']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.link_button("🌐 Open Official Product Page", row['Source URL'], use_container_width=True)

    if len(filtered_df) > display_limit:
        st.info(f"Showing the top {display_limit} matches. Use filters to narrow your results.")
