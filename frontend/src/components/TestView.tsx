import { useEffect, useState } from "react";
import { api } from "../api";

interface Question {
  id: number;
  question_text: string;
  question_type: string;
  options: string[];
  order_index: number;
}

interface TestData {
  id: number;
  title: string;
  questions: Question[];
}

export default function TestView({
  testId,
  onBack,
  onComplete,
}: {
  testId: number;
  onBack: () => void;
  onComplete: (result: { score: number; passed: boolean }) => void;
}) {
  const [test, setTest] = useState<TestData | null>(null);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState<{ score: number; passed: boolean } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get(`/api/tests/${testId}`)
      .then((res) => {
        setTest(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [testId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const answerList = Object.entries(answers).map(([questionId, selectedAnswer]) => ({
      question_id: parseInt(questionId),
      selected_answer: selectedAnswer,
    }));

    try {
      const res = await api.post(`/api/tests/${testId}/attempt`, {
        answers: answerList,
      });
      setResult({
        score: res.data.score,
        passed: res.data.passed,
      });
      setSubmitted(true);
    } catch (err) {
      console.error(err);
    }
  };

  if (!test) return null;

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <nav className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          ← Назад к уроку
        </button>
        <div className="text-sm text-gray-500">Тест</div>
      </nav>

      <div className="max-w-2xl mx-auto py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">{test.title}</h1>

        {submitted && result ? (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              Результат теста
            </h2>
            <div className={`text-2xl font-bold mb-4 ${
              result.passed ? "text-green-600" : "text-red-600"
            }`}>
              {result.passed ? "Зачёт" : "Не зачёт"}
            </div>
            <div className="text-gray-600">
              Правильных ответов: {result.score} из {test.questions.length}
            </div>
            <button
              onClick={() => onComplete(result)}
              className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
                            К уроку
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            {test.questions.map((q) => (
              <div key={q.id} className="mb-6">
                <p className="font-medium text-gray-900 mb-3">
                  {q.order_index}. {q.question_text}
                </p>
                {q.options.map((opt, i) => (
                  <label key={i} className="block">
                    <input
                      type="radio"
                      name={`q_${q.id}`}
                      value={opt}
                      checked={answers[q.id] === opt}
                      onChange={(e) =>
                        setAnswers({ ...answers, [q.id]: e.target.value })
                      }
                      className="mr-2 text-blue-600 focus:ring-blue-500"
                    />
                    {opt}
                  </label>
                ))}
              </div>
            ))}
            <button
              type="submit"
              className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-blue-300"
              disabled={Object.keys(answers).length !== test.questions.length}
            >
              Завершить тест
            </button>
            <p className="mt-3 text-sm text-gray-500">
              Ответьте на все вопросы, чтобы завершить
            </p>
          </form>
        )}
      </div>
    </div>
  );
}