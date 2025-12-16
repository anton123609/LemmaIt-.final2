import streamlit as st

def show():
    # --- LAYOUT SETUP ---
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        
        # --- HERO SECTION ---
        st.markdown("<h1 style='text-align: center; font-size: 3.5em;'>Ito's Lemma</h1>", unsafe_allow_html=True)
        
        st.write("") 
        
        # --- Original formula ---
        st.markdown("<p style='text-align: center; font-weight: bold;'>Formula:</p>", unsafe_allow_html=True)
        st.latex(r'''
        df(t, X_t) = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial x} + \frac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial x^2} \right) dt + \sigma \frac{\partial f}{\partial x} dW_t
        ''')
        
        st.divider()

        # --- THESIS ---
        st.error("### Thesis: The classical chain rule isn't working in the world of randomness. ")
        
        st.write("")

        # --- THE PURPOSE ---
        st.info("### Solving the Unsolvable")
        
        st.markdown("""
        **Why do we need Itôs Lemma?**
        * To solve stochastic differential equations.
        * To correct the the volatility drag.
        * Fundamental for many financial models (e.g. Black-Scholes).
        * To modell Monte-Carlo-simulations and stochastic processes in general correctly.
        """)

        st.divider()
        
        # --- NOTATION ---
        st.subheader("Simplification with substitution")
        st.write("""
        To make it more understandable, 
        we will strictly use the Simplified Notation throughout this presentation and we will resubstitute in the end.
        """)
            # Legend
        st.info("Legend:")
        st.markdown("""
        * $f_t$: Change with **Time** - Partial derivative of f to t.
        * $f_x$: Change with **Price** - Partial derivative of f to x.
        * $f_{xx}$: The **Curvature** - Second partial derivative of f to x.
        """)
        
        st.write("Simplified version:")
        
        st.latex(r'''
        df = \left( f_t + \mu f_x + \frac{1}{2} \sigma^2 f_{xx} \right) dt + \sigma f_x dW
        ''')
 
        st.caption("We trade academic complexity ($\partial$) for visual clarity ($f_t$).")
        
        st.divider()

        # --- STEP 1: CLASSICAL CHAIN RULE ---
        st.header("1. The Classical Chain Rule for differential equations with two variables (Deterministic)")
        
        st.write("""
        If you have a function $f(t, x)$, 
        the total change $df$ is simply the sum of changes in time and space.
        """)

        st.latex(r'''
        df = f_t \cdot dt + f_x \cdot dx
        ''')

        st.write("") 

        # --- STEP 2: TAYLOR Series ---
        st.header("2. Taylor Series for differential equations with two variables")
        st.write("""
        Derivatives may be portrayed as a infinite expansion with higher orders.
        """)

        # Tylor Series up to 3. order
        st.latex(r'''
        df = \underbrace{f_t dt + f_x dx}_{\text{1st Order}} 
        + \underbrace{\frac{1}{2} f_{xx} (dx)^2}_{\text{2nd Order}}
        + \underbrace{\frac{1}{6} f_{xxx} (dx)^3}_{\text{3rd Order}}
        + \dots
        ''')

        # Why unimportant
        st.warning("""
        **Why standard Calculus ignores the tail:**
        
        In standard math, $dx$ represents an infinitely small step (limit to 0).
        If $dx$ is tiny (e.g. $0.001$), look what happens to higher powers:
        
        * $(dx)^1 = 0.001$ (Small)
        * $(dx)^2 = 0.000001$ (Tiny)
        * $(dx)^3 = 0.000000001$ (Smaller then tiny)
        
        **Conclusion:** In the deterministic world, anything with $(dx)^2$ or higher vanishes to "zero" because the change is almost 0 and negligible. 
        That is why the Classical Chain Rule (Step 1) stops after the 1st Order.
        """)

        st.write("")

        # --- STEP 3: THE PROCESS ---
        st.header("3. Stochastic differential equation")
        
        st.write("We define our variable $X_t$ by the following Stochastic Differential Equation (SDE):")

        # Differential equation
        st.latex(r'''
        dX_t = \underbrace{\mu \cdot dt}_{\text{The Drift}} + \underbrace{\sigma \cdot dW_t}_{\text{The Diffusion}}
        ''')
        
        st.write("")
        
        # --- Comparison ---
        col_drift, col_diff = st.columns(2)
        
        with col_drift:
            st.info("**1. The Drift Term** ($\mu \cdot dt$)")
            st.markdown("""
            **What it represents:**
            The deterministic trend or expected return.
            
            **What it does:**
            It pushes the mean steadily in one direction (the mean drifts away).
            It is predictable and depends only on time $dt$.
            """)
        with col_diff:
            st.warning("**2. The Diffusion Term** ($\sigma \cdot dW_t$)")
            st.markdown("""
            **What it represents:**
            The stochastic volatility or risk.
            
            **What it does:**
            It scatters the value randomly around the trend. 
            Because of the **Brownian Motion ($dW$)**, this term creates the "wiggle" and makes the exact future price unpredictable.
            """)
        
        st.divider()

        st.caption("Swipe to next chapter >")
