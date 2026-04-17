# 🛡️ Audit Sentinel

**DSGVO / GDPR Code Compliance Scanner**

Audit Sentinel scans Python codebases for potential GDPR (DSGVO) violations using static code analysis and optional AI-powered deep analysis via Google Gemini.

> ⚠️ This tool assists developers in identifying potential DSGVO risks. It does **not** replace legal advice or a formal data protection audit.

---

## ✨ Features

- 🔍 **Static Analysis** – Pattern-based detection of common DSGVO violations (no API key needed)
- 🤖 **AI-Powered Analysis** – Deep analysis via Google Gemini API for complex code patterns
- 📊 **Severity Levels** – KRITISCH / HOCH / MITTEL / NIEDRIG
- 📄 **JSON Reports** – Machine-readable output for CI/CD integration
- 🖥️ **CLI Interface** – Simple command-line usage

---

## 🚀 Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/aepydraco/audit-sentinel.git
cd audit-sentinel
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Scan your code

```bash
# Scan a single file
python main.py scan meine_datei.py

# Scan an entire directory
python main.py scan ./mein_projekt

# With AI analysis (requires free Google Gemini API key)
python main.py scan ./mein_projekt --ai --api-key DEIN_GEMINI_API_KEY

# Save a JSON report
python main.py scan ./mein_projekt --report report.json
```

---

## 🔍 What Audit Sentinel detects

| Regel | Schweregrad | Beschreibung |
|---|---|---|
| `hardcoded_personal_data` | 🔴 KRITISCH | Hardcodierte E-Mails, Namen, Telefonnummern |
| `logging_personal_data` | 🟡 HOCH | Persönliche Daten in Logs |
| `third_party_data_sharing` | 🟡 HOCH | Datenübermittlung an Dritte |
| `unencrypted_storage` | 🟡 HOCH | Unverschlüsselte Speicherung sensibler Daten |
| `no_consent_check` | 🔵 MITTEL | Fehlende Einwilligungsprüfung |
| `missing_deletion` | 🔵 MITTEL | Kein Löschmechanismus für Nutzerdaten |

---

## 🤖 AI Analysis (optional)

Get a **free** Google Gemini API key at [aistudio.google.com](https://aistudio.google.com).

The AI analysis sends code snippets to Gemini for deeper DSGVO analysis including:
- Identification of affected DSGVO articles (Art. 5, 6, 17, 25...)
- Context-aware risk assessment
- Concrete remediation suggestions

---

## 📁 Project Structure

```
audit-sentinel/
├── main.py                          # CLI entry point
├── requirements.txt                 # Dependencies
├── src/
│   └── scanner.py                   # Core scanning logic
└── tests/
    └── beispiel_dsgvo_probleme.py   # Example file with DSGVO issues (for testing)
```

---

## 🗺️ Roadmap

- [ ] HTML report export
- [ ] Support for JavaScript / TypeScript
- [ ] GitHub Actions integration
- [ ] DSGVO article mapping (Art. 5, 6, 17, 25...)
- [ ] Web UI Dashboard
- [ ] Auto-fix suggestions

---

## 📄 License

MIT License – see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Tobias Hettmer**  
Fachinformatiker für Anwendungsentwicklung  
[GitHub](https://github.com/DEIN-USERNAME)

---

*Built with Python 🐍 and a passion for privacy 🛡️*
