#!/usr/bin/env python3
# ============================================================
#   MetaHunter — Metadata Extraction & Sanitization Tool
#   Built for Kali Linux | Cybersecurity & OSINT
# ============================================================

import os
import sys
import json
import csv
import subprocess
import shutil
import time
import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.columns import Columns
    from rich.rule import Rule
    from rich import box
    from rich.markup import escape
except ImportError:
    print("[!] Missing 'rich' library. Run: pip install rich")
    sys.exit(1)

W = 74  # Fixed UI width — keeps all panels/borders contained
console = Console(width=W)

# ─── Color Theme ─────────────────────────────────────────────
C_ACCENT   = "bright_cyan"
C_WARN     = "bright_yellow"
C_DANGER   = "bright_red"
C_SUCCESS  = "bright_green"
C_DIM      = "grey50"
C_TITLE    = "bold bright_cyan"

SUPPORTED_EXTENSIONS = {
    "Images":    [".jpg", ".jpeg", ".png", ".gif", ".tiff", ".tif", ".bmp", ".webp", ".heic", ".raw", ".cr2", ".nef"],
    "Audio":     [".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".aiff"],
    "Video":     [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"],
    "Documents": [".pdf", ".docx", ".xlsx", ".pptx", ".doc", ".odt", ".epub"],
    "Other":     [".zip", ".tar", ".gz", ".exe", ".apk"],
}

ALL_EXTENSIONS = [ext for exts in SUPPORTED_EXTENSIONS.values() for ext in exts]

BANNER = """
  █▀▄▀█ █▀▀ ▀█▀ ▄▀█   █░█ █░█ █▄░█ ▀█▀ █▀▀ █▀█
  █░▀░█ ██▄ ░█░ █▀█   █▀█ █▄█ █░▀█ ░█░ ██▄ █▀▄
"""

OUTPUT_DIR = Path("MetaHunter_Reports")


# ─── Utilities ────────────────────────────────────────────────

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def check_exiftool():
    return shutil.which("exiftool") is not None

def check_mat2():
    return shutil.which("mat2") is not None

def get_file_type(filepath: Path) -> str:
    ext = filepath.suffix.lower()
    for ftype, exts in SUPPORTED_EXTENSIONS.items():
        if ext in exts:
            return ftype
    return "Unknown"

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def ensure_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)


# ─── Display ─────────────────────────────────────────────────

def print_banner():
    clear()
    banner_text = Text(BANNER, style="bold bright_cyan")
    console.print(banner_text)
    console.print(
        Panel.fit(
            "[bold white]Metadata Extraction & Sanitization Framework[/bold white]\n"
            f"[{C_DIM}]For Kali Linux · OSINT · Digital Forensics · Privacy[/{C_DIM}]",
            border_style="cyan",
            padding=(0, 4),
        )
    )
    console.print()

def print_section(title: str):
    console.print()
    console.print(Rule(f"[bold cyan] {title} [/bold cyan]", style="cyan"), width=W)
    console.print()

def print_status():
    exif_ok  = check_exiftool()
    mat2_ok  = check_mat2()
    now      = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

    status_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    status_table.add_column(style="dim")
    status_table.add_column()

    status_table.add_row("exiftool",
        f"[{C_SUCCESS}]● Installed[/{C_SUCCESS}]" if exif_ok else f"[{C_DANGER}]✗ Not Found[/{C_DANGER}]")
    status_table.add_row("mat2",
        f"[{C_SUCCESS}]● Installed[/{C_SUCCESS}]" if mat2_ok else f"[{C_WARN}]○ Not Found (optional)[/{C_WARN}]")
    status_table.add_row("Time", f"[{C_DIM}]{now}[/{C_DIM}]")

    console.print(Panel(status_table, title="[bold]System Status[/bold]", border_style="cyan", padding=(0, 1)))
    console.print()

    if not exif_ok:
        console.print(f"[{C_DANGER}][!] exiftool is required. Install it:[/{C_DANGER}]")
        console.print(f"    [{C_ACCENT}]sudo apt install libimage-exiftool-perl[/{C_ACCENT}]\n")


# ─── Main Menu ────────────────────────────────────────────────

def main_menu() -> str:
    options = Table(box=box.ROUNDED, border_style="cyan", show_header=False, padding=(0, 2))
    options.add_column(style=f"bold {C_ACCENT}", width=4)
    options.add_column(style="bold white")
    options.add_column(style=C_DIM)

    options.add_row("  1", "Extract Metadata",        "Pull all metadata from a file")
    options.add_row("  2", "Batch Extract",            "Extract metadata from all files in a folder")
    options.add_row("  3", "Strip Metadata",           "Remove metadata from a file (creates clean copy)")
    options.add_row("  4", "Batch Strip",              "Strip metadata from all files in a folder")
    options.add_row("  5", "Export Report",            "Save last extraction to JSON / CSV / TXT")
    options.add_row("  6", "Supported File Types",     "View all supported formats")
    options.add_row("  7", "Help & Usage Guide",       "How to use MetaHunter")
    options.add_row("  0", "Exit",                     "Quit MetaHunter")

    console.print(Panel(options, title="[bold]Main Menu[/bold]", border_style="cyan"))
    console.print()
    choice = Prompt.ask(f"[{C_ACCENT}]metahunter[/{C_ACCENT}]", default="1")
    return choice.strip()


# ─── Metadata Extraction ──────────────────────────────────────

def run_exiftool(filepath: Path) -> dict:
    """Run exiftool and return parsed JSON metadata."""
    result = subprocess.run(
        ["exiftool", "-json", "-a", "-u", str(filepath)],
        capture_output=True, text=True
    )
    if result.returncode != 0 or not result.stdout.strip():
        return {}
    try:
        data = json.loads(result.stdout)
        return data[0] if data else {}
    except json.JSONDecodeError:
        return {}

def display_metadata(metadata: dict, filepath: Path):
    """Render metadata in a formatted rich table."""
    if not metadata:
        console.print(f"[{C_WARN}][!] No metadata found or file not supported.[/{C_WARN}]")
        return

    ftype = get_file_type(filepath)

    # Summary Panel
    summary = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    summary.add_column(style="dim", width=20)
    summary.add_column(style="white")
    summary.add_row("File",      escape(filepath.name))
    summary.add_row("Type",      ftype)
    summary.add_row("Size",      metadata.get("FileSize", "Unknown"))
    summary.add_row("Modified",  metadata.get("FileModifyDate", "Unknown"))
    summary.add_row("MIME",      metadata.get("MIMEType", "Unknown"))

    console.print(Panel(summary, title=f"[bold]{escape(filepath.name)}[/bold]", border_style="cyan"))

    # Metadata Table
    skip_keys = {"SourceFile", "ExifToolVersion", "Directory", "FilePermissions"}
    priority_groups = {
        "📍 Location":    ["GPSLatitude", "GPSLongitude", "GPSAltitude", "GPSPosition", "GPSLatitudeRef", "GPSLongitudeRef"],
        "👤 Author / Device": ["Author", "Creator", "Artist", "Make", "Model", "LensModel", "Software", "Producer", "CreatorTool"],
        "🕒 Timestamps":  ["CreateDate", "ModifyDate", "DateTimeOriginal", "MetadataDate", "TrackCreateDate"],
        "📷 Camera Settings": ["ExposureTime", "FNumber", "ISO", "FocalLength", "Flash", "WhiteBalance", "ExposureMode"],
        "📄 Document Info": ["Title", "Subject", "Description", "Keywords", "PageCount", "Language", "Company"],
        "🎵 Audio/Video": ["Duration", "AudioBitrate", "SampleRate", "VideoFrameRate", "ImageWidth", "ImageHeight", "ImageSize"],
        "🔒 Other Fields": [],
    }

    grouped = {g: [] for g in priority_groups}

    for key, val in metadata.items():
        if key in skip_keys:
            continue
        placed = False
        for group, keys in priority_groups.items():
            if group == "🔒 Other Fields":
                continue
            if key in keys:
                grouped[group].append((key, str(val)))
                placed = True
                break
        if not placed:
            grouped["🔒 Other Fields"].append((key, str(val)))

    for group, rows in grouped.items():
        if not rows:
            continue
        tbl = Table(box=box.SIMPLE_HEAD, border_style="cyan", show_header=True, padding=(0, 1))
        tbl.add_column("Field",  style=f"bold {C_ACCENT}", width=32)
        tbl.add_column("Value",  style="white", overflow="fold")

        for k, v in rows:
            # Highlight GPS data in red as privacy risk
            if "GPS" in k or "Latitude" in k or "Longitude" in k:
                tbl.add_row(k, f"[{C_DANGER}]{escape(v)} ⚠ GPS RISK[/{C_DANGER}]")
            elif any(x in k for x in ["Author", "Creator", "Artist", "Company", "Producer"]):
                tbl.add_row(k, f"[{C_WARN}]{escape(v)} ⚠ PII[/{C_WARN}]")
            else:
                tbl.add_row(k, escape(v))

        console.print(Panel(tbl, title=f"[bold]{group}[/bold]", border_style="cyan", padding=(0, 0)))

    # Risk summary
    has_gps = any("GPS" in k for k in metadata)
    has_pii = any(k in metadata for k in ["Author", "Creator", "Artist", "Company", "Producer"])

    if has_gps or has_pii:
        risks = []
        if has_gps:  risks.append(f"[{C_DANGER}]● GPS coordinates detected — location may be exposed[/{C_DANGER}]")
        if has_pii:  risks.append(f"[{C_WARN}]● Author/Creator info detected — personal data present[/{C_WARN}]")
        console.print(Panel("\n".join(risks), title="[bold red]⚠  Privacy Risk Summary[/bold red]", border_style="red"))

    return metadata


def extract_metadata(filepath_str: str) -> dict:
    """Entry point: extract metadata from a single file."""
    filepath = Path(filepath_str.strip().strip("'\""))

    if not filepath.exists():
        console.print(f"[{C_DANGER}][✗] File not found: {escape(str(filepath))}[/{C_DANGER}]")
        return {}

    if not check_exiftool():
        console.print(f"[{C_DANGER}][✗] exiftool is not installed.[/{C_DANGER}]")
        return {}

    console.print(f"\n[{C_DIM}]Analyzing:[/{C_DIM}] [bold]{escape(filepath.name)}[/bold] ...\n")

    with Progress(SpinnerColumn(), TextColumn("[cyan]Extracting metadata..."), transient=True) as p:
        p.add_task("", total=None)
        time.sleep(0.6)
        metadata = run_exiftool(filepath)

    display_metadata(metadata, filepath)
    return metadata


def batch_extract(folder_str: str) -> list:
    """Extract metadata from all supported files in a folder."""
    folder = Path(folder_str.strip().strip("'\""))

    if not folder.is_dir():
        console.print(f"[{C_DANGER}][✗] Directory not found: {escape(str(folder))}[/{C_DANGER}]")
        return []

    files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in ALL_EXTENSIONS]

    if not files:
        console.print(f"[{C_WARN}][!] No supported files found in that directory.[/{C_WARN}]")
        return []

    console.print(f"\n[{C_SUCCESS}][✓] Found {len(files)} supported file(s)[/{C_SUCCESS}]\n")
    results = []

    for i, f in enumerate(files, 1):
        console.print(f"[{C_DIM}][{i}/{len(files)}][/{C_DIM}] Processing: [bold]{escape(f.name)}[/bold]")
        meta = run_exiftool(f)
        if meta:
            results.append({"file": str(f), "metadata": meta})
            ftype = get_file_type(f)
            has_gps = any("GPS" in k for k in meta)
            has_pii = any(k in meta for k in ["Author", "Creator", "Artist"])
            flags = ""
            if has_gps: flags += f" [{C_DANGER}][GPS][/{C_DANGER}]"
            if has_pii: flags += f" [{C_WARN}][PII][/{C_WARN}]"
            console.print(f"    [{C_SUCCESS}]✓[/{C_SUCCESS}] {ftype} · {meta.get('FileSize','?')}{flags}")
        else:
            console.print(f"    [{C_WARN}]○ No metadata extracted[/{C_WARN}]")

    console.print(f"\n[{C_SUCCESS}][✓] Batch extraction complete: {len(results)}/{len(files)} files processed[/{C_SUCCESS}]")
    return results


