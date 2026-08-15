# ANGRY AMI - WORKING VERSION CHECKPOINT
## Date: August 15, 2026

### WHAT'S WORKING ✓

1. **CLI Chat Interface** (`./run_ami.sh`)
   - Krio/English language switching
   - Proactive questions about Charlie's interests
   - Research discovery questions
   - No hallucinations - honest about what she knows
   - Personality and authentication working

2. **API Server** (`./start_api.sh`)
   - Flask backend running on http://localhost:5000
   - Hermes Agent initialization
   - All endpoints functional:
     - /api/health
     - /api/chat
     - /api/profile
     - /api/interests
     - /api/greeting

3. **Web UI** (React)
   - Beautiful chat interface at http://localhost:3000
   - Message bubbles, timestamps
   - Send button working
   - Professional design

4. **Knowledge Bases**
   - 6 knowledge bases loaded (GII, GII_Connect, TechieVet, etc.)
   - Charlie's profile (charlie_profile.json)
   - Charlie's interests (charlie_interests.json)
   - Research system initialized

### HOW TO RUN (Terminal 1)
```bash
cd ~/Desktop/angry_ami_project
./start_api.sh
```

### HOW TO RUN (Terminal 2)
```bash
cd ~/Desktop/angry_ami_project/web
npm start
```

### KNOWN ISSUES
- Connection between React frontend and Flask backend sometimes requires both terminals
- Need to wait for Hermes Agent to initialize before chatting

### NEXT STEPS (NOT YET IMPLEMENTED)
- Electron desktop app wrapper
- Mobile app (React Native)
- Slack integration
- Document upload learning system
- Google Drive/Calendar integration

### FILES TO NOT LOSE
- src/agent.py (Main agent)
- src/ami_personality.py (Personality system)
- src/learning_system.py (Learning)
- src/api_server.py (Flask API)
- data/charlie_profile.json (Charlie's info)
- data/charlie_interests.json (What Ami researches)
- web/src/App.js (React UI)
- .env (Configuration)
- requirements.txt (Python dependencies)
