import { useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import LessonView from "./components/LessonView";
import TestView from "./components/TestView";
import SimulationView from "./components/SimulationView";
import ResultView from "./components/ResultView";
import ProgressView from "./components/ProgressView";
import { ErrorBoundary } from "./components/ErrorBoundary";

type View =
  | "login"
  | "dashboard"
  | "lesson"
  | "test"
  | "simulation"
  | "result"
  | "progress";

interface Lesson {
  id: number;
  title: string;
  has_test: boolean;
  has_simulation: boolean;
}

function App() {
  const [view, setView] = useState<View>("login");
  const [currentLesson, setCurrentLesson] = useState<Lesson | null>(null);
  const [simulationIdForResult, setSimulationIdForResult] = useState<number | null>(null);

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-50">
        {view === "login" && (
          <Login onLogin={() => setView("dashboard")} />
        )}

        {view === "dashboard" && (
          <Dashboard
            onLogout={() => setView("login")}
            onLessonClick={(lesson) => {
              setCurrentLesson(lesson);
              setView("lesson");
            }}
            onProgressClick={() => setView("progress")}
          />
        )}

        {view === "lesson" && currentLesson && (
          <LessonView
            lesson={currentLesson}
            onBack={() => setView("dashboard")}
            onTestClick={(_testId) => {
              setView("test");
            }}
            onSimulationClick={(_scenarioId, _personaId) => {
              setView("simulation");
            }}
          />
        )}

        {view === "test" && currentLesson && (
          <TestView
            testId={1}
            onBack={() => setView("lesson")}
            onComplete={() => setView("lesson")}
          />
        )}

        {view === "simulation" && (
          <SimulationView
            personaId={null}
            scenarioId={null}
            onBack={() => setView("lesson")}
            onFinish={(simId: number) => {
              setSimulationIdForResult(simId);
              setView("result");
            }}
          />
        )}

        {view === "result" && simulationIdForResult && (
          <ResultView
            simulationId={simulationIdForResult}
            onBack={() => {
              setView("dashboard");
              setSimulationIdForResult(null);
            }}
          />
        )}

        {view === "progress" && (
          <ProgressView onBack={() => setView("dashboard")} />
        )}
      </div>
    </ErrorBoundary>
  );
}

export default App;