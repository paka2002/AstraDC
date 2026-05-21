import json
import random
from http.server import HTTPServer, BaseHTTPRequestHandler

# In-memory database tracking the physical cluster infrastructure state
gpu_cluster = {
    "Node-01": {"id": "Node-01", "gpu_load": 85.0, "power_draw": 650.0, "temperature": 82.5, "status": "Hotspot"},
    "Node-02": {"id": "Node-02", "gpu_load": 92.0, "power_draw": 690.0, "temperature": 86.0, "status": "Hotspot"},
    "Node-03": {"id": "Node-03", "gpu_load": 30.0, "power_draw": 250.0, "temperature": 52.0, "status": "Healthy"},
    "Node-04": {"id": "Node-04", "gpu_load": 15.0, "power_draw": 180.0, "temperature": 45.5, "status": "Idle"},
}

def update_telemetry_physics():
    """Simulates real-time physical telemetry fluctuations on the chip clusters."""
    for node_id, metrics in gpu_cluster.items():
        fluc = random.uniform(-4.0, 4.0)
        metrics["gpu_load"] = max(0.0, min(100.0, metrics["gpu_load"] + fluc))
        metrics["power_draw"] = 150.0 + (metrics["gpu_load"] * 5.8)
        metrics["temperature"] = 40.0 + (metrics["gpu_load"] * 0.5)
        
        if metrics["temperature"] >= 78.0:
            metrics["status"] = "Hotspot"
        elif metrics["gpu_load"] <= 20.0:
            metrics["status"] = "Idle"
        else:
            metrics["status"] = "Healthy"

def compute_greedy_optimization():
    """Executes the greedy thermal balancing scheduling matrix."""
    nodes = list(gpu_cluster.values())
    recommendations = []
    
    hotspots = [n for n in nodes if n["temperature"] >= 78.0]
    cool_nodes = [n for n in nodes if n["temperature"] < 65.0 and n["gpu_load"] < 60.0]
    
    for host in hotspots:
        if not cool_nodes:
            break
        target = cool_nodes[0]
        excess_load = host["gpu_load"] - 50.0
        available_capacity = 80.0 - target["gpu_load"]
        migration_load = min(excess_load, available_capacity)
        
        if migration_load > 5:
            recommendations.append({
                "source_node": host["id"],
                "target_node": target["id"],
                "workload_migration_pct": round(migration_load, 1),
                "reason": f"Thermal threat detected. Routing payload from {host['id']} ({host['temperature']:.1f}°C) to cooling reservoir {target['id']}."
            })
            target["gpu_load"] += migration_load
            if target["gpu_load"] >= 60.0:
                cool_nodes.pop(0)
                
    return {"hotspots_detected": len(hotspots), "recommendations": recommendations}

class AstraDCServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Route 1: Serve UI Dashboard
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))
            
        # Route 2: Telemetry API Endpoint
        elif self.path == "/api/telemetry":
            update_telemetry_physics()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(list(gpu_cluster.values())).encode("utf-8"))
            
        # Route 3: Optimization Core Engine Endpoint
        elif self.path == "/api/optimize":
            plan = compute_greedy_optimization()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(plan).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint Not Found")

    def do_POST(self):
        # Route 4: Execute Workload Migration Command
        if self.path == "/api/migrate":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            
            src, tgt = req.get("source_node"), req.get("target_node")
            amt = float(req.get("workload_amount", 0))
            
            if src in gpu_cluster and tgt in gpu_cluster:
                actual_shift = min(gpu_cluster[src]["gpu_load"], amt)
                gpu_cluster[src]["gpu_load"] -= actual_shift
                gpu_cluster[tgt]["gpu_load"] += actual_shift
                
                # Immediate physics loop resolution
                for n in [src, tgt]:
                    gpu_cluster[n]["power_draw"] = 150.0 + (gpu_cluster[n]["gpu_load"] * 5.8)
                    gpu_cluster[n]["temperature"] = 40.0 + (gpu_cluster[n]["gpu_load"] * 0.5)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "Success"}).encode("utf-8"))
            else:
                self.send_error(400, "Bad Configuration")

