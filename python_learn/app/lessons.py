"""
All lesson content: theory, quiz questions, and coding exercises.
"""

LESSONS = [
    {
        "id": "01_intro",
        "title": "Introduction — print() et commentaires",
        "theory": [
            ("Bienvenue !", "Python est un langage de programmation lisible et puissant.\n"
             "Il est utilisé partout : sites web, intelligence artificielle, scripts...\n"
             "Voyons les toutes premières commandes."),
            ("print()", "La fonction print() affiche du texte dans le terminal.\n"
             "On lui passe du texte entre guillemets (une chaîne de caractères)."),
            ("Exemple", None, 'print("Bonjour le monde !")\nprint("Python, c\'est cool !")'),
            ("Commentaires", "Une ligne commençant par # est un commentaire.\n"
             "Python l'ignore complètement. Sert à expliquer le code."),
            ("Exemple", None, '# Ceci est un commentaire\nprint("Je suis exécuté")  # commentaire inline'),
        ],
        "quiz": [
            {
                "question": "Que fait print('Salut') ?",
                "choices": ["Affiche Salut dans le terminal", "Crée une variable", "Démarre Python", "Rien"],
                "answer": 0,
                "explanation": "print() affiche le texte passé entre parenthèses."
            },
            {
                "question": "Comment écrire un commentaire en Python ?",
                "choices": ["// commentaire", "/* commentaire */", "# commentaire", "-- commentaire"],
                "answer": 2,
                "explanation": "En Python, on utilise # pour les commentaires."
            },
        ],
        "exercises": [
            {
                "instruction": 'Écris un print() qui affiche exactement : Bonjour Python !',
                "test_output": "Bonjour Python !",
                "hint": 'print("Bonjour Python !")',
                "solution": 'print("Bonjour Python !")',
            },
            {
                "instruction": 'Affiche deux lignes : la première "J\'apprends Python", la deuxième "C\'est super !"',
                "test_output": "J'apprends Python\nC'est super !",
                "hint": "Tu as besoin de deux print() différents.",
                "solution": "print(\"J'apprends Python\")\nprint(\"C'est super !\")",
            },
        ],
    },
    {
        "id": "02_variables",
        "title": "Variables et types de base",
        "theory": [
            ("Qu'est-ce qu'une variable ?", "Une variable est une boîte qui stocke une valeur.\n"
             "On lui donne un nom et on lui assigne une valeur avec ="),
            ("Exemple", None, 'prenom = "Ismaila"\nage = 20\nprint(prenom)\nprint(age)'),
            ("Les types principaux", "int  → nombre entier        ex: 42\n"
             "float → nombre décimal      ex: 3.14\n"
             "str   → chaîne de texte    ex: \"Bonjour\"\n"
             "bool  → vrai ou faux       ex: True / False"),
            ("type()", "La fonction type() te dit le type d'une valeur."),
            ("Exemple", None, 'x = 10\nprint(type(x))     # <class \'int\'>\ny = "hello"\nprint(type(y))     # <class \'str\'>'),
        ],
        "quiz": [
            {
                "question": "Quel est le type de  age = 25 ?",
                "choices": ["str", "float", "int", "bool"],
                "answer": 2,
                "explanation": "25 est un entier, donc son type est int."
            },
            {
                "question": "Quel symbole utilise-t-on pour assigner une valeur à une variable ?",
                "choices": ["==", ":", "->", "="],
                "answer": 3,
                "explanation": "Le signe = sert à l'assignation. == compare deux valeurs."
            },
            {
                "question": "Quel est le type de  pi = 3.14 ?",
                "choices": ["int", "float", "str", "double"],
                "answer": 1,
                "explanation": "Un nombre avec virgule est un float."
            },
        ],
        "exercises": [
            {
                "instruction": 'Crée une variable "nom" avec ta valeur "Python" et affiche-la.',
                "test_output": "Python",
                "hint": 'nom = "Python"\nprint(nom)',
                "solution": 'nom = "Python"\nprint(nom)',
            },
            {
                "instruction": 'Crée deux variables : annee = 2024 et langage = "Python"\nAffiche les deux sur deux lignes.',
                "test_output": "2024\nPython",
                "hint": "Utilise print() deux fois.",
                "solution": 'annee = 2024\nlangage = "Python"\nprint(annee)\nprint(langage)',
            },
        ],
    },
    {
        "id": "03_strings",
        "title": "Chaînes de caractères (str)",
        "theory": [
            ("Les strings", "Une string est du texte entouré de guillemets simples ou doubles.\n"
             "On peut faire beaucoup de choses avec !"),
            ("Concaténation", "On peut coller deux strings avec +"),
            ("Exemple", None, 'prenom = "Ismaila"\nmessage = "Bonjour " + prenom + " !"\nprint(message)'),
            ("f-strings (formatage)", "Les f-strings permettent d'insérer des variables directement dans une string.\n"
             "On préfixe la string avec f et on met la variable entre {}"),
            ("Exemple", None, 'prenom = "Ismaila"\nage = 20\nprint(f"Je m\'appelle {prenom} et j\'ai {age} ans.")'),
            ("Méthodes utiles", "len(s)         → longueur\ns.upper()      → MAJUSCULES\ns.lower()      → minuscules\ns.strip()      → supprime les espaces aux bouts\ns.replace(a,b) → remplace a par b"),
            ("Exemple", None, 's = "  bonjour  "\nprint(len("Python"))    # 6\nprint("hello".upper())  # HELLO\nprint(s.strip())        # bonjour'),
        ],
        "quiz": [
            {
                "question": 'Que vaut "Bon" + "jour" ?',
                "choices": ["Bon jour", "Bonjour", "\"Bon\" + \"jour\"", "Erreur"],
                "answer": 1,
                "explanation": "L'opérateur + concatène (colle) les deux strings."
            },
            {
                "question": 'Que retourne len("Python") ?',
                "choices": ["5", "6", "7", "Python"],
                "answer": 1,
                "explanation": "Python a 6 caractères : P-y-t-h-o-n."
            },
        ],
        "exercises": [
            {
                "instruction": 'Crée prenom = "Alice" et affiche avec une f-string : "Bonjour Alice !"',
                "test_output": "Bonjour Alice !",
                "hint": 'prenom = "Alice"\nprint(f"Bonjour {prenom} !")',
                "solution": 'prenom = "Alice"\nprint(f"Bonjour {prenom} !")',
            },
            {
                "instruction": 'Affiche "python" en majuscules en utilisant la méthode upper().',
                "test_output": "PYTHON",
                "hint": 'print("python".upper())',
                "solution": 'print("python".upper())',
            },
        ],
    },
    {
        "id": "04_conditionals",
        "title": "Conditions — if, elif, else",
        "theory": [
            ("Prendre des décisions", "Les conditions permettent d'exécuter du code\n"
             "seulement si une condition est vraie."),
            ("Syntaxe de base", "ATTENTION : l'indentation (4 espaces) est obligatoire en Python !"),
            ("Exemple", None, 'age = 18\nif age >= 18:\n    print("Tu es majeur")\nelse:\n    print("Tu es mineur")'),
            ("elif", "elif = sinon si. Permet de tester plusieurs conditions."),
            ("Exemple", None, 'note = 75\nif note >= 90:\n    print("Excellent !")\nelif note >= 60:\n    print("Bien !")\nelse:\n    print("Peut mieux faire")'),
            ("Opérateurs de comparaison", "==  égal\n!=  différent\n>   supérieur\n<   inférieur\n>=  supérieur ou égal\n<=  inférieur ou égal"),
        ],
        "quiz": [
            {
                "question": "Qu'affiche ce code ?\nx = 5\nif x > 3:\n    print('grand')\nelse:\n    print('petit')",
                "choices": ["petit", "grand", "5", "Rien"],
                "answer": 1,
                "explanation": "5 > 3 est vrai, donc on affiche 'grand'."
            },
            {
                "question": "Quel opérateur teste l'égalité ?",
                "choices": ["=", "!=", "==", ">="],
                "answer": 2,
                "explanation": "== compare deux valeurs. = assigne."
            },
        ],
        "exercises": [
            {
                "instruction": 'Crée temperature = 35\nSi temperature > 30, affiche "Il fait chaud !", sinon affiche "Il fait frais."',
                "test_output": "Il fait chaud !",
                "hint": "if temperature > 30:",
                "solution": 'temperature = 35\nif temperature > 30:\n    print("Il fait chaud !")\nelse:\n    print("Il fait frais.")',
            },
            {
                "instruction": 'Crée nombre = 7\nSi nombre est pair, affiche "Pair", sinon affiche "Impair".\n(Conseil : utilise le modulo %, ex: nombre % 2 == 0 si pair)',
                "test_output": "Impair",
                "hint": "if nombre % 2 == 0:",
                "solution": 'nombre = 7\nif nombre % 2 == 0:\n    print("Pair")\nelse:\n    print("Impair")',
            },
        ],
    },
    {
        "id": "05_loops",
        "title": "Boucles — for et while",
        "theory": [
            ("Pourquoi des boucles ?", "Une boucle répète du code plusieurs fois.\n"
             "Indispensable pour éviter la répétition !"),
            ("La boucle for", "for parcourt une séquence (liste, range, string…)"),
            ("Exemple", None, 'for i in range(5):\n    print(i)\n# Affiche 0 1 2 3 4'),
            ("range()", "range(n)      → de 0 à n-1\nrange(a, b)   → de a à b-1\nrange(a, b, pas) → avec un pas"),
            ("Exemple", None, 'for i in range(1, 6):\n    print(i)   # 1 2 3 4 5'),
            ("La boucle while", "while répète tant qu'une condition est vraie.\nATTENTION aux boucles infinies !"),
            ("Exemple", None, 'compteur = 0\nwhile compteur < 3:\n    print(compteur)\n    compteur += 1\n# Affiche 0 1 2'),
            ("break et continue", "break  → sort de la boucle immédiatement\ncontinue → passe à l'itération suivante"),
        ],
        "quiz": [
            {
                "question": "Que produit range(3) ?",
                "choices": ["1, 2, 3", "0, 1, 2, 3", "0, 1, 2", "3"],
                "answer": 2,
                "explanation": "range(3) génère 0, 1, 2 (n valeurs de 0 à n-1)."
            },
            {
                "question": "Quel mot-clé sort immédiatement d'une boucle ?",
                "choices": ["exit", "stop", "break", "return"],
                "answer": 2,
                "explanation": "break interrompt la boucle et passe au code suivant."
            },
        ],
        "exercises": [
            {
                "instruction": 'Affiche les nombres de 1 à 5, un par ligne, en utilisant une boucle for.',
                "test_output": "1\n2\n3\n4\n5",
                "hint": "for i in range(1, 6):",
                "solution": 'for i in range(1, 6):\n    print(i)',
            },
            {
                "instruction": 'Affiche la table de multiplication de 3 (de 3×1 à 3×5).\nFormat : "3 x 1 = 3"',
                "test_output": "3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15",
                "hint": 'for i in range(1, 6):\n    print(f"3 x {i} = {3*i}")',
                "solution": 'for i in range(1, 6):\n    print(f"3 x {i} = {3*i}")',
            },
        ],
    },
    {
        "id": "06_lists",
        "title": "Listes",
        "theory": [
            ("Qu'est-ce qu'une liste ?", "Une liste stocke plusieurs valeurs dans un seul objet.\n"
             "Les éléments sont ordonnés et accessibles par leur index (commence à 0)."),
            ("Créer et accéder", None, 'fruits = ["pomme", "banane", "cerise"]\nprint(fruits[0])   # pomme\nprint(fruits[-1])  # cerise (dernier)'),
            ("Modifier une liste", "append()  → ajoute à la fin\ninsert()  → insère à un index\nremove()  → supprime un élément\npop()     → supprime et retourne le dernier"),
            ("Exemple", None, 'ma_liste = [1, 2, 3]\nma_liste.append(4)     # [1, 2, 3, 4]\nma_liste.remove(2)     # [1, 3, 4]\nprint(len(ma_liste))   # 3'),
            ("Parcourir une liste", None, 'couleurs = ["rouge", "vert", "bleu"]\nfor couleur in couleurs:\n    print(couleur)'),
            ("Slicing", "On peut extraire une portion avec [debut:fin]"),
            ("Exemple", None, 'nb = [0, 1, 2, 3, 4, 5]\nprint(nb[1:4])   # [1, 2, 3]\nprint(nb[:3])    # [0, 1, 2]\nprint(nb[3:])    # [3, 4, 5]'),
        ],
        "quiz": [
            {
                "question": 'Quel est l\'index du premier élément d\'une liste ?',
                "choices": ["1", "-1", "0", "Aucun"],
                "answer": 2,
                "explanation": "En Python, les index commencent à 0."
            },
            {
                "question": 'Quelle méthode ajoute un élément à la fin d\'une liste ?',
                "choices": ["add()", "push()", "insert()", "append()"],
                "answer": 3,
                "explanation": "append() ajoute un élément à la fin de la liste."
            },
        ],
        "exercises": [
            {
                "instruction": 'Crée une liste "animaux" avec "chat", "chien", "lapin".\nAffiche le deuxième élément.',
                "test_output": "chien",
                "hint": 'animaux = ["chat", "chien", "lapin"]\nprint(animaux[1])',
                "solution": 'animaux = ["chat", "chien", "lapin"]\nprint(animaux[1])',
            },
            {
                "instruction": 'Crée une liste de nombres [10, 20, 30, 40, 50]\nAffiche la somme avec sum() et la longueur avec len().\nFormat : "Somme: 150\nLongueur: 5"',
                "test_output": "Somme: 150\nLongueur: 5",
                "hint": "print(f\"Somme: {sum(nb)}\")",
                "solution": 'nb = [10, 20, 30, 40, 50]\nprint(f"Somme: {sum(nb)}")\nprint(f"Longueur: {len(nb)}")',
            },
        ],
    },
    {
        "id": "07_functions",
        "title": "Fonctions — def",
        "theory": [
            ("Pourquoi des fonctions ?", "Une fonction est un bloc de code réutilisable.\n"
             "On la définit une fois et on l'appelle autant de fois que voulu."),
            ("Définir une fonction", "On utilise le mot-clé def, suivi du nom et de parenthèses."),
            ("Exemple", None, 'def dire_bonjour():\n    print("Bonjour !")\n\ndire_bonjour()  # appel\ndire_bonjour()  # encore !'),
            ("Paramètres", "On peut passer des valeurs à la fonction."),
            ("Exemple", None, 'def saluer(prenom):\n    print(f"Salut {prenom} !")\n\nsaluer("Alice")\nsaluer("Bob")'),
            ("return", "return renvoie une valeur depuis la fonction."),
            ("Exemple", None, 'def additionner(a, b):\n    return a + b\n\nresultat = additionner(3, 5)\nprint(resultat)  # 8'),
            ("Valeurs par défaut", None, 'def puissance(base, exp=2):\n    return base ** exp\n\nprint(puissance(3))    # 9\nprint(puissance(2, 3)) # 8'),
        ],
        "quiz": [
            {
                "question": "Quel mot-clé définit une fonction ?",
                "choices": ["func", "function", "def", "define"],
                "answer": 2,
                "explanation": "En Python, on utilise def pour définir une fonction."
            },
            {
                "question": "Que fait return dans une fonction ?",
                "choices": ["Affiche une valeur", "Termine le programme", "Renvoie une valeur", "Appelle la fonction"],
                "answer": 2,
                "explanation": "return renvoie une valeur à l'endroit où la fonction a été appelée."
            },
        ],
        "exercises": [
            {
                "instruction": 'Crée une fonction "carre(n)" qui retourne le carré de n.\nAffiche carre(4).',
                "test_output": "16",
                "hint": "def carre(n):\n    return n ** 2",
                "solution": 'def carre(n):\n    return n ** 2\nprint(carre(4))',
            },
            {
                "instruction": 'Crée une fonction "est_pair(n)" qui retourne True si n est pair, False sinon.\nAffiche est_pair(6) et est_pair(7) sur deux lignes.',
                "test_output": "True\nFalse",
                "hint": "return n % 2 == 0",
                "solution": 'def est_pair(n):\n    return n % 2 == 0\nprint(est_pair(6))\nprint(est_pair(7))',
            },
        ],
    },
    {
        "id": "08_dicts",
        "title": "Dictionnaires",
        "theory": [
            ("Qu'est-ce qu'un dictionnaire ?", "Un dictionnaire stocke des paires clé → valeur.\n"
             "Comme un vrai dictionnaire : mot → définition."),
            ("Créer et accéder", None, 'personne = {\n    "nom": "Alice",\n    "age": 25,\n    "ville": "Paris"\n}\nprint(personne["nom"])   # Alice\nprint(personne["age"])   # 25'),
            ("Modifier et ajouter", None, 'personne["age"] = 26       # modifier\npersonne["email"] = "a@b.com"  # ajouter\ndel personne["ville"]      # supprimer'),
            ("Méthodes utiles", "keys()   → toutes les clés\nvalues() → toutes les valeurs\nitems()  → paires (clé, valeur)\nget()    → accès sécurisé (pas d'erreur si absent)"),
            ("Exemple", None, 'd = {"a": 1, "b": 2}\nfor cle, val in d.items():\n    print(f"{cle} → {val}")'),
        ],
        "quiz": [
            {
                "question": "Comment accède-t-on à la valeur d'une clé dans un dict ?",
                "choices": ["dict.cle", "dict[cle]", "dict->cle", "dict.get_cle()"],
                "answer": 1,
                "explanation": "On utilise la notation crochets : dict[\"cle\"]."
            },
            {
                "question": "Quelle méthode retourne les paires clé-valeur d'un dict ?",
                "choices": ["keys()", "values()", "pairs()", "items()"],
                "answer": 3,
                "explanation": "items() retourne des tuples (clé, valeur)."
            },
        ],
        "exercises": [
            {
                "instruction": 'Crée un dictionnaire "voiture" avec les clés "marque"="Toyota", "annee"=2020.\nAffiche la marque.',
                "test_output": "Toyota",
                "hint": 'voiture = {"marque": "Toyota", "annee": 2020}\nprint(voiture["marque"])',
                "solution": 'voiture = {"marque": "Toyota", "annee": 2020}\nprint(voiture["marque"])',
            },
            {
                "instruction": 'Crée un dict "scores" : {"Alice": 90, "Bob": 75, "Charlie": 85}\nAffiche chaque nom et son score au format "Alice : 90"',
                "test_output": "Alice : 90\nBob : 75\nCharlie : 85",
                "hint": "for nom, score in scores.items():",
                "solution": 'scores = {"Alice": 90, "Bob": 75, "Charlie": 85}\nfor nom, score in scores.items():\n    print(f"{nom} : {score}")',
            },
        ],
    },
    {
        "id": "09_exceptions",
        "title": "Gestion des erreurs — try/except",
        "theory": [
            ("Les erreurs en Python", "Quand Python rencontre une erreur, il lève une exception\n"
             "et stoppe le programme. On peut les attraper avec try/except."),
            ("Syntaxe", None, 'try:\n    resultat = 10 / 0\nexcept ZeroDivisionError:\n    print("Division par zéro impossible !")'),
            ("Plusieurs exceptions", None, 'try:\n    n = int(input("Nombre : "))\n    print(10 / n)\nexcept ValueError:\n    print("Ce n\'est pas un nombre !")\nexcept ZeroDivisionError:\n    print("Division par zéro !")'),
            ("else et finally", "else    → exécuté si aucune exception\nfinally → exécuté TOUJOURS (nettoyage)"),
            ("Exemple", None, 'try:\n    x = int("42")\nexcept ValueError:\n    print("Erreur")\nelse:\n    print(f"Succès : {x}")\nfinally:\n    print("Fin du try")'),
            ("Exceptions courantes", "ValueError     → mauvais type de valeur\nTypeError      → mauvais type\nIndexError     → index hors limites\nKeyError       → clé absente dans un dict\nFileNotFoundError → fichier inexistant"),
        ],
        "quiz": [
            {
                "question": "Quel bloc est TOUJOURS exécuté, qu'il y ait une erreur ou non ?",
                "choices": ["try", "except", "else", "finally"],
                "answer": 3,
                "explanation": "finally s'exécute toujours, idéal pour le nettoyage."
            },
            {
                "question": "Quelle exception est levée si on divise par zéro ?",
                "choices": ["ValueError", "ZeroDivisionError", "MathError", "ArithmeticException"],
                "answer": 1,
                "explanation": "Python lève ZeroDivisionError lors d'une division par 0."
            },
        ],
        "exercises": [
            {
                "instruction": 'Écris un try/except qui tente de convertir "abc" en entier avec int().\nEn cas de ValueError, affiche "Conversion impossible".',
                "test_output": "Conversion impossible",
                "hint": 'try:\n    int("abc")\nexcept ValueError:',
                "solution": 'try:\n    int("abc")\nexcept ValueError:\n    print("Conversion impossible")',
            },
            {
                "instruction": 'Crée une liste [1, 2, 3].\nTente d\'accéder à l\'index 10, capture IndexError\net affiche "Index hors limites !".',
                "test_output": "Index hors limites !",
                "hint": "except IndexError:",
                "solution": 'ma_liste = [1, 2, 3]\ntry:\n    print(ma_liste[10])\nexcept IndexError:\n    print("Index hors limites !")',
            },
        ],
    },
    {
        "id": "10_classes",
        "title": "Classes et objets — POO",
        "theory": [
            ("Programmation Orientée Objet", "La POO organise le code autour d'objets.\n"
             "Un objet est une instance d'une classe (un moule)."),
            ("Définir une classe", None, 'class Chien:\n    def __init__(self, nom, race):\n        self.nom = nom\n        self.race = race\n\n    def aboyer(self):\n        print(f"{self.nom} dit : Ouaf !")'),
            ("Créer des objets", None, 'rex = Chien("Rex", "Labrador")\nbella = Chien("Bella", "Berger")\nrex.aboyer()    # Rex dit : Ouaf !\nprint(bella.race)  # Berger'),
            ("__init__", "__init__ est le constructeur : il s'exécute\nautomatiquement à la création de l'objet.\nself désigne l'objet lui-même."),
            ("Attributs et méthodes", "Attribut = variable d'un objet (self.nom)\nMéthode  = fonction d'un objet (def aboyer(self))"),
            ("Héritage (aperçu)", None, 'class Animal:\n    def __init__(self, nom):\n        self.nom = nom\n    def respirer(self):\n        print(f"{self.nom} respire")\n\nclass Chat(Animal):\n    def miauler(self):\n        print(f"{self.nom} dit : Miaou !")\n\nkitty = Chat("Kitty")\nkitty.respirer()  # hérité\nkitty.miauler()'),
        ],
        "quiz": [
            {
                "question": "Quelle méthode est appelée automatiquement à la création d'un objet ?",
                "choices": ["__start__", "__new__", "__init__", "__create__"],
                "answer": 2,
                "explanation": "__init__ est le constructeur, appelé automatiquement lors de l'instanciation."
            },
            {
                "question": "Que représente 'self' dans une méthode ?",
                "choices": ["La classe", "L'objet lui-même", "Une variable globale", "Le constructeur"],
                "answer": 1,
                "explanation": "self fait référence à l'instance de l'objet sur laquelle la méthode est appelée."
            },
        ],
        "exercises": [
            {
                "instruction": 'Crée une classe Rectangle avec __init__(self, largeur, hauteur).\nAjoute une méthode aire() qui retourne largeur * hauteur.\nCrée un rectangle de 5x3 et affiche son aire.',
                "test_output": "15",
                "hint": "def aire(self):\n    return self.largeur * self.hauteur",
                "solution": 'class Rectangle:\n    def __init__(self, largeur, hauteur):\n        self.largeur = largeur\n        self.hauteur = hauteur\n    def aire(self):\n        return self.largeur * self.hauteur\n\nr = Rectangle(5, 3)\nprint(r.aire())',
            },
            {
                "instruction": 'Crée une classe Compteur avec un attribut "valeur" initialisé à 0.\nAjoute une méthode incrementer() qui ajoute 1 à valeur.\nAjoute une méthode afficher() qui print la valeur.\nCrée un compteur, appelle incrementer() 3 fois, puis afficher().',
                "test_output": "3",
                "hint": "self.valeur += 1",
                "solution": 'class Compteur:\n    def __init__(self):\n        self.valeur = 0\n    def incrementer(self):\n        self.valeur += 1\n    def afficher(self):\n        print(self.valeur)\n\nc = Compteur()\nc.incrementer()\nc.incrementer()\nc.incrementer()\nc.afficher()',
            },
        ],
    },
]
