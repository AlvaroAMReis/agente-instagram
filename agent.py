from google import genai
from google.genai import types
import os
import base64
import requests
from datetime import datetime
from dotenv import load_dotenv
from instagram_api import get_profile, get_posts

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"
PHOTOS_FOLDER = r"C:\Users\alvar\Desktop\Fotos para o insta"
PROFILE_FILE = r"C:\Users\alvar\Desktop\agente-instagram\perfil.txt"

# ============================================================
# CARREGAR PERFIL
# ============================================================

def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# ============================================================
# LONG-LIVED TOKEN — renova automaticamente
# ============================================================

def refresh_token():
    """Tenta renovar o token IGAA automaticamente"""
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    app_id = os.getenv("INSTAGRAM_APP_ID")
    app_secret = os.getenv("INSTAGRAM_APP_SECRET")

    if not app_id or not app_secret:
        return token

    try:
        url = "https://graph.instagram.com/refresh_access_token"
        params = {
            "grant_type": "ig_refresh_token",
            "access_token": token
        }
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        if "access_token" in data:
            print("🔄 Token renovado automaticamente!")
            return data["access_token"]
    except:
        pass
    return token

# ============================================================
# DADOS DO INSTAGRAM
# ============================================================

def get_instagram_data():
    try:
        profile = get_profile()
        posts = get_posts()
        post_metrics = []
        if "data" in posts:
            for post in posts["data"][:10]:
                metrics = {
                    "id": post.get("id", ""),
                    "tipo": post.get("media_type", ""),
                    "data": post.get("timestamp", ""),
                    "likes": post.get("like_count", 0),
                    "comentarios": post.get("comments_count", 0),
                    "legenda": post.get("caption", "")[:50] if post.get("caption") else ""
                }
                post_metrics.append(metrics)
        return f"Perfil: {profile}\nPosts recentes com métricas: {post_metrics}", True, post_metrics
    except Exception as e:
        return "Token do Instagram ainda não configurado.", False, []

# ============================================================
# CLIMA EM COIMBRA
# ============================================================

def get_weather():
    try:
        url = "https://wttr.in/Coimbra?format=j1"
        response = requests.get(url, timeout=5)
        data = response.json()
        temp = data["current_condition"][0]["temp_C"]
        desc = data["current_condition"][0]["weatherDesc"][0]["value"]
        is_sunny = any(word in desc.lower() for word in ["sun", "clear", "fair"])
        is_rainy = any(word in desc.lower() for word in ["rain", "drizzle", "shower"])
        if is_sunny:
            emoji = "☀️"
            tip = "Óptimo para conteúdo ao ar livre antes ou depois do treino!"
        elif is_rainy:
            emoji = "🌧️"
            tip = "Dia perfeito para ficar em casa e gravar o Álvaro na Cozinha! 🍳"
        else:
            emoji = "⛅"
            tip = "Sem chuva — podes gravar à saída do treino!"
        return f"{emoji} {desc} e {temp}°C\n💡 {tip}", is_sunny, is_rainy
    except:
        return "⛅ Clima não disponível de momento.", False, False

# ============================================================
# CONTEXTO DO DIA DA SEMANA
# ============================================================

def get_day_context():
    day = datetime.now().weekday()
    days = {
        0: ("Segunda-feira", "💪 Início de semana — o teu público está motivado!\n   Melhor dia para energia e motivação."),
        1: ("Terça-feira", "🔥 Terça-feira — mantém o ritmo da semana!"),
        2: ("Quarta-feira", "💪 A meio da semana — o teu público precisa de motivação!\n   Conteúdo 'ainda estou aqui' ressoa muito bem às quartas!"),
        3: ("Quinta-feira", "🏋️ Quinta-feira — quase lá! Bom dia para conteúdo de progresso."),
        4: ("Sexta-feira", "😄 Sexta-feira — conteúdo mais descontraído!\n   Tom: 'sobrevivi à semana 😂🔥'"),
        5: ("Sábado", "🔥 SÁBADO — DIA DE CROSSFIT SEMPRE!\n   Público mais ativo ao fim da manhã."),
        6: ("Domingo", "🍳 DOMINGO — DIA DO ÁLVARO NA COZINHA!\n   Sem pressão de treino para gravar — foca-te na receita da semana!")
    }
    return days[day]

