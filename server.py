"""Zero-dependency HTTP API server for NEPSE Cognitive Triad Mission Control.
Runs using Python standard library http.server on port 8000.
Serves OpenAPI docs, Triad evaluations, portfolio status, and market data.
"""

import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Ensure local app package is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "apps", "backend")))

from app.services.cognitive_triad.orchestrator import triad_orchestrator
from app.services.journaling.generator import journal_generator
from app.services.data_ingestion.nepse_client import NepseClient

nepse_client = NepseClient()


class NepseApiHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # 1. API Documentation (Swagger/OpenAPI representation)
        if path in ("/docs", "/"):
            html = """<!DOCTYPE html>
<html>
<head>
    <title>NEPSE Cognitive Triad API</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
    <style>body { margin: 0; background: #0f172a; }</style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        SwaggerUIBundle({
            dom_id: '#swagger-ui',
            spec: {
                openapi: "3.0.0",
                info: {
                    title: "NEPSE Cognitive Triad AI Trader API",
                    version: "1.0.0",
                    description: "Multi-Agent Literature-Grounded Algorithmic Trading Platform"
                },
                paths: {
                    "/health": { get: { summary: "Health Check", responses: { "200": { description: "OK" } } } },
                    "/api/v1/market/status": { get: { summary: "NEPSE Market Session Status", responses: { "200": { description: "OK" } } } },
                    "/api/v1/portfolio/balance": { get: { summary: "Portfolio Balance & T+2 Buying Power", responses: { "200": { description: "OK" } } } },
                    "/api/v1/triad/evaluate/{symbol}": { 
                        get: { 
                            summary: "Run Cognitive Triad Evaluation on Ticker", 
                            parameters: [{ name: "symbol", in: "path", required: true }],
                            responses: { "200": { description: "Evaluation with Route Alpha, Beta, Gamma scores and Taleb Veto" } } 
                        } 
                    }
                }
            }
        });
    </script>
</body>
</html>"""
            self._set_headers(200, "text/html")
            self.wfile.write(html.encode("utf-8"))
            return

        # 2. Health check
        if path == "/health":
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "ok", "system": "NEPSE Cognitive Triad"}).encode("utf-8"))
            return

        # 3. Market status
        if path == "/api/v1/market/status":
            self._set_headers(200)
            status_data = {
                "is_open": nepse_client.is_market_open(),
                "market_index": 2085.40,
                "index_change": 12.50,
                "percent_change": 0.60,
                "turnover_npr": 420500000.0,
                "currency": "NPR"
            }
            self.wfile.write(json.dumps(status_data).encode("utf-8"))
            return

        # 4. Portfolio balance & T+2 buying power
        if path == "/api/v1/portfolio/balance":
            self._set_headers(200)
            balance_data = {
                "total_equity_npr": 13300000.00,
                "settled_cash_npr": 13300000.00,
                "unsettled_cash_npr": 0.00,
                "available_buying_power_npr": 13300000.00,
                "unrealized_pnl_npr": 0.00,
                "realized_pnl_npr": 0.00,
                "currency": "NPR"
            }
            self.wfile.write(json.dumps(balance_data).encode("utf-8"))
            return

        # 5. Cognitive Triad Evaluation Endpoint
        if path.startswith("/api/v1/triad/evaluate/"):
            symbol = path.split("/")[-1].upper()
            features = {
                "trend_bullish": 1,
                "volume_ratio": 1.7,
                "volatility_20": 0.018,
                "volume_spike": 1,
                "rsi_14": 54.0,
                "candle_position": 0.82,
                "has_pending_action": 1,
                "action_value_pct": 15.0,
                "days_to_book_close": 8,
                "urgency_score": 0.73,
                "ltp": 510.0,
                "prev_close": 500.0,
                "current_sector_exposure": 0.10,
            }
            decision = triad_orchestrator.decide(features)
            
            # Simple synchronous fallback for journal synthesis
            journal_text = (
                f"### Executive Trade Audit: {decision.get('action')} {symbol}\n\n"
                f"**Consensus Score**: +{decision.get('final_score')}/100 (Disagreement Std: {decision.get('disagreement')})\n\n"
                f"#### Route Alpha (Structural Economics & Law)\n"
                f"Score: {decision.get('alpha', {}).get('score')}/100\n"
                + "\n".join([f"- {r}" for r in decision.get('alpha', {}).get('rationale', [])]) + "\n\n"
                f"#### Route Beta (Behavioral Psychology & Narrative)\n"
                f"Score: {decision.get('beta', {}).get('score')}/100\n"
                + "\n".join([f"- {r}" for r in decision.get('beta', {}).get('rationale', [])]) + "\n\n"
                f"#### Route Gamma (Philosophical Tail Risk & Complexity)\n"
                f"Score: {decision.get('gamma', {}).get('score')}/100 | Veto Status: {decision.get('gamma_vetoed')}\n"
                + "\n".join([f"- {r}" for r in decision.get('gamma', {}).get('rationale', [])]) + "\n\n"
                f"#### Literature Citations\n"
                f"- Hyman Minsky (1986): Early-stage credit expansion signal.\n"
                f"- Robert Shiller (2019): Narrative contagion driving book-close urgency.\n"
                f"- Nassim Nicholas Taleb (2012): Antifragility criteria met; low volatility regime.\n\n"
                f"---\n"
                f"*Cognitive Prosthetic Note: Final strategic authority rests strictly with the human strategist.*"
            )

            res_payload = {
                "symbol": symbol,
                "decision": decision,
                "synthesized_journal": journal_text,
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(res_payload).encode("utf-8"))
            return

        # 404 Fallback
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))


def run_server(port=8000):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, NepseApiHandler)
    print(f"[*] NEPSE Cognitive Triad API Server listening on http://localhost:{port}")
    print(f"[*] OpenAPI Interactive Docs available at: http://localhost:{port}/docs")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run_server()
