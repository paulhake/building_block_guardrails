<div align="center">
  <img src="assets/logo.png" alt="IBM Building Blocks AI Guardrails" width="300"/>
</div>

# IBM Building Block for Trusted AI: Guardrails

An advanced AI guardrails implementation using IBM watsonx.governance SDK for comprehensive AI safety evaluation and monitoring.

## Overview

This project provides real-time AI content safety detection and evaluation using IBM's watsonx.governance platform. It implements multiple guardrail metrics to assess AI-generated content for various risks including hate speech, bias, jailbreak attempts, and other harmful content.

## Features

### Content Safety Detection
- **HAP (Hate, Abuse, Profanity)**: Detects harmful language and offensive content
- **PII Detection**: Identifies and filters personally identifiable information
- **Harm Detection**: Assesses content for potential harmful intent
- **Social Bias Detection**: Identifies biased or discriminatory language
- **Jailbreak Detection**: Prevents prompt injection and manipulation attempts
- **Violence Detection**: Identifies violent or threatening content
- **Profanity Detection**: Filters inappropriate language
- **Unethical Behavior Detection**: Identifies content promoting unethical activities

### Advanced Evaluation Metrics
- **Topic Relevance**: Ensures content stays on-topic relative to system prompts
- **Prompt Safety Risk**: Detects off-topic content and prompt injection attempts
- **Answer Relevance**: Evaluates how well responses address input questions
- **Context Relevance**: Assesses relevance of provided context to questions
- **Faithfulness**: Measures consistency between generated content and source material

### Powered by Granite Guardian
Most metrics utilize IBM's Granite Guardian model (Beta) for comprehensive risk assessment including:
- Harm and violence detection
- Social bias assessment
- Jailbreak attempt identification
- Answer relevance evaluation
- Groundedness verification

## Technology Stack

- **Python 3.10+**
- **IBM watsonx.governance SDK**
- **Jupyter Notebooks** for interactive development
- **python-dotenv** for environment configuration
- **IBM Cloud SDK** for authentication

## Prerequisites

