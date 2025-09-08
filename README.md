# 🐱 Pet Game

A virtual pet game built with **Pygame**.  
The player takes care of a cat by feeding, playing, and interacting with it.  
The game includes saving/loading, animations, and a simple UI system.
<img width="362" height="263" alt="image" src="https://github.com/user-attachments/assets/05e2bcc9-78de-4e09-beef-69874548058c" />

---

## 🎮 Features
- Cute cat animations (hungry, play, sleepy, touched, normal)
- Interaction system (touch system, needs, clouds UI)
- Saving & loading game progress
- Day/Night cycle with clock system
- UI rendering with health/mood bars

---

## 📂 Project Structure
assets/ # Images & animations
│ ├── animations/ # Cat and loading animations
│ └── images/ # Backgrounds, UI elements
data/ # Save data storage
src/
├── config/ # Configurations (game, UI, text, animation)
├── core/ # Core gameplay logic (game loop, state)
├── events/ # Event handling (input, zones)
├── renderer/ # Renderers (cat, effects, UI)
├── systems/ # Systems (resource manager, save manager, touch system)
└── main.py # Game entry point
requirements.txt # Python dependencies
README.md # Project documentation

---

## 🚀 Installation & Run
1. Clone this repository:
   ```bash
   git clone https://github.com/meyyy-G/pet-game.git
   cd pet-game
2.Install dependencies:
pip install -r requirements.txt

3.Run the game:
python src/main.py

---

### 改成带启动脚本的版本

```markdown
## 🚀 Installation & Run
1. Clone this repository:
   ```bash
   git clone https://github.com/meyyy-G/pet-game.git
   cd pet-game
2.Install dependencies:
pip install -r requirements.txt
Run the game:
chmod +x run_game.sh
./run_game.sh
(If you prefer, you can also run directly with python src/main.py)
Windows: Double-click run_game.bat

Mac/Linux:

📸 Screenshots

Main Scene	
<img width="375" height="562" alt="image" src="https://github.com/user-attachments/assets/149d2930-c54e-406f-8e59-f1d443be5b28" />

Room Scene
<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/f9419f71-09f3-4586-bebe-1e8862ebd265" />
🛠️ Tech Stack

Language: Python 3

Library: Pygame

Tools: GitHub, GitHub Desktop

📝 Future Improvements

Add sound effects and background music.

Expand interaction needs (bath, shop system).

Add more cat moods & mini-games.

Package as executable and release on itch.io.

📜 License

This project is licensed under the MIT License
.

🙋‍♀️ Author

Created by Marbiya (meyyy-G).
If you like this project, ⭐ the repo and feel free to connect!
