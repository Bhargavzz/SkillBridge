export interface AnalysisRequest {
  resume_text: string;
  github_url: string;
  target_role: string;
}

export interface RoadmapStep {
  title: string;
  description: string;
  duration_weeks: number;
  resources: string[];
}

export interface GapAnalysis {
  missing_skills: string[];
  matching_skills: string[];
  match_score: number;
}

export interface AnalysisResponse {
  profile_summary: string;
  gap_analysis: GapAnalysis;
  roadmap: RoadmapStep[];
  critic_feedback: string;
}

export type AgentStreamEvent =
  | { type: "profile"; data: string }
  | { type: "gap"; data: GapAnalysis }
  | { type: "roadmap"; data: RoadmapStep[] }
  | { type: "critic"; data: string }
  | { type: "error"; data: string };
