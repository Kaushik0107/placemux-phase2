import time
import numpy as np

# In-memory store for live production telemetry
TELEMETRY_LOGS = []

def record_inference_telemetry(endpoint: str, latency_ms: float, is_error: bool = False):
    """
    Records real-time inference metrics from production traffic.
    """
    TELEMETRY_LOGS.append({
        "endpoint": endpoint,
        "latency_ms": latency_ms,
        "is_error": is_error,
        "timestamp": time.time()
    })

def evaluate_production_health(target_p95_ms: float = 100.0, max_error_rate: float = 0.01) -> dict:
    """
    Evaluates live production telemetry against SLAs (p95 latency and error rate).
    """
    if not TELEMETRY_LOGS:
        return {
            "status": "NO_TRAFFIC",
            "total_requests": 0,
            "explanation": "No production traffic recorded yet."
        }

    latencies = [log["latency_ms"] for log in TELEMETRY_LOGS]
    errors = [log["is_error"] for log in TELEMETRY_LOGS]

    total_requests = len(TELEMETRY_LOGS)
    p95_latency = float(np.percentile(latencies, 95))
    error_rate = sum(errors) / total_requests

    passes_p95 = p95_latency <= target_p95_ms
    passes_error_rate = error_rate <= max_error_rate

    is_healthy = passes_p95 and passes_error_rate

    return {
        "total_requests": total_requests,
        "p95_latency_ms": round(p95_latency, 2),
        "mean_latency_ms": round(float(np.mean(latencies)), 2),
        "error_rate": round(error_rate, 4),
        "health_status": "HEALTHY" if is_healthy else "UNHEALTHY_DEGRADED",
        "cutover_signoff": is_healthy,
        "explanation": f"Processed {total_requests} live requests. p95 Latency: {p95_latency:.2f}ms (target <= {target_p95_ms}ms), Error Rate: {error_rate:.2%}. " +
                       ("System healthy and ready for full production cutover." if is_healthy else "Performance degraded below SLA threshold.")
    }

if __name__ == "__main__":
    # Simulate live production traffic
    np.random.seed(42)
    for _ in range(100):
        lat = float(np.random.normal(35, 10))
        err = bool(np.random.rand() < 0.005)
        record_inference_telemetry("/api/v1/matching/jobs", max(5.0, lat), err)

    print("--- LIVE PRODUCTION MODEL MONITORING ---")
    print(evaluate_production_health())