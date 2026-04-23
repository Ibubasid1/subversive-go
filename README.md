# Go MCTS AI
## A Go adversarial AI agent implemented using Monte Carlo Tree Search. Runs a 9x9 Go board that compares a Monte Carlo Tree Search AI vs a random move baseline AI. 

To clone: 
```
git clone https://github.com/Ibubasid1/subversive-go.git
```
After cloning the repo, create a virtual environment then install requirements:
 
```
python -m venv venv
```
EITHER:
```
venv\Scripts\activate
```
(windows)

OR
```
source venv/bin/activate
```
(mac/linux)

Install dependencies:
```
pip install -r requirements.txt
```
 


When you add or remove dependencies, update the requirements file with:
```
pip freeze > requirements.txt
```
This gets all current dependencies installed and saves them to requirements.txt. This allows other users to download the new dependencies. 
Run: `pip install -r requirements.txt` every time you pull a new commit to make sure you have the latest dependencies. 