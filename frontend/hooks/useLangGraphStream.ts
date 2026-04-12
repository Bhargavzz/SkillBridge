"use client";

import { useCallback, useRef, useState } from "react";
import type { AgentStreamEvent, AnalysisRequest, AnalysisResponse } from "@/types/api";

interface StreamState {
  isStreaming: boolean;
  result: Partial<AnalysisResponse>;
  error: string | null;
}

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export function useLangGraphStream() {
  const [state, setState] = useState<StreamState>({
    isStreaming: false,
    result: {},
    error: null,
  });
  const eventSourceRef = useRef<EventSource | null>(null);

  const startStream = useCallback((payload: AnalysisRequest) => {
    eventSourceRef.current?.close();

    setState({ isStreaming: true, result: {}, error: null });

    const params = new URLSearchParams({
      resume_text: payload.resume_text,
      github_url: payload.github_url,
      target_role: payload.target_role,
    });

    const source = new EventSource(`${BASE_URL}/analysis/stream?${params.toString()}`);
    eventSourceRef.current = source;

    source.onmessage = (event: MessageEvent<string>) => {
      const parsed: AgentStreamEvent = JSON.parse(event.data);

      setState((prev) => {
        switch (parsed.type) {
          case "profile":
            return { ...prev, result: { ...prev.result, profile_summary: parsed.data } };
          case "gap":
            return { ...prev, result: { ...prev.result, gap_analysis: parsed.data } };
          case "roadmap":
            return { ...prev, result: { ...prev.result, roadmap: parsed.data } };
          case "critic":
            return { ...prev, result: { ...prev.result, critic_feedback: parsed.data } };
          case "error":
            return { ...prev, isStreaming: false, error: parsed.data };
          default:
            return prev;
        }
      });
    };

    source.onerror = () => {
      setState((prev) => ({
        ...prev,
        isStreaming: false,
        error: "Stream connection lost.",
      }));
      source.close();
    };

    source.addEventListener("done", () => {
      setState((prev) => ({ ...prev, isStreaming: false }));
      source.close();
    });
  }, []);

  const stopStream = useCallback(() => {
    eventSourceRef.current?.close();
    setState((prev) => ({ ...prev, isStreaming: false }));
  }, []);

  return { ...state, startStream, stopStream };
}
