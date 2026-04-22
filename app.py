import streamlit as st
import time
import random

st.set_page_config(page_title="Nutritionist Simulator", layout="centered")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "xp" not in st.session_state:
    st.session_state.xp = 0
    st.session_state.level = 1
    st.session_state.streak = 0

# -----------------------------
# FUNCTIONS
# -----------------------------
def add_xp(points):
    st.session_state.xp += points

    # Level up system
    if st.session_state.xp >= st.session_state.level * 100:
        st.session_state.level += 1
        st.success(f"🎉 LEVEL UP! You are now Level {st.session_state.level}")

def reset_game():
    st.session_state.xp = 0
    st.session_state.level = 1
    st.session_state.streak = 0

# -----------------------------
# SIDEBAR (PROFILE)
# -----------------------------
st.sidebar.title("🧑‍⚕️ Doctor Profile")
st.sidebar.write(f"⭐ Level: {st.session_state.level}")
st.sidebar.write(f"🔥 XP: {st.session_state.xp}")
st.sidebar.write(f"🏆 Streak: {st.session_state.streak}")
st.sidebar.progress((st.session_state.xp % 100) / 100)

if st.sidebar.button("🔄 Reset Progress"):
    reset_game()
    st.rerun()

# -----------------------------
# TITLE
# -----------------------------
st.title("🧑‍⚕️ Nutritionist Simulator")
st.write("Treat patients by building the correct diet plan!")

# -----------------------------
# PATIENTS
# -----------------------------
patients = {
    "Fatigue Student 😴": {"protein": 20, "carbs": 40, "fats": 10},
    "Athlete 🏃‍♂️": {"protein": 50, "carbs": 60, "fats": 20},
    "Overweight Patient ⚖️": {"protein": 30, "carbs": 30, "fats": 10},
    "Child Growth 👶": {"protein": 25, "carbs": 45, "fats": 15},
}

patient = st.selectbox("Select Patient:", list(patients.keys()))
target = patients[patient]

st.write("### 🧍 Patient Target Needs")
st.write(target)

# -----------------------------
# FOOD DATABASE
# -----------------------------
foods = {
    "Chicken 🐔": {"protein": 25, "carbs": 0, "fats": 5, "rarity": "common"},
    "Rice 🍚": {"protein": 4, "carbs": 45, "fats": 1, "rarity": "common"},
    "Egg 🥚": {"protein": 6, "carbs": 1, "fats": 5, "rarity": "common"},
    "Apple 🍎": {"protein": 0, "carbs": 25, "fats": 0, "rarity": "common"},
    "Broccoli 🥦": {"protein": 3, "carbs": 6, "fats": 0, "rarity": "rare"},
    "Nuts 🌰": {"protein": 5, "carbs": 5, "fats": 15, "rarity": "rare"},
    "Milk 🥛": {"protein": 8, "carbs": 12, "fats": 5, "rarity": "common"},
    "Salmon 🐟": {"protein": 30, "carbs": 0, "fats": 10, "rarity": "epic"},
}

# -----------------------------
# DIET BUILDER
# -----------------------------
st.write("## 🥗 Build Diet Plan")

selected = st.multiselect("Choose foods:", list(foods.keys()))

protein = sum(foods[f]["protein"] for f in selected)
carbs = sum(foods[f]["carbs"] for f in selected)
fats = sum(foods[f]["fats"] for f in selected)

st.write("### ⚖️ Nutrition Summary")
st.write(f"Protein: {protein}g")
st.write(f"Carbs: {carbs}g")
st.write(f"Fats: {fats}g")

# -----------------------------
# SCORE SYSTEM
# -----------------------------
diff = abs(target["protein"] - protein) + abs(target["carbs"] - carbs) + abs(target["fats"] - fats)
score = max(0, 100 - diff)

st.subheader("🏆 Treatment Score")
st.metric("Score", f"{int(score)}/100")
st.progress(score / 100)

# -----------------------------
# FEEDBACK SYSTEM
# -----------------------------
st.write("## 🧠 AI Feedback")

if score >= 80:
    st.success("Excellent treatment! Patient is recovering well 🟢")
    st.balloons()
    st.session_state.streak += 1
    add_xp(40)

elif score >= 50:
    st.warning("Good plan, but needs improvement 🟡")
    st.session_state.streak = 0
    add_xp(20)

else:
    st.error("Poor diet plan! Patient condition worsened 🔴")
    st.session_state.streak = 0
    add_xp(5)

# -----------------------------
# BADGES
# -----------------------------
st.write("## 🏅 Achievements")

if score >= 90:
    st.success("🏅 Badge Earned: Nutrition Master")
elif score >= 75:
    st.info("🏅 Badge Earned: Diet Specialist")
elif score >= 50:
    st.info("🏅 Badge Earned: Beginner Nutritionist")

# -----------------------------
# FOOD RARITY BONUS
# -----------------------------
rarity_xp = 0
for f in selected:
    if foods[f]["rarity"] == "rare":
        rarity_xp += 10
    elif foods[f]["rarity"] == "epic":
        rarity_xp += 25

if rarity_xp > 0:
    st.info(f"✨ Rare Food Bonus XP: +{rarity_xp}")
    add_xp(rarity_xp)

# -----------------------------
# STREAK DISPLAY
# -----------------------------
st.write(f"🔥 Current Streak: {st.session_state.streak}")
