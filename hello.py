from preswald import connect, get_df, query, table, text, plotly
import plotly.express as px
import pandas as pd

connect()  

file_path = "data/education.csv"
sql_data_alias = "education_data_table"
df = get_df(file_path) 

text("# Cost of International Education Insights")
text("An interactive app to explore and visualize the costs associated with studying abroad. "
     "The dataset covers tuition, living expenses, rent, and other costs across various countries, "
     "cities, universities, programs, and degree levels.")

text("## Visual Insights into International Education Costs")


if df is not None and not df.empty:
    text("### Distribution of Living Cost Index by Degree Level")
    text("Understand the spread and median of living cost indices for Undergraduate, Master's, and PhD")
    try:
        df_plot1 = df.copy()
        if 'Living_Cost_Index' in df_plot1.columns:
            df_plot1['Living_Cost_Index'] = pd.to_numeric(df_plot1['Living_Cost_Index'], errors='coerce')
        
        df_plot1 = df_plot1.dropna(subset=['Level', 'Living_Cost_Index'])
        
        if not df_plot1.empty:
            fig_box = px.box(df_plot1,
                          x="Level",
                          y="Living_Cost_Index",
                          color="Level",
                          title="Distribution of Living Cost Index by Degree Level",
                          labels={"Level": "Degree Level", "Living_Cost_Index": "Living Cost Index"}) 
            plotly(fig_box)
        else:
                text("Not enough valid data")
    except Exception as e:
        text(f"Could not generate Plot 1 (Box Plot - Living Cost by Degree Level): {e}")
    

    text("### Tuition Fees (USD) vs. Living Cost Index by Country")
    text("Explore the relationship between tuition fees (in USD) and the living cost index, "
         "with data points colored by country.")
    try:
        df_plot2 = df.copy() 
        if 'Tuition_USD' in df_plot2.columns:
            df_plot2['Tuition_USD'] = pd.to_numeric(df_plot2['Tuition_USD'], errors='coerce')
        
        if 'Living_Cost_Index' in df_plot2.columns:
            df_plot2['Living_Cost_Index'] = pd.to_numeric(df_plot2['Living_Cost_Index'], errors='coerce')

        df_scatter = df_plot2.dropna(subset=['Tuition_USD', 'Living_Cost_Index', 'Country'])

        if not df_scatter.empty:
            fig_scatter = px.scatter(df_scatter,
                                     x="Tuition_USD", 
                                     y="Living_Cost_Index",
                                     color="Country", 
                                     title="Tuition Fees (USD) vs. Living Cost Index by Country",
                                     labels={"Tuition_USD": "Tuition Fee (USD)", 
                                             "Living_Cost_Index": "Living Cost Index",
                                             "Country": "Country"}, 
                                     hover_data=['City', 'University', 'Level', 'Program', 'Duration_Years']
                                    )
            fig_scatter.update_layout(
                template='plotly_white',
                xaxis_title="Tuition Fee (USD)", 
                yaxis_title="Living Cost Index",
                margin=dict(l=80, r=20, t=50, b=50),
                legend_title_text='Country' 
            )
            
            plotly(fig_scatter)
        else:
            text("Not enough valid data")
    except Exception as e:
        text(f"Could not generate Plot 2 (Scatter Plot - Tuition vs. Living Cost): {e}")
    

    text("### Average Tuition Fee (USD) by Country")
    text("Compare the average tuition fees across different countries.")
    try:
        df_plot3 = df.copy()

        if 'Tuition_USD' in df_plot3.columns:
            df_plot3['Tuition_USD'] = pd.to_numeric(df_plot3['Tuition_USD'], errors='coerce')
        
        df_avg_tuition_filtered = df_plot3.dropna(subset=['Country', 'Tuition_USD']) 
        if not df_avg_tuition_filtered.empty:
            df_avg_tuition_grouped = df_avg_tuition_filtered.groupby('Country')['Tuition_USD'].mean().reset_index()
            df_avg_tuition_grouped = df_avg_tuition_grouped.sort_values(by='Tuition_USD', ascending=False)

            if not df_avg_tuition_grouped.empty:
                fig_bar_avg_tuition = px.bar(df_avg_tuition_grouped,
                                             x="Country",
                                             y="Tuition_USD",
                                             title="Average Tuition Fee (USD) by Country",
                                             labels={"Country": "Country", "Tuition_USD": "Average Tuition Fee (USD)"},
                                             color="Country", 
                                             text_auto=True 
                                             )
                fig_bar_avg_tuition.update_layout(
                    template='plotly_white',
                    xaxis_title="Country",
                    yaxis_title="Average Tuition Fee (USD)",
                    margin=dict(l=80, r=20, t=50, b=100) 
                )
                fig_bar_avg_tuition.update_xaxes(tickangle=45) 

                plotly(fig_bar_avg_tuition)
            else:
                text("Not enough valid data")
        else:
            text("Not enough valid data")

    except Exception as e:
        text(f"Could not generate Plot 3 (Bar Chart - Average Tuition by Country): {e}")

else:
    text("The DataFrame could not be loaded or is empty. Please check the data source and path.")