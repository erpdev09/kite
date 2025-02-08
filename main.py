import json
import os
import random
import time
import requests
import sys
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

# Configure agents with specific topics
agents = {
    "deployment_p5J9lz1Zxe7CYEoo0TZpRVay": {"name": "Professor 🧠", "topic": "ai"},
    "deployment_7sZJSiCqCNDy9bBHTEh7dwd9": {"name": "Crypto Buddy 💰", "topic": "crypto"},
    "deployment_SoFftlsf9z4fyA3QCHYkaANq": {"name": "Sherlock 🔎", "topic": "fraud_detection"}
}

# File to store daily interaction data
interaction_log_file = "interaction_log.json"
random_questions_file = "random_questions.json"

# Function to read daily interaction log
def read_interaction_log():
    try:
        with open(interaction_log_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save daily interaction log
def save_interaction_log(log_data):
    with open(interaction_log_file, "w") as f:
        json.dump(log_data, f, indent=2)

# Function to get today's date in UTC (YYYY-MM-DD)
def get_today_date_utc():
    now = datetime.utcnow()
    return now.strftime("%Y-%m-%d")

# Function to check and reset daily interactions if a new day has started
def check_and_reset_daily_interactions(log_data, daily_limit, wallet):
    today_utc = get_today_date_utc()
    if log_data.get("date") != today_utc:
        print(Fore.YELLOW + "⚠️ New day started! Resetting daily interactions for all agents.")
        log_data["date"] = today_utc
        log_data["wallet"] = wallet
        log_data["dailyLimit"] = daily_limit
        log_data["interactions"] = {agent_id: 0 for agent_id in agents}
    return log_data

# Function to read random questions from file based on topic
def get_random_questions_by_topic(file_path, topic, count):
    try:
        with open(file_path, "r") as f:
            questions = json.load(f)
        return random.sample(questions[topic], count)
    except Exception as e:
        print(Fore.RED + f"⚠️ Failed to read random questions for topic {topic}: {e}")
        exit(1)

# Function to send a question to an AI agent
def send_question_to_agent(agent_id, question):
    url = f"https://{agent_id.lower().replace('_', '-')}.stag-vxzy.zettablock.com/main"
    payload = {"message": question, "stream": False}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]
    except Exception as e:
        print(Fore.RED + f"⚠️ Error sending question to agent {agent_id}: {e}")
        return None

# Function to report usage
def report_usage(wallet, options):
    url = "https://quests-usage-dev.prod.zettablock.com/api/report_usage"
    payload = {
        "wallet_address": wallet,
        "agent_id": options["agent_id"],
        "request_text": options["question"],
        "response_text": options["response"],
        "request_metadata": {}
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(Fore.YELLOW + "✅ Usage data successfully reported!\n")
    except Exception as e:
        print(Fore.RED + f"⚠️ Failed to report usage: {e}\n")

# Main function
def main():
    print(Fore.CYAN + Style.BRIGHT + "🚀 Kite AI - Daily Interaction 🚀")
    print(Fore.CYAN + "----------------------------------------")
    print(Fore.MAGENTA + "Channel: Active")
    print(Fore.MAGENTA + "Author: jodohsaya")
    print(Fore.CYAN + "----------------------------------------\n")

    if not os.path.exists(random_questions_file):
        print(Fore.YELLOW + "⚠️ random_questions.json not found. Creating a new file...")
        os.system(f"{sys.executable} rand.py")
        print(Fore.GREEN + "✅ random_questions.json created successfully.")

    interaction_log = read_interaction_log()
    
    wallet = interaction_log.get("wallet")
    if not wallet:
        wallet = input(Fore.YELLOW + "🔑 Enter your wallet address: ").strip()
        if not wallet.startswith("0x") or len(wallet) != 42:
            print(Fore.RED + "⚠️ Invalid wallet address!")
            exit(1)
    
    daily_limit = interaction_log.get("dailyLimit", 20)
    if "dailyLimit" not in interaction_log:
        try:
            daily_limit = int(input(Fore.YELLOW + "🔢 Enter daily interaction limit per agent: "))
            if daily_limit <= 0:
                raise ValueError
        except ValueError:
            print(Fore.YELLOW + "⚠️ Invalid input! Using default limit of 20.")
            daily_limit = 20
    
    while True:
        interaction_log = check_and_reset_daily_interactions(interaction_log, daily_limit, wallet)
        save_interaction_log(interaction_log)

        random_questions_by_topic = {}
        for agent_id, agent_info in agents.items():
            topic = agent_info["topic"]
            random_questions_by_topic[agent_id] = get_random_questions_by_topic(random_questions_file, topic, daily_limit)

        for agent_id, agent_info in agents.items():
            if interaction_log["interactions"][agent_id] >= daily_limit:
                continue

            remaining_interactions = daily_limit - interaction_log["interactions"][agent_id]

            for _ in range(remaining_interactions):
                question = random_questions_by_topic[agent_id].pop()
                response = send_question_to_agent(agent_id, question)
                report_usage(wallet.lower(), {"agent_id": agent_id, "question": question, "response": response.get("content", "No response") if response else "No response"})
                interaction_log["interactions"][agent_id] += 1
                save_interaction_log(interaction_log)
                time.sleep(random.randint(5, 10))

        now = datetime.utcnow()
        next_reset = (now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))
        time.sleep((next_reset - now).total_seconds())

if __name__ == "__main__":
    main()
