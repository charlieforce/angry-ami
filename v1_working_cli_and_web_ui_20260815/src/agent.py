"""
ANGRY AMI HERMES AGENT
Main orchestrator - HERMES is the foundation, Ami is built ON it
"""
import os
import sys
import logging
import random
from dotenv import load_dotenv
import google.generativeai as genai

from src.utils import setup_logging, ensure_directories, get_config, logger
from src.knowledge_loader import KnowledgeLoader
from src.ami_personality import AmiPersonality
from src.ami_capabilities import AmiCapabilities
from src.learning_system import LearningSystem
from src.google_integration import GoogleIntegration

class HermesAgent:
    """
    HERMES Agent - Orchestration Manager for Angry Ami
    """
    
    def __init__(self):
        """Initialize Hermes Agent with all systems"""
        logger.info("=" * 80)
        logger.info("INITIALIZING HERMES AGENT FOR ANGRY AMI")
        logger.info("=" * 80)
        
        ensure_directories()
        load_dotenv()
        
        if get_config('HERMES_ENABLED') != 'true':
            logger.error("HERMES IS DISABLED - CANNOT PROCEED")
            sys.exit(1)
        
        logger.info("✓ Hermes orchestration enabled")
        logger.info("✓ Strict mode: " + get_config('HERMES_STRICT_MODE'))
        logger.info("✓ Hack detection: " + get_config('HERMES_HACK_DETECTION'))
        
        gemini_key = get_config('GEMINI_API_KEY')
        if not gemini_key:
            logger.error("GEMINI_API_KEY not found in .env")
            sys.exit(1)
        
        genai.configure(api_key=gemini_key)
        logger.info("✓ Gemini API configured")
        
        self.knowledge_loader = KnowledgeLoader()
        kbs = self.knowledge_loader.load_all()
        logger.info(f"✓ Loaded {len(kbs)} knowledge bases")
        
        self.personality = AmiPersonality()
        logger.info("✓ Ami personality initialized (Krio/English)")
        
        self.capabilities = AmiCapabilities(self.knowledge_loader)
        logger.info("✓ Ami capabilities initialized")
        
        self.learning = LearningSystem()
        logger.info("✓ Learning system initialized")
        
        self.google = GoogleIntegration()
        logger.info("✓ Google integration initialized")
        
        self.model = genai.GenerativeModel(
            model_name=get_config('GEMINI_MODEL', 'gemini-2.5-flash')
        )
        
        self.system_prompt = self.personality.get_personality_system_prompt()
        logger.info("✓ Ami personality system prompt loaded")
        
        logger.info("=" * 80)
        logger.info("HERMES AGENT FULLY INITIALIZED")
        logger.info("=" * 80)
    
    def chat(self, user_input, silent=True):
        """Chat with Ami through Hermes orchestration"""
        if not silent:
            logger.info(f"User: {user_input}")
        
        language = self.personality.get_language(user_input)
        full_prompt = f"{self.system_prompt}\n\nUser: {user_input}"
        
        try:
            response = self.model.generate_content(full_prompt)
            ami_response = response.text
            self.learning.log_conversation(user_input, ami_response)
            return ami_response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return "Sorry, I ran into an error. Let me get back to you."
    
    def get_proactive_opener(self):
        """Get a random proactive question Ami wants to ask"""
        questions = self.learning.get_proactive_questions()
        return random.choice(questions)
    
    def interactive_chat(self):
        """Start interactive chat session - CLEAN UI"""
        logging.getLogger('AmiAgent').setLevel(logging.WARNING)
        
        print(self.personality.format_greeting())
        print()
        
        # Track conversation count for proactive questions
        message_count = 0
        
        while True:
            try:
                sys.stdout.write("You: ")
                sys.stdout.flush()
                
                user_input = input().strip()
                
                if not user_input:
                    # Every 5 messages with no input, Ami asks a proactive question
                    message_count += 1
                    if message_count % 5 == 0:
                        proactive_q = self.get_proactive_opener()
                        print(f"\nAmi: {proactive_q}\n")
                    continue
                
                message_count = 0
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nAmi: No wahala! Holla soon, Charlie is DeMan! 🔥\n")
                    break
                
                response = self.chat(user_input, silent=True)
                print(f"\nAmi: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nAmi: See you later, Charlie is DeMan! 🔥\n")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    """Main entry point"""
    agent = HermesAgent()
    agent.interactive_chat()

if __name__ == "__main__":
    main()
