export interface ProcessOrderRequest {
  userId: string;
  email: string;
  productId: string;
  quantity: number;
  paymentMethod: string;
}

export interface ProcessOrderResponse {
  success: boolean;
  message: string;
  order_reference?: string;
  total_amount?: number;
  transaction_id?: string;
}

/**
 * Frontend Facade pattern usage:
 * Components/hooks call this class rather than using fetch directly.
 * This keeps API communication details centralized and replaceable.
 */
export class ApiFacade {
  private readonly baseUrl: string;

  constructor(baseUrl = "http://localhost:5000") {
    this.baseUrl = baseUrl;
  }

  async processOrder(payload: ProcessOrderRequest): Promise<ProcessOrderResponse> {
    console.log("[ApiFacade] Calling backend facade endpoint /process", payload);

    const response = await fetch(`${this.baseUrl}/process`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = (await response.json()) as ProcessOrderResponse;
    if (!response.ok) {
      throw new Error(data.message || "Failed to process order");
    }
    return data;
  }
}

export const apiFacade = new ApiFacade();