# ─── Metadata Stripping ───────────────────────────────────────

def strip_metadata(filepath_str: str):
    """Remove all metadata from a file using exiftool."""
    filepath = Path(filepath_str.strip().strip("'\""))

    if not filepath.exists():
        console.print(f"[{C_DANGER}][✗] File not found.[/{C_DANGER}]")
        return

    if not check_exiftool():
        console.print(f"[{C_DANGER}][✗] exiftool is not installed.[/{C_DANGER}]")
        return

    ensure_output_dir()
    clean_name = f"CLEAN_{filepath.stem}_{timestamp()}{filepath.suffix}"
    clean_path = OUTPUT_DIR / clean_name

    # Copy original then strip metadata from copy
    import shutil as sh
    sh.copy2(filepath, clean_path)

    console.print(f"\n[{C_DIM}]Stripping metadata from:[/{C_DIM}] [bold]{escape(filepath.name)}[/bold]\n")

    with Progress(SpinnerColumn(), TextColumn("[cyan]Removing metadata..."), transient=True) as p:
        p.add_task("", total=None)
        result = subprocess.run(
            ["exiftool", "-all=", "-overwrite_original", str(clean_path)],
            capture_output=True, text=True
        )

    if result.returncode == 0:
        console.print(Panel(
            f"[{C_SUCCESS}]✓ Metadata stripped successfully[/{C_SUCCESS}]\n\n"
            f"[bold]Original:[/bold] [{C_DIM}]{escape(str(filepath))}[/{C_DIM}]\n"
            f"[bold]Clean copy:[/bold] [{C_SUCCESS}]{escape(str(clean_path))}[/{C_SUCCESS}]\n\n"
            f"[{C_DIM}]The original file was NOT modified.[/{C_DIM}]",
            title="[bold green]Strip Complete[/bold green]",
            border_style="green"
        ))
    else:
        console.print(f"[{C_DANGER}][✗] Strip failed: {escape(result.stderr)}[/{C_DANGER}]")


