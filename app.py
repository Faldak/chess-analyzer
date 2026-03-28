from flask import Flask, render_template, request, jsonify
import chess
import chess.pgn
import chess.engine
import io
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_stockfish_path():
    paths = [
        "/usr/bin/stockfish",
        "/usr/games/stockfish",
        "stockfish.exe",
        "stockfish",
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return "stockfish"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
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

            # Получаем позицию ДО хода
            board_before = game.board()
            for i, move in enumerate(game.mainline_moves()):
                if i == move_index:
                    break
                board_before.push(move)

            fen_before = board_before.fen()

            # Stockfish анализ
            stockfish_info = ""
            try:
                sf_path = get_stockfish_path()
                with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
                    # Оценка ДО хода
                    info_before = engine.analyse(board_before, chess.engine.Limit(time=0.3))
                    score_before = info_before["score"].white().score(mate_score=10000)

                    # Применяем ход
                    board_after = board_before.copy()
                    for mv in board_after.legal_moves:
                        if board_after.san(mv) == target_move.replace("+","").replace("#",""):
                            board_after.push(mv)
                            break
                    else:
                        # Попробуем через parse_san
                        try:
                            mv = board_before.parse_san(target_move)
                            board_after = board_before.copy()
                            board_after.push(mv)
                        except:
                            board_after = board_before.copy()

                    # Оценка ПОСЛЕ хода
                    info_after = engine.analyse(board_after, chess.engine.Limit(time=0.3))
                    score_after = info_after["score"].white().score(mate_score=10000)

                    # Лучший ход по мнению Stockfish
                    best_move_obj = info_before.get("pv", [None])[0]
                    best_move_san = board_before.san(best_move_obj) if best_move_obj else "неизвестен"

                    if score_before is not None and score_after is not None:
                        diff = score_after - score_before if color == "Белые" else score_before - score_after
                        if diff > 50:
                            quality = "отличный ход (+{} центипешек)".format(abs(diff))
                        elif diff > 0:
                            quality = "хороший ход (+{} центипешек)".format(abs(diff))
                        elif diff > -50:
                            quality = "нейтральный ход"
                        elif diff > -150:
                            quality = "неточность (-{} центипешек)".format(abs(diff))
                        elif diff > -300:
                            quality = "ошибка (-{} центипешек)".format(abs(diff))
                        else:
                            quality = "грубая ошибка (-{} центипешек)".format(abs(diff))

                        stockfish_info = f"""
Оценка Stockfish: {quality}
Оценка позиции до хода: {score_before} центипешек
Оценка позиции после хода: {score_after} центипешек
Лучший ход по Stockfish: {best_move_san}"""

            except Exception as sf_err:
                stockfish_info = f"(Stockfish недоступен: {sf_err})"

            prompt = f"""Ты шахматный тренер. Проанализируй ход {move_num}. {target_move} ({color}) из партии {white} vs {black}.

Позиция в формате FEN до хода: {fen_before}
{stockfish_info}

Объясни простым языком (3-5 предложений):
1. Что за ход и зачем он сделан
2. Хороший или плохой ход — основывайся на оценке Stockfish
3. Если плохой — что надо было сыграть вместо этого и почему"""

        else:
            # Общий анализ партии со Stockfish
            blunders = []
            try:
                sf_path = get_stockfish_path()
                with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
                    board_tmp = game.board()
                    prev_score = 0
                    for i, move in enumerate(game.mainline_moves()):
                        info = engine.analyse(board_tmp, chess.engine.Limit(time=0.2))
                        score = info["score"].white().score(mate_score=10000)
                        san = board_tmp.san(move)
                        board_tmp.push(move)

                        if score is not None and prev_score is not None:
                            diff = score - prev_score if i % 2 == 0 else prev_score - score
                            if diff < -200:
                                color_bl = "Белые" if i % 2 == 0 else "Чёрные"
                                blunders.append(f"Ход {i//2+1}. {san} ({color_bl}) — грубая ошибка")
                        prev_score = score

            except Exception as sf_err:
                blunders = [f"Stockfish недоступен: {sf_err}"]

            moves_str = " ".join([f"{i//2+1}.{m}" if i%2==0 else m for i,m in enumerate(moves)])
            blunders_str = "\n".join(blunders) if blunders else "Грубых ошибок не найдено"

            prompt = f"""Ты шахматный тренер. Дай общий анализ партии:
Белые: {white}
Чёрные: {black}
Результат: {result}
Ходы: {moves_str}

Грубые ошибки найденные Stockfish:
{blunders_str}

Напиши краткий анализ (5-7 предложений):
- Общий характер партии
- Ключевые моменты
- Разбор грубых ошибок из списка выше
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