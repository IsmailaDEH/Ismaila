"""
Core learning engine: displays theory, runs quizzes, and evaluates exercises.
"""

from . import ui as U
from .runner import check_exercise
from . import progress as P


def _show_theory(lesson: dict):
    U.clear()
    U.banner()
    U.title(f"Leçon : {lesson['title']}")

    for item in lesson["theory"]:
        label = item[0]
        text  = item[1] if len(item) > 1 else None
        code  = item[2] if len(item) > 2 else None

        if code is not None:
            U.section(label)
            if text:
                print(f"  {text}\n")
            U.code_block(code)
        else:
            U.section(label)
            if text:
                for line in text.split("\n"):
                    print(f"  {line}")
            print()

        U.ask_continue()


def _run_quiz(lesson: dict) -> tuple[int, int]:
    questions = lesson.get("quiz", [])
    if not questions:
        return 0, 0

    score = 0
    U.clear()
    U.banner()
    U.title(f"Quiz — {lesson['title']}")

    for i, q in enumerate(questions, 1):
        U.section(f"Question {i}/{len(questions)}")
        print(f"  {U.C.BOLD}{q['question']}{U.C.RESET}\n")
        for j, choice in enumerate(q["choices"], 1):
            print(f"    {U.C.CYAN}{j}{U.C.RESET}. {choice}")
        print()

        while True:
            raw = U.prompt("Ton choix (numéro) : ")
            if raw.isdigit() and 1 <= int(raw) <= len(q["choices"]):
                break
            U.error("Saisis un numéro valide.")

        chosen = int(raw) - 1
        if chosen == q["answer"]:
            U.success("Bonne réponse !")
            score += 1
        else:
            U.error(f"Mauvaise réponse. La bonne réponse était : {U.C.BOLD}{q['choices'][q['answer']]}{U.C.RESET}")
        U.info(q["explanation"])
        print()
        U.ask_continue()

    return score, len(questions)


def _run_exercises(lesson: dict) -> tuple[int, int]:
    exercises = lesson.get("exercises", [])
    if not exercises:
        return 0, 0

    score = 0
    for i, ex in enumerate(exercises, 1):
        U.clear()
        U.banner()
        U.title(f"Exercice {i}/{len(exercises)} — {lesson['title']}")
        U.section("Consigne")
        for line in ex["instruction"].split("\n"):
            print(f"  {line}")
        print()

        attempts = 0
        while True:
            attempts += 1
            U.section("Ton code (tape FIN sur une ligne seule pour valider)")
            lines = []
            while True:
                line = U.prompt()
                if line.upper() == "FIN":
                    break
                lines.append(line)
            code = "\n".join(lines)

            if not code.strip():
                U.warning("Tu n'as rien écrit !")
                continue

            passed, actual, err = check_exercise(code, ex["test_output"])

            if passed:
                U.success("Parfait ! Exercice réussi !")
                score += 1
                break
            else:
                if err:
                    U.error("Ton code contient une erreur :")
                    print(f"{U.C.RED}{err}{U.C.RESET}")
                else:
                    U.error("La sortie ne correspond pas.")
                    print(f"  Attendu : {U.C.GREEN}{ex['test_output']!r}{U.C.RESET}")
                    print(f"  Obtenu  : {U.C.RED}{actual!r}{U.C.RESET}")

                options = ["Réessayer", "Voir l'indice", "Voir la solution", "Passer"]
                choice = U.numbered_menu(options)

                if choice == 1:
                    continue
                elif choice == 2:
                    U.info(f"Indice : {ex['hint']}")
                    U.ask_continue()
                elif choice == 3:
                    U.section("Solution")
                    U.code_block(ex["solution"])
                    U.ask_continue()
                    break
                elif choice == 4:
                    U.warning("Exercice passé.")
                    break

        U.ask_continue()

    return score, len(exercises)


def run_lesson(lesson: dict):
    _show_theory(lesson)

    quiz_score, quiz_max = _run_quiz(lesson)
    ex_score, ex_max     = _run_exercises(lesson)

    total = quiz_score + ex_score
    max_t = quiz_max + ex_max

    U.clear()
    U.banner()
    U.title(f"Résultats — {lesson['title']}")
    print(f"  Quiz     : {quiz_score}/{quiz_max}")
    print(f"  Exercices: {ex_score}/{ex_max}")
    print(f"  Total    : {U.C.BOLD}{total}/{max_t}{U.C.RESET}")
    print()

    pct = total / max_t if max_t else 1
    if pct >= 0.8:
        U.success("Excellent travail ! Tu maîtrises bien cette leçon.")
    elif pct >= 0.5:
        U.warning("Bien, mais relis la leçon pour consolider tes acquis.")
    else:
        U.error("N'abandonne pas ! Relis la leçon et réessaie.")

    P.mark_lesson_done(lesson["id"], total, max_t)
    xp = P.get_xp()
    print(f"\n  {U.C.YELLOW}{U.C.BOLD}+XP gagnés ! Total XP : {xp}{U.C.RESET}")
    print()
    U.ask_continue()
