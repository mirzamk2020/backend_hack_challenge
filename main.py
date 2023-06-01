import requests

def get_aggregated_stats(username, include_forks=True):
    base_url = f"https://api.github.com/users/{username}/repos"
    per_page = 100
    params = {"per_page": per_page, "page": 1}
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "Bearer <YOUR_TOKEN>"  # Replace with your token
    }

    if not include_forks:
        params["type"] = "owner"

    repositories = []

    while True:
        response = requests.get(base_url, params=params, headers=headers)
        repos = response.json()

        if not repos:
            break

        repositories.extend(repos)

        if len(repos) < per_page:
            break

        params["page"] += 1

    total_count = len(repositories)
    total_stargazers = sum(repo["stargazers_count"] for repo in repositories)
    total_forks = sum(repo["forks_count"] for repo in repositories)
    average_size = sum(repo["size"] for repo in repositories) / total_count

    languages = {}
    for repo in repositories:
        language = repo["language"]
        if language:
            if language in languages:
                languages[language] += 1
            else:
                languages[language] = 1

    sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)

    aggregated_stats = {
        "total_count": total_count,
        "total_stargazers": total_stargazers,
        "total_forks": total_forks,
        "average_size": average_size,
        "languages": sorted_languages
    }

    return aggregated_stats

# Demo usage
username = "seantomburke"
aggregated_stats = get_aggregated_stats(username, include_forks=False)
print(aggregated_stats)
