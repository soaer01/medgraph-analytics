import streamlit as st
import base64
import os

def render_particles():
    """Inject:
    1. Animated Ken Burns background image (base64-encoded, z-index:-2)
    2. Floating molecule particle canvas (z-index:-1)
    
    Particles start fast (simulating page transition) and decelerate
    to calm ambient speed over ~2 seconds.
    """
    # Load background image as base64
    bg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "bg_medgraph.png")
    bg_b64 = ""
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as f:
            bg_b64 = base64.b64encode(f.read()).decode()

    bg_style = ""
    if bg_b64:
        bg_style = f"""
        <style>
        .medgraph-bg {{
            position: fixed;
            top: -5%; left: -5%;
            width: 110%; height: 110%;
            background-image: url('data:image/png;base64,{bg_b64}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            animation: kenBurnsBg 30s ease-in-out infinite;
            opacity: 0.10;
            z-index: -2;
            pointer-events: none;
        }}
        @keyframes kenBurnsBg {{
            0%   {{ transform: scale(1.0) translate(0, 0); }}
            25%  {{ transform: scale(1.08) translate(-1%, -0.5%); }}
            50%  {{ transform: scale(1.05) translate(0.5%, 1%); }}
            75%  {{ transform: scale(1.1) translate(-0.5%, -1%); }}
            100% {{ transform: scale(1.0) translate(0, 0); }}
        }}
        </style>
        <div class="medgraph-bg"></div>
        """

    particle_html = f"""
    {bg_style}
    <canvas id="medgraph-particles"></canvas>
    <script>
    (function() {{
        const canvas = document.getElementById('medgraph-particles');
        if (!canvas || canvas.dataset.init) return;
        canvas.dataset.init = '1';
        const ctx = canvas.getContext('2d');
        
        let W, H;
        function resize() {{
            W = canvas.width = window.innerWidth;
            H = canvas.height = window.innerHeight;
        }}
        resize();
        window.addEventListener('resize', resize);

        const COLORS = ['#00f0ff', '#ff00e5', '#39ff14', '#d500f9', '#ffea00'];
        const NUM = 60;
        const CONNECT_DIST = 130;
        const BASE_SPEED = 0.3;
        
        // Speed multiplier: starts high (burst), decays to 1.0
        let speedMult = 5.0;
        const DECAY_RATE = 0.97;

        const particles = [];
        for (let i = 0; i < NUM; i++) {{
            const angle = Math.random() * Math.PI * 2;
            const speed = (0.2 + Math.random() * 0.5);
            particles.push({{
                x: Math.random() * W,
                y: Math.random() * H,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                r: 1.5 + Math.random() * 2,
                color: COLORS[Math.floor(Math.random() * COLORS.length)],
                alpha: 0.4 + Math.random() * 0.5
            }});
        }}

        function draw() {{
            ctx.clearRect(0, 0, W, H);

            if (speedMult > 1.02) {{
                speedMult *= DECAY_RATE;
            }} else {{
                speedMult = 1.0;
            }}

            for (const p of particles) {{
                p.x += p.vx * BASE_SPEED * speedMult;
                p.y += p.vy * BASE_SPEED * speedMult;
                if (p.x < 0) p.x = W;
                if (p.x > W) p.x = 0;
                if (p.y < 0) p.y = H;
                if (p.y > H) p.y = 0;
            }}

            for (let i = 0; i < NUM; i++) {{
                for (let j = i + 1; j < NUM; j++) {{
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < CONNECT_DIST) {{
                        const alpha = (1 - dist / CONNECT_DIST) * 0.25;
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = `rgba(0, 240, 255, ${{alpha}})`;
                        ctx.lineWidth = 0.6;
                        ctx.stroke();
                    }}
                }}
            }}

            for (const p of particles) {{
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.alpha;
                ctx.fill();
                
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r * 3, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.alpha * 0.08;
                ctx.fill();
                
                ctx.globalAlpha = 1;
            }}

            requestAnimationFrame(draw);
        }}
        draw();
    }})();
    </script>
    """
    st.components.v1.html(particle_html, height=0, scrolling=False)
