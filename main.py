import cv2
from pyzbar import pyzbar
import time
from datetime import datetime
import sys

# ANSI color codes for console output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'

def get_timestamp():
    """
    Returns a formatted timestamp string in the format [dd.mm.yyyy, hh:mm:ss]
    """
    now = datetime.now()
    timestamp = now.strftime("[%d.%m.%Y, %H:%M:%S]")
    return timestamp

def list_available_cameras():
    """
    List all available camera devices
    Returns a list of available camera indices
    """
    try:
        available_cameras = []
        # Try to open each camera index until we get an error
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.isOpened():
                break
            else:
                available_cameras.append(index)
            cap.release()
            index += 1
    except Exception as e:
        pass
    
    return available_cameras

def read_barcodes(frame):
    """
    Read barcodes from the given frame and return the frame with barcodes highlighted
    and the decoded barcode values
    """
    try:
        barcodes = pyzbar.decode(frame)
        barcode_values = []
        
        for barcode in barcodes:
            # Extract the barcode data as a string
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            
            # Add to our list of values
            barcode_values.append((barcode_data, barcode_type))
            
            # Draw a rectangle around the barcode in RED
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red color (BGR)
            
            # Put the barcode data and type UNDER the box
            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(frame, text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)  # Red text, positioned below the box
        
        return frame, barcode_values
    except Exception as e:
        log = get_timestamp()
        print(f"{CYAN}{log}{RED} Error decoding barcode: {str(e)}{RESET}")
        return frame, []

def main():
    # Define the logo
    logo = """

██████╗ ██╗   ██╗██████╗ ███████╗ █████╗ ██████╗ ███████╗██████╗ 
██╔══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗
██████╔╝ ╚████╔╝ ██████╔╝█████╗  ███████║██║  ██║█████╗  ██████╔╝
██╔═══╝   ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██║██║  ██║██╔══╝  ██╔══██╗
██║        ██║   ██║  ██║███████╗██║  ██║██████╔╝███████╗██║  ██║
╚═╝        ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                 
"""

    # Print the logo
    print(GREEN, logo, RESET)

    # Redirect stderr to suppress zbar assertion errors
    original_stderr = sys.stderr
    sys.stderr = open('zbar_errors.log', 'w')
    
    try:
        # List available cameras
        available_cameras = list_available_cameras()
        
        if not available_cameras:
            log = get_timestamp()
            print(f"{RED} No cameras detected on your system.{RESET}")
            return
        
        # Let the user choose a camera
        log = get_timestamp()
        print(f"Available cameras:")
        for i, cam_index in enumerate(available_cameras):
            print(f"{i+1}. Camera {cam_index}")
        
        choice = 0
        while choice < 1 or choice > len(available_cameras):
            try:
                choice = int(input(f"Select a camera (1-{len(available_cameras)}): "))
            except ValueError:
                log = get_timestamp()
                print(f"Please enter a valid number.")
        
        # Initialize the selected webcam
        camera_index = available_cameras[choice-1]
        cap = cv2.VideoCapture(camera_index)
        
        # Check if the webcam is opened correctly
        if not cap.isOpened():
            log = get_timestamp()
            print(f"{RED} Error: Could not open camera {camera_index}.{RESET}")
            return
        
        log = get_timestamp()
        print(f"Barcode Reader Started. Press 'q' to quit.")
        print(f"Place a barcode in front of the camera...")
        print(f"{CYAN}{log}{RESET} Using camera {camera_index}")
        
        # Set to keep track of already seen barcodes to avoid duplicates
        seen_barcodes = set()
        last_detection_time = time.time()
        
        while True:
            # Read a frame from the webcam
            ret, frame = cap.read()
            
            if not ret:
                log = get_timestamp()
                print(f"{CYAN}{log}{RED} Error: Failed to capture image{RESET}")
                break
            
            # Process the frame to find barcodes
            frame, barcode_values = read_barcodes(frame)
            
            # Display the frame
            cv2.imshow('Barcode Reader', frame)
            
            # Print new barcode values with a cooldown to avoid spam
            current_time = time.time()
            if barcode_values and current_time - last_detection_time > 2:  # 2 second cooldown
                for barcode_data, barcode_type in barcode_values:
                    if barcode_data not in seen_barcodes:
                        log = get_timestamp()
                        print(f"{CYAN}{log}{RESET} Barcode detected: {barcode_data} (Type: {barcode_type})")
                        seen_barcodes.add(barcode_data)
                last_detection_time = current_time
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release the webcam and close all windows
        log = get_timestamp()
        print(f"{CYAN}{log}{RESET} Closing barcode reader...")
        cap.release()
        cv2.destroyAllWindows()
    
    finally:
        # Restore stderr
        sys.stderr = original_stderr

if __name__ == "__main__":
    main()
