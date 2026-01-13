# app.py
from ui import create_ui
from ui_config import custom_css
import gradio as gr

if __name__ == "__main__":
    demo = create_ui()
    
    print("🚀 Starting PDF Analyzer on http://127.0.0.1:7860")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        css=custom_css,
        theme=gr.themes.Soft(primary_hue="emerald")
    )