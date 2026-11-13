import { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  errorMessage: string;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, errorMessage: "" };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, errorMessage: error.message };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback ?? (
          <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
            <div className="max-w-md bg-white p-8 rounded-lg shadow-md text-center border border-red-100">
              <h2 className="text-xl font-bold text-red-800 mb-2">
                Что-то пошло не так
              </h2>
              <p className="text-gray-600 mb-4">{this.state.errorMessage}</p>
              <button
                onClick={() => {
                  this.setState({ hasError: false, errorMessage: "" });
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Попробовать снова
              </button>
            </div>
          </div>
        )
      );
    }
    return this.props.children;
  }
}