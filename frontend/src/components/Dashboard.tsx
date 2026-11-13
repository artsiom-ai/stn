import { useEffect, useState } from "react";
import { api, authToken } from "../api";
import EmptyState from "./EmptyState";
import Loading from "./Loading";

interface Lesson {
  id: number;
  module_code: string;
  module_title: string;
  lesson_code: string;
  title: string;
  short_description: string;
  difficulty: string;
  is_completed: boolean;
  has_test: boolean;
  has_simulation: boolean;
}

export default function Dashboard({
  onLogout,
  onLessonClick,
  onProgressClick,
}: {
  onLogout: () => void;
  onLessonClick: (lesson: Lesson) => void;
  onProgressClick: () => void;
}) {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/api/lessons")
      .then((res) => {
        setLessons(res.data);
        setLoading(false);
      })
      .catch((err) => {
        setError("Не удалось загрузить уроки");
        setLoading(false);
        console.error(err);
      });
  }, []);

  const difficultyLabel = (d: string) => {
    switch (d) {
      case "easy": return "Легко";
      case "medium": return "Средне";
      case "hard": return "Сложно";
      default: return d;
    }
  };

  const difficultyBadge = (d: string) => {
    switch (d) {
      case "easy": return "bg-green-100 text-green-700";
      case "medium": return "bg-yellow-100 text-yellow-700";
      case "hard": return "bg-red-100 text-red-700";
      default: return "bg-gray-100 text-gray-700";
    }
  };

  if (loading) {
    return <Loading />;
  }

  const content = (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="text-xl font-bold text-gray-900">SalesLab</span>
            <span className="text-sm text-gray-500">Trainer</span>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={onProgressClick}
              className="px-4 py-2 text-sm text-blue-600 hover:text-blue-800"
            >
              Прогресс
            </button>
            <button
              onClick={onLogout}
              className="px-4 py-2 text-sm text-red-600 hover:text-red-800"
            >
              Выход
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {error || lessons.length === 0 ? (
          <EmptyState
            title={error || "Уроки не найдены"}
            description={
              error
                ? "Попробуйте обновить страницу или обратитесь к наставнику."
                : "Скоро здесь появятся уроки для тренировки продаж."
            }
            action={
              <button
                onClick={() => window.location.reload()}
                className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Обновить страницу
              </button>
            }
          />
        ) : (
          <>
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-900">Мои уроки</h1>
              <p className="text-gray-600">Выберите урок для начала обучения</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {lessons.map((lesson) => (
                <div
                  key={lesson.id}
                  className={`bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <span className={`text-xs font-medium px-2 py-1 rounded ${difficultyBadge(lesson.difficulty)}`}>
                      {difficultyLabel(lesson.difficulty)}
                    </span>
                    {lesson.is_completed && (
                      <span className="text-green-600 text-xs">✓ Завершён</span>
                    )}
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
                    {lesson.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4">
                    {lesson.short_description}
                  </p>
                  <div className="flex gap-2 text-xs text-gray-500 mb-4">
                    <span>{lesson.module_title}</span>
                    {lesson.has_test && <span>• Тест</span>}
                    {lesson.has_simulation && <span>• Симуляция</span>}
                  </div>
                  <button
                    onClick={() => onLessonClick(lesson)}
                    disabled={!authToken}
                    className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-300"
                  >
                    Открыть урок
                  </button>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );

  return content;
}