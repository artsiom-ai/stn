import { ReactNode } from "react";

interface Props {
  title: string;
  description?: string;
  icon?: string;
  action?: ReactNode;
}

export default function EmptyState({
  title,
  description,
  icon = "📭",
  action,
}: Props) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
      <div className="max-w-md text-center">
        <div className="text-4xl mb-4">{icon}</div>
        <h2 className="text-xl font-bold text-gray-900 mb-2">{title}</h2>
        {description && (
          <p className="text-gray-600 mb-6">{description}</p>
        )}
        {action && <div className="justify-center">{action}</div>}
      </div>
    </div>
  );
}