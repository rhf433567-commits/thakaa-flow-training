
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Space Scale", page_icon="🪐")

st.title("🪐 Space Scale")
st.write("Discover how much you would weigh on other planets!")

GRAVITY = {
    "Mercury": 0.38,
    "Venus": 0.90,
    "Earth": 1.00,
    "Moon": 0.17,
    "Mars": 0.38,
    "Jupiter": 2.53,
    "Saturn": 1.07,
    "Uranus": 0.89,
    "Neptune": 1.14
}

earth_weight = st.number_input(
    "Your weight on Earth (kg)",
    min_value=1.0,
    max_value=500.0,
    value=60.0,
    step=1.0
)

planet = st.selectbox("Choose a planet", list(GRAVITY.keys()))

planet_weight = earth_weight * GRAVITY[planet]
delta = planet_weight - earth_weight

st.metric(
    f"Your weight on {planet}",
    f"{planet_weight:.2f} kg",
    delta=f"{delta:.2f} kg compared with Earth"
)

if planet_weight < earth_weight:
    jump_factor = earth_weight / planet_weight
    st.success(
        f"You weigh less here! You could jump about {jump_factor:.2f} times higher."
    )
elif planet_weight > earth_weight:
    st.warning("You weigh more here than on Earth!")
else:
    st.info("Your weight is the same as on Earth.")

chart_data = pd.DataFrame({
    "Planet": list(GRAVITY.keys()),
    "Weight (kg)": [
        earth_weight * gravity for gravity in GRAVITY.values()
    ]
}).set_index("Planet")

st.subheader("Weight on All Planets")
st.bar_chart(chart_data)
