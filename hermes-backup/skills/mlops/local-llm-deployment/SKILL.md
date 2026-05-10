---
name: local-llm-deployment
description: Guidance for deploying LLMs (Gemma, Llama, Mistral) on local hardware or VPS, focusing on performance optimization (Quantization, VRAM/RAM management).
tags: [ollama, gguf, quantization, vram, hardware-requirements, vps]
---

# Local LLM Deployment Guide

This skill provides a framework for recommending and deploying Large Language Models based on available hardware, ensuring the user achieves the "fluid" performance seen in benchmarks/videos rather than slow CPU-fallback inference.

## 1. Hardware Matrix & Model Selection

The primary bottleneck for LLM performance is **Memory Bandwidth** and **Capacity (VRAM > RAM)**.

### Local PC (GPU Accelerated)
*   **Ultra-Fast (VRAM-Resident):** Fits entirely in GPU memory.
*   **Balanced (Hybrid):** Partially in VRAM, partially in System RAM.
*   **Slow (CPU-Only):** Runs entirely on System RAM (Ollama fallback).

| Model Scale | Min VRAM (Q4_K_M) | Rec. System RAM | Performance Profile |
| :--- | :--- | :--- | :--- |
| **Small (2B - 4B)** | 4GB | 8GB | Instant, mobile/laptop friendly. |
| **Medium (7B - 9B)** | 8GB - 12GB | 16GB | High utility, standard gaming PC. |
| **Large (30B - 70B)** | 24GB - 48GB | 32GB - 64GB | High reasoning, professional workstation. |

### VPS (CPU-Only)
VPS typically lack GPUs. Performance is driven by vCPU count and RAM speed.
- **Critical:** Use the smallest possible model that fits the task (e.g., Gemma 2B) to avoid extreme latency.
- **RAM Rule:** Allocate $ModelSize + 2GB$ for OS/Overhead.

## 2. Optimization Techniques (The "Speed" Secret)

To achieve high tokens-per-second (t/s), apply these settings:

### Quantization (GGUF)
Always prefer **Q4_K_M** or **Q5_K_M**. These offer the best "Intelligence vs. Speed" trade-off. 
- **Q2/Q3:** Faster, but prone to "hallucinations" and loss of logic.
- **Q6/Q8:** Negligible quality gain over Q4, but significantly slower and heavier.

### Backend Selection
- **Nvidia:** Ensure `CUDA` is active.
- **Mac:** Ensure `Metal` acceleration is used.
- **CPU:** Ensure `AVX2` or `AVX512` instruction sets are supported by the VPS/CPU.

## 3. Deployment Workflow (Ollama)

1.  **Assess Hardware:** Check `nvidia-smi` (GPU) or `free -m` (RAM).
2.  **Select Model:** Match the scale (2B $\rightarrow$ 9B $\rightarrow$ 31B) to VRAM.
3.  **Pull & Run:** `ollama run gemma2:2b` (or specific version).
4.  **Verify Performance:** Check token generation speed. If it's < 2 t/s on a PC, check if it's falling back to CPU.

## 4. Pitfalls & Troubleshooting
- **"The model is too slow":** Likely running on CPU. Check if VRAM is full or if the model is too large for the GPU.
- **"Out of Memory (OOM)":** Reduce the context window (num_ctx) or use a more aggressive quantization (e.g., move from Q8 to Q4).
- **VPS Lag:** Avoid using "Swap" memory for LLMs; it will make the model unusable. Ensure RAM is dedicated.
