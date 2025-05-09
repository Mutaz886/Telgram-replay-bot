from flask import Flask, request
import requests

app = Flask(__name__)

# توكن البوت
TOKEN = "8023491013:AAEAvenCGf04hoCIEijkNa54p2_Lz8hZQLA"
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ردود تلقائية
replies = {
    "مرحبا": "أهلاً وسهلاً! كيف أقدر أساعدك؟",
    "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته",
    "من انت": "أنا بوت تلقائي بسيط!",
    "كيفك": "الحمد لله، وانت؟"
}

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        data = request.get_json()
        if "message" in data and "text" in data["message"]:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"]["text"].strip().lower()
            if text in replies:
                reply = replies[text]
                requests.post(URL, json={"chat_id": chat_id, "text": reply})
        return "ok"
    return "Bot is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)