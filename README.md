# 🤖 Instagram Agent — @alvaroamreis

A personal AI agent that acts as a **strategic consultant** for Instagram growth, built in Python with Google Gemini and the Instagram Graph API.

Built for a real profile targeting growth from **1,900 to 10,000 followers** through CrossFit Reels and the weekly "Álvaro na Cozinha" series.

---

## 🎯 What it does

Every morning, run `python agent.py` and in under 1 minute you get a full strategic report:

- ☀️ **Live weather in Coimbra** — suggests indoor or outdoor content
- 📅 **Day context** — adapts tone to the day of the week
- 💪 **Workout of the day** — asks CrossFit / Hyrox / Rest and decides the content strategy
- 📊 **Real Instagram data analysis** — reach, views, retention (never likes)
- ⏰ **One exact time to post** — no contradictions, based on real audience data
- 📸 **Photo scoring (1-10)** — analyses all photos and picks the best one
- ✏️ **Exact editing table** — `Exposure: +15 | Contrast: +20 | Saturation: +10` (adapts to light detected)
- 🎬 **CrossFit Reel** — 5 retention hooks for the first 3 seconds, viral PT+BR music
- 🍳 **Álvaro na Cozinha** — every Sunday, trending recipe with full script
- #️⃣ **Hashtags 30-60-10 strategy** — 30% niche + 60% context + 10% own tags

---

## 🧠 Decision Logic — One Content Per Day

```
CrossFit day   → ONLY Reel (photo saved for tomorrow)
Hyrox/Rest day → ONLY photo (if good)
Sunday         → ONLY Álvaro na Cozinha
NEVER two pieces of content on the same day
```

---

## 🗂️ Project Structure

```
agente-instagram/
├── agent.py              ← main agent
├── instagram_api.py      ← Instagram API connection
├── requirements.txt      ← dependencies
├── .env                  ← secret keys (not on GitHub)
├── .gitignore            ← protects .env, perfil.txt and personal data
└── README.md
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/AlvaroAMReis/agente-instagram.git
cd agente-instagram
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create the `.env` file**
```
GEMINI_API_KEY=your_key_here
INSTAGRAM_ACCESS_TOKEN=your_token_here
INSTAGRAM_APP_ID=your_app_id_here
INSTAGRAM_APP_SECRET=your_app_secret_here
```

**4. Create the `perfil.txt` file** with your personal data (see format below)

**5. Run the agent**
```bash
python agent.py
```

---

## 🔑 How to get the API keys

**Gemini API Key** (free)
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **Get API Key → Create API Key**
3. Copy to your `.env` file

**Instagram Access Token**
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Create a **Business** type app
3. Add **Instagram Graph API** product
4. Instagram account must be **Business or Creator** with linked Facebook page
5. Generate token via **Graph API Explorer**
6. Copy to your `.env` file

---

## 📋 `perfil.txt` Format

The `perfil.txt` file never goes to GitHub (protected by `.gitignore`).

```
Nome: Your name
Localização: Your city, Country

PERSONALIDADE:
- Authentic and relaxed
- Natural sense of humor
- Informal tone
- Films with iPhone

PÚBLICO-ALVO:
- Target audience description
- Interests
- Tone that resonates

ESTÉTICA DO FEED:
- Visual style preferences
- Color preferences

SÉRIE ÁLVARO NA COZINHA:
- Publication: every Sunday
- Style: total improvisation, no script
- Trending recipe PT + BR
- Series hashtag

CONTEÚDO DESPORTIVO:
- CrossFit → always records for Reel
- Other sports → does not record
- Style: clips of each movement, improvisation

ESTRATÉGIA:
- CrossFit → ONLY Reel
- Rest days → ONLY photo
- Sunday → ONLY weekly series
- NEVER two pieces of content on the same day
- Focus metrics: Reach and Views (NEVER Likes)

OBJECTIVOS:
- Follower growth target
- Growth engine
- Weekly series

O QUE NUNCA FAZER:
- Reels without captions
- Two pieces of content on the same day
- Hashtags with millions of posts
- Starting video standing still without action

REGRAS IMPORTANTES:
- Never focus content on minors
- Always focus on the creator
```

---

## 🔄 Versions

| Version | Features |
|---------|----------|
| **v1** | Basic photo analysis + weekly plan |
| **v2** ✅ | Weather + day context + photo scoring + editing table + CrossFit Reels + Álvaro na Cozinha + real Instagram data + one content per day rule |
| **v3** 🔜 | Long-lived token + reel retention metrics + weekly report + viral music tracking |
| **v4** 🔜 | Webhooks + contradiction hook (CrossFit + Kitchen) + auto-strategy |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Google Gemini 2.5 Flash** — image analysis and content generation
- **Instagram Graph API** — real profile data
- **wttr.in API** — live weather in Coimbra
- **python-dotenv** — environment variable management
- **CapCut** — recommended video editing app

---

## 📊 Real Profile Stats

| Metric | Value |
|--------|-------|
| Followers | 1,900+ |
| Monthly growth | +9.7% |
| Female audience | 71.7% (age 25-34) |
| Portugal | 77.6% |
| Brazil | 11.5% |
| Stories views | 87.3% |
| Reels views | 1.8% ← huge opportunity |

---

## 🚀 Growth Strategy

```
CrossFit Reels  → attract new followers (reach)
Álvaro na Cozinha → weekly series, loved by Brazil
Stories          → keep current followers engaged
```

**Goal:** 1,900 → 10,000 followers through organic Reels growth

---

## 💰 Cost

| Period | Estimated Cost |
|--------|---------------|
| Per day | ~€0.00043 |
| Per month | ~€0.013 |
| Per year | **~€0.16** |

---

## ⚠️ Security

- `.env` **never** goes to GitHub
- `perfil.txt` with personal data is protected by `.gitignore`
- `get_token.py` is protected by `.gitignore`
- Never share your API keys publicly

---

## 📄 License

Personal project — free to use for learning and inspiration.