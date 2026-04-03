// translations.js — полные переводы ru / en / kk
const translations = {
  ru: {
    ui: {
      siteTitle:        "Шахматный Анализатор",
      trainer:          "🎓 Тренер",
      badge:            "AI + STOCKFISH",
      pgnTitle:         "Партия PGN",
      pgnLabel:         "// Вставь PGN партии",
      pgnPlaceholder:   "1. e4 e5 2. Nf3 Nc6...",
      loadBtn:          "♟ Загрузить и анализировать",
      loadingBtn:       "⏳ Анализируем...",
      aiTitle:          "Анализ ИИ",
      loadGame:         "Загрузи партию",
      explainBtn:       "🔍 Объяснить ход / позицию",
      modeReview:       "Просмотр партии",
      modeExplore:      "Исследование",
      exploreBanner:    "Режим исследования — перетаскивай фигуры для анализа",
      evalChart:        "График оценки",
      evalChartHint:    "кликни → перейти к ходу",
      movesTitle:       "Ходы",
      engineTitle:      "Движок",
      cancelPreview:    "✕ Отменить предпросмотр",
      analyzing:        "Анализируем...",
      scoreBefore:      "ДО",
      scoreAfter:       "ПОСЛЕ",
      scoreDelta:       "ИЗМЕНЕНИЕ",
      moveEval:         "Оценка хода",
      readMore:         "Подробнее ▾",
      collapse:         "Свернуть ▴",
      mPgnTitle:        "PGN",
      mLoadBtn:         "♟ Загрузить",
      mLoadingBtn:      "⏳ Анализ...",
      tabMoves:         "Ходы",
      tabEngine:        "Движок",
      tabAI:            "ИИ",
      mAnalyzeBtn:      "🔍 Объяснить позицию",
      chartTitle:       "График",
      pasteError:       "Вставь PGN",
      language:         "Язык",
    },
    chess: {
      white:  "Белые",
      black:  "Чёрные",
      move:   "Ход",
      check:  "Шах",
      mate:   "Мат",
    },
    ai: {
      thinking:   "ИИ думает...",
      suggestion: "Совет ИИ",
      // Системный промпт для анализа хода
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

Пиши живо, как настоящий тренер. Используй шахматную терминологию. Отвечай на том языке, на котором задан вопрос.`,
    },
  },

  en: {
    ui: {
      siteTitle:        "Chess Analyzer",
      trainer:          "🎓 Trainer",
      badge:            "AI + STOCKFISH",
      pgnTitle:         "Game PGN",
      pgnLabel:         "// Paste game PGN",
      pgnPlaceholder:   "1. e4 e5 2. Nf3 Nc6...",
      loadBtn:          "♟ Load & Analyze",
      loadingBtn:       "⏳ Analyzing...",
      aiTitle:          "AI Analysis",
      loadGame:         "Load a game",
      explainBtn:       "🔍 Explain move / position",
      modeReview:       "Game review",
      modeExplore:      "Exploration",
      exploreBanner:    "Exploration mode — drag pieces to analyze",
      evalChart:        "Eval chart",
      evalChartHint:    "click → jump to move",
      movesTitle:       "Moves",
      engineTitle:      "Engine",
      cancelPreview:    "✕ Cancel preview",
      analyzing:        "Analyzing...",
      scoreBefore:      "BEFORE",
      scoreAfter:       "AFTER",
      scoreDelta:       "CHANGE",
      moveEval:         "Move evaluation",
      readMore:         "Read more ▾",
      collapse:         "Collapse ▴",
      mPgnTitle:        "PGN",
      mLoadBtn:         "♟ Load",
      mLoadingBtn:      "⏳ Analyzing...",
      tabMoves:         "Moves",
      tabEngine:        "Engine",
      tabAI:            "AI",
      mAnalyzeBtn:      "🔍 Explain position",
      chartTitle:       "Chart",
      pasteError:       "Paste a PGN first",
      language:         "Language",
    },
    chess: {
      white:  "White",
      black:  "Black",
      move:   "Move",
      check:  "Check",
      mate:   "Mate",
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
    },
  },

  kk: {
    ui: {
      siteTitle:        "Шахмат Анализаторы",
      trainer:          "🎓 Жаттықтырушы",
      badge:            "AI + STOCKFISH",
      pgnTitle:         "Ойын PGN",
      pgnLabel:         "// PGN қойыңыз",
      pgnPlaceholder:   "1. e4 e5 2. Nf3 Nc6...",
      loadBtn:          "♟ Жүктеу және талдау",
      loadingBtn:       "⏳ Талдануда...",
      aiTitle:          "ЖИ талдауы",
      loadGame:         "Ойын жүктеңіз",
      explainBtn:       "🔍 Жүрісті / позицияны түсіндіру",
      modeReview:       "Ойынды қарау",
      modeExplore:      "Зерттеу",
      exploreBanner:    "Зерттеу режимі — талдау үшін фигураларды жылжытыңыз",
      evalChart:        "Баға графигі",
      evalChartHint:    "басу → жүріске өту",
      movesTitle:       "Жүрістер",
      engineTitle:      "Қозғалтқыш",
      cancelPreview:    "✕ Алдын ала қараудан бас тарту",
      analyzing:        "Талдануда...",
      scoreBefore:      "ДЕЙІН",
      scoreAfter:       "КЕЙІН",
      scoreDelta:       "ӨЗГЕРІС",
      moveEval:         "Жүріс бағасы",
      readMore:         "Толығырақ ▾",
      collapse:         "Жию ▴",
      mPgnTitle:        "PGN",
      mLoadBtn:         "♟ Жүктеу",
      mLoadingBtn:      "⏳ Талдау...",
      tabMoves:         "Жүрістер",
      tabEngine:        "Қозғалтқыш",
      tabAI:            "ЖИ",
      mAnalyzeBtn:      "🔍 Позицияны түсіндіру",
      chartTitle:       "График",
      pasteError:       "PGN қойыңыз",
      language:         "Тіл",
    },
    chess: {
      white:  "Ақ",
      black:  "Қара",
      move:   "Жүріс",
      check:  "Шах",
      mate:   "Мат",
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
1. Позицияны бағалаңыз
2. Негізгі тақырыптарды анықтаңыз (шабуыл, қорғаныс, пешка құрылымы)
3. Жүру кезегіндегі тарап үшін жоспар ұсыныңыз
4. Маңызды алаңдарды немесе әлсіз жерлерді көрсетіңіз

Нақты жаттықтырушы сияқты жазыңыз. Қазақ тілінде жауап беріңіз.`,
    },
  },
};

// ── Утилиты ──

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
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
}

function updateTranslations(lang) {
  document.querySelectorAll('[data-key]').forEach(el => {
    const key = el.getAttribute('data-key');
    const val = t(key, lang);
    if (el.hasAttribute('placeholder')) {
      el.placeholder = val;
    } else {
      el.textContent = val;
    }
  });
  document.title = t('ui.siteTitle', lang);
}

function initI18n() {
  const lang = getCurrentLang();
  updateTranslations(lang);
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
}

function setupLanguageSwitcher() {
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
  });
}

window.i18n = { t, getCurrentLang, setLanguage, updateTranslations, initI18n, setupLanguageSwitcher };
