# 🛡️ Sentinel-Node : Architecture Honeypot & Monitoring Réseau

Sonde d'écoute conteneurisée et capture passive d'intrusions réseau pour l'analyse télémétrique des vecteurs d'attaque.

## 📊 Fonctionnalités & Architecture
- **Sondes de capture multi-ports :** Leurre de services courants (SSH port 2222, HTTP port 8080).
- **Journalisation structurée :** Parsing et export des métriques d'attaque en continu au format JSON (IP source, port, payload brut, horodatage).
- **Conteneurisation :** Déploiement isolé et reproductible via **Docker** et **Docker-Compose**.
- **Supervision :** Export des indicateurs d'attaques vers des tableaux de bord **Grafana**.

## 🛠️ Stack Technique
- **Backend & Détection :** Python (Sockets, Threading, Logging)
- **Déploiement & Métriques :** Docker, Docker-Compose, Grafana

## 🚀 Installation & Exécution
```bash
# Lancement avec Docker Compose
docker-compose up -d --build

# Ou exécution locale directe
python sentinel_honeypot.py