def batch_strip(folder_str: str):
    """Strip metadata from all supported files in a folder."""
    folder = Path(folder_str.strip().strip("'\""))

    if not folder.is_dir():
        console.print(f"[{C_DANGER}][✗] Directory not found.[/{C_DANGER}]")
        return

    files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in ALL_EXTENSIONS]

    if not files:
        console.print(f"[{C_WARN}][!] No supported files found.[/{C_WARN}]")
        return

    console.print(f"\n[{C_WARN}][!] This will create clean copies of {len(files)} file(s) in:[/{C_WARN}]")
    console.print(f"    [{C_ACCENT}]{OUTPUT_DIR.resolve()}[/{C_ACCENT}]")
    console.print(f"[{C_DIM}]    Original files will NOT be modified.[/{C_DIM}]\n")

    if not Confirm.ask(f"[{C_WARN}]Proceed?[/{C_WARN}]"):
        return

    ensure_output_dir()
    success, failed = 0, 0

    import shutil as sh
    for i, f in enumerate(files, 1):
        clean_name = f"CLEAN_{f.stem}_{timestamp()}{f.suffix}"
        clean_path = OUTPUT_DIR / clean_name
        sh.copy2(f, clean_path)

        result = subprocess.run(
            ["exiftool", "-all=", "-overwrite_original", str(clean_path)],
            capture_output=True, text=True
        )
        status = f"[{C_SUCCESS}]✓[/{C_SUCCESS}]" if result.returncode == 0 else f"[{C_DANGER}]✗[/{C_DANGER}]"
        if result.returncode == 0: success += 1
        else: failed += 1
        console.print(f"  {status} [{i}/{len(files)}] {escape(f.name)}")

    console.print(f"\n[{C_SUCCESS}][✓] Done — {success} stripped, {failed} failed[/{C_SUCCESS}]")


