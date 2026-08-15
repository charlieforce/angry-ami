"""
Ami's Research Capability
Discovers news and topics Charlie might care about
"""
import json
import os
from src.utils import logger, get_config

class AmiResearch:
    def __init__(self):
        self.interests_path = './data/charlie_interests.json'
        self.research_log_path = './data/learning/research_discoveries.json'
        
        self.interests = self.load_interests()
        self.discoveries = self.load_discoveries()
    
    def load_interests(self):
        """Load Charlie's interests"""
        if os.path.exists(self.interests_path):
            with open(self.interests_path, 'r') as f:
                return json.load(f)
        return {}
    
    def load_discoveries(self):
        """Load previous research discoveries"""
        if os.path.exists(self.research_log_path):
            with open(self.research_log_path, 'r') as f:
                return json.load(f)
        return {"discoveries": []}
    
    def add_discovery(self, topic, source, summary, relevance):
        """Log a discovery Ami makes"""
        discovery = {
            "topic": topic,
            "source": source,
            "summary": summary,
            "relevance": relevance,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
        
        self.discoveries["discoveries"].append(discovery)
        
        with open(self.research_log_path, 'w') as f:
            json.dump(self.discoveries, f, indent=2)
        
        return discovery
    
    def get_discovery_topics(self):
        """Get topics Ami has discovered"""
        if not self.discoveries.get("discoveries"):
            return []
        
        return [d["topic"] for d in self.discoveries["discoveries"][-5:]]
    
    def generate_research_questions(self):
        """Generate questions based on discovered topics"""
        questions = [
            # Seahawks/Sports
            "Eh eh! I see say Seahawks won their last game! You watching the season?",
            "My brodda, I read say Seahawks de make some moves. Wetin you think about the team this season?",
            "I discover something about your Seahawks! They winning lately?",
            
            # Tech discoveries
            "I read something interesting about offline-first EdTech... reminds me of GII_Connect!",
            "Found an article on AI in education that's doing exactly what you're trying with GII!",
            "Saw news about a new EdTech startup in East Africa - their model different from yours?",
            
            # Africa/Sierra Leone
            "I saw some news about Sierra Leone politics. Wetin you make of the latest developments?",
            "Found an interesting article about African tech startups. Some of them moving like GII!",
            "Read about Kenya's tech scene - Quinter must be seeing some interesting things on the ground!",
            
            # US Politics & News
            "I read about new US education policy changes. Could affect how EdTech is funded!",
            "Saw something on US AI regulation - could be important for GII_Connect's future!",
            "Found an article about veteran entrepreneurship in the US - your people!",
            "US tech industry news just dropped - any implications for your work?",
            "Read about US nonprofits scaling impact - some doing similar to GII's model!",
            "Saw news on US markets - anything affecting your fundraising strategy?",
            "I discovered some US policy changes on social impact metrics - relevant to GII?",
            
            # Canada News & Politics
            "Eh eh! I read Canadian government backing more tech initiatives - good timing for GII!",
            "Found article about Canada-Africa tech partnerships - that could help you!",
            "Saw Canadian startup success story - reminds me of what you're building with GII!",
            "Read about Canadian education innovation - your homeland doing interesting things!",
            "I saw news about Vancouver tech scene - any of that relevant to TechieVet or GII_Connect?",
            "Found article on Canadian nonprofits - they scaling different from you?",
            "Saw Canadian government announcing new social impact funding - could be opportunity!",
            
            # Nonprofit/Business
            "I discovered a nonprofit doing interesting work with revenue models like GII_Connect!",
            "Found an article about sustainable nonprofits - reminded me of your 18-month profitability plan!",
            "Saw a case study on scaling EdTech in Africa - you should check it out!",
            "Read about impact measurement best practices - how does GII compare?",
            
            # Cross-borders
            "Interesting article on US-Canada tech collaboration - relevant to your work?",
            "Found news about diaspora entrepreneurs connecting Africa to North America - like you!",
            "Saw article about triple-passport holders doing interesting work - that's you!",
        ]
        
        return questions
