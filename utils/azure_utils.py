# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Chris Polewiak

"""
azure_utils.py

Purpose:
    Integration with Azure Vision API for image analysis and tag extraction.

Main Functions:
    - image_analyse(image_data): Sends image data to Azure Vision API and returns extracted caption and tags.

Requires Azure credentials configured in the .env file.
This module centralizes all Azure Vision API communication for the photo processing pipeline.
"""

import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from utils.log_utils import *


load_dotenv()

AZURE_IMAGE_MAX_DIM = 16000
AZURE_IMAGE_MIN_DIM = 50

endpoint = os.environ.get("VISION_ENDPOINT")
key = os.environ.get("VISION_KEY")
client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

visual_features = [VisualFeatures.TAGS, VisualFeatures.CAPTION]

def image_analyse(image_data):

    log_debug("Analyzing image...")

    result = client.analyze(
        image_data=image_data,
        visual_features=visual_features,
        gender_neutral_caption=True
        )

    metadata = {"caption": '', "keywords": []}
    caption_data = result.get("captionResult")
    if caption_data and caption_data.get('confidence', 0) > 0.6:
        metadata['caption'] = caption_data['text']

    metadata['keywords'] = []
    tags_result = result.get("tagsResult", {})
    tags = tags_result.get("values", [])
    metadata['keywords'] = [t['name'] for t in tags if t.get("confidence", 0) > 0.6 and t.get("name")]

    return metadata
