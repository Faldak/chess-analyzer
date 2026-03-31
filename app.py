from flask import Flask, render_template, request, jsonify
import chess
import chess.pgn
import chess.engine
import io
import os
import shutil
import logging
import traceback
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Configure logging - set to INFO to avoid rate limiting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Disable verbose chess engine logging
logging.getLogger('chess.engine').setLevel(logging.WARNING)

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

def classify_move_accuracy(player_move, best_move, eval_before, eval_after, is_white):
    """
    Классифицирует точность хода на основе сравнения с best move и оценок.
    
    Возвращает кортеж: (accuracy_score, classification_text)
    Где accuracy_score: 100, 75, 50, 25, 0
    """
    if not best_move:
        return 100, "Неизвестно"
    
    # Сравниваем ход с best move
    is_best_move = (player_move == best_move)
    
    # Вычисляем потерю оценки
    if eval_before is None or eval_after is None:
        return 100, "Неизвестно"
    
    eval_loss = eval_after - eval_before if is_white else eval_before - eval_after
    
    # Классификация по потере оценки
    if is_best_move or eval_loss >= 0:
        # Точный ход - best move или не ухудшил позицию
        return 100, "Точно"
    elif -50 <= eval_loss < 0:
        # Незначительная ошибка (до 50 пешек)
        return 75, "Хорошо"
    elif -200 <= eval_loss < -50:
        # Средняя ошибка (50-200 пешек)
        return 50, "Нормально"
    elif -500 <= eval_loss < -200:
        # Крупная ошибка (200-500 пешек)
        return 25, "Слабо"
    else:
        # Проигрышная ошибка (> 500 пешек)
        return 0, "Ошибка"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/annotate", methods=["POST"])
