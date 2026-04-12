import type { RoadmapStep } from "@/types/api";
import { cn } from "@/lib/utils";

interface RoadmapCardProps {
  step: RoadmapStep;
  index: number;
}

function RoadmapCard({ step, index }: RoadmapCardProps) {
  return (
    <div className={cn("rounded-lg border p-4 shadow-sm", "bg-card text-card-foreground")}>
      <div className="flex items-center gap-3">
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-semibold">
          {index + 1}
        </span>
        <h3 className="font-semibold">{step.title}</h3>
        <span className="ml-auto text-xs text-muted-foreground">
          {step.duration_weeks}w
        </span>
      </div>
      <p className="mt-2 text-sm text-muted-foreground">{step.description}</p>
      {step.resources.length > 0 && (
        <ul className="mt-3 space-y-1">
          {step.resources.map((resource) => (
            <li key={resource} className="text-xs text-blue-600 underline truncate">
              {resource}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

interface RoadmapDisplayProps {
  steps: RoadmapStep[];
}

export function RoadmapDisplay({ steps }: RoadmapDisplayProps) {
  if (steps.length === 0) return null;

  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-bold tracking-tight">Your Learning Roadmap</h2>
      <div className="grid gap-4 md:grid-cols-2">
        {steps.map((step, i) => (
          <RoadmapCard key={step.title} step={step} index={i} />
        ))}
      </div>
    </section>
  );
}
