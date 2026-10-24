import {
  GenerateRequest,
  GenerateResponse,
  PaginatedResponse,
  ProblemDetail,
  ProblemSummary
} from '../types/api';

const API_BASE = '/api/v1';

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorData;
    try {
      errorData = await res.json();
    } catch {
      throw new Error(`HTTP Error ${res.status}: ${res.statusText}`);
    }
    const message = errorData?.error?.message || errorData?.detail || `Request failed with status ${res.status}`;
    const code = errorData?.error?.code || 'UNKNOWN_ERROR';
    const error: any = new Error(message);
    error.code = code;
    error.details = errorData?.error?.details;
    throw error;
  }
  return res.json();
}

export const apiClient = {
  async searchProblems(
    query?: string,
    difficulty?: string,
    limit: number = 20,
    offset: number = 0
  ): Promise<PaginatedResponse<ProblemSummary>> {
    const params = new URLSearchParams();
    if (query) params.append('query', query);
    if (difficulty) params.append('difficulty', difficulty);
    params.append('limit', limit.toString());
    params.append('offset', offset.toString());

    const res = await fetch(`${API_BASE}/problems?${params.toString()}`);
    return handleResponse<PaginatedResponse<ProblemSummary>>(res);
  },

  async getProblem(slug: string): Promise<ProblemDetail> {
    const res = await fetch(`${API_BASE}/problems/${encodeURIComponent(slug)}`);
    return handleResponse<ProblemDetail>(res);
  },

  async generateTestCases(slug: string, req: GenerateRequest): Promise<GenerateResponse> {
    const res = await fetch(`${API_BASE}/problems/${encodeURIComponent(slug)}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(req),
    });
    return handleResponse<GenerateResponse>(res);
  },

  async checkHealth(): Promise<{ status: string; database: string }> {
    const res = await fetch(`${API_BASE}/health`);
    return handleResponse<{ status: string; database: string }>(res);
  }
};
