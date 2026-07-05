# Weather Web App 실행 및 Vercel 배포 방법

## 구성

- `index.html`: 웹 화면
- `static/app.css`: 화면 스타일
- `static/app.js`: 브라우저에서 `/api/weather` 호출
- `api/weather.py`: Vercel Python 서버리스 API
- `weather_service.py`: Open-Meteo 호출 및 Matplotlib 그래프 생성
- `weather_web_app.py`: 로컬 테스트용 Python 웹 서버
- `requirements.txt`: Vercel Python 함수 의존성
- `.python-version`: Vercel Python 버전 지정
- `vercel.json`: Vercel 함수 옵션 및 라우팅 설정

## 로컬 실행

프로젝트 폴더에서 아래 명령을 실행합니다.

```powershell
& 'C:\Users\hanchae0820\AppData\Local\Python\bin\python.exe' weather_web_app.py
```

브라우저에서 아래 주소를 엽니다.

```text
http://127.0.0.1:8000
```

## Vercel 배포

Vercel CLI를 사용하는 경우:

```powershell
npm i -g vercel
vercel login
vercel
```

프로덕션 배포:

```powershell
vercel --prod
```

GitHub 저장소를 Vercel에 연결하는 경우:

1. 이 프로젝트를 GitHub에 push합니다.
2. Vercel 대시보드에서 `Add New Project`를 선택합니다.
3. 저장소를 선택하고 기본 설정 그대로 배포합니다.
4. 배포 후 `https://배포주소.vercel.app`에서 웹 페이지를 확인합니다.

## Vercel 동작 방식

- 정적 파일인 `index.html`, `static/app.css`, `static/app.js`는 Vercel에서 그대로 호스팅됩니다.
- 브라우저가 `/api/weather?location=Seoul`로 요청합니다.
- Vercel이 `api/weather.py`의 `handler`를 서버리스 함수로 실행합니다.
- 서버리스 함수가 Open-Meteo API에서 오늘 시간별 날씨를 가져오고 Matplotlib 그래프를 base64 PNG로 만들어 반환합니다.

## 참고

- Vercel Python 런타임은 `requirements.txt`를 보고 `matplotlib`을 설치합니다.
- `.python-version`은 Vercel에서 Python `3.12`를 사용하도록 지정합니다.
- `vercel.json`은 API 함수 제한 시간과 번들 제외 파일을 설정합니다.
