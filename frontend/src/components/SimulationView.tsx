import { useEffect, useState, useRef } from "react";
import { api } from "../api";

interface Message {
  id: number;
  sender: "user" | "persona";
  content: string;
  created_at?: string;
}

export default function SimulationView({
  personaId,
  scenarioId,
  onBack,
  onFinish,
}: {
  personaId: number | null;
  scenarioId: number | null;
  onBack: () => void;
  onFinish: (evaluation: any) => void;
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [simulationId, setSimulationId] = useState<number | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "active" | "finished" | "limited">("idle");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Запуск симуляции при монтировании
  useEffect(() => {
    if (!personaId) return;
    setStatus("loading");
    api
      .post("/api/simulations/start", {
        persona_id: personaId,
        scenario_id: scenarioId,
        difficulty: "medium",
      })
      .then((res) => {
        setSimulationId(res.data.simulation_id);
        setMessages([
          {
            id: 0,
            sender: "persona",
            content: res.data.opening_message,
          },
        ]);
        setStatus("active");
      })
      .catch((err) => {
        console.error(err);
        setStatus("idle");
      });
  }, [personaId, scenarioId]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !simulationId) return;

    const userMessage: Message = {
      id: Date.now(),
      sender: "user",
      content: input,
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setStatus("loading");
    scrollToBottom();

    try {
      const res = await api.post(
        `/api/simulations/${simulationId}/messages`,
        { content: input }
      );

      if (res.data.status === "limited") {
        setStatus("limited");
        setMessages((prev) => [
          ...prev,
          { id: Date.now() + 1, sender: "persona", content: res.data.persona_reply },
        ]);
        return;
      }

      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: "persona", content: res.data.persona_reply },
      ]);
      setStatus("active");
    } catch (err) {
      console.error(err);
      setStatus("active");
    } finally {
      scrollToBottom();
    }
  };

  const finishSimulation = async () => {
    if (!simulationId) return;
    setStatus("loading");
    try {
      await api.post(`/api/simulations/${simulationId}/finish`);
      setStatus("finished");

      // Запускаем оценку
      await api.post(`/api/simulations/${simulationId}/evaluate`);
      onFinish(simulationId);
    } catch (err) {
      console.error(err);
      setStatus("active");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <nav className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          ← Назад к уроку
        </button>
        <div className="text-sm font-medium text-gray-900">
          Симуляция с клиентом
        </div>
      </nav>

      <div className="flex-1 overflow-hidden">
        <div className="h-full overflow-y-auto p-6 space-y-4" ref={messagesEndRef}>
          {messages.map((m) => (
            <div
              key={m.id}
              className={`max-w-[80%] p-3 rounded-lg ${
                m.sender === "user"
                  ? "ml-auto bg-blue-600 text-white"
                  : "mr-auto bg-white border border-gray-200 text-gray-900"
              }`}
            >
              <p className="text-sm leading-relaxed">{m.content}</p>
              <span className={`text-xs mt-1 block ${
                m.sender === "user" ? "text-blue-100" : "text-gray-400"
              }`}>
                {m.sender === "user" ? "Вы" : "Клиент"}
              </span>
            </div>
          ))}
        </div>

        <div className="bg-white border-t border-gray-200 p-4">
          {status === "limited" && (
            <div className="mb-3 p-3 bg-amber-50 border border-amber-200 text-amber-700 rounded text-sm">
              Сессия достигла лимита сообщений. Вы можете завершить симуляцию.
            </div>
          )}
          <form onSubmit={sendMessage} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={status !== "active" && status !== "idle"}
              placeholder="Напишите сообщение..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
            />
            <button
              type="submit"
              disabled={!input.trim() || status !== "active" && status !== "idle"}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300"
            >
              Отправить
            </button>
          </form>
          <button
            onClick={finishSimulation}
            disabled={status !== "active" && status !== "limited"}
            className="mt-3 w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:bg-gray-400"
          >
            Завершить симуляцию
          </button>
        </div>
      </div>
    </div>
  );
}