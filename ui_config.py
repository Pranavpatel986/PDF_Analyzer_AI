# ui_config.py

custom_css = """
footer {visibility: hidden}
.gradio-container {
    background: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), 
                url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1920&q=80');
    background-size: cover;
    background-attachment: fixed;
}
.hero-content {
    margin-top: 60px;
    margin-left: 40px;
    max-width: 600px;
    color: #064e3b;
    animation: fadeIn 1s ease-out;
}
#floating_container {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 420px;
    height: 620px;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.4);
    overflow: hidden;
    z-index: 1000;
    animation: slideUp 0.6s ease-out;
}
.widget-header {
    background: linear-gradient(90deg, #059669, #10b981);
    color: white;
    padding: 18px 25px;
    font-size: 1.25rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 12px;
}
#min_button {
    max-width: 40px;
    background: rgba(255,255,255,0.2);
    border: none;
    color: white;
    font-weight: bold;
    cursor: pointer;
}
#open_chat_btn {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 1001;
    border-radius: 50px;
    padding: 15px 25px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    background: #10b981;
    color: white;
    font-weight: bold;
}
@keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@media (max-width: 1000px) {
    .hero-content { display: none; }
    #floating_container { width: 100%; height: 100%; bottom: 0; right: 0; border-radius: 0; }
}
"""

hero_html = """
<div class="hero-content">
    <h1 style="font-size: 4rem; line-height: 1; font-weight: 900; margin-bottom: 20px;">
        PDF Analyzer <br><span style="color: #10b981;">Simplified.</span>
    </h1>
    <p style="font-size: 1.25rem; color: #374151; font-weight: 500; margin-bottom: 30px;">
        Upload any document and get instant AI insights. 
        Powered by RAG and Gemini 2.5 Flash.
    </p>
    <div style="display: flex; gap: 15px; margin-bottom: 50px;">
        <span style="background: #059669; color: white; padding: 12px 25px; border-radius: 50px; font-weight: 700;">✓ PDF Analysis</span>
        <span style="background: white; border: 2px solid #059669; color: #059669; padding: 12px 25px; border-radius: 50px; font-weight: 700;">📄 Smart Retrieval</span>
    </div>
</div>
"""