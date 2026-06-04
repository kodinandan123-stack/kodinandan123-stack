import os
import re
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
USERNAME = os.environ.get("GITHUB_USERNAME", "kodinandan123-stack")

# Repos to always skip (profile repo itself + empty/non-project repos)
SKIP_REPOS = {USERNAME, "daily-log"}

# Custom descriptions for each project
CUSTOM_DESCRIPTIONS = {
    "Chat-App": "Real-time chat application",
    "Weather-App": "Live weather data fetcher",
    "Task-Manager-App": "Task organizer with CRUD",
    "Personal-Finance-Tracker": "Income, expense & savings tracker",
}

# Full tech stack for each project
# When you start a new project, just add a line here like:
# "My-New-Repo": "React, Node.js, MongoDB",
TECH_STACK = {
    "Chat-App": "HTML, CSS, JS, Node.js, Socket.io",
    "Weather-App": "HTML, CSS, JS, REST API",
    "Task-Manager-App": "HTML, CSS, JS, Node.js, Express",
    "Personal-Finance-Tracker": "React, Node.js, Express, MongoDB, Chart.js",
}

# Emoji map by tech/language
TECH_EMOJI = {
    "Chat-App": "💬",
    "Weather-App": "🌤️",
    "Task-Manager-App": "✅",
    "Personal-Finance-Tracker": "💰",
}

DEFAULT_EMOJI = "📁"

def get_repos():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def build_row(repo):
    name = repo["name"]
    url = repo["html_url"]
    description = CUSTOM_DESCRIPTIONS.get(name) or repo.get("description") or "No description yet"
    tech = TECH_STACK.get(name) or repo.get("language") or "N/A"
    emoji = TECH_EMOJI.get(name, DEFAULT_EMOJI)
    return f"| [{emoji} {name}]({url}) | {description} | {tech} |"

def update_readme(rows_markdown):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    table_header = "| Project | Description | Tech |\n|---|---|---|\n"
    new_table = table_header + "\n".join(rows_markdown)

    pattern = r"<!-- PROJECTS:START -->.*?<!-- PROJECTS:END -->"
    replacement = f"<!-- PROJECTS:START -->\n{new_table}\n<!-- PROJECTS:END -->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md updated successfully!")

def main():
    repos = get_repos()
    rows = []
    for repo in repos:
        if repo["name"] in SKIP_REPOS:
            continue
        if repo.get("fork"):
            continue
        rows.append(build_row(repo))

    if rows:
        update_readme(rows)
    else:
        print("No repos found to add.")

if __name__ == "__main__":
    main()
