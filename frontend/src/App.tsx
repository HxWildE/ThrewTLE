import React, { useEffect, useState } from 'react';
import { Loader2, Zap } from 'lucide-react';
import { CategorySelector } from './components/CategorySelector';
import { ErrorState } from './components/ErrorState';
import { Header } from './components/Header';
import { ProblemCard } from './components/ProblemCard';
import { ProblemSearch } from './components/ProblemSearch';
import { TestCaseList } from './components/TestCaseList';
import { useProblem } from './hooks/useProblem';
import { useTestCases } from './hooks/useTestCases';
import { Category } from './types/api';

export const App: React.FC = () => {
  // Default to Two Sum for immediate interactive demo
  const [selectedSlug, setSelectedSlug] = useState<string>('two-sum');
  const [selectedCategories, setSelectedCategories] = useState<Category[]>([
    'basic',
    'boundary',
    'structural',
    'numeric_extremes',
    'stress',
  ]);
  const [count, setCount] = useState<number>(20);
  const [seed, setSeed] = useState<number>(42);

  const { problem, loading: problemLoading, error: problemError } = useProblem(selectedSlug);
  const {
    testCases,
    rawBatchInput,
    limitations,
    generating,
    error: generateError,
    generate,
    clear,
  } = useTestCases(selectedSlug);

  // Automatically clear and generate default test suite when problem changes
  useEffect(() => {
    if (selectedSlug) {
      clear();
      generate(count, selectedCategories, seed);
    }
  }, [selectedSlug]);

  const handleToggleCategory = (cat: Category) => {
    setSelectedCategories((prev) =>
      prev.includes(cat) ? prev.filter((c) => c !== cat) : [...prev, cat]
    );
  };

  const handleGenerate = () => {
    generate(count, selectedCategories, seed);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#070a12] text-slate-900 dark:text-slate-100 flex flex-col relative overflow-x-hidden transition-colors">
      {/* Background Ambient Glows (strictly absolute, blurred, and non-blocking) */}
      <div className="pointer-events-none absolute -z-0 rounded-full blur-[140px] opacity-15 w-[500px] h-[500px] bg-blue-500 dark:bg-orange-600 -top-40 -left-40" />
      <div className="pointer-events-none absolute -z-0 rounded-full blur-[140px] opacity-15 w-[450px] h-[450px] bg-indigo-500 dark:bg-amber-600 -bottom-20 -right-20" />

      {/* Header */}
      <Header />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 relative z-10">
        {/* Hero & Search Section */}
        <div className="space-y-4">
          <div className="space-y-1">
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
              LeetCode Test Case Generator
              <Zap className="w-6 h-6 text-blue-600 dark:text-orange-500 fill-current inline-block" />
            </h1>
            <p className="text-sm text-slate-600 dark:text-slate-400 max-w-2xl leading-relaxed font-medium">
              Expose algorithmic edge failures, subtle integer overflows, and worst-case quadratic complexity before submitting your solution.
            </p>
          </div>

          <ProblemSearch
            onSelectProblem={setSelectedSlug}
            selectedSlug={selectedSlug}
          />
        </div>

        {/* Content Area */}
        {problemLoading ? (
          <div className="theme-card rounded-2xl p-16 flex flex-col items-center justify-center gap-3 border shadow-sm">
            <Loader2 className="w-8 h-8 text-blue-600 dark:text-orange-500 animate-spin" />
            <p className="text-sm font-semibold text-slate-600 dark:text-slate-400">
              Loading problem metadata and constraint specifications...
            </p>
          </div>
        ) : problemError ? (
          <ErrorState error={problemError} onRetry={() => setSelectedSlug(selectedSlug)} />
        ) : problem ? (
          <div className="space-y-6">
            {/* Problem Metadata Card */}
            <ProblemCard problem={problem} />

            {/* Test Configuration & Generation Bar */}
            <CategorySelector
              selectedCategories={selectedCategories}
              onToggleCategory={handleToggleCategory}
              count={count}
              onChangeCount={setCount}
              seed={seed}
              onChangeSeed={setSeed}
              onGenerate={handleGenerate}
              generating={generating}
              disabled={problem.support_status === 'UNSUPPORTED_FORMAT'}
            />

            {/* Generation Error if any */}
            {generateError && (
              <ErrorState error={generateError} onRetry={handleGenerate} />
            )}

            {/* Generated Test Suite List with Categorized Collective Boxes */}
            <TestCaseList
              testCases={testCases}
              rawBatchInput={rawBatchInput}
              limitations={limitations}
              problemSlug={selectedSlug}
            />
          </div>
        ) : null}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-[#070a12] py-6 text-center text-xs text-slate-500 dark:text-slate-400 font-medium transition-colors">
        <p>
          ThrewTLE &bull; Problem-Specific Edge Case Synthesis &bull; MIT License
        </p>
      </footer>
    </div>
  );
};
