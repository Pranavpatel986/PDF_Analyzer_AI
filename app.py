from ui import create_ui
from ui_config import custom_css
import gradio as gr
import os

if __name__ == "__main__":
    demo = create_ui()
    
    current_path = os.path.dirname(os.path.abspath(__file__))

    print("🚀 Gemini UI Starting on http://127.0.0.1:7860")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        css=custom_css, # CSS must be here in Gradio 6.0
        allowed_paths=[current_path],
        theme=gr.themes.Soft(
            primary_hue="blue", 
            spacing_size="sm", 
            radius_size="lg",
            font=["Google Sans", "ui-sans-serif", "system-ui"]
        )
    )