# travel-agent

# backend setup

cd backend/
python3 -m venv agenv
source agenv/bin/activate
pip3 install -r requirements.txt

<!-- python3 agent.py -->

uvicorn main:app --reload