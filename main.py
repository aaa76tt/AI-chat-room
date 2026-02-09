import AI1
import AI2
import AI3
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading

# API Configuration
API_KEY = "sk-qyyqisyvwfdvbprugtcqpvozvzwnjbrgbmmybgofarbbytbn"
API_URL = "https://api.siliconflow.cn/v1/chat/completions"#<- your api key
MODEL = "deepseek-ai/DeepSeek-V3"
PLATFORM = "SiliconFlow"

# Dark Theme Color Scheme
DARK_BG = "#1e1e1e"
DARKER_BG = "#252526"
LIGHT_TEXT = "#d4d4d4"
ACCENT_COLOR = "#007acc"
AI1_COLOR = "#4ec9b0"
AI2_COLOR = "#ce9178"
AI3_COLOR = "#c586c0"
BUTTON_BG = "#0e639c"
BUTTON_HOVER = "#1177bb"

class AIConversationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Multi-Agent Conversation System")
        self.root.geometry("1000x700")
        self.root.configure(bg=DARK_BG)
        
        self.shared_memory = []
        self.is_running = False
        self.conversation_thread = None
        self.round_num = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg=DARK_BG)
        title_frame.pack(pady=10, padx=10, fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="🤖 AI Multi-Agent Conversation System",
            font=("Segoe UI", 18, "bold"),
            bg=DARK_BG,
            fg=LIGHT_TEXT
        )
        title_label.pack()
        
        # Control Panel
        control_frame = tk.Frame(self.root, bg=DARKER_BG)
        control_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Initial Topic Input
        topic_label = tk.Label(
            control_frame,
            text="Initial Topic:",
            font=("Segoe UI", 10),
            bg=DARKER_BG,
            fg=LIGHT_TEXT
        )
        topic_label.pack(side=tk.LEFT, padx=5)
        
        self.topic_entry = tk.Entry(
            control_frame,
            font=("Segoe UI", 10),
            bg=DARK_BG,
            fg=LIGHT_TEXT,
            insertbackground=LIGHT_TEXT,
            relief=tk.FLAT,
            width=40
        )
        self.topic_entry.insert(0, "Hello everyone, let's have a chat!")
        self.topic_entry.pack(side=tk.LEFT, padx=5, ipady=5)
        
        # Start Button
        self.start_button = tk.Button(
            control_frame,
            text="▶ Start",
            font=("Segoe UI", 10, "bold"),
            bg=BUTTON_BG,
            fg=LIGHT_TEXT,
            activebackground=BUTTON_HOVER,
            activeforeground=LIGHT_TEXT,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_conversation
        )
        self.start_button.pack(side=tk.LEFT, padx=5, ipady=5, ipadx=10)
        
        # Stop Button
        self.stop_button = tk.Button(
            control_frame,
            text="⏸ Stop",
            font=("Segoe UI", 10, "bold"),
            bg="#d13438",
            fg=LIGHT_TEXT,
            activebackground="#e74c3c",
            activeforeground=LIGHT_TEXT,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.stop_conversation,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5, ipady=5, ipadx=10)
        
        # Status Label
        self.status_label = tk.Label(
            control_frame,
            text="● Ready",
            font=("Segoe UI", 10),
            bg=DARKER_BG,
            fg="#4ec9b0"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Chat Display Area
        chat_frame = tk.Frame(self.root, bg=DARK_BG)
        chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            font=("Segoe UI", 10),
            bg=DARKER_BG,
            fg=LIGHT_TEXT,
            insertbackground=LIGHT_TEXT,
            relief=tk.FLAT,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure Text Tag Styles
        self.chat_display.tag_config("ai1", foreground=AI1_COLOR, font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("ai2", foreground=AI2_COLOR, font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("ai3", foreground=AI3_COLOR, font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("round", foreground=ACCENT_COLOR, font=("Segoe UI", 9))
        self.chat_display.tag_config("system", foreground="#608b4e", font=("Segoe UI", 9, "italic"))
        
        # Statistics Info
        stats_frame = tk.Frame(self.root, bg=DARKER_BG)
        stats_frame.pack(pady=5, padx=10, fill=tk.X)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Rounds: 0 | Messages: 0",
            font=("Segoe UI", 9),
            bg=DARKER_BG,
            fg=LIGHT_TEXT
        )
        self.stats_label.pack()
        
    def append_message(self, text, tag=None):
        """Append message to chat display area"""
        self.chat_display.config(state=tk.NORMAL)
        if tag:
            self.chat_display.insert(tk.END, text, tag)
        else:
            self.chat_display.insert(tk.END, text)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def update_stats(self):
        """Update statistics information"""
        self.stats_label.config(text=f"Rounds: {self.round_num} | Messages: {len(self.shared_memory)}")
        
    def format_shared_memory(self, max_messages=10):
        """Format shared memory"""
        if not self.shared_memory:
            return "(No conversation history yet)"
        
        recent_memory = self.shared_memory[-max_messages:] if len(self.shared_memory) > max_messages else self.shared_memory
        
        memory_text = "=== Shared Memory ===\n"
        for record in recent_memory:
            memory_text += f"[Round {record['round']}] {record['speaker']}: {record['message']}\n\n"
        
        return memory_text
        
    def conversation_loop(self, initial_message):
        """Conversation loop"""
        self.append_message("=== Starting Multi-AI Conversation ===\n", "system")
        self.append_message(f"Initial Topic: {initial_message}\n\n", "system")
        
        while self.is_running:
            self.round_num += 1
            self.append_message(f"--- Round {self.round_num} ---\n", "round")
            
            # AI1 Response
            self.root.after(0, lambda: self.status_label.config(text="● AI1 (Alice) is thinking...", fg=AI1_COLOR))
            memory_context = self.format_shared_memory()
            ai1_prompt = f"""You are Alice.

{memory_context}

Initial Topic: {initial_message}

Please continue the conversation based on the shared memory above. If this is the first round, please start the topic."""
            
            try:
                ai1_response, _ = AI1.call_deepseek(
                    ai1_prompt,
                    conversation_history=None,
                    api_key=API_KEY,
                    model=MODEL,
                    platform=PLATFORM,
                    url=API_URL
                )
                self.shared_memory.append({"speaker": "AI1 (Alice)", "round": self.round_num, "message": ai1_response})
                self.append_message("AI1 (Alice): ", "ai1")
                self.append_message(f"{ai1_response}\n\n")
                self.update_stats()
            except Exception as e:
                self.append_message(f"[Error] AI1: {str(e)}\n\n", "system")
                
            if not self.is_running:
                break
                
            # AI2 Response
            self.root.after(0, lambda: self.status_label.config(text="● AI2 (Bob) is thinking...", fg=AI2_COLOR))
            memory_context = self.format_shared_memory()
            ai2_prompt = f"""You are Bob.

{memory_context}

Please continue the conversation based on the shared memory above."""
            
            try:
                ai2_response, _ = AI2.call_deepseek(
                    ai2_prompt,
                    conversation_history=None,
                    api_key=API_KEY,
                    model=MODEL,
                    platform=PLATFORM,
                    url=API_URL
                )
                self.shared_memory.append({"speaker": "AI2 (Bob)", "round": self.round_num, "message": ai2_response})
                self.append_message("AI2 (Bob): ", "ai2")
                self.append_message(f"{ai2_response}\n\n")
                self.update_stats()
            except Exception as e:
                self.append_message(f"[Error] AI2: {str(e)}\n\n", "system")
                
            if not self.is_running:
                break
                
            # AI3 Response
            self.root.after(0, lambda: self.status_label.config(text="● AI3 (Charlie) is thinking...", fg=AI3_COLOR))
            memory_context = self.format_shared_memory()
            ai3_prompt = f"""You are Charlie.

{memory_context}

Please continue the conversation based on the shared memory above."""
            
            try:
                ai3_response, _ = AI3.call_deepseek(
                    ai3_prompt,
                    conversation_history=None,
                    api_key=API_KEY,
                    model=MODEL,
                    platform=PLATFORM,
                    url=API_URL
                )
                self.shared_memory.append({"speaker": "AI3 (Charlie)", "round": self.round_num, "message": ai3_response})
                self.append_message("AI3 (Charlie): ", "ai3")
                self.append_message(f"{ai3_response}\n\n")
                self.update_stats()
            except Exception as e:
                self.append_message(f"[Error] AI3: {str(e)}\n\n", "system")
                
        self.append_message("\n=== Conversation Stopped ===\n", "system")
        self.root.after(0, lambda: self.status_label.config(text="● Stopped", fg="#d13438"))
        self.root.after(0, self.reset_buttons)
        
    def start_conversation(self):
        """Start conversation"""
        if self.is_running:
            return
            
        initial_topic = self.topic_entry.get().strip()
        if not initial_topic:
            initial_topic = "Hello everyone, let's have a chat!"
            
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.topic_entry.config(state=tk.DISABLED)
        
        # Clear display area
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Reset statistics
        self.shared_memory = []
        self.round_num = 0
        self.update_stats()
        
        # Run conversation in new thread
        self.conversation_thread = threading.Thread(
            target=self.conversation_loop,
            args=(initial_topic,),
            daemon=True
        )
        self.conversation_thread.start()
        
    def stop_conversation(self):
        """Stop conversation"""
        self.is_running = False
        self.status_label.config(text="● Stopping...", fg="#ce9178")
        
    def reset_buttons(self):
        """Reset button states"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.topic_entry.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = AIConversationGUI(root)
    root.mainloop()
