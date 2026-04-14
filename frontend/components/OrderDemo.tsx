import React from "react";
import { useOrderProcessor } from "../hooks/useOrderProcessor";

/**
 * UI component:
 * Triggers processing by calling the hook, which calls the API facade.
 */
export function OrderDemo() {
  const { loading, result, error, process } = useOrderProcessor();

  const onProcessClick = () => {
    process({
      userId: "student01",
      email: "student01@example.com",
      productId: "p2",
      quantity: 2,
      paymentMethod: "VISA_TOKEN_123",
    });
  };

  return (
    <div style={{ fontFamily: "sans-serif", maxWidth: 500, margin: "2rem auto" }}>
      <h2>Facade Pattern Demo - E-commerce Order</h2>
      <p>
        Button click → Frontend API Facade → Backend OrderFacade → Subsystems.
      </p>

      <button onClick={onProcessClick} disabled={loading}>
        {loading ? "Processing..." : "Process Sample Order"}
      </button>

      {error && <p style={{ color: "crimson" }}>Error: {error}</p>}

      {result && (
        <div style={{ marginTop: "1rem", background: "#f7f7f7", padding: "1rem" }}>
          <strong>Response</strong>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