# ============================================================
# TREINO DO DIA
# ============================================================

def ask_workout(day_name):
    day = datetime.now().weekday()
    if day == 5:
        print("\n💪 TREINO DE HOJE:")
        print("   CrossFit SEMPRE ao sábado! 🔥")
        return "crossfit"
    elif day == 6:
        print("\n💪 TREINO DE HOJE:")
        print("   Hyrox ao domingo! 🏃 (sem gravação)")
        return "hyrox"
    else:
        print("\n💪 TREINO DE HOJE:")
        print("   1. CrossFit 🔥")
        print("   2. Hyrox 🏃")
        print("   3. Descanso 😴")
        choice = input("\n   Escolhe (1/2/3): ").strip()
        if choice == "1":
            return "crossfit"
        elif choice == "2":
            return "hyrox"
        else:
            return "descanso"

# ============================================================
# ANÁLISE DE DADOS REAIS
# ============================================================

def get_daily_focus(instagram_data, personal_profile, has_token, post_metrics):
    today = datetime.now().strftime("%A")
    if has_token and post_metrics:
        prompt = f"""
        És um consultor estratégico de Instagram agressivo e focado em dados.
        Hoje é {today}.
        Perfil: {personal_profile}
        Dados reais do Instagram: {instagram_data}
        Métricas dos posts: {post_metrics}

        REGRAS:
        - NUNCA mencionar Likes como métrica de sucesso
        - SEMPRE focar em Alcance (Reach) e Views
        - Uma hora EXACTA para publicar — sem contradições
        - Reels são SEMPRE prioridade sobre fotos
        - Se não publicou Reel há 3+ dias: ALERTA URGENTE

        Responde em português:

        📊 PERFORMANCE DOS ÚLTIMOS POSTS:
        Para cada post: Tipo | Views estimadas | Alcance | Impacto crescimento
        "Este Reel trouxe-te X novos seguidores" — NUNCA falar em likes

        🔥 ANÁLISE DE RETENÇÃO:
        Onde perdes a audiência nos Reels?
        Recomendação concreta para hoje

        💡 TENDÊNCIA:
        O que está a crescer | O que evitar

        🎯 ORDEM DO DIA:
        1 ação concreta e agressiva
        Meta: X novos seguidores hoje

        ⏰ HORA EXACTA:
        Uma hora só — baseada nos dados reais
        """
    else:
        prompt = f"""
        És um consultor estratégico de Instagram.
        Hoje é {today}.
        Perfil: {personal_profile}

        Responde em português:

        ⏰ HORA EXACTA PARA PUBLICAR:
        Uma hora só — para Portugal + Brasil

        🎯 ORDEM DO DIA:
        1 ação concreta para crescer hoje
        """
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

# ============================================================
# ANÁLISE DE FOTOS
# ============================================================

