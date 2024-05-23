import httpx
from prefect import flow, task
from prefect_aws.ecs import ECSTask
from prefect_aws import AwsCredentials
from prefect_aws.secrets_manager import AwsSecret

@task(retries=2)
def get_repo_info(repo_owner: str, repo_name: str):
    """Get info about a repo - will retry twice after failing"""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    api_response = httpx.get(url)
    api_response.raise_for_status()
    repo_info = api_response.json()
    return repo_info


@task
def get_contributors(repo_info: dict):
    """Get contributors for a repo"""
    contributors_url = repo_info["contributors_url"]
    response = httpx.get(contributors_url)
    response.raise_for_status()
    contributors = response.json()
    return contributors


@flow(log_prints=True)
def repo_info(repo_owner: str = "PrefectHQ", repo_name: str = "prefect"):
    """
    Given a GitHub repository, logs the number of stargazers
    and contributors for that repo.
    """
    repo_info = get_repo_info(repo_owner, repo_name)
    print(f"Stars 🌠 : {repo_info['stargazers_count']}")

    contributors = get_contributors(repo_info)
    print(f"Number of contributors 👷: {len(contributors)}")

    print("hello world")

    aws_secret_block = AwsSecret.load("non")
    aws_credentials_block = AwsCredentials.load("my-aws-creds")
    ecs_task_block = ECSTask.load("test")
    
    print(aws_secret_block, aws_credentials_block, ecs_task_block)
    print("_____________")


if __name__ == "__main__":
    repo_info()