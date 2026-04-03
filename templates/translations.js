// translations.js
// Структурированные переводы для ru, en, kk
const translations = {
  ru: {
    ui: {
      play: "Играть",
      stop: "Стоп",
      language: "Язык",
      siteTitle: "Шахматный Анализатор",
      comment: "Комментарий к ходу",
      aiAnalysis: "Анализ ИИ"
    },
    chess: {
      move: "Ход",
      check: "Шах",
      mate: "Мат"
    },
    ai: {
      thinking: "ИИ думает...",
      suggestion: "Совет ИИ"
    }
  },
  en: {
    ui: {
      play: "Play",
      stop: "Stop",
      language: "Language",
      siteTitle: "Chess Analyzer",
      comment: "Move comment",
      aiAnalysis: "AI Analysis"
    },
    chess: {
      move: "Move",
      check: "Check",
      mate: "Mate"
    },
    ai: {
      thinking: "AI is thinking...",
      suggestion: "AI Suggestion"
    }
  },
  kk: {
    ui: {
      play: "Ойнау",
      stop: "Тоқтату",
      language: "Тіл",
      siteTitle: "Шахмат Анализаторы",
      comment: "Жүріс түсіндірмесі",
      aiAnalysis: "ЖИ талдауы"
    },
    chess: {
      move: "Жүріс",
      check: "Шах",
      mate: "Мат"
    },
    ai: {
      thinking: "ЖИ ойлануда...",
      suggestion: "ЖИ ұсынысы"
    }
  }
};

// Получить перевод по ключу с поддержкой вложенности и fallback на ru
function t(key, lang) {
  const keys = key.split('.');
  let value = translations[lang];
  for (const k of keys) {
    if (value && k in value) value = value[k];
    else {
      // fallback to ru
      value = translations['ru'];
      for (const k2 of keys) {
        if (value && k2 in value) value = value[k2];
        else return key;
      }
      return value;
    }
  }
  return value;
}

// Обновить все элементы с data-key
function updateTranslations(lang) {
  document.querySelectorAll('[data-key]').forEach(el => {
    const key = el.getAttribute('data-key');
    if (el.placeholder !== undefined && el.hasAttribute('placeholder')) {
      el.placeholder = t(key, lang);
    } else {
      el.textContent = t(key, lang);
    }
  });
  // Обновить title сайта
  document.title = t('ui.siteTitle', lang);
}

// Сохранить выбранный язык
function setLanguage(lang) {
  localStorage.setItem('lang', lang);
  updateTranslations(lang);
}

// Получить язык (из localStorage или по умолчанию ru)
function getLanguage() {
  return localStorage.getItem('lang') || 'ru';
}

// Инициализация
function initI18n() {
  const lang = getLanguage();
  updateTranslations(lang);
  // Установить активную кнопку
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
}

// Логика переключения языка
function setupLanguageSwitcher() {
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      setLanguage(btn.dataset.lang);
      document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
}

// Для динамического контента (например, AI комментарии)
function translateDynamic(key, lang) {
  return t(key, lang);
}

window.i18n = {
  t,
  updateTranslations,
  setLanguage,
  getLanguage,
  initI18n,
  setupLanguageSwitcher,
  translateDynamic
};
