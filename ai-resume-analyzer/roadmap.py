def generate_roadmap(missing_skills):
    roadmap = []

    for skill in missing_skills:
        roadmap.append(f"Learn basics of {skill}")
        roadmap.append(f"Practice {skill} with projects")
        roadmap.append(f"Get certified in {skill}")

    return roadmap
