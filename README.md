# solar-advisor-agent

Sistema multi-agente de consultoria em energia solar para residências e condomínios — desenvolvido com Azure AI Foundry

## Stack

![Azure AI Foundry](https://img.shields.io/badge/Azure%20AI%20Foundry-SDK-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-green)

## Desenvolvimento & Colaboração

![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Enabled-blue)

Este projeto é desenvolvido com **colaboração humano-IA** usando GitHub Copilot integrado ao VS Code. O Copilot atua como co-autor no desenvolvimento de agentes, assistindo na geração de código, arquitetura e boas práticas de implementação.

O projeto segue o acordo de boas práticas definido no documento local `acordo_boas_praticas_v1.3.pdf` (não versionado), que formaliza esta colaboração humano-IA com preâmbulo, glossário, antipadrões e compromissos de revisão por pull request.

## Roadmap v1

### Semana 1 — Fundação

- [x] v1: task 1 — Setup Azure AI Foundry + VS Code + GitHub
- [x] v1: task 2 — Content Filter + Responsible AI (M-A-M-G)
- [x] v1: task 3 — Document Intelligence (extrator de fatura de energia PDF)
- [ ] v1: task 4 — Language Service no Document Analyzer
- [ ] v1: task 5 — Azure AI Search (indexar docs ANEEL / RN 482 / RN 1000)
- [ ] v1: task 6 — Orchestrator Agent + detector de perfil (residencial / condomínio)

### Semana 2 — Agentes + Deploy

- [ ] v1: task 7 — Solar Sizing Agent + ROI Agent
- [ ] v1: task 8 — Regulation Agent + Condo Rateio Agent
- [ ] v1: task 9 — MCP Server (Solar Sizing Agent)
- [ ] v1: task 10 — Report Generator
- [ ] v1: task 11 — OpenTelemetry + Application Insights
- [ ] v1: task 12 — Streamlit UI + FastAPI
- [ ] v1: task 13 — Deploy Azure Container Apps + CI/CD
- [ ] v1: task 14 — README técnico + post LinkedIn

## Decisões descontinuadas

<!-- Registrar aqui decisões abandonadas com motivo e data -->
<!-- Exemplo: [~] SQLite substituído por Supabase — Jun/2025 -->

## Arquitetura

> Diagrama será adicionado na task 6