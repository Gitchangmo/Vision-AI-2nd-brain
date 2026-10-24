# Vision Wiki Chat

위키(정식 문서 + raw 원본)를 근거로 답하는 로컬 채팅 앱이다.
FastAPI 서버가 저장소의 마크다운을 직접 읽으므로, 위키를 고치면 다음 질문부터
바로 반영된다.

## 처음 한 번

```bash
# 저장소 루트에서
python -m venv app/.venv
app/.venv/Scripts/python -m pip install -r app/requirements.txt   # macOS/Linux: app/.venv/bin/python
```

## 실행

```bash
app/.venv/Scripts/python -m uvicorn app.server:app --reload
```

브라우저에서 http://127.0.0.1:8000 을 연다.

## 답변 방식 (백엔드)

| 백엔드 | 조건 | 비용 |
| --- | --- | --- |
| `cli` (기본) | 이 PC에 Claude Code가 설치·로그인돼 있음 | Claude 구독 사용량에 포함 |
| `api` | `app/.env`에 `ANTHROPIC_API_KEY`가 있음 | 토큰 사용량만큼 별도 과금 |

API 키가 있으면 `api`, 없으면 `cli`를 쓴다. 강제로 고르려면 `app/.env`에
`WIKI_CHAT_BACKEND=cli` 또는 `api`를 넣는다. 양식은 `app/.env.example`에 있고,
`app/.env`는 .gitignore에 있어 커밋되지 않는다.

`cli` 백엔드는 질문마다 `claude -p`를 도구 없이(`--tools ""`) 빈 작업 폴더에서
실행한다. 위키는 시스템 프롬프트 파일로만 전달되고, CLI는 저장소 파일에 접근하지 않는다.

## 동작 방식

- 질문마다 `index.md`, 정식 문서, `raw/` 원본 전체를 시스템 프롬프트로 넣는다.
  위키가 바뀌지 않는 한 같은 내용이 재사용돼 프롬프트 캐시가 적용된다.
- 답변은 근거 문서를 `[[concepts/...]]` 형태로, raw 근거를 경로로 표시한다.
  위키에 없는 내용은 "위키 밖 일반 지식"으로 구분한다.
- 대화는 답변이 끝날 때마다 `app/data/conversations/<id>.json`에 자동 저장된다.
  왼쪽 목록에서 다시 열거나 삭제한다. 이 폴더는 .gitignore에 있어 커밋되지 않는다.
  대화에는 회사 정보와 첨부 이미지가 그대로 들어가므로, 위키(공개 저장소)로
  옮길 때는 익명화를 거친다.
- 이미지는 📎 버튼, 붙여넣기(Ctrl+V), 드래그로 한 번에 5장까지 첨부하고,
  썸네일을 누르면 크게 볼 수 있다(←/→ 이동, Esc 닫기).
  JPEG·PNG·GIF·WebP를 지원하고, 긴 변이 1568px을 넘으면 브라우저에서 줄여 보낸다.
  이어지는 질문에서 다시 참조할 수 있도록 대화 기록과 함께 매번 다시 전송된다
  (이미지가 많을수록 사용량이 늘어남). 회사 제품 사진은 답변 생성을 위해
  Anthropic으로 전송된다는 점에 유의한다.
- 모델과 effort는 `app/.env`의 `WIKI_CHAT_MODEL`, `WIKI_CHAT_EFFORT`로 바꿀 수 있다.
  `cli`에서 `WIKI_CHAT_MODEL`을 비우면 Claude Code에 설정된 기본 모델을 쓴다.

## 한계

- 위키 전체를 매번 넣는 방식이라, 위키가 수십만 자 규모로 커지면 검색 단계를
  추가해야 한다.
- 서버는 기본적으로 이 PC(127.0.0.1)에서만 접속된다.
