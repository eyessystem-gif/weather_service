# Weather Web App 실행 및 Vercel 배포 방법

## 구성

- `app.py`: Flask 앱 엔트리포인트, 웹 화면과 `/api/weather` API 제공
- `index.html`: 웹 화면
- `static/app.css`: 화면 스타일
- `static/app.js`: 브라우저에서 `/api/weather` 호출
- `weather_service.py`: Open-Meteo 호출 및 Matplotlib 그래프 생성
- `weather_web_app.py`: 기존 실행명 호환용 Flask 실행 파일
- `requirements.txt`: Flask, Matplotlib 의존성
- `.python-version`: Vercel Python 버전 지정
- `vercel.json`: Vercel이 모든 요청을 Flask 앱으로 보내도록 설정

## 로컬 실행

필요한 패키지를 설치합니다.

```powershell
& 'C:\Users\hanchae0820\AppData\Local\Python\bin\python.exe' -m pip install -r requirements.txt
```

Flask 앱을 실행합니다.

```powershell
& 'C:\Users\hanchae0820\AppData\Local\Python\bin\python.exe' app.py
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

- Vercel Python 런타임은 `app.py`의 최상위 `app` Flask 객체를 WSGI 앱으로 인식합니다.
- `vercel.json`의 rewrite 설정이 모든 요청을 `/app.py`로 전달합니다.
- Flask가 `/`에서는 `index.html`을 반환하고, `/static/*`는 정적 파일을 반환합니다.
- `/api/weather?location=Seoul` 요청은 Flask API 라우트에서 처리합니다.
- API는 Open-Meteo에서 오늘 시간별 날씨를 가져오고 Matplotlib 그래프를 base64 PNG로 만들어 JSON으로 반환합니다.

## 참고

- Vercel은 `requirements.txt`를 보고 Flask와 Matplotlib을 설치합니다.
- `.python-version`은 Vercel에서 Python `3.12`를 사용하도록 지정합니다.
