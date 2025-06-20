from http.server import BaseHTTPRequestHandler
import json
import os
from gemini import Gemini

cookies = {
  "SID": "g.a000yQgMd6M6PdLhOsM-cpJnCYDGbsFrYmvO-ePk0qQr6Vj28d9GU4yjczENUwoXW1N4aolYyQACgYKAUcSARISFQHGX2MiNtRif3PgjuzvJbeYKjHkwBoVAUF8yKpZVJzn4AyTXwwe_Ak5oae-0076",
  "__Secure-1PSID": "g.a000yQgMd6M6PdLhOsM-cpJnCYDGbsFrYmvO-ePk0qQr6Vj28d9GEj0uPkcJMhLG6se5lKhbUAACgYKAUwSARISFQHGX2Mion3ntADn0odeCh-S21m2jBoVAUF8yKqaRWxPFdlsH6CeLEBinqKF0076",
  "__Secure-3PSID": "g.a000yQgMd6M6PdLhOsM-cpJnCYDGbsFrYmvO-ePk0qQr6Vj28d9Gotn1vcrda_UGxtBGTFnrhgACgYKAdASARISFQHGX2Mip0dFO4qyq2Z-WCGs6pdfYRoVAUF8yKoeGPS2_DJEMLDXbQr5a5tT0076",
  "HSID": "A3ec3EtUa-izSoN8V",
  "SSID": "AamEuCXQVv17OWZCG",
  "APISID": "uZpuELdCX6EmgsvN/AO9Ir15-mso3lJjP0",
  "SAPISID": "1ln7OKXnrZoiiRzN/AD2HLrAD2t4P-LFFb",
  "__Secure-1PAPISID": "1ln7OKXnrZoiiRzN/AD2HLrAD2t4P-LFFb",
  "__Secure-3PAPISID": "1ln7OKXnrZoiiRzN/AD2HLrAD2t4P-LFFb",
  "NID": "524=fCsG53Ke9twXz33r3aRrBXc6GhQR5IhihXIqg2a6vfXcasfvDHwrYjitLRCGwaH0dU0vyEv6eMOuXMfKoKlqjIeMWFw2A1le5zcQf7dnTpR6SNpwoUoj5uIyJho_WIpMQs-BPVoCfd2jV_ulbpzqGmVG5_SSwD1eiy2HAXiGpH0D3Bl--cVUyAIdZlNHBs_PcvfA6oaZCCot1v6BifeAMLVywo4I1YdftQ-YGWsm",
  "SIDCC": "AKEyXzW6k2g0VL_c0PtqJYPrIkLj_s8OQ4CsDzPjz49JGGCI2CCVlPrQUvQgbFUe9mhKLDZu",
  "__Secure-1PSIDCC": "AKEyXzVFcfxZiZTy8mXrdv_DHfHnJrPXoekQxlVumXoT0nMg83NAED8ImiFsVwceTZooDjQm",
  "__Secure-3PSIDCC": "AKEyXzVhNe1vuzHoJVhGaTtTRrwjrhacALcoZW6I7CJcK6KEA7_BzSERPR05ZdztikUGj6PAwRg"
}
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            # Get prompt from URL params
            query = self.path.split('?')[1] if '?' in self.path else ''
            params = dict(q.split('=') for q in query.split('&')) if query else {}
            prompt = params.get('prompt', '')
            
            if not prompt:
                raise ValueError("Missing 'prompt' parameter")
            
            # Initialize Gemini client
            os.environ["GEMINI_ULTRA"] = "1"
            client = Gemini(
                cookies=cookies
            )
            
            # Get Gemini response
            gemini_response = client.generate_content(prompt)
            payload = gemini_response.payload
            
            # Extract text and code from response
            response_text = ""
            response_code = {}
            
            if 'candidates' in payload and len(payload['candidates']) > 0:
                candidate = payload['candidates'][0]
                response_text = candidate.get('text', '')
                
                # Extract code snippets
                if 'code' in candidate:
                    response_code = candidate['code']
                else:
                    # Fallback: extract code from text if not in structured format
                    import re
                    code_blocks = re.findall(r'```(?:html|python|javascript)?\n(.*?)\n```', response_text, re.DOTALL)
                    if code_blocks:
                        response_code = {"snippet_1": code_blocks[0]}
            
            # Build final response
            response_data = {
                "status": "success",
                "response": {
                    "text": response_text,
                    "code": response_code
                }
            }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {
                "status": "error",
                "message": str(e),
                "response": {
                    "text": "",
                    "code": {}
                }
            }
            self.wfile.write(json.dumps(error_response).encode())
