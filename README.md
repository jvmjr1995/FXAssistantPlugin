# 🎛️ FXAssistantPlugin

**FXAssistant** is an AI-powered audio plugin designed for modern music producers. Built with JUCE, it integrates advanced machine learning models and cloud sync features to assist with mixing, collaboration, and production across genres.

> “Your AI co-producer — guiding your mix, managing your session, and evolving with your sound.”

---

## 🚀 Features

FXAssistant is built as a modular plugin with six key components:

1. **AI Session Assistant** – Auto-names tracks, logs revisions, and recommends next steps.
2. **Smart Mixing for Niche Genres** – Learns from reference tracks to shape EQ, compression, and FX choices.
3. **Mobile Mix Optimizer** – Simulates phone speakers and exports optimized formats.
4. **MIDI Humanizer** – Adds groove-based velocity/timing adjustments.
5. **DAW Collaboration Engine** – Enables sync, commenting, and stem sharing across DAWs.
6. **FX Chain AI Recommender** – Suggests plugin chains based on reference tracks or stems.

---

## 🛠️ Tech Stack

| Layer        | Tech                            |
|--------------|----------------------------------|
| Plugin       | C++ + JUCE (AU, VST3, AAX)       |
| DSP (Optional) | Rust                            |
| AI/ML        | Python (PyTorch, TensorFlow), ONNX |
| Backend      | Django (REST API), PostgreSQL    |
| Monetization | Stripe, tiered access            |

---

## 📦 Installation

1. Clone and build with CMake or open in Projucer/Xcode.
2. Deploy the `.component` to:
3. Open Logic Pro or other AU-compatible DAW.

---

## 🧪 Development Phases

See [roadmap/v1.0.md](./roadmap/v1.0.md) for module timelines.

---

## 💰 Pricing Tiers

| Tier     | Features                                                   | Price     |
|----------|------------------------------------------------------------|-----------|
| Free     | 1 AI FX/month, MIDI humanizer (lite), basic UI             | $0        |
| Creator  | Full AI mixing, session assistant                          | $15/month |
| Studio   | Genre FX chains, session recall, team collab               | $30/month |
| Pro      | All features + cloud sync, unlimited stems, priority AI    | $50/month |

---

## 🧠 Learn More

- [Project Plan](./PROJECT_PLAN.md)
- [Roadmap](./roadmap/v1.0.md)
- Backend: `/django_backend/` (coming soon)
