import React, { useState } from 'react';
import { 
  CheckCircle2, 
  ChevronDown, 
  ChevronUp, 
  Code2, 
  ExternalLink, 
  FileText, 
  ListOrdered, 
  ShieldAlert, 
  Sliders 
} from 'lucide-react';
import { ProblemDetail } from '../types/api';

interface ProblemCardProps {
  problem: ProblemDetail;
}

export const ProblemCard: React.FC<ProblemCardProps> = ({ problem }) => {
  const [showFullDesc, setShowFullDesc] = useState(false);
  const [showExamples, setShowExamples] = useState(false);

  const getDifficultyBadge = (diff: string) => {
    switch (diff?.toUpperCase()) {
      case 'EASY':
        return 'text-emerald-700 bg-emerald-50 border-emerald-200 dark:text-emerald-400 dark:bg-emerald-950/60 dark:border-emerald-800/40';
      case 'MEDIUM':
        return 'text-amber-700 bg-amber-50 border-amber-200 dark:text-amber-400 dark:bg-amber-950/60 dark:border-amber-800/40';
      case 'HARD':
        return 'text-rose-700 bg-rose-50 border-rose-200 dark:text-rose-400 dark:bg-rose-950/60 dark:border-rose-800/40';
      default:
        return 'text-slate-700 bg-slate-100 border-slate-300 dark:text-slate-400 dark:bg-slate-800 dark:border-slate-700';
    }
  };

  const isUnsupported = problem.support_status === 'UNSUPPORTED_FORMAT';

  // Format problem statement cleanly (strip HTML tags, separate paragraphs)
  const formatContent = (content: string) => {
    if (!content) return [];
    // Strip HTML tags like <p>, <code>, <strong> etc.
    const clean = content
      .replace(/<[^>]*>/g, ' ')
      .replace(/&nbsp;/g, ' ')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&amp;/g, '&');
    
    // Split into paragraphs
    return clean
      .split('\n')
      .map((p) => p.trim())
      .filter((p) => p.length > 0);
  };

  const paragraphs = formatContent(problem.content);

  return (
    <div className="theme-card rounded-2xl p-5 sm:p-6 border shadow-lg space-y-6 transition-colors">
      {/* Top Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800/80 pb-5">
        <div className="space-y-1.5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-200 dark:bg-orange-950/80 dark:text-orange-400 dark:border-orange-800/60">
              LeetCode #{problem.source_id}
            </span>
            <span
              className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${getDifficultyBadge(
                problem.difficulty
              )}`}
            >
              {problem.difficulty}
            </span>

            {/* Support Status */}
            {isUnsupported ? (
              <span className="flex items-center gap-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-rose-50 text-rose-700 border border-rose-200 dark:bg-rose-950/60 dark:text-rose-300 dark:border-rose-800/40">
                <ShieldAlert className="w-3.5 h-3.5" />
                Unsupported Format
              </span>
            ) : (
              <span className="flex items-center gap-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 dark:bg-orange-950/60 dark:text-orange-300 dark:border-orange-800/40">
                <CheckCircle2 className="w-3.5 h-3.5 text-blue-600 dark:text-orange-400" />
                Ready for Generation
              </span>
            )}
          </div>

          <h2 className="text-xl sm:text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white pt-1">
            {problem.title}
          </h2>
        </div>

        <a
          href={`https://leetcode.com/problems/${problem.slug}/`}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-xs font-mono font-medium text-blue-600 dark:text-orange-400 hover:underline self-start sm:self-auto px-2.5 py-1 rounded-lg bg-blue-50/50 dark:bg-slate-900/60 border border-blue-100 dark:border-slate-800"
        >
          <span>leetcode.com/problems/{problem.slug}</span>
          <ExternalLink className="w-3 h-3" />
        </a>
      </div>

      {/* Structured Problem Overview */}
      <div className="space-y-3">
        <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          <FileText className="w-4 h-4 text-blue-600 dark:text-orange-400" />
          <span>Problem Statement & Overview</span>
        </div>

        <div className="rounded-xl p-4 bg-slate-50/70 dark:bg-[#070b16] border border-slate-200 dark:border-slate-800/80 space-y-2.5 text-sm text-slate-700 dark:text-slate-300 leading-relaxed font-sans">
          {paragraphs.slice(0, showFullDesc ? paragraphs.length : 2).map((para, i) => (
            <p key={i}>{para}</p>
          ))}

          {paragraphs.length > 2 && (
            <button
              onClick={() => setShowFullDesc(!showFullDesc)}
              className="mt-1 text-xs font-bold text-blue-600 dark:text-orange-400 hover:underline flex items-center gap-1 pt-1"
            >
              {showFullDesc ? (
                <>
                  Collapse Statement <ChevronUp className="w-3.5 h-3.5" />
                </>
              ) : (
                <>
                  Read Full Description ({paragraphs.length - 2} more paragraphs) <ChevronDown className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          )}
        </div>
      </div>

      {/* Grid: Structured Schema & Constraints */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Input Parameters Schema */}
        <div className="theme-card rounded-xl p-4 border space-y-2.5">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
            <Code2 className="w-4 h-4 text-blue-600 dark:text-orange-400" />
            <span>Input Parameters Schema</span>
          </div>

          <div className="space-y-2">
            {problem.input_schema.length > 0 ? (
              <div className="divide-y divide-slate-100 dark:divide-slate-800/80 text-xs">
                {problem.input_schema.map((param, idx) => (
                  <div key={idx} className="py-1.5 flex items-center justify-between font-mono">
                    <span className="font-semibold text-slate-800 dark:text-slate-200">
                      {param.name}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 dark:bg-slate-800 dark:text-orange-300 border border-blue-200 dark:border-slate-700 text-[11px]">
                      {param.type}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic">No structured parameters defined.</p>
            )}
          </div>
        </div>

        {/* Constraints */}
        <div className="theme-card rounded-xl p-4 border space-y-2.5">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
            <Sliders className="w-4 h-4 text-blue-600 dark:text-orange-400" />
            <span>Algorithmic Constraints</span>
          </div>

          <div className="space-y-1.5">
            {problem.constraints.length > 0 ? (
              <div className="flex flex-col gap-1.5">
                {problem.constraints.map((c, idx) => (
                  <div
                    key={idx}
                    className="flex items-center gap-2 text-xs font-mono px-2.5 py-1.5 rounded-lg bg-slate-50 dark:bg-[#070b16] border border-slate-200 dark:border-slate-800/80 text-slate-800 dark:text-slate-200"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500 dark:bg-orange-500 shrink-0" />
                    <span>{c}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic">No explicit constraints recorded.</p>
            )}
          </div>
        </div>
      </div>

      {/* Curated Benchmark Examples Drawer */}
      {problem.example_test_cases && problem.example_test_cases.length > 0 && (
        <div className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden">
          <button
            onClick={() => setShowExamples(!showExamples)}
            className="w-full p-3.5 bg-slate-50/80 dark:bg-slate-900/60 flex items-center justify-between text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <div className="flex items-center gap-2">
              <ListOrdered className="w-4 h-4 text-blue-600 dark:text-orange-400" />
              <span>Curated Catalogue Examples ({problem.example_test_cases.length} cases)</span>
            </div>
            {showExamples ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {showExamples && (
            <div className="p-4 bg-white dark:bg-[#0a0f1d] divide-y divide-slate-100 dark:divide-slate-800 space-y-3">
              {problem.example_test_cases.map((ex, i) => (
                <div key={i} className="pt-2 first:pt-0 space-y-1 text-xs">
                  <div className="flex items-center justify-between font-semibold text-slate-700 dark:text-slate-300">
                    <span>Example {i + 1} ({ex.category})</span>
                    {ex.expected_output && (
                      <span className="font-mono text-emerald-600 dark:text-emerald-400">
                        Expected: {ex.expected_output}
                      </span>
                    )}
                  </div>
                  <pre className="p-2 rounded bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 font-mono text-[11px] text-slate-900 dark:text-orange-200 overflow-x-auto">
                    {ex.raw_input}
                  </pre>
                  {ex.explanation && (
                    <p className="text-[11px] text-slate-500">{ex.explanation}</p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
