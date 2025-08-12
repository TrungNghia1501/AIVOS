AI Receptionist Tracking System
This system uses a webcam and the MediaPipe library to detect the presence of a person at a close distance (approximately 1 meter). It triggers a status flag that can be used to control the display of a virtual AI receptionist on a screen, creating an automated and interactive customer experience.

1. Prerequisites
To run this system, you'll need the following:

Operating System: Linux, Windows, or macOS.

Python: Version 3.10.10 or newer.

Webcam: A working webcam connected to your machine.

Resources: Sufficient CPU and RAM to handle real-time video processing.

2. Installation
First, clone this repository (or copy the ai_receptionist_tracker.py file).

Then, install the required Python libraries using pip:

Bash

pip install -r requirements.txt

3. Configuration and Calibration
This step is crucial for the system to work accurately in your specific environment.

a. Camera Configuration
Open the ai_receptionist_tracker.py file and check the following line:

Python

cap = cv2.VideoCapture(0)
The 0 is the index of your default webcam. If you are using a different camera, you may need to change this number (e.g., to 1, 2, etc.).

b. Distance Calibration
To define the 1-meter distance, you must calibrate the distance_threshold value.

Open the ai_receptionist_tracker.py file and uncomment the print statement by removing the # at the beginning of the line:

Python

print(f"Relative person height: {person_height}")
Run the script from your terminal:

Bash

python ai_receptionist_tracker.py
Stand approximately 1 meter away from the webcam and observe the Relative person height values being printed in the terminal.

Note a stable value. For example, if you see the value 0.45 consistently, use that.

Stop the script, and set the distance_threshold value in the code:

Python

distance_threshold = 0.45  # Set your calibrated value here
Re-comment the print statement to keep the console clean.

Run the script again to test your new threshold. The AI should activate when you move closer than 1 meter.

4. Usage
The system is designed to run continuously in the background.

When a person approaches within the calibrated distance, the system will print:

Customer detected! Activating the AI receptionist...
When the person moves away, it will print:

Customer has left. Deactivating the AI receptionist...
Notes:
To run the script in the background on Linux, you can use nohup and &:

Bash

nohup python ai_receptionist_tracker.py &
Ensure your machine does not go to sleep or turn off the screen, as this could interrupt the webcam's video stream.

5. Integration with Your AI System
The core purpose of this script is to provide a trigger signal. To integrate it with your AI character, focus on the TODO sections:

Python

# Logic to activate or deactivate the AI
if person_is_close and not ai_active:
    # ...
    # TODO: Add your code here to display the AI character
    # For example: my_ai_system.show_character()

elif not person_is_close and ai_active:
    # ...
    # TODO: Add your code here to hide the AI character
    # For example: my_ai_system.hide_character()
You can replace the TODO lines with your own function calls or API requests that communicate with your AI display software.