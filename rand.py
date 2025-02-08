import json
import random

# List of keywords based on category
keywords = {
    "ai": [
        "AI", "machine learning", "neural networks", "AI ethics", "AI governance",
        "AI-powered trading", "automated decision-making", "AI-driven security",
        "natural language processing", "computer vision", "reinforcement learning",
        "AI in healthcare", "AI in finance", "AI in education", "AI in robotics"
    ],
    "crypto": [
        "blockchain", "smart contracts", "NFT", "DeFi", "DAO", "consensus mechanism",
        "public ledger", "crypto wallet", "Ethereum", "Bitcoin", "staking",
        "cryptographic algorithms", "tokenomics", "crypto regulations", "crypto mining",
        "crypto exchanges", "initial coin offerings", "stablecoins"
    ],
    "fraud_detection": [
        "identify fraudulent transactions", "security concerns", "zero-knowledge proofs",
        "transparency", "game theory in crypto", "privacy coins", "oracles",
        "anomaly detection", "behavioral analytics", "fraud prevention strategies",
        "biometric authentication", "multi-factor authentication", "risk assessment",
        "transaction monitoring", "fraud detection algorithms"
    ]
}

# Additional phrases for question variations
extra_phrases = [
    "in the future", "impact on economy", "challenges faced", "advantages and disadvantages",
    "real-world applications", "security concerns", "scalability issues", "role in financial markets",
    "integration with IoT", "comparison with traditional systems", "future predictions",
    "ethical concerns", "adoption by enterprises", "potential for mass adoption"
]

# Starters for different question structures
starters = [
    "What is", "How does", "Why is", "Can you explain", "What are the benefits of",
    "How can", "What makes", "What are the features of", "How does", "What is the purpose of",
    "Why should we use", "What are the risks of", "What are the future prospects of",
    "Discuss the role of", "Analyze the impact of", "Explain the concept of"
]

# Additional contexts for variation
contexts = ["in today's world", "for businesses", "for individuals", "in technology"]

# Function to generate a random question based on a topic
def generate_random_question(topic):
    random_starter = random.choice(starters)
    random_keyword = random.choice(keywords[topic])
    random_extra = random.choice(extra_phrases)
    random_context = random.choice(contexts)
    return f"{random_starter} {random_keyword} {random_extra} {random_context}?"

# Function to generate a set number of random questions per topic
def generate_questions_per_topic(count):
    questions = {
        "ai": [generate_random_question("ai") for _ in range(count)],
        "crypto": [generate_random_question("crypto") for _ in range(count)],
        "fraud_detection": [generate_random_question("fraud_detection") for _ in range(count)]
    }
    return questions

# Number of questions to generate per topic
question_count_per_topic = 500

# Generate questions and save to a JSON file
if __name__ == "__main__":
    questions_by_topic = generate_questions_per_topic(question_count_per_topic)
    with open("random_questions.json", "w") as f:
        json.dump(questions_by_topic, f, indent=2)
    print(f"{question_count_per_topic} random questions per topic have been saved in random_questions.json")
