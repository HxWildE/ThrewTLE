import { useState } from 'react';
import { apiClient } from '../api/client';
import { Category, GenerateResponse, TestCase } from '../types/api';

export function useTestCases(slug: string | null) {
  const [testCases, setTestCases] = useState<TestCase[]>([]);
  const [rawBatchInput, setRawBatchInput] = useState<string>('');
  const [limitations, setLimitations] = useState<string | null>(null);
  const [generating, setGenerating] = useState<boolean>(false);
  const [error, setError] = useState<{ message: string; code?: string } | null>(null);

  const generate = async (count: number, categories: Category[], seed: number = 42) => {
    if (!slug) return;
    setGenerating(true);
    setError(null);

    try {
      const response: GenerateResponse = await apiClient.generateTestCases(slug, {
        count,
        categories,
        seed
      });
      setTestCases(response.test_cases);
      setRawBatchInput(response.raw_batch_input);
      setLimitations(response.limitations || null);
    } catch (err: any) {
      setError({
        message: err.message || 'Generation failed',
        code: err.code
      });
    } finally {
      setGenerating(false);
    }
  };

  const clear = () => {
    setTestCases([]);
    setRawBatchInput('');
    setLimitations(null);
    setError(null);
  };

  return {
    testCases,
    rawBatchInput,
    limitations,
    generating,
    error,
    generate,
    clear,
    setTestCases
  };
}
