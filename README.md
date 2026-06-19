# YOLOv8 기반 Driver Monitoring System

실시간 웹캠 영상을 이용해 운전자의 졸음 상태와 전방 주시 태만 상태를 감지하는 시스템입니다.
위험 상황이 감지되면 화면 경고와 경고음을 제공하고, 공공데이터 API를 활용해 현재 위치 기준 가까운 졸음쉼터를 안내합니다.

## 주요 기능

### 1. 운전자 상태 감지

YOLOv8 모델을 사용해 운전자의 상태를 실시간으로 감지합니다.

* `eyesyawn.pt`: 눈 감김, 하품 등 졸음 상태 감지
* `distract.pt`: 전방 미주시, 휴대폰 사용 등 주시 태만 상태 감지

### 2. 영상 전처리

차량 내부 밝기 변화에 대응하기 위해 OpenCV 기반 전처리를 적용했습니다.

* 프레임 평균 밝기 계산
* 밝기에 따른 동적 Gamma 조정
* 주간, 야간, 터널 등 환경 변화 대응

### 3. 단계별 경고 시스템

위험 카운트를 기준으로 운전자 상태를 단계별로 관리합니다.

* Normal: 정상 상태
* Caution: 화면에 노란색 테두리와 경고 메시지 표시
* Danger: 화면에 빨간색 테두리 표시 및 경고음 출력

경고음은 별도 스레드에서 실행하여 영상 처리 흐름이 멈추지 않도록 구성했습니다.

### 4. 졸음쉼터 안내

공공데이터포털의 전국 졸음쉼터 표준 데이터 API를 사용해 가까운 졸음쉼터를 안내합니다.

* 현재 좌표 기준 졸음쉼터 Top 3 탐색
* Haversine 공식 기반 거리 계산
* 졸음쉼터 이름, 노선명, 방향, 거리 표시
* Pillow를 이용한 한글 UI 오버레이

API 호출 실패나 네트워크 오류에 대비해 로컬 JSON 캐시를 사용하도록 구성했습니다.

## 기술 스택

* Python
* OpenCV
* Ultralytics YOLOv8
* Pillow
* Requests
* JSON
* python-dotenv

## 프로젝트 구조

```text
├── model/
│   ├── eyesyawn.pt
│   └── distract.pt
├── src/
│   ├── alert_system.py
│   ├── rest_area_service.py
│   └── event_logger.py
├── assets/
│   └── fonts/
│       └── NotoSansKR-VariableFont_wght.ttf
├── .env
└── main.py
```

## 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 값을 입력합니다.

```env
DROWSY_SHELTER_API_KEY=your_public_api_key_here
DEFAULT_LAT=
DEFAULT_LNG=
```

좌표를 따로 설정하지 않으면 기본 좌표로 강남역 좌표가 사용됩니다.

## 실행 방법

```bash
python main.py
```

웹캠 화면이 실행되며, 종료하려면 창을 선택한 상태에서 `q` 키를 누르면 됩니다.
