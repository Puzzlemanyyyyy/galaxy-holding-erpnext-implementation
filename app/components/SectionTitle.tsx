interface SectionTitleProps {
  title: string;
  description: string;
  actionLabel?: string;
  actionHref?: string;
}

export function SectionTitle({ title, description, actionHref, actionLabel }: SectionTitleProps) {
  return (
    <div className="section-title">
      <div>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
      {actionHref && actionLabel ? (
        <a className="chip" href={actionHref} target="_blank" rel="noreferrer">
          {actionLabel}
        </a>
      ) : null}
    </div>
  );
}
