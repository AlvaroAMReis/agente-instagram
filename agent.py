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
MODEL = "gemini-2.0-flash"
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
# DADOS DO INSTAGRAM
# ============================================================

def get_instagram_data():
    try:
        profile = get_profile()
        posts = get_posts()
        return f"Perfil: {profile}\nPosts recentes: {posts}", True
    except:
        return "Token do Instagram ainda não configurado.", False

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
    day = datetime.now().weekday()  # 0=segunda, 6=domingo
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
    
    if day == 5:  # Sábado
        print("\n💪 TREINO DE HOJE:")
        print("   CrossFit SEMPRE ao sábado! 🔥")
        return "crossfit"
    elif day == 6:  # Domingo
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
# ANÁLISE DE FOTOS COM PONTUAÇÃO
# ============================================================

def score_all_photos(photos, instagram_data, personal_profile):
    """Pontua todas as fotos da pasta de 1 a 10"""
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
            score = 5  # default
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
            
            # Mostrar resultado
            if score >= 8:
                emoji = "✅"
            elif score >= 6:
                emoji = "⚠️ "
            else:
                emoji = "❌"
            
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
    És um especialista em Instagram e marketing digital.
    Hoje é {today}.
    
    Perfil do criador:
    {personal_profile}
    
    Dados do Instagram:
    {instagram_data}
    
    Analisa esta foto tendo em conta:
    - Público: 71.7% mulheres, 25-34 anos, Portugal (77.6%) e Brasil (11.5%)
    - Estilo: descontraído, autêntico, bem-disposto
    - Nunca sugerir conteúdo focado em menores de idade
    
    Responde em português com:
    
    📸 AVALIAÇÃO DA FOTO ({score}/10):
    - Pontos fortes
    - O que melhorar
    
    ✏️ EDIÇÃO RECOMENDADA:
    - Ajustes específicos (brilho, contraste, saturação, crop)
    - Preset recomendado
    - App sugerida (Lightroom Mobile, VSCO, etc.)
    
    ✍️ 3 LEGENDAS NO ESTILO DO ÁLVARO:
    - Opção 1: informal e engraçada
    - Opção 2: autêntica e próxima do público
    - Opção 3: com pergunta para gerar comentários
    
    🎵 MÚSICA SUGERIDA:
    - 2 músicas adequadas ao conteúdo da foto e virais em PT + BR agora
    
    #️⃣ HASHTAGS (20):
    - Específicas para o conteúdo desta foto
    - Mix de hashtags portuguesas e brasileiras
    - Divididas por: populares, médias, nicho, Brasil, lifestyle
    
    ⏰ MELHOR HORA PARA PUBLICAR:
    - Hora exata para Portugal + Brasil
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

