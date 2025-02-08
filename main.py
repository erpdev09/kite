import json
import os
import random
import time
import requests
import sys
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Inisialisasi Colorama
init(autoreset=True)

# Konfigurasi agents dengan topik spesifik
agents = {
    "deployment_p5J9lz1Zxe7CYEoo0TZpRVay": {"name": "Professor 🧠", "topic": "ai"},
    "deployment_7sZJSiCqCNDy9bBHTEh7dwd9": {"name": "Crypto Buddy 💰", "topic": "crypto"},
    "deployment_SoFftlsf9z4fyA3QCHYkaANq": {"name": "Sherlock 🔎", "topic": "fraud_detection"}
}

# File untuk menyimpan data interaksi harian
interaction_log_file = "interaction_log.json"
random_questions_file = "random_questions.json"

# Fungsi untuk membaca data interaksi harian
def read_interaction_log():
    try:
        with open(interaction_log_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Fungsi untuk menyimpan data interaksi harian
def save_interaction_log(log_data):
    with open(interaction_log_file, "w") as f:
        json.dump(log_data, f, indent=2)

# Fungsi untuk mendapatkan tanggal hari ini dalam format YYYY-MM-DD (UTC)
def get_today_date_utc():
    now = datetime.utcnow()
    return now.strftime("%Y-%m-%d")

# Fungsi untuk memeriksa dan mereset interaksi harian jika hari sudah berganti (UTC)
def check_and_reset_daily_interactions(log_data, daily_limit, wallet):
    today_utc = get_today_date_utc()
    if log_data.get("date") != today_utc:
        print(Fore.YELLOW + "⚠️ Hari baru dimulai! Mereset interaksi harian untuk semua agent.")
        log_data["date"] = today_utc
        log_data["wallet"] = wallet
        log_data["dailyLimit"] = daily_limit
        log_data["interactions"] = {agent_id: 0 for agent_id in agents}
    return log_data

# Fungsi untuk membaca pertanyaan acak dari file random_questions.json berdasarkan topik
def get_random_questions_by_topic(file_path, topic, count):
    try:
        with open(file_path, "r") as f:
            questions = json.load(f)
        return random.sample(questions[topic], count)
    except Exception as e:
        print(Fore.RED + f"⚠️ Gagal membaca pertanyaan acak untuk topik {topic}: {e}")
        exit(1)

# Fungsi untuk mengirim pertanyaan ke agent AI
def send_question_to_agent(agent_id, question):
    url = f"https://{agent_id.lower().replace('_', '-')}.stag-vxzy.zettablock.com/main"
    payload = {"message": question, "stream": False}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]
    except Exception as e:
        print(Fore.RED + f"⚠️ Error saat mengirim pertanyaan ke agent {agent_id}: {e}")
        return None

# Fungsi untuk melaporkan penggunaan
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
        print(Fore.YELLOW + "✅ Data penggunaan berhasil dilaporkan!\n")
    except Exception as e:
        print(Fore.RED + f"⚠️ Gagal melaporkan penggunaan: {e}\n")

