import requests
import unittest

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

class LlmTest(unittest.TestCase):

    def test_ollama_prompt(self):
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": "Was ist die Hauptstadt von Frankreich?",
                "stream": False
            },
            timeout=300
        )

        self.assertEqual(200, response.status_code)

        data = response.json()

        self.assertIn("response", data)
        self.assertIn("Paris", data["response"])
        print(data)
if __name__ == "__main__":
    unittest.main()