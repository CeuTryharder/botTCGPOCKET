# Pokemon TCG Pocket Bot

An open-source, AFK automation bot for Pokémon TCG Pocket. This bot uses ADB (Android Debug Bridge) and OpenCV (Computer Vision) to interact with an Android emulator playing the game. 

## Features
- **AFK Automation**: Run the bot completely unattended.
- **Mission Harvesting**: Automatically navigates the UI to claim missions and rewards (Coming Soon).
- **Solo Battle Farming**: Uses image recognition to loop solo battles, utilize game auto-battle sequences, and harvest EXP/Stamina (Coming Soon).

## Prerequisites
- **Python 3.8+**
- **Android Emulator**: Such as BlueStacks, Nox, or Android Studio AVD.
- **ADB (Android Debug Bridge)**

## Installation
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Open your Android emulator and launch Pokémon TCG Pocket.
2. Ensure ADB connection is enabled in your emulator settings.
3. Run the bot:
   ```bash
   python bot/main.py
   ```

## Disclaimer
> **Warning:** This bot violates the Terms of Service for Pokémon TCG Pocket. Using macros or automated tools can result in your account being permanently banned. Use at your own risk. This project is for educational purposes regarding Computer Vision and ADB interactions.

## License
Distributed under the MIT License. See `LICENSE` for more information.
