import json
from pathlib import Path


def create_plan(client, mission):

    prompt_template = Path(
        "prompts/planner.txt"
    ).read_text()

    prompt = prompt_template + "\n" + mission


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )


    text = response.text.strip()


    # Remove markdown formatting if Gemini adds it

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")


    return json.loads(text)
