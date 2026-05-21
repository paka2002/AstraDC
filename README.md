# AstraDC: AI Infrastructure Cluster Power & Thermal Optimizer

AstraDC is a full-stack AI infrastructure simulation utility designed to optimize GPU cluster energy efficiency and automate thermal management. The system processes live hardware telemetry data to detect computational hotspots and orchestrates autonomous workload balancing before hardware degradation or thermal throttling occurs.

## 📊 Core System Design & Architecture
Modern AI data centers running dense LLM training loops experience massive thermal spikes and erratic power consumption behaviors. AstraDC addresses this by creating a real-time observation loop paired with an algorithmic mitigation layer:

1. **Telemetry Capture Layer:** Built using a lightweight single-file Python server framework that maintains state arrays for distributed enterprise compute nodes (simulating H100/A100 clusters). It dynamically simulates hardware physics mappings, calculating real-time thermal responses and power draw metrics based on fluctuating GPU computation loads.
2. **Algorithmic Layer (Greedy Load-Balancer):** A greedy scheduling matrix that continuously scans the cluster telemetry grid. When a node crosses a critical thermal threshold (>= 78°C), the algorithm dynamically calculates excess compute loads and dispatches precise workload migration instructions.
3. **Target Routing Layer:** Executes the workload balance shift across node memory states, routing processing loads away from critical hotspots to the coolest available idle reservoir servers to ensure continuous uptime.
4. **Frontend Control Dashboard:** Built with a high-performance web interface styled via Tailwind CSS. It visualizes the live telemetry grid, active compute loads, thermal variations, power draw indicators, and live optimization logs.

## 💎 Key Features
* **Telemetry-Driven Orchestration:** Continuous streaming of active hardware node metrics (Load, Power, and Temperature).
* **Thermal-Aware Workload Balancing:** Automated identification of thermal hotspots with proactive relocation logic.
* **Deterministic Resource Profiling:** Physics-based simulation mapping core processing loads to realistic wattages and core temperatures.
* **One-Click Remediation Execution:** Direct frontend-to-backend pipeline integration allowing users to trigger calculated balancing matrices instantly.

## 🛠️ Tech Stack
* **Core Engine & Backend:** Python (Native HTTP Networking Architectures, JSON State Management, Multithreaded Telemetry Simulation Loops)
* **Interface Matrix & Frontend:** HTML5, Tailwind CSS, JavaScript (Async Telemetry Polling, API Communication, Dynamic UI Rendering Layers)
* https://github.com/paka2002/AstraDC/blob/fb7eb7679b5734511201ecf70c302e079bb7cad9/Screenshot_20260522-033424.png
