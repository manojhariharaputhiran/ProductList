import streamlit as st
import pandas as pd
import html
import re

# Set page configuration
st.set_page_config(
    page_title="TechSlice Solutions | Product Index",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- THE EXPANDED TRANSLATION ENGINE ---
TRANSLATIONS = {
    # Keywords
    '発電所保全装置': 'Power Plant Maintenance Equipment',
    '管内面用': 'Internal Pipe',
    'ウォータージェット': 'Water Jet',
    '洗浄ノズル': 'Cleaning Nozzle',
    'ビューレットノズル': 'Bullet Nozzle',
    'セルフプロペラノズル': 'Self-Propelled Nozzle',
    '小径管': 'Small Diameter Pipe',
    '研削': 'Grinding',
    '旋盤': 'Lathe',
    '研磨': 'Polishing',
    '切削': 'Cutting',
    '部品': 'Parts/Components',
    '創業の精神': 'Corporate Spirit',
    '自ら考え、自ら造り、自ら販売・サービスする': 'Think for yourself, Create for yourself, Sell and Service for yourself',
    '高圧水技術': 'High Pressure Water Tech',
    '空気圧技術': 'Pneumatic Tech',
    'エネルギー市場関連': 'Energy Market Related',
    '技術開発': 'Technical Development',
    '現在では': 'Currently',
    '切る・削る・洗う・磨く・砕く・解す': 'Cut, Shave, Wash, Polish, Crush, and Unravel',
    '６つの「超技術」を展開しています': 'Developing 6 "Super Technologies"',
    'EWS Ansprechpartner': 'EWS Contact Person',
    'Produkte': 'Products',
    'Lösungen': 'Solutions',
    'Werkzeug': 'Tooling',
    'Ansprechpartner': 'Contact',
    'Halter': 'Holder',
    'Spannfutter': 'Chuck',
    'Fräsen': 'Milling',
    'Drehen': 'Turning'
}

def translate_text(text):
    if pd.isna(text): return ""
    text = str(text)
    # Global replacement of all mapped terms
    for jp, en in TRANSLATIONS.items():
        text = text.replace(jp, en)
    return text

# Clean, robust CSS
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .card {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 340px;
    }
    .badge {
        background-color: #eff6ff; color: #1e40af;
        padding: 4px 10px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 700;
        text-transform: uppercase; margin-bottom: 12px;
    }
    .title {
        color: #0f172a; font-size: 1.1rem; font-weight: 700;
        margin-bottom: 8px; min-height: 3rem;
    }
    .source { color: #3b82f6; font-size: 0.85rem; font-weight: 600; margin-bottom: 12px; }
    .desc { 
        color: #64748b; font-size: 0.85rem; line-height: 1.6; 
        height: 7.5rem; overflow: hidden;
        display: -webkit-box; -webkit-line-clamp: 5; -webkit-box-orient: vertical;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('imtex_products_final.csv')
    # Apply translation to BOTH Name and Description
    df['Product Name'] = df['Product Name'].apply(translate_text)
    df['Description'] = df['Description'].apply(translate_text)
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
st.markdown(f"**{len(filtered_df):,}** matches found.")

if len(filtered_df) == 0:
    st.warning("No matches found. Please adjust your filters.")
else:
    display_limit = 99
    cols_per_row = 3
    
    for i in range(0, min(len(filtered_df), display_limit), cols_per_row):
        cols = st.columns(cols_per_row)
        batch = filtered_df.iloc[i : i + cols_per_row]
        
        for j, (idx, row) in enumerate(batch.iterrows()):
            with cols[j]:
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
        st.info(f"Showing top {display_limit} matches.")
