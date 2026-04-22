export const MODULES = [
  {
    id: 'html',
    title: 'HTML — La structure',
    icon: '🏗️',
    color: '#e34c26',
    colorLight: '#fff3f0',
    description: 'Apprends à construire la structure d\'une page web',
    lessons: [
      {
        id: 'html-1',
        title: 'Qu\'est-ce que le HTML ?',
        icon: '🌐',
        xp: 50,
        theory: `
# Qu'est-ce que le HTML ?

**HTML** signifie **HyperText Markup Language**. C'est le langage qui définit la **structure** d'une page web.

Imagine une maison :
- 🏗️ **HTML** = la charpente (structure)
- 🎨 **CSS** = la peinture et la décoration (style)
- ⚡ **JavaScript** = l'électricité et la plomberie (fonctionnement)

## Les balises HTML

Le HTML fonctionne avec des **balises** (tags en anglais). Une balise ressemble à ceci :

\`\`\`html
<p>Bonjour tout le monde !</p>
\`\`\`

- \`<p>\` est la **balise ouvrante**
- \`</p>\` est la **balise fermante**
- Le texte entre les deux est le **contenu**

## Structure de base d'une page

\`\`\`html
<!DOCTYPE html>
<html>
  <head>
    <title>Mon site</title>
  </head>
  <body>
    <h1>Bienvenue !</h1>
    <p>C'est ma première page web.</p>
  </body>
</html>
\`\`\`
`,
        exercise: {
          instructions: 'Écris une balise \`<p>\` contenant le texte "Je code !"',
          starterCode: `<!-- Écris ton code ici -->
`,
          solution: '<p>Je code !</p>',
          hint: 'N\'oublie pas la balise ouvrante <p> et la balise fermante </p>',
          type: 'html',
        },
        quizId: 'quiz-html-1',
      },
      {
        id: 'html-2',
        title: 'Les titres et paragraphes',
        icon: '📝',
        xp: 50,
        theory: `
# Les titres et paragraphes

## Les titres (headings)

HTML propose **6 niveaux de titres**, du plus grand au plus petit :

\`\`\`html
<h1>Titre principal</h1>
<h2>Sous-titre</h2>
<h3>Section</h3>
<h4>Sous-section</h4>
<h5>Petit titre</h5>
<h6>Tout petit titre</h6>
\`\`\`

## Les paragraphes

Pour écrire du texte normal, utilise la balise \`<p>\` :

\`\`\`html
<p>Voici un paragraphe de texte.</p>
<p>Et voici un deuxième paragraphe.</p>
\`\`\`

## Résultat

\`\`\`html
<h1>Mon Blog</h1>
<h2>Premier article</h2>
<p>Bienvenue sur mon blog ! Aujourd'hui je parle de HTML.</p>
\`\`\`
`,
        exercise: {
          instructions: 'Crée une page avec un titre \`<h1>\` "Mon Site" et un paragraphe \`<p>\` "Bienvenue !"',
          starterCode: `<!-- Écris les balises h1 et p ici -->
`,
          solution: '<h1>Mon Site</h1>\n<p>Bienvenue !</p>',
          hint: 'Tu as besoin de deux balises : <h1>...</h1> et <p>...</p>',
          type: 'html',
        },
        quizId: 'quiz-html-2',
      },
      {
        id: 'html-3',
        title: 'Les liens et images',
        icon: '🔗',
        xp: 60,
        theory: `
# Les liens et images

## Les liens

La balise \`<a>\` crée un **lien cliquable** :

\`\`\`html
<a href="https://www.google.com">Aller sur Google</a>
\`\`\`

- \`href\` = l'adresse du lien (URL)
- Le texte entre les balises = ce qu'on voit sur la page

## Les images

La balise \`<img>\` affiche une **image** :

\`\`\`html
<img src="chat.jpg" alt="Photo d'un chat" />
\`\`\`

- \`src\` = le chemin vers l'image
- \`alt\` = une description (pour les personnes malvoyantes)
- C'est une balise **auto-fermante** (pas besoin de \`</img>\`)

## Exemple complet

\`\`\`html
<h1>Mon animal préféré</h1>
<img src="chat.jpg" alt="Mon chat Miaou" />
<p>Voici mon chat !</p>
<a href="https://chats.com">En savoir plus sur les chats</a>
\`\`\`
`,
        exercise: {
          instructions: 'Crée un lien vers "https://google.com" avec le texte "Rechercher"',
          starterCode: `<!-- Crée un lien ici -->
`,
          solution: '<a href="https://google.com">Rechercher</a>',
          hint: 'Utilise <a href="URL">texte du lien</a>',
          type: 'html',
        },
        quizId: 'quiz-html-3',
      },
      {
        id: 'html-4',
        title: 'Les listes',
        icon: '📋',
        xp: 50,
        theory: `
# Les listes

## Liste non ordonnée (avec puces)

\`\`\`html
<ul>
  <li>Pomme</li>
  <li>Banane</li>
  <li>Orange</li>
</ul>
\`\`\`

Résultat :
• Pomme
• Banane
• Orange

## Liste ordonnée (numérotée)

\`\`\`html
<ol>
  <li>Premier pas</li>
  <li>Deuxième pas</li>
  <li>Troisième pas</li>
</ol>
\`\`\`

Résultat :
1. Premier pas
2. Deuxième pas
3. Troisième pas

> 💡 **Astuce** : \`<ul>\` = **u**nordered **l**ist, \`<ol>\` = **o**rdered **l**ist, \`<li>\` = **l**ist **i**tem
`,
        exercise: {
          instructions: 'Crée une liste non ordonnée avec 3 fruits de ton choix',
          starterCode: `<!-- Crée ta liste ici -->
`,
          solution: '<ul>\n  <li>Pomme</li>\n  <li>Banane</li>\n  <li>Mangue</li>\n</ul>',
          hint: 'Utilise <ul> pour la liste et <li> pour chaque élément',
          type: 'html',
        },
        quizId: 'quiz-html-4',
      },
    ],
  },
  {
    id: 'css',
    title: 'CSS — Le style',
    icon: '🎨',
    color: '#264de4',
    colorLight: '#f0f4ff',
    description: 'Apprends à rendre tes pages belles et colorées',
    lessons: [
      {
        id: 'css-1',
        title: 'Qu\'est-ce que le CSS ?',
        icon: '✨',
        xp: 50,
        theory: `
# Qu'est-ce que le CSS ?

**CSS** signifie **Cascading Style Sheets** (Feuilles de style en cascade).

Le CSS permet de **modifier l'apparence** des éléments HTML : couleurs, tailles, polices...

## Comment écrire du CSS ?

\`\`\`css
p {
  color: red;
  font-size: 18px;
}
\`\`\`

- \`p\` = le **sélecteur** (quel élément on veut modifier)
- \`color\` = la **propriété** (qu'est-ce qu'on modifie ?)
- \`red\` = la **valeur** (par quoi on le remplace ?)

## Les couleurs

\`\`\`css
h1 {
  color: blue;         /* nom de couleur */
  color: #FF5733;      /* code hexadécimal */
  color: rgb(255, 0, 0); /* rouge, vert, bleu */
}
\`\`\`

## Le fond

\`\`\`css
body {
  background-color: lightblue;
}
\`\`\`
`,
        exercise: {
          instructions: 'Écris du CSS pour rendre tous les \`<h1>\` de couleur bleue',
          starterCode: `/* Écris ton CSS ici */
`,
          solution: 'h1 {\n  color: blue;\n}',
          hint: 'Utilise le sélecteur h1 et la propriété color',
          type: 'css',
        },
        quizId: 'quiz-css-1',
      },
      {
        id: 'css-2',
        title: 'Taille et police du texte',
        icon: '🔠',
        xp: 50,
        theory: `
# Taille et police du texte

## Taille du texte

\`\`\`css
p {
  font-size: 16px;   /* en pixels */
  font-size: 1.5em;  /* relatif (1em = taille normale) */
}
\`\`\`

## Style du texte

\`\`\`css
p {
  font-weight: bold;   /* gras */
  font-style: italic;  /* italique */
  text-decoration: underline; /* souligné */
  text-align: center;  /* centré */
}
\`\`\`

## Police de caractères

\`\`\`css
body {
  font-family: Arial, sans-serif;
  font-family: 'Georgia', serif;
  font-family: 'Courier New', monospace;
}
\`\`\`

## Exemple complet

\`\`\`css
h1 {
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  color: #6c63ff;
  font-family: Arial, sans-serif;
}
\`\`\`
`,
        exercise: {
          instructions: 'Écris du CSS pour centrer le texte des \`<p>\` et le mettre en gras',
          starterCode: `/* Écris ton CSS ici */
`,
          solution: 'p {\n  text-align: center;\n  font-weight: bold;\n}',
          hint: 'Utilise text-align: center et font-weight: bold',
          type: 'css',
        },
        quizId: 'quiz-css-2',
      },
      {
        id: 'css-3',
        title: 'Marges et espacements',
        icon: '📐',
        xp: 60,
        theory: `
# Marges et espacements

## margin vs padding

Imagine un emballage cadeau :
- 📦 **padding** = l'espace entre le cadeau et la boîte (intérieur)
- 🎁 **margin** = l'espace entre la boîte et les autres objets (extérieur)

\`\`\`css
div {
  padding: 20px;  /* espace intérieur */
  margin: 10px;   /* espace extérieur */
}
\`\`\`

## Côtés individuels

\`\`\`css
div {
  margin-top: 10px;
  margin-right: 20px;
  margin-bottom: 10px;
  margin-left: 20px;

  /* Raccourci : haut droite bas gauche */
  margin: 10px 20px 10px 20px;

  /* Raccourci : haut/bas  gauche/droite */
  margin: 10px 20px;
}
\`\`\`

## Bordures

\`\`\`css
div {
  border: 2px solid black;
  border-radius: 10px; /* coins arrondis */
}
\`\`\`
`,
        exercise: {
          instructions: 'Ajoute un padding de 20px et une bordure arrondie (border-radius: 10px) aux \`<div>\`',
          starterCode: `/* Écris ton CSS ici */
`,
          solution: 'div {\n  padding: 20px;\n  border-radius: 10px;\n}',
          hint: 'Utilise padding: 20px et border-radius: 10px dans le sélecteur div',
          type: 'css',
        },
        quizId: 'quiz-css-3',
      },
    ],
  },
  {
    id: 'js',
    title: 'JavaScript — L\'action',
    icon: '⚡',
    color: '#f0db4f',
    colorLight: '#fffef0',
    description: 'Apprends à rendre tes pages interactives',
    lessons: [
      {
        id: 'js-1',
        title: 'Qu\'est-ce que JavaScript ?',
        icon: '🤖',
        xp: 50,
        theory: `
# Qu'est-ce que JavaScript ?

**JavaScript** est le langage qui rend les pages web **interactives** !

Sans JavaScript : la page est statique (comme une photo)
Avec JavaScript : la page réagit aux actions (comme une vidéo)

## Ton premier programme

\`\`\`javascript
console.log("Bonjour !");
\`\`\`

\`console.log()\` affiche un message dans la console du navigateur.

## Les commentaires

\`\`\`javascript
// Ceci est un commentaire (ignoré par le navigateur)

/* Ceci est un commentaire
   sur plusieurs lignes */
\`\`\`

## Afficher une alerte

\`\`\`javascript
alert("Bienvenue sur mon site !");
\`\`\`

## Exemples d'utilisations

- 🖱️ Réagir aux clics de l'utilisateur
- ✅ Valider un formulaire
- 🌙 Activer le mode sombre
- 🎮 Créer des jeux dans le navigateur
`,
        exercise: {
          instructions: 'Écris une ligne JavaScript pour afficher "Bonjour le monde !" dans la console',
          starterCode: `// Écris ton code JavaScript ici
`,
          solution: 'console.log("Bonjour le monde !");',
          hint: 'Utilise console.log("ton message")',
          type: 'js',
        },
        quizId: 'quiz-js-1',
      },
      {
        id: 'js-2',
        title: 'Les variables',
        icon: '📦',
        xp: 60,
        theory: `
# Les variables

Une **variable** est une boîte qui stocke une information.

## Déclarer une variable

\`\`\`javascript
let prenom = "Alice";
let age = 25;
let estEtudiant = true;
\`\`\`

- \`let\` = mot-clé pour créer une variable
- \`prenom\` = le nom de la variable
- \`"Alice"\` = la valeur

## Les types de données

\`\`\`javascript
let texte = "Bonjour";      // String (chaîne de caractères)
let nombre = 42;             // Number (nombre)
let decimal = 3.14;          // Number (décimal)
let vrai = true;             // Boolean (vrai/faux)
let faux = false;            // Boolean
\`\`\`

## Utiliser une variable

\`\`\`javascript
let nom = "Marie";
console.log("Bonjour " + nom + " !");
// Affiche : Bonjour Marie !

// Avec les template literals (plus moderne)
console.log(\`Bonjour \${nom} !\`);
\`\`\`

## Modifier une variable

\`\`\`javascript
let score = 0;
score = 10;       // on change la valeur
score = score + 5; // on ajoute 5
console.log(score); // affiche 15
\`\`\`
`,
        exercise: {
          instructions: 'Crée une variable \`nom\` avec ton prénom et affiche "Bonjour [ton prénom] !" avec console.log',
          starterCode: `// Crée ta variable et affiche le message
`,
          solution: 'let nom = "Alice";\nconsole.log("Bonjour " + nom + " !");',
          hint: 'let nom = "TonPrenom"; puis console.log("Bonjour " + nom + " !");',
          type: 'js',
        },
        quizId: 'quiz-js-2',
      },
      {
        id: 'js-3',
        title: 'Les conditions',
        icon: '🔀',
        xp: 70,
        theory: `
# Les conditions

Les conditions permettent d'exécuter du code **selon une situation**.

## if / else

\`\`\`javascript
let age = 18;

if (age >= 18) {
  console.log("Tu es majeur !");
} else {
  console.log("Tu es mineur.");
}
\`\`\`

## Les opérateurs de comparaison

| Opérateur | Signification |
|-----------|--------------|
| \`===\`   | égal à |
| \`!==\`   | différent de |
| \`>\`     | supérieur à |
| \`<\`     | inférieur à |
| \`>=\`    | supérieur ou égal |
| \`<=\`    | inférieur ou égal |

## else if

\`\`\`javascript
let note = 85;

if (note >= 90) {
  console.log("Excellent !");
} else if (note >= 70) {
  console.log("Bien !");
} else if (note >= 50) {
  console.log("Passable.");
} else {
  console.log("À améliorer.");
}
\`\`\`

## Les opérateurs logiques

\`\`\`javascript
// ET (les deux conditions vraies)
if (age >= 18 && possedPermis === true) {
  console.log("Tu peux conduire !");
}

// OU (au moins une condition vraie)
if (jour === "samedi" || jour === "dimanche") {
  console.log("C'est le week-end !");
}
\`\`\`
`,
        exercise: {
          instructions: 'Crée une variable \`temperature\` à 35 et affiche "Il fait chaud !" si elle est > 30, sinon "Il fait frais."',
          starterCode: `// Écris ta condition ici
`,
          solution: 'let temperature = 35;\nif (temperature > 30) {\n  console.log("Il fait chaud !");\n} else {\n  console.log("Il fait frais.");\n}',
          hint: 'Utilise if (temperature > 30) { ... } else { ... }',
          type: 'js',
        },
        quizId: 'quiz-js-3',
      },
      {
        id: 'js-4',
        title: 'Les fonctions',
        icon: '🔧',
        xp: 70,
        theory: `
# Les fonctions

Une **fonction** est un bloc de code réutilisable. C'est comme une recette de cuisine !

## Définir une fonction

\`\`\`javascript
function direBonjour() {
  console.log("Bonjour !");
}
\`\`\`

## Appeler une fonction

\`\`\`javascript
direBonjour(); // Affiche : Bonjour !
direBonjour(); // On peut l'appeler autant de fois qu'on veut
\`\`\`

## Fonction avec paramètres

\`\`\`javascript
function saluer(prenom) {
  console.log("Bonjour " + prenom + " !");
}

saluer("Alice"); // Affiche : Bonjour Alice !
saluer("Bob");   // Affiche : Bonjour Bob !
\`\`\`

## Fonction qui retourne une valeur

\`\`\`javascript
function additionner(a, b) {
  return a + b;
}

let resultat = additionner(5, 3);
console.log(resultat); // Affiche : 8
\`\`\`

## Exemple pratique

\`\`\`javascript
function calculerAge(anneeNaissance) {
  let anneeActuelle = 2024;
  return anneeActuelle - anneeNaissance;
}

let monAge = calculerAge(2000);
console.log("Tu as " + monAge + " ans !"); // Tu as 24 ans !
\`\`\`
`,
        exercise: {
          instructions: 'Crée une fonction \`multiplier(a, b)\` qui retourne le produit de a et b, puis affiche le résultat de multiplier(4, 5)',
          starterCode: `// Définis ta fonction ici
`,
          solution: 'function multiplier(a, b) {\n  return a * b;\n}\nconsole.log(multiplier(4, 5));',
          hint: 'function multiplier(a, b) { return a * b; } puis console.log(multiplier(4, 5));',
          type: 'js',
        },
        quizId: 'quiz-js-4',
      },
    ],
  },
]

export const getAllLessons = () => MODULES.flatMap(m => m.lessons)

export const getLessonById = (id) => getAllLessons().find(l => l.id === id)

export const getModuleByLessonId = (lessonId) =>
  MODULES.find(m => m.lessons.some(l => l.id === lessonId))