def score_all_photos(photos, instagram_data, personal_profile):
    scored = []
    print(f"\n📁 A ANALISAR AS FOTOS DA PASTA...")
    print(f"   Encontrei {len(photos)} foto(s)!\n")
    for photo in photos:
        full_path = os.path.join(PHOTOS_FOLDER, photo)
        try:
            with open(full_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")
            ext = photo.split(".")[-1].lower()
            mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
            prompt = f"""
            Perfil: {personal_profile}
            Público: 71.7% mulheres, 25-34 anos, Portugal e Brasil.
            Analisa esta foto para Instagram e responde APENAS neste formato:
            PONTUACAO: [número de 1 a 10]
            MOTIVO: [razão curta em português]
            """
            response = client.models.generate_content(
                model=MODEL,
                contents=[
                    types.Part.from_bytes(data=base64.b64decode(image_data), mime_type=mime),
                    prompt
                ]
            )
            text = response.text
            score = 5
            motivo = ""
            for line in text.split("\n"):
                if "PONTUACAO:" in line or "PONTUAÇÃO:" in line:
                    try:
                        score = int(''.join(filter(str.isdigit, line.split(":")[-1][:3])))
                    except:
                        score = 5
                if "MOTIVO:" in line:
                    motivo = line.split(":", 1)[-1].strip()
            scored.append((photo, score, motivo))
            emoji = "✅" if score >= 8 else ("⚠️ " if score >= 6 else "❌")
            print(f"   📸 {photo} .............. {score}/10 {emoji}")
            if motivo:
                print(f"      → {motivo}")
            print()
        except Exception as e:
            scored.append((photo, 5, "Erro ao analisar"))
    return scored

# ============================================================
# ANÁLISE COMPLETA DA MELHOR FOTO
# ============================================================

def analyze_best_photo(image_path, instagram_data, personal_profile, score):
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    ext = image_path.split(".")[-1].lower()
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
    today = datetime.now().strftime("%A")
    prompt = f"""
    És um especialista em Instagram e edição de fotografia.
    Hoje é {today}.
    Perfil: {personal_profile}
    Dados: {instagram_data}
    Público: 71.7% mulheres, 25-34 anos, Portugal (77.6%) e Brasil (11.5%)

    IMPORTANTE: Detecta se a foto é ESCURA, CLARA ou EQUILIBRADA
    e ajusta os valores de edição automaticamente:
    - Foto escura (ex: indoor, CrossFit) → Exposição +25 a +35, Sombras +35 a +45
    - Foto clara (ex: exterior, sol forte) → Exposição +5 a +10, Highlights -25 a -35
    - Foto equilibrada → valores standard

    Responde em português:

    📸 AVALIAÇÃO ({score}/10):
    - Pontos fortes (máximo 3)
    - O que melhorar (máximo 2)
    - TIPO DE LUZ DETECTADA: [Escura/Clara/Equilibrada]

    ✏️ TABELA DE EDIÇÃO — valores exactos ajustados à luz detectada:
    ╔══════════════════╦═══════════╦══════════════════════════════════╗
    ║ Ajuste           ║ Valor     ║ Porquê                           ║
    ╠══════════════════╬═══════════╬══════════════════════════════════╣
    ║ Exposição        ║ +/- XX    ║ [razão específica]               ║
    ║ Contraste        ║ +/- XX    ║ [razão específica]               ║
    ║ Brilho           ║ +/- XX    ║ [razão específica]               ║
    ║ Sombras          ║ +/- XX    ║ [razão específica]               ║
    ║ Highlights       ║ +/- XX    ║ [razão específica]               ║
    ║ Saturação        ║ +/- XX    ║ [razão específica]               ║
    ║ Nitidez          ║ +/- XX    ║ [razão específica]               ║
    ║ Claridade        ║ +/- XX    ║ [razão específica]               ║
    ╚══════════════════╩═══════════╩══════════════════════════════════╝
    App: Lightroom Mobile
    Preset base: [nome adequado]
    ⚠️ NOTA: Estes são valores de BASE — ajusta ±5 conforme o teu gosto!

    ✍️ 3 LEGENDAS NO ESTILO DO ÁLVARO:
    (curtas, PT+BR, sem forçar)

    Opção 1 — Humor:
    [legenda]

    Opção 2 — Autêntica:
    [legenda]

    Opção 3 — Com pergunta:
    [legenda]

    🎵 2 MÚSICAS SUGERIDAS:
    (virais agora PT+BR, adequadas ao conteúdo)
    1. [Nome - Artista] → [porquê]
    2. [Nome - Artista] → [porquê]

    #️⃣ HASHTAGS — ESTRATÉGIA 30-60-10:
    🎯 30% NICHO (6 tags): [específicas ao conteúdo da foto]
    📍 60% CONTEXTO (12 tags): [localização/tema PT+BR]
    🏷️ 10% PRÓPRIAS (2 tags): #AlvaroNaCozinha #alvaroreis17

    🎬 COMO TRANSFORMAR EM REEL:
    → Conceito em 1 frase
    → Gancho dos primeiros 3 segundos
    → Duração ideal

    ⏰ HORA EXACTA: [hora] — [justificação em 1 linha]
    """
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=base64.b64decode(image_data), mime_type=mime),
            prompt
        ]
    )
    return response.text

