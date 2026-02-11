# ChatBootPerso# ❄️ SnowChat AI - Assistant Snowflake Cortex

Une application de type Chatbot entièrement hébergée sur Snowflake, développée avec **Streamlit** et propulsée par le moteur d'IA **Snowflake Cortex**.

![Architecture](https://img.shields.io/badge/Architecture-Streamlit%20%7C%20Snowflake%20%7C%20Cortex-blue)

## 🎯 Objectif du projet
Créer un assistant conversationnel sécurisé capable de répondre à des questions techniques en utilisant les LLM (Large Language Models) intégrés à Snowflake, sans sortir les données du Cloud.

## 🛠️ Stack Technique
* **Frontend :** Streamlit (in Snowflake)
* **Backend :** Snowflake Snowpark (Python)
* **IA / LLM :** Snowflake Cortex (Mistral-Large / Llama-3-70b)
* **Base de Données :** Snowflake Tables (Pour l'historique de conversation)

## 🚀 Fonctionnalités
1.  **Interface Chat :** Style moderne avec avatars et gestion d'état (Session State).
2.  **Multi-Modèles :** Possibilité de choisir le modèle (Mistral, Llama, Gemma) via la sidebar.
3.  **Persistance :** Chaque message est sauvegardé en temps réel dans une table Snowflake (`CONVERSATION_HISTORY`).
4.  **Sécurité :** Gestion des quotas via Resource Monitor.

## ⚠️ Challenge Technique & Résolution
Durant le développement, une contrainte majeure a été rencontrée :
> Les comptes Snowflake **Trial** (Essai gratuit) bloquent souvent l'accès aux fonctions Cortex `COMPLETE` pour éviter les abus.

**Ma Solution :**
J'ai configuré un environnement Snowflake en région **AWS US East (N. Virginia)** et validé le compte (Payment Method) pour débloquer l'accès complet aux APIs Cortex. Cela permet à l'application de fonctionner en production réelle avec les modèles les plus puissants, plutôt que d'utiliser des données simulées.

## 📦 Installation
1.  Exécuter le script `setup.sql` dans une Worksheet Snowflake.
2.  Créer une Streamlit App dans Snowsight.
3.  Ajouter les packages : `snowflake-ml-python`.
4.  Copier le contenu de `app.py`.

---
*Projet réalisé dans le cadre de ma formation Développeur.*