interface DomainCardProps {
  name: string;
  teamSize: string;
  focus: string[];
  status: 'Activo' | 'Planificado';
}

export function DomainCard({ name, teamSize, focus, status }: DomainCardProps) {
  return (
    <article className="domain-card">
      <div>
        <strong>{name}</strong>
        <p>{teamSize}</p>
        <div className="chip-list">
          <span className="chip">{status}</span>
        </div>
      </div>
      <ul>
        {focus.map((item) => (
          <li key={item}>• {item}</li>
        ))}
      </ul>
    </article>
  );
}
