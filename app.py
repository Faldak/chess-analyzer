from flask import Flask, render_template, request, jsonify
import chess
import chess.pgn
import chess.engine
import io
import os
import shutil
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def get_sf():
    sf = shutil.which("stockfish")
    if sf:
        return sf
    for p in ["/usr/local/bin/stockfish", "/usr/bin/stockfish", "/usr/games/stockfish"]:
        if os.path.exists(p):
            return p
    return None

def get_annotation(diff, is_sacrifice):
    """Return annotation symbol based on centipawn difference."""
    if diff <= -300:
        return "??"
    elif diff <= -100:
        return "?"
    elif diff <= -50:
        return "?!"
    elif is_sacrifice and diff >= 100:
        return "!!"
    elif diff >= 200:
        return "!!"
    elif diff >= 50:
        return "!"
    elif diff >= 20:
        return "!?"
    return ""

def is_sacrifice(board_before, move, score_before, score_after):
    """Check if move sacrifices material (gives up piece for positional/tactical gain)."""
    captured = board_before.piece_at(move.to_square)
    if captured is None:
        return False
    piece_values = {chess.PAWN: 100, chess.KNIGHT: 300, chess.BISHOP: 310,
                    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}
    captured_val = piece_values.get(captured.piece_type, 0)
    moving_piece = board_before.piece_at(move.from_square)
    moving_val = piece_values.get(moving_piece.piece_type if moving_piece else chess.PAWN, 0)
    return moving_val > captured_val and score_after is not None and score_before is not None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/annotate", methods=["POST"])
