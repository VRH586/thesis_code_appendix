import pickle
import time
import cv2
import numpy as np
from pupil_apriltags import Detector


# Camera information, NOT CONFIGURED
#FPS = 50
RES = (1920, 1080)
camera_info = {}
# Camera Resolution
camera_info["res"] = RES
camera_info["K"] = np.array([[314.22174729465604, 0.0, 337.0278425306902],
                             [0.0, 311.4202447283487, 238.99954338265644],
                             [0.0, 0.0, 1.0]])
camera_info["D"] = np.array([[-0.03953861358665185],
                             [0.014918638704331555],
                             [-0.022402610396196412],
                             [0.00863418416543917]])

# Camera Intrinsic Matrix (3x3)
# The non-default elements of the K array, in the AprilTag specification
camera_info["params"] = [314.222, 311.420, 337.028, 239.]
# Fisheye Camera Distortion Matrix

# Fisheye flag
camera_info["fisheye"] = True
camera_info["map_1"], camera_info["map_2"] = cv2.fisheye.initUndistortRectifyMap(camera_info["K"], camera_info["D"], np.eye(3), camera_info["K"], camera_info["res"], cv2.CV_16SC2)

# Tag information
TAG_SIZE = .123
#FAMILIES = 'tag36h11, tag16h5'
FAMILIES = 'tag36h11'
#tags = Tag(TAG_SIZE, FAMILIES)


def main():
    # Initialize the camera capture
    camera = cv2.VideoCapture(0)
    camera.set(3, RES[0])  # Set horizontal resolution
    camera.set(4, RES[1])  # Set vertical resolution

    # Configure the AprilTags detector
    detector = Detector(families=FAMILIES, nthreads=4)

    # Initialize variables for calculating frame rate
    start_time = time.time()
    frame_count = 0
    
    while True:
        # Clear write_list
        write_list = ['4','4','4','4']
        
        # Capture frame from the camera
        ret, frame = camera.read()

        # Undistort the frame
        # frame = cv2.remap(frame, camera_info["map_1"], camera_info["map_2"], interpolation=cv2.INTER_LINEAR)

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags in the grayscale image
        results = detector.detect(gray, estimate_tag_pose=True, camera_params=camera_info["params"], tag_size=TAG_SIZE)

        # Draw bounding boxes and IDs on the frame
        for tag in results:
            # Add bounding rectangle
            cv2.polylines(frame, [np.int32(tag.corners)], True, (0, 255, 0), thickness=2)
            # Add Tag ID text
            cv2.putText(frame, str(tag.tag_id),
                        org=(tag.corners[0, 0].astype(int) + 10, tag.corners[0, 1].astype(int) + 10),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.8,
                        color=(0, 0, 255),
                        thickness=3)
            cv2.circle(frame, tuple(tag.corners[0].astype(int)),2, color=(255, 0, 255),thickness=2)
            
            # Display rotation and translation
            cv2.putText(frame, f"Rot: {tag.pose_R}", (tag.corners[0][0].astype(int), tag.corners[0][1].astype(int) - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, f"Trans: {tag.pose_t}", (tag.corners[0][0].astype(int), tag.corners[0][1].astype(int) - 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if tag.tag_id < 4:
                write_list[tag.tag_id] = str(tag.tag_id)
            
        # Write to shared.txt
        text_file = open("shared_1.txt", "w")
        write_string = ''.join(write_list)
        text_file.write(write_string)
        text_file.close()
        
        # Calculate frame rate
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time

        # Display the frame rate on the frame
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the frame
        cv2.imshow('AprilTags Detection', frame)

        # Exit program when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
