#!/usr/bin/env python3
"""
Apprendre Python — application d'apprentissage interactive en CLI.
Lancement : python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import ui as U
from app.lessons import LESSONS
from app.engine import run_lesson
from app import progress as P


def _lesson_label(lesson: dict) -> str:
    done = P.is_done(lesson["id"])
    sc   = P.get_score(lesson["id"])
    mark = f"{U.C.GREEN}✓{U.C.RESET} " if done else "  "
    score_str = ""
    if sc:
        score_str = f"  {U.C.DIM}({sc['score']}/{sc['max']}){U.C.RESET}"
    return f"{mark}{lesson['title']}{score_str}"


def menu_principal():
    while True:
        U.clear()
        U.banner()

        xp   = P.get_xp()
        done = sum(1 for l in LESSONS if P.is_done(l["id"]))
        total = len(LESSONS)

        print(f"  Progression : {U.progress_bar(done, total)}")
        print(f"  XP total    : {U.C.YELLOW}{U.C.BOLD}{xp} XP{U.C.RESET}")
        print()

        options = [_lesson_label(l) for l in LESSONS]
        options += ["Réinitialiser la progression", "Quitter"]

        choice = U.numbered_menu(options, "Choisis une leçon :")

        if choice <= len(LESSONS):
            lesson = LESSONS[choice - 1]
            run_lesson(lesson)
        elif choice == len(LESSONS) + 1:
            confirm = U.prompt("Confirmes-tu la réinitialisation ? (oui/non) : ")
            if confirm.lower() in ("oui", "o", "yes", "y"):
                P.reset()
                U.success("Progression réinitialisée !")
                U.ask_continue()
        else:
            U.clear()
            print(f"\n{U.C.CYAN}{U.C.BOLD}Merci d'avoir utilisé Apprendre Python !{U.C.RESET}")
            print(f"{U.C.DIM}Continue à coder, tu es sur la bonne voie ! 🐍{U.C.RESET}\n")
            sys.exit(0)


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(f"\n\n{U.C.DIM}À bientôt !{U.C.RESET}\n")
        sys.exit(0)
