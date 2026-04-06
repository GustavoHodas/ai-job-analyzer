import requests
import json

url = "https://arbeitnow.com/api/job-board-api"

response = requests.get(url)

print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    jobs = data.get("data", [])

    print("Quantidade total de vagas encontradas:", len(jobs))

    keywords = ["data", "engineer", "analyst", "python", "ai", "machine learning"]
    user_profile = ["python", "sql", "docker"]

    skill_keywords = [
        "python",
        "sql",
        "docker",
        "aws",
        "airflow",
        "pandas",
        "machine learning",
        "ai",
        "data engineering",
        "etl",
        "spark",
        "linux"
    ]

    job_list = []

    for job in jobs:
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()

        if any(keyword in title for keyword in keywords):
            found_skills = []

            for skill in skill_keywords:
                if skill in title or skill in description:
                    found_skills.append(skill)

            matched_skills = [skill for skill in found_skills if skill in user_profile]
            missing_skills = [skill for skill in found_skills if skill not in user_profile]

            if len(found_skills) > 0:
                match_percentage = int((len(matched_skills) / len(found_skills)) * 100)
            else:
                match_percentage = 0

            job_data = {
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location"),
                "remote": job.get("remote"),
                "url": job.get("url"),
                "found_skills": found_skills,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "match_percentage": match_percentage
            }

            job_list.append(job_data)

    job_list.sort(key=lambda x: x["match_percentage"], reverse=True)

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

    skill_demand = {}

    for job in job_list:
        for skill in job["missing_skills"]:
            if skill in skill_demand:
                skill_demand[skill] += 1
            else:
                skill_demand[skill] = 1

    sorted_skills = sorted(skill_demand.items(), key=lambda x: x[1], reverse=True)

    print("\nSkills mais pedidas que você NÃO tem:")
    for skill, count in sorted_skills[:10]:
        print(f"{skill} aparece em {count} vagas")

else:
    print("Erro ao acessar a API")
