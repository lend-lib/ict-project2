import cv2
import pandas as pd
from datetime import datetime


cap = cv2.VideoCapture(0)
attendance_list = []
entering_name = False
current_name = ""
captured_image = None

while True:
    if entering_name:
        frame = captured_image.copy()
    else:
        ret, frame = cap.read()
        if not ret:
            break

    if not entering_name:
        cv2.putText(frame, "Press SPACE to take attendance", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Enter your name:", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(frame, current_name, (50, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow('Attendance System', frame)

    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break
    elif key == 32 and not entering_name: 
        captured_image = frame.copy()
        entering_name = True
    elif entering_name:
        if key == 13:  
            if current_name:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                image_name = f"{current_name}_{current_time.replace(':', '-')}.jpg"
                cv2.imwrite(image_name, captured_image)
                attendance_list.append({
                    "name": current_name,
                    "time": current_time,
                    "image_name": image_name
                })
                current_name = ""
                entering_name = False
        elif key == 8:
            current_name = current_name[:-1]
        elif 32 <= key <= 126:  # Printable characters
            current_name += chr(key)

if attendance_list:
    df = pd.DataFrame(attendance_list)
    df.to_excel(r"C:\Users\lenovo\Desktop\attendance.xlsx", index=False, engine='openpyxl')

cap.release()
cv2.destroyAllWindows()