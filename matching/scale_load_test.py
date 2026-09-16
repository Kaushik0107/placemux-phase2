import numpy as np
import time

def execute_concurrency_load_test(target_qps: int = 600, breaking_point_qps: int = 500) -> dict:
    """
    Simulates high-concurrency load testing to identify QPS breaking points, latency degradation curves, and fallback triggers.
    """
    start_time = time.perf_counter()
    
    # Simulate latency curve exponential degradation near breaking point
    if target_qps <= breaking_point_qps:
        simulated_p95_ms = 15.0 + (target_qps / breaking_point_qps) * 20.0
        degraded = False
        fallback_active = False
    else:
        # Load exceeds system capacity -> Latency spikes & triggers fallback
        simulated_p95_ms = 180.0 + (target_qps - breaking_point_qps) * 0.8
        degraded = True
        fallback_active = True

    headroom_required_pct = max(0.0, ((target_qps - breaking_point_qps) / breaking_point_qps) * 100.0)
    
    return {
        "target_qps": target_qps,
        "breaking_point_qps": breaking_point_qps,
        "simulated_p95_latency_ms": round(simulated_p95_ms, 2),
        "system_degraded": degraded,
        "fallback_activated": fallback_active,
        "headroom_needed_percent": round(headroom_required_pct, 2),
        "fallback_mode": "RULE_BASED_PRECOMPUTE_CACHE" if fallback_active else "LIVE_ML_INFERENCE",
        "explanation": f"System capacity capped at {breaking_point_qps} QPS. At {target_qps} QPS, p95 latency reached {simulated_p95_ms:.1f}ms. " +
                       ("Graceful fallback to precomputed recommendations activated." if fallback_active else "System Operating within normal SLO bounds.")
    }

def get_horizontal_scaling_plan() -> dict:
    """
    Generates actionable autoscale, precompute, and queue-based scaling specifications for DevOps.
    """
    return {
        "scaling_architecture": {
            "target_qps_capacity": 2000,
            "autoscale_policy": "Horizontal Pod Autoscaler (HPA) CPU > 70% or QPS > 400 per pod",
            "min_replicas": 3,
            "max_replicas": 15,
            "precompute_strategy": "Pre-calculate Top 50 job matches nightly for inactive candidates",
            "fallback_mechanism": "Precomputed cache serving when latency > 100ms or queue depth > 50"
        },
        "devops_hand-off_ready": True,
        "explanation": "Scaling plan formulated: 3-15 pod HPA autoscale policy with nightly precompute fallback for high-load readiness."
    }

if __name__ == "__main__":
    print("--- CONCURRENCY LOAD TEST (WITHIN CAPACITY) ---")
    print(execute_concurrency_load_test(target_qps=400))

    print("\n--- CONCURRENCY LOAD TEST (EXCEEDING BREAKING POINT) ---")
    print(execute_concurrency_load_test(target_qps=650))

    print("\n--- HORIZONTAL SCALING PLAN ---")
    print(get_horizontal_scaling_plan())