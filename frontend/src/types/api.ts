export type Difficulty = 'EASY' | 'MEDIUM' | 'HARD';
export type SupportStatus = 'SUPPORTED' | 'PARTIAL' | 'UNSUPPORTED_FORMAT';

export type Category = 
  | 'basic'
  | 'boundary'
  | 'structural'
  | 'numeric_extremes'
  | 'stress';

export interface TestCase {
  id: string;
  category: Category;
  raw_input: string;
  explanation: string;
  generation_method: string;
  validation_status: string;
  expected_output: string | null;
  verification_status: 'VERIFIED' | 'UNVERIFIED' | 'NOT_APPLICABLE';
  comparison_mode?: string;
}

export interface ProblemSummary {
  id: string;
  source: string;
  source_id: number;
  slug: string;
  title: string;
  difficulty: Difficulty;
  support_status: SupportStatus;
  constraints_count: number;
  test_cases_count: number;
}

export interface ProblemDetail {
  id: string;
  source: string;
  source_id: number;
  slug: string;
  title: string;
  difficulty: Difficulty;
  content: string;
  constraints: string[];
  input_schema: Array<{ name: string; type: string }>;
  support_status: SupportStatus;
  example_test_cases: TestCase[];
  created_at: string;
  updated_at: string;
}

export interface GenerateRequest {
  count: number;
  categories: Category[];
  seed?: number;
}

export interface GenerateResponse {
  problem_slug: string;
  requested_count: number;
  returned_count: number;
  seed: number;
  test_cases: TestCase[];
  raw_batch_input: string;
  limitations?: string | null;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  offset: number;
  limit: number;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
}
