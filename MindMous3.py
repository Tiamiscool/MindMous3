import pyautogui
import cv2
import mediapipe as mp
import math
import webbrowser as wb
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cam = input("Enter Specified Camera(0 for built in Webcam, the rest for others): ")
cam = int(cam)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

language = "en"


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Define my_drawing_specs
my_drawing_specs = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1)

# Initialize Pose
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    # Initialize Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    # Initialize Hands
    mphands = mp.solutions.hands
    hands = mphands.Hands()

    # Set a lower frame size
    frame_width, frame_height = 2000, 2000

    cap = cv2.VideoCapture(cam)  # replace "video_path" with "0" for webcam access
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        exit()

    frame_count = 0
    frame_skip = 3  # Process every 3rd frame

    # Initialize prev_upper_lip_y outside the loop
    prev_upper_lip_y = None

    while True:
        count = 0
        ret, img = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        img_rgb = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

        # Resize frame
        img_rgb = cv2.resize(img_rgb, (frame_width, frame_height))


        # Hand detection
        results_hands = hands.process(img_rgb)

        currentVol = volume.GetMasterVolumeLevelScalar() * 100
        currentVol = currentVol/100
        add10 = currentVol + (2/100)
        remove10 = currentVol - (2/100)

        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP]
                middle_finger_tip = hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_TIP]
                pinky_finger_tip = hand_landmarks.landmark[mphands.HandLandmark.PINKY_TIP]
                ring_finger_tip = hand_landmarks.landmark[mphands.HandLandmark.RING_FINGER_TIP]

                thumb_tip = hand_landmarks.landmark[mphands.HandLandmark.THUMB_TIP]
                thumb_tip_x, thumb_tip_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)

                index_finger_tip_x, index_finger_tip_y = int(index_finger_tip.x * frame_width), int(
                    index_finger_tip.y * frame_height)
                middle_finger_tip_x, middle_finger_tip_y = int(middle_finger_tip.x * frame_width), int(
                    middle_finger_tip.y * frame_height)
                pinky_finger_tip_x, pinky_finger_tip_y = int(pinky_finger_tip.x * frame_width), int(
                    pinky_finger_tip.y * frame_height)
                ring_finger_tip_x, ring_finger_tip_y = int(ring_finger_tip.x * frame_width), int(
                    ring_finger_tip.y * frame_height)

                x = index_finger_tip_x
                y = (index_finger_tip_y/3) 

                ##print("x: " + str(x))
                ##print("y: " + str(y))

                distance1 = math.sqrt((index_finger_tip_x - thumb_tip_x) ** 2 + (index_finger_tip_y - thumb_tip_y) ** 2)
                distance2 = math.sqrt((middle_finger_tip_x - thumb_tip_x) ** 2 + (middle_finger_tip_y - thumb_tip_y) ** 2)
                distance3 = math.sqrt((ring_finger_tip_x - thumb_tip_x) ** 2 + (ring_finger_tip_y - thumb_tip_y) ** 2)

                
                
                # Set a threshold for fingertip touching
                touch_threshold = 41.5  # Adjust as needed

                pyautogui.moveTo(x, y, duration = 0)

                action = ""

                if index_finger_tip_y < middle_finger_tip_y and middle_finger_tip_y > index_finger_tip_y and thumb_tip_x < index_finger_tip_x:
                    action = "true"
                    print(action)
                elif thumb_tip_x > index_finger_tip_x:
                    action = "false"
                    print(action)
                    if distance1 < touch_threshold:
                        pyautogui.leftClick()
                        print("True: leftClick")
                        action = "true"
                        print(action)
                    if distance2 < touch_threshold:
                        pyautogui.rightClick()
                        print("true: rightClick")
                        action = "true"
                        print(action)
                    if distance3 < touch_threshold:
                        print("Google: True")
                        wb.open("https://www.google.com/")
                        action = "true"
                        print(action)

                if distance1 < touch_threshold:
                    pyautogui.leftClick()
                    print("True: leftClick")
                if distance2 < touch_threshold:
                    pyautogui.rightClick()
                    print("true: rightClick")
                if distance3 < touch_threshold:
                    print("Google: True")
                    wb.open("https://www.google.com/")
                



                #if thumb_tip_y < index_finger_tip_y and thumb_tip_y < middle_finger_tip_y and thumb_tip_x < index_finger_tip_x and pinky_finger_tip_y < index_finger_tip_y and pinky_finger_tip_y < index_finger_tip_y:
                 #   wb.open("https://WWW.Google.com/")
                if pinky_finger_tip_y < middle_finger_tip_y and thumb_tip_y > pinky_finger_tip_y and action == "false":
                    print("True: volume")
                    print("Current Volume:", (currentVol*100))  # For debugging
                    new_vol = min(add10, 1.0)  # Ensure new volume doesn't exceed 1.0
                    volume.SetMasterVolumeLevelScalar(new_vol, None)
                
                if pinky_finger_tip_y > middle_finger_tip_y and thumb_tip_y < pinky_finger_tip_y and action == "false":
                    print("True: volume")
                    print("Current Volume:", (currentVol*100))  # For debugging
                    new_vol = max(remove10, 0.0)  # Ensure new volume doesn't exceed 1.0
                    volume.SetMasterVolumeLevelScalar(new_vol, None)


                mp_drawing.draw_landmarks(img_bgr, hand_landmarks, mphands.HAND_CONNECTIONS)



        cv2.imshow('video:', img_bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




