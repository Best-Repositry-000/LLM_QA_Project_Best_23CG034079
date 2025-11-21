from flask import Flask, render_template, request
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_groq(question):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        temperature=0.7
    )
    return response.choices[0].message["content"]


@app.route("/", methods=["GET", "POST"])
def home():
    user_question = ""
    llm_answer = ""

    if request.method == "POST":
        user_question = request.form.get("question")
        llm_answer = ask_groq(user_question)

    return render_template("index.html",
                           question=user_question,
                           answer=llm_answer)


if __name__ == "__main__":
    app.run(debug=True)