# ============================================================
# REEL DE CROSSFIT
# ============================================================

def suggest_crossfit_reel(instagram_data, personal_profile, post_metrics):
    today = datetime.now().strftime("%A")
    day = datetime.now().weekday()
    day_tone = {
        0: "motivação de início de semana",
        1: "energia de terça-feira",
        2: "força a meio da semana",
        3: "quase lá, quinta-feira",
        4: "sexta-feira descontraída",
        5: "sábado de CrossFit always 🔥",
        6: "domingo"
    }
    tone = day_tone.get(day, "")
    prompt = f"""
    És um especialista em Reels virais de fitness.
    Hoje é {today} — tom: {tone}.
    Perfil: {personal_profile}
    Dados: {instagram_data}
    Performance últimos Reels: {post_metrics}

    REGRA DE OURO: Os primeiros 3 segundos determinam tudo.
    ESTILO: clips de cada movimento do WOD, improviso, transições dinâmicas.
    NUNCA focar em menores de idade.

    Responde em português:

    🔥 ANÁLISE DE RETENÇÃO:
    Onde perdes a audiência com base nos dados?
    Recomendação concreta: "Evita X porque..."

    ⚡ 5 GANCHOS — primeiros 3 segundos (do mais ao menos agressivo):
    1. [gancho] → [porquê funciona]
    2. [gancho] → [porquê funciona]
    3. [gancho] → [porquê funciona]
    4. [gancho] → [porquê funciona]
    5. [gancho] → [porquê funciona]

    💪 COMO GRAVAR:
    → Improviso total, clips naturais
    → X clips de Y segundos cada
    → Foca nas transições entre movimentos

    ✂️ EDIÇÃO NO CAPCUT:
    → Auto Beat activado
    → Dica específica para transições

    🎵 3 MÚSICAS — por potencial viral AGORA em PT+BR:
    1. [Nome - Artista] → BPM, porquê
    2. [Nome - Artista] → BPM, porquê
    3. [Nome - Artista] → BPM, porquê

    ✍️ 3 LEGENDAS — curtas, PT+BR:
    1. [humor]
    2. [autêntica]
    3. [com pergunta]

    #️⃣ HASHTAGS — 30-60-10:
    🎯 30% NICHO (6): [CrossFit específico]
    📍 60% CONTEXTO (12): [PT+BR fitness]
    🏷️ 10% PRÓPRIAS (2): #alvaroreis17 #AlvaroCrossfit

    ⏰ HORA EXACTA: [hora] — [justificação 1 linha]
    """
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

# ============================================================
# ÁLVARO NA COZINHA
# ============================================================

