from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
import json
from openai import OpenAI

app = Flask(__name__)
CORS(app)

API_KEY = ""  
client = OpenAI(api_key=API_KEY)


def get_mock():
    """نستخدمه لو فيه أي خطأ في OpenAI عشان ما يطيح الديمو."""
    return {
        "success": True,
        "analysis": {
            "type": "إشعار تحديث بيانات الهوية",
            "required_action": "تحديث الهوية عبر منصة أبشر أو مراجعة مكتب الأحوال المدنية",
            "deadline": "14 يوم",
            "next_step": "أبشر > الخدمات الإلكترونية > الأحوال المدنية > تحديث بيانات الهوية"
        }
    }


@app.route("/")
def home():
    # يعرض صفحة عدسة أبشر
    return render_template("index.html")


@app.route("/action")
def action_page():
    # صفحة تنفيذ الإجراء
    return render_template("action.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if "image" not in request.files:
            return jsonify(get_mock())

        img_bytes = request.files["image"].read()
        b64 = base64.b64encode(img_bytes).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
حلل هذا الإشعار الحكومي وأعد الاستجابة بصيغة JSON فقط، بدون أي نص خارجي.
أعد التحليل باللغة العربية الفصحى فقط. لا تستخدم اللغة الإنجليزية إطلاقًا في أي جزء من الإجابة.

استخدم هذا الهيكل:

{
  "success": true,
  "analysis": {
    "type": "...",
    "required_action": "...",
    "deadline": "...",
    "next_step": "..."
  }
}
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64}"
                            }
                        }
                    ]
                }
            ]
        )

        raw = response.choices[0].message.content.strip()
        clean = raw.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean)

        # نتأكد أن عندنا analysis
        if "analysis" not in parsed:
            return jsonify(get_mock())

        return jsonify(parsed)

    except Exception as e:
        print("ERR:", e)
        return jsonify(get_mock())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