def annotate():
    """Analyze full game and return per-move annotations + accuracy scores."""
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
        top_moves = [[] for _ in range(len(moves_san) + 1)]  # Initialize as lists, not None
        white_accuracy = 0
        black_accuracy = 0

        if sf_path:
            board2 = game.board()
            white_accuracies = []
            black_accuracies = []
            
            with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
                # Evaluate initial position
                info = engine.analyse(board2, chess.engine.Limit(time=0.05), multipv=2)
                if isinstance(info, list):
                    scores[0] = info[0]["score"].white().score(mate_score=10000)
                    top_moves[0] = []
                    for i in info:
                        if "pv" in i and i["pv"]:
                            try:
                                top_moves[0].append(board2.san(chess.Move.from_uci(str(i["pv"][0]))))
                            except:
                                pass
                else:
                    scores[0] = info["score"].white().score(mate_score=10000)
                    top_moves[0] = []

                for i, mv in enumerate(move_objects):
                    # Get best move BEFORE this move
                    info_before = engine.analyse(board2, chess.engine.Limit(time=0.05), multipv=2)
                    best_move = None
                    if info_before:
                        if isinstance(info_before, list):
                            if info_before[0].get("pv"):
                                move_uci = info_before[0]["pv"][0]
                                try:
                                    best_move = board2.san(chess.Move.from_uci(str(move_uci)))
                                except:
                                    best_move = None
                        elif isinstance(info_before, dict) and "pv" in info_before:
                            if info_before["pv"]:
                                move_uci = info_before["pv"][0]
                                try:
                                    best_move = board2.san(chess.Move.from_uci(str(move_uci)))
                                except:
                                    best_move = None
                    
                    player_move = moves_san[i]
                    eval_before = scores[i]
                    
                    # Push move and get new evaluation
                    sac = is_sacrifice(board2, mv, scores[i], None)
                    board2.push(mv)

                    info = engine.analyse(board2, chess.engine.Limit(time=0.05), multipv=2)
                    if isinstance(info, list):
                        scores[i+1] = info[0]["score"].white().score(mate_score=10000)
                        top_moves[i+1] = []
                        for j in info:
                            if "pv" in j and j["pv"]:
                                try:
                                    top_moves[i+1].append(board2.san(chess.Move.from_uci(str(j["pv"][0]))))
                                except:
                                    pass
                    elif isinstance(info, dict):
                        scores[i+1] = info["score"].white().score(mate_score=10000)
                        top_moves[i+1] = []
                        if "pv" in info and info["pv"]:
                            try:
                                top_moves[i+1].append(board2.san(chess.Move.from_uci(str(info["pv"][0]))))
                            except:
                                pass
                    else:
                        scores[i+1] = None
                        top_moves[i+1] = []

                    eval_after = scores[i+1]
                    
                    # Старая аннотация
                    if scores[i] is not None and scores[i+1] is not None:
                        is_white_move = (i % 2 == 0)
                        diff = scores[i+1] - scores[i] if is_white_move else scores[i] - scores[i+1]
                        annotations[i] = get_annotation(diff, sac)
                    
                    # Новая классификация точности
                    is_white_move = (i % 2 == 0)
                    accuracy_score, classification = classify_move_accuracy(
                        player_move, best_move, eval_before, eval_after, is_white_move
                    )
                    
                    if is_white_move:
                        white_accuracies.append(accuracy_score)
                    else:
                        black_accuracies.append(accuracy_score)
            
            # Вычисляем среднюю точность для каждого игрока
            white_accuracy = round(sum(white_accuracies) / len(white_accuracies), 1) if white_accuracies else 0
            black_accuracy = round(sum(black_accuracies) / len(black_accuracies), 1) if black_accuracies else 0


        return jsonify({
            "moves": moves_san,
            "white": white,
            "black": black,
            "result": result,
            "annotations": annotations,
            "scores": scores,
            "top_moves": top_moves,
            "white_accuracy": white_accuracy,
            "black_accuracy": black_accuracy
        })

    except Exception as e:
        logger.error(f"Error in /annotate: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

# Serve favicon
@app.route("/favicon.ico")
def favicon():
    return "", 204  # Return 204 No Content for favicon

@app.route("/analyze_move", methods=["POST"])
def analyze_move():
    data = request.get_json()
    pgn_text = data.get("pgn", "").strip()
    move_index = data.get("move_index", None)
    custom_fen = data.get("fen", None)
    custom_move = data.get("move", None)
    language = data.get("language", "ru")  # языковой параметр

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        sf_path = get_sf()

        def get_sf_data(board, move_obj=None, engine=None):
            """Получает данные Stockfish для позиции и хода."""
            info_before = engine.analyse(board, chess.engine.Limit(time=0.3), multipv=3)
            score_before = info_before[0]["score"].white().score(mate_score=10000)

            top_moves = []
            for entry in info_before:
                if "pv" in entry and entry["pv"]:
                    top_moves.append({
                        "san": board.san(entry["pv"][0]),
                        "score": entry["score"].white().score(mate_score=10000)
                    })

            score_after = None
            if move_obj:
                board_after = board.copy()
                board_after.push(move_obj)
                info_after = engine.analyse(board_after, chess.engine.Limit(time=0.3))
                score_after = (info_after if not isinstance(info_after, list) else info_after[0])["score"].white().score(mate_score=10000)

            return score_before, score_after, top_moves

        # ── Режим исследования ──
        if custom_fen:
            board = chess.Board(custom_fen)
            is_white = board.turn == chess.WHITE
            color_name = "Белые" if is_white else "Чёрные"

            sb, sa, top_moves = None, None, []
            if sf_path:
                with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
                    move_obj = None
                    if custom_move:
                        try:
                            move_obj = board.parse_san(custom_move)
                        except Exception:
                            pass
                    sb, sa, top_moves = get_sf_data(board, move_obj, engine)

            top1 = top_moves[0]["san"] if len(top_moves) > 0 else "?"
            top2 = top_moves[1]["san"] if len(top_moves) > 1 else "?"
            top3 = top_moves[2]["san"] if len(top_moves) > 2 else "?"

            sb_fmt = f"{sb/100:+.2f}" if sb is not None else "?"
            sa_fmt = f"{sa/100:+.2f}" if sa is not None else "?"
            diff = None
            if sb is not None and sa is not None:
                diff = (sa - sb) if is_white else (sb - sa)
            diff_fmt = f"{diff:+d} сантипешек" if diff is not None else "?"

            if custom_move:
                prompt = f"""Ты опытный шахматный тренер. Игрок сделал ход и хочет понять его качество.

Позиция (FEN): {custom_fen}
Ход: {custom_move} ({color_name})

=== Данные Stockfish ===
Оценка ДО хода: {sb_fmt}
Оценка ПОСЛЕ хода: {sa_fmt}
Изменение оценки: {diff_fmt}
Лучший ход: {top1}
Второй лучший: {top2}
Третий лучший: {top3}

Дай полный разбор по разделам:

**🎯 Идея хода {custom_move}:**
Объясни что делает этот ход 2 предложениями — атака, защита, развитие фигуры, захват пространства, тактика?

**📊 Качество хода:**
На основе изменения оценки Stockfish определи категорию (отличный ход / хороший / неточность / ошибка / грубая ошибка) и объясни почему 1-2 предложениями.

**♟ Тактика и план:**
Какие угрозы создаёт или снимает этот ход? Какой план он открывает или закрывает? объясни 1 предложением.

**⚡ Лучшая альтернатива:**
Объясни почему {top1} был бы {'лучше' if custom_move != top1 else 'тоже хорош'} — какую конкретную идею он реализует? объясни 2 предложением.

**💡 Урок:**
Один практический совет — что нужно помнить в похожих позициях? объясни 2 предложением."""

            else:
                prompt = f"""Ты опытный шахматный тренер. Проанализируй позицию очень точно для игрока.

Позиция (FEN): {custom_fen}
Очередь хода: {color_name}

=== Данные Stockfish ===
Оценка позиции: {sb_fmt}
Лучший ход: {top1}
Второй лучший: {top2}
Третий лучший: {top3}

Дай полный разбор:

**📍 Оценка позиции:**
Кто стоит лучше, почему — материал, король, пешечная структура, активность фигур? объясни 2 предложением.

**🎯 Лучший план для {color_name}:**
Объясни идею хода {top1} — что он даёт, какую угрозу создаёт или проблему решает? объясни 1 предложением.

**♟ Альтернативный план:**
Коротко объясни идею {top2}.

**⚠️ Чего избегать:**
Какие ходы были бы ошибкой и почему?объясни 1 предложением"""

        # ── Режим просмотра партии ──
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
                context_before = " ".join(moves_san[max(0, move_index-4):move_index])
                context_after = " ".join(moves_san[move_index+1:move_index+3])

                # Восстанавливаем позицию ДО хода
                board2 = game.board()
                for i, mv in enumerate(move_objects):
                    if i == move_index:
                        break
                    board2.push(mv)
                fen_before = board2.fen()

                sb, sa, top_moves = None, None, []
                if sf_path:
                    with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
                        sb, sa, top_moves = get_sf_data(board2, move_objects[move_index], engine)

                top1 = top_moves[0]["san"] if len(top_moves) > 0 else "?"
                top2 = top_moves[1]["san"] if len(top_moves) > 1 else "?"
                top3 = top_moves[2]["san"] if len(top_moves) > 2 else "?"

                sb_fmt = f"{sb/100:+.2f}" if sb is not None else "?"
                sa_fmt = f"{sa/100:+.2f}" if sa is not None else "?"
                diff = None
                if sb is not None and sa is not None:
                    diff = (sa - sb) if color == "Белые" else (sb - sa)
                diff_fmt = f"{diff:+d} сантипешек" if diff is not None else "?"

                prompt = f"""Ты опытный шахматный тренер. Разбери конкретный ход из партии.

Партия: {white} vs {black} (результат: {result})
Ход {move_num}: {target} ({color})
Позиция до хода (FEN): {fen_before}
Ходы до: {context_before}
Ходы после: {context_after}

=== Данные Stockfish ===
Оценка ДО хода: {sb_fmt}
Оценка ПОСЛЕ хода: {sa_fmt}
Изменение оценки: {diff_fmt}
Лучший ход Stockfish: {top1}
Второй лучший: {top2}
Третий лучший: {top3}

Дай полный разбор по разделам:

**🎯 Идея хода {target}:**
Что делает этот ход — атака, защита, тактика, развитие, захват пространства?объясни кратко.

**📊 Качество хода:**
На основе изменения оценки определи категорию и объясни. Если это ошибка — почему игрок мог её допустить? объясни 1 предложением.

**♟ Тактика и план:**
Какие угрозы создаёт или нейтрализует этот ход? Как он влияет на дальнейшую игру (на это указывают ходы после)? объясни 2 предложением.

**⚡ Лучшая альтернатива:**
Объясни идею хода {top1} — что конкретно он давал лучшего? объясни 1 предложением.

**💡 Урок из этого момента:**
Один практический вывод для игрока — что нужно помнить в похожих позициях? объясни 1 предложением."""

            else:
                # Общий анализ партии
                moves_str = " ".join([f"{i//2+1}.{m}" if i%2==0 else m for i,m in enumerate(moves_san)])
                prompt = f"""Ты опытный шахматный тренер. Дай полный анализ партии.

Партия: {white} vs {black}, результат: {result}
Ходы: {moves_str}

**🏁 Характер партии:**
Открытая/закрытая, тактическая/позиционная, дебют? объясни 1 предложением.

**📍 Ключевой момент:**
Самый важный ход или позиция — где решилась партия? объясни 1 предложением.

**❌ Ошибки белых:**
Главные ошибки и почему они проигрышны. объясни 1 предложением.

**❌ Ошибки чёрных:**
Главные ошибки и почему они проигрышны. объясни 1 предложением.

**🏆 Вывод:**
Почему выиграл победитель — тактика, стратегия, ошибки соперника? объясни 1 предложением."""

        # Краткое резюме
        def get_quality_label(diff):
            if diff is None: return "Позиция"
            if diff <= -300: return "?? Грубая ошибка"
            if diff <= -100: return "? Ошибка"
            if diff <= -50:  return "?! Неточность"
            if diff >= 200:  return "!! Блестящий ход"
            if diff >= 50:   return "! Хороший ход"
            if diff >= 20:   return "!? Интересный ход"
            return "Нейтральный ход"

        # Вычисляем diff для резюме
        summary_diff = None
        summary_sb = None
        summary_sa = None
        if 'sb' in dir() and sb is not None and sa is not None:
            is_w = True
            if custom_move and custom_fen:
                board_tmp = chess.Board(custom_fen)
                is_w = board_tmp.turn == chess.WHITE
            elif move_index is not None:
                is_w = move_index % 2 == 0
            summary_diff = (sa - sb) if is_w else (sb - sa)
            summary_sb = sb
            summary_sa = sa

        quality = get_quality_label(summary_diff)
        sb_s = f"{summary_sb/100:+.2f}" if summary_sb is not None else "?"
        sa_s = f"{summary_sa/100:+.2f}" if summary_sa is not None else "?"
        summary = f"{sb_s} → {sa_s}  ·  {quality}"

        # добавляем языковую инструкцию в конец промпта
        lang_instruction = ""
        if language == "en":
            lang_instruction = "\n\nIMPORTANT: Answer ONLY in English."
        elif language == "kk":
            lang_instruction = "\n\nОЛІ: Жауапты ТЕК қазақша беріңіз."
        # иначе Russian по умолчанию
        
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt + lang_instruction}],
            model="llama-3.3-70b-versatile",
        )
        return jsonify({
            "analysis": chat.choices[0].message.content,
            "summary": summary
        })

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

