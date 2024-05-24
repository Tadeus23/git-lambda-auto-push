import os
import git
from git import Repo

def lambda_handler(event, context):
    repo_url = os.getenv('REPO_URL')
    git_user = os.getenv('GIT_USER')
    git_password = os.getenv('GIT_PASSWORD')

    local_path = '/tmp/repo'

    authenticated_url = repo_url.replace('https://', f'https://{git_user}:{git_password}@')

    repo = Repo.clone_from(authenticated_url, local_path, branch='main')

    file_path = os.path.join(local_path, 'your_file.txt')
    with open(file_path, 'w') as file:
        file.write('Automated change by AWS Lambda\n')

    repo.git.add(update=True)
    repo.index.commit('Automated commit by AWS Lambda')

    origin = repo.remote(name='origin')
    origin.push()

    return {
        'statusCode': 200,
        'body': 'Code change pushed successfully'
    }