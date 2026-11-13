import { useEffect, useState } from "react";
import { api } from "../api";

export default function ResultView({
  simulationId,
  onBack,
}: {
  simulationId: number;
  onBack: () => void;
}) {
  const [evaluation, setEvaluation] = useState<any>(null);
  const [mistakes, setMistakes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get(`/api/simulations/${simulationId}/evaluation`),
      api.get(`/api/simulations/${simulationId}/mistakes`),
    ])
      .then(([evalRes, mistakesRes]) => {
        setEvaluation(evalRes.data);
        setMistakes(mistakesRes.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [simulationId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  const scoreColor = (score: number) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-yellow-600";
    return "text-red-600";
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <nav className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          ← Назад к уроку
        </button>
        <div className="text-sm text-gray-500">Результат</div>
      </nav>

      <div className="max-w-3xl mx-auto py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          Разбор симуляции
        </h1>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">
            Итоговая оценка
          </h2>
          <div className={`text-4xl font-bold mb-2 ${scoreColor(evaluation.total_score)}`}>
            {evaluation.total_score} / 100
          </div>
          <p className="text-gray-600">{evaluation.judge_summary}</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Рубрикатор
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(evaluation.rubric || {}).map(([key, val]: any) => (
              <div key={key} className="p-4 bg-gray-50 rounded-lg border border-gray-100">
                <h4 className="text-sm font-medium text-gray-700 mb-1">
                  {key === "contact" ? "Контакт" : key === "needs" ? "Потребности" : key === "objections" ? "Возражения" : "Закрытие"}
                </h4>
                <div className="text-2xl font-bold mb-1">{val.score} / 25</div>
                <p className="text-sm text-gray-600">{val.comment}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Сильные стороны
          </h2>
          <ul className="space-y-2 text-gray-600">
            {evaluation.strengths?.map((s: string, i: number) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-green-500">✓</span>
                {s}
              </li>
            ))}
            {evaluation.strengths?.length === 0 && (
              <p className="text-gray-400 text-sm">Не указаны</p>
            )}
          </ul>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Слабые стороны
          </h2>
          <ul className="space-y-2 text-gray-600">
            {evaluation.weaknesses?.map((w: string, i: number) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-red-500">✕</span>
                {w}
              </li>
            ))}
            {evaluation.weaknesses?.length === 0 && (
              <p className="text-gray-400 text-sm">Не указаны</p>
            )}
          </ul>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Ошибки
          </h2>
          <ul className="space-y-3">
            {mistakes.map((m, i) => (
              <li key={i} className="p-3 bg-amber-50 border border-amber-100 rounded">
                <p className="text-sm font-medium text-gray-900">{m.skill}</p>
                <p className="text-sm text-gray-600">{m.description}</p>
                {m.recommendation && (
                  <p className="text-xs text-amber-700 mt-1">
                    Рекомендация: {m.recommendation}
                  </p>
                )}
              </li>
            ))}
            {mistakes.length === 0 && (
              <p className="text-gray-400 text-sm">Ошибок не выявлено</p>
            )}
          </ul>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Что тренировать дальше
          </h2>
          <ul className="space-y-2 text-gray-600">
            {evaluation.recommendations?.map((r: string, i: number) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-blue-500">→</span>
                {r}
              </li>
            ))}
            {evaluation.recommendations?.length === 0 && (
              <p className="text-gray-400 text-sm">Рекомендации не получены</p>
            )}
          </ul>
        </div>

        <div className="mt-8">
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
  }