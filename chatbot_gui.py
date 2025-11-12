import tkinter as tk
from tkinter import scrolledtext
import threading
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ Transformers not available. Running in knowledge-base only mode.")


class CollegeChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Amity University Support Chatbot")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.bg_color = "#f0f2f5"
        self.primary_color = "#0084ff"
        self.user_msg_color = "#0084ff"
        self.bot_msg_color = "#e4e6eb"
        self.text_color = "#000000"
        
        self.college_name = "Amity University"
        self.model = None
        self.tokenizer = None
        self.chat_history_ids = None
        
        self.setup_gui()
        self.load_knowledge_base()
        
        self.show_bot_message("🎓 Welcome to Amity University Support Chatbot!\n\nI can help you with:\n• Admissions & Courses\n• Fees & Scholarships\n• Facilities & Campus\n• Placements & Events\n\nType your question or type 'help' for more options!")
        
        if TRANSFORMERS_AVAILABLE:
            threading.Thread(target=self.load_ai_model, daemon=True).start()
    
    def setup_gui(self):
        """Setup the GUI components"""
        self.root.configure(bg=self.bg_color)
        
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="🎓 Amity University Support",
            font=("Segoe UI", 20, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        header_label.pack(pady=15)
        
        self.status_label = tk.Label(
            header_frame,
            text="",
            font=("Segoe UI", 9),
            bg=self.primary_color,
            fg="white"
        )
        self.status_label.pack()
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        chat_frame = tk.Frame(main_frame, bg="white", relief=tk.FLAT)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="white",
            fg=self.text_color,
            relief=tk.FLAT,
            padx=15,
            pady=15,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        self.chat_display.tag_config("user", 
            foreground="white", 
            background=self.user_msg_color,
            spacing1=10, spacing3=10, 
            lmargin1=10, rmargin=10, 
            font=("Segoe UI", 11))
        
        self.chat_display.tag_config("bot", 
            foreground=self.text_color, 
            background=self.bot_msg_color,
            spacing1=10, spacing3=10, 
            lmargin1=10, rmargin=10,
            font=("Segoe UI", 11))
        
        self.chat_display.tag_config("time", 
            foreground="#65676b", 
            font=("Segoe UI", 8))

        quick_frame = tk.Frame(main_frame, bg=self.bg_color)
        quick_frame.pack(fill=tk.X, pady=(10, 0))
        
        quick_label = tk.Label(
            quick_frame,
            text="Quick Actions:",
            font=("Segoe UI", 9, "bold"),
            bg=self.bg_color,
            fg="#65676b"
        )
        quick_label.pack(side=tk.LEFT, padx=(0, 10))
        
        quick_actions = [
            ("📚 Courses", "what courses do you offer"),
            ("💰 Fees", "tell me about fees"),
            ("🏠 Hostel", "hostel information"),
            ("💼 Placements", "placement information")
        ]
        
        for text, query in quick_actions:
            btn = tk.Button(
                quick_frame,
                text=text,
                font=("Segoe UI", 9),
                bg="white",
                fg=self.text_color,
                relief=tk.FLAT,
                cursor="hand2",
                padx=10,
                pady=5,
                command=lambda q=query: self.quick_action(q)
            )
            btn.pack(side=tk.LEFT, padx=5)

        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.input_field = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            bg="white",
            fg=self.text_color,
            insertbackground=self.primary_color
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=10, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        self.input_field.focus()
        
        self.send_button = tk.Button(
            input_frame,
            text="Send ➤",
            font=("Segoe UI", 11, "bold"),
            bg=self.primary_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)
  
        footer_frame = tk.Frame(self.root, bg=self.bg_color, height=30)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 10))
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="AI Chatbot using HuggingFace Transformers | Type 'help' for assistance",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg="#65676b"
        )
        footer_label.pack()
    
    def load_knowledge_base(self):
        """Load college knowledge base"""
        self.knowledge_base = {
            'greetings': {
                'keywords': ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'hii', 'helo', 'hy'],
                'response': f"👋 Hello! Welcome to {self.college_name} Support!\n\nI can help you with:\n• 📚 Admissions & Courses\n• 💰 Fees & Scholarships\n• 🏢 Facilities\n• 💼 Placements\n• 📞 Contact Info\n\nWhat would you like to know?"
            },
            'about_college': {
                'keywords': ['about college', 'about your college', 'tell me about', 'know about college', 'college info'],
                'response': f"🎓 **About {self.college_name}**\n\n✨ Highlights:\n• 15+ Departments\n• 5000+ Students\n• 200+ Faculty Members\n• Modern Infrastructure\n• 100+ Companies for Placements\n• Active Sports & Cultural Activities\n\n📚 Programs: B.Tech, MBA, BBA, M.Tech, B.Sc, M.Sc\n\nWhat specific information would you like?"
            },
            'admission': {
                'keywords': ['admission', 'admissions', 'apply', 'application', 'how to join', 'enroll'],
                'response': "📝 **Admission Information**\n\n🎯 Programs: B.Tech, MBA, BBA, M.Tech, B.Sc, M.Sc\n\n✅ Eligibility:\n• UG: Min 60% in 12th\n• PG: Min 60% in Graduation\n\n📋 Entrance Exams: JEE Main, State CET\n📅 Deadline: June 30, 2025\n\n📧 Contact: admissions@amityuniversity.edu"
            },
            'courses': {
                'keywords': ['courses', 'programs', 'what courses', 'degrees', 'branches'],
                'response': "📚 **Programs Offered**\n\n🔧 Engineering:\n• CSE, ECE, Mechanical, Civil, EEE\n\n💼 Management:\n• MBA (Marketing, Finance, HR)\n• BBA\n\n💻 Computer Applications:\n• BCA\n\n🔬 Sciences:\n• B.Sc, M.Sc (Various streams)\n\n⏱️ Duration: 3-4 years (UG), 2 years (PG)"
            },
            'fees': {
                'keywords': ['fees', 'fee', 'cost', 'price', 'tuition', 'charges'],
                'response': "💰 **Fee Structure**\n\n💳 Annual Fees:\n• B.Tech: ₹75,000 - ₹1,20,000\n• MBA: ₹1,50,000 - ₹2,00,000\n• BBA/BCA: ₹60,000 - ₹80,000\n• B.Sc/M.Sc: ₹50,000 - ₹70,000\n\n🏠 Hostel: ₹40,000 - ₹60,000/year\n\n🎖️ Scholarships available!\n\n📞 accounts@amityuniversity.edu"
            },
            'facilities': {
                'keywords': ['facilities', 'infrastructure', 'amenities', 'campus facilities'],
                'response': "🏢 **Campus Facilities**\n\n📖 Library: 24/7 digital, 50,000+ books\n🔬 Labs: Computer & Engineering labs\n🏠 Hostel: Boys & Girls, 500+ capacity\n⚽ Sports: Cricket, Basketball, Gym\n🍽️ Cafeteria: 7 AM-10 PM\n📡 WiFi: Campus-wide\n\nWhat specific facility?"
            },
            'placement': {
                'keywords': ['placement', 'placements', 'job', 'companies', 'recruitment', 'package'],
                'response': "💼 **Placement Record**\n\n🎯 Statistics:\n• Rate: 85-90%\n• Companies: 100+ annually\n• Avg Package: ₹3.5-4.5 LPA\n• Highest: ₹15-18 LPA\n\n🏢 Top Recruiters:\n• TCS, Infosys, Wipro\n• Tech Mahindra, Cognizant\n\n📧 placements@amityuniversity.edu"
            },
            'scholarship': {
                'keywords': ['scholarship', 'scholarships', 'financial aid'],
                'response': "🎖️ **Scholarships**\n\n💡 Available:\n• Merit (Top 10%): 50% waiver\n• Sports: Up to 50%\n• Need-based: Up to 40%\n• Government scholarships\n\n📝 Apply during admission\n📞 scholarships@amityuniversity.edu"
            },
            'library': {
                'keywords': ['library', 'books', 'reading'],
                'response': "📖 **Library**\n\n📚 50,000+ Books, 5,000+ Journals\n⏰ Physical: 8 AM - 8 PM\n⏰ Digital: 24/7\n\n📱 Services:\n• Book Issue (3 books, 15 days)\n• Internet access\n• Study cubicles\n\n📧 library@amityuniversity.edu"
            },
            'hostel': {
                'keywords': ['hostel', 'accommodation', 'room'],
                'response': "🏠 **Hostel Facilities**\n\n🛏️ Separate Boys & Girls\n💰 Fees:\n• Non-AC: ₹40,000/year\n• AC: ₹60,000/year\n• Mess: ₹30,000-40,000/year\n\n✨ 24/7 Security, WiFi, Laundry\n\n📧 hostel@amityuniversity.edu"
            },
            'exam': {
                'keywords': ['exam', 'examination', 'test'],
                'response': "📝 **Examination**\n\n📅 Schedule:\n• Mid-term: Oct & March\n• End-term: Nov/Dec & Apr/May\n\n📊 Evaluation:\n• Mid: 30 marks\n• End: 50 marks\n• Internal: 20 marks\n\n📋 75% attendance mandatory"
            },
            'result': {
                'keywords': ['result', 'marks', 'grade'],
                'response': "🎓 **Results**\n\n📊 Published online within 30 days\n🔐 Check: www.amityuniversity.edu/results\n\n🔄 Revaluation:\n• Apply within 7 days\n• Fee: ₹500 per subject"
            },
            'contact': {
                'keywords': ['contact', 'phone', 'email', 'address'],
                'response': "📞 **Contact**\n\n📧 info@amityuniversity.edu\n📧 admissions@amityuniversity.edu\n📱 +91-141-XXXXXXX\n\n📍 Amity University\nCollege Road, Jaipur\n\n⏰ Mon-Fri: 9 AM - 5 PM"
            },
            'thanks': {
                'keywords': ['thanks', 'thank you'],
                'response': "😊 You're welcome! Happy to help! 🎓"
            },
            'help': {
                'keywords': ['help', 'menu'],
                'response': "📋 **I can help with:**\n\n🎓 Admissions\n📚 Courses\n💰 Fees\n🏢 Facilities\n💼 Placements\n📝 Exams\n📞 Contact\n\nJust ask!"
            }
        }
    
    def load_ai_model(self):
        """Load AI model in background"""
        try:
            self.status_label.config(text="Loading AI model... (2-5 minutes first time)")
            
            model_name = "microsoft/DialoGPT-medium"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)

            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.tokenizer.eos_token_id
            
            self.status_label.config(text="✓ AI model loaded successfully!")
            self.root.after(3000, lambda: self.status_label.config(text=""))
            
        except Exception as e:
            self.status_label.config(text="⚠️ Running in knowledge-base mode only")
            self.root.after(5000, lambda: self.status_label.config(text=""))
            print(f"Error loading model: {e}")
    
    def find_answer(self, user_input):
        """Search knowledge base with better matching"""
        user_lower = user_input.lower().strip()
        for category, data in self.knowledge_base.items():
            for keyword in data['keywords']:
                if ' ' in keyword:
                    if keyword in user_lower:
                        return data['response']

        words_in_query = user_lower.split()
        for category, data in self.knowledge_base.items():
            for keyword in data['keywords']:
                if ' ' not in keyword and keyword in words_in_query:
                    return data['response']
        
        return None
    
    def get_ai_response(self, user_input):
        """Get AI-generated response using DialoGPT"""
        if self.model is None or self.tokenizer is None:
            return "I'm here to help with college queries! Ask about admissions, courses, facilities, placements, or type 'help'."
        
        try:
            new_input_ids = self.tokenizer.encode(
                user_input + self.tokenizer.eos_token,
                return_tensors='pt'
            )
            
            attention_mask = torch.ones(new_input_ids.shape, dtype=torch.long)
            
            if self.chat_history_ids is not None:
                bot_input_ids = torch.cat([self.chat_history_ids, new_input_ids], dim=-1)
                attention_mask = torch.ones(bot_input_ids.shape, dtype=torch.long)
            else:
                bot_input_ids = new_input_ids
            
            with torch.no_grad():
                self.chat_history_ids = self.model.generate(
                    bot_input_ids,
                    attention_mask=attention_mask,
                    max_length=1000,
                    pad_token_id=self.tokenizer.eos_token_id,
                    temperature=0.8,
                    top_k=50,
                    top_p=0.9,
                    do_sample=True,
                    no_repeat_ngram_size=3
                )
            
            response = self.tokenizer.decode(
                self.chat_history_ids[:, bot_input_ids.shape[-1]:][0],
                skip_special_tokens=True
            )
            
            return response if response else "Could you rephrase that? I'm here to help with college queries!"
            
        except Exception as e:
            print(f"AI Error: {e}")
            return "I'm here to help! Ask me about admissions, courses, facilities, or type 'help'."
    
    def quick_action(self, query):
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, query)
        self.send_message()
    
    def send_message(self):
        message = self.input_field.get().strip()
        
        if not message:
            return
        
        self.input_field.delete(0, tk.END)
        self.show_user_message(message)
        
        if message.lower() in ['quit', 'exit', 'bye']:
            self.show_bot_message("Thank you! Good luck with your studies! 👋")
            return
        
        if message.lower() == 'reset':
            self.chat_history_ids = None
            self.show_bot_message("Conversation reset! 💬")
            return
        
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message):
        response = self.find_answer(message)
        
        if response is None:
            response = self.get_ai_response(message)
        self.root.after(0, lambda: self.show_bot_message(response))
    
    def show_user_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        
        time_str = datetime.now().strftime("%I:%M %p")
        self.chat_display.insert(tk.END, f"\n{time_str}\n", "time")
        self.chat_display.insert(tk.END, f"You: {message}\n", "user")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def show_bot_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        
        time_str = datetime.now().strftime("%I:%M %p")
        self.chat_display.insert(tk.END, f"\n{time_str}\n", "time")
        self.chat_display.insert(tk.END, f"🤖 Bot: {message}\n", "bot")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)


def main():
    root = tk.Tk()
    app = CollegeChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
