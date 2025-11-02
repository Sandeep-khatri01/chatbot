from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')

class CollegeSupportChatbot:
    def __init__(self, college_name="Amity University"):
        print("🎓 Loading College Support Chatbot...")
        print("(First run may take 2-5 minutes to download model)\n")
        
        try:
            self.conversational_ai = pipeline("conversational", model="microsoft/DialoGPT-medium")
        except:
            self.conversational_ai = None
            print("⚠️ Running in knowledge-base only mode\n")
        
        self.college_name = college_name
        self.conversation_history = []
        
        self.knowledge_base = {
            'greetings': {
                'keywords': ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'hii', 'helo', 'hy'],
                'response': f"👋 Hello! Welcome to {college_name} Support Chatbot!\n\nI can help you with:\n• 📚 Admissions & Courses\n• 💰 Fees & Scholarships\n• 🏢 Facilities (Library, Hostel, Labs, Sports)\n• 💼 Placements & Companies\n• 📞 Contact Information\n• 🎉 Events & Campus Life\n\nWhat would you like to know?"
            },

            'about_college': {
                'keywords': ['about college', 'about your college', 'tell me about', 'know about college', 'college info', 'what is this college'],
                'response': f"🎓 **About {college_name}**\n\n{college_name} is a premier educational institution committed to excellence in education and research.\n\n✨ **Highlights:**\n• Established with modern infrastructure\n• 15+ Departments across Engineering, Management & Sciences\n• 5000+ Students\n• 200+ Experienced Faculty Members\n• State-of-the-art Facilities\n• 100+ Companies for Campus Placements\n• Active Sports & Cultural Activities\n\n📚 We offer programs in B.Tech, MBA, BBA, M.Tech, B.Sc, M.Sc and more!\n\nWhat specific information would you like to know?"
            },
            

            'admission': {
                'keywords': ['admission', 'admissions', 'apply', 'application', 'how to join', 'enroll', 'enrollment', 'how to apply'],
                'response': f"📝 **Admission Information - {college_name}**\n\n🎯 **Programs Offered:**\n• B.Tech (CSE, ECE, Mechanical, Civil, EEE)\n• MBA (Marketing, Finance, HR)\n• BBA, BCA, B.Sc, M.Tech, M.Sc\n\n✅ **Eligibility:**\n• UG Programs: Minimum 60% in 12th grade\n• PG Programs: Minimum 60% in Graduation\n\n📋 **Entrance Exams:**\n• JEE Main (for B.Tech)\n• State CET\n• College Entrance Test\n\n📅 **Important Dates:**\n• Application Opens: April 2025\n• Application Deadline: June 30, 2025\n• Admission Starts: July 2025\n\n📧 **Contact:** admissions@amityuniversity.edu\n🌐 **Apply Online:** www.amityuniversity.edu/admissions"
            },
            

            'courses': {
                'keywords': ['courses', 'programs', 'what courses', 'degrees', 'branches', 'streams', 'what do you offer'],
                'response': f"📚 **Programs Offered at {college_name}**\n\n🔧 **Engineering (B.Tech/M.Tech):**\n• Computer Science & Engineering (CSE)\n• Electronics & Communication (ECE)\n• Mechanical Engineering\n• Civil Engineering\n• Electrical & Electronics (EEE)\n\n💼 **Management:**\n• MBA (Marketing, Finance, HR, Operations)\n• BBA (Business Administration)\n\n💻 **Computer Applications:**\n• BCA (Bachelor of Computer Applications)\n\n🔬 **Sciences:**\n• B.Sc (Physics, Chemistry, Mathematics)\n• M.Sc (Various specializations)\n\n⏱️ **Duration:**\n• B.Tech/BBA/BCA/B.Sc: 3-4 years\n• MBA/M.Tech/M.Sc: 2 years"
            },
            
            
            'fees': {
                'keywords': ['fees', 'fee', 'cost', 'price', 'tuition', 'charges', 'how much', 'expensive'],
                'response': f"💰 **Fee Structure - {college_name}**\n\n💳 **Annual Fees:**\n• B.Tech/B.E: ₹75,000 - ₹1,20,000\n• MBA: ₹1,50,000 - ₹2,00,000\n• BBA/BCA: ₹60,000 - ₹80,000\n• B.Sc/M.Sc: ₹50,000 - ₹70,000\n• M.Tech: ₹80,000 - ₹1,00,000\n\n📝 **Additional Charges:**\n• Hostel: ₹40,000 - ₹60,000/year\n• Mess: ₹30,000 - ₹40,000/year\n• Transportation: ₹10,000 - ₹15,000/year\n\n🎖️ **Scholarships Available:**\n• Merit-based (Top 10%): Up to 50% waiver\n• Sports quota: 25-50% waiver\n• Need-based financial aid\n• Government scholarships\n\n📞 For detailed fee structure, contact: accounts@amityuniversity.edu"
            },
    
            'facilities': {
                'keywords': ['facilities', 'infrastructure', 'amenities', 'campus facilities', 'what facilities'],
                'response': f"🏢 **Facilities at {college_name}**\n\n📖 **Library:**\n• 24/7 Digital Library\n• 50,000+ Books & Journals\n• E-resources & Online Databases\n• Reading Rooms & Study Areas\n\n🔬 **Laboratories:**\n• Computer Labs (500+ systems)\n• Engineering Labs (Mechanical, Electronics, Electrical)\n• Research Labs with modern equipment\n\n🏠 **Hostel:**\n• Separate Boys & Girls Hostels\n• 500+ capacity each\n• AC & Non-AC rooms\n• 24/7 Security & WiFi\n• Mess with quality food\n\n⚽ **Sports:**\n• Cricket Ground & Football Field\n• Basketball & Volleyball Courts\n• Indoor Games (Badminton, Table Tennis)\n• Well-equipped Gymnasium\n\n🍽️ **Cafeteria:**\n• Multi-cuisine options\n• Hygienic & affordable\n• Open 7 AM - 10 PM\n\n📡 **Other:**\n• High-speed WiFi campus-wide\n• Medical facility\n• Transportation facility\n• Auditorium & Seminar halls"
            },
            
            'placement': {
                'keywords': ['placement', 'placements', 'job', 'jobs', 'companies', 'recruitment', 'campus placement', 'placed', 'package'],
                'response': f"💼 **Placement Record - {college_name}**\n\n🎯 **Placement Statistics:**\n• Placement Rate: 85-90%\n• Companies Visiting: 100+ annually\n• Average Package: ₹3.5 - 4.5 LPA\n• Highest Package: ₹15-18 LPA\n\n🏢 **Top Recruiters:**\n• TCS, Infosys, Wipro, Accenture\n• Tech Mahindra, Cognizant, HCL\n• Amazon, Microsoft, Google (occasional)\n• HDFC, ICICI, Axis Bank\n• Deloitte, Ernst & Young\n\n📚 **Training & Development:**\n• Pre-placement training programs\n• Soft skills development\n• Technical workshops\n• Mock interviews\n• Resume building sessions\n• Internship opportunities\n\n📧 **Contact Placement Cell:**\nplacements@amityuniversity.edu"
            },
            
            'scholarship': {
                'keywords': ['scholarship', 'scholarships', 'financial aid', 'concession', 'fee waiver'],
                'response': f"🎖️ **Scholarships at {college_name}**\n\n💡 **Available Scholarships:**\n\n1️⃣ **Merit Scholarship:**\n   • Top 10% students: 50% fee waiver\n   • Top 20% students: 25% fee waiver\n   • Based on entrance exam/12th marks\n\n2️⃣ **Sports Scholarship:**\n   • National level: 50% waiver\n   • State level: 25% waiver\n   • District level: 10% waiver\n\n3️⃣ **Need-based Aid:**\n   • For economically weaker sections\n   • Up to 40% fee concession\n\n4️⃣ **Government Scholarships:**\n   • SC/ST/OBC scholarships\n   • Minority scholarships\n   • Girl child scholarships\n\n📝 **How to Apply:**\n• Fill scholarship form during admission\n• Submit required documents\n• Scholarships reviewed annually\n\n📞 Contact: scholarships@amityuniversity.edu"
            },
            
            'library': {
                'keywords': ['library', 'books', 'reading room', 'library timing'],
                'response': f"📖 **Library - {college_name}**\n\n📚 **Collection:**\n• 50,000+ Books\n• 5,000+ Journals & Magazines\n• E-books & Online Resources\n• Digital Library Access\n• Research Databases\n\n⏰ **Timings:**\n• Physical Library: 8:00 AM - 8:00 PM\n• Digital Library: 24/7 Access\n• Reading Room: 6:00 AM - 11:00 PM\n\n📱 **Services:**\n• Book Issue/Return\n• Reference Section\n• Photocopy facility\n• Internet & Computer access\n• Study cubicles\n\n📋 **Rules:**\n• ID card mandatory\n• Maximum 3 books for 15 days\n• Late return fine: ₹5 per day\n• Maintain silence\n\n📧 library@amityuniversity.edu"
            },
            
            'hostel': {
                'keywords': ['hostel', 'accommodation', 'room', 'residence', 'pg', 'staying'],
                'response': f"🏠 **Hostel Facilities - {college_name}**\n\n🛏️ **Accommodation:**\n• Separate Boys & Girls Hostels\n• Single, Double, Triple sharing rooms\n• AC & Non-AC options\n• Attached washrooms\n\n💰 **Hostel Fees:**\n• Non-AC: ₹40,000/year\n• AC: ₹60,000/year\n• Mess charges: ₹30,000-40,000/year\n• Security deposit: ₹10,000 (refundable)\n\n🍽️ **Mess Facilities:**\n• 4 meals daily (Breakfast, Lunch, Snacks, Dinner)\n• Hygienic & nutritious food\n• Special diet on request\n• Separate veg & non-veg menus\n\n✨ **Amenities:**\n• 24/7 Security & CCTV\n• High-speed WiFi\n• Common rooms with TV\n• Laundry service\n• Medical facility nearby\n• Recreational areas\n\n📝 **Admission:**\nApply after course admission confirmation\n\n📞 hostel@amityuniversity.edu"
            },
            
            'exam': {
                'keywords': ['exam', 'exams', 'examination', 'test', 'midterm', 'final exam'],
                'response': f"📝 **Examination System - {college_name}**\n\n📅 **Exam Schedule:**\n• Mid-term Exams: October & March\n• End-term Exams: November/December & April/May\n• Internal Assessments: Throughout semester\n\n📊 **Evaluation Pattern:**\n• Mid-term: 30 marks\n• End-term: 50 marks\n• Internal Assessment: 20 marks\n• Total: 100 marks\n\n⏰ **Important Dates:**\n• Exam schedule published 1 month prior\n• Hall tickets: 1 week before exams\n• Results: Within 30 days of exams\n\n📋 **Exam Rules:**\n• ID card & Hall ticket mandatory\n• Minimum 75% attendance to appear\n• No electronic devices allowed\n• Academic integrity strictly enforced\n\n🔄 **Revaluation:**\n• Apply within 7 days of result\n• Fee: ₹500 per subject\n• Results in 15 days\n\n📞 examinations@amityuniversity.edu"
            },
            
            'result': {
                'keywords': ['result', 'results', 'marks', 'grade', 'score', 'marksheet'],
                'response': f"🎓 **Results - {college_name}**\n\n📊 **Result Declaration:**\n• Published on college website\n• Within 30 days of exam completion\n• SMS notification to registered mobile\n\n🔐 **How to Check:**\n1. Visit: www.amityuniversity.edu/results\n2. Enter Roll Number\n3. Enter Date of Birth\n4. View/Download Result\n\n📜 **Documents Available:**\n• Online marksheet (PDF)\n• Grade sheet\n• Semester-wise results\n• Consolidated marksheet\n\n🔄 **Revaluation/Rechecking:**\n• Apply within 7 days\n• Fee: ₹500 per subject\n• Results in 15 days\n• Refund if marks increase\n\n📧 For result queries:\nexaminations@amityuniversity.edu"
            },
            
            'events': {
                'keywords': ['events', 'event', 'fest', 'festival', 'function', 'activities', 'cultural', 'tech fest'],
                'response': f"🎉 **Events & Activities - {college_name}**\n\n🎪 **Annual Events:**\n\n🔧 **TechFest (March):**\n• Technical competitions\n• Hackathons & Coding contests\n• Robotics competitions\n• Project exhibitions\n• Celebrity speakers\n\n🎭 **Cultural Fest (February):**\n• Dance & Music competitions\n• Drama & Fashion shows\n• Art exhibitions\n• Celebrity performances\n• Food stalls\n\n⚽ **Sports Week (January):**\n• Inter-department tournaments\n• Athletics meet\n• Indoor games competitions\n• Prize distribution\n\n📚 **Regular Activities:**\n• Technical workshops\n• Guest lectures\n• Industrial visits\n• Seminars & conferences\n• Club activities\n• Social service initiatives\n\n📱 Follow us on social media for updates!"
            },
            
            'contact': {
                'keywords': ['contact', 'phone', 'email', 'address', 'location', 'reach', 'call'],
                'response': f"📞 **Contact Information - {college_name}**\n\n📧 **Email Addresses:**\n• General Queries: info@amityuniversity.edu\n• Admissions: admissions@amityuniversity.edu\n• Placements: placements@amityuniversity.edu\n• Examinations: examinations@amityuniversity.edu\n• Library: library@amityuniversity.edu\n• Hostel: hostel@amityuniversity.edu\n\n📱 **Phone:**\n• Main Office: +91-141-XXXXXXX\n• Admissions: +91-141-XXXXXXX\n• Toll-free: 1800-XXX-XXXX\n\n📍 **Address:**\n{college_name}\nCollege Road, Sector-XX\nCity, State - 123456\nIndia\n\n⏰ **Office Hours:**\nMonday - Friday: 9:00 AM - 5:00 PM\nSaturday: 9:00 AM - 2:00 PM\nSunday: Closed\n\n🌐 **Website:** www.amityuniversity.edu\n📱 **Social Media:** @amityuniversity"
            },
            
            'faculty': {
                'keywords': ['faculty', 'teachers', 'professors', 'staff', 'teaching'],
                'response': f"👨‍🏫 **Faculty - {college_name}**\n\n🎓 **Qualification:**\n• 200+ Faculty Members\n• 70%+ with PhD degrees\n• Industry experts & researchers\n• International exposure\n\n✨ **Teaching Approach:**\n• Interactive learning methods\n• Practical & theory balance\n• Industry-relevant curriculum\n• Doubt clearing sessions\n• Mentorship programs\n\n📚 **Specializations:**\n• Engineering & Technology\n• Management & Business\n• Sciences & Research\n\n👥 **Student Support:**\n• Available during office hours\n• Personal mentoring\n• Career guidance\n• Project supervision\n\n🏆 **Achievements:**\n• Published research papers\n• Industry collaborations\n• Conference presentations\n• Patents & innovations"
            },
            
            'thanks': {
                'keywords': ['thanks', 'thank you', 'thankyou', 'thnx', 'thx'],
                'response': "😊 You're most welcome! Feel free to ask if you need any more information about college. Happy to help! 🎓"
            }
        }
        
        print(f"✓ {college_name} Support Bot ready! Type 'quit' to exit.\n")
    
    def find_answer(self, user_input):
        """Search knowledge base for answer"""
        user_lower = user_input.lower()
        
        for category, data in self.knowledge_base.items():
            for keyword in data['keywords']:
                if keyword in user_lower:
                    return data['response']
        
        return None
    
    def get_ai_response(self, user_input):
        """Get AI response for non-college questions"""
        if self.conversational_ai is None:
            return "I'm here to help with college-related queries! Ask me about admissions, courses, facilities, placements, fees, or any other college information. Type 'help' to see all topics!"
        
        try:
            from transformers import Conversation
            conversation = Conversation(user_input)
            result = self.conversational_ai(conversation)
            return result.generated_responses[-1]
        except:
            return "I specialize in college-related queries. Ask me about admissions, courses, facilities, placements, or type 'help' for all topics!"
    
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
                print("\n🎓 Bot: Thank you for using our support system! Good luck with your studies! 👋\n")
                break
            
            if user_input.lower() == 'help':
                print("\n📋 **I can help you with:**\n")
                print("🎓 Admissions & Eligibility")
                print("📚 Courses & Programs")
                print("💰 Fees & Scholarships")
                print("🏢 Facilities (Library, Hostel, Labs, Sports, Cafeteria)")
                print("💼 Placements & Companies")
                print("📝 Exams & Results")
                print("🎉 Events & Activities")
                print("👨‍🏫 Faculty Information")
                print("📞 Contact Information\n")
                print("Just type your question naturally!\n")
                continue
            
            if user_input.lower() == 'reset':
                self.conversation_history = []
                print("💬 Conversation reset!\n")
                continue
            
            response = self.find_answer(user_input)
            
            if response:
                print(f"🤖 Bot: {response}\n")
            else:
                ai_response = self.get_ai_response(user_input)
                print(f"🤖 Bot: {ai_response}\n")


def main():
    """Main function"""
    college_name = "Amity University"
    bot = CollegeSupportChatbot(college_name)
    bot.chat()


if __name__ == "__main__":
    main()