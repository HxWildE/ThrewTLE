import React, { useEffect, useState } from 'react';
import { Database, ExternalLink, Github, Info, Moon, Sun, X, Zap } from 'lucide-react';
import { apiClient } from '../api/client';
import { useTheme } from '../context/ThemeContext';

export const Header: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const [dbHealthy, setDbHealthy] = useState<boolean | null>(null);
  const [showEngineInfo, setShowEngineInfo] = useState(false);

  useEffect(() => {
    apiClient.checkHealth()
      .then((res) => setDbHealthy(res.database === 'connected'))
      .catch(() => setDbHealthy(false));
  }, []);

  return (
    <>
      <header className="border-b border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-[#070a12]/95 backdrop-blur-md sticky top-0 z-40 transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          {/* Logo & Subtitle */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-blue-600 dark:bg-orange-500 flex items-center justify-center shadow-md shadow-blue-500/20 dark:shadow-orange-500/30 transition-colors">
              <Zap className="w-5 h-5 text-white fill-current" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg tracking-tight text-slate-900 dark:text-white">
                  ThrewTLE
                </span>
                <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 dark:bg-orange-950/60 dark:text-orange-400 dark:border-orange-800/60 transition-colors">
                  MVP v0.2
                </span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 hidden sm:block font-medium">
                Problem-Specific LeetCode Test Case Generator
              </p>
            </div>
          </div>

          {/* Right Action Controls */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Engine Info Button */}
            <button
              onClick={() => setShowEngineInfo(true)}
              className="flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/80 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              title="How test cases are generated"
            >
              <Info className="w-3.5 h-3.5 text-blue-600 dark:text-orange-400" />
              <span className="hidden md:inline">How It Works</span>
            </button>

            {/* Catalogue Status */}
            <div className="flex items-center gap-2 text-xs font-medium px-2.5 py-1.5 rounded-lg bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800">
              <span
                className={`w-2 h-2 rounded-full ${
                  dbHealthy === null
                    ? 'bg-slate-400 animate-pulse'
                    : dbHealthy
                    ? 'bg-emerald-500 shadow-sm shadow-emerald-500/50'
                    : 'bg-rose-500'
                }`}
              />
              <span className="text-slate-600 dark:text-slate-300 text-[11px] hidden sm:inline">
                {dbHealthy === null ? 'Connecting...' : dbHealthy ? '200+ Problems' : 'Offline'}
              </span>
            </div>

            {/* Theme Toggle (Light: White+Blue, Dark: Dark+Orange) */}
            <button
              onClick={toggleTheme}
              aria-label="Toggle Theme"
              className="p-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/80 text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              title={theme === 'light' ? 'Switch to Dark Mode (Carbon + Orange)' : 'Switch to Light Mode (White + Blue)'}
            >
              {theme === 'light' ? (
                <Moon className="w-4 h-4 text-blue-600" />
              ) : (
                <Sun className="w-4 h-4 text-orange-400" />
              )}
            </button>

            {/* GitHub Link */}
            <a
              href="https://github.com/HxWildE/ThrewTLE"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/80 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              <Github className="w-4 h-4" />
              <span className="hidden sm:inline">GitHub</span>
              <ExternalLink className="w-3 h-3 text-slate-400" />
            </a>
          </div>
        </div>
      </header>

      {/* Engine Architecture & Source Info Modal */}
      {showEngineInfo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
          <div className="bg-white dark:bg-[#0d1322] border border-slate-200 dark:border-slate-800 rounded-2xl max-w-xl w-full p-6 shadow-2xl relative space-y-4 text-slate-800 dark:text-slate-200">
            <button
              onClick={() => setShowEngineInfo(false)}
              className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-orange-950/60 flex items-center justify-center text-blue-600 dark:text-orange-400">
                <Database className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-lg text-slate-900 dark:text-white">
                  Where Does Test Generation Come From?
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Algorithmic Engine &bull; Property Synthesis &bull; Verified Oracles
                </p>
              </div>
            </div>

            <div className="space-y-3 text-xs leading-relaxed text-slate-600 dark:text-slate-300">
              <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800/80 space-y-1.5">
                <p className="font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-600 dark:bg-orange-500" />
                  1. Algorithmic Synthesis Engine (Python Engine, not static DB)
                </p>
                <p>
                  Tests are generated on-the-fly dynamically using mathematical strategies in Python: 
                  <strong> Boundary</strong> (array length limits), <strong>Structural</strong> (alternating/zigzag/all-equal permutations), 
                  <strong> Numeric Extremes</strong> (&plusmn;2<sup>31</sup>-1, 0, sign flips), and <strong>Stress</strong> (scaled inputs to catch O(N<sup>2</sup>) bottlenecks).
                </p>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800/80 space-y-1.5">
                <p className="font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-600 dark:bg-orange-500" />
                  2. Hypothesis Property Testing
                </p>
                <p>
                  Property-based strategies generate diverse, valid inputs matching the exact parameter signatures (<code className="font-mono">int[]</code>, <code className="font-mono">string</code>, <code className="font-mono">matrix</code>) while strictly respecting problem constraints.
                </p>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800/80 space-y-1.5">
                <p className="font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-600 dark:bg-orange-500" />
                  3. Truthful Oracles & Deduplication
                </p>
                <p>
                  Canonical solutions verify expected outputs (labeled <strong>Verified</strong>). Special-judge problems (like #1968 where multiple valid answers exist) are honestly marked <strong>Input Only</strong> with <code className="font-mono">expected_output: null</code>.
                  All generated test cases are SHA-256 fingerprinted and cached in the local database to eliminate duplicates.
                </p>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setShowEngineInfo(false)}
                className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 dark:bg-orange-500 dark:hover:bg-orange-600 transition-colors"
              >
                Got It
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
