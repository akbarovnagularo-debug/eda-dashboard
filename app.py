import streamlit as st
import pandas as pd
import plotly.express as px

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="EDA Dashboard", page_icon="📊", layout="wide")

# --- Sarlavha ---
st.title("📈 Interaktiv EDA Dashboard")
st.caption("CSV yoki Excel fayl yuklab, ma'lumotlaringizni avtomatik tahlil qiling 📊")

# --- Ma'lumot yuklash ---
st.sidebar.header("📁 Ma'lumot yuklash")
uploaded_file = st.sidebar.file_uploader("Fayl yuklang (.csv yoki .xlsx)", type=["csv", "xlsx"])

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return df

# --- Fayl yuklangandan keyin ---
if uploaded_file is not None:
    with st.spinner("⏳ Ma'lumot yuklanmoqda..."):
        try:
            df = load_data(uploaded_file)
            st.success("✅ Ma'lumot muvaffaqiyatli yuklandi!")
        except Exception as e:
            st.error(f"❌ Xatolik: {e}")
            st.stop()

    # --- Asosiy ma'lumot ko‘rsatish ---
    st.subheader("🔍 Ma'lumotni ko‘rish")
    rows = st.slider("Nechta qatorni ko‘rsatamiz?", 5, 100, 10)
    st.dataframe(df.head(rows), use_container_width=True)

    # --- Ustunlar ro‘yxati ---
    with st.expander("📋 Ustun nomlari"):
        st.write(list(df.columns))

    # --- Statistik tahlil ---
    st.markdown("---")
    st.subheader("📊 Statistik tahlil")
    st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

    # --- Vizual tahlil ---
    st.markdown("---")
    st.subheader("📈 Vizual tahlil")

    # Ustunlarni aniqlash
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    if len(num_cols) >= 2 and len(cat_cols) >= 1:
        st.write("Quyidagi ustunlardan tanlang:")

        price_col = st.selectbox("💰 Narx ustunini tanlang:", options=num_cols)
        qty_col = st.selectbox("📦 Miqdor ustunini tanlang:", options=num_cols)
        cat_col = st.selectbox("🏷️ Kategoriya ustunini tanlang:", options=cat_cols)

        if price_col and qty_col and cat_col:
            df['Revenue'] = df[price_col] * df[qty_col]
            revenue_by_cat = df.groupby(cat_col)['Revenue'].sum().reset_index()

            # Bar chart
            fig_bar = px.bar(
                revenue_by_cat, x=cat_col, y='Revenue',
                text='Revenue', title=f"{cat_col} bo‘yicha daromad",
                color=cat_col, color_discrete_sequence=px.colors.sequential.Blues
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            # Pie chart
            fig_pie = px.pie(
                revenue_by_cat, names=cat_col, values='Revenue',
                title=f"{cat_col} bo‘yicha ulush", hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # Line chart (agar sana ustuni mavjud bo‘lsa)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                revenue_by_date = df.groupby('Date')['Revenue'].sum().reset_index()
                fig_line = px.line(
                    revenue_by_date, x='Date', y='Revenue',
                    title="📅 Vaqt bo‘yicha daromad trendi"
                )
                st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("⬅️ Yuqoridan ustunlarni tanlang — shunda grafiklar hosil bo‘ladi.")
    else:
        st.warning("⚠️ Grafik hosil qilish uchun kamida 2 ta raqamli va 1 ta matnli ustun bo‘lishi kerak.")

    # --- Xotirani tozalash tugmasi ---
    if st.button("🧹 Xotirani tozalash"):
        load_data.clear()
        st.success("Cache tozalandi.")
else:
    st.info("⬅️ Chap tomondan CSV yoki Excel fayl yuklang.")






