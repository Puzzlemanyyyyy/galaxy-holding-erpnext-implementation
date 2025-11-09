interface MetricCardProps {
  value: string;
  label: string;
  caption: string;
}

export function MetricCard({ value, label, caption }: MetricCardProps) {
  return (
    <article className="metric-card">
      <span>{value}</span>
      <h3>{label}</h3>
      <p>{caption}</p>
    </article>
  );
}
