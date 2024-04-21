# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python."
    exit 1
fi

# Install Python packages
pip install pyautogui opencv-python mediapipe pycaw comtypes

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "Failed to install one or more Python packages."
    exit 1
fi

echo "Python packages installed successfully."
