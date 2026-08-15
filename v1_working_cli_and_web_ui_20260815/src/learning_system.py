"""
Ami's Continuous Learning System
Learns from conversations, documents, feedback
"""
import os
import json
from datetime import datetime
from src.utils import logger, get_config

class LearningSystem:
    def __init__(self):
        self.learning_log_path = get_config('AMI_LEARNING_LOG_PATH', './data/learning/')
        self.conversation_log_path = get_config('AMI_CONVERSATION_LOG_PATH', './data/conversations/')
        self.profile_path = './data/charlie_profile.json'
        
        os.makedirs(self.learning_log_path, exist_ok=True)
        os.makedirs(self.conversation_log_path, exist_ok=True)
        
        # Load Charlie's profile
        self.charlie_profile = self.load_profile()
    
    def load_profile(self):
        """Load Charlie's profile"""
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        return {}
    
    def log_conversation(self, user_input, ami_response):
        """Log each conversation for learning"""
        timestamp = datetime.now().isoformat()
        
        conversation_entry = {
            'timestamp': timestamp,
            'user_input': user_input,
            'ami_response': ami_response
        }
        
        log_file = os.path.join(self.conversation_log_path, f"conversation_{datetime.now().strftime('%Y%m%d')}.jsonl")
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(conversation_entry) + '\n')
    
    def log_learning(self, insight):
        """Log new insight or learning"""
        timestamp = datetime.now().isoformat()
        
        learning_entry = {
            'timestamp': timestamp,
            'insight': insight
        }
        
        log_file = os.path.join(self.learning_log_path, f"learning_{datetime.now().strftime('%Y%m%d')}.jsonl")
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(learning_entry) + '\n')
    
    def get_proactive_questions(self):
        """Generate proactive questions Ami can ask"""
        questions = [
            # GII questions
            "How's the GII scaling going? You targeting 1,500 beneficiaries this year, yeah?",
            "Any new grants coming through? You were tracking LINGUA Africa, AWS Imagine, D-Prize...",
            "How's Quinter doing with Kenya operations? Any challenges we need to address?",
            "Bo Hub reaching 4,600 students? That's ambitious! How's the team holding up?",
            
            # GII_Connect questions
            "GII_Connect moving forward? Have you done those NGO validation conversations yet?",
            "How's the commercial strategy looking? Still targeting that $50K-$100K ARR by end of 2026?",
            "Nelson and Jackson making progress on the platform? Any blockers?",
            
            # TechieVet questions
            "TechieVet MVP coming Q4 2026? How's that veteran market looking?",
            "You taking full ownership of TechieVet now? How's that feeling?",
            "Any veteran community partnerships forming for TechieVet?",
            
            # Personal questions
            "How's the Spanish coming along? You practicing?",
            "Freetown property renovation moving? Any updates?",
            "How's the travel memoir coming with Emmanuel?",
            "You maintaining those Army discipline habits? Sleep, exercise, focus?",
            
            # Relationship questions
            "How's Baby Laz doing? Family all good?",
            "Kiana keeping you accountable on the goals?",
            "When's your next trip to Freetown or Kenya?",
            
            # Reflection questions
            "Biggest win this week? We need to celebrate something!",
            "Any learnings from GII this week that changed how you think?",
            "What's been the hardest part of managing 7 projects simultaneously?",
        ]
        
        return questions
