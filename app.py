
import streamlit as st
import matplotlib.pyplot as plt
import math 
from buffon import buffon_needle_pi_with_data

st.title("Buffon's needle")

# sliders for adjustable metrics
line_spacing = st.slider('Line spacing (d)', 1.0, 5.0, 2.0, 0.5)
needle_length = st.slider('Needle length (l)', 0.5, line_spacing, min(1.0, line_spacing), 0.5)  # add line_spacing as a param so the needle_length can be <= to the spacing width
num_trials = st.slider("Number of trials", 1000, 100000, 10000, 1000)   # from 1000 trials to 100000 with a step of 1000

# set up buttons 
col1, col2 = st.columns(2)

estimate_clicked = col1.button('Estimate pi')
reset_clicked = col2.button('Reset')

if reset_clicked or 'pi_est' not in st.session_state:
    st.session_state.pi_est = None
    st.session_state.needles = []

num_lines = st.slider('Number of lines on the graph', 5, 20, 5, 1)  # fixed line count for simulation and visualization

needle_count = st.slider('Needle count on image', 50, 1000, 100, 50) # needle count on the image min=50, max=1000

# call the main calculation function from buffon.py
if estimate_clicked:
    st.session_state.pi_est, st.session_state.needles = buffon_needle_pi_with_data(num_trials, needle_length, line_spacing, num_lines=num_lines)

# display the error from the real pi value
if st.session_state.pi_est:
    st.metric("pi estimate", f"{st.session_state.pi_est:.8f}", f"{st.session_state.pi_est - math.pi:+.8f} error")


# draw the needle sim 
if st.checkbox('Show visualisation') and st.session_state.needles:
    needles = st.session_state.needles
    display = needles[:needle_count]

    board_size = num_lines * line_spacing
    margin = needle_length / 2 + 0.2  # padding so needle tips dont get cut off at borders

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.set_aspect('equal')  # apply true 1:1 physical scale

    for i in range(num_lines + 1):
        ax.axhline(i * line_spacing, color='orange', lw=1.5)

    for n in display:
        color = 'red' if n['crosses'] else 'limegreen'
        ax.plot([n['x1'], n['x2']], [n['y1'], n['y2']], color=color, lw=1)

    ax.set_xlim(-margin, board_size + margin)
    ax.set_ylim(-margin, board_size + margin)
    crossing_count = sum(1 for n in display if n['crosses'])
    ax.set_title(f"Needle simulation — {len(display)} shown, {crossing_count} cross a line (red)")
    st.pyplot(fig)
