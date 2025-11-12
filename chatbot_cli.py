"""
College Support Chatbot - CLI Version
AI-powered chatbot using HuggingFace Transformers
Optimized for CPU - No GPU required
"""

import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ Transformers not available. Running in knowledge-base only mode.\n")


class CollegeChatbotCLI:
    def __init__(self, college_name="Amity University"):
        print("🎓 Loading College Support Chatbot...")
        print("(First run may take 2-5 minutes to download model)\n")
        
        self.college_name = college_name
        self.model = None
        self.tokenizer = None
        self.chat_history_ids = None

        self.load_knowledge_base()

        if TRANSFORMERS_AVAILABLE:
            self.load_ai_model()
        
        print(f"✓ {college_name} Support Bot ready! Type 'quit' to exit.\n")
    
    def load_knowledge_base(self):
        """Load college knowledge base"""
        self.knowledge_base = {
            'greetings': {
                'keywords': ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'hii', 'helo', 'hy'],
                'response': f"👋 Hello! Welcome to {self.college_name} Support!\n\nI can help you with:\n• 📚 Admissions & Courses\n• 💰 Fees & Scholarships\n• 🏢 Facilities\n• 💼 Placements\n• 📞 Contact Info\n\nWhat would you like to know?"
            },
            'about_college': {
                'keywords': ['about college', 'about your college', 'tell me about', 'know about college', 'college info'],
                'response': f"🎓 About {self.college_name}\n\n✨ Highlights:\n• 15+ Departments\n• 5000+ Students\n• 200+ Faculty Members\n• Modern Infrastructure\n• 100+ Companies for Placements\n• Active Sports & Cultural Activities\n\n📚 Programs: B.Tech, MBA, BBA, M.Tech, B.Sc, M.Sc\n\nWhat specific information would you like?"
            },
            'admission': {
                'keywords': ['admission', 'admissions', 'apply', 'application', 'how to join', 'enroll'],
                'response': "📝 Admission Information\n\n🎯 Programs: B.Tech, MBA, BBA, M.Tech, B.Sc, M.Sc\n\n✅ Eligibility:\n• UG: Min 60% in 12th\n• PG: Min 60% in Graduation\n\n📋 Entrance Exams: JEE Main, State CET\n📅 Deadline: June 30, 2025\n\n📧 Contact: admissions@amityuniversity.edu"
            },
            'courses': {
                'keywords': ['courses', 'programs', 'what courses', 'degrees', 'branches'],
                'response': "📚 Programs Offered\n\n🔧 Engineering:\n• CSE, ECE, Mechanical, Civil, EEE\n\n💼 Management:\n• MBA (Marketing, Finance, HR)\n• BBA\n\n💻 Computer Applications:\n• BCA\n\n🔬 Sciences:\n• B.Sc, M.Sc (Various streams)\n\n⏱️ Duration: 3-4 years (UG), 2 years (PG)"
            },
            'fees': {
                'keywords': ['fees', 'fee', 'cost', 'price', 'tuition', 'charges'],
                'response': "💰 Fee Structure\n\n💳 Annual Fees:\n• B.Tech: ₹75,000 - ₹1,20,000\n• MBA: ₹1,50,000 - ₹2,00,000\n• BBA/BCA: ₹60,000 - ₹80,000\n• B.Sc/M.Sc: ₹50,000 - ₹70,000\n\n🏠 Hostel: ₹40,000 - ₹60,000/year\n\n🎖️ Scholarships available!\n\n📞 accounts@amityuniversity.edu"
            },
            'facilities': {
                'keywords': ['facilities', 'infrastructure', 'amenities', 'campus facilities'],
                'response': "🏢 Campus Facilities\n\n📖 Library: 24/7 digital, 50,000+ books\n🔬 Labs: Computer & Engineering labs\n🏠 Hostel: Boys & Girls, 500+ capacity\n⚽ Sports: Cricket, Basketball, Gym\n🍽️ Cafeteria: 7 AM-10 PM\n📡 WiFi: Campus-wide"
            },
            'placement': {
                'keywords': ['placement', 'placements', 'job', 'companies', 'recruitment', 'package'],
                'response': "💼 Placement Record\n\n🎯 Statistics:\n• Rate: 85-90%\n• Companies: 100+ annually\n• Avg Package: ₹3.5-4.5 LPA\n• Highest: ₹15-18 LPA\n\n🏢 Top Recruiters:\n• TCS, Infosys, Wipro\n• Tech Mahindra, Cognizant\n\n📧 placements@amityuniversity.edu"
            },
            'scholarship': {
                'keywords': ['scholarship', 'scholarships', 'financial aid'],
                'response': "🎖️ Scholarships\n\n💡 Available:\n• Merit (Top 10%): 50% waiver\n• Sports: Up to 50%\n• Need-based: Up to 40%\n• Government scholarships\n\n📝 Apply during admission\n📞 scholarships@amityuniversity.edu"
            },
            'library': {
                'keywords': ['library', 'books', 'reading'],
                'response': "📖 Library\n\n📚 50,000+ Books, 5,000+ Journals\n⏰ Physical: 8 AM - 8 PM\n⏰ Digital: 24/7\n\n📱 Services:\n• Book Issue (3 books, 15 days)\n• Internet access\n• Study cubicles\n\n📧 library@amityuniversity.edu"
            },
            'hostel': {
                'keywords': ['hostel', 'accommodation', 'room'],
                'response': "🏠 Hostel Facilities\n\n🛏️ Separate Boys & Girls\n💰 Fees:\n• Non-AC: ₹40,000/year\n• AC: ₹60,000/year\n• Mess: ₹30,000-40,000/year\n\n✨ 24/7 Security, WiFi, Laundry\n\n📧 hostel@amityuniversity.edu"
            },
            'exam': {
                'keywords': ['exam', 'examination', 'test'],
                'response': "📝 Examination\n\n📅 Schedule:\n• Mid-term: Oct & March\n• End-term: Nov/Dec & Apr/May\n\n📊 Evaluation:\n• Mid: 30 marks\n• End: 50 marks\n• Internal: 20 marks\n\n📋 75% attendance mandatory"
            },
            'result': {
                'keywords': ['result', 'marks', 'grade'],
                'response': "🎓 Results\n\n📊 Published online within 30 days\n🔐 Check: www.amityuniversity.edu/results\n\n🔄 Revaluation:\n• Apply within 7 days\n• Fee: ₹500 per subject"
            },
            'contact': {
                'keywords': ['contact', 'phone', 'email', 'address'],
                'response': "📞 Contact\n\n📧 info@amityuniversity.edu\n📧 admissions@amityuniversity.edu\n📱 +91-141-XXXXXXX\n\n📍 Amity University\nCollege Road, Jaipur\n\n⏰ Mon-Fri: 9 AM - 5 PM"
            },
            'thanks': {
                'keywords': ['thanks', 'thank you'],
                'response': "😊 You're welcome! Happy to help! 🎓"
            },
            'help': {
                'keywords': ['help', 'menu'],
                'response': "📋 I can help with:\n\n🎓 Admissions & Eligibility\n📚 Courses & Programs\n💰 Fees & Scholarships\n🏢 Facilities (Library, Hostel, Labs)\n💼 Placements & Companies\n📝 Exams & Results\n🎉 Events & Activities\n📞 Contact Information\n\nJust type your question!"
            }
        }
    
    def load_ai_model(self):
        """Load AI model"""
        try:
            print("⏳ Loading AI model (DialoGPT-medium)...")
            
            model_name = "microsoft/DialoGPT-medium"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)

            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.tokenizer.eos_token_id
            
            print("✓ AI model loaded successfully!\n")
            
        except Exception as e:
            print(f"⚠️ Could not load AI model: {e}")
            print("Running in knowledge-base only mode\n")
    
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
            return "I'm here to help! Ask me about admissions, courses, facilities, or type 'help'."
    
    def reset_conversation(self):
        """Reset chat history"""
        self.chat_history_ids = None
        print("\n💬 Conversation reset! Starting fresh.\n")
    
    def chat(self):
        """Main chat loop"""
        print("=" * 70)
        print(f"     🎓 {self.college_name} Support Chatbot")
        print("=" * 70)
        print("Ask me about: admissions, courses, facilities, placements, fees, etc.")
        print("Commands: 'help', 'reset', 'quit'")
        print("=" * 70 + "\n")
        
        while True:
            user_input = input("Student: ").strip()
            
            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🎓 Bot: Thank you! Good luck with your studies! 👋\n")
                break
            
            if user_input.lower() == 'reset':
                self.reset_conversation()
                continue

            response = self.find_answer(user_input)
            
            if response:
                print(f"\n🤖 Bot: {response}\n")
            else:
                print("\n🤖 Bot: ", end="", flush=True)
                ai_response = self.get_ai_response(user_input)
                print(f"{ai_response}\n")


def main():
    """Main function"""
    college_name = "Amity University"
    bot = CollegeChatbotCLI(college_name)
    bot.chat()


if __name__ == "__main__":
    main()
