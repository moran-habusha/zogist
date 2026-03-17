# Zogist — Project Context for Claude

## Overview
Zogist is a two-player Hebrew game for couples with two experiences:
1. **זוגיסט** — competitive 4-stage quiz game
2. **שפות האהבה** — love languages mini-game (separate entry point, same room)

The app runs as a **Python FastAPI backend + WebSocket** with a single-page HTML frontend.
Deployed on **Render.com free tier**, connected to GitHub for auto-deploy.

---

## Repository
- GitHub: `git@github.com:moran-habusha/zogist.git`
- Local path: `C:\Users\moran\OneDrive\שולחן העבודה\Claude\zogist\`

## SSH Authentication
- Private key: `C:\Users\moran\OneDrive\שולחן העבודה\Claude\zogist_key`
- Configured in repo git config (`core.sshCommand`) — no manual flags needed for push/pull
- User: `moran-habusha@users.noreply.github.com`

---

## Architecture

```
Frontend (static/index.html)
    ↕ WebSocket (/ws)
Backend (main.py — FastAPI + asyncio)
    — all game logic, scoring, question banks
    — in-memory state (no database)
```

### Backend (`main.py`)
- FastAPI with a single WebSocket endpoint at `/ws`
- Serves `static/index.html` at `/`
- `GameRoom` class holds all room state:
  - `ws` — `{1: ws, 2: ws}`
  - `players` — `{1: {name, gender, score}, 2: {...}}`
  - `mode`, `stage`, `q`
  - `questions` — `{s1:[10 items], s2:[...], s3:[...], s4:[...]}` (sampled from banks of 70/60/70/70)
  - `s1_ans`, `s2_state`, `s3_ans`, `s4_state`
  - `ll_results` — `{1: {receiving:[...], giving:[...]}, 2: {...}}` (love languages results)
- 16 WebSocket message handlers: `create_room`, `join_room`, `choose_experience`, `ll_done`, `start_zogist_after_ll`, `choose_mode`, `start_game`, `start_stage`, `next_question`, `answer_s1`, `buzz`, `judge_s2`, `answer_s3`, `answer_s4`, `guess_s4`, `restart`
- Buzz race resolved with `asyncio.sleep(0.15)` cooperative yield + guard

### Frontend (`static/index.html`)
- Pure HTML/CSS/JS, no frameworks, no Firebase
- WebSocket:
  ```javascript
  const ws = new WebSocket((location.protocol==='https:'?'wss://':'ws://')+location.host+'/ws');
  ```
- `MSG_HANDLERS` dispatcher for all server messages
- No scoring logic on client — only rendering
- Hebrew RTL UI with full gender-adapted text helpers
- Love languages quiz is entirely **client-side** (shuffle, scoring, rendering) — only final results sent to server

### Legacy file
- `index.html` (root level) — original Firebase version, kept in repo but not served

---

## Full App Flow

```
Room creation → P1 creates, P2 joins by code
→ Both see experience select (sc-experience)
  → P1 chooses: זוגיסט OR שפות האהבה
  → P2 sees waiting screen

  [If love_languages chosen]
  → Both see LL intro (sc-ll-intro)
  → Both answer 20 shuffled questions privately (sc-ll-q)
  → First to finish waits (sc-ll-wait)
  → When both done → results screen (sc-ll-results)
  → P1 clicks "continue to Zogist" → same room, same flow below

  [If zogist chosen / after LL]
  → P1 chooses mode (sc-mode)
  → P2 sees waiting screen (sc-wait-mode)
  → Both see mode announcement (sc-mode-announce)
  → Stages play in order based on mode
  → Final score screen
```

### Game Modes (Zogist)
- `full` — all 4 stages (S1 → S2 → S3 → S4)
- `2` — start from Stage 2
- `3` — start from Stage 3
- `4` — start from Stage 4

### Stages (Zogist)
| Stage | Type | Description |
|-------|------|-------------|
| S1 | Yes/No | 10 questions, gender-adapted text per player |
| S2 | Buzzer trivia | 10 questions (sampled from 60), first to buzz answers, host judges |
| S3 | 1-5 scale | 10 questions (sampled from 70), both answer, score for closeness |
| S4 | Guess partner | 10 questions (sampled from 70), guess what your partner said |

### Love Languages Mini-Game
- 20 questions: 10 receiving (`type:'r'`) + 10 giving (`type:'g'`), shuffled together
- Answer options also shuffled per question at runtime
- Each option maps to one of 5 love languages: `quality_time`, `words`, `service`, `touch`, `gifts`
- Scoring: `topTwo(countLangs(...))` — top 2 languages by frequency, split by receiving/giving
- Server only involved for: broadcasting `experience_chosen`, syncing `ll_done` between players, broadcasting `ll_results`
- `LL_RECEIVING`, `LL_GIVING`, `LL_DEFS` — all defined in frontend JS

---

## Gender System
Players register as `m` (זכר) or `f` (נקבה).
All question text is stored as dual variants and selected per player's gender at render time.
Key helpers in frontend: `gOf(n)`, `nOf(n)`, `heStr(n)`, `choseStr(n)`, `thoughtStr(n)`
S1 question reveal uses `myNum` (not hardcoded `1`) so each player sees their own gender variant.

---

## Deployment (Render.com)
- Config: `render.yaml` (declarative, no manual env vars needed)
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- `$PORT` injected automatically by Render
- Python 3.11
- Free tier: sleeps after 15 min inactivity, single instance
- Auto-deploys on every push to `main`

### `render.yaml`
```yaml
services:
  - type: web
    name: zogist
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.0"
    plan: free
    healthCheckPath: /
```

---

## Dependencies (`requirements.txt`)
```
fastapi==0.111.0
uvicorn[standard]==0.30.1
websockets==12.0
```

---

## Local Testing
- Local Python: `C:\Users\moran\AppData\Local\Programs\Python\Python38-32\python.exe`
- Run server: `python.exe -m uvicorn main:app --port 8765`
- Simulation script: `simulate.py` — tests full LL flow + Zogist mode select with 2 WebSocket clients

---

## Important Notes
- **Always update `preview.html`** after any UI or game changes, and tell the user "הפריוויו עודכן"
- **Terminal freezes** when user runs commands directly — always use Claude's Bash tool for git/file operations
- **Hebrew path** (`שולחן העבודה`) can cause issues in some tools — use absolute paths carefully
- All git operations use the SSH key via `core.sshCommand` stored in `.git/config`
- The frontend has **no Zogist question banks** — all questions served by backend per session
- Love languages questions live entirely in the frontend JS
- Two concurrent users max on free tier (by design — game is 2-player)
