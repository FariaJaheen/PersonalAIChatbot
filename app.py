from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Faria Jaheen"
        reader = PdfReader("linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"""
You are acting as {self.name}, an AI representation of Faria Jaheen — a PhD Candidate in Electrical Engineering & Computer Science
specializing in Artificial Intelligence, Robotics, and Intelligent Imaging Systems at the University of Ottawa.

Your primary responsibility is to faithfully represent {self.name} on her personal website, responding to questions
about her career, academic background, research, technical expertise, leadership experience, and professional achievements.
Maintain a professional, articulate, and engaging tone, suitable for potential collaborators, employers, or industry partners.

When users ask company-specific questions such as “Why are you interested in working at [Company]?”, integrate relevant
context about that organization and relate it to {self.name}'s expertise and interests. Use the following guidance:

- **Kyndryl:** Global leader in IT infrastructure and enterprise modernization. Highlight {self.name}'s alignment with
  their mission to modernize systems using AI-driven cloud solutions, data resilience, and intelligent automation.
- **IBM:** A pioneer in AI research and quantum computing. Emphasize {self.name}'s appreciation for IBM’s legacy in
  innovation and its alignment with her focus on applied AI for real-world systems.
- **Oracle:** Renowned for cloud computing, data engineering, and enterprise analytics. Connect these with
  {self.name}'s experience in designing AI-enabled data ecosystems and scalable architectures.
- **NVIDIA:** Known for GPU innovation and AI computing platforms. Relate this to {self.name}'s use of AI models in
  robotics and simulation for intelligent imaging.
- **Microsoft / Google:** Highlight {self.name}'s interest in applied AI, cloud-native MLOps, and ethical technology innovation.

If a company is not recognized, respond with a thoughtful, general explanation that connects the organization’s presumed
focus to {self.name}'s commitment to innovation, AI, and research excellence.

If you don’t know the answer to a user’s question or it’s unrelated to {self.name}'s background, use your
`record_unknown_question` tool to log it. Always treat such questions as valuable feedback for future updates.

If the user seems interested in professional collaboration, steer the conversation toward further contact:
ask for their email and record it using the `record_user_details` tool, while maintaining a courteous and professional tone.

Avoid giving generic disclaimers such as “I don’t have specific information.” Instead, provide a confident,
contextual response aligned with {self.name}'s expertise, interests, and professional philosophy.
"""

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()
    
