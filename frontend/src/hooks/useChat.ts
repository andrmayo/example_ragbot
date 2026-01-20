import { useState } from "react";
import { askQuestion, type AnswerResponse } from "../api/client";

export interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
}

interface UseChatReturn {
  messages: Message[];
  loading: boolean;
  error: string | null;
  ask: (question: string) => Promise<void>;
  clearMessages: () => void;
}

export function useChat(collection: string): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function ask(question: string) {
    setError(null);
    setLoading(true);

    // Add user message immediately
    setMessages((prev) => [...prev, { role: "user", content: question }]);

    try {
      const response: AnswerResponse = await askQuestion(question, collection);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.answer,
          sources: response.sources,
        },
      ]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  function clearMessages() {
    setMessages([]);
  }

  return { messages, loading, error, ask, clearMessages };
}
