# ui.py
import gradio as gr
from engine import process_pdf, get_chat_response
from ui_config import hero_html

def create_ui():
    # css=custom_css is removed here and moved to app.py's launch()
    with gr.Blocks() as demo:
        state_retriever = gr.State(None)
        
        with gr.Row():
            # SIDEBAR: scale=1 gives it that narrow Gemini drawer look
            with gr.Column(scale=1, elem_id="side_panel"):
                gr.Markdown("### 💎 Gemini PDF")
                file_input = gr.File(label="Upload Document", file_types=[".pdf"])
                
                process_btn = gr.Button("Initialize AI", variant="primary", elem_classes="primary-btn")
                reset_btn = gr.Button("New Chat", variant="secondary", elem_classes="secondary-btn")
                
                status = gr.Markdown("Status: **Ready**")

            # MAIN CHAT: scale=4 makes the chat area wide
            with gr.Column(scale=4):
                # Placeholder acts as the Gemini hero/greeting
                chatbot = gr.Chatbot(
                    label=None, 
                    elem_id="chatbot", 
                    show_label=False,
                    placeholder=hero_html, # Gemini-style greeting inside chat
                    avatar_images=(None, "https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6298a4245f.png")
                )
                
                chat_interface = gr.ChatInterface(
                    fn=get_chat_response,
                    chatbot=chatbot,
                    additional_inputs=[state_retriever],
                    multimodal=False,
                    textbox=gr.Textbox(
                        placeholder="Ask anything about the document...", 
                        elem_id="chat_input", 
                        container=False
                    )
                )

        # LOGIC
        def handle_upload(file):
            if not file: return None, "❌ No file.", []
            retriever = process_pdf(file.name)
            if retriever:
                summary_gen = get_chat_response("Summarize this document in 3 concise bullet points.", [], retriever)
                full_summary = ""
                for chunk in summary_gen: full_summary = chunk
                initial_msg = [{"role": "assistant", "content": f"**Analysis Complete!**\n\n{full_summary}"}]
                return retriever, "✅ AI Ready!", initial_msg
            return None, "❌ Error.", []

        process_btn.click(handle_upload, inputs=[file_input], outputs=[state_retriever, status, chatbot])
        reset_btn.click(lambda: (None, "Status: **Ready**", []), outputs=[file_input, status, chatbot])
        
    return demo