import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import pipeline, Conversation
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
        self.secondary_color = "#e4e6eb"
        self.user_msg_color = "#0084ff"
        self.bot_msg_color = "#e4e6eb"
        self.text_color = "#000000"
        
        self.college_name = "Amity University"
        self.conversational_ai = None
        self.loading = False
        
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
        header_label.pack(pady=20)
        
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
        
        chat_frame = tk.Frame(main_frame, bg="white", relief=tk.FLAT, bd=0)
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
            state=tk.DISABLED,
            cursor="arrow"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        self.chat_display.tag_config("user", foreground="white", background=self.user_msg_color, 
                                     spacing1=10, spacing3=10, lmargin1=10, lmargin2=10, 
                                     rmargin=10, font=("Segoe UI", 11))
        self.chat_display.tag_config("bot", foreground=self.text_color, background=self.bot_msg_color,
                                     spacing1=10, spacing3=10, lmargin1=10, lmargin2=10,
                                     rmargin=10, font=("Segoe UI", 11))
        self.chat_display.tag_config("time", foreground="#65676b", font=("Segoe UI", 8))
        
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
            text="Project - AI Chatbot using HuggingFace Transformers | Type 'help' for assistance",
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
                'response': "💰 **Fee Structure**\n\n💳 Annual Fees:\n• B.Tech: ₹75,000 - ₹1,20,000\n• MBA: ₹1,50,000 - ₹2,00,000\n• BBA/BCA: ₹60,000 - ₹80,000\n• B.Sc/M.Sc: ₹50,000 - ₹70,000\n\n🏠 Hostel: ₹40,000 - ₹60,000/year\n\n🎖️ Scholarships available for merit students!\n\n📞 Contact: accounts@amityuniversity.edu"
            },
            'facilities': {
                'keywords': ['facilities', 'infrastructure', 'amenities', 'campus facilities'],
                'response': "🏢 **Campus Facilities**\n\n📖 Library: 24/7 digital, 50,000+ books\n🔬 Labs: Computer & Engineering labs\n🏠 Hostel: Boys & Girls, 500+ capacity\n⚽ Sports: Cricket, Basketball, Gym\n🍽️ Cafeteria: Multi-cuisine, 7 AM-10 PM\n📡 WiFi: High-speed campus-wide\n\nWhat specific facility would you like to know about?"
            },
            'placement': {
                'keywords': ['placement', 'placements', 'job', 'companies', 'recruitment', 'package'],
                'response': "💼 **Placement Record**\n\n🎯 Statistics:\n• Placement Rate: 85-90%\n• Companies: 100+ annually\n• Avg Package: ₹3.5-4.5 LPA\n• Highest: ₹15-18 LPA\n\n🏢 Top Recruiters:\n• TCS, Infosys, Wipro\n• Tech Mahindra, Cognizant\n• Amazon, Microsoft (occasional)\n\n📚 Pre-placement training provided!\n\n📧 placements@amityuniversity.edu"
            },
            'scholarship': {
                'keywords': ['scholarship', 'scholarships', 'financial aid', 'concession'],
                'response': "🎖️ **Scholarships**\n\n💡 Available:\n• Merit (Top 10%): 50% waiver\n• Sports: Up to 50% waiver\n• Need-based: Up to 40%\n• Government scholarships\n\n📝 Apply during admission with documents\n\n📞 scholarships@amityuniversity.edu"
            },
            'library': {
                'keywords': ['library', 'books', 'reading room'],
                'response': "📖 **Library**\n\n📚 Collection:\n• 50,000+ Books\n• 5,000+ Journals\n• E-books & Online Resources\n\n⏰ Timings:\n• Physical: 8 AM - 8 PM\n• Digital: 24/7\n\n📱 Services:\n• Book Issue (3 books, 15 days)\n• Internet access\n• Study cubicles\n\n📧 library@amityuniversity.edu"
            },
            'hostel': {
                'keywords': ['hostel', 'accommodation', 'room', 'residence'],
                'response': "🏠 **Hostel Facilities**\n\n🛏️ Accommodation:\n• Separate Boys & Girls\n• Single/Double/Triple sharing\n• AC & Non-AC options\n\n💰 Fees:\n• Non-AC: ₹40,000/year\n• AC: ₹60,000/year\n• Mess: ₹30,000-40,000/year\n\n✨ Amenities:\n• 24/7 Security\n• WiFi\n• Laundry\n• Common rooms\n\n📧 hostel@amityuniversity.edu"
            },
            'exam': {
                'keywords': ['exam', 'exams', 'examination', 'test'],
                'response': "📝 **Examination System**\n\n📅 Schedule:\n• Mid-term: October & March\n• End-term: Nov/Dec & April/May\n\n📊 Evaluation:\n• Mid-term: 30 marks\n• End-term: 50 marks\n• Internal: 20 marks\n\n📋 75% attendance mandatory\n\n📧 examinations@amityuniversity.edu"
            },
            'result': {
                'keywords': ['result', 'results', 'marks', 'grade'],
                'response': "🎓 **Results**\n\n📊 Declaration:\n• Published online\n• Within 30 days of exams\n• SMS notification sent\n\n🔐 Check at:\nwww.amityuniversity.edu/results\n\n🔄 Revaluation:\n• Apply within 7 days\n• Fee: ₹500 per subject\n\n📧 examinations@amityuniversity.edu"
            },
            'events': {
                'keywords': ['events', 'fest', 'festival', 'activities', 'cultural'],
                'response': "🎉 **Events & Activities**\n\n🎪 Annual Events:\n• TechFest (March)\n• Cultural Fest (February)\n• Sports Week (January)\n\n📚 Regular:\n• Workshops\n• Guest lectures\n• Industrial visits\n• Club activities\n\nFollow us on social media for updates!"
            },
            'contact': {
                'keywords': ['contact', 'phone', 'email', 'address', 'location'],
                'response': "📞 **Contact Information**\n\n📧 Email:\n• General: info@amityuniversity.edu\n• Admissions: admissions@amityuniversity.edu\n• Placements: placements@amityuniversity.edu\n\n📱 Phone: +91-141-XXXXXXX\n\n📍 Address:\nAmity University\nCollege Road, Sector-XX\nCity, State - 123456\n\n⏰ Office: Mon-Fri, 9 AM - 5 PM\n\n🌐 www.amityuniversity.edu"
            },
            'thanks': {
                'keywords': ['thanks', 'thank you', 'thankyou'],
                'response': "😊 You're welcome! Feel free to ask anything else about the college. Happy to help! 🎓"
            },
            'help': {
                'keywords': ['help', 'menu', 'options'],
                'response': "📋 **I can help you with:**\n\n🎓 Admissions & Eligibility\n📚 Courses & Programs\n💰 Fees & Scholarships\n🏢 Facilities (Library, Hostel, Labs)\n💼 Placements & Companies\n📝 Exams & Results\n🎉 Events & Activities\n📞 Contact Information\n\nJust type your question!"
            }
        }
    
    def load_ai_model(self):
        """Load AI model in background"""
        try:
            self.status_label.config(text="Loading AI model... (first time may take 2-5 minutes)")
            self.conversational_ai = pipeline("conversational", model="microsoft/DialoGPT-medium")
            self.status_label.config(text="✓ AI model loaded")
            self.root.after(3000, lambda: self.status_label.config(text=""))
        except Exception as e:
            self.status_label.config(text="⚠️ Running in knowledge-base mode")
            self.root.after(5000, lambda: self.status_label.config(text=""))
    
    def find_answer(self, user_input):
        """Search knowledge base"""
        user_lower = user_input.lower()
        
        for category, data in self.knowledge_base.items():
            for keyword in data['keywords']:
                if keyword in user_lower:
                    return data['response']
        
        return None
    
    def get_ai_response(self, user_input):
        """Get AI response"""
        if self.conversational_ai is None:
            return "I specialize in college queries! Ask me about admissions, courses, facilities, placements, fees, or type 'help' for all topics."
        
        try:
            conversation = Conversation(user_input)
            result = self.conversational_ai(conversation)
            return result.generated_responses[-1]
        except:
            return "I'm here to help with college information! Type 'help' to see all topics."
    
    def quick_action(self, query):
        """Handle quick action button clicks"""
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, query)
        self.send_message()
    
    def send_message(self):
        """Send user message"""
        message = self.input_field.get().strip()
        
        if not message:
            return
        
        self.input_field.delete(0, tk.END)
        
        self.show_user_message(message)
        
        if message.lower() in ['quit', 'exit', 'bye']:
            self.show_bot_message("Thank you for using our support system! Good luck with your studies! 👋")
            return
        
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message):
        """Process message and get response"""
        response = self.find_answer(message)
        
        if response is None:
            response = self.get_ai_response(message)
        
        self.root.after(0, lambda: self.show_bot_message(response))
    
    def show_user_message(self, message):
        """Display user message"""
        self.chat_display.config(state=tk.NORMAL)
        
        time_str = datetime.now().strftime("%I:%M %p")
        self.chat_display.insert(tk.END, f"\n{time_str}\n", "time")
        
        self.chat_display.insert(tk.END, f"You: {message}\n", "user")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def show_bot_message(self, message):
        """Display bot message"""
        self.chat_display.config(state=tk.NORMAL)
        
        time_str = datetime.now().strftime("%I:%M %p")
        self.chat_display.insert(tk.END, f"\n{time_str}\n", "time")

        self.chat_display.insert(tk.END, f"🤖 Bot: {message}\n", "bot")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)


def main():
    """Main function"""
    root = tk.Tk()
    app = CollegeChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()