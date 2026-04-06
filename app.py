import streamlit as st
import json
from analyzer import analyze_jobs

# Configuração da página (SEMPRE no topo)
st.set_page_config(page_title="AI Job Analyzer", layout="wide")

# Input do usuário
user_input = st.text_input("Digite suas skills (ex: python, sql, aws)")

user_skills = [skill.strip().lower() for skill in user_input.split(",")] if user_input else ["python", "sql", "docker"]

st.info(f"🔎 Analisando com base nas skills: {', '.join(user_skills)}")

# Título
st.title("🤖 AI Job Analyzer - Seu Assistente de Carreira")
st.write("Analise vagas, compare com seu perfil e descubra skills em alta no mercado.")

# Carregar jobs
with open("jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

# Analisar jobs dinamicamente
analyzed_jobs = analyze_jobs(
    jobs,
    keywords=["engineer", "data", "python"],
    user_profile=user_skills,
    skill_keywords=["python", "sql", "aws", "docker", "ai"]
)

st.subheader("📊 Top vagas para você")

# Mostrar vagas
for job in analyzed_jobs[:10]:
    with st.container():
        st.markdown("---")
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"### {job['title']}")
            st.write(f"**Empresa:** {job['company'] or 'Não informado'}")
            st.write(f"**Local:** {job['location']}")
            st.markdown(f"[🔗 Ver vaga]({job['url']})")

        with col2:
            st.metric("Match", f"{job['match_percentage']}%")
            st.progress(job["match_percentage"] / 100)

if job["matched_skills"]:
    st.success("✅ " + " | ".join(job["matched_skills"]))
else:
    st.info("ℹ️ Nenhuma skill relevante encontrada")

if job["missing_skills"]:
    st.error("❌ " + " | ".join(job["missing_skills"]))
else:
    st.success("🎉 Nenhuma skill faltando")
# Skills mais demandadas
st.subheader("📈 Skills mais pedidas que você NÃO tem")

skill_count = {}

for job in analyzed_jobs:
    for skill in job["missing_skills"]:
        skill_count[skill] = skill_count.get(skill, 0) + 1

sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)

for skill, count in sorted_skills[:10]:
    st.write(f"🔥 {skill} aparece em {count} vagas")