# open camera to detect qr code.
# Prerequisite: opencv-python

import cv2

def qr_scanner():
    # Create a new VideoCapture object
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Could not open camera")
        exit()

    # Initialize the QR code detector
    qr_detector = cv2.QRCodeDetector()

    while True:
        # Read a new frame from the camera
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Failed to grab frame")
            break

        # Detect and decode the QR code in the frame
        data, bbox, _ = qr_detector.detectAndDecode(frame)

        # Check if a QR code was detected
        if (bbox is not None) and (data != ""):

            # Draw a bounding box around the QR code
            for i in range(3):
                #cv2.line(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
                cv2.line(frame, tuple(map(int,bbox[0][i])), tuple(map(int,bbox[0][i+1])), (0, 255, 0),2 )    
            cv2.line(frame, tuple(map(int,bbox[0][-1])), tuple(map(int,bbox[0][0])), (0, 255, 0),2 )


        # Display the frame with the detected QR code (if any)
        cv2.imshow("QR Code Scanner", frame)
        if data:
                #print(f"Decoded Data: {data}")
                cv2.waitKey(200)
                cap.release()
                cv2.destroyAllWindows()
                # send_data()
                return data
        # Check if the 'q' key was pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Release the VideoCapture object and close all windows
            cap.release()
            cv2.destroyAllWindows()
            break


# data=qr_scanner()
