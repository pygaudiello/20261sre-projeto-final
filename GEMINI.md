# Project Context: Olist SRE & Data Engineering Challenge

This repository contains the specifications and architectural modeling for a reliable data engineering pipeline. It focuses on the ingestion, processing, and visualization of Olist marketplace data while ensuring system resilience and data trustworthiness.

## Project Overview

The project aims to define a robust ETL (Extract, Transform, Load) pipeline that processes approximately 100k daily orders from CSV files into a Postgres analytical database.

## Documentation Structure

The core project documentation is located in the `/documents` directory, organized as follows:

- **[Index](documents/00_index.md)**: Map of the documentation directory.
- **[Functional Requirements](documents/01_functional_requirements.md)**: Detailed RF-01 to RF-NN.
- **[Non-Functional Requirements](documents/02_non_functional_requirements.md)**: RNF, SLOs, and SLIs.
- **[Architecture](documents/03_architecture.md)**: RM-ODP 5 viewpoints.
- **[RTM](documents/04_rtm.md)**: Requirement Traceability Matrix.
- **[Test Plans](documents/00_index.md)**: Load (05), Security (06), and Modeling (07) plans.
- **[System Design](documents/08_system_design.md)**: Mermaid diagrams and technical narrative.
- **[AWS Setup](documents/09_aws_cli_session.md)**: Guide for AWS CLI in Codespaces.

## AI Agents & Skills

Specific instructions and skills for AI agents (like Gemini CLI) are located in `documents/agents/`.
- **[GEMINI.md](documents/agents/GEMINI.md)**: Tailored instructions for the Gemini CLI and general agent guidelines.
- **Skills**: Specialized prompts for eliciting requirements, reviewing architecture, and planning tests are in `documents/agents/skills/`.

## Usage for AI

When interacting with this repository, always refer to the requirements and architecture defined in `/documents`. Use the specialized skills in `documents/agents/skills/` to perform complex analysis or documentation updates.

---
*Note: This GEMINI.md file was updated to reflect the full documentation and agent framework.*
