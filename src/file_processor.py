"""
Process uploaded documents for Ami's learning
Handles: PDF, Word, TXT, images (with OCR)
"""
import os
import json
from pathlib import Path
from datetime import datetime

class FileProcessor:
    def __init__(self):
        self.upload_dir = './data/uploads'
        self.knowledge_dir = './data/knowledge_bases'
        
        # Create upload directory if it doesn't exist
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)
    
    def process_file(self, file_path):
        """Process uploaded file and extract text"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.txt':
            return self.read_text(file_path)
        elif file_ext == '.pdf':
            return self.read_pdf(file_path)
        elif file_ext == '.docx':
            return self.read_docx(file_path)
        else:
            return None
    
    def read_text(self, file_path):
        """Read plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading text file: {e}")
            return None
    
    def read_pdf(self, file_path):
        """Read PDF file - basic support"""
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except ImportError:
            print("PyPDF2 not installed. Install with: pip install PyPDF2")
            return None
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    
    def read_docx(self, file_path):
        """Read Word document"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except ImportError:
            print("python-docx not installed. Install with: pip install python-docx")
            return None
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return None
    
    def save_to_knowledge_base(self, filename, content):
        """Save extracted content to knowledge base"""
        try:
            # Create a new knowledge base file
            kb_filename = f"uploaded_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            kb_path = os.path.join(self.knowledge_dir, kb_filename)
            
            # Format as markdown
            formatted_content = f"""# Uploaded Document: {filename}

**Uploaded:** {datetime.now().isoformat()}

## Content

{content}
"""
            
            with open(kb_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            return {
                'success': True,
                'filename': kb_filename,
                'path': kb_path,
                'size': len(content)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