# ─── Export Report ────────────────────────────────────────────

def export_report(metadata: dict | list):
    """Export metadata to JSON, CSV, or TXT."""
    if not metadata:
        console.print(f"[{C_WARN}][!] No metadata to export. Run an extraction first.[/{C_WARN}]")
        return

    ensure_output_dir()
    print_section("Export Report")

    fmt_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    fmt_table.add_column(style=f"bold {C_ACCENT}", width=4)
    fmt_table.add_column(style="white")
    fmt_table.add_row("1", "JSON   — structured, machine-readable")
    fmt_table.add_row("2", "CSV    — spreadsheet-compatible")
    fmt_table.add_row("3", "TXT    — human-readable plain text")
    console.print(fmt_table)

    fmt = Prompt.ask(f"[{C_ACCENT}]Format[/{C_ACCENT}]", choices=["1","2","3"], default="1")
    fname = f"MetaHunter_Report_{timestamp()}"

    if fmt == "1":
        out = OUTPUT_DIR / f"{fname}.json"
        with open(out, "w") as fh:
            json.dump(metadata, fh, indent=2, default=str)

    elif fmt == "2":
        out = OUTPUT_DIR / f"{fname}.csv"
        data = metadata if isinstance(metadata, dict) else metadata[0].get("metadata", {})
        with open(out, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["Field", "Value"])
            for k, v in data.items():
                writer.writerow([k, v])

    elif fmt == "3":
        out = OUTPUT_DIR / f"{fname}.txt"
        data = metadata if isinstance(metadata, dict) else metadata
        with open(out, "w") as fh:
            fh.write("MetaHunter Report\n")
            fh.write("=" * 60 + "\n")
            fh.write(f"Generated: {datetime.datetime.now()}\n\n")
            if isinstance(data, dict):
                for k, v in data.items():
                    fh.write(f"{k:<35} {v}\n")
            else:
                for entry in data:
                    fh.write(f"\nFile: {entry['file']}\n")
                    fh.write("-" * 40 + "\n")
                    for k, v in entry["metadata"].items():
                        fh.write(f"  {k:<33} {v}\n")

    console.print(Panel(
        f"[{C_SUCCESS}]✓ Report saved:[/{C_SUCCESS}]\n[bold]{escape(str(out.resolve()))}[/bold]",
        border_style="green"
    ))


