from http.server import BaseHTTPRequestHandler
from gemini import Gemini
import json
import os
os.environ["GEMINI_ULTRA"] = "1"

# Cookies hardcoded (TIDAK DISARANKAN untuk produksi)
COOKIES = {
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
client = Gemini(cookies=COOKIES)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            query = self.path.split('?')[1] if '?' in self.path else ''
            params = dict(qc.split('=') for qc in query.split('&')) if query else {}
            prompt = params.get('prompt', '')
            
            if not prompt:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Parameter 'prompt' diperlukan"
                }).encode())
                return
            
            # Get response from Gemini
            response = client.generate_content(prompt)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "response": response.payload
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