def suggest_crossfit_reel(instagram_data, personal_profile):
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
    
    O Álvaro faz CrossFit hoje e grava sempre.
    Os vídeos são IMPROVISO — clips de cada movimento do WOD,
    sem planeamento, transições dinâmicas entre movimentos.
    
    Cria sugestões para o Reel de CrossFit de hoje em português:
    
    ⚡ GANCHO — 5 opções diferentes para escolher:
    (os primeiros 3 segundos que param o scroll)
    
    💪 COMO GRAVAR:
    - Estilo de gravação (improviso, clips naturais)
    - Quantos clips e duração de cada
    
    ✂️ EDIÇÃO NO CAPCUT:
    - Como usar o Auto Beat
    - Dica de transições
    
    🎵 3 MÚSICAS SUGERIDAS:
    - Músicas com beat forte, virais em Portugal e Brasil agora
    - Perfeitas para CrossFit e transições rápidas
    
    ✍️ LEGENDA:
    - 3 opções no estilo do Álvaro (curtas, descontraídas, PT + BR)
    
    #️⃣ HASHTAGS (20):
    - Específicas para CrossFit
    - Mix PT + BR
    
    ⏰ MELHOR HORA PARA PUBLICAR:
    - Hora exata para Portugal + Brasil
    
    REGRAS:
    - Tom descontraído e autêntico
    - Nunca focar em menores de idade
    - Sugestões práticas para iPhone
    """
    
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

# ============================================================
# ÁLVARO NA COZINHA (DOMINGO)
# ============================================================

def suggest_alvaro_na_cozinha(instagram_data, personal_profile):
    prompt = f"""
    És um especialista em conteúdo de culinária para Instagram.
    Hoje é domingo — dia do Álvaro na Cozinha!
    
    Perfil: {personal_profile}
    Dados: {instagram_data}
    
    O Álvaro cozinha sempre em IMPROVISO — sem guião, natural e autêntico.
    O público é 71.7% mulheres, Portugal (77.6%) e Brasil (11.5%).
    Os brasileiros ADORAM receitas portuguesas tradicionais.
    
    Cria o episódio semanal do Álvaro na Cozinha em português:
    
    📈 RECEITA EM ALTA ESTA SEMANA PT + BR:
    - Nome da receita (que esteja viral agora em Portugal e/ou Brasil)
    - Porquê está em alta
    
    📝 RECEITA COMPLETA:
    - Ingredientes simples
    - Passo a passo fácil
    
    📱 COMO GRAVAR — IMPROVISO TOTAL:
    - Coloca o iPhone apoiado na cozinha
    - Deixa gravar enquanto cozinhas
    - Fala naturalmente como se contasses a um amigo
    - Momentos de ouro a NÃO cortar (erros, reações, surpresas)
    
    ✂️ EDIÇÃO NO CAPCUT:
    - Como montar o vídeo
    - Dica de texto e música
    
    🎵 3 MÚSICAS SUGERIDAS:
    - Descontraídas, tom de domingo em casa
    - Virais em PT + BR agora
    
    ⚡ GANCHO — 5 opções para escolher:
    (primeiros 3 segundos do Reel)
    
    ✍️ 3 LEGENDAS NO ESTILO DO ÁLVARO:
    - Opção 1: humor e improviso
    - Opção 2: série reconhecível (#AlvaroNaCozinha)
    - Opção 3: call to action para o Brasil
    
    #️⃣ HASHTAGS (20):
    - Série: #AlvaroNaCozinha
    - Receita específica
    - Mix PT + BR
    
    ⏰ MELHOR HORA PARA PUBLICAR:
    - Hora exata para Portugal + Brasil ao domingo
    """
    
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

# ============================================================
# SUGESTÃO QUANDO NÃO HÁ FOTOS BOAS
# ============================================================

def suggest_no_photo_content(workout, instagram_data, personal_profile, is_rainy):
    today = datetime.now().strftime("%A")
    
    prompt = f"""
    És um especialista em conteúdo para Instagram.
    Hoje é {today}.
    Treino de hoje: {workout}
    Está a chover: {is_rainy}
    
    Perfil: {personal_profile}
    Dados: {instagram_data}
    
    Não há fotos boas na pasta hoje.
    Com base no perfil e gostos do Álvaro, sugere alternativas em português:
    
    {'🏋️ DIA DE CROSSFIT — sem fotos mas há treino para gravar!' if workout == 'crossfit' else ''}
    {'🏃 DIA DE HYROX — sem gravação de treino, sugere outras opções:' if workout == 'hyrox' else ''}
    {'😴 DIA DE DESCANSO — sugere conteúdo lifestyle:' if workout == 'descanso' else ''}
    
    Sugere 3 opções de conteúdo com base nos gostos do Álvaro:
    - CrossFit / treino
    - Álvaro na Cozinha (se for fim de semana ou estiver a chover)
    - Humor do dia a dia em Coimbra
    - Lifestyle / foto rápida ao ar livre (se houver sol)
    
    Para cada opção:
    - Conceito concreto
    - Como executar em menos de 30 minutos com iPhone
    - Gancho sugerido
    """
    
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

# ============================================================
# FOCO DO DIA (com ou sem token)
# ============================================================

def get_daily_focus(instagram_data, personal_profile, has_token):
    today = datetime.now().strftime("%A")
    
    if has_token:
        prompt = f"""
        Hoje é {today}.
        Perfil: {personal_profile}
        Dados reais do Instagram desta semana: {instagram_data}
        
        Com base nos dados reais, responde em português:
        
        📊 ANÁLISE DOS ÚLTIMOS DIAS:
        - Posts recentes e performance (views, seguidores ganhos)
        - O que funcionou melhor
        - O que não funcionou
        
        💡 TENDÊNCIA:
        - O que está a crescer
        - O que evitar esta semana
        
        🎯 FOCO DE HOJE:
        - Seguidores atuais
        - Meta realista para hoje
        - Ação concreta para crescer
        
        ⏰ MELHOR HORA PARA PUBLICAR HOJE:
        - Hora exata baseada nos teus dados reais
        - Segunda melhor opção
        """
    else:
        prompt = f"""
        Hoje é {today}.
        Perfil: {personal_profile}
        
        Responde em português:
        
        ⏰ MELHOR HORA PARA PUBLICAR HOJE:
        - Hora exata para Portugal + Brasil
        - Segunda melhor opção
        - Justificação baseada no dia da semana e público PT + BR
        
        🎯 FOCO DE HOJE:
        - Uma dica concreta para crescer hoje
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
    instagram_data, has_token = get_instagram_data()
    if has_token:
        print("✅ Dados reais carregados!")
    else:
        print("⚠️  Sem token — usando perfil.txt")
    
    # 3. Clima em Coimbra
    print("\n🌤️ CLIMA EM COIMBRA AGORA:")
    weather_text, is_sunny, is_rainy = get_weather()
    print(f"   {weather_text}")
    
    # 4. Contexto do dia
    day_name, day_context = get_day_context()
    print(f"\n📅 CONTEXTO — {day_name.upper()}:")
    print(f"   {day_context}")
    
    # 5. Treino do dia
    workout = ask_workout(day_name)
    
    # 6. Foco do dia + melhor hora
    print("\n" + "=" * 50)
    print("⏰ MELHOR HORA PARA PUBLICAR HOJE:")
    print("=" * 50)
    focus = get_daily_focus(instagram_data, personal_profile, has_token)
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
    
    if photos:
        scored_photos = score_all_photos(photos, instagram_data, personal_profile)
        
        # Ordenar por pontuação
        scored_photos.sort(key=lambda x: x[1], reverse=True)
        best_name, best_score, best_motivo = scored_photos[0]
        
        if best_score >= 7:
            print(f"🏆 MELHOR FOTO: {best_name} ({best_score}/10)")
            if len(scored_photos) > 1:
                second = scored_photos[1]
                print(f"⚠️  Segunda melhor: {second[0]} ({second[1]}/10) se não gostares")
            
            best_photo = os.path.join(PHOTOS_FOLDER, best_name)
            
            # Aviso sobre fotos vs reels com token
            if has_token:
                print(f"\n⚠️  ATENÇÃO:")
                print(f"   Verifica os dados — se os Reels têm muito mais views que fotos,")
                print(f"   considera focar-te no Reel hoje e guardar a foto para outro dia!")
            
            print("\n" + "=" * 50)
            print(f"📋 ANÁLISE COMPLETA — {best_name}:")
            print("=" * 50)
            analysis = analyze_best_photo(best_photo, instagram_data, personal_profile, best_score)
            print(analysis)
        else:
            print(f"⚠️  NENHUMA FOTO EXCELENTE HOJE!")
            print(f"   A melhor foi {best_name} com {best_score}/10 — abaixo do ideal (7+)")
            best_photo = None
    else:
        if day == 6:  # Domingo
            print("📁 Pasta vazia! Sem fotos hoje.")
            print("   💡 Sem problema — hoje é domingo e o foco é o Álvaro na Cozinha! 🍳")
        else:
            print("📁 Pasta vazia! Sem fotos hoje.")
    
    # 8. Conteúdo do dia
    print("\n" + "=" * 50)
    
    if day == 6:  # Domingo — Álvaro na Cozinha
        print("🍳 ÁLVARO NA COZINHA — EPISÓDIO DA SEMANA:")
        print("=" * 50)
        cozinha = suggest_alvaro_na_cozinha(instagram_data, personal_profile)
        print(cozinha)
    
    elif workout == "crossfit":
        print("🎬 REEL DE CROSSFIT — HOJE:")
        print("=" * 50)
        reel = suggest_crossfit_reel(instagram_data, personal_profile)
        print(reel)
    
    elif workout == "hyrox":
        print("🏃 DIA DE HYROX — SEM GRAVAÇÃO")
        print("=" * 50)
        if not best_photo:
            print("💡 Sem foto boa e sem gravação de Hyrox...")
            print("   Aqui estão alternativas com base nos teus gostos:\n")
            alternatives = suggest_no_photo_content(workout, instagram_data, personal_profile, is_rainy)
            print(alternatives)
        else:
            print("✅ Tens a foto para publicar hoje — sem necessidade de gravar!")
    
    else:  # Descanso
        print("😴 DIA DE DESCANSO")
        print("=" * 50)
        if not best_photo:
            print("💡 Sem foto boa e dia de descanso...")
            print("   Aqui estão alternativas com base nos teus gostos:\n")
            alternatives = suggest_no_photo_content(workout, instagram_data, personal_profile, is_rainy)
            print(alternatives)
        else:
            print("✅ Tens a foto para publicar hoje — aproveita o descanso!")
    
    print("\n" + "=" * 50)
    print("✅ Tudo pronto! Boas publicações Álvaro! 🚀")
    print("=" * 50)

if __name__ == "__main__":
    run_agent()