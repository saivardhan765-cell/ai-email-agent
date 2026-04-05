import streamlit as st
import time
import streamlit.components.v1 as components
from env import EmailEnv



# Initialize session
if "env" not in st.session_state:
    st.session_state.env = EmailEnv()
    st.session_state.obs = st.session_state.env.reset()
    st.session_state.done = False
    st.session_state.total_reward = 0
    st.session_state.step_done = False

env = st.session_state.env

st.set_page_config(page_title="AI Email Assistant")

st.title("📧 AI Email Assistant")

# 🎨 Animation CSS
st.markdown("""
<style>

.container {
    position: relative;
    height: 300px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.inner{
            position: absolute;
            width: 0;
            height: 0;
            border-left: 110px solid transparent;
            border-right: 110px solid transparent;
            border-top:70px solid #f4e2c9;
            top: 0;
            }

/* Envelope body */
.envelope {
    position: absolute;
    width: 200px;
    height: 120px;
    background: white;
    border: 2px solid black;
}

/* Top flap */
.top-flap {
    position: absolute;
    width: 0;
    height: 0;
    border-left: 100px solid transparent;
    border-right: 100px solid transparent;
    border-bottom: 60px solid white;
    top: -60px;
    transform-origin: bottom;
    animation: openFlap 0.8s forwards;
}

/* Side flaps */
.left-flap, .right-flap {
    position: absolute;
    width: 100px;
    height: 120px;
    background: white;
    top: 0;
    transform-origin: center;
    animation: openSide 0.8s forwards;
    animation-delay: 0.8s;
}

.left-flap {
    left: 0;
}

.right-flap {
    right: 0;
}

/* Bar emerging */
.bar {
    position: absolute;
    width: 6px;
    height: 0;
    background: black;
    top: 60px;
    animation: riseBar 0.8s forwards;
    animation-delay: 1.6s;
}

/* Move animation */
.move-left {
    animation: moveLeft 0.8s forwards;
    animation-delay: 2.4s;
}

.move-right {
    animation: moveRight 0.8s forwards;
    animation-delay: 2.4s;
}

/* Transform to horizontal bar */
.transform-bar {
    animation: transformBar 0.8s forwards;
    animation-delay: 3.2s;
}

/* Animations */

@keyframes openFlap {
    to { transform: rotateX(180deg); }
}

@keyframes openSide {
    to { transform: rotateY(90deg); }
}

@keyframes riseBar {
    to { height: 150px; }
}

@keyframes moveLeft {
    to { transform: translateX(-200px); }
}

@keyframes moveRight {
    to { transform: translateX(200px); }
}

@keyframes transformBar {
    to {
        width: 300px;
        height: 4px;
    }
}

</style>
""", unsafe_allow_html=True)
#email display
components.html("""
<!DOCTYPE html>
<html>
<head>
<style>

body {
    margin: 0;
    background: transparent;
}

/* Container */
.container {
    position: relative;
    height: 300px;
}

/* Envelope base */
.envelope {
    position: absolute;
    width: 220px;
    height: 140px;
    background: linear-gradient(145deg, #f4e2c9, #e8d3a8); /* paper colour */
    border: 2px solid #c9a66b;
    border-radius: 6px;
    left: 50%;
    top: 100px;
    transform: translateX(-50%);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3),inset 0 2px 5px rgba(255,255,255,0.4),inset 0 -3px 6px rgba(0,0,0,0.15);
    overflow: visible;
    transition: all 0.5s ease;
}

                
            

/* Top flap (triangle) */
.flap {
    position: absolute;
    width: 0;
    height: 0;

    border-left: 110px solid transparent;
    border-right: 110px solid transparent;
    border-bottom: 70px solid #f1d8a6; /* slightly darker */

    top: -70px;
    left: 0;

    transform-origin: bottom;

    filter: drop-shadow(0 3px 4px rgba(0,0,0,0.2));

    animation: openFlap 1s forwards;
}
.envelope::before {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;

    background: linear-gradient(
        to bottom right,
        transparent 49%,
        rgba(0,0,0,0.1) 50%,
        transparent 51%
    );

    pointer-events: none;
}

.envelope::after {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;

    background: linear-gradient(
        to bottom left,
        transparent 49%,
        rgba(0,0,0,0.1) 50%,
        transparent 51%
    );

    pointer-events: none;
}

/* Inner letter (bar) */
.letter {
    position: absolute;
    width: 6px;
    height: 0;
    background: black;
    left: 50%;
    transform: translateX(-50%);
    top: 70px;
    animation: rise 1s forwards 1s;
}

/* Move animations */
.move-left {
    animation: moveLeft 1s forwards 2.5s;
}

.move-right {
    animation: moveRight 1s forwards 2.5s, expand 1s forwards 3.5s;
}

/* Animations */

@keyframes openFlap {
    0% { transform: rotateX(0deg); }
    100% { transform: rotateX(180deg); }
}

@keyframes rise {
    0% { height: 0; }
    100% { height: 150px; }
}

@keyframes moveLeft {
    100% { transform: translateX(-300px); }
}

@keyframes moveRight {
    100% { transform: translateX(300px); }
}

@keyframes expand {
    100% {
        width: 300px;
        height: 4px;
    }
}

</style>
</head>

<body>

<div class="container">

    <div class="envelope move-left">
    <div class="flap"></div>
    <div class="inner"></div>   <!-- ADD THIS LINE -->
</div>

    <div class="letter move-right"></div>

</div>

</body>
</html>
""", height=320)
#time contolling
time.sleep(4)

