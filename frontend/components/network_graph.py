import plotly.graph_objects as go
import numpy as np

# Professional palette matching the app theme
NODE_COLORS = {
    'Compound':  '#63b3ed',   # blue
    'Disease':   '#fc8181',   # red/coral
    'Gene':      '#68d391',   # green
    'Anatomy':   '#f6e05e',   # gold
    'Pathway':   '#b794f4',   # purple
    'Biological Process': '#4fd1c5',
    'Cellular Component': '#f687b3',
    'Molecular Function': '#fbd38d',
    'default':   '#a0aec0',   # grey for unknown
}

def _get_node_color(kind: str) -> str:
    return NODE_COLORS.get(kind, NODE_COLORS['default'])


def _spring_layout_2d(nodes: list, edges: list) -> dict:
    """Simple deterministic circular layout for ego graph."""
    pos = {}
    n = len(nodes)
    if n == 0:
        return pos
    # Center node at origin, others in circle
    center_id = nodes[0]['id']
    pos[center_id] = (0.0, 0.0)
    angle_step = 2 * np.pi / max(n - 1, 1)
    for i, node in enumerate(nodes[1:]):
        angle = i * angle_step
        r = 1.0 + 0.3 * (i % 3)   # stagger radius for readability
        pos[node['id']] = (r * np.cos(angle), r * np.sin(angle))
    return pos


def _spring_layout_3d(nodes: list, edges: list) -> dict:
    """Spherical layout for 3D view."""
    pos = {}
    n = len(nodes)
    if n == 0:
        return pos
    center_id = nodes[0]['id']
    pos[center_id] = (0.0, 0.0, 0.0)
    angle_step = 2 * np.pi / max(n - 1, 1)
    for i, node in enumerate(nodes[1:]):
        angle = i * angle_step
        phi = np.pi * (i + 1) / max(n, 2)
        r = 1.0 + 0.25 * (i % 3)
        pos[node['id']] = (
            r * np.sin(phi) * np.cos(angle),
            r * np.sin(phi) * np.sin(angle),
            r * np.cos(phi)
        )
    return pos


def create_2d_network(nodes: list, edges: list, title: str = "Node Connections") -> go.Figure:
    """Render an interactive 2D ego-graph using Plotly Scatter traces."""
    if not nodes:
        fig = go.Figure()
        fig.update_layout(title="No data to display")
        return fig

    pos = _spring_layout_2d(nodes, edges)
    node_index = {n['id']: n for n in nodes}

    # ── Edge traces ──
    edge_x, edge_y = [], []
    for e in edges:
        src = pos.get(e.get('source', ''))
        tgt = pos.get(e.get('target', ''))
        if src and tgt:
            edge_x += [src[0], tgt[0], None]
            edge_y += [src[1], tgt[1], None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y, mode='lines',
        line=dict(width=1.2, color='rgba(160,174,192,0.35)'),
        hoverinfo='none', showlegend=False
    )

    # ── Node traces per kind for legend ──
    kind_groups: dict[str, list] = {}
    for node in nodes:
        k = node.get('kind', 'default')
        kind_groups.setdefault(k, []).append(node)

    node_traces = []
    for kind, group in kind_groups.items():
        xs = [pos[n['id']][0] for n in group if n['id'] in pos]
        ys = [pos[n['id']][1] for n in group if n['id'] in pos]
        texts = [n.get('name', n['id']) for n in group if n['id'] in pos]
        hover = [
            f"<b>{n.get('name', n['id'])}</b><br>Type: {kind}<br>ID: {n['id']}"
            for n in group if n['id'] in pos
        ]
        sizes = [18 if i == 0 else 10 for i, n in enumerate(group)]
        node_traces.append(go.Scatter(
            x=xs, y=ys, mode='markers+text',
            marker=dict(size=sizes, color=_get_node_color(kind),
                        line=dict(width=1.5, color='rgba(255,255,255,0.3)')),
            text=texts,
            textposition='top center',
            textfont=dict(size=9, color='#f0f4f8'),
            hovertext=hover, hoverinfo='text',
            name=kind, legendgroup=kind
        ))

    fig = go.Figure(data=[edge_trace] + node_traces)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#f0f4f8', family='Inter')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f0f4f8', family='Roboto, sans-serif'),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        legend=dict(
            orientation='v', x=1.02, y=1,
            bgcolor='rgba(30,32,41,0.8)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(size=11, color='#a0aec0')
        ),
        hovermode='closest',
        margin=dict(l=10, r=120, t=50, b=10),
        height=500,
    )
    return fig


def create_3d_network(nodes: list, edges: list, title: str = "3D Node Graph") -> go.Figure:
    """Render an interactive 3D ego-graph using Plotly Scatter3d."""
    if not nodes:
        fig = go.Figure()
        fig.update_layout(title="No data to display")
        return fig

    pos = _spring_layout_3d(nodes, edges)

    # ── Edge traces ──
    ex, ey, ez = [], [], []
    for e in edges:
        src = pos.get(e.get('source', ''))
        tgt = pos.get(e.get('target', ''))
        if src and tgt:
            ex += [src[0], tgt[0], None]
            ey += [src[1], tgt[1], None]
            ez += [src[2], tgt[2], None]

    edge_trace = go.Scatter3d(
        x=ex, y=ey, z=ez, mode='lines',
        line=dict(width=1.5, color='rgba(160,174,192,0.3)'),
        hoverinfo='none', showlegend=False
    )

    # ── Node traces per kind ──
    kind_groups: dict[str, list] = {}
    for node in nodes:
        k = node.get('kind', 'default')
        kind_groups.setdefault(k, []).append(node)

    node_traces = []
    for kind, group in kind_groups.items():
        xs = [pos[n['id']][0] for n in group if n['id'] in pos]
        ys = [pos[n['id']][1] for n in group if n['id'] in pos]
        zs = [pos[n['id']][2] for n in group if n['id'] in pos]
        hover = [
            f"<b>{n.get('name', n['id'])}</b><br>Type: {kind}<br>ID: {n['id']}"
            for n in group if n['id'] in pos
        ]
        sizes = [14 if i == 0 else 7 for i, n in enumerate(group)]
        node_traces.append(go.Scatter3d(
            x=xs, y=ys, z=zs, mode='markers',
            marker=dict(size=sizes, color=_get_node_color(kind),
                        line=dict(width=1, color='rgba(255,255,255,0.2)'),
                        opacity=0.9),
            hovertext=hover, hoverinfo='text',
            name=kind, legendgroup=kind
        ))

    fig = go.Figure(data=[edge_trace] + node_traces)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#f0f4f8', family='Inter')),
        paper_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            bgcolor='rgba(15,17,23,1)',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                       backgroundcolor='rgba(0,0,0,0)'),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                       backgroundcolor='rgba(0,0,0,0)'),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                       backgroundcolor='rgba(0,0,0,0)'),
        ),
        legend=dict(
            font=dict(size=11, color='#a0aec0'),
            bgcolor='rgba(30,32,41,0.8)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        height=520,
    )
    return fig
