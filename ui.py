# ui.py
import gradio as gr
from engine import process_pdf, get_chat_response
from ui_config import hero_html

def create_ui():
    with gr.Blocks() as demo:
        gr.HTML(hero_html)
        state_retriever = gr.State(None)
        
        # --- 1. UPLOAD & RESET SECTION ---
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📂 Document Management")
                
                # UPDATED: Simplified file input
                file_input = gr.File(
                    label="Choose PDF", 
                    file_types=[".pdf"],
                    file_count="single",
                    show_label=True,
                    container=True # Keeps it contained without the extra 'X' in some themes
                )
                
                with gr.Row():
                    process_btn = gr.Button("🚀 Initialize AI", variant="primary")
                    reset_btn = gr.Button("🗑️ Reset/Replace PDF", variant="stop")
                
                status = gr.Markdown("Status: *Waiting for upload...*")

        # --- 2. FLOATING CHAT WIDGET ---
        open_btn = gr.Button("💬 Open Chat", elem_id="open_chat_btn", visible=False)

        with gr.Column(elem_id="floating_container", visible=False) as chat_container:
            with gr.Row():
                gr.HTML('<div class="widget-header" style="flex-grow: 1;"><span>📄</span> AI Assistant</div>')
                min_btn = gr.Button("➖", variant="secondary", size="sm", elem_id="min_button")
            
            chatbot = gr.Chatbot(label="Chat History")
            
            chat_interface = gr.ChatInterface(
                fn=get_chat_response,
                chatbot=chatbot,
                additional_inputs=[state_retriever],
                multimodal=False
            )

        # --- 3. FUNCTIONS ---
        def handle_upload(file):
            if not file:
                return None, "❌ No file uploaded.", [], gr.update(visible=False)
            
            retriever = process_pdf(file.name)
            if retriever:
                summary_gen = get_chat_response("Summarize this document in 3 concise bullet points.", [], retriever)
                full_summary = ""
                for chunk in summary_gen:
                    full_summary = chunk
                
                initial_msg = [{"role": "assistant", "content": f"✅ **Analysis Complete!**\n\n{full_summary}"}]
                return retriever, "✅ AI is ready!", initial_msg, gr.update(visible=True)
            
            return None, "❌ Processing failed.", [], gr.update(visible=False)

        def reset_app():
            return (
                None,                       
                "Status: *Ready for new upload*", 
                None,                       
                [],                         
                gr.update(visible=False),    
                gr.update(visible=False)     
            )

        # --- 4. EVENT LISTENERS ---
        process_btn.click(
            handle_upload, 
            inputs=[file_input], 
            outputs=[state_retriever, status, chatbot, chat_container],
            show_progress="full"
        )

        reset_btn.click(
            reset_app,
            outputs=[file_input, status, state_retriever, chatbot, chat_container, open_btn]
        )

        min_btn.click(
            lambda: (gr.update(visible=False), gr.update(visible=True)),
            outputs=[chat_container, open_btn]
        )

        open_btn.click(
            lambda: (gr.update(visible=True), gr.update(visible=False)),
            outputs=[chat_container, open_btn]
        )
        
    return demo