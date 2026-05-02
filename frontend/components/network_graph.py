import plotly.graph_objects as go
import numpy as np

# Neon palette matching the futuristic theme
NODE_COLORS = {
    'Compound':  '#00d4ff',   # neon cyan
    'Disease':   '#ff4081',   # neon pink-red
    'Gene':      '#39ff14',   # neon green
    'Anatomy':   '#ffea00',   # neon yellow
    'Pathway':   '#d500f9',   # neon purple
    'Biological Process': '#00e5ff',
    'Cellular Component': '#ff80ab',
    'Molecular Function': '#ffab40',
    'default':   '#b0bec5',
}

# Neon glow border color for all nodes
GLOW_COLOR = 'rgba(0,240,255,0.8)'
GLOW_COLOR_3D = 'rgba(0,240,255,0.7)'
EDGE_COLOR = 'rgba(0,240,255,0.18)'
EDGE_COLOR_3D = 'rgba(0,240,255,0.15)'

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


def create_2d_network(nodes: list, edges: list, title: str = "Node Connections", focus_ids: list = None) -> go.Figure:
    """Render an interactive 2D ego-graph with neon glowing nodes.
    
    If focus_ids is provided, edges connected to these nodes will be colored 
    with the respective node's color for visual distinction.
    """
    if not nodes:
        fig = go.Figure()
        fig.update_layout(title="No data to display")
        return fig

    pos = _spring_layout_2d(nodes, edges)
    node_index = {n['id']: n for n in nodes}

    # ── Edge traces (categorized by focus) ──
    edge_traces = []
    
    # Define focus color mapping
    focus_map = {}
    if focus_ids:
        for fid in focus_ids:
            # Find node kind to get color
            node = next((n for n in nodes if n['id'] == fid), None)
            if node:
                focus_map[fid] = _get_node_color(node.get('kind', 'default'))

    # Group edges
    # Category: 'default', or node_id of a focus node
    edge_groups = {'default': {'x': [], 'y': []}}
    for fid in focus_map:
        edge_groups[fid] = {'x': [], 'y': []}

    for e in edges:
        s_id = e.get('source', '')
        t_id = e.get('target', '')
        src = pos.get(s_id)
        tgt = pos.get(t_id)
        
        if src and tgt:
            # Assign to group
            if s_id in focus_map:
                group = s_id
            elif t_id in focus_map:
                group = t_id
            else:
                group = 'default'
            
            edge_groups[group]['x'] += [src[0], tgt[0], None]
            edge_groups[group]['y'] += [src[1], tgt[1], None]

    # Create traces
    for group, data in edge_groups.items():
        if not data['x']:
            continue
            
        color = focus_map.get(group, EDGE_COLOR)
        opacity = 0.6 if group != 'default' else 0.18
        width = 1.6 if group != 'default' else 1.0
        
        edge_traces.append(go.Scatter(
            x=data['x'], y=data['y'], mode='lines',
            line=dict(width=width, color=color),
            opacity=opacity,
            hoverinfo='none', showlegend=False
        ))

    # ── Node traces per kind for legend ──
    kind_groups: dict[str, list] = {}
    for node in nodes:
        k = node.get('kind', 'default')
        kind_groups.setdefault(k, []).append(node)

    node_traces = []
    glow_traces = []  # Glow halos behind nodes

    for kind, group in kind_groups.items():
        xs = [pos[n['id']][0] for n in group if n['id'] in pos]
        ys = [pos[n['id']][1] for n in group if n['id'] in pos]
        texts = [n.get('name', n['id']) for n in group if n['id'] in pos]
        hover = [
            f"<b>{n.get('name', n['id'])}</b><br>Type: {kind}<br>ID: {n['id']}"
            for n in group if n['id'] in pos
        ]
        sizes = [20 if i == 0 else 11 for i, n in enumerate(group)]

        # Glow halo trace (behind)
        glow_sizes = [s + 10 for s in sizes]
        glow_traces.append(go.Scatter(
            x=xs, y=ys, mode='markers',
            marker=dict(
                size=glow_sizes,
                color=_get_node_color(kind),
                opacity=0.12,
                line=dict(width=0)
            ),
            hoverinfo='none', showlegend=False
        ))

        # Main node trace
        node_traces.append(go.Scatter(
            x=xs, y=ys, mode='markers+text',
            marker=dict(
                size=sizes,
                color=_get_node_color(kind),
                line=dict(width=2.5, color=GLOW_COLOR),
                opacity=0.95,
            ),
            text=texts,
            textposition='top center',
            textfont=dict(size=9, color='#e8ecf4'),
            hovertext=hover, hoverinfo='text',
            name=kind, legendgroup=kind
        ))

    fig = go.Figure(data=edge_traces + glow_traces + node_traces)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#e8ecf4', family='Inter')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8ecf4', family='Roboto, sans-serif'),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        legend=dict(
            orientation='v', x=1.02, y=1,
            bgcolor='rgba(15,18,28,0.85)',
            bordercolor='rgba(0,240,255,0.15)',
            borderwidth=1,
            font=dict(size=11, color='#8896ab')
        ),
        hovermode='closest',
        margin=dict(l=10, r=120, t=50, b=10),
        height=500,
    )
    return fig


def create_3d_network(nodes: list, edges: list, title: str = "3D Node Graph") -> go.Figure:
    """Render an interactive 3D ego-graph with neon glowing nodes and auto-rotation.
    
    The graph auto-rotates via Plotly animation frames (orbital camera).
    User can click/drag to stop and take manual control.
    """
    import math

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
        line=dict(width=2, color=EDGE_COLOR_3D),
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
        sizes = [16 if i == 0 else 8 for i, n in enumerate(group)]
        node_traces.append(go.Scatter3d(
            x=xs, y=ys, z=zs, mode='markers',
            marker=dict(
                size=sizes,
                color=_get_node_color(kind),
                line=dict(width=2.5, color=GLOW_COLOR_3D),
                opacity=0.92
            ),
            hovertext=hover, hoverinfo='text',
            name=kind, legendgroup=kind
        ))

    fig = go.Figure(data=[edge_trace] + node_traces)

    # ── Auto-rotation: 72 frames for smooth 360° orbital camera ──
    frames = []
    for i in range(72):
        angle = i * 5 * (math.pi / 180)
        eye = dict(x=2.2 * math.cos(angle), y=2.2 * math.sin(angle), z=0.8)
        frames.append(go.Frame(
            layout=dict(scene_camera=dict(eye=eye)),
            name=str(i)
        ))
    fig.frames = frames

    fig.update_layout(
        title=None,
        paper_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            bgcolor='rgba(10,12,20,1)',
            camera=dict(eye=dict(x=2.2, y=0, z=0.8)),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                       backgroundcolor='rgba(0,0,0,0)'),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                       backgroundcolor='rgba(0,0,0,0)'),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                       backgroundcolor='rgba(0,0,0,0)'),
        ),
        legend=dict(
            font=dict(size=11, color='#8896ab'),
            bgcolor='rgba(15,18,28,0.85)',
            bordercolor='rgba(0,240,255,0.15)',
            borderwidth=1
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=500,
        autosize=True,
        # Auto-play rotation animation
        updatemenus=[dict(
            type="buttons", showactive=False, visible=False,
            x=0, y=0, xanchor="left", yanchor="bottom",
            buttons=[dict(
                label="",
                method="animate",
                args=[None, {
                    "frame": {"duration": 100, "redraw": True},
                    "fromcurrent": True,
                    "transition": {"duration": 0},
                    "mode": "immediate"
                }]
            )]
        )]
    )
    fig.update_scenes(aspectmode='cube')
    return fig
