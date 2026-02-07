from dotenv import load_dotenv

from src.crew.app_review_crew import build_crew


print("main started")

def main():
    load_dotenv()
    result = build_crew().kickoff()
    print(result)
    print("main finished")


if __name__ == "__main__":
    main()
