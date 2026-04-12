import type { AnalysisRequest, AnalysisResponse } from "@/types/api";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export async function runAnalysis(payload: AnalysisRequest): Promise<AnalysisResponse> {
  const res = await fetch(`${BASE_URL}/analysis/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(`Analysis request failed: ${res.statusText}`);
  }

  return res.json() as Promise<AnalysisResponse>;
}
