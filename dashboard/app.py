import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 1. CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# 2. CHARGEMENT DES DONNÉES
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv("data/sample_clean.csv")

    # Conversion de la date
    data["Order_Date"] = pd.to_datetime(data["Order_Date"])

    return data


df = load_data()


# ============================================================
# 3. TITRE
# ============================================================

st.markdown(
    '<div class="main-title">🛒 E-Commerce Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyse interactive des ventes, des clients et de la rentabilité'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 4. SIDEBAR — FILTRES
# ============================================================

st.sidebar.header("🔎 Filtres")


# Customer Segment
segment = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(
        df["Customer_Segment"].dropna().unique()
    ),
    default=[]
)


# Product Category
category = st.sidebar.multiselect(
    "Product Category",
    options=sorted(
        df["Product_Category"].dropna().unique()
    ),
    default=[]
)


# Return Status
return_status = st.sidebar.multiselect(
    "Return Status",
    options=sorted(
        df["Return_Status"].dropna().unique()
    ),
    default=[]
)


# Payment Method
payment = st.sidebar.multiselect(
    "Payment Method",
    options=sorted(
        df["Payment_Method"].dropna().unique()
    ),
    default=[]
)



# ============================================================
# 5. APPLICATION DES FILTRES
# ============================================================

filtered_df = df.copy()


if segment:
    filtered_df = filtered_df[
        filtered_df["Customer_Segment"].isin(segment)
    ]


if category:
    filtered_df = filtered_df[
        filtered_df["Product_Category"].isin(category)
    ]


if return_status:
    filtered_df = filtered_df[
        filtered_df["Return_Status"].isin(return_status)
    ]


if payment:
    filtered_df = filtered_df[
        filtered_df["Payment_Method"].isin(payment)
    ]


# Nombre de lignes après filtrage
st.sidebar.divider()

st.sidebar.metric(
    "Transactions sélectionnées",
    f"{len(filtered_df):,}"
)


# ============================================================
# 6. KPI
# ============================================================

total_sales = filtered_df["Net_Sales_USD"].sum()

total_profit = filtered_df["Order_Profit_USD"].sum()

total_orders = filtered_df["Order_ID"].nunique()

average_order = filtered_df["Total_Order_Value_USD"].mean()


st.header("📌 Indicateurs clés")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Sales",
        f"${total_sales:,.0f}"
    )


with col2:

    st.metric(
        "Total Profit",
        f"${total_profit:,.0f}"
    )


with col3:

    st.metric(
        "Number of Orders",
        f"{total_orders:,}"
    )


with col4:

    st.metric(
        "Average Order Value",
        f"${average_order:,.2f}"
    )


# ============================================================
# 7. ANALYSE DES VENTES
# ============================================================

st.divider()

st.header("📊 Analyse des ventes")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# 7.1 Évolution des ventes
# ------------------------------------------------------------

with col1:

    st.subheader("Évolution des ventes")

    sales_over_time = (
        filtered_df
        .groupby("Order_Date", as_index=False)
        ["Net_Sales_USD"]
        .sum()
    )

    fig_sales = px.line(
        sales_over_time,
        x="Order_Date",
        y="Net_Sales_USD",
        title="Évolution des ventes nettes"
    )

    fig_sales.update_layout(
        xaxis_title="Date",
        yaxis_title="Ventes nettes (USD)"
    )

    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )


# ------------------------------------------------------------
# 7.2 Ventes par catégorie
# ------------------------------------------------------------

