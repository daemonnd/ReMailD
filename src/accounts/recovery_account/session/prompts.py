from typing import Dict, Union
from rich import print
from . . . import __version__
# define prompt for the first usage of the app (welcome msg, recovery email, login pass, ...)
SIGN_UP_PROMPTS: dict = { # type: ignore
    "en": {
            "intro": {"start": f"""\n [#00aa77]
        Welcome to ReMailD ([#00cadb bold]v{__version__}[/#00cadb bold])!

        ReMailD is a secure, command-line email auto-responder designed for Ubuntu.

        It uses advanced filters to automatically reply to safe emails while blocking phishing, ads, or suspicious messages.

        Your data stays private and secure, stored only on your device with strong AES encryption.

        Let's get started by setting up remaild! [/#00aa77]

        [Press Enter to continue]
        """,
        "recovery": "[blue]\nConfigure your recovery email address now.\nReMailD needs a recovery email address for 2FA logins, \nnotifications on logins on user accounts and much more!\n[/blue]"
        },
        "login": {
            "intro": "[blue]Let's start with your master password. You will always need it to use remaild.\nOver 20 characters are recommended.\n[/blue]",
            "pass": "Enter a strong master password: ",
            "repeat_pass": "Repeat the password: "
        },

        "askEmail": "Enter your recovery email address: ",
        "askPassword": {
                "password": "Enter the correct password for your recovery email: ",
                "repeatPassword": "Repeat your recovery email password: "
            },
        "askSmtp": {
            "server_address": "Enter the smtp server address (host) of your email: ",
            "port": "Enter the smtp port of your email address: "
        },



        },
        "de": {
        "intro": {
            "start": """\n
            Willkommen bei ReMailD (v1.01.1 alpha)!

            ReMailD ist ein sicherer, Kommandozeilen-basierter E-Mail-Autoresponder für Ubuntu.

            Es verwendet fortschrittliche Filter, um automatisch auf sichere E-Mails zu antworten und Phishing, Werbung oder verdächtige Nachrichten zu blockieren.

            Ihre Daten bleiben privat und sicher, nur auf Ihrem Gerät mit starker AES-Verschlüsselung gespeichert.

            Lasst uns beginnen, ihr erstes Konto einzurichten!

            [Drücken Sie Enter, um fortzufahren]
            """,
            "recovery": "Konfigurieren Sie jetzt Ihre Wiederherstellungs-E-Mail-Adresse.\nReMailD benötigt eine Wiederherstellungs-E-Mail-Adresse für 2FA-Logins, \nBenachrichtigungen bei Logins in user-Konten und vieles mehr!"
        },
        "askEmail": "Geben Sie Ihre Wiederherstellungs-E-Mail-Adresse ein: ",
        "askPassword": {
            "password": "Geben Sie das korrekte Passwort für Ihre Wiederherstellungs-E-Mail ein: ",
            "repeatPassword": "Wiederholen Sie das Passwort Ihrer Wiederherstellungs-E-Mail: "
        },
        "askSmtp": {
            "server_address": "Geben Sie die SMTP-Serveradresse (Host) Ihrer E-Mail ein: ",
            "port": "Geben Sie den SMTP-Port Ihrer E-Mail-Adresse ein: "
        },
        "login": "Geben Sie ein starkes Passwort für die Anmeldung bei ReMailD ein: "
    },
    "fr": {
        "intro": {
            "start": """\n
            Bienvenue sur ReMailD (v1.01.1 alpha) !

            ReMailD est un répondeur automatique d'emails sécurisé en ligne de commande, conçu pour Ubuntu.

            Il utilise des filtres avancés pour répondre automatiquement aux emails sécurisés tout en bloquant les emails de phishing, publicités ou messages suspects.

            Vos données restent privées et sécurisées, stockées uniquement sur votre appareil avec un chiffrement AES robuste.

            Commençons par configurer votre premier compte email !

            [Appuyez sur Entrée pour continuer]
            """,
            "recovery": "Configurez maintenant votre adresse email de récupération.\nReMailD a besoin d'une adresse email de récupération pour les connexions 2FA, \nles notifications sur les connexions aux user-comptes et bien plus encore !"
        },
        "askEmail": "Entrez votre adresse email de récupération : ",
        "askPassword": {
            "password": "Entrez le mot de passe correct pour votre email de récupération : ",
            "repeatPassword": "Répétez le mot de passe de votre email de récupération : "
        },
        "askSmtp": {
            "server_address": "Entrez l'adresse du serveur SMTP (hôte) de votre email : ",
            "port": "Entrez le port SMTP de votre adresse email : "
        },
        "login": "Entrez un mot de passe robuste pour vous connecter à ReMailD : "
    },
    "es": {
        "intro": {
            "start": """\n
            ¡Bienvenido a ReMailD (v1.01.1 alpha)!

            ReMailD es un respondedor automático de correos electrónicos seguro basado en línea de comandos, diseñado para Ubuntu.

            Utiliza filtros avanzados para responder automáticamente a correos electrónicos seguros mientras bloquea phishing, anuncios o mensajes sospechosos.

            Tus datos permanecen privados y seguros, almacenados solo en tu dispositivo con un cifrado AES robusto.

            ¡Empecemos configurando tu primera cuenta de correo electrónico!

            [Presiona Enter para continuar]
            """,
            "recovery": "Configura ahora tu dirección de correo electrónico de recuperación.\nReMailD necesita una dirección de correo de recuperación para inicios de sesión con 2FA, \nnotificaciones sobre inicios de sesión en cuentas secundarias y mucho más."
        },
        "askEmail": "Ingresa tu dirección de correo electrónico de recuperación: ",
        "askPassword": {
            "password": "Ingresa la contraseña correcta para tu correo de recuperación: ",
            "repeatPassword": "Repite la contraseña de tu correo de recuperación: "
        },
        "askSmtp": {
            "server_address": "Ingresa la dirección del servidor SMTP (host) de tu correo: ",
            "port": "Ingresa el puerto SMTP de tu dirección de correo electrónico: "
        },
        "login": "Ingresa una contraseña segura para iniciar sesión en ReMailD: "
    }

}