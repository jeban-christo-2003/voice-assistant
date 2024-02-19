import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import random
import cv2
import mediapipe as mp
import pyautogui
import subprocess
import os
import datetime

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the pyautogui settings
pyautogui.FAILSAFE = False  # Disable the fail-safe feature

# Initialize the MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Flag to control hand movement
hand_movement_on = False

# Flag to control typing in command prompt or browser
typing_in_command_prompt = False

# Counter for consecutive failed voice recognitions
failed_attempts = 0

# Function to speak a given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process voice commands
# Function to process voice commands
def process_command(command):
    global hand_movement_on, typing_in_command_prompt, failed_attempts
    if "open spotify" in command:
        speak("Opening Spotify")
        open_spotify()
        failed_attempts = 0
    elif "close spotify" in command:
        speak("Closing Spotify")
        close_spotify()
        failed_attempts = 0
    elif "play favorite song" in command:
        speak("Playing your favorite song")
        play_favorite_song()
        failed_attempts = 0
    elif "pause" in command:
        speak("Pausing playback")
        pause_playback()
        failed_attempts = 0
    elif "forward" in command:
        speak("Forwarding playback by 10 seconds")
        forward_playback()
        failed_attempts = 0
    elif "next" in command:
        speak("Playing the next song")
        play_next_song()
        failed_attempts = 0
    elif "no hand" in command:
        speak("Turning off hand movement")
        hand_movement_on = False
        failed_attempts = 0
    elif "hand" in command:
        speak("Turning on hand movement")
        hand_movement_on = True
        failed_attempts = 0
    elif "type" in command and not typing_in_command_prompt:
        speak("What should I type?")
        typing_in_command_prompt = True
        failed_attempts = 0
    elif "stop typing" in command:
        speak("Stopping typing")
        typing_in_command_prompt = False
        failed_attempts = 0
    elif "open command prompt" in command:
        speak("Opening command prompt")
        open_command_prompt()
        failed_attempts = 0
    elif "close command prompt" in command:
        speak("Closing command prompt")
        close_command_prompt()
        failed_attempts = 0
    elif "open browser" in command:
        speak("Opening browser")
        open_browser()
        failed_attempts = 0
    elif "close browser" in command:
        speak("Closing browser")
        close_browser()
        failed_attempts = 0
    elif "date" in command:
        speak("Today is " + get_date())
        failed_attempts = 0
    elif "day" in command:
        speak("Today is " + get_day())
        failed_attempts = 0
    elif "time" in command:
        speak("The current time is " + get_time())
        failed_attempts = 0
    elif "year" in command:
        speak("The current year is " + get_year())
        failed_attempts = 0
    elif "week" in command:
        speak("Today is in week " + get_week())
        failed_attempts = 0
    elif "quit" in command:
        speak("Ok, bye!")
        exit()  # Terminate the program
    elif typing_in_command_prompt:
        speak("Typing: " + command)
        type_text(command)
        pyautogui.press('enter')  # Press enter after typing the command
        failed_attempts = 0
    else:
        failed_attempts += 1
        if failed_attempts >= 2:
            speak("I didn't understand that. Please type your command.")
            command = input("Type your command: ").lower()
            failed_attempts = 0
            process_command(command)
        else:
            speak("Sorry, I didn't understand that.")
# Function to get today's date
def get_date():
    return datetime.datetime.now().strftime("%B %d, %Y")

# Function to get today's day
def get_day():
    return datetime.datetime.now().strftime("%A")

# Function to get current time
def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

# Function to get current year
def get_year():
    return datetime.datetime.now().strftime("%Y")

# Function to get current week number
def get_week():
    return datetime.datetime.now().strftime("%U")

# Function to open Spotify web player in a web browser
def open_spotify():
    webbrowser.open("https://open.spotify.com/")

# Function to close Spotify web player
def close_spotify():
    os.system("taskkill /F /IM spotify.exe")  # Close Spotify using taskkill

# Function to play a favorite song on Spotify web player
def play_favorite_song():
    # Replace the URL with your favorite song's Spotify URL
    song_url=""
    webbrowser.open(song_url)

# Function to pause playback (not applicable for web player)
def pause_playback():
    pass

# Function to forward playback by 10 seconds (not applicable for web player)
def forward_playback():
    pass

# Function to play next song (not applicable for web player)
def play_next_song():
    pass

# Function to control mouse cursor based on hand movements
def control_hand_movement():
    global hand_movement_on
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while hand_movement_on:
            # Capture frame from webcam
            success, image = cap.read()
            if not success:
                break

            # Convert the image to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process hand detection
            results = hands.process(image_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    # Convert normalized coordinates to pixel coordinates
                    ih, iw, _ = image.shape
                    x = int(index_finger_tip.x * iw)
                    y = int(index_finger_tip.y * ih)

                    # Simulate left mouse button click if index finger is raised
                    if y < 200:  # Adjust threshold as needed
                        pyautogui.click(x, y, button='left')

                    # Simulate right mouse button click if thumb is raised
                    if y > 400:  # Adjust threshold as needed
                        pyautogui.click(x, y, button='right')

            cv2.imshow('Hand Tracking', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Function to type text into the command prompt or a web browser
def type_text(text):
    if typing_in_command_prompt:
        subprocess.Popen("cmd.exe").communicate(input=text.encode())
    else:
        pyautogui.typewrite(text)

# Function to open command prompt
def open_command_prompt():
    subprocess.Popen("cmd.exe")

# Function to close command prompt
def close_command_prompt():
    os.system("taskkill /im cmd.exe /f")

# Function to open browser
def open_browser():
    webbrowser.open("https://www.google.com")

# Function to close browser
def close_browser():
    os.system("taskkill /im chrome.exe /f")  # Close Chrome browser using taskkill

# Main program
if __name__ == "__main__":
    # Open webcam
    cap = cv2.VideoCapture(0)

    speak("Hello, how would you like to input commands? Voice or keyboard?")
    while True:
        input_method = input("Voice or keyboard? ").lower()
        if input_method == "voice":
            speak("You chose voice input. Please start speaking.")
            break
        elif input_method == "keyboard":
            speak("You chose keyboard input. Please type your command.")
            break
        else:
            speak("Invalid input. Please choose voice or keyboard.")

    if input_method == "voice":
        while True:
            command = listen()
            if command:
                process_command(command)
            if hand_movement_on:
                control_hand_movement()
    elif input_method == "keyboard":
        while True:
            command = input("Type your command: ").lower()
            process_command(command)
            if hand_movement_on:
                control_hand_movement()

    # Release webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
