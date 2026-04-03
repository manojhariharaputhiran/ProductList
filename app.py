import streamlit as st
import pandas as pd
import html

# Set page configuration
st.set_page_config(
    page_title="TechSlice Solutions | Product Index",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Clean, robust CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    /* The Card Container */
    .card {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 320px;
        transition: all 0.2s ease-in-out;
    }
    .card:hover {
        border-color: #3b82f6;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .card-top {
        flex-grow: 1;
    }
    .badge {
        background-color: #eff6ff;
        color: #1e40af;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 12px;
    }
    .title {
        color: #0f172a;
        font-size: 1.1rem;
        font-weight: 700;
        line-height: 1.4;
        margin-bottom: 8px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .source {
        color: #3b82f6;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .desc {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.6;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    /* Reset Streamlit column padding for a tighter grid */
    [data-testid="column"] {
        padding: 0 10px !important;
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
st.sidebar.header("🎯 Filters")
search_query = st.sidebar.text_input("Global Search", placeholder="Keywords, brands, models...")

st.sidebar.divider()
all_categories = sorted(df['Category'].unique().tolist())
selected_categories = st.sidebar.multiselect("Category", all_categories)

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

# --- MAIN UI ---
st.title("🏗️ TechSlice Solutions: Industrial Index")
st.markdown(f"**{len(filtered_df):,}** matches found across **{df['Exhibitor Name'].nunique()}** global sources.")

if len(filtered_df) == 0:
    st.warning("No matches found. Please adjust your filters.")
else:
    # Use a dynamic grid based on columns
    display_limit = 99
    cols_per_row = 3
    
    for i in range(0, min(len(filtered_df), display_limit), cols_per_row):
        cols = st.columns(cols_per_row)
        batch = filtered_df.iloc[i : i + cols_per_row]
        
        for j, (idx, row) in enumerate(batch.iterrows()):
            with cols[j]:
                # Escaping content for safety
                p_name = html.escape(str(row['Product Name']))
                p_cat = html.escape(str(row['Category']))
                p_brand = html.escape(str(row['Exhibitor Name']))
                p_desc = html.escape(str(row['Description']))
                
                st.markdown(f"""
                    <div class="card">
                        <div class="card-top">
                            <div class="badge">{p_cat}</div>
                            <div class="title">{p_name}</div>
                            <div class="source">Source: {p_brand}</div>
                            <div class="desc">{p_desc}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.link_button("🌐 Open Catalog", row['Source URL'], use_container_width=True)

    if len(filtered_df) > display_limit:
        st.info(f"Showing top {display_limit} matches. Refine your filters to see more.")
