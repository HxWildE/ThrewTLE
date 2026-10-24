import { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { ProblemDetail } from '../types/api';

export function useProblem(slug: string | null) {
  const [problem, setProblem] = useState<ProblemDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<{ message: string; code?: string } | null>(null);

  useEffect(() => {
    if (!slug) {
      setProblem(null);
      setError(null);
      return;
    }

    let isMounted = true;
    setLoading(true);
    setError(null);

    apiClient.getProblem(slug)
      .then((data) => {
        if (isMounted) {
          setProblem(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError({
            message: err.message || 'Failed to load problem details',
            code: err.code
          });
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [slug]);

  return { problem, loading, error };
}
