import React, { useState } from 'react';
import { Check, Copy } from 'lucide-react';

interface CopyButtonProps {
  text: string;
  label?: string;
  className?: string;
  variant?: 'primary' | 'secondary' | 'category' | 'icon';
}

export const CopyButton: React.FC<CopyButtonProps> = ({
  text,
  label = 'Copy',
  className = '',
  variant = 'secondary'
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async (e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy to clipboard:', err);
    }
  };

  if (variant === 'icon') {
    return (
      <button
        onClick={handleCopy}
        title={copied ? 'Copied to clipboard!' : 'Copy raw input'}
        className={`p-1.5 rounded-md text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-orange-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors ${className}`}
        aria-label="Copy code"
      >
        {copied ? <Check className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> : <Copy className="w-4 h-4" />}
      </button>
    );
  }

  const baseStyles = "inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-150 active:scale-95";
  
  const variants = {
    primary: "bg-blue-600 hover:bg-blue-700 text-white shadow-md shadow-blue-500/20 dark:bg-orange-500 dark:hover:bg-orange-600 dark:text-white dark:shadow-orange-500/30",
    category: "bg-blue-50 text-blue-700 border border-blue-200 hover:bg-blue-100 dark:bg-orange-950/60 dark:text-orange-300 dark:border-orange-800/60 dark:hover:bg-orange-900/60 shadow-sm",
    secondary: "bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 dark:bg-slate-800/90 dark:hover:bg-slate-700 dark:text-slate-200 dark:border-slate-700",
  };

  return (
    <button
      onClick={handleCopy}
      className={`${baseStyles} ${variants[variant]} ${className}`}
    >
      {copied ? (
        <>
          <Check className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
          <span className="text-emerald-700 dark:text-emerald-300 font-bold">Copied!</span>
        </>
      ) : (
        <>
          <Copy className="w-3.5 h-3.5" />
          <span>{label}</span>
        </>
      )}
    </button>
  );
};