# Embedded Core UI Code Architecture
HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AstraDC - AI Infrastructure Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0b0f19] text-gray-100 font-sans min-h-screen p-8">
    <header class="mb-8 border-b border-gray-800 pb-6 flex justify-between items-center">
        <div>
            <h1 class="text-3xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">ASTRA DC</h1>
            <p class="text-gray-400 mt-1">AI Infrastructure Cluster Power & Thermal Optimizer</p>
        </div>
        <button onclick="syncClusterState()" class="px-4 py-2 bg-gray-800 hover:bg-gray-700 font-medium rounded-lg transition border border-gray-700">Force Matrix Sync</button>
    </header>

    <h2 class="text-xl font-bold mb-4 text-cyan-400">Active Compute Clusters Telemetry</h2>
    <div id="telemetry-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"></div>

    <div class="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 class="text-xl font-bold mb-4 text-yellow-500">Automated Greedy Optimization Intelligence</h2>
        <div id="optimization-panel"></div>
    </div>

    <script>
        async function syncClusterState() {
            try {
                const telRes = await fetch('/api/telemetry');
                const telemetry = await telRes.json();
                const grid = document.getElementById('telemetry-grid');
                grid.innerHTML = '';
                
                telemetry.forEach(node => {
                    const statusColor = node.status === 'Hotspot' ? 'bg-red-950 text-red-400 border-red-800' : node.status === 'Idle' ? 'bg-gray-800 text-gray-400' : 'bg-emerald-950 text-emerald-400 border-emerald-800';
                    grid.innerHTML += `
                        <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 shadow-lg">
                            <div class="flex justify-between items-center mb-4">
                                <span class="font-mono text-gray-300 font-bold">${node.id}</span>
                                <span class="px-2 py-0.5 rounded text-xs font-semibold border ${statusColor}">${node.status}</span>
                            </div>
                            <div class="space-y-3">
                                <div>
                                    <div class="flex justify-between text-xs text-gray-400 mb-1"><span>Compute Load</span><span>${node.gpu_load.toFixed(1)}%</span></div>
                                    <div class="w-full bg-gray-800 h-2 rounded-full overflow-hidden">
                                        <div class="bg-cyan-500 h-full transition-all duration-500" style="width: ${node.gpu_load}%"></div>
                                    </div>
                                </div>
                                <div class="flex justify-between items-center text-sm"><span class="text-gray-400">Power Draw</span><span class="font-mono text-yellow-500 font-bold">${node.power_draw.toFixed(0)} W</span></div>
                                <div class="flex justify-between items-center text-sm"><span class="text-gray-400">Thermal Core</span><span class="font-mono font-bold ${node.temperature > 78 ? 'text-red-400' : 'text-gray-200'}">${node.temperature.toFixed(1)}°C</span></div>
                            </div>
                        </div>`;
                });

                const optRes = await fetch('/api/optimize');
                const opt = await optRes.json();
                const panel = document.getElementById('optimization-panel');
                panel.innerHTML = '';

                if(opt.recommendations.length === 0) {
                    panel.innerHTML = `<div class="bg-emerald-950/40 border border-emerald-900 text-emerald-400 p-4 rounded-lg">Thermal equilibrium optimized. Zero node execution balancing adjustments required at this cycle.</div>`;
                } else {
                    opt.recommendations.forEach(rec => {
                        panel.innerHTML += `
                            <div class="bg-gray-950 border border-yellow-900/40 p-4 rounded-lg flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                                <div>
                                    <p class="text-yellow-400 font-medium text-sm mb-1">🚨 Workload Relocation Urgently Dispatched</p>
                                    <p class="text-sm text-gray-300">${rec.reason}</p>
                                    <p class="text-xs text-gray-500 mt-1">Strategy payload: Shift <span class="text-cyan-400 font-mono font-bold">${rec.workload_migration_pct}%</span> processing load → <span class="text-white font-mono">${rec.target_node}</span>.</p>
                                </div>
                                <button onclick="executeShift('${rec.source_node}', '${rec.target_node}', ${rec.workload_migration_pct})" class="px-4 py-2 bg-gradient-to-r from-yellow-600 to-yellow-500 hover:from-yellow-500 hover:to-yellow-400 text-gray-950 font-bold rounded-lg text-sm shadow-md transition">Balance Core Load</button>
                            </div>`;
                    });
                }
            } catch(e) { console.error("Synchronization execution error context link fault", e); }
        }

        async function executeShift(source, target, amount) {
            await fetch('/api/migrate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({source_node: source, target_node: target, workload_amount: amount})
            });
            syncClusterState();
        }

        syncClusterState();
        setInterval(syncClusterState, 3000);
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), AstraDCServer)
    print("🚀 AstraDC Simulator Infrastructure Deployment Active at http://localhost:8080")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Infrastructure Simulation Engine...")
        server.server_close()
      
