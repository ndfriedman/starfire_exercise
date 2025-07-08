#written by Noah Friedman

import streamlit as st
from PIL import Image

def vertical_line_element():
	return """<div style="
	    display: flex;
	    justify-content: center;
	    margin-top: 10px;
	">
	 <div style="
		 width: 2px;
		 height: 50px;
		 background-color: black;
	  "></div>
    </div>
    """

def long_vertical_line_element():
	return """<div style="
	    display: flex;
	    justify-content: center;
	    margin-top: 10px;
	">
	 <div style="
		 width: 2px;
		 height: 300px;
		 background-color: black;
	  "></div>
    </div>
    """

def render_carousel(streamlitWriteColumn):
	# 1. Initialize the index exactly once
	if "idx" not in st.session_state:
		st.session_state.idx = 0

	# 2. Build three columns: prev-button, image, next-button
	prev_col, img_col, next_col = streamlitWriteColumn.columns([1, 8, 1])

	# 3. In the left column, bump the index backward
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")
	prev_col.write("")

	if prev_col.button("◀️", key="prev"):
		st.session_state.idx = (st.session_state.idx - 1) % len(st.session_state.plot_paths)

	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	next_col.write("")
	

	# 4. In the right column, bump the index forward
	if next_col.button("▶️", key="next"):
		st.session_state.idx = (st.session_state.idx + 1) % len(st.session_state.plot_paths)

	# 5. Finally, re-open and render the “current” image in the middle column
	print("the index is:", st.session_state.idx)
	current_img = Image.open(st.session_state.plot_paths[st.session_state.idx][0])
	img_col.image(
		current_img,
		use_column_width=True,
		caption=st.session_state.plot_paths[st.session_state.idx][1]
	)


