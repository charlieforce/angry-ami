"""
Load Ami's knowledge bases at startup
"""
import os
from pathlib import Path
from src.utils import logger, get_config

class KnowledgeLoader:
    def __init__(self):
        self.kb_path = get_config('AMI_KNOWLEDGE_BASE_PATH', './data/knowledge_bases/')
        self.knowledge_bases = {}
        
    def load_all(self):
        """Load all knowledge bases"""
        logger.info("Loading knowledge bases...")
        
        kb_files = {
            'gii': 'gii_kb.md',
            'gii_connect': 'gii_connect_kb.md',
            'techievert': 'techievert_kb.md',
            'global_impact_innovators': 'global_impact_innovators_kb.md',
            'learning_system': 'learning_system.md',
            'knowledge_index': 'knowledge_index.md'
        }
        
        for key, filename in kb_files.items():
            filepath = os.path.join(self.kb_path, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.knowledge_bases[key] = f.read()
                logger.info(f"✓ Loaded {key} knowledge base")
            else:
                logger.warning(f"✗ Missing {filename}")
        
        return self.knowledge_bases
    
    def get(self, key):
        """Get a specific knowledge base"""
        return self.knowledge_bases.get(key, None)
    
    def search(self, query):
        """Search across knowledge bases"""
        results = {}
        query_lower = query.lower()
        
        for key, content in self.knowledge_bases.items():
            if query_lower in content.lower():
                results[key] = content
        
        return results