with col2:

    st.subheader("Ventes par catégorie")

    sales_category = (
        filtered_df
        .groupby(
            "Product_Category",
            as_index=False
        )
        ["Net_Sales_USD"]
        .sum()
        .sort_values(
            "Net_Sales_USD",
            ascending=False
        )
    )

    fig_category = px.bar(
        sales_category,
        x="Product_Category",
        y="Net_Sales_USD",
        title="Ventes nettes par catégorie"
    )

    fig_category.update_layout(
        xaxis_title="Catégorie",
        yaxis_title="Ventes nettes (USD)"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ============================================================
# 8. CLIENTS ET RENTABILITÉ
# ============================================================

st.header("👥 Clients et rentabilité")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# 8.1 Ventes par segment
# ------------------------------------------------------------

with col1:

    st.subheader("Ventes par segment")

    sales_segment = (
        filtered_df
        .groupby(
            "Customer_Segment",
            as_index=False
        )
        ["Net_Sales_USD"]
        .sum()
        .sort_values(
            "Net_Sales_USD",
            ascending=False
        )
    )

    fig_segment = px.bar(
        sales_segment,
        x="Customer_Segment",
        y="Net_Sales_USD",
        title="Ventes nettes par segment client"
    )

    fig_segment.update_layout(
        xaxis_title="Segment client",
        yaxis_title="Ventes nettes (USD)"
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )


# ------------------------------------------------------------
# 8.2 Ventes vs bénéfice
# ------------------------------------------------------------

with col2:

    st.subheader("Ventes vs bénéfice")

    fig_profit = px.scatter(
        filtered_df,
        x="Net_Sales_USD",
        y="Order_Profit_USD",
        color="Customer_Segment",
        hover_data=[
            "Product_Category",
            "Order_ID"
        ],
        title="Relation entre ventes et bénéfice"
    )

    fig_profit.update_layout(
        xaxis_title="Ventes nettes (USD)",
        yaxis_title="Bénéfice (USD)"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


# ============================================================
# 9. RETOURS ET PERFORMANCE
# ============================================================

st.header("↩️ Retours et performance")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# 9.1 Statut des retours
# ------------------------------------------------------------

with col1:

    st.subheader("Répartition des retours")

    return_data = (
        filtered_df
        .groupby("Return_Status")
        .size()
        .reset_index(name="Orders")
    )

    fig_returns = px.pie(
        return_data,
        names="Return_Status",
        values="Orders",
        hole=0.4,
        title="Statut des commandes"
    )

    st.plotly_chart(
        fig_returns,
        use_container_width=True
    )


# ------------------------------------------------------------
# 9.2 Bénéfice par catégorie
# ------------------------------------------------------------

with col2:

    st.subheader("Bénéfice par catégorie")

    profit_category = (
        filtered_df
        .groupby(
            "Product_Category",
            as_index=False
        )
        ["Order_Profit_USD"]
        .sum()
        .sort_values(
            "Order_Profit_USD",
            ascending=False
        )
    )

    fig_profit_category = px.bar(
        profit_category,
        x="Product_Category",
        y="Order_Profit_USD",
        title="Bénéfice total par catégorie"
    )

    fig_profit_category.update_layout(
        xaxis_title="Catégorie",
        yaxis_title="Bénéfice (USD)"
    )

    st.plotly_chart(
        fig_profit_category,
        use_container_width=True
    )


# ============================================================
# 10. TAUX DE RETOUR PAR CATÉGORIE
# ============================================================

st.subheader("Taux de retour par catégorie")


return_category = pd.crosstab(
    filtered_df["Product_Category"],
    filtered_df["Return_Status"],
    normalize="index"
).reset_index()


if "Returned" in return_category.columns:

    return_category["Return_Rate"] = (
        return_category["Returned"] * 100
    )

    return_category = return_category.sort_values(
        "Return_Rate",
        ascending=False
    )

    fig_return_rate = px.bar(
        return_category,
        x="Product_Category",
        y="Return_Rate",
        title="Taux de retour par catégorie",
        labels={
            "Product_Category": "Catégorie",
            "Return_Rate": "Taux de retour (%)"
        }
    )

    st.plotly_chart(
        fig_return_rate,
        use_container_width=True
    )


# ============================================================
# 11. INFORMATION SUR LES DONNÉES
# ============================================================

st.divider()

with st.expander("ℹ️ Informations sur les données"):

    st.write(
        f"Nombre total de lignes dans le dataset : "
        f"**{len(df):,}**"
    )

    st.write(
        f"Nombre de lignes après filtrage : "
        f"**{len(filtered_df):,}**"
    )

    st.write(
        f"Nombre de colonnes : "
        f"**{len(df.columns)}**"
    )

    # ============================================================
# STYLE DU DASHBOARD
# ============================================================

st.markdown("""
<style>

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 25px;
    }

    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 18px;
        border-radius: 12px;
    }

</style>
""", unsafe_allow_html=True)