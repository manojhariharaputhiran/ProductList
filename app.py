import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="TechSlice Solutions | Industrial Product Index 2026",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Responsive CSS Grid Design
st.markdown("""
    <style>
    .main {
        background-color: #f4f7f9;
    }
    /* Responsive Grid Container */
    .product-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 20px;
        padding: 10px 0;
    }
    /* Individual Card */
    .product-card {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 24px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s, box-shadow 0.2s;
        min-height: 280px;
    }
    .product-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }
    .card-content {
        margin-bottom: 20px;
    }
    .product-title {
        color: #1a1a1a;
        font-size: 1.15rem;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 8px;
    }
    .category-badge {
        background-color: #f0f2f6;
        color: #475569;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: inline-block;
        margin-bottom: 12px;
    }
    .exhibitor-name {
        color: #1f77b4;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .description-text {
        font-size: 0.9rem;
        color: #4b5563;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    /* Button Style */
    .catalog-link {
        display: block;
        text-align: center;
        background-color: #1f77b4;
        color: white !important;
        text-decoration: none !important;
        padding: 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: background-color 0.2s;
    }
    .catalog-link:hover {
        background-color: #155a8a;
    }
    </style>
    """, unsafe_allow_html=True)

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

# --- SIDEBAR ---
st.sidebar.header("🔍 TechSlice Search")
search_query = st.sidebar.text_input("Global Search", placeholder="Search products or manufacturers...")

st.sidebar.divider()
all_categories = sorted(df['Category'].unique().tolist())
selected_categories = st.sidebar.multiselect("Industrial Category", all_categories)

all_exhibitors = sorted(df['Exhibitor Name'].unique().tolist())
selected_exhibitors = st.sidebar.multiselect("Manufacturer / Brand", all_exhibitors)

st.sidebar.divider()
st.sidebar.info("Powered by **TechSlice Solutions**")

# --- FILTERING ---
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

# --- UI ---
st.title("🏗️ TechSlice Solutions: Industrial Index")
st.markdown(f"Accessing **{len(filtered_df):,}** products from **{df['Exhibitor Name'].nunique()}** global manufacturers.")

if len(filtered_df) == 0:
    st.warning("No matches found.")
else:
    display_limit = 100
    cards_html = ""
    
    # Building the HTML for the Responsive Grid
    for idx, row in filtered_df.head(display_limit).iterrows():
        desc = str(row['Description'])
        cards_html += f"""
            <div class="product-card">
                <div class="card-content">
                    <div class="category-badge">{row['Category']}</div>
                    <div class="product-title">{row['Product Name']}</div>
                    <div class="exhibitor-name">Source: {row['Exhibitor Name']}</div>
                    <div class="description-text">{desc}</div>
                </div>
                <a href="{row['Source URL']}" target="_blank" class="catalog-link">🌐 Open Product Page</a>
            </div>
        """
    
    st.markdown(f'<div class="product-grid">{cards_html}</div>', unsafe_allow_html=True)

    if len(filtered_df) > display_limit:
        st.info(f"Showing the top {display_limit} matches. Please use filters to refine your search.")
