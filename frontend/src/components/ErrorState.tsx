import React from 'react';
import { AlertOctagon, HelpCircle, RefreshCw } from 'lucide-react';

interface ErrorStateProps {
  error: {
    message: string;
    code?: string;
  };
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ error, onRetry }) => {
  const isUnsupported = error.code === 'UNSUPPORTED_FORMAT';

  return (
    <div className="rounded-2xl p-6 border border-rose-200 dark:border-rose-900/60 bg-rose-50/80 dark:bg-rose-950/30 text-slate-800 dark:text-slate-200 space-y-4 shadow-sm">
      <div className="flex items-start gap-3">
        <AlertOctagon className="w-5 h-5 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <h4 className="font-bold text-sm text-rose-900 dark:text-rose-200">
            {isUnsupported ? 'Unsupported Problem Format' : 'Execution Error'}
          </h4>
          <p className="text-xs text-rose-700 dark:text-rose-300 leading-relaxed font-medium">
            {error.message}
          </p>
        </div>
      </div>

      {isUnsupported && (
        <div className="text-xs text-slate-600 dark:text-slate-400 bg-white dark:bg-[#070b16] p-3.5 rounded-xl border border-rose-100 dark:border-slate-800 space-y-1.5">
          <div className="flex items-center gap-1.5 font-bold text-slate-800 dark:text-slate-200">
            <HelpCircle className="w-3.5 h-3.5 text-blue-600 dark:text-orange-400" />
            Why is this problem format unsupported?
          </div>
          <p className="leading-relaxed">
            ThrewTLE currently synthesizes deterministic edge-cases for array, primitive numeric, string, and matrix arguments. Pointer-based structures like TreeNode (binary trees) and ListNode (linked lists) require dedicated node serializations slated for subsequent milestones.
          </p>
        </div>
      )}

      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-rose-100 hover:bg-rose-200 dark:bg-rose-900/40 dark:hover:bg-rose-800/50 text-rose-800 dark:text-rose-200 border border-rose-200 dark:border-rose-800/40 transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Retry
        </button>
      )}
    </div>
  );
};
