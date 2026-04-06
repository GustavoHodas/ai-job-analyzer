import json
from api import fetch_jobs
from analyzer import analyze_jobs, get_missing_skill_demand
from config import KEYWORDS, USER_PROFILE, SKILL_KEYWORDS

jobs = fetch_jobs()

if jobs is None:
    print("Erro ao acessar a API")
else:
    print("Quantidade total de vagas encontradas:", len(jobs))

    job_list = analyze_jobs(jobs, KEYWORDS, USER_PROFILE, SKILL_KEYWORDS)

    print("\nVagas analisadas:")
    for item in job_list[:10]:
        print("-" * 50)
        print("Título:", item["title"])
        print("Empresa:", item["company"])
        print("Match:", f'{item["match_percentage"]}%')
        print("Skills encontradas:", item["found_skills"])
        print("Skills que você já tem:", item["matched_skills"])
        print("Skills faltando:", item["missing_skills"])

    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(job_list, f, indent=4, ensure_ascii=False)

    print("\nArquivo jobs.json atualizado com sucesso!")

    sorted_skills = get_missing_skill_demand(job_list)

    print("\nSkills mais pedidas que você NÃO tem:")
    for skill, count in sorted_skills[:10]:
        print(f"{skill} aparece em {count} vagas")