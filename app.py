
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(
    page_title="Loan Dashboard",
    page_icon="🏦",
    layout="wide"
)

# عنوان التطبيق
st.title("🏦 Loan Applications Dashboard")
st.write("Interactive dashboard to analyze loan applications and approval rates.")

# قراءة البيانات
@st.cache_data
def load_data():
    return pd.read_csv("loan_clean.csv")

df = load_data()

# الشريط الجانبي والفلاتر
st.sidebar.header("Filters")

property_options = sorted(df["Property_Area"].dropna().unique())

selected_property = st.sidebar.multiselect(
    "Property Area",
    property_options,
    default=property_options
)

education_options = ["All"] + sorted(df["Education"].dropna().unique().tolist())

selected_education = st.sidebar.radio(
    "Education",
    education_options
)

max_income = int(df["ApplicantIncome"].max())

income_limit = st.sidebar.slider(
    "Maximum Applicant Income",
    min_value=0,
    max_value=max_income,
    value=max_income
)

# تطبيق الفلاتر
filtered_df = df[
    (df["Property_Area"].isin(selected_property)) &
    (df["ApplicantIncome"] <= income_limit)
]

if selected_education != "All":
    filtered_df = filtered_df[
        filtered_df["Education"] == selected_education
    ]

st.subheader("Key Metrics")

if filtered_df.empty:
    st.warning("No applications match the selected filters.")
else:
    total_applications = len(filtered_df)
    approval_rate = filtered_df["Loan_Status"].mean() * 100
    median_loan = filtered_df["LoanAmount"].median()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Applications", f"{total_applications:,}")
    col2.metric("Approval Rate", f"{approval_rate:.2f}%")
    col3.metric("Median Loan Amount", f"{median_loan:.2f}")

    # الرسوم البيانية
    st.subheader("Data Visualizations")

    chart1, chart2 = st.columns(2)

    with chart1:
        st.write("### Loan Applications by Property Area")
        fig1, ax1 = plt.subplots()
        sns.countplot(
            data=filtered_df,
            x="Property_Area",
            hue="Property_Area",
            legend=False,
            ax=ax1
        )
        ax1.set_xlabel("Property Area")
        ax1.set_ylabel("Number of Applications")
        st.pyplot(fig1)
        plt.close(fig1)

    with chart2:
        st.write("### Loan Amount Distribution")
        fig2, ax2 = plt.subplots()
        sns.histplot(
            data=filtered_df,
            x="LoanAmount",
            kde=True,
            ax=ax2
        )
        ax2.set_xlabel("Loan Amount")
        ax2.set_ylabel("Frequency")
        st.pyplot(fig2)
        plt.close(fig2)

    # اختيار عمود رقمي
    st.subheader("Explore Numeric Columns")

    numeric_columns = filtered_df.select_dtypes(
        include="number"
    ).columns.tolist()

    selected_column = st.selectbox(
        "Select a numeric column",
        numeric_columns
    )

    fig3, ax3 = plt.subplots()
    sns.histplot(
        data=filtered_df,
        x=selected_column,
        kde=True,
        ax=ax3
    )
    ax3.set_title(f"Distribution of {selected_column}")
    st.pyplot(fig3)
    plt.close(fig3)

    # جدول البيانات
    with st.expander("View Filtered Data"):
        st.dataframe(filtered_df, use_container_width=True)
