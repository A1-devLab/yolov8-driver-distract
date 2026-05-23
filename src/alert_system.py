import cv2
import threading
import winsound

class AlertSystem:
    def __init__(self, alarm=30):
        self.danger_count = 0
        self.alarm = alarm
        self.is_alarming = False

    def play_sound(self):
        winsound.Beep(2500, 500)
        self.is_alarming = False

    def process_frame(self, frame, is_drowsy, is_distracted):
        height, width = frame.shape[:2]

        if is_drowsy or is_distracted:
            self.danger_count += 1
        else:
            self.danger_count = max(0, self.danger_count - 1)

        if 5 < self.danger_count <= self.alarm:
            cv2.rectangle(frame, (0, 0), (width, height), (0, 255, 255), 10)
            
            status_text = "CAUTION: "
            if is_drowsy: status_text += "DROWSY "
            if is_distracted: status_text += "DISTRACTED"
            
            cv2.putText(frame, status_text, (30, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 3)

        elif self.danger_count > self.alarm:
            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 20)
            cv2.putText(frame, "DANGER", (30, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)
            
            if not self.is_alarming:
                self.is_alarming = True
                threading.Thread(target=self.play_sound, daemon=True).start()

        return frame