export const QUIZZES = {
  'quiz-html-1': {
    title: 'Quiz — Introduction HTML',
    questions: [
      {
        question: 'Que signifie HTML ?',
        options: [
          'HyperText Markup Language',
          'High Tech Modern Language',
          'Home Tool Markup Language',
          'HyperText Machine Learning',
        ],
        correct: 0,
        explanation: 'HTML = HyperText Markup Language. C\'est le langage de balisage pour créer des pages web.',
      },
      {
        question: 'Comment s\'appelle \`</p>\` ?',
        options: [
          'Balise ouvrante',
          'Balise fermante',
          'Balise vide',
          'Commentaire',
        ],
        correct: 1,
        explanation: 'Une balise avec \`/\` est une balise fermante. Elle marque la fin d\'un élément.',
      },
      {
        question: 'Quelle balise est utilisée pour le titre principal d\'une page ?',
        options: ['<title>', '<header>', '<h1>', '<main>'],
        correct: 2,
        explanation: '<h1> est le titre principal (heading 1). C\'est le plus grand et le plus important.',
      },
    ],
  },
  'quiz-html-2': {
    title: 'Quiz — Titres et paragraphes',
    questions: [
      {
        question: 'Combien de niveaux de titres existe-t-il en HTML ?',
        options: ['3', '4', '6', '8'],
        correct: 2,
        explanation: 'HTML propose 6 niveaux : <h1>, <h2>, <h3>, <h4>, <h5> et <h6>.',
      },
      {
        question: 'Quelle balise utilise-t-on pour un paragraphe ?',
        options: ['<text>', '<para>', '<p>', '<t>'],
        correct: 2,
        explanation: 'La balise <p> (paragraph) est utilisée pour les paragraphes de texte.',
      },
      {
        question: 'Quel est le plus petit titre HTML ?',
        options: ['<h1>', '<h4>', '<h6>', '<small>'],
        correct: 2,
        explanation: '<h6> est le plus petit niveau de titre en HTML.',
      },
    ],
  },
  'quiz-html-3': {
    title: 'Quiz — Liens et images',
    questions: [
      {
        question: 'Quel attribut définit l\'URL d\'un lien ?',
        options: ['src', 'href', 'url', 'link'],
        correct: 1,
        explanation: 'L\'attribut \`href\` (HyperReference) définit l\'adresse du lien dans la balise <a>.',
      },
      {
        question: 'Quelle balise crée un lien cliquable ?',
        options: ['<link>', '<url>', '<a>', '<click>'],
        correct: 2,
        explanation: 'La balise <a> (anchor) crée des liens hypertexte cliquables.',
      },
      {
        question: 'À quoi sert l\'attribut \`alt\` dans une image ?',
        options: [
          'Définir la taille',
          'Décrire l\'image (accessibilité)',
          'Changer la couleur',
          'Ajouter un lien',
        ],
        correct: 1,
        explanation: 'L\'attribut alt donne une description textuelle de l\'image, utile pour l\'accessibilité.',
      },
    ],
  },
  'quiz-html-4': {
    title: 'Quiz — Les listes',
    questions: [
      {
        question: 'Quelle balise crée une liste à puces ?',
        options: ['<ol>', '<ul>', '<li>', '<list>'],
        correct: 1,
        explanation: '<ul> = unordered list (liste non ordonnée). Les éléments sont présentés avec des puces.',
      },
      {
        question: 'Quelle balise représente un élément de liste ?',
        options: ['<item>', '<element>', '<li>', '<point>'],
        correct: 2,
        explanation: '<li> = list item. C\'est la balise pour chaque élément dans une liste.',
      },
      {
        question: 'Quelle balise crée une liste numérotée ?',
        options: ['<ul>', '<numbered>', '<ol>', '<nl>'],
        correct: 2,
        explanation: '<ol> = ordered list (liste ordonnée). Les éléments sont automatiquement numérotés.',
      },
    ],
  },
  'quiz-css-1': {
    title: 'Quiz — Introduction CSS',
    questions: [
      {
        question: 'Que signifie CSS ?',
        options: [
          'Cascading Style Sheets',
          'Computer Style System',
          'Creative Style Script',
          'Color Style Sheets',
        ],
        correct: 0,
        explanation: 'CSS = Cascading Style Sheets (Feuilles de style en cascade).',
      },
      {
        question: 'Comment appelle-t-on \`p\` dans \`p { color: red; }\` ?',
        options: ['Propriété', 'Valeur', 'Sélecteur', 'Règle'],
        correct: 2,
        explanation: '\`p\` est le sélecteur. Il désigne quel élément HTML on veut styliser.',
      },
      {
        question: 'Quelle propriété CSS change la couleur du texte ?',
        options: ['text-color', 'font-color', 'color', 'foreground'],
        correct: 2,
        explanation: 'La propriété \`color\` change la couleur du texte en CSS.',
      },
    ],
  },
  'quiz-css-2': {
    title: 'Quiz — Texte et police',
    questions: [
      {
        question: 'Quelle propriété CSS met le texte en gras ?',
        options: ['font-style: bold', 'text-weight: bold', 'font-weight: bold', 'bold: true'],
        correct: 2,
        explanation: '\`font-weight: bold\` rend le texte en gras.',
      },
      {
        question: 'Comment centre-t-on un texte en CSS ?',
        options: [
          'font-align: center',
          'text-align: center',
          'align: center',
          'center: true',
        ],
        correct: 1,
        explanation: '\`text-align: center\` centre le texte horizontalement.',
      },
      {
        question: 'Quelle unité est souvent utilisée pour la taille du texte ?',
        options: ['cm', 'px', 'pt', 'mm'],
        correct: 1,
        explanation: '\`px\` (pixels) est l\'unité la plus courante pour définir la taille des éléments.',
      },
    ],
  },
  'quiz-css-3': {
    title: 'Quiz — Marges et espacements',
    questions: [
      {
        question: 'Quelle propriété définit l\'espace intérieur d\'un élément ?',
        options: ['margin', 'padding', 'spacing', 'gap'],
        correct: 1,
        explanation: '\`padding\` définit l\'espace entre le contenu et la bordure (intérieur).',
      },
      {
        question: 'Quelle propriété arrondit les coins d\'une boîte ?',
        options: ['border-round', 'corner-radius', 'border-radius', 'round-corners'],
        correct: 2,
        explanation: '\`border-radius\` arrondit les coins d\'un élément.',
      },
      {
        question: 'Que représente \`margin: 10px 20px\` ?',
        options: [
          '10px partout',
          '10px gauche/droite, 20px haut/bas',
          '10px haut/bas, 20px gauche/droite',
          '10px haut, 20px partout',
        ],
        correct: 2,
        explanation: 'Avec deux valeurs : première = haut/bas, deuxième = gauche/droite.',
      },
    ],
  },
  'quiz-js-1': {
    title: 'Quiz — Introduction JavaScript',
    questions: [
      {
        question: 'Quelle commande affiche un message dans la console ?',
        options: ['print()', 'echo()', 'console.log()', 'display()'],
        correct: 2,
        explanation: '\`console.log()\` est la fonction JavaScript pour afficher des messages dans la console.',
      },
      {
        question: 'Comment commence un commentaire sur une ligne en JS ?',
        options: ['#', '/*', '//', '--'],
        correct: 2,
        explanation: '\`//\` commence un commentaire sur une ligne en JavaScript.',
      },
      {
        question: 'Quelle fonction affiche une boîte de dialogue ?',
        options: ['popup()', 'dialog()', 'alert()', 'message()'],
        correct: 2,
        explanation: '\`alert()\` affiche une boîte de dialogue avec un message.',
      },
    ],
  },
  'quiz-js-2': {
    title: 'Quiz — Les variables',
    questions: [
      {
        question: 'Quel mot-clé moderne crée une variable ?',
        options: ['var', 'let', 'def', 'variable'],
        correct: 1,
        explanation: '\`let\` est le mot-clé moderne recommandé pour déclarer une variable.',
      },
      {
        question: 'Quel est le type de \`true\` et \`false\` ?',
        options: ['String', 'Number', 'Boolean', 'Object'],
        correct: 2,
        explanation: '\`true\` et \`false\` sont des valeurs booléennes (Boolean). Elles représentent vrai/faux.',
      },
      {
        question: 'Comment affiche-t-on une variable \`nom\` dans un texte ?',
        options: [
          '"Bonjour " + nom',
          '"Bonjour " & nom',
          '"Bonjour " . nom',
          '"Bonjour nom"',
        ],
        correct: 0,
        explanation: 'L\'opérateur \`+\` concatène (combine) des chaînes de caractères en JavaScript.',
      },
    ],
  },
  'quiz-js-3': {
    title: 'Quiz — Les conditions',
    questions: [
      {
        question: 'Quel opérateur teste l\'égalité stricte en JavaScript ?',
        options: ['=', '==', '===', '!='],
        correct: 2,
        explanation: '\`===\` est l\'opérateur d\'égalité stricte (vérifie la valeur ET le type).',
      },
      {
        question: 'Que signifie \`&&\` en JavaScript ?',
        options: ['OU logique', 'ET logique', 'NON logique', 'Égalité'],
        correct: 1,
        explanation: '\`&&\` est l\'opérateur ET logique. Les deux conditions doivent être vraies.',
      },
      {
        question: 'Quel est le résultat de \`if (5 > 3)\` ?',
        options: ['Le bloc if s\'exécute', 'Le bloc else s\'exécute', 'Erreur', 'Rien'],
        correct: 0,
        explanation: '5 > 3 est vrai, donc le code dans le bloc if s\'exécute.',
      },
    ],
  },
  'quiz-js-4': {
    title: 'Quiz — Les fonctions',
    questions: [
      {
        question: 'Quel mot-clé définit une fonction ?',
        options: ['def', 'func', 'function', 'fn'],
        correct: 2,
        explanation: '\`function\` est le mot-clé pour déclarer une fonction en JavaScript.',
      },
      {
        question: 'Quel mot-clé renvoie une valeur depuis une fonction ?',
        options: ['send', 'output', 'return', 'give'],
        correct: 2,
        explanation: '\`return\` renvoie une valeur depuis une fonction et arrête son exécution.',
      },
      {
        question: 'Comment appelle-t-on une fonction \`direBonjour\` ?',
        options: ['direBonjour', 'call direBonjour', 'direBonjour()', 'run direBonjour'],
        correct: 2,
        explanation: 'On appelle une fonction en écrivant son nom suivi de parenthèses : \`direBonjour()\`.',
      },
    ],
  },
}
