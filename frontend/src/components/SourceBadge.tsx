interface SourceBadgeProps {
  filename: string;
}

export function SourceBadge({ filename }: SourceBadgeProps) {
  return (
    <span className="inline-block px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
      {filename}
    </span>
  );
}