# ─── Info Screens ─────────────────────────────────────────────

def show_supported_types():
    print_section("Supported File Types")
    for category, exts in SUPPORTED_EXTENSIONS.items():
        t = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        t.add_column(style=f"bold {C_ACCENT}", width=16)
        t.add_column(style=C_DIM)
        for ext in exts:
            t.add_row(ext, "")
        console.print(Panel(t, title=f"[bold]{category}[/bold]", border_style="cyan", padding=(0,0)))


def show_help():
    print_section("Help & Usage Guide")
    console.print(Panel(
        f"""[bold {C_ACCENT}]What is MetaHunter?[/bold {C_ACCENT}]
MetaHunter is a metadata analysis and sanitization tool for security
professionals. It uses [bold]exiftool[/bold] to extract hidden data embedded in files
that can reveal sensitive information like GPS location, device model,
author names, software used, and creation timestamps.

[bold {C_ACCENT}]Why Does Metadata Matter?[/bold {C_ACCENT}]
Every file you create or share may contain hidden metadata:
  [{C_DANGER}]⚠[/{C_DANGER}] Photos can leak your exact GPS coordinates
  [{C_WARN}]⚠[/{C_WARN}] Documents can expose your name, company, and software
  [{C_WARN}]⚠[/{C_WARN}] Audio files can reveal recording device and software info

[bold {C_ACCENT}]Workflow[/bold {C_ACCENT}]
  1. Extract metadata → inspect what's hidden in a file
  2. Review the Privacy Risk Summary at the bottom
  3. Strip metadata → create a clean version before sharing
  4. Export a report → save findings as JSON / CSV / TXT

[bold {C_ACCENT}]Tips[/bold {C_ACCENT}]
  • Always strip metadata from photos before posting online
  • Use batch extract on folders from seized devices (forensics)
  • Export JSON reports to import into other security tools
  • metahunter never modifies original files — only creates copies

[bold {C_ACCENT}]Requirements[/bold {C_ACCENT}]
  [{C_SUCCESS}]●[/{C_SUCCESS}] exiftool     [dim]sudo apt install libimage-exiftool-perl[/dim]
  [{C_DIM}]○[/{C_DIM}] mat2 (opt)   [dim]sudo apt install mat2[/dim]
""",
        title="[bold]MetaHunter — Help Guide[/bold]",
        border_style="cyan",
        padding=(1, 2),
    ))


