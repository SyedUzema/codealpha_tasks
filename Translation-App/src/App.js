import React, { useState, useEffect, useRef } from 'react';
import { Copy, Volume2, RefreshCw, Sparkles, Zap, Brain, Trash2, Moon, Sun } from 'lucide-react';

function App() {
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLang, setSourceLang] = useState('en');
  const [targetLang, setTargetLang] = useState('es');
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');
  const [darkMode, setDarkMode] = useState(true);
  const debounceTimer = useRef(null);

  const speechLangMap = {
    'en': 'en-US',
    'es': 'es-ES',
    'fr': 'fr-FR',
    'de': 'de-DE',
    'it': 'it-IT',
    'pt': 'pt-PT',
    'ru': 'ru-RU',
    'ja': 'ja-JP',
    'ko': 'ko-KR',
    'zh': 'zh-CN',
    'ar': 'ar-SA',
    'hi': 'hi-IN',
    'tr': 'tr-TR',
    'nl': 'nl-NL',
    'pl': 'pl-PL',
  };

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'it', name: 'Italian' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'ru', name: 'Russian' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
    { code: 'zh', name: 'Chinese' },
    { code: 'ar', name: 'Arabic' },
    { code: 'hi', name: 'Hindi' },
    { code: 'tr', name: 'Turkish' },
    { code: 'nl', name: 'Dutch' },
    { code: 'pl', name: 'Polish' },
  ];

  // LibreTranslate API - Much better than MyMemory!
  const translateWithAPI = async (text, source, target) => {
    try {
      const response = await fetch('https://libretranslate.com/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          q: text,
          source: source,
          target: target,
          format: 'text'
        })
      });

      if (!response.ok) {
        throw new Error('Translation service error');
      }

      const data = await response.json();

      if (data.translatedText) {
        return data.translatedText;
      } else {
        throw new Error('Translation failed');
      }
    } catch (error) {
      throw new Error('Network error. Please check your connection.');
    }
  };

  // Main translation function
  const translateText = async () => {
    if (!sourceText.trim()) {
      setTranslatedText('');
      setError('');
      return;
    }

    if (sourceLang === targetLang) {
      setError('Source and target languages cannot be the same');
      setTranslatedText('');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const result = await translateWithAPI(sourceText, sourceLang, targetLang);
      setTranslatedText(result);
    } catch (err) {
      console.error('Translation error:', err);
      setError(err.message || 'Translation failed. Please try again.');
      setTranslatedText('');
    } finally {
      setIsLoading(false);
    }
  };

  // Debouncing
  useEffect(() => {
    if (sourceText.trim()) {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }

      debounceTimer.current = setTimeout(() => {
        translateText();
      }, 1200);

      return () => {
        if (debounceTimer.current) {
          clearTimeout(debounceTimer.current);
        }
      };
    } else {
      setTranslatedText('');
      setError('');
    }
  }, [sourceText, sourceLang, targetLang]);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(translatedText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      setError('Failed to copy to clipboard');
    }
  };

  const speakText = (text, lang) => {
    if (!text.trim()) return;

    try {
      speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      const mappedLang = speechLangMap[lang] || lang;
      utterance.lang = mappedLang;
      utterance.rate = 0.9;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;
      speechSynthesis.speak(utterance);
    } catch (err) {
      console.error('Speech synthesis error:', err);
      setError('Text-to-speech is not supported in your browser');
      setTimeout(() => setError(''), 3000);
    }
  };

  const swapLanguages = () => {
    if (!sourceText.trim() && !translatedText.trim()) {
      setError('Nothing to swap. Please enter some text first.');
      setTimeout(() => setError(''), 3000);
      return;
    }

    const tempLang = sourceLang;
    const tempText = sourceText;
    
    setSourceLang(targetLang);
    setTargetLang(tempLang);
    setSourceText(translatedText);
    setTranslatedText(tempText);
  };

  const clearAll = () => {
    setSourceText('');
    setTranslatedText('');
    setError('');
    setCopied(false);
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 p-6 sm:p-10 ${
      darkMode 
        ? 'bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900' 
        : 'bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50'
    }`}>
      <div className="max-w-7xl mx-auto">
        {/* Dark Mode Toggle */}
        <div className="flex justify-end mb-4">
          <button
            onClick={toggleDarkMode}
            className={`p-3 rounded-xl transition-all ${
              darkMode 
                ? 'bg-white/10 hover:bg-white/20 text-yellow-300' 
                : 'bg-slate-800/10 hover:bg-slate-800/20 text-slate-800'
            }`}
            title="Toggle dark mode"
          >
            {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </div>

        {/* Header */}
        <div className="text-center mb-12">
          <div className={`inline-flex items-center gap-2 backdrop-blur-sm border rounded-full px-6 py-2 mb-4 ${
            darkMode 
              ? 'bg-blue-500/20 border-blue-400/30' 
              : 'bg-blue-100 border-blue-300'
          }`}>
            <Brain className={`w-5 h-5 ${darkMode ? 'text-blue-300' : 'text-blue-600'}`} />
            <span className={`text-sm font-semibold tracking-wide ${
              darkMode ? 'text-blue-200' : 'text-blue-800'
            }`}>
              POWERED BY AI
            </span>
            <Sparkles className={`w-5 h-5 ${darkMode ? 'text-blue-300' : 'text-blue-600'}`} />
          </div>
          
          <h1 className={`text-6xl font-bold mb-3 ${
            darkMode 
              ? 'text-transparent bg-clip-text bg-gradient-to-r from-blue-200 via-cyan-200 to-teal-200' 
              : 'text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600'
          }`}>
            Neural Translate
          </h1>
          <p className={`text-lg ${darkMode ? 'text-blue-200/80' : 'text-slate-700'}`}>
            Experience lightning-fast AI translation • 15+ languages
          </p>
        </div>

        {/* Main Translation Interface */}
        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          {/* Source Panel */}
          <div className={`backdrop-blur-xl border rounded-3xl shadow-2xl p-8 transition-all duration-300 ${
            darkMode 
              ? 'bg-white/10 border-white/20 hover:border-blue-400/50' 
              : 'bg-white/80 border-slate-200 hover:border-blue-400'
          }`}>
            <div className="flex items-center justify-between mb-6">
              <label className={`text-sm font-bold tracking-wider uppercase ${
                darkMode ? 'text-blue-300' : 'text-blue-600'
              }`}>
                Source Language
              </label>
              <Zap className={`w-5 h-5 ${darkMode ? 'text-yellow-400' : 'text-yellow-600'}`} />
            </div>
            
            <select
              value={sourceLang}
              onChange={(e) => setSourceLang(e.target.value)}
              className={`w-full p-4 mb-6 border rounded-2xl font-medium focus:outline-none focus:ring-2 transition-all ${
                darkMode 
                  ? 'bg-slate-800/50 border-blue-500/30 text-white focus:ring-blue-500' 
                  : 'bg-white border-blue-300 text-slate-800 focus:ring-blue-400'
              }`}
            >
              {languages.map((lang) => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>

            <div className="relative">
              <textarea
                value={sourceText}
                onChange={(e) => setSourceText(e.target.value)}
                placeholder="Type or paste your text here..."
                className={`w-full h-72 p-6 border rounded-2xl text-lg resize-none focus:outline-none focus:ring-2 transition-all ${
                  darkMode 
                    ? 'bg-slate-800/50 border-blue-500/30 text-white placeholder-slate-400 focus:ring-blue-500' 
                    : 'bg-white border-blue-300 text-slate-800 placeholder-slate-400 focus:ring-blue-400'
                }`}
              />
              <button
                onClick={() => speakText(sourceText, sourceLang)}
                disabled={!sourceText}
                className="absolute bottom-6 right-6 p-3 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-xl hover:scale-110 transition-all disabled:opacity-30 disabled:cursor-not-allowed shadow-lg"
                title="Listen to text"
              >
                <Volume2 className="w-5 h-5" />
              </button>
            </div>

            <div className={`mt-4 text-sm text-right font-medium ${
              darkMode ? 'text-blue-300/70' : 'text-slate-600'
            }`}>
              {sourceText.length} characters
            </div>
          </div>

          {/* Target Panel */}
          <div className={`backdrop-blur-xl border rounded-3xl shadow-2xl p-8 transition-all duration-300 ${
            darkMode 
              ? 'bg-white/10 border-white/20 hover:border-cyan-400/50' 
              : 'bg-white/80 border-slate-200 hover:border-cyan-400'
          }`}>
            <div className="flex items-center justify-between mb-6">
              <label className={`text-sm font-bold tracking-wider uppercase ${
                darkMode ? 'text-cyan-300' : 'text-cyan-600'
              }`}>
                Target Language
              </label>
              <Sparkles className={`w-5 h-5 ${darkMode ? 'text-cyan-400' : 'text-cyan-600'}`} />
            </div>
            
            <select
              value={targetLang}
              onChange={(e) => setTargetLang(e.target.value)}
              className={`w-full p-4 mb-6 border rounded-2xl font-medium focus:outline-none focus:ring-2 transition-all ${
                darkMode 
                  ? 'bg-slate-800/50 border-cyan-500/30 text-white focus:ring-cyan-500' 
                  : 'bg-white border-cyan-300 text-slate-800 focus:ring-cyan-400'
              }`}
            >
              {languages.map((lang) => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>

            <div className="relative">
              <div className={`w-full h-72 p-6 border rounded-2xl text-lg overflow-y-auto ${
                darkMode 
                  ? 'bg-slate-800/50 border-cyan-500/30 text-white' 
                  : 'bg-white border-cyan-300 text-slate-800'
              }`}>
                {isLoading ? (
                  <div className="flex flex-col items-center justify-center h-full gap-3">
                    <RefreshCw className={`w-10 h-10 animate-spin ${
                      darkMode ? 'text-cyan-400' : 'text-cyan-600'
                    }`} />
                    <p className={`text-sm font-semibold ${
                      darkMode ? 'text-cyan-300' : 'text-cyan-700'
                    }`}>Translating...</p>
                  </div>
                ) : translatedText ? (
                  <p className="leading-relaxed">{translatedText}</p>
                ) : (
                  <p className={`italic ${darkMode ? 'text-slate-400' : 'text-slate-500'}`}>
                    Your translation will appear here...
                  </p>
                )}
              </div>
              <div className="absolute bottom-6 right-6 flex gap-3">
                <button
                  onClick={() => speakText(translatedText, targetLang)}
                  disabled={!translatedText}
                  className="p-3 bg-gradient-to-r from-cyan-500 to-teal-500 text-white rounded-xl hover:scale-110 transition-all disabled:opacity-30 disabled:cursor-not-allowed shadow-lg"
                  title="Listen to translation"
                >
                  <Volume2 className="w-5 h-5" />
                </button>
                <button
                  onClick={copyToClipboard}
                  disabled={!translatedText}
                  className="p-3 bg-gradient-to-r from-emerald-500 to-green-500 text-white rounded-xl hover:scale-110 transition-all disabled:opacity-30 disabled:cursor-not-allowed shadow-lg"
                  title="Copy translation"
                >
                  <Copy className="w-5 h-5" />
                </button>
              </div>
            </div>

            {copied && (
              <div className={`mt-4 text-sm text-right font-semibold flex items-center justify-end gap-2 ${
                darkMode ? 'text-emerald-400' : 'text-emerald-600'
              }`}>
                <span className="text-lg">✓</span>
                Copied successfully!
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center gap-4 mb-8">
          <button
            onClick={swapLanguages}
            className="p-5 bg-gradient-to-r from-violet-500 to-purple-500 text-white rounded-2xl shadow-2xl hover:scale-110 transition-all duration-300 group"
            title="Swap languages"
          >
            <RefreshCw className="w-7 h-7 group-hover:rotate-180 transition-transform duration-500" />
          </button>
          
          <button
            onClick={clearAll}
            className="p-5 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-2xl shadow-2xl hover:scale-110 transition-all duration-300"
            title="Clear all"
          >
            <Trash2 className="w-7 h-7" />
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className={`mb-8 p-5 backdrop-blur-sm border rounded-2xl text-center font-semibold ${
            darkMode 
              ? 'bg-red-500/20 border-red-400/50 text-red-200' 
              : 'bg-red-100 border-red-300 text-red-800'
          }`}>
            {error}
          </div>
        )}

        {/* AI Features Showcase */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className={`backdrop-blur-sm border rounded-2xl p-6 text-center transition-all ${
            darkMode 
              ? 'bg-white/5 border-white/10 hover:bg-white/10' 
              : 'bg-white/60 border-slate-200 hover:bg-white/80'
          }`}>
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-xl">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <h3 className={`text-xl font-bold mb-2 ${darkMode ? 'text-white' : 'text-slate-800'}`}>
              AI-Powered
            </h3>
            <p className={`text-sm ${darkMode ? 'text-blue-200/70' : 'text-slate-600'}`}>
              Advanced translation technology for accurate results
            </p>
          </div>

          <div className={`backdrop-blur-sm border rounded-2xl p-6 text-center transition-all ${
            darkMode 
              ? 'bg-white/5 border-white/10 hover:bg-white/10' 
              : 'bg-white/60 border-slate-200 hover:bg-white/80'
          }`}>
            <div className="w-16 h-16 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-xl">
              <Zap className="w-8 h-8 text-white" />
            </div>
            <h3 className={`text-xl font-bold mb-2 ${darkMode ? 'text-white' : 'text-slate-800'}`}>
              Lightning Fast
            </h3>
            <p className={`text-sm ${darkMode ? 'text-cyan-200/70' : 'text-slate-600'}`}>
              Get instant translations as you type
            </p>
          </div>

          <div className={`backdrop-blur-sm border rounded-2xl p-6 text-center transition-all ${
            darkMode 
              ? 'bg-white/5 border-white/10 hover:bg-white/10' 
              : 'bg-white/60 border-slate-200 hover:bg-white/80'
          }`}>
            <div className="w-16 h-16 bg-gradient-to-br from-violet-500 to-purple-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-xl">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <h3 className={`text-xl font-bold mb-2 ${darkMode ? 'text-white' : 'text-slate-800'}`}>
              15+ Languages
            </h3>
            <p className={`text-sm ${darkMode ? 'text-purple-200/70' : 'text-slate-600'}`}>
              Break language barriers with wide language support
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;