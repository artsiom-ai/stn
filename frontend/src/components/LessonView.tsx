import { useEffect, useState } from "react";
import { api } from "../api";

interface LessonDetail {
  id: number;
  title: string;
  theory_markdown: string;
  skills: string[];
  test: {
    id: number;
    question_count: number;
    min_pass_score: number;
  } | null;
  simulation_scenarios: any[];
}

interface Lesson {
  id: number;
  title: string;
  has_test: boolean;
  has_simulation: boolean;
}

export default function LessonView({
  lesson,
  onBack,
  onTestClick,
  onSimulationClick,
}: {
  lesson: Lesson;
  onBack: () => void;
  onTestClick: (testId: number) => void;
  onSimulationClick: (scenarioId: number | null, personaId: number | null) => void;
}) {
  const [detail, setDetail] = useState<LessonDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get(`/api/lessons/${lesson.id}`)
      .then((res) => {
        setDetail(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [lesson.id]);

  if (loading) {
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
        <div className="text-sm text-gray-500">Урок</div>
      </nav>

      <div className="max-w-3xl mx-auto py-8">
        {detail ? (
          <>
            <h1 className="text-3xl font-bold text-gray-900 mb-6">
              {detail.title}
            </h1>

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Теория
              </h2>
              <div className="prose prose-sm max-w-none text-gray-700">
                {detail.theory_markdown
                  ? detail.theory_markdown.split("\n\n").map((para, i) => (
                      <p key={i} className="mb-4 whitespace-pre-line">
                        {para}
                      </p>
                    ))
                  : "Теория не описана"}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {detail.test && detail.test.question_count > 0 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">
                    Тест ({detail.test.question_count} вопросов)
                  </h3>
                  <p className="text-gray-600 text-sm mb-4">
                    Проходной балл: {detail.test.min_pass_score}%
                  </p>
                  <button
                    onClick={() => onTestClick(detail.test!.id)}
                    className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                  >
                    Пройти тест
                  </button>
                </div>
              )}

              {detail.simulation_scenarios && detail.simulation_scenarios.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">
                    Симуляция
                  </h3>
                  <p className="text-gray-600 text-sm mb-4">
                    Попрактикуйтесь в диалоге с ИИ-клиентом
                  </p>
                  <button
                    onClick={() =>
                      onSimulationClick(
                        detail.simulation_scenarios[0]?.id ?? null,
                        null
                      )
                    }
                    className="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                  >
                    Начать симуляцию
                  </button>
                </div>
              )}
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
}