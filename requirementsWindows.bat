pip install pyautogui opencv-python mediapipe pycaw 
if %errorlevel% == 0 (
python3 MindMous3.py
) else (
echo Please Install Python
)