# Fungsi utama
def main():
    # Judul aplikasi
    print(Fore.CYAN + Style.BRIGHT + "🚀 Kite AI - Daily Interaction 🚀")
    print(Fore.CYAN + "----------------------------------------")
    print(Fore.MAGENTA + "Channel: https://t.me/ugdairdrop")
    print(Fore.MAGENTA + "Author: https://t.me/jodohsaya")
    print(Fore.CYAN + "----------------------------------------\n")

    # Periksa apakah file random_questions.json ada
    if not os.path.exists(random_questions_file):
        print(Fore.YELLOW + "⚠️ File random_questions.json tidak ditemukan. Membuat file baru...")
        try:
            # Jalankan file rand.py menggunakan interpreter Python yang sama
            os.system(f"{sys.executable} rand.py")
            print(Fore.GREEN + "✅ File random_questions.json berhasil dibuat.")
        except Exception as e:
            print(Fore.RED + f"⚠️ Gagal menjalankan rand.py: {e}")
            exit(1)

    # Baca data interaksi harian
    interaction_log = read_interaction_log()

    # Input wallet address hanya jika belum tersimpan di log
    wallet = interaction_log.get("wallet")
    if not wallet:
        wallet = input(Fore.YELLOW + "🔑 Masukkan wallet address Anda: ").strip()
        if not wallet.startswith("0x") or len(wallet) != 42:
            print(Fore.RED + "⚠️ Wallet address tidak valid! Harap masukkan wallet address yang benar.")
            exit(1)

    # Input batas harian hanya jika belum tersimpan di log
    daily_limit = interaction_log.get("dailyLimit", 20)
    if "dailyLimit" not in interaction_log:
        try:
            daily_limit = int(input(Fore.YELLOW + "🔢 Masukkan batas interaksi harian per agent: "))
            if daily_limit <= 0:
                raise ValueError
        except ValueError:
            print(Fore.YELLOW + "⚠️ Input tidak valid! Menggunakan batas default 20.")
            daily_limit = 20

    print(Fore.BLUE + f"\n📌 Wallet address: {wallet}")
    print(Fore.BLUE + f"📊 Batas interaksi harian per agent: {daily_limit}\n")

    # Loop kontinu untuk menjaga program tetap berjalan
    while True:
        # Perbarui log interaksi dengan batas harian (UTC)
        interaction_log = check_and_reset_daily_interactions(interaction_log, daily_limit, wallet)
        save_interaction_log(interaction_log)

        # Ambil pertanyaan acak dari file random_questions.json berdasarkan topik
        random_questions_by_topic = {}
        for agent_id, agent_info in agents.items():
            topic = agent_info["topic"]
            random_questions_by_topic[agent_id] = get_random_questions_by_topic(
                random_questions_file, topic, daily_limit
            )

        # Loop untuk setiap agent
        for agent_id, agent_info in agents.items():
            agent_name = agent_info["name"]
            topic = agent_info["topic"]
            print(Fore.MAGENTA + f"\n🤖 Menggunakan Agent: {agent_name}")
            print(Fore.CYAN + "----------------------------------------")

            # Periksa apakah batas harian sudah tercapai
            if interaction_log["interactions"][agent_id] >= daily_limit:
                print(Fore.YELLOW + f"⚠️ Batas interaksi harian untuk agent {agent_name} sudah tercapai ({daily_limit}x).")
                continue

            # Hitung sisa interaksi yang diizinkan
            remaining_interactions = daily_limit - interaction_log["interactions"][agent_id]

            for i in range(remaining_interactions):
                question = random_questions_by_topic[agent_id].pop()  # Ambil satu pertanyaan
                print(Fore.YELLOW + f"🔄 interaksi ke-{interaction_log['interactions'][agent_id] + 1}")
                print(Fore.CYAN + f"❓ Pertanyaan: {question}")

                response = send_question_to_agent(agent_id, question)
                print(Fore.GREEN + f"💡 Jawaban: {response.get('content', 'Tidak ada jawaban') if response else 'Tidak ada jawaban'}")

                # Laporkan penggunaan
                try:
                    report_usage(wallet.lower(), {
                        "agent_id": agent_id,
                        "question": question,
                        "response": response.get("content", "Tidak ada jawaban") if response else "Tidak ada jawaban"
                    })
                except Exception as e:
                    print(Fore.RED + f"⚠️ Gagal melaporkan penggunaan: {e}")

                # Update jumlah interaksi
                interaction_log["interactions"][agent_id] += 1
                save_interaction_log(interaction_log)

                # Tambahkan delay acak antara 5 hingga 15 detik
                delay = random.randint(5, 10)
                print(Fore.BLUE + f"⏳ Menunggu {delay} detik sebelum interaksi berikutnya...\n")
                time.sleep(delay)

            print(Fore.CYAN + "----------------------------------------")

        print(Fore.GREEN + "\n🎉 Sesi selesai! Menunggu hingga ±00:00 UTC untuk interaksi berikutnya...\n")

        # Hitung waktu hingga 00:00 UTC berikutnya
        now = datetime.utcnow()
        next_reset = (now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))
        time_until_reset = (next_reset - now).total_seconds()
        print(Fore.BLUE + f"⏰ Waktu hingga reset harian: {int(time_until_reset)} detik")

        # Tunggu hingga 00:00 UTC berikutnya
        time.sleep(time_until_reset)

if __name__ == "__main__":
    main()