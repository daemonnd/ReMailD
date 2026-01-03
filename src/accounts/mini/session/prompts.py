from typing import Dict, Union
from rich import print
# prompts für den Abfragebereich "start" definieren
email_config_prompts = {
    "en": {
        "intro": {
            "main": "\n[blue]In the next inputs, you have to enter your main email address where ReMailD will auto-answer. \nNote:\n    To proceed, you need a strong email password because enabling imap and smtp is a potential security risk for your email account.[/blue]\n",
            "recovery": "\n[blue]Now, configure your recovery email for ReMailD: [/blue]\n",
            "meta": "\n[blue]Let's start creating your new account! To begin, enter the new account path and name.[/blue]\n"
        },
        "askMeta": {
            "path": "Where do you want to save your account? ",
            "name": "How do you want to name your account? "
        },
        "askEmail": {
            "mainEmail": "Enter your email address: ",
            "recoveryEmail": "Enter your recovery email address: "
        },
        "askPassword": {
            "password": "Enter the correct password for your email: ",
            "repeatPassword": "Repeat your email password: "
        },
        "askImap": {
            "server_address": "Enter the imap server address (host) of your email: ",
            "port": "Enter the imap port of your email address: "
        },
        "askSmtp": {
            "server_address": "Enter the smtp server address (host) of your email: ",
            "port": "Enter the smtp port of your email address: "
        }
    },
    "de": {
        "intro": {
            "main": "\nGeben Sie in den nächsten Eingaben Ihre Haupt-E-Mail-Adresse ein, auf die ReMailD automatisch antworten soll.\n",
            "recovery": "\nKonfigurieren Sie jetzt Ihre Wiederherstellungs-E-Mail für ReMailD: \n",
            "meta": "\nLassen Sie uns mit der Erstellung Ihres neuen Kontos beginnen! Geben Sie zuerst den Pfad und Namen des neuen Kontos ein.\n"
        },
        "askMeta": {
            "path": "Wo möchten Sie Ihr Konto speichern? ",
            "name": "Wie möchten Sie Ihr Konto nennen? "
        },
        "askEmail": {
            "mainEmail": "Geben Sie Ihre E-Mail-Adresse ein: ",
            "recoveryEmail": "Geben Sie Ihre Wiederherstellungs-E-Mail-Adresse ein: "
        },
        "askPassword": {
            "password": "Geben Sie das korrekte Passwort für Ihre E-Mail ein: ",
            "repeatPassword": "Wiederholen Sie das Passwort Ihrer E-Mail: "
        },
        "askImap": {
            "server_address": "Geben Sie die IMAP-Serveradresse (Host) Ihrer E-Mail ein: ",
            "port": "Geben Sie den IMAP-Port Ihrer E-Mail-Adresse ein: "
        },
        "askSmtp": {
            "server_address": "Geben Sie die SMTP-Serveradresse (Host) Ihrer E-Mail ein: ",
            "port": "Geben Sie den SMTP-Port Ihrer E-Mail-Adresse ein: "
        }
    },
    "fr": {
        "intro": {
            "main": "\nDans les prochaines entrées, vous devez saisir votre adresse email principale où ReMailD répondra automatiquement.\n",
            "recovery": "\nMaintenant, configurez votre email de récupération pour ReMailD : \n",
            "meta": "\nCommençons à créer votre nouveau compte ! Pour commencer, entrez le chemin et le nom du nouveau compte.\n"
        },
        "askMeta": {
            "path": "Où souhaitez-vous enregistrer votre compte ? ",
            "name": "Comment souhaitez-vous nommer votre compte ? "
        },
        "askEmail": {
            "mainEmail": "Entrez votre adresse email : ",
            "recoveryEmail": "Entrez votre adresse email de récupération : "
        },
        "askPassword": {
            "password": "Entrez le mot de passe correct pour votre email : ",
            "repeatPassword": "Répétez le mot de passe de votre email : "
        },
        "askImap": {
            "server_address": "Entrez l'adresse du serveur IMAP (hôte) de votre email : ",
            "port": "Entrez le port IMAP de votre adresse email : "
        },
        "askSmtp": {
            "server_address": "Entrez l'adresse du serveur SMTP (hôte) de votre email : ",
            "port": "Entrez le port SMTP de votre adresse email : "
        }
    },
    "es": {
        "intro": {
            "main": "\nEn las siguientes entradas, debes ingresar tu dirección de correo electrónico principal donde ReMailD responderá automáticamente.\n",
            "recovery": "\nAhora, configura tu correo electrónico de recuperación para ReMailD: \n",
            "meta": "\n¡Empecemos a crear tu nueva cuenta! Para comenzar, ingresa la ruta y el nombre de la nueva cuenta.\n"
        },
        "askMeta": {
            "path": "¿Dónde quieres guardar tu cuenta? ",
            "name": "¿Cómo quieres nombrar tu cuenta? "
        },
        "askEmail": {
            "mainEmail": "Ingresa tu dirección de correo electrónico: ",
            "recoveryEmail": "Ingresa tu dirección de correo electrónico de recuperación: "
        },
        "askPassword": {
            "password": "Ingresa la contraseña correcta para tu correo electrónico: ",
            "repeatPassword": "Repite la contraseña de tu correo electrónico: "
        },
        "askImap": {
            "server_address": "Ingresa la dirección del servidor IMAP (host) de tu correo electrónico: ",
            "port": "Ingresa el puerto IMAP de tu dirección de correo electrónico: "
        },
        "askSmtp": {
            "server_address": "Ingresa la dirección del servidor SMTP (host) de tu correo electrónico: ",
            "port": "Ingresa el puerto SMTP de tu dirección de correo electrónico: "
        }
    }
}