if st.session_state.obs:
    st.markdown(
        f"<h3 style='text-align:center;'>📩 {st.session_state.obs}</h3>",
        unsafe_allow_html=True
    )

# 🤖 Run AI (only once per step)
if not st.session_state.done and not st.session_state.step_done:

    st.write("🤖 AI is thinking...")
    time.sleep(1.5)

    email=st.session_state.obs.lower() if st.session_state.obs else ""
    
st.write("🤖 AI is thinking...")
time.sleep(1.5)

try:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Classify the email into Important or Promotions. Only return one word."},
            {"role": "user", "content": email}
        ]
    )

    action = response.choices[0].message.content.strip()

except Exception as e:
    st.warning("⚠️ API failed, using fallback AI")

    # 🔥 Fallback logic
    email = st.session_state.obs.lower() if st.session_state.obs else ""
    if any(word in email for word in ["discount", "sale", "offer", "deal"]):
        action = "Promotions"
    elif any(word in email for word in ["interview", "meeting", "deadline"]):
        action = "Important"
    else:
        action = "Important"

st.session_state.action = action
email = st.session_state.obs.lower() if st.session_state.obs else ""

# 🟡 Priority detection
if any(word in email for word in ["interview", "meeting", "deadline"]):
    priority = "High"
else:
    priority = "Low"

# 🟢 Reply generation
if "interview" in email:
    reply = "Thank you, I will attend."
elif any(word in email for word in ["discount", "sale", "offer"]):
    reply = "Not interested."
else:
    reply = "Okay"
env.priority=priority
env.reply=reply

# Save to session
st.session_state.priority = priority
st.session_state.reply = reply
st.session_state.step_done = True
# 🧠 Show AI output
if "action" in st.session_state:
    if "action" in st.session_state:
        st.write(f"🤖 AI chose: **{st.session_state.action}**")

        st.write(f"📌 Priority: **{st.session_state.priority}**")
        st.write(f"💬 Suggested Reply: **{st.session_state.reply}**")
        st.markdown(f"""
        ### 🧠 AI Reasoning

        - Detected keywords in the email  
        - Classified it as **{st.session_state.action}**  
        - Assigned priority **{priority}** based on urgency  
        - Generated reply based on context  

  """)

    
# ▶️ Next button
if st.session_state.step_done and not st.session_state.done:

    if st.button("Next ➡️"):

        obs, reward, done, _ = env.step(st.session_state.action)

        st.session_state.total_reward += reward
        st.session_state.done = done
        st.session_state.obs = obs
        st.session_state.step_done = False

        if reward == 1.0:
            st.success("✅ Correct")
        else:
            st.error("❌ Wrong")

        st.write(f"Reward: {reward}")
        if env.index < len(env.tasks):
           task = env.tasks[env.index]

           # show email
           st.write(task["email"])

           # reward display
           st.write(f"Reward: {reward}")

           # ✅ reward reasoning (SAFE now)
           st.markdown(f"""
           ### 📊 Evaluation Breakdown

           - Classification: {"✅" if st.session_state.action == task["category"] else "❌"}
           - Priority: {"✅" if priority == task["priority"] else "❌"}
           - Reply Quality: {"⚠️" if reply.lower() in ["ok", "okay"] else "✅"}
           ℹ️ Evaluation is based on matching AI output with predefined expected answers.

           **Final Score: {round(reward,2)}**
        """)

        else:


            st.success("🎉 All emails processed!")
            st.write(f"Final Score: {st.session_state.total_reward}")

        time.sleep(1)
        st.rerun()
#final screen
if st.session_state.done:
    st.success("🎉 All emails processed!")
    st.write(f"Final Score: {st.session_state.total_reward}")

    if st.button("Restart"):
        st.session_state.env = EmailEnv()
        st.session_state.obs = st.session_state.env.reset()
        st.session_state.done = False
        st.session_state.total_reward = 0
        st.session_state.step_done = False
        st.rerun()