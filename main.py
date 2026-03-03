import streamlit as st
import langchain_helper  # uses the function from langchain_helper.py

st.title("Restaurant Name Generator")

cuisine = st.sidebar.selectbox(
    "Pick a Cuisine",
    ("Indian", "Italian", "Mexican", "American")
)

if cuisine:
    # Call helper function
    response = langchain_helper.generate_restaurant_name_and_items(cuisine)

    # Show restaurant name FIRST
    st.header(response["restaurant_name"])

    # Menu items (this is already a list)
    st.write("**Menu Items**")
    for item in response["menu_items"]:
        st.write(f"- {item}")   # no extra commas