def suggest_alvaro_na_cozinha(instagram_data, personal_profile):
    prompt = f"""
    És um especialista em conteúdo de culinária viral.
    Hoje é domingo — Álvaro na Cozinha!
    Perfil: {personal_profile}
    Dados: {instagram_data}

    ESTILO: improviso total, autêntico, sem guião.
    PÚBLICO: 71.7% mulheres, PT (77.6%) e BR (11.5%).
    Brasileiros ADORAM receitas portuguesas!

    Responde em português:

    📈 RECEITA EM TENDÊNCIA AGORA PT+BR:
    → Nome + porquê está viral esta semana

    📝 RECEITA COMPLETA:
    Ingredientes (máximo 6):
    Passo a passo (máximo 5 passos):

    📱 COMO GRAVAR — IMPROVISO TOTAL:
    → iPhone apoiado, grava tudo
    → Fala como se contasses a um amigo
    → Momentos de ouro a NÃO cortar

    ✂️ EDIÇÃO NO CAPCUT:
    → Dica específica para este tipo de receita

    🎵 3 MÚSICAS:
    (descontraídas, domingo em casa, virais PT+BR)

    ⚡ 5 GANCHOS:
    1. [humor] 2. [série] 3. [Brasil] 4. [curiosidade] 5. [relatable]

    ✍️ 3 LEGENDAS:
    Opção 1 — Humor: [legenda]
    Opção 2 — Série: "ep. X do Álvaro na Cozinha 👨‍🍳..."
    Opção 3 — Brasil: [legenda]

    #️⃣ HASHTAGS — 30-60-10:
    🎯 30% NICHO (6): [receita específica]
    📍 60% CONTEXTO (12): [culinária PT+BR]
    🏷️ 10% PRÓPRIAS (2): #AlvaroNaCozinha #alvaroreis17

    ⏰ HORA EXACTA: 20h15 Portugal / 16h15 Brasil
    """
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

# ============================================================
# SUGESTÃO SEM FOTO BOA
# ============================================================

def suggest_no_photo_content(workout, instagram_data, personal_profile, is_rainy):
    today = datetime.now().strftime("%A")
    prompt = f"""
    Consultor estratégico de Instagram.
    Hoje é {today}. Treino: {workout}. Chuva: {is_rainy}.
    Perfil: {personal_profile}
    Dados: {instagram_data}

    Sem fotos boas hoje. Sugere 3 alternativas baseadas nos gostos do Álvaro.
    SEMPRE prioriza Reels. Para cada opção:
    → Conceito concreto
    → Como executar em 30 min com iPhone
    → Gancho sugerido

    {'CrossFit hoje — transforma em Reel!' if workout == 'crossfit' else ''}
    {'Hyrox hoje — sem gravação, outras opções:' if workout == 'hyrox' else ''}
    {'Descanso — lifestyle ou Álvaro na Cozinha:' if workout == 'descanso' else ''}
    """
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

# ============================================================
# AGENTE PRINCIPAL
# ============================================================

