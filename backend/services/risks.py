from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_risk_analysis(ticker: str):
  prompt = f"""
  Analyze the key risks facing {ticker}'s stock performance from a macroeconomic, industry, and company perspective.
  Provide:
  - Top 2 macro risks
  - Top 2 industry risks
  - Top 2 company risks
  - A short overall LLM-generated summary
  Respond in structured JSON.
  """

  response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
  )

  try:
    return eval(response.choices[0].message.content)
  except Exception as e:
    return {
      "macro_risks": [],
      "industry_risks": [],
      "company_risks": [],
      "llm_generated_risk_summary": "Unable to parse AI response."
    }
