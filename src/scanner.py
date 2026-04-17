"""
Audit Sentinel - DSGVO/GDPR Code Scanner
Core scanning module with static analysis + AI-powered analysis via Google Gemini
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Optional


# ──────────────────────────────────────────────
# Static pattern rules (no API needed)
# ──────────────────────────────────────────────

DSGVO_PATTERNS = {
    "hardcoded_personal_data": {
        "severity": "KRITISCH",
        "description": "Hardcodierte persönliche Daten gefunden",
        "patterns": [
            r'email\s*=\s*["\'][^"\']+@[^"\']+["\']',
            r'phone\s*=\s*["\'][\d\s\+\-\(\)]+["\']',
            r'(vorname|nachname|geburtsdatum|name)\s*=\s*["\'][^"\']{2,}["\']',
        ],
    },
    "unencrypted_storage": {
        "severity": "HOCH",
        "description": "Mögliche unverschlüsselte Speicherung sensibler Daten",
        "patterns": [
            r'open\(.+["\']w["\'].+\).*password',
            r'pickle\.dump.*personal',
            r'json\.dump.*email',
        ],
    },
    "logging_personal_data": {
        "severity": "HOCH",
        "description": "Persönliche Daten könnten in Logs landen",
        "patterns": [
            r'(print|logging\.(info|debug|warning|error))\s*\(.*?(email|password|name|phone|passwort)',
            r'logger\.(info|debug)\s*\(.*?(user|nutzer|kunde)',
        ],
    },
    "missing_deletion": {
        "severity": "MITTEL",
        "description": "Kein Löschmechanismus für Nutzerdaten erkennbar",
        "patterns": [
            r'def\s+create_user|def\s+save_user|def\s+register',
        ],
        "require_absence": r'def\s+(delete_user|remove_user|daten_loeschen)',
    },
    "third_party_data_sharing": {
        "severity": "HOCH",
        "description": "Datenübermittlung an Dritte ohne erkennbare Einwilligung",
        "patterns": [
            r'requests\.(post|put)\s*\(.+\)',
        ],
    },
    "no_consent_check": {
        "severity": "MITTEL",
        "description": "Fehlende Einwilligungsprüfung vor Datenverarbeitung",
        "patterns": [
            r'def\s+process_data|def\s+analyze_user|def\s+collect',
        ],
        "require_absence": r'(consent|einwilligung|zustimmung|approved)',
    },
}


def scan_file_static(filepath: str) -> list[dict]:
    """Run static pattern analysis on a single file."""
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.splitlines()
    except Exception as e:
        return [{"type": "scan_error", "file": filepath, "message": str(e)}]

    for rule_id, rule in DSGVO_PATTERNS.items():
        for pattern in rule["patterns"]:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    # Check require_absence rules (whole file scope)
                    if "require_absence" in rule:
                        if re.search(rule["require_absence"], content, re.IGNORECASE):
                            continue  # Mitigation found, skip
                    findings.append(
                        {
                            "regel": rule_id,
                            "schweregrad": rule["severity"],
                            "beschreibung": rule["description"],
                            "datei": filepath,
                            "zeile": i,
                            "code": line.strip(),
                        }
                    )

    return findings


def scan_directory(path: str) -> list[dict]:
    """Scan all Python files in a directory recursively."""
    all_findings = []
    p = Path(path)
    py_files = list(p.rglob("*.py"))

    if not py_files:
        print(f"  Keine Python-Dateien in '{path}' gefunden.")
        return []

    for py_file in py_files:
        findings = scan_file_static(str(py_file))
        all_findings.extend(findings)

    return all_findings


# ──────────────────────────────────────────────
# AI-powered analysis via Google Gemini
# ──────────────────────────────────────────────

def analyze_with_gemini(code_snippet: str, api_key: str) -> Optional[str]:
    """
    Send a code snippet to Google Gemini for deeper DSGVO analysis.
    Requires: pip install google-generativeai
    """
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
Du bist ein DSGVO-Experte und Code-Auditor. Analysiere den folgenden Python-Code
auf Verstöße oder Risiken bezüglich der DSGVO (Datenschutz-Grundverordnung).

Gib deine Antwort strukturiert aus:
1. Gefundene Risiken (mit Schweregrad: KRITISCH / HOCH / MITTEL / NIEDRIG)
2. Betroffene Artikel der DSGVO
3. Empfehlung zur Behebung

Code:
```python
{code_snippet}
```
"""
        response = model.generate_content(prompt)
        return response.text

    except ImportError:
        return "⚠️  google-generativeai nicht installiert. Führe aus: pip install google-generativeai"
    except Exception as e:
        return f"⚠️  Gemini API Fehler: {str(e)}"


# ──────────────────────────────────────────────
# Report generation
# ──────────────────────────────────────────────

def generate_report(findings: list[dict], output_path: str = "report.json") -> str:
    """Save findings to a structured JSON report."""
    report = {
        "audit_sentinel_version": "0.1.0",
        "anzahl_befunde": len(findings),
        "befunde": findings,
        "zusammenfassung": {
            "KRITISCH": sum(1 for f in findings if f.get("schweregrad") == "KRITISCH"),
            "HOCH": sum(1 for f in findings if f.get("schweregrad") == "HOCH"),
            "MITTEL": sum(1 for f in findings if f.get("schweregrad") == "MITTEL"),
            "NIEDRIG": sum(1 for f in findings if f.get("schweregrad") == "NIEDRIG"),
        },
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return output_path