def run_agent():
    print("\n🤖 AGENTE INSTAGRAM — BOM DIA ÁLVARO! 👋")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%A, %d de %B de %Y — %H:%M')}")
    print("=" * 50)

    # 1. Carregar perfil
    personal_profile = load_profile()
    if not personal_profile:
        print("⚠️  Ficheiro perfil.txt não encontrado!")
        return

    # 2. Dados do Instagram
    print("\n🔍 A LIGAR AO INSTAGRAM...")
    instagram_data, has_token, post_metrics = get_instagram_data()
    if has_token:
        print("✅ Dados reais carregados!")
    else:
        print("⚠️  Sem token — usando perfil.txt")

    # 3. Clima
    print("\n🌤️ CLIMA EM COIMBRA AGORA:")
    weather_text, is_sunny, is_rainy = get_weather()
    print(f"   {weather_text}")

    # 4. Contexto do dia
    day_name, day_context = get_day_context()
    print(f"\n📅 CONTEXTO — {day_name.upper()}:")
    print(f"   {day_context}")

    # 5. Treino do dia
    workout = ask_workout(day_name)

    # 6. Análise de dados + hora exacta
    print("\n" + "=" * 50)
    print("📊 ANÁLISE DE DADOS + HORA EXACTA:")
    print("=" * 50)
    focus = get_daily_focus(instagram_data, personal_profile, has_token, post_metrics)
    print(focus)

    # 7. Análise de fotos
    day = datetime.now().weekday()

    if not os.path.exists(PHOTOS_FOLDER):
        print("\n❌ Pasta 'Fotos para o insta' não encontrada!")
        photos = []
    else:
        extensions = [".jpg", ".jpeg", ".png", ".webp"]
        photos = [f for f in os.listdir(PHOTOS_FOLDER)
                  if os.path.splitext(f)[1].lower() in extensions]

    print("\n" + "=" * 50)

    best_photo = None
    best_score = 0
    best_name = None

    if photos:
        scored_photos = score_all_photos(photos, instagram_data, personal_profile)
        scored_photos.sort(key=lambda x: x[1], reverse=True)
        best_name, best_score, best_motivo = scored_photos[0]

        if best_score >= 7:
            print(f"🏆 MELHOR FOTO: {best_name} ({best_score}/10)")
            if len(scored_photos) > 1:
                second = scored_photos[1]
                print(f"⚠️  Segunda melhor: {second[0]} ({second[1]}/10) — guarda para outro dia!")
            best_photo = os.path.join(PHOTOS_FOLDER, best_name)
        else:
            print(f"⚠️  NENHUMA FOTO EXCELENTE HOJE!")
            print(f"   A melhor foi {best_name} com {best_score}/10 — abaixo do ideal (7+)")
            best_photo = None
    else:
        if day == 6:
            print("📁 Pasta vazia — hoje é domingo, foco no Álvaro na Cozinha! 🍳")
        else:
            print("📁 Pasta vazia hoje.")

    # 8. DECISÃO DO DIA — UMA acção só, sem conflitos
    print("\n" + "=" * 50)

    if day == 6:  # Domingo — SEMPRE Álvaro na Cozinha
        print("🍳 ÁLVARO NA COZINHA — EPISÓDIO DA SEMANA:")
        print("=" * 50)
        cozinha = suggest_alvaro_na_cozinha(instagram_data, personal_profile)
        print(cozinha)

    elif workout == "crossfit":
        # CrossFit = SEMPRE Reel — foto fica para outro dia
        print("🎬 REEL DE CROSSFIT — HOJE:")
        print("=" * 50)
        if best_photo:
            print(f"📸 Tens a foto {best_name} ({best_score}/10) disponível.")
            print(f"   → GUARDA para amanhã — hoje o foco é 100% no Reel!")
            print(f"   → Dois conteúdos no mesmo dia canibalizam-se!\n")
        reel = suggest_crossfit_reel(instagram_data, personal_profile, post_metrics)
        print(reel)

    elif workout == "hyrox":
        # Hyrox = sem gravação — usa foto se boa
        print("🏃 DIA DE HYROX — SEM GRAVAÇÃO")
        print("=" * 50)
        if best_photo:
            print(f"✅ DECISÃO: Publicas a foto {best_name} ({best_score}/10) hoje!")
            print(f"   → Sem Reel de Hyrox — foco total na foto!\n")
            print("\n" + "=" * 50)
            print(f"📋 ANÁLISE COMPLETA — {best_name}:")
            print("=" * 50)
            analysis = analyze_best_photo(best_photo, instagram_data, personal_profile, best_score)
            print(analysis)
        else:
            alternatives = suggest_no_photo_content(workout, instagram_data, personal_profile, is_rainy)
            print(alternatives)

    else:  # Descanso
        print("😴 DIA DE DESCANSO")
        print("=" * 50)
        if best_photo:
            print(f"✅ DECISÃO: Publicas a foto {best_name} ({best_score}/10) hoje!")
            print(f"   → Dia perfeito — sem competição com Reels!\n")
            print("\n" + "=" * 50)
            print(f"📋 ANÁLISE COMPLETA — {best_name}:")
            print("=" * 50)
            analysis = analyze_best_photo(best_photo, instagram_data, personal_profile, best_score)
            print(analysis)
        else:
            alternatives = suggest_no_photo_content(workout, instagram_data, personal_profile, is_rainy)
            print(alternatives)

    print("\n" + "=" * 50)
    print("✅ Tudo pronto! Boas publicações Álvaro! 🚀")
    print("=" * 50)

if __name__ == "__main__":
    run_agent()