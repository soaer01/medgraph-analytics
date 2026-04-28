import streamlit as st

def render_particles():
    """Inject a lightweight canvas-based floating molecule particle system.
    
    Particles start fast (simulating page transition acceleration) and 
    decelerate to a calm ambient speed over 2 seconds after page load.
    """
    particle_html = """
    <canvas id="medgraph-particles"></canvas>
    <script>
    (function() {
        const canvas = document.getElementById('medgraph-particles');
        if (!canvas || canvas.dataset.init) return;
        canvas.dataset.init = '1';
        const ctx = canvas.getContext('2d');
        
        let W, H;
        function resize() {
            W = canvas.width = window.innerWidth;
            H = canvas.height = window.innerHeight;
        }
        resize();
        window.addEventListener('resize', resize);

        const COLORS = ['#00f0ff', '#ff00e5', '#39ff14', '#d500f9', '#ffea00'];
        const NUM = 60;
        const CONNECT_DIST = 130;
        const BASE_SPEED = 0.3;
        
        // Speed multiplier: starts high (burst), decays to 1.0
        let speedMult = 5.0;
        const DECAY_RATE = 0.97; // per frame

        const particles = [];
        for (let i = 0; i < NUM; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = (0.2 + Math.random() * 0.5);
            particles.push({
                x: Math.random() * W,
                y: Math.random() * H,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                r: 1.5 + Math.random() * 2,
                color: COLORS[Math.floor(Math.random() * COLORS.length)],
                alpha: 0.4 + Math.random() * 0.5
            });
        }

        function draw() {
            ctx.clearRect(0, 0, W, H);

            // Decelerate toward base speed
            if (speedMult > 1.02) {
                speedMult *= DECAY_RATE;
            } else {
                speedMult = 1.0;
            }

            // Update positions
            for (const p of particles) {
                p.x += p.vx * BASE_SPEED * speedMult;
                p.y += p.vy * BASE_SPEED * speedMult;

                // Wrap around edges
                if (p.x < 0) p.x = W;
                if (p.x > W) p.x = 0;
                if (p.y < 0) p.y = H;
                if (p.y > H) p.y = 0;
            }

            // Draw connection lines
            for (let i = 0; i < NUM; i++) {
                for (let j = i + 1; j < NUM; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < CONNECT_DIST) {
                        const alpha = (1 - dist / CONNECT_DIST) * 0.25;
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = `rgba(0, 240, 255, ${alpha})`;
                        ctx.lineWidth = 0.6;
                        ctx.stroke();
                    }
                }
            }

            // Draw particles
            for (const p of particles) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.alpha;
                ctx.fill();
                
                // Glow halo
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r * 3, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.alpha * 0.08;
                ctx.fill();
                
                ctx.globalAlpha = 1;
            }

            requestAnimationFrame(draw);
        }
        draw();
    })();
    </script>
    """
    st.components.v1.html(particle_html, height=0, scrolling=False)
