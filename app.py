import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Data Visualizer", page_icon="📊", layout="wide")

# Title
st.title("📊 Data to Graph Visualizer")
st.markdown("Upload your data and create beautiful interactive charts instantly!")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"✅ File uploaded! Found {len(df)} rows and {len(df.columns)} columns.")

        # Show data preview
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10))

        # Chart configuration
        st.subheader("🎨 Create Your Chart")

        col1, col2 = st.columns(2)

        with col1:
            chart_type = st.selectbox(
                "Chart Type",
                ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Area Chart", "Histogram"]
            )

        with col2:
            color_theme = st.selectbox(
                "Color Theme",
                ["plotly", "seaborn", "ggplot2", "viridis", "plasma"]
            )

        # Get numeric and categorical columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        all_cols = df.columns.tolist()

        if len(numeric_cols) == 0:
            st.warning("⚠️ No numeric columns found in your data!")
        else:
            # X and Y axis selection
            col3, col4 = st.columns(2)

            with col3:
                if chart_type == "Pie Chart":
                    x_axis = st.selectbox("Labels (Categories)", all_cols)
                else:
                    x_axis = st.selectbox("X-Axis", all_cols)

            with col4:
                if chart_type == "Histogram":
                    y_axis = None
                elif chart_type == "Pie Chart":
                    y_axis = st.selectbox("Values", numeric_cols)
                else:
                    y_axis = st.selectbox("Y-Axis", numeric_cols)

            # Optional: Color grouping
            if chart_type not in ["Pie Chart", "Histogram"]:
                color_by = st.selectbox("Color by (optional)", ["None"] + all_cols)
                if color_by == "None":
                    color_by = None
            else:
                color_by = None

            # Chart title
            chart_title = st.text_input("Chart Title", f"{chart_type} of {y_axis if y_axis else x_axis}")

            # Generate chart button
            if st.button("🚀 Generate Chart", type="primary"):
                try:
                    # Create the chart based on type
                    if chart_type == "Line Chart":
                        fig = px.line(df, x=x_axis, y=y_axis, color=color_by,
                                      title=chart_title,)

                    elif chart_type == "Bar Chart":
                        fig = px.bar(df, x=x_axis, y=y_axis, color=color_by,
                                     title=chart_title,)

                    elif chart_type == "Scatter Plot":
                        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by,
                                         title=chart_title,)

                    elif chart_type == "Pie Chart":
                        fig = px.pie(df, names=x_axis, values=y_axis,
                                     title=chart_title,)

                    elif chart_type == "Area Chart":
                        fig = px.area(df, x=x_axis, y=y_axis, color=color_by,
                                      title=chart_title)

                    elif chart_type == "Histogram":
                        fig = px.histogram(df, x=x_axis, color=color_by,
                                           title=chart_title)

                    # Make it interactive and nice
                    fig.update_layout(
                        hovermode='x unified',
                        height=600,
                        showlegend=True
                    )

                    # Display the chart
                    st.plotly_chart(fig, use_container_width=True)

                    # Download options
                    st.subheader("💾 Download Your Chart")

                    # Download button removed, just keep HTML
                    html_buffer = fig.to_html()
                    st.download_button(
                        label="📥 Download as Interactive HTML",
                        data=html_buffer,
                        file_name=f"{chart_title}.html",
                        mime="text/html"
                    )

                except Exception as e:
                    st.error(f"❌ Error creating chart: {str(e)}")
                    st.info("Try selecting different columns or chart type.")

    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        st.info("Make sure your file is a valid CSV or Excel format.")

else:
    st.info("👆 Upload a CSV or Excel file to get started!")

    # Example section
    st.markdown("---")
    st.subheader("What can you visualize?")

    col_ex1, col_ex2, col_ex3 = st.columns(3)

    with col_ex1:
        st.markdown("**📈 Sales Data**")
        st.markdown("Track revenue over time with line charts")

    with col_ex2:
        st.markdown("**📊 Comparisons**")
        st.markdown("Compare categories with bar charts")

    with col_ex3:
        st.markdown("**🎯 Distributions**")
        st.markdown("Analyze patterns with histograms")

    st.markdown("---")
    st.markdown("**Supported formats:** CSV, Excel (.xlsx, .xls)")
    st.markdown("**Chart types:** Line, Bar, Scatter, Pie, Area, Histogram")
    st.markdown("**Export options:** Interactive HTML or PNG image")

st.markdown("---")
