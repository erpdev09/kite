import json
import random

# Daftar kata kunci berdasarkan kategori
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

# Frasa tambahan untuk variasi pertanyaan
extra_phrases = [
    "in the future", "impact on economy", "challenges faced", "advantages and disadvantages",
    "real-world applications", "security concerns", "scalability issues", "role in financial markets",
    "integration with IoT", "comparison with traditional systems", "future predictions",
    "ethical concerns", "adoption by enterprises", "potential for mass adoption"
]

# Starter untuk variasi struktur pertanyaan
starters = [
    "What is", "How does", "Why is", "Can you explain", "What are the benefits of",
    "How can", "What makes", "What are the features of", "How does", "What is the purpose of",
    "Why should we use", "What are the risks of", "What are the future prospects of",
    "Discuss the role of", "Analyze the impact of", "Explain the concept of"
]

# Konteks tambahan untuk variasi
contexts = ["in today's world", "for businesses", "for individuals", "in technology"]

# Fungsi untuk menghasilkan pertanyaan acak berdasarkan topik
def generate_random_question(topic):
    random_starter = random.choice(starters)
    random_keyword = random.choice(keywords[topic])
    random_extra = random.choice(extra_phrases)
    random_context = random.choice(contexts)
    return f"{random_starter} {random_keyword} {random_extra} {random_context}?"

# Fungsi untuk menghasilkan sejumlah pertanyaan acak per topik
def generate_questions_per_topic(count):
    questions = {
        "ai": [generate_random_question("ai") for _ in range(count)],
        "crypto": [generate_random_question("crypto") for _ in range(count)],
        "fraud_detection": [generate_random_question("fraud_detection") for _ in range(count)]
    }
    return questions

# Jumlah pertanyaan yang ingin dihasilkan per topik
question_count_per_topic = 500

# Hasilkan pertanyaan dan simpan ke file JSON
if __name__ == "__main__":
    questions_by_topic = generate_questions_per_topic(question_count_per_topic)
    with open("random_questions.json", "w") as f:
        json.dump(questions_by_topic, f, indent=2)
    print(f"{question_count_per_topic} pertanyaan acak per topik telah disimpan di random_questions.json")