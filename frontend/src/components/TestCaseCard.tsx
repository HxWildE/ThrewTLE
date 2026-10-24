import React from 'react';
import { AlertCircle, CheckCircle, Terminal } from 'lucide-react';
import { TestCase } from '../types/api';
import { CopyButton } from './CopyButton';

interface TestCaseCardProps {
  testCase: TestCase;
  index: number;
}

export const TestCaseCard: React.FC<TestCaseCardProps> = ({ testCase, index }) => {
  const getCategoryColor = (cat: string) => {
    switch (cat?.toLowerCase()) {
      case 'boundary':
        return 'text-amber-700 bg-amber-50 border-amber-200 dark:text-amber-400 dark:bg-amber-950/50 dark:border-amber-800/40';
      case 'structural':
        return 'text-blue-700 bg-blue-50 border-blue-200 dark:text-sky-400 dark:bg-sky-950/50 dark:border-sky-800/40';
      case 'numeric_extremes':
        return 'text-rose-700 bg-rose-50 border-rose-200 dark:text-rose-400 dark:bg-rose-950/50 dark:border-rose-800/40';
      case 'stress':
        return 'text-purple-700 bg-purple-50 border-purple-200 dark:text-purple-400 dark:bg-purple-950/50 dark:border-purple-800/40';
      case 'basic':
      default:
        return 'text-emerald-700 bg-emerald-50 border-emerald-200 dark:text-emerald-400 dark:bg-emerald-950/50 dark:border-emerald-800/40';
    }
  };

  const isVerified = testCase.verification_status === 'VERIFIED';

  return (
    <div className="theme-card rounded-xl p-4 transition-all space-y-3 relative group">
      {/* Header Bar */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="font-mono text-xs font-bold text-slate-400 dark:text-slate-500">
            Case #{index + 1}
          </span>
          <span
            className={`text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${getCategoryColor(
              testCase.category
            )}`}
          >
            {testCase.category.replace('_', ' ')}
          </span>
          <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400 uppercase px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
            {testCase.generation_method.replace('_', ' ')}
          </span>
        </div>

        {/* Verification Status Badge */}
        <div>
          {isVerified ? (
            <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 dark:text-emerald-400 dark:bg-emerald-950/40 dark:border-emerald-800/40 px-2 py-0.5 rounded-full">
              <CheckCircle className="w-3 h-3" /> Verified
            </span>
          ) : (
            <span
              title="Expected output is not verified against a reference oracle. Test input is constraint-validated."
              className="inline-flex items-center gap-1 text-[11px] font-semibold text-amber-700 bg-amber-50 border border-amber-200 dark:text-amber-400 dark:bg-amber-950/40 dark:border-amber-800/40 px-2 py-0.5 rounded-full"
            >
              <AlertCircle className="w-3 h-3" /> Input Only
            </span>
          )}
        </div>
      </div>

      {/* LeetCode Raw Code Box */}
      <div className="relative rounded-lg bg-slate-50 border border-slate-200 dark:bg-[#050811] dark:border-slate-800/90 p-3 font-mono text-xs text-slate-900 dark:text-orange-200 overflow-x-auto shadow-inner group/code">
        <div className="absolute right-2 top-2">
          <CopyButton text={testCase.raw_input} variant="icon" />
        </div>
        <pre className="pr-8 whitespace-pre-wrap leading-relaxed select-all font-mono text-[11px] sm:text-xs">
          {testCase.raw_input}
        </pre>
      </div>

      {/* Rationale / Explanation */}
      <div className="flex items-start gap-2 text-xs text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-900/40 p-2.5 rounded-lg border border-slate-200 dark:border-slate-800/60">
        <Terminal className="w-3.5 h-3.5 text-blue-600 dark:text-orange-400 mt-0.5 shrink-0" />
        <span className="leading-snug">{testCase.explanation}</span>
      </div>

      {/* Expected Output */}
      {isVerified && testCase.expected_output !== null ? (
        <div className="flex items-center justify-between text-xs font-mono px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 dark:bg-emerald-950/20 dark:border-emerald-900/30 dark:text-emerald-300">
          <span className="text-[11px] text-emerald-600 dark:text-emerald-400 font-sans font-semibold">Expected:</span>
          <span className="font-bold">{testCase.expected_output}</span>
        </div>
      ) : (
        <div className="flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400 px-3 py-1.5 rounded-lg bg-slate-50 dark:bg-slate-900/30 border border-slate-200 dark:border-slate-800/40">
          <span>Expected Output:</span>
          <span className="italic">Special Judge / Unverified</span>
        </div>
      )}
    </div>
  );
};
