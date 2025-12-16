import streamlit as st

def show():
    # --- LAYOUT SETUP ---
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        
        # --- 1. TITEL & SUBTITEL ---
        st.write("") 
        st.markdown("<h1 style='text-align: center; font-size: 4em;'>Ito's Lemma</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: gray;'>Journal Review Group 8</h3>", unsafe_allow_html=True)
        
        st.divider()

        # --- 2. NAMES ---
        st.markdown("<p style='text-align: center; font-size: 1.2em; font-weight: bold;'>Presented by:</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.5em;'>Anton Jungbauer, Julian Baur, Leander Friedmann, Emil Höfer, Luca Russo, Abdoulie Njie</p>", unsafe_allow_html=True)
        
        st.write("") 
        st.write("") 

        # --- 3. THESIS ---
        st.info("### Core Thesis")
        st.markdown("""
        > The classical chain rule isn't working in the world of randomness.""")

        st.write("")
        st.divider()

        # --- 4. ABSTRACT ---
        st.header("Abstract")
        st.write("""This journal deals with the solution of stochastic differential equations using Ito's lemma.

It hypothesizes that the classical chain rule fails in the world of randomness. To confirm this hypothesis, the Taylor Series for deterministic and stochastic differential equations are compared. It can be seen that second-order terms are not negligible in the stochastic world. This justifies the mathematical identity (dX)^2 = dt, from which the Ito correction term arises. Finally, the hypothesis was validated using a Monte Carlo simulation. The results show that applying the classical chain rule leads to systematic errors.

This work concludes that the Ito lemma is an indispensable tool for solving stochastic differential equations.
        """)

        st.write("")
        st.write("")

        # --- 5. SOURCES ---

        with st.expander("References / Sources"):
            st.markdown("""
            * *https://math.nyu.edu/~goodman/teaching/StochCalc2018/notes/Lesson4.pdf*
            * *https://www.math.hu-berlin.de/~foellmer/papers/Gauss_Lecture.pdf*
            * *https://nzdr.ru/data/media/biblio/kolxoz/M/MV/MVspa/Oksendal%20B.%20Stochastic%20differential%20equations%20(5ed,%20Springer,%202000)(332s).pdf*
            * *https://www.cambridge.org/core/services/aop-cambridge-core/content/view/CA39C46B3829C055DBD1BF839BA0E140/S0027763000012216a.pdf/on_a_formula_concerning_stochastic_differentials.pdf*
            * *Thomas Beck: Der Itô-Kalkül ISBN-10 3-540-25392-0 Springer Berlin Heidelberg New York
                        
            * *Tool: Google Gemini pro*
            """)
            
        st.write("")

        st.caption("Project Presentation • 2026")
