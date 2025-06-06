from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

app = Flask(__name__)

def load_data():
    df = pd.read_csv("WHO-COVID-19-global-data.csv")
    df['Date_reported'] = pd.to_datetime(df['Date_reported'])
    numeric_cols = ['New_cases', 'Cumulative_cases', 'New_deaths', 'Cumulative_deaths']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df.fillna(0, inplace=True)
    return df

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    df = load_data()
    current_viz = request.form.get('viz_type', '1') if request.method == 'POST' else '1'
    
    # Set common layout parameters
    layout = {
        'height': 800,
        'margin': {'l': 50, 'r': 50, 'b': 100, 't': 100, 'pad': 4},
        'hovermode': 'x unified',
        'xaxis': {'fixedrange': False},  # Enable zoom on x-axis
        'yaxis': {'fixedrange': False},  # Enable zoom on y-axis
        'legend': {'orientation': 'h', 'y': -0.2}
    }
    
    if current_viz == "1":
        # Global Trend
        data = df.groupby("Date_reported")[['Cumulative_cases', 'Cumulative_deaths']].sum().reset_index()
        fig = px.line(data, x='Date_reported', y=['Cumulative_cases', 'Cumulative_deaths'],
                     title='<b>Global COVID-19 Cases Trend</b>')
        fig.update_layout(**layout)
        
    elif current_viz == "2":
        # Top Countries
        data = df.groupby("Country")[['Cumulative_cases', 'Cumulative_deaths']].sum()\
               .nlargest(10, 'Cumulative_cases').reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data['Country'], y=data['Cumulative_cases'], name='Cases'))
        fig.add_trace(go.Bar(x=data['Country'], y=data['Cumulative_deaths'], name='Deaths'))
        fig.update_layout(title='<b>Top 10 Countries by COVID-19 Cases & Deaths</b>',
                         barmode='group', **layout)
        
    elif current_viz == "3":
        # Daily Cases
        data = df.groupby("Date_reported")['New_cases'].sum().reset_index()
        fig = px.line(data, x='Date_reported', y='New_cases',
                     title='<b>Daily New COVID-19 Cases Trend</b>')
        fig.update_layout(**layout)
        
    elif current_viz == "4":
        # Heatmap
        data = df.groupby("Country")['Cumulative_cases'].sum().nlargest(20).reset_index()
        fig = px.treemap(data, path=['Country'], values='Cumulative_cases',
                        title='<b>COVID-19 Cases Distribution</b>')
        fig.update_layout(**layout)
        
    elif current_viz == "5":
        # Pie Chart
        data = df.groupby("Country")['Cumulative_cases'].sum().nlargest(5).reset_index()
        fig = px.pie(data, values='Cumulative_cases', names='Country',
                    title='<b>Top 5 Countries with Highest COVID-19 Cases</b>')
        fig.update_layout(height=800)
        
    elif current_viz == "7":
        # Full Data Table
        return render_template('dashboard.html', 
                            current_viz=current_viz,
                            table_data=df.to_dict('records'),
                            columns=df.columns.tolist())
    
    return render_template('dashboard.html',
                         current_viz=current_viz,
                         chart_html=fig.to_html(full_html=False, config={'displayModeBar': True}))

if __name__ == '__main__':
    app.run(debug=True, port=5000)