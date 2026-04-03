// translations.js — ru / en / kk  |  index + trainer pages
const translations = {

  // ════════════════════════════════════════════════════════
  //  РУССКИЙ
  // ════════════════════════════════════════════════════════
  ru: {
    ui: {
      // index.html
      siteTitle:      "Шахматный Анализатор",
      trainer:        "🎓 Тренер",
      badge:          "AI + STOCKFISH",
      pgnTitle:       "Партия PGN",
      pgnLabel:       "// Вставь PGN партии",
      pgnPlaceholder: "1. e4 e5 2. Nf3 Nc6...",
      loadBtn:        "♟ Загрузить и анализировать",
      loadingBtn:     "⏳ Анализируем...",
      aiTitle:        "Анализ ИИ",
      loadGame:       "Загрузи партию",
      explainBtn:     "🔍 Объяснить ход / позицию",
      modeReview:     "Просмотр партии",
      modeExplore:    "Исследование",
      exploreBanner:  "Режим исследования — перетаскивай фигуры для анализа",
      evalChart:      "График оценки",
      evalChartHint:  "кликни → перейти к ходу",
      movesTitle:     "Ходы",
      engineTitle:    "Движок",
      cancelPreview:  "✕ Отменить предпросмотр",
      analyzing:      "Анализируем...",
      scoreBefore:    "ДО",
      scoreAfter:     "ПОСЛЕ",
      scoreDelta:     "ИЗМЕНЕНИЕ",
      moveEval:       "Оценка хода",
      readMore:       "Подробнее ▾",
      collapse:       "Свернуть ▴",
      mPgnTitle:      "PGN",
      mLoadBtn:       "♟ Загрузить",
      mLoadingBtn:    "⏳ Анализ...",
      tabMoves:       "Ходы",
      tabEngine:      "Движок",
      tabAI:          "ИИ",
      mAnalyzeBtn:    "🔍 Объяснить позицию",
      chartTitle:     "График",
      pasteError:     "Вставь PGN",
      language:       "Язык",
    },

    trainer: {
      // Заголовок страницы
      pageTitle:       "Chess Trainer — Игра с тренером",
      // Header
      siteTitle:       "Chess Trainer",
      siteSubtitle:    "Игра с ИИ тренером + Stockfish",
      backBtn:         "← Анализатор",
      // Setup screen
      setupTitle:      "⚙️ Новая партия",
      setupColorLabel: "Играю",
      colorWhite:      "Белые",
      colorBlack:      "Чёрные",
      colorRandom:     "Случайно",
      setupLevelLabel: "Уровень",
      levelNovice:     "Новичок",
      levelNoviceDesc: "Skill 3",
      levelMedium:     "Средний",
      levelMediumDesc: "Skill 10",
      levelMaster:     "Мастер",
      levelMasterDesc: "Skill 18",
      startBtn:        "🎮 Начать партию",
      // Trainer panel
      trainerName:     "Тренер",
      // Player bars
      thinking:        "думает...",
      // Controls
      offerDraw:       "🤝 Предложить ничью",
      resign:          "🏳️ Сдаться",
      // Game info panel
      statusTitle:     "Статус партии",
      statMoveLabel:   "ХОД",
      statScoreLabel:  "ОЦЕНКА",
      statTurnLabel:   "ОЧЕРЕДЬ ХОДА",
      turnWhite:       "Белые",
      turnBlack:       "Чёрные",
      // Moves panel
      movesTitle:      "Ходы партии",
      // After game panel
      afterTitle:      "После партии",
      getPGN:          "📋 Получить PGN",
      newGame:         "🔄 Ещё партию",
      // Eval toggle
      evalShow:        "👁 шкала",
      evalHidden:      "👁 скрыта",
      // Game over overlay
      gameoverTitle:   "Партия завершена",
      goGetPGN:        "📋 Получить PGN партии",
      goNewGame:       "🔄 Новая партия",
      // PGN modal
      pgnModalTitle:   "📋 PGN партии",
      pgnCopy:         "📋 Копировать",
      pgnClose:        "✕ Закрыть",
      // Toast
      pgnCopied:       "PGN скопирован!",
      // Chat messages
      greetWhite:      "Приветствую! Партия началась. Ты играешь белыми — твой первый ход.",
      greetBlack:      "Приветствую! Партия началась. Ты играешь чёрными — я делаю первый ход.",
      errorMove:       "Произошла ошибка при обработке хода.",
      resignMsg:       "Достойно признавать поражение. Разбери партию и сделай выводы!",
      // Gameover messages
      winTitle:        "Победа!",
      winSub:          "Отличная игра! Ты поставил мат тренеру.",
      winTrainerMsg:   "Поздравляю — ты победил! Отлично сыграл.",
      loseTitle:       "Поражение",
      loseSub:         "Тренер поставил тебе мат. Проанализируй партию!",
      loseTrainerMsg:  "Мат! Хорошая попытка — разбери партию.",
      drawTitle:       "Ничья",
      drawSub:         "Партия закончилась вничью.",
      resignTitle:     "Вы сдались",
      resignSub:       "Не расстраивайся — проанализируй партию!",
      // Footer
      footer:          "chess-trainer · stockfish + groq + chessboard.js",
    },

    chess: {
      white: "Белые",
      black: "Чёрные",
      move:  "Ход",
      check: "Шах",
      mate:  "Мат",
    },

    ai: {
      thinking:   "ИИ думает...",
      suggestion: "Совет ИИ",
      systemPrompt: `Ты — опытный шахматный тренер и аналитик. Анализируй шахматные позиции чётко и полезно.
При анализе конкретного хода:
1. Оцени качество хода (отличный/хороший/неточность/ошибка/зевок)
2. Объясни главную идею или проблему хода
3. Укажи лучшую альтернативу, если ход неоптимален
4. Кратко опиши стратегические/тактические последствия
5. Дай конкретный совет игроку

При анализе позиции без конкретного хода:
1. Оцени позицию (+/= для белых, =/+ для чёрных и т.д.)
2. Определи ключевые темы (атака, защита, структура пешек, активность фигур)
3. Предложи план для стороны, чья очередь ходить
4. Укажи критические поля или слабости

Пиши живо, как настоящий тренер. Используй шахматную терминологию. Отвечай на русском языке.`,

      trainerSystemPrompt: `Ты — живой шахматный тренер. Ты только что сделал ход в партии против ученика.
Дай короткий, живой комментарий (1-2 предложения) о своём ходе или позиции.
Иногда давай совет, иногда подбадривай, иногда предупреждай об угрозе.
Говори от первого лица, как настоящий тренер. Отвечай на русском языке.`,
    },
  },

  // ════════════════════════════════════════════════════════
  //  ENGLISH
  // ════════════════════════════════════════════════════════
  en: {
    ui: {
      siteTitle:      "Chess Analyzer",
      trainer:        "🎓 Trainer",
      badge:          "AI + STOCKFISH",
      pgnTitle:       "Game PGN",
      pgnLabel:       "// Paste game PGN",
      pgnPlaceholder: "1. e4 e5 2. Nf3 Nc6...",
      loadBtn:        "♟ Load & Analyze",
      loadingBtn:     "⏳ Analyzing...",
      aiTitle:        "AI Analysis",
      loadGame:       "Load a game",
      explainBtn:     "🔍 Explain move / position",
      modeReview:     "Game review",
      modeExplore:    "Exploration",
      exploreBanner:  "Exploration mode — drag pieces to analyze",
      evalChart:      "Eval chart",
      evalChartHint:  "click → jump to move",
      movesTitle:     "Moves",
      engineTitle:    "Engine",
      cancelPreview:  "✕ Cancel preview",
      analyzing:      "Analyzing...",
      scoreBefore:    "BEFORE",
      scoreAfter:     "AFTER",
      scoreDelta:     "CHANGE",
      moveEval:       "Move evaluation",
      readMore:       "Read more ▾",
      collapse:       "Collapse ▴",
      mPgnTitle:      "PGN",
      mLoadBtn:       "♟ Load",
      mLoadingBtn:    "⏳ Analyzing...",
      tabMoves:       "Moves",
      tabEngine:      "Engine",
      tabAI:          "AI",
      mAnalyzeBtn:    "🔍 Explain position",
      chartTitle:     "Chart",
      pasteError:     "Paste a PGN first",
      language:       "Language",
    },

    trainer: {
      pageTitle:       "Chess Trainer — Play with a Coach",
      siteTitle:       "Chess Trainer",
      siteSubtitle:    "Play vs AI Trainer + Stockfish",
      backBtn:         "← Analyzer",
      setupTitle:      "⚙️ New Game",
      setupColorLabel: "I play as",
      colorWhite:      "White",
      colorBlack:      "Black",
      colorRandom:     "Random",
      setupLevelLabel: "Level",
      levelNovice:     "Beginner",
      levelNoviceDesc: "Skill 3",
      levelMedium:     "Intermediate",
      levelMediumDesc: "Skill 10",
      levelMaster:     "Master",
      levelMasterDesc: "Skill 18",
      startBtn:        "🎮 Start Game",
      trainerName:     "Trainer",
      thinking:        "thinking...",
      offerDraw:       "🤝 Offer Draw",
      resign:          "🏳️ Resign",
      statusTitle:     "Game Status",
      statMoveLabel:   "MOVE",
      statScoreLabel:  "SCORE",
      statTurnLabel:   "TO MOVE",
      turnWhite:       "White",
      turnBlack:       "Black",
      movesTitle:      "Move List",
      afterTitle:      "After the game",
      getPGN:          "📋 Get PGN",
      newGame:         "🔄 New Game",
      evalShow:        "👁 eval",
      evalHidden:      "👁 hidden",
      gameoverTitle:   "Game Over",
      goGetPGN:        "📋 Get Game PGN",
      goNewGame:       "🔄 New Game",
      pgnModalTitle:   "📋 Game PGN",
      pgnCopy:         "📋 Copy",
      pgnClose:        "✕ Close",
      pgnCopied:       "PGN copied!",
      greetWhite:      "Welcome! The game has started. You play White — make your first move.",
      greetBlack:      "Welcome! The game has started. You play Black — I'll go first.",
      errorMove:       "An error occurred while processing the move.",
      resignMsg:       "It takes courage to resign. Study the game and learn from it!",
      winTitle:        "Victory!",
      winSub:          "Great game! You checkmated the trainer.",
      winTrainerMsg:   "Congratulations — you won! Well played.",
      loseTitle:       "Defeat",
      loseSub:         "The trainer checkmated you. Analyze the game!",
      loseTrainerMsg:  "Checkmate! Good try — review the game.",
      drawTitle:       "Draw",
      drawSub:         "The game ended in a draw.",
      resignTitle:     "You Resigned",
      resignSub:       "Don't worry — analyze the game!",
      footer:          "chess-trainer · stockfish + groq + chessboard.js",
    },

    chess: {
      white: "White",
      black: "Black",
      move:  "Move",
      check: "Check",
      mate:  "Mate",
    },

    ai: {
      thinking:   "AI is thinking...",
      suggestion: "AI Suggestion",
      systemPrompt: `You are an experienced chess coach and analyst. Analyze chess positions clearly and helpfully.
When analyzing a specific move:
1. Evaluate the move quality (brilliant/good/inaccuracy/mistake/blunder)
2. Explain the main idea or problem with the move
3. Suggest the best alternative if the move is suboptimal
4. Briefly describe the strategic/tactical consequences
5. Give actionable advice to the player

When analyzing a position without a specific move:
1. Evaluate the position (+/= for White, =/+ for Black, etc.)
2. Identify key themes (attack, defense, pawn structure, piece activity)
3. Suggest a plan for the side to move
4. Highlight critical squares or weaknesses

Write vividly, like a real coach. Use chess terminology. Always respond in English.`,

      trainerSystemPrompt: `You are a live chess trainer. You just made a move against your student.
Give a short, lively comment (1-2 sentences) about your move or the position.
Sometimes give advice, sometimes encourage, sometimes warn about a threat.
Speak in first person, like a real coach. Always respond in English.`,
    },
  },

  // ════════════════════════════════════════════════════════
  //  ҚАЗАҚША
  // ════════════════════════════════════════════════════════
  kk: {
    ui: {
      siteTitle:      "Шахмат Анализаторы",
      trainer:        "🎓 Жаттықтырушы",
      badge:          "AI + STOCKFISH",
      pgnTitle:       "Ойын PGN",
      pgnLabel:       "// PGN қойыңыз",
      pgnPlaceholder: "1. e4 e5 2. Nf3 Nc6...",
      loadBtn:        "♟ Жүктеу және талдау",
      loadingBtn:     "⏳ Талдануда...",
      aiTitle:        "ЖИ талдауы",
      loadGame:       "Ойын жүктеңіз",
      explainBtn:     "🔍 Жүрісті / позицияны түсіндіру",
      modeReview:     "Ойынды қарау",
      modeExplore:    "Зерттеу",
      exploreBanner:  "Зерттеу режимі — талдау үшін фигураларды жылжытыңыз",
      evalChart:      "Баға графигі",
      evalChartHint:  "басу → жүріске өту",
      movesTitle:     "Жүрістер",
      engineTitle:    "Қозғалтқыш",
      cancelPreview:  "✕ Алдын ала қараудан бас тарту",
      analyzing:      "Талдануда...",
      scoreBefore:    "ДЕЙІН",
      scoreAfter:     "КЕЙІН",
      scoreDelta:     "ӨЗГЕРІС",
      moveEval:       "Жүріс бағасы",
      readMore:       "Толығырақ ▾",
      collapse:       "Жию ▴",
      mPgnTitle:      "PGN",
      mLoadBtn:       "♟ Жүктеу",
      mLoadingBtn:    "⏳ Талдау...",
      tabMoves:       "Жүрістер",
      tabEngine:      "Қозғалтқыш",
      tabAI:          "ЖИ",
      mAnalyzeBtn:    "🔍 Позицияны түсіндіру",
      chartTitle:     "График",
      pasteError:     "PGN қойыңыз",
      language:       "Тіл",
    },

    trainer: {
      pageTitle:       "Chess Trainer — Жаттықтырушымен ойын",
      siteTitle:       "Chess Trainer",
      siteSubtitle:    "ЖИ жаттықтырушымен ойын + Stockfish",
      backBtn:         "← Анализатор",
      setupTitle:      "⚙️ Жаңа ойын",
      setupColorLabel: "Ойнаймын",
      colorWhite:      "Ақ",
      colorBlack:      "Қара",
      colorRandom:     "Кездейсоқ",
      setupLevelLabel: "Деңгей",
      levelNovice:     "Жаңадан бастаушы",
      levelNoviceDesc: "Skill 3",
      levelMedium:     "Орташа",
      levelMediumDesc: "Skill 10",
      levelMaster:     "Шебер",
      levelMasterDesc: "Skill 18",
      startBtn:        "🎮 Ойынды бастау",
      trainerName:     "Жаттықтырушы",
      thinking:        "ойлануда...",
      offerDraw:       "🤝 Тең ойын ұсыну",
      resign:          "🏳️ Бас тарту",
      statusTitle:     "Ойын мәртебесі",
      statMoveLabel:   "ЖҮРіС",
      statScoreLabel:  "БАҒА",
      statTurnLabel:   "ЖҮРУ КЕЗЕГІ",
      turnWhite:       "Ақ",
      turnBlack:       "Қара",
      movesTitle:      "Жүрістер тізімі",
      afterTitle:      "Ойыннан кейін",
      getPGN:          "📋 PGN алу",
      newGame:         "🔄 Тағы ойын",
      evalShow:        "👁 шкала",
      evalHidden:      "👁 жасырын",
      gameoverTitle:   "Ойын аяқталды",
      goGetPGN:        "📋 PGN алу",
      goNewGame:       "🔄 Жаңа ойын",
      pgnModalTitle:   "📋 Ойын PGN",
      pgnCopy:         "📋 Көшіру",
      pgnClose:        "✕ Жабу",
      pgnCopied:       "PGN көшірілді!",
      greetWhite:      "Сәлем! Ойын басталды. Сіз ақпен ойнайсыз — бірінші жүрісіңіз.",
      greetBlack:      "Сәлем! Ойын басталды. Сіз қарамен ойнайсыз — мен бірінші жүремін.",
      errorMove:       "Жүрісті өңдеу кезінде қате орын алды.",
      resignMsg:       "Жеңілісті мойындау — ер азаматтың ісі. Ойынды талдап, қорытынды жасаңыз!",
      winTitle:        "Жеңіс!",
      winSub:          "Тамаша ойын! Сіз жаттықтырушыға мат қойдыңыз.",
      winTrainerMsg:   "Құттықтаймын — жеңдіңіз! Тамаша ойнадыңыз.",
      loseTitle:       "Жеңіліс",
      loseSub:         "Жаттықтырушы сізге мат қойды. Ойынды талдаңыз!",
      loseTrainerMsg:  "Мат! Жақсы әрекет — ойынды қарап шығыңыз.",
      drawTitle:       "Тең ойын",
      drawSub:         "Ойын тең нәтижемен аяқталды.",
      resignTitle:     "Сіз бас тарттыңыз",
      resignSub:       "Ренжімеңіз — ойынды талдаңыз!",
      footer:          "chess-trainer · stockfish + groq + chessboard.js",
    },

    chess: {
      white: "Ақ",
      black: "Қара",
      move:  "Жүріс",
      check: "Шах",
      mate:  "Мат",
    },

    ai: {
      thinking:   "ЖИ ойлануда...",
      suggestion: "ЖИ ұсынысы",
      systemPrompt: `Сіз — тәжірибелі шахмат жаттықтырушысы және талдаушысысыз. Шахмат позицияларын нақты және пайдалы талдаңыз.
Нақты жүрісті талдаған кезде:
1. Жүріс сапасын бағалаңыз (тамаша/жақсы/дәлсіздік/қате/зевок)
2. Жүрістің негізгі идеясын немесе мәселесін түсіндіріңіз
3. Жүріс оңтайлы болмаса, ең жақсы балама ұсыныңыз
4. Стратегиялық/тактикалық салдарды қысқаша сипаттаңыз
5. Ойыншыға нақты кеңес беріңіз

Нақты жүріссіз позицияны талдаған кезде:
1. Позицияны бағалаңыз (+/= ақ үшін, =/+ қара үшін және т.б.)
2. Негізгі тақырыптарды анықтаңыз (шабуыл, қорғаныс, пешка құрылымы, фигуралар белсенділігі)
3. Жүру кезегіндегі тарап үшін жоспар ұсыныңыз
4. Маңызды алаңдарды немесе әлсіз жерлерді көрсетіңіз

Нақты жаттықтырушы сияқты жазыңыз. Қазақ тілінде жауап беріңіз.`,

      trainerSystemPrompt: `Сіз — тірі шахмат жаттықтырушысысыз. Жаңа ғана оқушыңызға қарсы жүріс жасадыңыз.
Жүрісіңіз немесе позиция туралы қысқа, тірі түсініктеме беріңіз (1-2 сөйлем).
Кейде кеңес беріңіз, кейде қолдаңыз, кейде қауіп туралы ескертіңіз.
Бірінші жақтан, нақты жаттықтырушы сияқты сөйлеңіз. Қазақ тілінде жауап беріңіз.`,
    },
  },
};

