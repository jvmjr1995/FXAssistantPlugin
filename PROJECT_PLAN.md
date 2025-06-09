# 🧠 FXAssistant Project Plan

---

## 🎯 Vision

FXAssistant is a modular, intelligent music production tool that helps producers streamline workflow, collaborate across DAWs, and mix more effectively with AI-guided assistance. It blends plugin design (C++/JUCE) with a Python/Django backend and optional AI/ML integration.

---

## 🧩 Modules

1. **AI Session Assistant**  
   - Auto-names tracks  
   - Logs plugin & session changes  
   - Suggests next steps  

2. **Smart Mixing for Niche Genres**  
   - Learns from reference mixes  
   - Suggests EQ curves, dynamics settings  

3. **Mobile Mix Optimizer**  
   - Simulates phone speaker output  
   - Optimized export for Instagram, TikTok, Spotify  

4. **MIDI Humanizer**  
   - Applies groove and dynamic templates to MIDI  
   - Velocity & timing randomization using context  

5. **DAW Collaboration Engine**  
   - Syncs sessions across DAWs  
   - Enables comments, stem exchange  

6. **FX Chain AI Recommender**  
   - Matches genres to plugin chains  
   - Visualizes recommended chains in the GUI  

---

## 🔧 Tech Stack

| Layer        | Tool/Language                          |
|--------------|----------------------------------------|
| Plugin Core  | C++ with JUCE                          |
| DSP Option   | Rust (for AI-heavy or low-latency tasks)|
| ML Training  | Python, PyTorch, TensorFlow            |
| Model Runtime| ONNX, TorchScript                      |
| Backend      | Django + PostgreSQL                    |
| Auth/Billing | Stripe                                 |
| Cloud Sync   | Django REST API                        |

---

## 💰 Pricing Model

| Tier     | Features                                                     | Price     |
|----------|--------------------------------------------------------------|-----------|
| Free     | Basic UI, 1 AI FX/month, MIDI Humanizer Lite                 | $0        |
| Creator  | All AI FX + Session Assistant                                | $15/month |
| Studio   | Genre-aware FX chains, team collaboration, preset sync       | $30/month |
| Pro      | Full suite, priority inference, unlimited stems              | $50/month |

---

## 🔨 MVP Development Roadmap

| Phase | Focus                                 | Duration     |
|-------|----------------------------------------|--------------|
| 1     | Build JUCE plugin shell + basic GUI    | 1–2 weeks    |
| 2     | FX Chain Recommender w/ JSON mapping   | 3–4 weeks    |
| 3     | MIDI Humanizer + Session Logger        | 3–4 weeks    |
| 4     | Cloud Sync (Django), Mobile Mix sim    | 3–4 weeks    |
| 5     | Stripe Integration + GUI polish        | 2–3 weeks    |

---

## ✅ Deliverables (v1.0)

- AU plugin validated in Logic Pro  
- Working GUI with genre selector  
- FX Chain preset loader (genre-based)  
- Django API with preset endpoints  
- Public roadmap and GitHub docs  

---

## 📁 Repo Layout (planned)

```
FXAssistantPlugin/
├── FXAssistant/              # JUCE source code
├── django_backend/           # Django app (API, models, Stripe)
├── roadmap/                  # Milestones and feature goals
├── .github/                  # Issue templates, workflows
├── README.md
├── LICENSE
├── PROJECT_PLAN.md
```
