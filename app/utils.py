import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    """Check if file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file_path, file_type):
    """Read and process uploaded file"""
    try:
        if file_type == 'csv':
            df = pd.read_csv(file_path)
        else:  # excel
            df = pd.read_excel(file_path)
        return df
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def generate_dashboard_data(file_path, file_type):
    """Generate dashboard data including summary statistics and visualizations"""
    df = process_file(file_path, file_type)
    
    # Data summary
    data_summary = {
        'rows': len(df),
        'columns': len(df.columns),
        'column_names': df.columns.tolist(),
        'data_types': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'head': df.head(10).to_dict('records')
    }
    
    # Generate visualizations
    charts = []
    
    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Chart 1: Summary statistics for numeric columns
    if numeric_cols:
        stats_df = df[numeric_cols].describe().round(2)
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Statistic'] + numeric_cols,
                       fill_color='paleturquoise',
                       align='left'),
            cells=dict(values=[stats_df.index] + [stats_df[col] for col in numeric_cols],
                      fill_color='lavender',
                      align='left'))
        ])
        fig.update_layout(title='Summary Statistics for Numeric Columns', height=400)
        charts.append({
            'title': 'Summary Statistics',
            'json': json.dumps(fig, cls=PlotlyJSONEncoder)
        })
    
    # Chart 2: Distribution of first numeric column (histogram)
    if len(numeric_cols) > 0:
        col = numeric_cols[0]
        fig = px.histogram(df, x=col, title=f'Distribution of {col}', 
                          color_discrete_sequence=['#636EFA'])
        fig.update_layout(height=400)
        charts.append({
            'title': f'Distribution of {col}',
            'json': json.dumps(fig, cls=PlotlyJSONEncoder)
        })
    
    # Chart 3: Bar chart for first categorical column
    if len(categorical_cols) > 0:
        col = categorical_cols[0]
        value_counts = df[col].value_counts().head(10)
        fig = px.bar(x=value_counts.index, y=value_counts.values,
                    title=f'Top 10 Values in {col}',
                    labels={'x': col, 'y': 'Count'},
                    color_discrete_sequence=['#EF553B'])
        fig.update_layout(height=400)
        charts.append({
            'title': f'Top Values in {col}',
            'json': json.dumps(fig, cls=PlotlyJSONEncoder)
        })
    
    # Chart 4: Correlation heatmap for numeric columns
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        fig = px.imshow(corr_matrix,
                       text_auto=True,
                       aspect='auto',
                       title='Correlation Heatmap',
                       color_continuous_scale='RdBu_r')
        fig.update_layout(height=500)
        charts.append({
            'title': 'Correlation Heatmap',
            'json': json.dumps(fig, cls=PlotlyJSONEncoder)
        })
    
    # Chart 5: Scatter plot for first two numeric columns
    if len(numeric_cols) >= 2:
        col1, col2 = numeric_cols[0], numeric_cols[1]
        fig = px.scatter(df, x=col1, y=col2,
                        title=f'{col1} vs {col2}',
                        color_discrete_sequence=['#00CC96'])
        fig.update_layout(height=400)
        charts.append({
            'title': f'{col1} vs {col2}',
            'json': json.dumps(fig, cls=PlotlyJSONEncoder)
        })
    
    # Chart 6: Box plot for numeric columns
    if len(numeric_cols) > 0:
        # Select first 5 numeric columns for box plot
        cols_to_plot = numeric_cols[:5]
        fig = go.Figure()
        for col in cols_to_plot:
            fig.add_trace(go.Box(y=df[col], name=col))
        fig.update_layout(title='Box Plot of Numeric Columns', 
                         yaxis_title='Value',
                         height=400)
        charts.append({
            'title': 'Box Plot',
            'json': json.dumps(fig, cls=PlotlyJSONEncoder)
        })
    
    return data_summary, charts
