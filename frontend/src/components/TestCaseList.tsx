import React, { useMemo, useState } from 'react';
import { 
  AlertCircle, 
  Check, 
  Copy, 
  FileText, 
  Layers, 
  Terminal 
} from 'lucide-react';
import { TestCase } from '../types/api';
import { TestCaseCard } from './TestCaseCard';

interface TestCaseListProps {
  testCases: TestCase[];
  rawBatchInput: string;
  limitations?: string | null;
  problemSlug?: string;
}

interface CategoryMeta {
  title: string;
  desc: string;
  badgeLight: string;
  badgeDark: string;
}

const CATEGORY_META: Record<string, CategoryMeta> = {
  boundary: {
    title: 'Boundary Cases',
    desc: 'Min/max lengths & single-element bounds',
    badgeLight: 'bg-amber-50 text-amber-800 border-amber-200',
    badgeDark: 'dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800/60',
  },
  structural: {
    title: 'Structural Permutations',
    desc: 'Alternating, zigzag, and all-equal distributions',
    badgeLight: 'bg-blue-50 text-blue-800 border-blue-200',
    badgeDark: 'dark:bg-sky-950/60 dark:text-sky-300 dark:border-sky-800/60',
  },
  numeric_extremes: {
    title: 'Numeric Extremes',
    desc: '32-bit limits, zeroes, and sign inversions',
    badgeLight: 'bg-rose-50 text-rose-800 border-rose-200',
    badgeDark: 'dark:bg-rose-950/60 dark:text-rose-300 dark:border-rose-800/60',
  },
  stress: {
    title: 'Stress Limits',
    desc: 'Scaled inputs to challenge quadratic O(N²) time',
    badgeLight: 'bg-purple-50 text-purple-800 border-purple-200',
    badgeDark: 'dark:bg-purple-950/60 dark:text-purple-300 dark:border-purple-800/60',
  },
  basic: {
    title: 'Baseline Examples',
    desc: 'Curated public examples and sanity cases',
    badgeLight: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    badgeDark: 'dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800/60',
  },
};

