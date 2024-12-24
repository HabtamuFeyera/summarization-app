# Models for Summarization App

## Overview

This directory contains the models used for summarization. For this project, we use HuggingFace models for natural language processing tasks like text summarization. The model in use for this example is `t5-small`, a lightweight transformer model that can be used for tasks like summarization.

### Downloading Models

The models used in this project are managed through the HuggingFace `transformers` library. You don't need to manually download the models because they are automatically fetched when the app is run.

To download the model, the backend FastAPI service uses the following code:

```python
from transformers import pipeline
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
