# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI guardrails project (version 2) that integrates with IBM watsonx services. The project is in early development stage with minimal initial setup.

## Technology Stack

- **Primary Language**: Python (expected)
- **Development Environment**: Jupyter Notebooks
- **AI Platform**: IBM watsonx
- **Configuration**: Environment-based (.env file)

## IBM watsonx Configuration

The project is configured to work with IBM watsonx services:
- **Region**: US South (us-south.ml.cloud.ibm.com)
- **Service Instance ID**: aef94d9e-5fb6-4b34-bbff-3d3c5ea098d7
- **Project ID**: f6658fd6-c56d-4e01-9477-919f48184b33

**Important**: API credentials are stored in `.env` file - handle with appropriate security measures.

## Project Structure

Currently minimal structure:
- `.env` - watsonx API configuration
- `api_config.ipynb` - Main notebook for API configuration and testing

## Development Commands

**Note**: This project lacks standard development tooling. Common commands will need to be established as the project develops.

Expected development workflow:
- Start Jupyter notebook server: `jupyter notebook` or `jupyter lab`
- Install Python dependencies: `pip install -r requirements.txt` (once created)

## Architecture Notes

This appears to be a focused project for implementing AI guardrails using IBM's watsonx platform. The "v2" designation suggests this is an iteration or improvement on a previous guardrails implementation.

The project is in its initial phase - future development should establish:
- Python package structure
- Requirements management
- Testing framework
- Documentation structure

## Security Considerations

- The `.env` file contains sensitive API credentials and should not be committed to version control
- Consider adding `.gitignore` to exclude sensitive files
- IBM watsonx API keys should be rotated periodically according to enterprise security policies