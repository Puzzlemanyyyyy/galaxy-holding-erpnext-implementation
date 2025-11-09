interface TimelineItem {
  title: string;
  description: string;
}

interface TimelineProps {
  items: TimelineItem[];
}

export function Timeline({ items }: TimelineProps) {
  return (
    <div className="timeline">
      {items.map((item) => (
        <div className="timeline-item" key={item.title}>
          <span className="timeline-marker" aria-hidden="true" />
          <div className="timeline-content">
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
