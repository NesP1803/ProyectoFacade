import { useState } from "react";
import { apiFacade, ProcessOrderRequest, ProcessOrderResponse } from "../api/apiFacade";

/**
 * Service/Hook layer:
 * Orchestrates UI interactions with the API facade.
 */
export function useOrderProcessor() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ProcessOrderResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const process = async (payload: ProcessOrderRequest) => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiFacade.processOrder(payload);
      console.log("[useOrderProcessor] Order processed", response);
      setResult(response);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      console.error("[useOrderProcessor] Processing failed", message);
      setError(message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return { loading, result, error, process };
}
