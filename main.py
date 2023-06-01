from flask import Flask, request, jsonify
import requests, math

app = Flask(__name__)

def format_size(size):
    if size < 1024:
        return f"{size} KB"
    elif size < 1024 * 1024:
        return f"{math.ceil(size / 1024)} MB"
    else:
        return f"{math.ceil(size / (1024 * 1024))} GB"
    
def get_all_repositories(username, access_token, forked):
  url = f'https://api.github.com/users/{username}/repos'
  headers = {'Authorization': f'Bearer {access_token}'}
  repositories = []

  params = {'page': 1, 'per_page': 100}
  if not forked:
    params["type"] = "owner"

  while True:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
      page_repositories = response.json()
      repositories.extend(page_repositories)

      if len(page_repositories) < 100:
        break  # Reached the last page of repositories
      else:
        params['page'] += 1
    else:
      break  # Error occurred, break the loop

  return repositories


@app.route('/repositories', methods=['GET'])
def get_repository_stats():
  username = request.args.get('username')
  forked = request.args.get('forked')

  access_token = 'YOUR_TOEKN' #add your token

  repositories = get_all_repositories(username, access_token, forked)

  if repositories:
    total_repositories = len(repositories)
    total_stargazers = sum(repo['stargazers_count'] for repo in repositories)
    total_forks = sum(repo['forks_count'] for repo in repositories)
    average_repository_size = sum(
      repo['size'] for repo in repositories) / total_repositories

    languages = {}
    for repo in repositories:
      language = repo['language']
      if language:
        if language in languages:
          languages[language] += 1
        else:
          languages[language] = 1

    sorted_languages = sorted(languages.items(),
                              key=lambda x: x[1],
                              reverse=True)

    response_data = {
      'total_repositories': total_repositories,
      'total_stargazers': total_stargazers,
      'total_forks': total_forks,
      'average_repository_size': format_size(average_repository_size),
      'languages': sorted_languages
    }

    return jsonify(
      response_data), 200  # Return response with status code 200 (OK)
  else:
    error_message = f'Failed to retrieve repository data for user {username}.'
    return jsonify({
      'error': error_message
    }), 500  # Return response with status code 500 (Internal Server Error)


if __name__ == '__main__':
  app.run()