// ════════════════════════════════════════════════════════
//  УТИЛИТЫ — общие для обеих страниц
// ════════════════════════════════════════════════════════

/**
 * Получить перевод по ключу вида "namespace.key" или "key"
 * Пространства: ui, trainer, chess, ai
 */
function t(key, lang) {
  lang = lang || getCurrentLang();
  const keys = key.split('.');
  const resolve = (obj) => keys.reduce((v, k) => (v && k in v ? v[k] : undefined), obj);
  return resolve(translations[lang]) ?? resolve(translations['ru']) ?? key;
}

function getCurrentLang() {
  try { return localStorage.getItem('lang') || 'ru'; } catch { return 'ru'; }
}

function setLanguage(lang) {
  try { localStorage.setItem('lang', lang); } catch {}
  updateTranslations(lang);
  document.querySelectorAll('.lang-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.lang === lang)
  );
  // Уведомляем страницу об изменении языка (для trainer.html)
  document.dispatchEvent(new CustomEvent('langChanged', { detail: { lang } }));
}

/**
 * Обходит все элементы с data-key и data-key-placeholder и подставляет перевод.
 * Работает для обеих страниц: ищет ключи вида "ui.loadBtn", "trainer.startBtn" и т.д.
 */
function updateTranslations(lang) {
  document.querySelectorAll('[data-key]').forEach(el => {
    const key = el.getAttribute('data-key');
    const val = t(key, lang);
    if (val !== key) el.textContent = val;
  });
  document.querySelectorAll('[data-key-placeholder]').forEach(el => {
    const key = el.getAttribute('data-key-placeholder');
    const val = t(key, lang);
    if (val !== key) el.placeholder = val;
  });
  // Заголовок вкладки браузера
  const titleKey = document.body.dataset.titleKey;
  if (titleKey) document.title = t(titleKey, lang);
}

function initI18n() {
  const lang = getCurrentLang();
  updateTranslations(lang);
  document.querySelectorAll('.lang-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.lang === lang)
  );
}

function setupLanguageSwitcher() {
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
  });
}

// Глобальный экспорт
window.i18n = { t, getCurrentLang, setLanguage, updateTranslations, initI18n, setupLanguageSwitcher };
