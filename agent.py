from google import genai
from google.genai import types
import os
import base64
from dotenv import load_dotenv
from instagram_api import get_profile, get_posts

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-1.5-flash-8b"
PHOTOS_FOLDER = r"C:\Users\alvar\Desktop\Fotos para o insta"
PROFILE_FILE = r"C:\Users\alvar\Desktop\agente-instagram\perfil.txt"

def load_profile():
    """Lê o ficheiro de perfil pessoal"""
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def get_best_time(instagram_data, personal_profile):
    """Sugere a melhor hora para postar"""
    prompt = f"""
    És um especialista em Instagram e marketing digital.
    
    Perfil pessoal:
    {personal_profile}
    
    Dados do Instagram:
    {instagram_data}
    
    Com base nestes dados reais, responde em português:
    
    ⏰ MELHOR HORA PARA POSTAR HOJE:
    - Hora exata recomendada e porquê
    - Segunda melhor opção
    
    📅 MELHORES DIAS DA SEMANA:
    - Top 3 dias para publicar
    
    💡 DICA PERSONALIZADA:
    - Uma sugestão específica para o perfil do Álvaro
    """
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

def analyze_best_photo(image_path, instagram_data, personal_profile):
    """Analisa a foto com contexto completo do perfil"""
    
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    ext = image_path.split(".")[-1].lower()
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"

    prompt = f"""
    És um especialista em Instagram e marketing digital.
    
    Perfil pessoal do criador:
    {personal_profile}
    
    Dados reais do Instagram:
    {instagram_data}
    
    Analisa esta foto tendo em conta que:
    - O público é 71.7% mulheres, 25-34 anos
    - O melhor conteúdo é pessoal e descontraído
    - O perfil é português mas tem audiência no Brasil
    - Os Stories têm 87.3% das views (muito mais que posts)
    - Os Reels têm apenas 1.8% (grande oportunidade!)
    
    Responde em português com:
    
    📸 AVALIAÇÃO DA FOTO:
    - Pontos fortes
    - O que melhorar
    
    ✏️ EDIÇÃO RECOMENDADA:
    - Ajustes específicos (brilho, contraste, saturação)
    - Filtro ou preset recomendado
    - App sugerida (Lightroom, VSCO, etc.)
    
    ✍️ 3 DESCRIÇÕES PERSONALIZADAS:
    - Opção 1: tom informal e engraçado (estilo do Álvaro)
    - Opção 2: mais inspiracional mas autêntico
    - Opção 3: com pergunta para gerar comentários
    
    🎵 MÚSICA SUGERIDA:
    - 2 músicas ou géneros para Reel/Story
    
    #️⃣ HASHTAGS (20):
    - Mix de hashtags portuguesas e brasileiras
    - Divididas por: populares, médias e nicho
    
    🎬 IDEIA DE REEL:
    - Como transformar esta foto num Reel viral
    - Os teus Reels têm apenas 1.8% das views — grande oportunidade!
    """
    
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(
                data=base64.b64decode(image_data),
                mime_type=mime
            ),
            prompt
        ]
    )
    return response.text

def pick_best_photo(photos, personal_profile):
    """Escolhe a melhor foto para publicar hoje"""
    prompt = f"""
    Perfil do criador:
    {personal_profile}
    
    Fotos disponíveis para publicar:
    {chr(10).join([f"- {p}" for p in photos])}
    
    O público é 71.7% mulheres, 25-34 anos, Portugal e Brasil.
    O melhor conteúdo é pessoal e descontraído.
    
    Qual o melhor ficheiro para publicar hoje?
    Responde APENAS com o nome do ficheiro e uma razão curta em português.
    """
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

def run_agent():
    print("\n🤖 AGENTE INSTAGRAM - A INICIAR...")
    print("=" * 50)
    
    # 1. Carregar perfil pessoal
    print("\n👤 A carregar o teu perfil...")
    personal_profile = load_profile()
    if personal_profile:
        print("✅ Perfil pessoal carregado!")
    else:
        print("⚠️  Ficheiro perfil.txt não encontrado!")
    
    # 2. Buscar dados do Instagram
    print("\n🔍 A ligar ao Instagram...")
    try:
        instagram_profile = get_profile()
        instagram_posts = get_posts()
        instagram_data = f"Perfil: {instagram_profile}\nPosts: {instagram_posts}"
        print("✅ Dados do Instagram carregados!")
    except Exception as e:
        print(f"⚠️  Instagram sem token ainda — usando apenas perfil.txt")
        instagram_data = "Token do Instagram ainda não configurado."
    
    # 3. Melhor hora para postar
    print("\n⏰ A calcular a melhor hora para postar hoje...")
    best_time = get_best_time(instagram_data, personal_profile)
    print("\n" + "=" * 50)
    print(best_time)
    
    # 4. Ver fotos na pasta
    print("\n🖼️  A verificar a tua pasta de fotos...")
    extensions = [".jpg", ".jpeg", ".png", ".webp"]
    
    if not os.path.exists(PHOTOS_FOLDER):
        print("❌ Pasta 'Fotos para o insta' não encontrada no Desktop!")
        return
    
    photos = [f for f in os.listdir(PHOTOS_FOLDER)
              if os.path.splitext(f)[1].lower() in extensions]
    
    if not photos:
        print("❌ Nenhuma foto encontrada na pasta!")
        return
    
    print(f"✅ Encontrei {len(photos)} foto(s)!")
    
    # 5. Escolher melhor foto
    if len(photos) == 1:
        chosen_photo = photos[0]
        print(f"\n📸 Apenas uma foto disponível: {chosen_photo}")
    else:
        print("\n🏆 A escolher a melhor foto para hoje...")
        best_photo_response = pick_best_photo(photos, personal_profile)
        print(best_photo_response)
        chosen_photo = photos[0]
        for photo in photos:
            if photo.lower() in best_photo_response.lower():
                chosen_photo = photo
                break
    
    # 6. Análise completa da foto
    full_path = os.path.join(PHOTOS_FOLDER, chosen_photo)
    print(f"\n📸 A analisar em detalhe: {chosen_photo}")
    print("⏳ A gerar sugestões personalizadas para o teu perfil...")
    
    analysis = analyze_best_photo(full_path, instagram_data, personal_profile)
    
    print("\n" + "=" * 50)
    print("📋 ANÁLISE COMPLETA:")
    print("=" * 50)
    print(analysis)
    print("\n" + "=" * 50)
    print("✅ Análise concluída! Boas publicações! 🚀")

if __name__ == "__main__":
    run_agent()