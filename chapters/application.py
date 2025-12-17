import streamlit as st
import numpy as np
import plotly.graph_objects as go

def show():
    # --- LAYOUT SETUP ---
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.markdown("<h1 style='text-align: center;'>Visualisation and conclusion</h1>", unsafe_allow_html=True)
        st.write("")
        st.divider()

        # ==========================================
        # 1. VISUAL INTUITION (FULL TEXT)
        # ==========================================
        st.header("1. Intuiton for stochastic chain rule")
        
        st.write("""
        At first we need to understand why the deterministic approach fails with stochastic.
        """)

        st.subheader("Coastline ")
        st.write("""Imagine you have a high end microscope and you zoom in  at a coastline. 
        * **The Rough World (Coastline):** From far away it looks like a smooth line. If you zoom in on a coastline, you see bays. If you zoom further, you see rocks. Further? Grains of sand... It's the same with a stock price. 
        
                 """)

        st.info("Info to remember: A derivative is nothing else then the change of f at a certain ``point´´ x. ")

        # --- DATA GENERATION ---
        n_points = 50000
        t = np.linspace(0, 1, n_points) 
        
        # 1. Smooth (Sine Wave)
        y_smooth = np.sin(t * 5) + 100 
        
        # 2. Rough (Geometric Brownian Motion)
        dt = t[1] - t[0]
        np.random.seed(42) 
        random_shocks = np.random.normal(0, np.sqrt(dt), n_points)
        y_rough = 100 * np.exp(np.cumsum(random_shocks))

        # --- CHARTS ---
        col_plot1, col_plot2 = st.columns(2)

        with col_plot1:
            st.markdown("**A) Deterministic**")
            fig1 = go.Figure()
            fig1.add_trace(go.Scattergl(x=t, y=y_smooth, mode='lines', line=dict(color='#007AFF', width=2), name='Smooth'))
            fig1.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), template="plotly_white", xaxis_title="Time", yaxis_title="Value")
            st.plotly_chart(fig1) 
            st.write("**Zoom Effect:** It becomes a straight line.")

        with col_plot2:
            st.markdown("**B) Stochastic**")
            fig2 = go.Figure()
            fig2.add_trace(go.Scattergl(x=t, y=y_rough, mode='lines', line=dict(color='#ff4b4b', width=1), name='Rough'))
            fig2.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), template="plotly_white", xaxis_title="Time", yaxis_title="Price ($)")
            st.plotly_chart(fig2) 
            st.write("**Zoom Effect:** It never gets straight.")

        st.divider()

        # ==========================================
        # 2. INTERACTIVE PROOF (SIMULATION)
        # ==========================================
        st.header("2. Interactive Proof (Monte Carlo)")
        st.caption("Simulation: 1 Year (360 days) | Start: $100 | 50000 Paths")

        # --- PRESETS ---
        if 'mu_val' not in st.session_state: st.session_state.mu_val = 0.08
        if 'sigma_val' not in st.session_state: st.session_state.sigma_val = 0.15

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("MSCI World"):
                st.session_state.mu_val, st.session_state.sigma_val = 0.08, 0.15
        with b2:
            if st.button("NVIDIA"):
                st.session_state.mu_val, st.session_state.sigma_val = 0.45, 0.55
        with b3:
            if st.button("Dogecoin"):
                st.session_state.mu_val, st.session_state.sigma_val = 1.20, 1.80

        # --- SLIDERS ---
        c1, c2 = st.columns(2)
        with c1:
            mu_input = st.slider(r"Drift ($\mu$)", -0.9, 3.0, key='mu_val', format="%.2f")
        with c2:
            sigma_input = st.slider(r"Volatility ($\sigma$)", 0.01, 4.0, key='sigma_val', format="%.2f")

        # --- CALCULATION ---
        S0, days, dt, N_SIM = 100.0, 360, 1/252, 50000
        t_vec = np.linspace(0, 1, days).reshape(-1, 1)
        
        # Paths
        random_shocks = np.random.normal(0, np.sqrt(dt), (days, N_SIM))
        W = np.cumsum(random_shocks, axis=0)
        
        # Calculate individual paths for the "Cloud" and Histogram
        ito_paths = S0 * np.exp((mu_input - 0.5 * sigma_input**2) * t_vec + sigma_input * W)
        
        # Averages (Lines)
        naive_mean = np.mean(S0 * np.exp(mu_input * t_vec + sigma_input * W), axis=1)
        ito_mean = np.mean(ito_paths, axis=1)
        target = S0 * np.exp(mu_input * np.linspace(0, 1, days))

        # --- CHART 1: PATHS OVER TIME ---
        fig = go.Figure()
        
        # 1. The Cloud
        for i in range(50):
            fig.add_trace(go.Scatter(y=ito_paths[:, i], mode='lines', line=dict(color='lightgrey', width=0.5), opacity=0.1, showlegend=False, hoverinfo='skip'))

        # 2. Target - BLUE DASHED
        fig.add_trace(go.Scatter(y=target, mode='lines', name='Target (Correct mean)', 
                                line=dict(color='#0055ff', width=3, dash='dash')))
        
        # 3. Naive - RED SOLID
        fig.add_trace(go.Scatter(y=naive_mean, mode='lines', name='Naive Prediction (deterministic)', 
                                line=dict(color='#ff4b4b', width=4)))
        
        # 4. Ito - GREEN SOLID
        fig.add_trace(go.Scatter(y=ito_mean, mode='lines', name='With Itô correction', 
                                line=dict(color='#00cc44', width=4)))

        fig.update_layout(xaxis_title="Days", yaxis_title="Price ($)", 
                          template="plotly_white", height=450, 
                          legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        st.plotly_chart(fig)

        # --- RESULTS METRICS ---
        end_target = target[-1]
        end_naive = naive_mean[-1]
        end_ito = ito_mean[-1]

        m1, m2, m3 = st.columns(3)
        m1.metric("Target Price", f"${end_target:.2f}")
        m2.metric("Naive Model", f"${end_naive:.2f}")
        m3.metric("Ito Model", f"${end_ito:.2f}")

        st.write("")
        err_col1, err_col2 = st.columns(2)
        
        with err_col1:
            st.markdown("##### :red[Naive Error (Naive vs Target)]")
            diff = end_naive - end_target
            st.write(f"Overestimation: **+${diff:.2f}**")

        with err_col2:
            st.markdown("##### :green[Ito Accuracy (Ito vs Target)]")
            diff = end_ito - end_target
            st.write(f"Difference: **${diff:.2f}**")

        # --- NEW CHART 2: DISTRIBUTION (LOG-NORMAL) ---
        st.write("")
        st.subheader("Distribution of Outcomes")
        st.caption("Where do the 50000 paths actually end up?")

        # End values of all simulations
        final_values = ito_paths[-1, :]
        
        # Statistics
        val_classical = S0 * np.exp(mu_input * 1.0) # The theoretical "Red Line" value
        val_ito_median = np.median(final_values)    # The realistic "Green Line" center
        
        fig_dist = go.Figure()
        
        # Histogram
        fig_dist.add_trace(go.Histogram(
            x=final_values,
            nbinsx=100,
            marker_color='lightgrey',
            name='Simulated Outcomes',
            opacity=0.7
        ))

        # Red Line (Classical Expectation)
        fig_dist.add_vline(x=val_classical, line_width=4, line_dash="dash", line_color="#ff4b4b")
        fig_dist.add_annotation(x=val_classical, y=0.95, yref="paper", text="Classical Exp. (Wrong)", 
                                showarrow=False, font=dict(color="#ff4b4b"))

        # Green Line (Ito Median/Reality)
        fig_dist.add_vline(x=val_ito_median, line_width=4, line_color="#00cc44")
        fig_dist.add_annotation(x=val_ito_median, y=1.05, yref="paper", text="Median (Reality)", 
                                showarrow=False, font=dict(color="#00cc44"))

        # Cut off extreme outliers for visibility
        cutoff = np.percentile(final_values, 96)
        cutoff = max(cutoff, val_classical * 1.2)
        
        fig_dist.update_layout(
            xaxis_title="Final Price ($)", 
            yaxis_title="Number of paths", 
            template="plotly_white", 
            height=400,
            xaxis_range=[0, cutoff],
            showlegend=False
        )
        st.plotly_chart(fig_dist)

        st.divider()

        # ==========================================
        # 3. DEEP DIVE: VOLATILITY DRAG (EXPANDED, NO SYMBOLS)
        # ==========================================
        st.header("3. Deep Dive: The Volatility Drag")
        st.write("""
        The naive prediction (Red) consistently overestimates the result. 
        This is not a random error. It is a systematic cost of volatility, known as the "Volatility Drag".
        """)

        st.subheader("A) Why averages lie")
        st.write("Consider a simple investment example starting at **$100**.")

        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            st.markdown("**Scenario 1: No Volatility**")
            st.write("Year 1: 0%")
            st.write("Year 2: 0%")
            st.metric("Final Value", "$100")
            st.caption("Arithmetic Average: 0%")

        with col_ex2:
            st.markdown("**Scenario 2: High Volatility**")
            st.write("Year 1: +50% ($150)")
            st.write("Year 2: -50% ($75)")
            st.metric("Final Value", "$75", delta="-25%", delta_color="inverse")
            st.caption("Arithmetic Average: 0%")

        st.warning("""
        Both scenarios have an arithmetic average return of **0%**. 
        However, the volatile scenario results in a **25% loss**. 
        Standard calculus (Naive Model) only sees the average of 0%. Ito calculus sees the loss and his additional term corrects it.
        """)

        st.write("")

        st.subheader("B) The Correction Formula")
        st.write("Ito's Lemma provides the mathematical correction term to adjust the expected growth rate.")
        
        st.latex(r'''
        \text{Real Growth} = \text{Average Return} - \frac{1}{2}\sigma^2
        ''')

        st.write("The term $\\frac{1}{2}\\sigma^2$ represents the energy that is lost due to market fluctuations.")

        st.divider()

        # ==========================================
        # 4. THE THESIS ANSWERED (MATH & CONCLUSION)
        # ==========================================
        st.header("4. Conclusion")
        st.write("Comparing the rules of calculus:")

        col_class, col_ito = st.columns(2)

        with col_class:
            st.markdown("##### :red[Classical Chain Rule]")
            
            # Simplified first
            st.caption("**1. Simplified Notation**")
            st.latex(r'''df = f_t \cdot dt + f_x \cdot dx''')

            # Formal second
            st.caption("**2. Formal Notation**")
            st.latex(r'''df = \frac{\partial f}{\partial t} dt + \frac{\partial f}{\partial x} dx''')
            
            st.error("Linear Approximation (**Wrong**)")

        with col_ito:
            st.markdown("##### :green[Stochastic Chain Rule (Ito)]")
            
            # Simplified first
            st.caption("**1. Simplified Notation**")
            st.latex(r'''df = f_t \cdot dt + f_x \cdot dx + \textcolor{red}{\frac{1}{2} f_{xx} (dx)^2}''')
            
            # Formal second
            st.caption("**2. Formal Notation**")
            st.latex(r'''df = \frac{\partial f}{\partial t} dt + \frac{\partial f}{\partial x} dx + \textcolor{red}{\frac{1}{2} \frac{\partial^2 f}{\partial x^2} (dx)^2}''')
            
            st.success("Convex Correction (**Correct**)")

        # --- FAZIT ---
        st.write("")
        st.markdown("### Final Conclusion")
        st.success("""
        **Thesis Confirmed:** The classical chain rule isn't working in the world of randomness.  **Correct!**
        
        Because markets are rough and not smooth, we cannot use simple derivatives.
        We have to use Itô's Lemma and have to subtract the "energy" of volatility ($1/2 \sigma^2$). 
        Without this correction, every financial model would overestimate profits and underestimate risk.

        """)

