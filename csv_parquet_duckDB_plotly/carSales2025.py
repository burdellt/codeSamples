import duckdb
import pandas as pd
import plotly.graph_objects as go
import os
import webbrowser

# Get current working directory
path = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(os.getcwd(), 'carSales')

# Create DuckDB in-memory connection
con = duckdb.connect(database=':memory:')

# Create duckDB query to convert CSV records to partitioned parquet
query = f"SELECT id, firstName, lastName, email, gender, carYear + 10 as automobileYear, automobileMake, automobileModel, customerRegion, customerState, customerPostal, customerCountry_ISO2, customerRegionLatitude, ownerRegionLongitude, automobilePrice, customer, purchaseDate, YEAR(purchaseDate) as purchaseYear FROM read_csv_auto('{output_path}/csvFiles/*.csv', HEADER=TRUE)"

# Check if parquet file exists, if not create it
if not os.path.exists(f'{output_path}/carSales.parquet'):
    con.execute(f"COPY ({query}) TO '{output_path}/carSales.parquet' (FORMAT PARQUET, PARTITION_BY ('purchaseYear'), COMPRESSION 'SNAPPY')")

# Query carsales for 2025 revenue by automobile make and customer region into Pandas df
df = con.execute(f"""
    SELECT 
        date_trunc('month', purchaseDate) AS purchaseMonth,
        automobileMake,
        customerState,
        customerRegion,
        SUM(automobilePrice) AS Revenue
    FROM read_parquet('{output_path}/carSales.parquet')
    where purchaseYear = 2025
    GROUP BY 1, 2, 3, 4;
""").fetchdf()

# Format purchaseMonth as YYYY-MM
df['purchaseMonth'] = pd.to_datetime(df['purchaseMonth']).dt.strftime('%Y-%m')

# Create pivot table
pivot_df = pd.pivot_table(
    df,
    index=['automobileMake','customerState'],
    columns='purchaseMonth',
    values='Revenue',
    aggfunc='sum',
    fill_value=0
)


# Create plotly Crosstab
fig = go.Figure(data=[go.Table(
    header=dict(values=['Automobile Make', 'Customer State'] + list(pivot_df.columns),
                fill_color='black',
                font_color='white',
                line_color='black',
                align='left'),
    cells=dict(values=[pivot_df.index.get_level_values(0), pivot_df.index.get_level_values(1)] + [pivot_df[col].apply(lambda x: f'${x:,.0f}') for col in pivot_df.columns],
               fill_color='white',
               align='left',
               line_color='black')
)])

fig.update_layout(title='Monthly Automobile Revenue by Make', height=600)
                                                                           
# Create HTML file for rendering crosstab
fig.write_html(f'{output_path}/revenue_report.html')

# Open browser window with output
webbrowser.open(f'{output_path}/revenue_report.html')


 
