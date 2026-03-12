# 🤖 Instagram Agent — @alvaroamreis

A personal AI agent for Instagram content analysis and suggestions, built in Python with Google Gemini.

Built for a real profile with **1,900+ followers**, primarily female audience (25-34 years old) in **Portugal and Brazil**.

---

## 🎯 What it does

Every morning, run `python agent.py` and in under 1 minute you get:

- ☀️ **Live weather in Coimbra** — suggests indoor or outdoor content based on conditions
- 📅 **Day context** — adapts tone and suggestions to the day of the week
- ⏰ **Best time to post** — optimized for Portugal + Brazil audiences
- 📸 **Photo analysis** — scores all photos in the folder (1-10) and picks the best one
- 🎬 **CrossFit Reel** — 5 hook options, trending PT+BR music, specific hashtags
- 🍳 **Álvaro na Cozinha** — every Sunday, trending recipe with full script
- 💡 **Alternative suggestions** — if no good photos, suggests content based on your interests

---

## 🗂️ Project Structure

```
agente-instagram/
├── agent.py              ← main agent
├── instagram_api.py      ← Instagram API connection
├── requirements.txt      ← dependencies
├── .env                  ← secret keys (not on GitHub)
├── .gitignore            ← protects .env and personal data
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
2. Click **Get API Key**
3. Copy the key to your `.env` file

**Instagram Access Token**
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Create a **Business** type app
3. Add the **Instagram Graph API** product
4. Instagram account must be **Business or Creator** with a linked Facebook page
5. Generate the token and copy it to your `.env` file

---

## 📋 `perfil.txt` Format

The `perfil.txt` file does not go to GitHub (protected by `.gitignore`). It contains your personal data to personalize suggestions:

```
Name: your name
Location: your city
Followers: current count

AUDIENCE:
- % female / male
- Main age group
- Main countries

WEEKLY ROUTINE:
- Monday to Friday: workout type
- Saturday: fixed workout
- Sunday: workout + weekly series

CONTENT STRATEGY:
- Content types
- Weekly series
- Style and personality

GOALS:
- Growth targets
- Content focus
```

---

## 🔄 Versions

| Version | Features |
|---------|----------|
| **v1** | Basic photo analysis + weekly plan |
| **v2** ✅ | Weather + day context + photo scoring + CrossFit + Álvaro na Cozinha |
| **v3** 🔜 | Instagram token + real data + weekly history + automatic strategy |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Google Gemini 1.5 Flash** — image analysis and content generation
- **Instagram Graph API** — real profile data
- **wttr.in API** — live weather
- **python-dotenv** — environment variable management

---

## 💰 Cost

The agent uses **Gemini Flash** which is extremely affordable:

| Period | Estimated Cost |
|--------|---------------|
| Per day | ~€0.00043 |
| Per month | ~€0.013 |
| Per year | **~€0.16** |

Basically free! 🎉

---

## 📊 Real Profile Stats

This agent was built for a real profile with:

- 👥 **1,900+ followers** — growing at +9.7% per month
- 👩 **71.7% female audience** — age range 25-34
- 🇵🇹 **Portugal 77.6%** + 🇧🇷 **Brazil 11.5%**
- 📱 **Stories: 87.3%** of views — strong point
- 🎬 **Reels: 1.8%** of views — huge growth opportunity

---

## 🚀 Content Strategy

```
Monday to Friday  → CrossFit or Hyrox (always record CrossFit)
Saturday          → CrossFit ALWAYS 🔥
Sunday            → Hyrox + 🍳 Álvaro na Cozinha (weekly series)
```

**Goal:** grow through CrossFit Reels + Álvaro na Cozinha weekly series

---

## ⚠️ Security

- The `.env` file **never** goes to GitHub
- The `perfil.txt` file with personal data is protected by `.gitignore`
- Never share your API keys publicly

---

## 📄 License

Personal project — free to use for learning and inspiration.