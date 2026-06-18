# Mettre l'application en ligne (obtenir un vrai lien internet)

Guide pas-à-pas, sans aucune connaissance technique requise. À la fin, tu auras un lien du type
`https://ton-app.onrender.com` accessible depuis n'importe quel ordinateur.

Tout se passe en 3 étapes : **GitHub** (stocker le code) → **Render** (héberger le site) → **lien final**.

---

## Étape 1 — Mettre le code sur GitHub

1. Va sur https://github.com et crée un compte gratuit (bouton "Sign up").
2. Une fois connecté, clique sur le bouton **"+"** en haut à droite → **"New repository"**.
3. Donne-lui un nom, par exemple `analyse-bdd-fiches`. Laisse le reste par défaut. Clique **"Create repository"**.
4. Sur la page qui s'affiche, cherche le lien **"uploading an existing file"** (ou "upload files").
5. Ouvre le dossier `C:\Users\IT Admin\Desktop\CLAUDE\app` sur ton PC, sélectionne **tout son contenu**
   (les dossiers `backend`, `frontend`, `data`, le `Dockerfile`, le `README.md`, etc.) et **glisse-les**
   dans la zone d'upload de GitHub.
   - ⚠️ Glisse le **contenu** du dossier `app`, pas le dossier `app` lui-même (le `Dockerfile` doit être
     directement visible à la racine du dépôt GitHub, pas dans un sous-dossier `app/Dockerfile`).
6. En bas de page, clique **"Commit changes"** (tu peux laisser le message par défaut).

Ton code est maintenant sur GitHub.

---

## Étape 2 — Héberger le site sur Render

1. Va sur https://render.com et crée un compte gratuit — choisis **"Sign up with GitHub"**, c'est le
   plus simple (ça connecte directement ton compte GitHub).
2. Une fois connecté, clique **"New +"** → **"Web Service"**.
3. Sélectionne le dépôt `analyse-bdd-fiches` que tu viens de créer (Render te demandera peut-être
   l'autorisation d'accéder à GitHub — accepte).
4. Render va détecter automatiquement le fichier `Dockerfile` — laisse "Docker" comme environnement.
5. Choisis le plan **"Free"**.
6. Clique **"Create Web Service"**.

Render va construire l'application (ça prend 3 à 5 minutes la première fois — tu verras les logs défiler).

---

## Étape 3 — Récupérer le lien

Une fois le déploiement terminé (statut **"Live"** en vert), Render affiche ton lien en haut de la page,
sous la forme :

```
https://analyse-bdd-fiches.onrender.com
```

Clique sur ce lien (ou copie-le dans ton navigateur) : ton application est en ligne. C'est ce lien que tu
peux partager ou utiliser depuis n'importe quel appareil.

---

## À savoir (limites du plan gratuit Render)

- Le service gratuit **s'endort après 15 minutes d'inactivité** : le premier accès après une pause peut
  prendre 30-50 secondes à se réveiller (totalement normal, pas un bug).
- L'**historique des analyses est réinitialisé** à chaque redéploiement (le plan gratuit ne garde pas de
  stockage permanent). Pour un usage quotidien sérieux et permanent, il faudra passer à un plan payant
  avec un disque persistant — dis-le moi si tu veux que je t'aide à configurer ça plus tard.

## Mettre à jour le site après une modification du code

Si je modifie le code plus tard : il suffira de remplacer les fichiers correspondants sur GitHub
(bouton "Upload files" à nouveau, ou "Edit" sur un fichier précis) — Render redéploiera automatiquement
le site avec la nouvelle version en quelques minutes.
