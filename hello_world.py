import httpx
from prefect import flow


@flow(log_prints=True)
def hello_world():
    print("hello world")
    print("_______________")


if __name__ == "__main__":
    hello_world()