1. **IBM watsonx.governance Service Instance**
   - Create an instance at [IBM Cloud Catalog](https://cloud.ibm.com/catalog/services/watsonxgovernance)

2. **IBM Cloud API Key**
   - Generate at [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
   - Requires access to watsonx.governance service

## Installation & Setup

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd guardrails_v2
```

### 2. Create Python Environment
```bash
# Using conda (recommended)
conda create -n guardrails-app python=3.10
conda activate guardrails-app

# Or using venv
python -m venv guardrails-app
source guardrails-app/bin/activate  # On Windows: guardrails-app\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Core IBM watsonx.governance SDK (if not in requirements.txt)
pip install 'ibm-watsonx-gov[metrics]'
```

### 4. Environment Configuration

Create a `.env` file in the project root:
```bash
cp .env.example .env  # If example exists, or create new file
```

Add your IBM watsonx credentials to `.env`:
```env
# IBM watsonx.governance API Configuration
WATSONX_APIKEY=your_ibm_cloud_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Optional: Service Instance ID (required if you have multiple instances)
WXG_SERVICE_INSTANCE_ID=your_service_instance_id_here

# Optional: Region (default is us-south)
# WATSONX_REGION=us-south
```

**Security Note**: Never commit the `.env` file to version control. It's already included in `.gitignore`.

### 5. Verify Installation
Option A - Run the Streamlit web app:
```bash
streamlit run app.py
```

Option B - Start Jupyter and run the main notebook:
```bash
jupyter notebook "Real Time Detections_v1.ipynb"
```

## Usage

### Option 1: Streamlit Web App (Recommended)
The easiest way to use the guardrails is through the interactive web interface:

```bash
streamlit run app.py
```

**Features:**
- **Interactive UI**: User-friendly web interface
- **Real-time Evaluation**: Enter text and get instant results
- **Customizable Guardrails**: Select which metrics to run using checkboxes
- **Configurable Threshold**: Adjust risk threshold with a slider (default: 0.7)
- **Color-coded Results**: Red highlighting for high-risk content
- **Advanced Options**: Support for RAG metrics and system prompts
- **Export Results**: Download results as CSV
- **Reset Functionality**: Clear inputs and start fresh

### Option 2: Jupyter Notebook
For development and experimentation:

1. **Launch Jupyter**: `jupyter notebook` or `jupyter lab`
2. **Open Main Notebook**: `Real Time Detections_v1.ipynb`
3. **Run Setup Cells**: Execute the first few cells to load environment and initialize the evaluator
4. **Test Guardrails**: Run any of the example cells to test different safety metrics

### Basic Example
```python
from ibm_watsonx_gov.evaluators import MetricsEvaluator
from ibm_watsonx_gov.metrics import HAPMetric, PIIMetric

# Initialize evaluator (credentials loaded from .env)
evaluator = MetricsEvaluator()

# Test content
text = "This is a sample text to evaluate"

# Run multiple guardrails
result = evaluator.evaluate(
    data={"input_text": text}, 
    metrics=[HAPMetric(), PIIMetric()]
)

# View results
print(result.to_df())
```

### Available Applications

#### `app.py` - Streamlit Web Application
Interactive web interface for AI guardrails evaluation:
- User-friendly dashboard with text input and metric selection
- Real-time guardrail evaluation with color-coded results
- Configurable risk thresholds and advanced options
- Export functionality for results

#### `Real Time Detections_v1.ipynb` - Jupyter Notebook
Comprehensive demonstration of all available guardrail metrics including:
- Content safety detection examples
- RAG (Retrieval-Augmented Generation) evaluation metrics
- Batch evaluation using metric groups
- Real-world content analysis examples

## Configuration

### Regional Settings
By default, the project uses the US South region. To use other regions:

```python
import os
os.environ["WATSONX_REGION"] = "eu-de"  # Frankfurt
# Supported: us-south, eu-de, au-syd, ca-tor, jp-tok
```

### Metric Groups
Use predefined metric groups for batch evaluation:
```python
from ibm_watsonx_gov.entities.enums import MetricGroup

# Run all content safety metrics at once
result = evaluator.evaluate(
    data={"input_text": text}, 
    metric_groups=[MetricGroup.CONTENT_SAFETY]
)
```

## Language Support

**Important**: AI guardrails in IBM watsonx.governance currently support **English-language text only**.

## Regional Availability

- **Topic Relevance**: Available in Dallas (us-south) and Frankfurt (eu-de) regions only
- **Prompt Safety Risk**: Available in Dallas (us-south) and Frankfurt (eu-de) regions only
- **Other Metrics**: Available in all supported regions

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your API key is correct and has watsonx.governance access
   - Check that WXG_SERVICE_INSTANCE_ID is set if you have multiple instances

2. **Module Import Errors**
   - Ensure you're using the correct Python environment
   - Reinstall requirements: `pip install -r requirements.txt`

3. **Regional Errors**
   - Some metrics require specific regions (Dallas/Frankfurt)
   - Set WATSONX_REGION environment variable appropriately

### Getting Help

1. Check [IBM watsonx.governance Documentation](https://ibm.github.io/ibm-watsonx-gov/index.html)
2. Review IBM Cloud service status
3. Verify your service instance has the required permissions

## Development

### Project Structure
```
guardrails_v2/
├── .env                           # Environment variables (not in git)
├── .gitignore                     # Git ignore rules
├── CLAUDE.md                      # AI assistant instructions
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── app.py                         # Streamlit web application
└── Real Time Detections_v1.ipynb # Jupyter notebook demonstration
```

### Contributing
1. Follow the existing code style and patterns
2. Test all changes with the provided notebooks
3. Update documentation for any new features
4. Ensure security best practices (no hardcoded credentials)

## Security Considerations

- **API Keys**: Never commit API keys or credentials to version control
- **Environment Variables**: Use `.env` file for all sensitive configuration
- **Access Control**: Ensure proper IBM Cloud IAM permissions for watsonx.governance
- **Key Rotation**: Regularly rotate API keys according to security policies

## License

[Add appropriate license information]

## Support

For technical support:
- IBM watsonx.governance: [IBM Support](https://cloud.ibm.com/docs/watsonxgovernance)
- Project Issues: [Create an issue in this repository]