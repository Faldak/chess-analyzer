from flask import Flask, render_template, request, jsonify
import chess.pgn
import io
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    pgn_text = data.get("pgn", "").strip()
    move_index = data.get("move_index", None)

    if not pgn_text:
        return jsonify({"error": "Вставь PGN партии"}), 400

    try:
        game = chess.pgn.read_game(io.StringIO(pgn_text))
        if game is None:
            return jsonify({"error": "Неверный формат PGN"}), 400

        moves = []
        board = game.board()
        for move in game.mainline_moves():
            san = board.san(move)
            board.push(move)
            moves.append(san)

        white = game.headers.get("White", "Белые")
        black = game.headers.get("Black", "Чёрные")
        result = game.headers.get("Result", "*")

        if move_index is not None and 0 <= move_index < len(moves):
            target_move = moves[move_index]
            color = "Белые" if move_index % 2 == 0 else "Чёрные"
            move_num = move_index // 2 + 1
            context_moves = moves[max(0, move_index-3):move_index+2]
            prompt = f"""Ты шахматный тренер. Проанализируй ход {move_num}. {target_move} ({color}) из партии {white} vs {black}.

Контекст партии (последние ходы): {" ".join(context_moves)}

Объясни простым языком (2-4 предложения):
1. Что за ход, зачем он сделан
2. Хороший или плохой ход и почему
3. Если плохой — как надо было лучше сыграть"""
        else:
            moves_str = " ".join([f"{i//2+1}.{m}" if i%2==0 else m for i,m in enumerate(moves)])
            prompt = f"""Ты шахматный тренер. Дай общий анализ партии:
Белые: {white}
Чёрные: {black}
Результат: {result}
Ходы: {moves_str}

Напиши краткий анализ (4-6 предложений):
- Общий характер партии
- Ключевые моменты
- Главные ошибки каждой стороны
- Чему можно научиться из этой партии"""

        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        analysis = chat.choices[0].message.content

        return jsonify({
            "moves": moves,
            "white": white,
            "black": black,
            "result": result,
            "analysis": analysis
        })

    except Exception as e:
        return jsonify({"error": f"Ошибка: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
