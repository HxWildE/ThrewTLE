import React from 'react';
import { Check, Dice5, Filter, Loader2, Sliders, Sparkles } from 'lucide-react';
import { Category } from '../types/api';

interface CategorySelectorProps {
  selectedCategories: Category[];
  onToggleCategory: (category: Category) => void;
  count: number;
  onChangeCount: (count: number) => void;
  seed: number;
  onChangeSeed: (seed: number) => void;
  onGenerate: () => void;
  generating: boolean;
  disabled?: boolean;
}

export const CategorySelector: React.FC<CategorySelectorProps> = ({
  selectedCategories,
  onToggleCategory,
  count,
  onChangeCount,
  seed,
  onChangeSeed,
  onGenerate,
  generating,
  disabled = false,
}) => {
  const categoriesList: Array<{ id: Category; label: string; desc: string }> = [
    { id: 'basic', label: 'Basic', desc: 'Sanity & baseline inputs' },
    { id: 'boundary', label: 'Boundary', desc: 'Min/max lengths & array bounds' },
    { id: 'structural', label: 'Structural', desc: 'Permutations, duplicates, sequences' },
    { id: 'numeric_extremes', label: 'Extremes', desc: 'Zeros, negatives, 32-bit limits' },
    { id: 'stress', label: 'Stress', desc: 'Large scale to challenge O(N²) limits' },
  ];

  const handleRandomSeed = () => {
    onChangeSeed(Math.floor(Math.random() * 100000));
  };

  return (
    <div className="theme-card rounded-2xl p-5 sm:p-6 border shadow-md space-y-6 transition-colors">
      {/* Category Chips Bar */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <label className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider flex items-center gap-2">
            <Filter className="w-4 h-4 text-blue-600 dark:text-orange-400" />
            Target Test Categories ({selectedCategories.length}/5 Selected)
          </label>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3">
          {categoriesList.map((cat) => {
            const isSelected = selectedCategories.includes(cat.id);
            return (
              <button
                key={cat.id}
                type="button"
                onClick={() => onToggleCategory(cat.id)}
                className={`p-3.5 rounded-xl border text-left transition-all relative ${
                  isSelected
                    ? 'bg-blue-50/90 border-blue-500 shadow-sm shadow-blue-500/10 dark:bg-orange-950/70 dark:border-orange-500 dark:shadow-orange-500/20'
                    : 'bg-white hover:bg-slate-50 border-slate-200 text-slate-600 dark:bg-slate-900/60 dark:hover:bg-slate-800 dark:border-slate-800 dark:text-slate-400'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span
                    className={`font-bold text-xs sm:text-sm ${
                      isSelected
                        ? 'text-blue-900 dark:text-orange-200 font-extrabold'
                        : 'text-slate-800 dark:text-slate-200'
                    }`}
                  >
                    {cat.label}
                  </span>
                  <span
                    className={`w-4 h-4 rounded-full flex items-center justify-center transition-colors ${
                      isSelected
                        ? 'bg-blue-600 text-white dark:bg-orange-500 dark:text-white'
                        : 'border border-slate-300 dark:border-slate-700'
                    }`}
                  >
                    {isSelected && <Check className="w-2.5 h-2.5 stroke-[3]" />}
                  </span>
                </div>
                <p
                  className={`text-[11px] leading-snug mt-1.5 ${
                    isSelected
                      ? 'text-blue-700/80 dark:text-orange-300/80'
                      : 'text-slate-500 dark:text-slate-400'
                  }`}
                >
                  {cat.desc}
                </p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Generation Parameters: Count & Deterministic Seed */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 pt-2 border-t border-slate-100 dark:border-slate-800/80 items-end">
        {/* Count Slider */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs font-bold text-slate-700 dark:text-slate-300">
            <span className="flex items-center gap-1.5">
              <Sliders className="w-3.5 h-3.5 text-blue-600 dark:text-orange-400" />
              Target Test Cases
            </span>
            <span className="font-mono px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 dark:bg-orange-950/80 dark:text-orange-400 dark:border-orange-800">
              {count} cases
            </span>
          </div>
          <input
            type="range"
            min="1"
            max="20"
            value={count}
            onChange={(e) => onChangeCount(parseInt(e.target.value, 10))}
            className="w-full accent-blue-600 dark:accent-orange-500 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] text-slate-400 font-mono">
            <span>1</span>
            <span>10</span>
            <span>20</span>
          </div>
        </div>

        {/* Deterministic Seed */}
        <div className="space-y-2">
          <label className="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-blue-600 dark:text-orange-400" />
              RNG Seed (Reproducibility)
            </span>
          </label>
          <div className="flex items-center gap-2">
            <input
              type="number"
              value={seed}
              onChange={(e) => onChangeSeed(parseInt(e.target.value, 10) || 0)}
              className="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-[#070b16] border border-slate-300 dark:border-slate-800 text-xs font-mono font-bold text-slate-800 dark:text-slate-100 focus:outline-none focus:border-blue-500 dark:focus:border-orange-500"
            />
            <button
              type="button"
              onClick={handleRandomSeed}
              className="px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 text-xs flex items-center gap-1 transition-colors"
              title="Generate Random Seed"
            >
              <Dice5 className="w-4 h-4 text-blue-600 dark:text-orange-400" />
            </button>
          </div>
        </div>

        {/* Synthesis Generate Button */}
        <div>
          <button
            type="button"
            onClick={onGenerate}
            disabled={generating || disabled || selectedCategories.length === 0}
            className={`w-full py-3 px-4 rounded-xl font-extrabold text-sm flex items-center justify-center gap-2 transition-all shadow-md active:scale-95 ${
              generating || disabled || selectedCategories.length === 0
                ? 'bg-slate-200 dark:bg-slate-800 text-slate-400 dark:text-slate-600 cursor-not-allowed shadow-none'
                : 'bg-blue-600 hover:bg-blue-700 text-white shadow-blue-500/20 dark:bg-orange-500 dark:hover:bg-orange-600 dark:text-white dark:shadow-orange-500/30'
            }`}
          >
            {generating ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-white" />
                <span>Synthesizing Test Cases...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 text-white" />
                <span>Generate Edge-Case Suite</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