export const TestCaseList: React.FC<TestCaseListProps> = ({
  testCases,
  rawBatchInput,
  limitations,
}) => {
  if (testCases.length === 0) {
    return null;
  }

  // Active category filter tab for the Master Aggregated Box: 'all' or specific category
  const [activeTab, setActiveTab] = useState<string>('all');
  const [masterCopied, setMasterCopied] = useState<boolean>(false);

  // Group cases by category
  const groupedCases = useMemo(() => {
    const map: Record<string, TestCase[]> = {};
    testCases.forEach((tc) => {
      const cat = tc.category || 'basic';
      if (!map[cat]) map[cat] = [];
      map[cat].push(tc);
    });
    return map;
  }, [testCases]);

  const categories = Object.keys(groupedCases);

  // Compute text content for the Master Box based on active tab
  const displayedCases = useMemo(() => {
    if (activeTab === 'all') return testCases;
    return groupedCases[activeTab] || [];
  }, [activeTab, testCases, groupedCases]);

  const displayedRawInput = useMemo(() => {
    if (activeTab === 'all') return rawBatchInput;
    return displayedCases.map((c) => c.raw_input).join('\n');
  }, [activeTab, rawBatchInput, displayedCases]);

  // Master One-Click Copy Handler
  const handleMasterCopy = async () => {
    try {
      await navigator.clipboard.writeText(displayedRawInput);
      setMasterCopied(true);
      setTimeout(() => setMasterCopied(false), 2200);
    } catch (e) {
      console.error('Copy failed:', e);
    }
  };

  const lineCount = displayedRawInput.split('\n').filter((l) => l.trim().length > 0).length;

  return (
    <div className="space-y-8">
      {/* =========================================================================
          MASTER AGGREGATED TEST CASE BOX (PLACED DIRECTLY ABOVE ALL INDIVIDUAL CARDS)
          Contains all generated test cases together in one box for 1-click paste
          ========================================================================= */}
      <div className="theme-card rounded-2xl border-2 border-blue-500/40 dark:border-orange-500/40 overflow-hidden shadow-lg transition-colors">
        {/* Master Box Header */}
        <div className="p-4 sm:p-5 bg-gradient-to-r from-blue-50/80 via-white to-blue-50/40 dark:from-orange-950/40 dark:via-[#0b101d] dark:to-[#070b16] border-b border-slate-200 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex flex-wrap items-center gap-2">
              <div className="p-1.5 rounded-lg bg-blue-600 text-white dark:bg-orange-500 shadow-sm">
                <Terminal className="w-4 h-4" />
              </div>
              <h3 className="font-extrabold text-base sm:text-lg text-slate-900 dark:text-white">
                LeetCode Custom Testcase Master Box
              </h3>
              <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700 dark:bg-orange-950 dark:text-orange-300 border border-blue-200 dark:border-orange-800">
                {displayedCases.length} Cases Aggregated
              </span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              All test cases generated together in one box. Click once to copy and paste directly into LeetCode's custom testcase runner.
            </p>
          </div>

          {/* Master 1-Click Paste / Copy Button */}
          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={handleMasterCopy}
              className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs sm:text-sm tracking-wide shadow-md transition-all active:scale-95 ${
                masterCopied
                  ? 'bg-emerald-600 text-white'
                  : 'bg-blue-600 hover:bg-blue-700 text-white shadow-blue-500/20 dark:bg-orange-500 dark:hover:bg-orange-600 dark:text-white dark:shadow-orange-500/30'
              }`}
            >
              {masterCopied ? (
                <>
                  <Check className="w-4 h-4 stroke-[3]" />
                  <span>Copied {displayedCases.length} Cases to Clipboard!</span>
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  <span>One-Click Copy {activeTab === 'all' ? `All (${displayedCases.length})` : activeTab.replace('_', ' ')} for LeetCode</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Category Type Filter Tabs (Switch what is displayed together inside the box) */}
        <div className="px-4 py-2.5 bg-slate-100/70 dark:bg-[#070b16] border-b border-slate-200 dark:border-slate-800/80 flex flex-wrap items-center gap-2">
          <span className="text-xs font-bold text-slate-500 dark:text-slate-400 flex items-center gap-1 mr-1">
            <Layers className="w-3.5 h-3.5 text-blue-600 dark:text-orange-400" /> Filter Types:
          </span>

          {/* 'All Types' Tab */}
          <button
            onClick={() => setActiveTab('all')}
            className={`text-xs px-3 py-1 rounded-lg font-bold transition-all ${
              activeTab === 'all'
                ? 'bg-blue-600 text-white shadow-sm dark:bg-orange-500 dark:text-white'
                : 'bg-white hover:bg-slate-200 text-slate-700 border border-slate-200 dark:bg-slate-900/80 dark:text-slate-300 dark:border-slate-800 dark:hover:bg-slate-800'
            }`}
          >
            All Types ({testCases.length})
          </button>

          {/* Individual Category Tabs */}
          {categories.map((cat) => {
            const count = groupedCases[cat].length;
            const meta = CATEGORY_META[cat];
            const isActive = activeTab === cat;
            return (
              <button
                key={cat}
                onClick={() => setActiveTab(cat)}
                className={`text-xs px-2.5 py-1 rounded-lg font-semibold transition-all ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-sm dark:bg-orange-500 dark:text-white'
                    : 'bg-white hover:bg-slate-200 text-slate-700 border border-slate-200 dark:bg-slate-900/80 dark:text-slate-300 dark:border-slate-800 dark:hover:bg-slate-800'
                }`}
              >
                {meta ? meta.title : cat} ({count})
              </button>
            );
          })}
        </div>

        {/* Unified Test Case Raw Text Box (The actual box containing the cases together) */}
        <div className="p-4 sm:p-5 bg-white dark:bg-[#050811] space-y-3">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-mono">
            <span>
              Showing {displayedCases.length} {displayedCases.length === 1 ? 'case' : 'cases'} &bull; {lineCount} argument lines
            </span>
            <span className="text-[11px] font-sans">
              Matches LeetCode multi-line parameter format
            </span>
          </div>

          <div className="relative rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#070b16] p-4 font-mono text-xs text-slate-900 dark:text-orange-200 overflow-x-auto shadow-inner max-h-72 overflow-y-auto">
            <pre className="whitespace-pre-wrap leading-relaxed select-all">
              {displayedRawInput}
            </pre>
          </div>
        </div>
      </div>

      {/* Limitations Notice if present */}
      {limitations && (
        <div className="flex items-start gap-2.5 p-3.5 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 text-xs text-amber-800 dark:text-amber-200">
          <AlertCircle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
          <span>{limitations}</span>
        </div>
      )}

      {/* =========================================================================
          INDIVIDUAL TEST CASE CARDS (DESCRIBING TIER TYPES & DETAILS FOR EACH CASE)
          ========================================================================= */}
      <div className="space-y-4 pt-2">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
          <div>
            <h4 className="font-extrabold text-base text-slate-900 dark:text-white flex items-center gap-2">
              <FileText className="w-4 h-4 text-blue-600 dark:text-orange-400" />
              Individual Test Case Diagnostic Breakdown ({testCases.length} Cases)
            </h4>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Detailed failure modes, synthesis rationale, and verification status for each individual test case.
            </p>
          </div>
        </div>

        {/* Grid of Individual Test Case Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {testCases.map((tc, idx) => (
            <TestCaseCard
              key={tc.id || idx}
              testCase={tc}
              index={idx}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
