import { useEffect, useState } from "react";
import { api } from "../api";

interface Skill {
  name: string;
  level: number;
  description: string;
}

interface ProgressData {
  skills: Skill[];
  weak_skill: string;
  frequent_mistake: string;
  recommended_training: {
    skill: string;
    level: number;
    action: string;
  };
}

export default function ProgressView({
  onBack,
}: {
  onBack: () => void;
}) {
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [mistakes, setMistakes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get("/api/progress"), api.get("/api/mistakes")])
      .then(([progRes, mistakesRes]) => {
        setProgress(progRes.data);
        setMistakes(mistakesRes.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading || !progress) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <nav className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          ← Назад к урокам
        </button>
        <div className="text-sm font-medium text-gray-900">Прогресс</div>
      </nav>

      <div className="max-w-3xl mx-auto py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Ваш прогресс</h1>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Слабое место
          </h2>
          <div className="flex items-center gap-4">
            <div className="text-2xl font-bold text-red-600">
              {progress.weak_skill || "—"}
            </div>
            <div className="text-gray-600">
              {progress.recommended_training.action}
            </div>
          </div>
        </div>

        {progress.frequent_mistake && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Частая ошибка
            </h2>
            <p className="text-gray-600">{progress.frequent_mistake}</p>
          </div>
        )}

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Навыки</h2>
          <div className="space-y-3">
            {progress.skills?.map((skill, i) => (
              <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded border border-gray-100">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-900">{skill.name}</span>
                    <span className={`text-xs font-medium px-2 py-0.5 rounded ${
                      skill.level >= 70
                        ? "bg-green-100 text-green-700"
                        : skill.level >= 40
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-red-100 text-red-700"
                    }`}>
                      {skill.level}%
                    </span>
                  </div>
                  <p className="text-xs text-gray-500">{skill.description}</p>
                </div>
                <div className="w-48 bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      skill.level >= 70
                        ? "bg-green-500"
                        : skill.level >= 40
                        ? "bg-yellow-500"
                        : "bg-red-500"
                    }`}
                    style={{ width: `${Math.max(skill.level, 0)}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-100 rounded-lg p-6 mb-6">
          <h2 className="text-lg font-semibold text-blue-900 mb-2">
            Рекомендация дня
          </h2>
          <p className="text-blue-700">{progress.recommended_training.action}</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Журнал ошибок
          </h2>
          <div className="space-y-3">
            {mistakes.map((m, i) => (
              <div key={i} className="p-3 bg-amber-50 border border-amber-100 rounded">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{m.skill}</p>
                    <p className="text-sm text-gray-600">{m.description}</p>
                    <span className="text-xs text-amber-600">{m.mistake_type}</span>
                  </div>
                  <span className="text-xs text-gray-400">
                    {m.last_seen_at ? new Date(m.last_seen_at).toLocaleDateString("ru-RU") : ""}
                  </span>
                </div>
              </div>
            ))}
            {mistakes.length === 0 && (
              <p className="text-gray-400 text-sm">Ошибок не зарегистрировано</p>
            )}
          </div>
        </div>

        <div className="mt-6">
          <button
            onClick={onBack}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Вернуться к урокам
          </button>
        </div>
      </div>
    </div>
  );
}