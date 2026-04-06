def analyze_jobs(jobs, keywords, user_profile, skill_keywords):
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
    return job_list


def get_missing_skill_demand(job_list):
    skill_demand = {}

    for job in job_list:
        for skill in job["missing_skills"]:
            if skill in skill_demand:
                skill_demand[skill] += 1
            else:
                skill_demand[skill] = 1

    return sorted(skill_demand.items(), key=lambda x: x[1], reverse=True)