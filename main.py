#!/usr/bin/env python3
"""
Audit Sentinel - DSGVO/GDPR Code Scanner
Einstiegspunkt für die Kommandozeilennutzung

Verwendung:
    python main.py scan ./mein_projekt
    python main.py scan ./mein_projekt --ai --api-key DEIN_GEMINI_KEY
    python main.py scan einzelne_datei.py
"""

import sys
import argparse
from pathlib import Path
from src.scanner import scan_directory, scan_file_static, analyze_with_gemini, generate_report

# ── Farben für Terminal-Output ──
COLORS = {
    "KRITISCH": "\033[91m",  # Rot
    "HOCH":     "\033[93m",  # Gelb
    "MITTEL":   "\033[94m",  # Blau
    "NIEDRIG":  "\033[92m",  # Grün
    "RESET":    "\033[0m",
    "BOLD":     "\033[1m",
    "CYAN":     "\033[96m",
}


def print_banner():
    print(f"""
{COLORS['CYAN']}{COLORS['BOLD']}
 █████╗ ██╗   ██╗██████╗ ██╗████████╗    ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
██╔══██╗██║   ██║██╔══██╗██║╚══██╔══╝    ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║
███████║██║   ██║██║  ██║██║   ██║       ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║
██╔══██║██║   ██║██║  ██║██║   ██║       ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║
██║  ██║╚██████╔╝██████╔╝██║   ██║       ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝   ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
{COLORS['RESET']}
{COLORS['BOLD']}  DSGVO / GDPR Code Compliance Scanner  |  v0.1.0  |  by Tobias Hettmer{COLORS['RESET']}
""")


def print_finding(finding: dict):
    severity = finding.get("schweregrad", "UNBEKANNT")
    color = COLORS.get(severity, COLORS["RESET"])
    print(f"  {color}{COLORS['BOLD']}[{severity}]{COLORS['RESET']} {finding['beschreibung']}")
    print(f"    📄 Datei : {finding['datei']}")
    print(f"    📍 Zeile : {finding['zeile']}")
    print(f"    💻 Code  : {finding['code']}")
    print()


def print_summary(findings: list[dict]):
    counts = {
        "KRITISCH": sum(1 for f in findings if f.get("schweregrad") == "KRITISCH"),
        "HOCH":     sum(1 for f in findings if f.get("schweregrad") == "HOCH"),
        "MITTEL":   sum(1 for f in findings if f.get("schweregrad") == "MITTEL"),
        "NIEDRIG":  sum(1 for f in findings if f.get("schweregrad") == "NIEDRIG"),
    }
    print(f"\n{COLORS['BOLD']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}  ZUSAMMENFASSUNG{COLORS['RESET']}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  {COLORS['KRITISCH'] if counts['KRITISCH'] else ''}🔴 KRITISCH : {counts['KRITISCH']}{COLORS['RESET']}")
    print(f"  {COLORS['HOCH'] if counts['HOCH'] else ''}🟡 HOCH     : {counts['HOCH']}{COLORS['RESET']}")
    print(f"  {COLORS['MITTEL'] if counts['MITTEL'] else ''}🔵 MITTEL   : {counts['MITTEL']}{COLORS['RESET']}")
    print(f"  {COLORS['NIEDRIG'] if counts['NIEDRIG'] else ''}🟢 NIEDRIG  : {counts['NIEDRIG']}{COLORS['RESET']}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    total = sum(counts.values())
    if total == 0:
        print(f"  ✅ Keine Befunde! Code sieht DSGVO-konform aus.")
    else:
        print(f"  ⚠️  {total} Befund(e) gefunden. Bitte prüfen!")
    print()


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Audit Sentinel – DSGVO Code Scanner"
    )
    subparsers = parser.add_subparsers(dest="command")

    # scan command
    scan_parser = subparsers.add_parser("scan", help="Scanne eine Datei oder ein Verzeichnis")
    scan_parser.add_argument("path", help="Pfad zur Datei oder zum Verzeichnis")
    scan_parser.add_argument("--ai", action="store_true", help="KI-Analyse via Google Gemini aktivieren")
    scan_parser.add_argument("--api-key", help="Google Gemini API Key")
    scan_parser.add_argument("--report", help="JSON-Report speichern unter diesem Pfad", default=None)

    args = parser.parse_args()

    if args.command == "scan":
        target = Path(args.path)

        if not target.exists():
            print(f"❌ Pfad nicht gefunden: {args.path}")
            sys.exit(1)

        print(f"{COLORS['BOLD']}🔍 Scanne: {target.resolve()}{COLORS['RESET']}\n")

        # Static scan
        if target.is_file():
            findings = scan_file_static(str(target))
        else:
            findings = scan_directory(str(target))

        if not findings:
            print("  ✅ Keine statischen Befunde gefunden.\n")
        else:
            print(f"{COLORS['BOLD']}  Gefundene Probleme:{COLORS['RESET']}\n")
            for f in findings:
                print_finding(f)

        # Optional AI analysis
        if args.ai:
            if not args.api_key:
                print("⚠️  Bitte --api-key angeben für KI-Analyse.")
            else:
                print(f"\n{COLORS['CYAN']}{COLORS['BOLD']}🤖 KI-Analyse via Google Gemini...{COLORS['RESET']}\n")
                if target.is_file():
                    code = target.read_text(encoding="utf-8", errors="ignore")
                else:
                    # Combine first 3 files for AI analysis (token limit)
                    py_files = list(target.rglob("*.py"))[:3]
                    code = "\n\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in py_files)

                ai_result = analyze_with_gemini(code, args.api_key)
                print(ai_result)

        print_summary(findings)

        # Optional report
        if args.report:
            path = generate_report(findings, args.report)
            print(f"📊 Report gespeichert: {path}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
