import csv
import os
import uuid
from datetime import datetime


LOG_DIR = "logs"


class EventLogger:
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        self.log_path = os.path.join(LOG_DIR, f"driving_log_{datetime.now().strftime('%Y-%m-%d')}.csv")
        self._ensure_header()

        self.current_event = None  # 진행 중인 이벤트

    def _ensure_header(self):
        """CSV 파일이 없으면 헤더 생성"""
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "event_id",
                    "start_time",
                    "end_time",
                    "duration_sec",
                    "event_type",
                    "max_risk_level",
                    "drowsy_detected",
                    "distracted_detected",
                    "nearest_shelter",
                    "distance_km",
                ])

    def start_event(self, is_drowsy, is_distracted, risk_level):
        """위험 이벤트 시작 시 호출"""
        if self.current_event is not None:
            # 이미 이벤트 진행 중 — 상태만 업데이트
            if is_drowsy:
                self.current_event["drowsy_detected"] = True
            if is_distracted:
                self.current_event["distracted_detected"] = True
            if risk_level == "DANGER":
                self.current_event["max_risk_level"] = "DANGER"
            return

        if is_drowsy and is_distracted:
            event_type = "BOTH"
        elif is_drowsy:
            event_type = "DROWSY"
        else:
            event_type = "DISTRACTED"

        self.current_event = {
            "event_id": str(uuid.uuid4())[:8],
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "max_risk_level": risk_level,
            "drowsy_detected": is_drowsy,
            "distracted_detected": is_distracted,
            "nearest_shelter": "",
            "distance_km": "",
        }

    def update_shelter(self, shelter_name, distance_km):
        """DANGER 시 가장 가까운 쉼터 정보 업데이트"""
        if self.current_event is None:
            return
        self.current_event["nearest_shelter"] = shelter_name
        self.current_event["distance_km"] = round(distance_km, 2)

    def end_event(self):
        """정상 상태로 돌아왔을 때 호출 — CSV에 저장"""
        if self.current_event is None:
            return

        end_time = datetime.now()
        start_time = datetime.strptime(self.current_event["start_time"], "%Y-%m-%d %H:%M:%S")
        duration_sec = round((end_time - start_time).total_seconds(), 1)

        with open(self.log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                self.current_event["event_id"],
                self.current_event["start_time"],
                end_time.strftime("%Y-%m-%d %H:%M:%S"),
                duration_sec,
                self.current_event["event_type"],
                self.current_event["max_risk_level"],
                self.current_event["drowsy_detected"],
                self.current_event["distracted_detected"],
                self.current_event["nearest_shelter"],
                self.current_event["distance_km"],
            ])

        print(f"[EVENT_LOG] 이벤트 기록: {self.current_event['event_id']} "
              f"| {self.current_event['event_type']} "
              f"| {duration_sec}초")
        self.current_event = None