# ─── Main Loop ────────────────────────────────────────────────

def main():
    last_metadata = None

    while True:
        print_banner()
        print_status()
        choice = main_menu()

        if choice == "0":
            console.print(f"\n[{C_DIM}]Goodbye. Stay secure.[/{C_DIM}]\n")
            break

        elif choice == "1":
            print_section("Extract Metadata — Single File")
            console.print(f"[{C_DIM}]Drag a file here or enter its full path:[/{C_DIM}]")
            path = Prompt.ask(f"[{C_ACCENT}]File path[/{C_ACCENT}]")
            result = extract_metadata(path)
            if result:
                last_metadata = result
                if Confirm.ask(f"\n[{C_DIM}]Export this report?[/{C_DIM}]", default=False):
                    export_report(last_metadata)

        elif choice == "2":
            print_section("Batch Extract — Entire Folder")
            console.print(f"[{C_DIM}]Enter the folder path:[/{C_DIM}]")
            path = Prompt.ask(f"[{C_ACCENT}]Folder path[/{C_ACCENT}]")
            results = batch_extract(path)
            if results:
                last_metadata = results
                if Confirm.ask(f"\n[{C_DIM}]Export batch report?[/{C_DIM}]", default=False):
                    export_report(last_metadata)

        elif choice == "3":
            print_section("Strip Metadata — Single File")
            console.print(f"[{C_WARN}]A clean copy will be created. The original is NEVER modified.[/{C_WARN}]")
            console.print(f"[{C_DIM}]Enter file path:[/{C_DIM}]")
            path = Prompt.ask(f"[{C_ACCENT}]File path[/{C_ACCENT}]")
            strip_metadata(path)

        elif choice == "4":
            print_section("Batch Strip — Entire Folder")
            path = Prompt.ask(f"[{C_ACCENT}]Folder path[/{C_ACCENT}]")
            batch_strip(path)

        elif choice == "5":
            export_report(last_metadata)

        elif choice == "6":
            show_supported_types()

        elif choice == "7":
            show_help()

        else:
            console.print(f"[{C_WARN}][!] Invalid option.[/{C_WARN}]")

        console.print()
        Prompt.ask(f"[{C_DIM}]Press Enter to return to menu[/{C_DIM}]", default="")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n\n[{C_DIM}]Interrupted. Goodbye.[/{C_DIM}]\n")
        sys.exit(0)
