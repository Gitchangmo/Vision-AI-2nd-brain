# Vision Wiki Chat

위키(정식 문서 + raw 원본)를 근거로 답하는 로컬 채팅 앱이다.
FastAPI 서버가 저장소의 마크다운을 직접 읽으므로, 위키를 고치면 다음 질문부터
바로 반영된다. 현장 메모와 좋은 답변을 익명화해서 위키에 넣는 기능도 있다.

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

`cli` 백엔드는 매번 `claude -p`를 도구 없이(`--tools ""`) 빈 작업 폴더에서
실행한다. 위키는 시스템 프롬프트 파일로만 전달되고, CLI는 저장소 파일에 접근하지 않는다.

## 기능

### 질문

- 질문마다 `index.md`, 정식 문서, `raw/` 원본 전체를 시스템 프롬프트로 넣는다.
  위키가 바뀌지 않는 한 같은 내용이 재사용돼 프롬프트 캐시가 적용된다.
- 답변 속 `[[concepts/...]]` 칩, `출처` 칩, `raw/...md` 경로를 누르면 오른쪽 패널에
  해당 문서가 열린다. 패널 안 링크도 따라갈 수 있고 ←로 돌아온다.
- 답변 중 `■ 중지`를 누르면 생성을 멈춘다. 중지한 답변은 대화 기록에 남지 않는다.
- 이미지는 📎 버튼, 붙여넣기(Ctrl+V), 드래그로 한 번에 5장까지 첨부하고,
  썸네일을 누르면 크게 볼 수 있다(←/→ 이동, Esc 닫기). 긴 변이 1568px을 넘으면
  브라우저에서 줄여 보낸다. 이어지는 질문에서 참조할 수 있도록 대화와 함께 매번
  다시 전송된다. 회사 제품 사진은 답변 생성을 위해 Anthropic으로 전송된다.
- 대화는 답변마다 `app/data/conversations/<id>.json`에 자동 저장되고, 왼쪽 목록에서
  다시 열거나 삭제한다. 이 폴더는 git에서 제외된다.

### 답변을 위키 문서로 (📄 위키 초안으로)

1. 답변 아래 버튼을 누르면 그 답변까지의 대화로 `queries/` 문서 초안을 만든다
   (30초~1분). 질문 속 회사·제품 정보는 일반화된다.
2. 경로, index 요약, 본문을 확인하고 고친다. `다시 검사`로 검사를 다시 돌릴 수 있다.
3. `위키에 저장`을 누르면 위키 검사(`scripts.wikilint`)와 민감어 검사를 통과할 때만
   저장되고, `index.md`와 `log.md`가 함께 갱신된다. 저장된 문서는 `status: draft`다.

### 현장 메모

1. `현장 메모` 탭에서 공정, 단계, 시기와 상황·시도·결과·문제·교훈을 편하게 적는다.
2. `AI 익명화 초안 만들기`를 누르면 회사·고객·제품·사람·장소·사업 수치를 일반화한
   초안과, 무엇을 바꿨는지 보여주는 표(저장되지 않음)가 나온다.
3. 확인·수정 후 `위키에 저장`하면 `raw/field-notes/YYYY-MM-<공정>-NN.md`로 저장되고
   `log.md`에 기록된다. 저장한 메모는 수정하지 않는다(SCHEMA.md Field Notes).

### 민감어 차단

`현장 메모` 탭의 `가릴 단어 목록`에 회사명, 고객사명, 제품명, 품번을 한 줄에
하나씩 등록한다(`app/data/sensitive-terms.txt`, git 제외). 위키에 쓰기 직전에
등록 단어, 이메일, 전화번호, ㈜·주식회사 같은 회사 표기가 하나라도 있으면
저장을 거부하고 무엇이 걸렸는지 보여준다. AI 익명화가 놓친 것을 기계적으로 막는
마지막 단계다.

## 테스트

```bash
app/.venv/Scripts/python -m pip install -r app/requirements-dev.txt
app/.venv/Scripts/python -m pytest tests                  # 서버·검사기 (AI 호출 없음)
app/.venv/Scripts/python tests/e2e/ui_check.py            # 브라우저 화면 (로컬 Chrome 필요)
app/.venv/Scripts/python tests/e2e/ui_check.py --llm      # 실제 답변·초안·중지까지 (몇 분, 사용량 발생)
```

브라우저 테스트는 위키 복사본으로 서버를 따로 띄워 실행하므로 실제 위키를 바꾸지 않는다.

## 한계

- 위키 전체를 매번 넣는 방식이라, 위키가 수십만 자 규모로 커지면 검색 단계를
  추가해야 한다.
- 서버는 이 PC(127.0.0.1)에서만 접속된다. 로그인 기능이 없으므로 외부에 열지 않는다.
