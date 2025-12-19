# coding: utf-8

import os

from vertexai.generative_models import GenerativeModel
import vertexai


def ask_gemini(prompt):
    """
    Ask Gemini for a response.
    """
    project_id = os.environ.get("PROJECT_ID", "Not Set")
    location = os.environ.get("LOCATION", "Not Set")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text