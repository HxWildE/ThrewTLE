import React, { useEffect, useState } from 'react';
import { ChevronRight, Hash, Loader2, Search, Sparkles, X } from 'lucide-react';
import { apiClient } from '../api/client';
import { ProblemSummary } from '../types/api';

interface ProblemSearchProps {
  onSelectProblem: (slug: string) => void;
  selectedSlug: string | null;
}

export const ProblemSearch: React.FC<ProblemSearchProps> = ({
  onSelectProblem,
  selectedSlug,
}) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<ProblemSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  // Curated Benchmark Presets with classic 1, 2, 3, and 4-digit questions
  const presets = [
    { id: 1, title: 'Two Sum', slug: 'two-sum', diff: 'EASY' },
    { id: 100, title: 'Same Tree', slug: 'same-tree', diff: 'EASY' },
    { id: 121, title: 'Buy & Sell Stock', slug: 'best-time-to-buy-and-sell-stock', diff: 'EASY' },
    { id: 125, title: 'Valid Palindrome', slug: 'valid-palindrome', diff: 'EASY' },
    { id: 141, title: 'Linked List Cycle', slug: 'linked-list-cycle', diff: 'EASY' },
    { id: 200, title: 'Number of Islands', slug: 'number-of-islands', diff: 'MEDIUM' },
    { id: 217, title: 'Contains Duplicate', slug: 'contains-duplicate', diff: 'EASY' },
    { id: 704, title: 'Binary Search', slug: 'binary-search', diff: 'EASY' },
    { id: 1968, title: 'Array Not Avg Neighbors', slug: 'array-with-elements-not-equal-to-average-of-neighbors', diff: 'MEDIUM' },
  ];

  useEffect(() => {
    let active = true;
    if (!query.trim()) {
      apiClient.searchProblems(undefined, undefined, 12)
        .then((res) => {
          if (active) setResults(res.items);
        })
        .catch(() => {});
      return;
    }

    setLoading(true);
    const debounce = setTimeout(() => {
      apiClient.searchProblems(query.trim(), undefined, 25)
        .then((res) => {
          if (active) {
            setResults(res.items);
            setLoading(false);
          }
        })
        .catch(() => {
          if (active) setLoading(false);
        });
    }, 120);

    return () => {
      active = false;
      clearTimeout(debounce);
    };
  }, [query]);

  // Handle Enter key for instantaneous selection
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && results.length > 0) {
      const trimmed = query.trim();
      if (trimmed.length > 0) {
        // If exact source_id match exists, select it
        const exactMatch = results.find((r) => String(r.source_id) === trimmed);
        if (exactMatch) {
          onSelectProblem(exactMatch.slug);
          setIsOpen(false);
          return;
        }
      }
      onSelectProblem(results[0].slug);
      setIsOpen(false);
    }
  };

  const getDifficultyColor = (diff: string) => {
    switch (diff?.toUpperCase()) {
      case 'EASY':
        return 'text-emerald-700 bg-emerald-50 border-emerald-200 dark:text-emerald-400 dark:bg-emerald-950/50 dark:border-emerald-800/40';
      case 'MEDIUM':
        return 'text-amber-700 bg-amber-50 border-amber-200 dark:text-amber-400 dark:bg-amber-950/50 dark:border-amber-800/40';
      case 'HARD':
        return 'text-rose-700 bg-rose-50 border-rose-200 dark:text-rose-400 dark:bg-rose-950/50 dark:border-rose-800/40';
      default:
        return 'text-slate-600 bg-slate-100 border-slate-300 dark:text-slate-400 dark:bg-slate-800 dark:border-slate-700';
    }
  };

  return (
    <div className="w-full relative">
      {/* Search Input Box */}
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400 dark:text-slate-500">
          <Search className="w-4 h-4 text-blue-600 dark:text-orange-400" />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onKeyDown={handleKeyDown}
          onFocus={() => setIsOpen(true)}
          placeholder="Search by problem number (e.g. 100, 121, 200, 704), title, or slug..."
          className="w-full pl-10 pr-10 py-3 rounded-xl bg-white dark:bg-[#0b101e] border border-slate-300 dark:border-slate-800 focus:border-blue-500 dark:focus:border-orange-500 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-orange-500/20 text-sm font-medium text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 transition-all shadow-sm"
        />
        {loading ? (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400">
            <Loader2 className="w-4 h-4 animate-spin text-blue-600 dark:text-orange-400" />
          </div>
        ) : query ? (
          <button
            onClick={() => setQuery('')}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
          >
            <X className="w-4 h-4" />
          </button>
        ) : null}
      </div>

      {/* Quick Select Benchmark Chips */}
      <div className="flex flex-wrap items-center gap-1.5 sm:gap-2 mt-2.5">
        <span className="text-xs text-slate-500 dark:text-slate-400 flex items-center gap-1 font-semibold mr-1">
          <Sparkles className="w-3.5 h-3.5 text-blue-600 dark:text-orange-400" /> Popular:
        </span>
        {presets.map((p) => {
          const isSelected = selectedSlug === p.slug;
          return (
            <button
              key={p.slug}
              onClick={() => {
                onSelectProblem(p.slug);
                setIsOpen(false);
              }}
              className={`text-xs px-2.5 py-1 rounded-lg border font-semibold transition-all ${
                isSelected
                  ? 'bg-blue-50 text-blue-700 border-blue-400 dark:bg-orange-950/80 dark:text-orange-300 dark:border-orange-700 shadow-sm'
                  : 'bg-white hover:bg-slate-50 text-slate-700 border-slate-200 dark:bg-slate-900/60 dark:text-slate-300 dark:border-slate-800 dark:hover:bg-slate-800'
              }`}
            >
              #{p.id} {p.title}
            </button>
          );
        })}
      </div>

      {/* Dropdown Results */}
      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-20"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute left-0 right-0 top-12 mt-2 bg-white dark:bg-[#0d1322] border border-slate-200 dark:border-slate-800 rounded-xl shadow-2xl z-30 max-h-80 overflow-y-auto divide-y divide-slate-100 dark:divide-slate-800/60 animate-fade-in">
            {/* Header info in dropdown */}
            <div className="px-3.5 py-2 bg-slate-50/80 dark:bg-slate-900/80 text-[11px] font-bold text-slate-500 dark:text-slate-400 flex items-center justify-between">
              <span>
                {results.length > 0
                  ? `Showing top ${results.length} questions`
                  : loading
                  ? 'Searching catalogue...'
                  : 'No questions found'}
              </span>
              <span className="text-[10px] font-mono">Press [Enter] to select #1</span>
            </div>

            {results.length > 0 ? (
              results.map((prob) => (
                <div
                  key={prob.id}
                  onClick={() => {
                    onSelectProblem(prob.slug);
                    setIsOpen(false);
                  }}
                  className={`p-3.5 hover:bg-slate-50 dark:hover:bg-slate-800/80 cursor-pointer flex items-center justify-between transition-colors ${
                    selectedSlug === prob.slug ? 'bg-blue-50/60 dark:bg-orange-950/30' : ''
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-xs font-bold text-blue-700 dark:text-orange-400 w-12 shrink-0">
                      #{prob.source_id}
                    </span>
                    <div>
                      <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100">{prob.title}</h4>
                      <p className="text-xs font-mono text-slate-500 dark:text-slate-400">{prob.slug}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getDifficultyColor(
                        prob.difficulty
                      )}`}
                    >
                      {prob.difficulty}
                    </span>
                    <ChevronRight className="w-4 h-4 text-slate-400" />
                  </div>
                </div>
              ))
            ) : !loading && query.trim() ? (
              <div className="p-6 text-center text-xs text-slate-500 dark:text-slate-400 space-y-1">
                <p className="font-semibold text-slate-700 dark:text-slate-300">
                  No problems matched "{query}"
                </p>
                <p>Try searching by number like 100, 121, 141, 200, 217, or 704.</p>
              </div>
            ) : null}
          </div>
        </>
      )}
    </div>
  );
};
