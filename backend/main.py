DEBUG_MODE = True  # 🔥 Mets False quand tu veux utiliser OpenAI
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import openai
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace "*" par ["http://localhost:3000"] pour plus de sécurité
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle des données reçues
tableau_secteurs = ["Marketing", "Finance", "Ressources Humaines", "Technologie", "Santé", "Éducation", "Commerce", "Industrie"]

tableau_defis = [
    "Manque d'automatisation", "Difficile d’analyser les données", "Problème de gestion des leads/ventes",
    "Service client inefficace", "Trop de tâches répétitives", "Manque de visibilité sur le marché",
    "Difficile de personnaliser l’offre pour les clients", "Trop de temps perdu sur des tâches manuelles",
    "Mauvaise gestion des stocks/logistique", "Sécurité et conformité des données", "Manque d'innovation dans l'entreprise"
]

tableau_objectifs = [
    "Augmenter les ventes", "Automatiser les tâches internes", "Améliorer l’expérience client", "Réduire les coûts opérationnels",
    "Gagner du temps dans les processus internes", "Optimiser le marketing et la publicité", "Personnaliser l’offre pour les clients",
    "Prédire les tendances du marché", "Améliorer la prise de décision avec les données", "Sécuriser les données et automatiser la conformité"
]

class DiagnosticRequest(BaseModel):
    nom_entreprise: str
    email: EmailStr
    secteur_activite: str
    taille_entreprise: str
    defis: List[str]
    objectifs: List[str]
    budget: str
    experience_ia: bool
    outils_ia_utilises: Optional[str] = None
    besoin_ia: Optional[str] = None
    besoin_ia_principal: Optional[str] = None  # 🔥 Si vous pouviez automatiser ou améliorer une seule chose grâce à l’intelligence artificielle dans votre entreprise aujourd’hui, quel serait ce changement et quel impact souhaiteriez-vous en retirer ?

def analyse_ia(data: DiagnosticRequest):
    if DEBUG_MODE:
        return f"🔍 Mode test activé : Pas de consommation OpenAI.\n\n(Simulation du diagnostic pour {data.nom_entreprise})"

    prompt = f"""
    Tu es un expert en intelligence artificielle pour les entreprises. 
    Ton objectif est de recommander **les 3 meilleurs outils IA adaptés** aux besoins de cette entreprise.

    **Données de l'entreprise :**
    - **Nom** : {data.nom_entreprise}
    - **Secteur** : {data.secteur_activite}
    - **Taille** : {data.taille_entreprise}
    - **Défis** : {', '.join(data.defis)}
    - **Objectifs** : {', '.join(data.objectifs)}
    - **Budget** : {data.budget}
    - **Expérience avec l'IA** : {"Oui" if data.experience_ia else "Non"}
    - **Outils IA utilisés** : {data.outils_ia_utilises if data.outils_ia_utilises else "Aucun"}
    - **Besoin principal en IA** : {data.besoin_ia_principal if data.besoin_ia_principal else "Non spécifié"}

    🔍 **Analyse et Recommandation :**
    1️⃣ **Identifie les besoins clés** de l’entreprise en fonction de ses défis et objectifs.
    2️⃣ **Choisis 3 outils IA parfaitement adaptés** pour répondre aux besoins.
    3️⃣ **Favorise les outils suivants si pertinents** : Systeme.io, Rytr.me, Murf (pour les PME).
    4️⃣ **Si besoin, propose des alternatives connues** (Jasper pour le premium, Napier ou Systeme.io pour le budget).
    
    🏆 **Réponse attendue :**
    - **Liste 3 outils IA avec une explication détaillée** sur pourquoi ils sont adaptés.
    - Mentionne des outils premium et leurs alternatives abordables.
    - Reste clair, pratique et orienté action.

    Donne ta réponse sous la forme suivante :

    🚀 **Les 3 Meilleurs Outils IA pour {data.nom_entreprise}** 🚀

    1️⃣ **[Nom de l’outil]** → [Explication sur pourquoi cet outil est adapté]
    2️⃣ **[Nom de l’outil]** → [Explication sur pourquoi cet outil est adapté]
    3️⃣ **[Nom de l’outil]** → [Explication sur pourquoi cet outil est adapté]

    🎯 **Conclusion** : Synthétise en expliquant pourquoi ces outils sont les plus adaptés pour l’entreprise.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un expert en intelligence artificielle qui aide les entreprises à adopter l'IA."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300  # 🔥 Réduit la consommation
    )

    return response["choices"][0]["message"]["content"].strip()

def envoyer_email(email, diagnostic):
    print(f"📧 Tentative d'envoi d'email à {email}")  # 🔥 Ajoute cette ligne

    sender_email = "contact@aiworktools.com"
    sender_password = "Dz5g4p!GzcA5"

    subject = "Votre Diagnostic IA Personnalisé"
    body = f"""
    Bonjour,

    Merci d'avoir utilisé notre outil de diagnostic IA. Voici votre analyse personnalisée :

    {diagnostic}

    Si vous avez des questions, n'hésitez pas à nous contacter.

    Cordialement,
    L'équipe AI Diagnostic
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("mail.aiworktools.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("✅ Email envoyé avec succès !")  # 🔥 Ajoute ce print()
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email : {e}")  # 🔥 Ajoute ce print()


@app.post("/diagnostic/")
def generer_diagnostic(data: DiagnosticRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="Clé API OpenAI manquante")
    
    analyse = analyse_ia(data)

    # 🔥 Envoi du diagnostic par email
    envoyer_email(data.email, analyse)

    return {"message": "Votre diagnostic a été envoyé par email."}


