import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Neon Palette
COLORS = {
    'bg': 'rgba(0,0,0,0)',
    'text': '#e8ecf4',
    'text_muted': '#8896ab',
    'accent': '#00f0ff',
    'accent_green': '#39ff14',
    'accent_coral': '#ff4081',
    'grid': 'rgba(0,240,255,0.05)',
    'palette': ['#00f0ff', '#39ff14', '#ff4081', '#ffea00', '#d500f9', '#00e5ff']
}

def apply_theme(fig):
    """Apply the neon dark theme to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor=COLORS['bg'],
        plot_bgcolor=COLORS['bg'],
        font=dict(color=COLORS['text'], family="Inter, Roboto, sans-serif", size=13),
        xaxis=dict(
            gridcolor=COLORS['grid'], zerolinecolor=COLORS['grid'],
            title_font=dict(size=12, color=COLORS['text_muted']),
            tickfont=dict(size=11, color=COLORS['text_muted'])
        ),
        yaxis=dict(
            gridcolor=COLORS['grid'], zerolinecolor=COLORS['grid'],
            title_font=dict(size=12, color=COLORS['text_muted']),
            tickfont=dict(size=11, color=COLORS['text_muted'])
        ),
        legend=dict(
            font=dict(size=12, color=COLORS['text_muted']),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=50, r=30, t=50, b=50),
        title_font=dict(size=16, color=COLORS['text'], family="Inter, sans-serif"),
        hoverlabel=dict(
            bgcolor='#12151f',
            font_size=13,
            font_family="Roboto, sans-serif",
            font_color=COLORS['text'],
            bordercolor='rgba(0,240,255,0.3)'
        )
    )
    return fig

def create_model_comparison_chart(metrics_data):
    df = pd.DataFrame(metrics_data)
    fig = px.bar(
        df, x='Metric', y='Score', color='Model', barmode='group',
        color_discrete_sequence=COLORS['palette']
    )
    fig.update_layout(
        title="Model Performance Comparison",
        yaxis_range=[0.7, 1.0],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_traces(marker_line_width=0)
    return apply_theme(fig)

def create_feature_importance_chart(importance_data):
    df = pd.DataFrame(importance_data).head(13)
    df = df.sort_values('importance_score', ascending=True)
    
    fig = go.Figure(go.Bar(
        x=df['importance_score'],
        y=df['feature'],
        orientation='h',
        marker=dict(
            color=df['importance_score'],
            colorscale=[[0, '#0a1628'], [0.3, '#00f0ff'], [0.7, '#39ff14'], [1, '#d500f9']],
            showscale=False,
            line=dict(width=1, color='rgba(0,240,255,0.3)')
        )
    ))
    fig.update_layout(
        title="Feature Importances (Random Forest)",
        xaxis_title="Importance Score",
        yaxis_title="",
        height=420
    )
    return apply_theme(fig)

def create_distribution_chart(data, metric_name):
    fig = go.Figure(data=[go.Bar(
        x=data['bin_edges'][:-1], y=data['counts'],
        marker_color=COLORS['accent'],
        marker_line_width=0,
        opacity=0.85,
    )])
    fig.update_layout(
        title=f"{metric_name.replace('_', ' ').title()} — Distribution",
        xaxis_title=metric_name.replace('_', ' ').title(),
        yaxis_title="Frequency (Log)",
        yaxis_type="log",
        height=400
    )
    return apply_theme(fig)

def create_gauge_chart(probability):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        number={'suffix': '%', 'font': {'size': 40, 'color': COLORS['text'], 'family': 'Orbitron, Inter, sans-serif'}},
        title={'text': "Repurposing Confidence", 'font': {'size': 16, 'color': COLORS['text_muted']}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': COLORS['text_muted'],
                     'tickfont': {'color': COLORS['text_muted']}},
            'bar': {'color': COLORS['accent']},
            'bgcolor': 'rgba(0,240,255,0.03)',
            'borderwidth': 1,
            'bordercolor': 'rgba(0,240,255,0.15)',
            'steps': [
                {'range': [0, 40], 'color': 'rgba(255, 64, 129, 0.12)'},
                {'range': [40, 70], 'color': 'rgba(255, 234, 0, 0.08)'},
                {'range': [70, 100], 'color': 'rgba(57, 255, 20, 0.12)'}
            ],
        }
    ))
    fig.update_layout(height=280)
    return apply_theme(fig)

def create_donut_chart(data_dict, title):
    labels = list(data_dict.keys())
    values = list(data_dict.values())
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=.45,
        marker=dict(
            colors=COLORS['palette'],
            line=dict(color='rgba(0,240,255,0.2)', width=2)
        ),
        textfont=dict(size=12, color=COLORS['text']),
        hoverinfo='label+percent+value'
    )])
    fig.update_layout(title=title, height=400)
    return apply_theme(fig)
