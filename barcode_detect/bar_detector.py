import cv2
# there's a possibility that this code only works for upc bar codes
def bar_detector():
    bar_detector = cv2.barcode.BarcodeDetector()
    cap = cv2.VideoCapture(0)
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Could not open camera")
        exit()

    while True:
        # Read a new frame from the camera
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Failed to grab frame")
            break

        # data1=bar_detector.detectAndDecodeWithType(frame)
        # print("data1",data1)

        # Detect and decode the QR code in the frame
        _ , data, bar_type, bbox = bar_detector.detectAndDecodeWithType(frame)

        # Check if a QR code was detected
        if (bbox is not None) and (data):

            # print("data",data)

            # Draw a bounding box around the QR code
            for i in range(3):
                #cv2.line(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
                cv2.line(frame, tuple(map(int,bbox[0][i])), tuple(map(int,bbox[0][i+1])), (0, 255, 0),2 )    
            cv2.line(frame, tuple(map(int,bbox[0][-1])), tuple(map(int,bbox[0][0])), (0, 255, 0),2 )

            if data[0]:
                print(f"Decoded Data: {data[0]}")
                cv2.waitKey(500)
                cap.release()
                cv2.destroyAllWindows()
                return data[0]
                break
        # Display the frame with the detected QR code (if any)
        cv2.imshow("Bar Code Scanner", frame)

        # Check if the 'q' key was pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Release the VideoCapture object and close all windows
            cap.release()
            cv2.destroyAllWindows()
            break

bar_detector()
