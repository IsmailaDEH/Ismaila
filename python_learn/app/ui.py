import os
import sys
import time


class Colors:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BG_BLUE = "\033[44m"
    BG_GREEN= "\033[42m"

C = Colors


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════╗
║     🐍  Apprendre Python — Cours Interactif  🐍  ║
╚══════════════════════════════════════════════════╝{C.RESET}
""")


def title(text: str):
    width = 52
    line = "─" * width
    print(f"\n{C.BLUE}{C.BOLD}┌{line}┐")
    print(f"│  {text:<{width - 2}}│")
    print(f"└{line}┘{C.RESET}\n")


def section(text: str):
    print(f"\n{C.YELLOW}{C.BOLD}▶  {text}{C.RESET}")
    print(f"{C.DIM}{'─' * 54}{C.RESET}")


def info(text: str):
    print(f"{C.CYAN}ℹ  {text}{C.RESET}")


def success(text: str):
    print(f"{C.GREEN}{C.BOLD}✓  {text}{C.RESET}")


def error(text: str):
    print(f"{C.RED}{C.BOLD}✗  {text}{C.RESET}")


def warning(text: str):
    print(f"{C.YELLOW}⚠  {text}{C.RESET}")


def code_block(code: str):
    print(f"\n{C.DIM}┌── Python ──────────────────────────────────────┐{C.RESET}")
    for line in code.strip().split("\n"):
        print(f"{C.DIM}│{C.RESET}  {C.GREEN}{line}{C.RESET}")
    print(f"{C.DIM}└────────────────────────────────────────────────┘{C.RESET}\n")


def progress_bar(done: int, total: int, width: int = 30):
    pct = done / total if total else 0
    filled = int(width * pct)
    bar = f"{C.GREEN}{'█' * filled}{C.DIM}{'░' * (width - filled)}{C.RESET}"
    return f"[{bar}] {C.BOLD}{done}/{total}{C.RESET}"


def prompt(text: str = "") -> str:
    try:
        return input(f"{C.MAGENTA}❯ {text}{C.RESET}").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return ""


def ask_continue():
    prompt("Appuie sur Entrée pour continuer…")


def typewrite(text: str, delay: float = 0.012):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def numbered_menu(options: list[str], title_text: str = "Que veux-tu faire ?") -> int:
    print(f"\n{C.BOLD}{title_text}{C.RESET}")
    for i, opt in enumerate(options, 1):
        print(f"  {C.CYAN}{i}{C.RESET}. {opt}")
    print()
    while True:
        raw = prompt()
        if raw.isdigit():
            n = int(raw)
            if 1 <= n <= len(options):
                return n
        error(f"Saisis un nombre entre 1 et {len(options)}")
