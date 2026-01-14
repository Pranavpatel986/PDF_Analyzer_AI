# ui_config.py

custom_css = """
footer {visibility: hidden}
.gradio-container { background-color: #f8fafd !important; }

#side_panel {
    background-color: #f0f4f9;
    border-radius: 24px;
    padding: 20px;
    margin: 10px;
    border: none;
}

#chatbot {
    background: transparent !important;
    border: none !important;
}

/* User Message Bubble */
.message.user {
    background-color: #e9eef6 !important;
    border-radius: 20px !important;
    padding: 12px 20px !important;
    color: #1f1f1f !important;
}

/* Assistant Message */
.message.assistant {
    background-color: transparent !important;
    padding: 12px 0px !important;
}

#chat_input {
    border: 1px solid #747775 !important;
    border-radius: 28px !important;
    padding: 10px 20px !important;
    background: white !important;
}

.primary-btn { background: #0b57d0 !important; border-radius: 50px !important; color: white !important; }
.secondary-btn { border-radius: 50px !important; border: 1px solid #747775 !important; background: transparent !important; }
"""

hero_html = """
<div style="padding: 20px;">
    <h1 style="font-size: 2.8rem; font-weight: 400; color: #1f1f1f;">
        Hello, <span style="background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Knowledge Seeker</span>
    </h1>
    <p style="color: #444746; font-size: 1.2rem;">Ready to analyze your PDF documents with Gemini AI?</p>
</div>
"""