@app.route("/trainer")
def trainer():
    return render_template("trainer.html")

@app.route("/trainer_move", methods=["POST"])
def trainer_move():
    """Stockfish делает ход за тренера + ИИ объясняет оба хода."""
    data = request.get_json()
    fen = data.get("fen", "")
    player_move = data.get("player_move", "")   # ход игрока (SAN) или "" если первый ход
    level = data.get("level", "medium")          # novice / medium / master
    move_number = data.get("move_number", 1)
    game_pgn = data.get("pgn", "")              # вся партия до этого момента
    language = data.get("language", "ru")        # языковой параметр

    # Skill levels для Stockfish
    skill_map = {"novice": 3, "medium": 10, "master": 18}
    depth_map  = {"novice": 5, "medium": 10, "master": 15}
    skill = skill_map.get(level, 10)
    depth = depth_map.get(level, 10)

    try:
        board = chess.Board(fen)
        sf_path = get_sf()
        if not sf_path:
            return jsonify({"error": "Stockfish не найден"}), 500

        # Оценка позиции до хода тренера
        with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
            engine.configure({"Skill Level": skill})

            # Оценка текущей позиции
            info_before = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=1)
            score_before = info_before[0]["score"].white().score(mate_score=10000) if isinstance(info_before, list) else info_before["score"].white().score(mate_score=10000)

            # Ход тренера
            result = engine.play(board, chess.engine.Limit(depth=depth))
            trainer_mv = result.move
            trainer_san = board.san(trainer_mv)

            board.push(trainer_mv)

            # Оценка после хода тренера
            info_after = engine.analyse(board, chess.engine.Limit(depth=8), multipv=1)
            score_after = info_after[0]["score"].white().score(mate_score=10000) if isinstance(info_after, list) else info_after["score"].white().score(mate_score=10000)

            # Проверка на мат/конец игры
            game_over = board.is_game_over()
            game_over_reason = ""
            if board.is_checkmate():
                game_over_reason = "checkmate"
            elif board.is_stalemate():
                game_over_reason = "stalemate"
            elif board.is_insufficient_material():
                game_over_reason = "insufficient"

        # Генерируем комментарий тренера через ИИ
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        level_names = {"novice": "начинающий", "medium": "средний", "master": "продвинутый"}
        level_name = level_names.get(level, "средний")

        player_block = ""
        if player_move:
            player_block = f"\nИгрок только что сделал ход: {player_move}"

        prompt = f"""Ты шахматный тренер, играешь против ученика ({level_name} уровень).
Ход номер {move_number} в партии.
FEN до твоего хода: {fen}
{player_block}
Твой ход: {trainer_san}
Оценка позиции до: {score_before/100 if score_before else 0:.2f}
Оценка после твоего хода: {score_after/100 if score_after else 0:.2f}

Напиши короткий живой комментарий (2-3 предложения) КАК НАСТОЯЩИЙ ТРЕНЕР во время игры.
Говори от первого лица ("Я делаю...", "Интересный ход...", "Хм...").
{'Прокомментируй ход ученика и объясни свой ответный ход.' if player_move else 'Объясни свой первый ход и намерения.'}
Будь живым, используй шахматные термины, иногда хвали или критикуй.
Не используй markdown, только обычный текст."""

        # добавляем языковую инструкцию в конец промпта
        lang_instruction = ""
        if language == "en":
            lang_instruction = "\n\nIMPORTANT: Answer ONLY in English."
        elif language == "kk":
            lang_instruction = "\n\nОЛІ: Жауапты ТЕК қазақша беріңіз."
        
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt + lang_instruction}],
            model="llama-3.3-70b-versatile",
            max_tokens=200,
        )
        comment = chat.choices[0].message.content.strip()

        return jsonify({
            "trainer_move": trainer_san,
            "trainer_move_uci": trainer_mv.uci(),
            "fen_after": board.fen(),
            "score_before": score_before,
            "score_after": score_after,
            "comment": comment,
            "game_over": game_over,
            "game_over_reason": game_over_reason,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/trainer_draw", methods=["POST"])
def trainer_draw():
    """Проверяет — примет ли тренер ничью (если после 20 ходов позиция ничейная)."""
    data = request.get_json()
    fen = data.get("fen", "")
    move_number = data.get("move_number", 0)

    try:
        if move_number < 20:
            return jsonify({"accept": False, "reason": "too_early",
                            "message": "Партия только началась, рано говорить о ничьей!"})

        board = chess.Board(fen)
        sf_path = get_sf()
        if not sf_path:
            return jsonify({"accept": False})

        with chess.engine.SimpleEngine.popen_uci(sf_path) as engine:
            info = engine.analyse(board, chess.engine.Limit(time=0.3))
            score = info["score"].white().score(mate_score=10000) if not isinstance(info, list) else info[0]["score"].white().score(mate_score=10000)

        # Принимаем ничью если оценка в диапазоне ±80 сантипешек
        accept = score is not None and abs(score) <= 80

        if accept:
            message = "Позиция действительно равна... Хорошо, принимаю ничью. Хорошая партия!"
        else:
            advantage = "у меня" if score > 0 else "у тебя"
            message = f"Нет, я не принимаю ничью — преимущество сейчас {advantage}. Играем дальше!"

        return jsonify({"accept": accept, "score": score, "message": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/trainer_pgn", methods=["POST"])
def trainer_pgn():
    """Генерирует PGN сыгранной партии с тренером."""
    data = request.get_json()
    moves = data.get("moves", [])      # список SAN ходов
    player_color = data.get("player_color", "white")
    level = data.get("level", "medium")
    result = data.get("result", "*")

    try:
        game = chess.pgn.Game()
        game.headers["Event"] = "Игра с тренером Chess Analyzer"
        game.headers["White"] = "Игрок" if player_color == "white" else f"Тренер ({level})"
        game.headers["Black"] = f"Тренер ({level})" if player_color == "white" else "Игрок"
        game.headers["Result"] = result

        node = game
        board = chess.Board()
        for san in moves:
            try:
                mv = board.parse_san(san)
                node = node.add_variation(mv)
                board.push(mv)
            except Exception:
                break

        pgn_str = str(game)
        return jsonify({"pgn": pgn_str})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)