def annotate():
    """Analyze full game and return per-move annotations + scores."""
    data = request.get_json()
    pgn_text = data.get("pgn", "").strip()
    if not pgn_text:
        return jsonify({"error": "Вставь PGN"}), 400
    try:
        game = chess.pgn.read_game(io.StringIO(pgn_text))
        if not game:
            return jsonify({"error": "Неверный PGN"}), 400

        moves_san = []
        board = game.board()
        move_objects = list(game.mainline_moves())
        for mv in move_objects:
            moves_san.append(board.san(mv))
            board.push(mv)

        white = game.headers.get("White", "Белые")
        black = game.headers.get("Black", "Чёрные")
        result = game.headers.get("Result", "*")

        sf_path = get_sf()
        annotations = [""] * len(moves_san)
        scores = [None] * (len(moves_san) + 1)
        top_moves = [None] * (len(moves_san) + 1)

        if sf_path:
            board2 = game.board()
            with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
                # Evaluate initial position
                info = engine.analyse(board2, chess.engine.Limit(time=0.15), multipv=2)
                if isinstance(info, list):
                    scores[0] = info[0]["score"].white().score(mate_score=10000)
                    top_moves[0] = [board2.san(i["pv"][0]) for i in info if "pv" in i and i["pv"]]
                else:
                    scores[0] = info["score"].white().score(mate_score=10000)

                for i, mv in enumerate(move_objects):
                    sac = is_sacrifice(board2, mv, scores[i], None)
                    board2.push(mv)

                    info = engine.analyse(board2, chess.engine.Limit(time=0.15), multipv=2)
                    if isinstance(info, list):
                        scores[i+1] = info[0]["score"].white().score(mate_score=10000)
                        top_moves[i+1] = [board2.san(j["pv"][0]) for j in info if "pv" in j and j["pv"]]
                    else:
                        scores[i+1] = info["score"].white().score(mate_score=10000)
                        top_moves[i+1] = []

                    if scores[i] is not None and scores[i+1] is not None:
                        is_white = (i % 2 == 0)
                        diff = scores[i+1] - scores[i] if is_white else scores[i] - scores[i+1]
                        annotations[i] = get_annotation(diff, sac)

        return jsonify({
            "moves": moves_san,
            "white": white,
            "black": black,
            "result": result,
            "annotations": annotations,
            "scores": scores,
            "top_moves": top_moves
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze_move", methods=["POST"])
def analyze_move():
    """Get AI explanation for a specific move or position."""
    data = request.get_json()
    pgn_text = data.get("pgn", "").strip()
    move_index = data.get("move_index", None)
    custom_fen = data.get("fen", None)
    custom_move = data.get("move", None)

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        if custom_fen and custom_move:
            # Analyzing a user's custom move in exploration mode
            board = chess.Board(custom_fen)
            sf_path = get_sf()
            stockfish_info = ""
            if sf_path:
                with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
                    info_before = engine.analyse(board, chess.engine.Limit(time=0.3), multipv=2)
                    score_before = info_before[0]["score"].white().score(mate_score=10000) if isinstance(info_before, list) else info_before["score"].white().score(mate_score=10000)
                    top1 = board.san(info_before[0]["pv"][0]) if isinstance(info_before, list) and info_before[0].get("pv") else "?"
                    top2 = board.san(info_before[1]["pv"][0]) if isinstance(info_before, list) and len(info_before) > 1 and info_before[1].get("pv") else "?"

                    try:
                        mv = board.parse_san(custom_move)
                        board_after = board.copy()
                        board_after.push(mv)
                        info_after = engine.analyse(board_after, chess.engine.Limit(time=0.3))
                        score_after = info_after["score"].white().score(mate_score=10000) if not isinstance(info_after, list) else info_after[0]["score"].white().score(mate_score=10000)
                        diff = score_after - score_before
                        stockfish_info = f"Оценка до: {score_before}, после: {score_after}, изменение: {diff:+d}\nЛучший ход: {top1}\nАльтернатива: {top2}"
                    except:
                        stockfish_info = f"Лучший ход: {top1}, альтернатива: {top2}"

            is_white = board.turn == chess.WHITE
            prompt = f"""Ты шахматный тренер. Игрок сделал ход {custom_move} в позиции FEN: {custom_fen}
{stockfish_info}

Объясни коротко (2-3 предложения):
1. Что за ход и идея
2. Хороший или плохой — на основе оценки Stockfish
3. Если плохой — что лучше было сыграть"""

        else:
            game = chess.pgn.read_game(io.StringIO(pgn_text))
            moves_san = []
            board = game.board()
            move_objects = list(game.mainline_moves())
            for mv in move_objects:
                moves_san.append(board.san(mv))
                board.push(mv)

            white = game.headers.get("White", "Белые")
            black = game.headers.get("Black", "Чёрные")
            result = game.headers.get("Result", "*")

            if move_index is not None and 0 <= move_index < len(moves_san):
                target = moves_san[move_index]
                color = "Белые" if move_index % 2 == 0 else "Чёрные"
                move_num = move_index // 2 + 1
                context = moves_san[max(0, move_index-3):move_index+2]

                board2 = game.board()
                for i, mv in enumerate(move_objects):
                    if i == move_index:
                        break
                    board2.push(mv)
                fen = board2.fen()

                sf_path = get_sf()
                sf_info = ""
                if sf_path:
                    with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
                        info_b = engine.analyse(board2, chess.engine.Limit(time=0.3), multipv=2)
                        sb = info_b[0]["score"].white().score(mate_score=10000) if isinstance(info_b, list) else info_b["score"].white().score(mate_score=10000)
                        top1 = board2.san(info_b[0]["pv"][0]) if isinstance(info_b, list) and info_b[0].get("pv") else "?"
                        top2 = board2.san(info_b[1]["pv"][0]) if isinstance(info_b, list) and len(info_b) > 1 and info_b[1].get("pv") else "?"
                        try:
                            mv_obj = move_objects[move_index]
                            b2 = board2.copy(); b2.push(mv_obj)
                            info_a = engine.analyse(b2, chess.engine.Limit(time=0.3))
                            sa = info_a["score"].white().score(mate_score=10000) if not isinstance(info_a, list) else info_a[0]["score"].white().score(mate_score=10000)
                            diff = sa - sb if color == "Белые" else sb - sa
                            sf_info = f"Оценка Stockfish: до={sb}, после={sa}, изменение={diff:+d}\nЛучший ход: {top1}, альтернатива: {top2}"
                        except:
                            sf_info = f"Лучший ход: {top1}, альтернатива: {top2}"

                prompt = f"""Ты шахматный тренер. Проанализируй ход {move_num}. {target} ({color}) из партии {white} vs {black}.
Позиция FEN: {fen}
Контекст: {" ".join(context)}
{sf_info}

Объясни (3-4 предложения):
1. Идея и смысл хода
2. Качество хода по Stockfish
3. Что лучше было сыграть если ход плохой"""
            else:
                moves_str = " ".join([f"{i//2+1}.{m}" if i%2==0 else m for i,m in enumerate(moves_san)])
                prompt = f"""Ты шахматный тренер. Общий анализ партии {white} vs {black} ({result}):
{moves_str}

Анализ (4-5 предложений): характер партии, ключевые моменты, ошибки, вывод."""

        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return jsonify({"analysis": chat.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze_position", methods=["POST"])
def analyze_position():
    """Get top 2 moves for a given FEN position."""
    data = request.get_json()
    fen = data.get("fen", "")
    try:
        board = chess.Board(fen)
        sf_path = get_sf()
        if not sf_path:
            return jsonify({"error": "Stockfish не найден"}), 500
        with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
            info = engine.analyse(board, chess.engine.Limit(time=0.5), multipv=2)
            result = []
            for entry in (info if isinstance(info, list) else [info]):
                if "pv" in entry and entry["pv"]:
                    score = entry["score"].white().score(mate_score=10000)
                    result.append({
                        "move": board.san(entry["pv"][0]),
                        "score": score
                    })
            return jsonify({"top_moves": result, "score": result[0]["score"] if result else 0})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
