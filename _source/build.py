#!/usr/bin/env python3
"""Build the BAS Digital Solutions static site into ../site (or argv[1])."""
import json, os, sys, shutil

SITE = "https://basdigitalsolutions.ca"
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "site")
EMAIL = "info@basdigitalsolutions.ca"
TALLY = "https://tally.so/r/rDybZX"
TALLY_EMBED = "https://tally.so/embed/rDybZX?alignLeft=1&amp;hideTitle=1&amp;transparentBackground=1&amp;dynamicHeight=1"
NB = " "  # non-breaking space for French typography

# ---------- shared UI strings ----------
UI = {
    "en": {
        "skip": "Skip to content",
        "nav": [("rfq.html", "RFQ automation"), ("dynamics365.html", "Dynamics 365"),
                ("customer-support.html", "Customer support"), ("/#pilot", "Pilot"),
                ("/#resources", "Guides"), ("#contact", "Contact")],
        "cta": "Book a free 30-min call",
        "menu": "Menu",
        "home": "/",
        "contact_h": "Book your free 30-minute workflow call",
        "contact_p": "Describe your business, your current tools and the task you want to improve. Choose English or French in the form. Sending an inquiry does not place an order.",
        "contact_alt": f'Prefer email? <a href="mailto:{EMAIL}">{EMAIL}</a>',
        "contact_open": "Open the form in a new tab",
        "contact_note": "Suggest your availability in the form. We confirm the time by email; the form does not reserve a slot automatically.",
        "after_h": "What happens after you submit?",
        "after_p": "We review your request, identify missing details and discuss fit and scope with you. You receive a proposal before any implementation.",
        "form_title": "Project request form",
        "privacy_short": "Your contact details and project description are used only to review and answer your inquiry. Please do not send confidential drawings, passwords or payment details through the form.",
        "privacy_link": "Privacy policy",
        "privacy_href": "privacy.html",
        "tagline": "RFQ and workflow automation for industrial companies. Montreal, Quebec.",
        "guides": "Guides",
        "services": "Services",
    },
    "fr": {
        "skip": "Aller au contenu",
        "nav": [("rfq-fr.html", "Demandes de prix"), ("dynamics365-fr.html", "Dynamics 365"),
                ("service-client.html", "Service à la clientèle"), ("fr.html#pilot", "Projet pilote"),
                ("fr.html#resources", "Guides"), ("#contact", "Contact")],
        "cta": "Réserver un appel gratuit",
        "menu": "Menu",
        "home": "fr.html",
        "contact_h": "Réservez votre appel gratuit de 30 minutes",
        "contact_p": "Décrivez votre entreprise, vos outils actuels et la tâche à améliorer. Choisissez le français ou l'anglais dans le formulaire. L'envoi d'une demande ne constitue pas une commande.",
        "contact_alt": f'Vous préférez le courriel{NB}? <a href="mailto:{EMAIL}">{EMAIL}</a>',
        "contact_open": "Ouvrir le formulaire dans un nouvel onglet",
        "contact_note": "Indiquez vos disponibilités dans le formulaire. Nous confirmons l'heure par courriel; le formulaire ne réserve pas de plage horaire automatiquement.",
        "after_h": "Que se passe-t-il après l'envoi?",
        "after_p": "Nous examinons votre demande, relevons les renseignements manquants et discutons avec vous de la pertinence et de la portée. Vous recevez une proposition avant toute mise en œuvre.",
        "form_title": "Formulaire de demande de projet",
        "privacy_short": "Vos coordonnées et la description de votre projet servent uniquement à examiner votre demande et à y répondre. N'envoyez pas de dessins confidentiels, de mots de passe ni de renseignements de paiement par le formulaire.",
        "privacy_link": "Politique de confidentialité",
        "privacy_href": "confidentialite.html",
        "tagline": "Automatisation des demandes de prix et des processus pour les entreprises industrielles. Montréal, Québec.",
        "guides": "Guides",
        "services": "Services",
    },
}

LOGO_MARK = """<svg class="mark" viewBox="0 0 96 96" aria-hidden="true" focusable="false"><rect width="96" height="96" rx="20" fill="#173a31"/><g fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".85"><path d="M22 28 C40 28 40 48 56 48"/><path d="M22 48 H56"/><path d="M22 68 C40 68 40 48 56 48"/></g><path d="M56 48 H64" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="73" cy="48" r="12" fill="#e0954a"/><path d="M67.5 48.5 L71.5 52.5 L79 44" fill="none" stroke="#173a31" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>"""


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def steps(lang):
    if lang == "en":
        items = [("Capture", "Requests from email and forms land in one queue."),
                 ("Check", "Quantity, revision, material, drawing and delivery date are extracted. Gaps are flagged."),
                 ("Prepare", "A draft record is ready for your system, such as Dynamics 365 after assessment."),
                 ("Approve", "Your estimator reviews and sends. Nothing is quoted automatically.")]
        label = "How an RFQ moves through the process"
    else:
        items = [("Recevoir", "Les demandes par courriel et formulaire arrivent dans une seule file."),
                 ("Vérifier", "Quantité, révision, matériau, dessin et date de livraison sont extraits. Les manques sont signalés."),
                 ("Préparer", "Une fiche provisoire est prête pour votre système, comme Dynamics 365 après évaluation."),
                 ("Approuver", "Votre estimateur vérifie et envoie. Aucune soumission n'est faite automatiquement.")]
        label = "Le parcours d'une demande de prix"
    lis = "".join(f'<li><span class="n">{i}</span><b>{t}</b>{d}</li>' for i, (t, d) in enumerate(items, 1))
    return f'<ol class="steps" aria-label="{label}">{lis}</ol>'


def trust(lang):
    return ('<p class="trust">English and French service. Human approval on every quote. Scope and price agreed before we build.</p>'
            if lang == "en" else
            '<p class="trust">Service en français et en anglais. Approbation humaine pour chaque soumission. Portée et prix convenus avant la réalisation.</p>')


def pilot(lang):
    if lang == "en":
        return """<section id="pilot"><div class="wrap">
<h2>The 2-week RFQ pilot</h2>
<div class="pilot">
<div class="cols">
<div><h3>Week 1: Map</h3><p>We map your current RFQ process and choose one request type to automate.</p></div>
<div><h3>Week 2: Build and test</h3><p>We build and test it on your sample requests, then hand over documentation.</p></div>
<div><h3>What you get</h3><p>Working intake, a missing-information checklist, a review step and a clear recommendation on next steps.</p></div>
</div>
<p><strong>Fixed price, confirmed in your proposal. No ongoing commitment.</strong> The schedule starts once scope, access and sample requests are agreed. No revenue guarantees. No production ERP writes until you approve.</p>
<p class="note">Any discount and any permission to describe results are agreed separately. No case study, even anonymized, is published without your approval.</p>
</div></div></section>"""
    return f"""<section id="pilot"><div class="wrap">
<h2>Le projet pilote de 2 semaines</h2>
<div class="pilot">
<div class="cols">
<div><h3>Semaine 1{NB}: cartographier</h3><p>Nous cartographions votre processus actuel et choisissons un type de demande à automatiser.</p></div>
<div><h3>Semaine 2{NB}: réaliser et tester</h3><p>Nous le réalisons et le testons avec vos exemples de demandes, puis remettons la documentation.</p></div>
<div><h3>Ce que vous obtenez</h3><p>Une réception fonctionnelle, une liste de vérification des renseignements manquants, une étape de révision et une recommandation claire pour la suite.</p></div>
</div>
<p><strong>Prix fixe, confirmé dans votre proposition. Aucun engagement continu.</strong> L'échéancier commence une fois la portée, les accès et les exemples convenus. Aucune garantie de revenus. Aucune écriture dans l'ERP de production sans votre approbation.</p>
<p class="note">Tout rabais et toute permission de décrire les résultats sont convenus séparément. Aucune étude de cas, même anonymisée, n'est publiée sans votre approbation.</p>
</div></div></section>"""


def page(slug, lang, alt, title, desc, body, h1, lede, *, hero_extra="", contact=True, schema=None, kind="page"):
    u = UI[lang]
    other = "fr" if lang == "en" else "en"
    url = f"{SITE}/" if slug == "index.html" else f"{SITE}/{slug}"
    alt_url = None
    if alt:
        alt_url = f"{SITE}/" if alt == "index.html" else f"{SITE}/{alt}"
    links = [f'<link rel="canonical" href="{url}">']
    if alt_url:
        en_url, fr_url = (url, alt_url) if lang == "en" else (alt_url, url)
        links += [f'<link rel="alternate" hreflang="en" href="{en_url}">',
                  f'<link rel="alternate" hreflang="fr" href="{fr_url}">',
                  f'<link rel="alternate" hreflang="x-default" href="{en_url}">']
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in u["nav"])
    alt_href = ("/" if alt == "index.html" else alt) if alt else ("fr.html" if lang == "en" else "/")
    lang_link = (f'<a class="lang" href="{alt_href}" lang="{other}" hreflang="{other}">'
                 f'{"Français" if lang == "en" else "English"}</a>')
    ld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "BAS Digital Solutions",
          "url": f"{SITE}/", "logo": f"{SITE}/bas-logo.svg", "email": EMAIL,
          "areaServed": ["Montreal", "Quebec", "Canada"], "availableLanguage": ["English", "French"],
          "founder": {"@type": "Person", "name": "Bandar Sharkh"},
          "description": "RFQ and workflow automation for industrial companies, with human approval on every quote."}
    if schema:
        ld = [ld, schema]
    contact_html = ""
    if contact:
        contact_html = f"""<section id="contact" class="contact"><div class="wrap">
<h2>{u["contact_h"]}</h2>
<p>{u["contact_p"]}</p>
<p>{u["contact_alt"]} · <a href="{TALLY}" target="_blank" rel="noopener">{u["contact_open"]}</a></p>
<p class="note">{u["contact_note"]}</p>
<h3>{u["after_h"]}</h3>
<p>{u["after_p"]}</p>
<iframe src="{TALLY_EMBED}" title="{u["form_title"]}" loading="lazy"></iframe>
</div></section>"""
    hero = f"""<section class="hero"><div class="wrap">
<h1>{h1}</h1>
<p class="lede">{lede}</p>
{hero_extra}
</div></section>""" if h1 else ""
    doc = f"""<!DOCTYPE html>
<html lang="{lang}-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{chr(10).join(links)}
<meta name="theme-color" content="#173a31">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="BAS Digital Solutions">
<meta property="og:locale" content="{"en_CA" if lang == "en" else "fr_CA"}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:alt" content="BAS Digital Solutions">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="{kind}">
<a class="skip" href="#main">{u["skip"]}</a>
<header class="site"><div class="wrap bar">
<a class="logo" href="{u["home"]}" aria-label="BAS Digital Solutions">{LOGO_MARK}<span><b>BAS</b> Digital Solutions</span></a>
<details class="menu"><summary>{u["menu"]}</summary>
<nav aria-label="{"Main" if lang == "en" else "Principal"}">{nav}{lang_link}</nav>
</details>
<nav class="wide" aria-label="{"Main" if lang == "en" else "Principal"}">{nav}{lang_link}</nav>
</div></header>
<main id="main">
{hero}
{body}
{contact_html}
</main>
<footer class="site"><div class="wrap">
<div class="fcols">
<div><p class="flogo">{LOGO_MARK}<b>BAS Digital Solutions</b></p><p>{u["tagline"]}</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><p><b>{u["services"]}</b></p><p>{"<br>".join(f'<a href="{h}">{t}</a>' for h, t in u["nav"][:3])}</p></div>
<div><p><b>{u["guides"]}</b></p><p>{GUIDE_LINKS[lang]}</p></div>
</div>
<p id="privacy" class="note">{u["privacy_short"]} <a href="{u["privacy_href"]}">{u["privacy_link"]}</a>.</p>
<p class="note">© 2026 BAS Digital Solutions · {lang_link}</p>
</div></footer>
<script src="/site.js" defer></script>
</body>
</html>
"""
    if not contact:
        home = "index.html" if lang == "en" else "fr.html"
        doc = doc.replace('href="#contact"', f'href="{home}#contact"')
    for a, b in [('href="/styles.css"', 'href="styles.css"'), ('src="/site.js"', 'src="site.js"'),
                 ('href="/favicon.svg"', 'href="favicon.svg"'), ('href="/#', 'href="index.html#'),
                 ('href="/"', 'href="index.html"'), ('href="/fr.html', 'href="fr.html')]:
        doc = doc.replace(a, b)
    return doc


GUIDE_LINKS = {
    "en": '<a href="rfq-intake.html">How to automate RFQ intake</a><br><a href="law25-ai.html">Law 25 and AI for Quebec manufacturers</a><br><a href="quebec-en.html">RFQ automation in Montreal and Quebec</a><br><a href="rfq-checklist-en.html">RFQ readiness checklist</a>',
    "fr": '<a href="reception-demandes-prix.html">Automatiser la réception des demandes de prix</a><br><a href="loi25-ia.html">Loi 25 et IA pour les manufacturiers du Québec</a><br><a href="quebec.html">Automatisation industrielle à Montréal et au Québec</a><br><a href="rfq-checklist-fr.html">Liste de préparation aux demandes de prix</a>',
}

CTA = {
    "en": '<p><a class="btn" href="#contact">Book a free 30-min workflow call</a></p><p class="note">We confirm the time by email after your request.</p>',
    "fr": '<p><a class="btn" href="#contact">Réserver un appel gratuit de 30 minutes</a></p><p class="note">Nous confirmons l\'heure par courriel après votre demande.</p>',
}


def demo(lang):
    if lang == "en":
        h, p = "See a sample request move through the workflow", "Choose a scenario. Fictional data; nothing is sent and no AI runs on this page."
        sc = [("Industrial RFQ", "“Please quote 40 brackets, revision B, for November delivery.”",
               ["Collect quantity, revision and requested date", "Flag missing material and drawing", "Prepare the RFQ for a quotation reviewer"],
               [("Quantity", "40"), ("Missing", "Material and drawing"), ("ERP status", "Assessment required, no production write")]),
              ("Support question", "“Can you explain how your service works in French?”",
               ["Read the question and language", "Answer from approved service information", "Hand anything uncertain to the team"],
               [("Language", "French"), ("Reply", "Draft for review"), ("Handoff", "Team handles pricing and commitments")]),
              ("Customer request", "“We need our website to send new requests into our customer tracker.”",
               ["Capture the request and preferred language", "Check the service and missing details", "Prepare a record and next action"],
               [("Service", "Website and CRM"), ("Status", "Needs review"), ("Next action", "Confirm current tools and scope")])]
        lab = ("Sample input", "Workflow steps", "Example result")
    else:
        h, p = "Voyez une demande type traverser le processus", f"Choisissez un scénario. Données fictives{NB}: rien n'est envoyé et aucune IA ne fonctionne sur cette page."
        sc = [("Demande de prix industrielle", "« Pouvez-vous soumissionner 40 supports, révision B, livraison en novembre? »",
               ["Recueillir la quantité, la révision et la date demandée", "Signaler le matériau et le dessin manquants", "Préparer la demande pour l'estimateur"],
               [("Quantité", "40"), ("Manquant", "Matériau et dessin"), ("Statut ERP", "Évaluation requise, aucune écriture en production")]),
              ("Question au service à la clientèle", "« Pouvez-vous m'expliquer votre service en anglais? »",
               ["Lire la question et la langue", "Répondre à partir de l'information approuvée", "Transférer à l'équipe tout ce qui est incertain"],
               [("Langue", "Anglais"), ("Réponse", "Brouillon à réviser"), ("Transfert", "L'équipe gère les prix et les engagements")]),
              ("Demande de client", "« Notre site Web doit envoyer les nouvelles demandes dans notre outil de suivi. »",
               ["Recevoir la demande et la langue préférée", "Vérifier le service et les détails manquants", "Préparer une fiche et la prochaine action"],
               [("Service", "Site Web et CRM"), ("Statut", "À réviser"), ("Prochaine action", "Confirmer les outils et la portée")])]
        lab = ("Demande type", "Étapes du processus", "Résultat type")
    tabs = "".join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" aria-controls="sc{i}" id="tab{i}">{s[0]}</button>' for i, s in enumerate(sc))
    panels = ""
    for i, (name, q, st, res) in enumerate(sc):
        lis = "".join(f"<li>{x}</li>" for x in st)
        dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in res)
        panels += f"""<div class="panel" role="tabpanel" id="sc{i}" aria-labelledby="tab{i}"{"" if i == 0 else " hidden"}>
<div><p class="lab">{lab[0]}</p><blockquote>{q}</blockquote></div>
<div><p class="lab">{lab[1]}</p><ol>{lis}</ol></div>
<div><p class="lab">{lab[2]}</p><dl>{dl}</dl></div></div>"""
    return f"""<section id="demo"><div class="wrap">
<h2>{h}</h2><p>{p}</p>
<div class="demo"><div class="tabs" role="tablist">{tabs}</div>{panels}</div>
</div></section>"""


def faq(items):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


def faq_schema(items):
    import re
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": re.sub("<[^>]+>", "", q),
                            "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in items]}


FAQ_EN = [
    ("Do we have to change our ERP?", "Not necessarily. We assess your current tools, interfaces and access first. A pilot can start in a separate review queue. Any integration, including Dynamics 365, depends on that assessment."),
    ("Are quotes sent automatically?", "No. Your estimator reviews and approves every quote before it is sent. The workflow flags gaps; it does not make commercial commitments for you."),
    ("How much does a project cost?", "It depends on scope, applications and ongoing support. The pilot has a fixed price in your proposal, and you always receive a proposal before work begins. Third-party subscriptions are agreed separately."),
    ("Do you guarantee revenue or time savings?", "No. We agree on a measurable objective and test the workflow. Results depend on your process, data quality, adoption and external tools."),
    ("Who sees our drawings?", "Do not send confidential drawings through the public form. Before any project data is shared, we agree on who can access it, which providers are used, where it is stored and how long it is kept. Redacted samples are used for the pilot."),
]
FAQ_FR = [
    (f"Devons-nous changer d'ERP{NB}?", "Pas nécessairement. Nous évaluons d'abord vos outils, interfaces et accès. Un projet pilote peut commencer dans une file de révision distincte. Toute intégration, y compris Dynamics 365, dépend de cette évaluation."),
    ("Les soumissions sont-elles envoyées automatiquement?", "Non. Votre estimateur vérifie et approuve chaque soumission avant l'envoi. Le processus signale les manques; il ne prend aucun engagement commercial à votre place."),
    ("Combien coûte un projet?", "Cela dépend de la portée, des applications et du soutien continu. Le projet pilote a un prix fixe dans votre proposition, et vous recevez toujours une proposition avant le début des travaux. Les abonnements de tiers sont convenus séparément."),
    ("Garantissez-vous des revenus ou des gains de temps?", "Non. Nous convenons d'un objectif mesurable et testons le processus. Les résultats dépendent de votre processus, de la qualité des données, de l'adoption et des outils externes."),
    ("Qui voit nos dessins?", "N'envoyez pas de dessins confidentiels par le formulaire public. Avant tout partage de données de projet, nous convenons des personnes autorisées, des fournisseurs, du lieu de stockage et de la durée de conservation. Le projet pilote utilise des exemples caviardés."),
]


def services(lang):
    if lang == "en":
        cards = [("rfq.html", "RFQ intake and workflow automation", "Capture, check and prepare quote requests in a process your team approves."),
                 ("dynamics365.html", "CRM and ERP integration", "Connect your intake to your tools and assess a Microsoft Dynamics 365 integration."),
                 ("customer-support.html", "Customer support assistants", "Answer from approved information in English and French, capture requests and hand exceptions to your team.")]
        h, more, also = "Services built around your operations", "Learn more", "Also available: lead capture and follow-up, and websites connected to your business tools."
    else:
        cards = [("rfq-fr.html", "Réception des demandes et automatisation des processus", "Recevoir, vérifier et préparer les demandes de prix dans un processus approuvé par votre équipe."),
                 ("dynamics365-fr.html", "Intégration CRM et ERP", "Relier la réception à vos outils et évaluer une intégration Microsoft Dynamics 365."),
                 ("service-client.html", "Assistants de service à la clientèle", "Répondre en français et en anglais à partir d'information approuvée, recevoir les demandes et transférer les exceptions à votre équipe.")]
        h, more, also = "Des services adaptés à vos opérations", "En savoir plus", "Aussi offerts : suivi des prospects et sites Web reliés à vos outils d'affaires.".replace(" :", NB + ":")
    c = "".join(f'<div class="card"><h3>{t}</h3><p>{d}</p><p><a href="{href}">{more}</a></p></div>' for href, t, d in cards)
    return f'<section id="services"><div class="wrap"><h2>{h}</h2><div class="grid">{c}</div><p class="note">{also}</p></div></section>'


def resources(lang):
    if lang == "en":
        h, p = "Practical guides", "Short, plain-language guides for planning your first workflow."
    else:
        h, p = "Guides pratiques", "De courts guides en langage clair pour planifier votre premier processus."
    items = GUIDE_LINKS[lang].split("<br>")
    return f'<section id="resources"><div class="wrap"><h2>{h}</h2><p>{p}</p><ul class="guides">{"".join(f"<li>{x}</li>" for x in items)}</ul></div></section>'


def about(lang):
    if lang == "en":
        return """<section id="about"><div class="wrap narrow">
<h2>Industrial experience, a practical approach</h2>
<p>Bandar Sharkh, founder of BAS Digital Solutions, is a mechanical design specialist with more than 15 years in manufactured products and industrial systems. He builds RFQ and customer-request workflows that your team approves at every step.</p>
</div></section>"""
    return """<section id="about"><div class="wrap narrow">
<h2>Une expérience industrielle, une approche pratique</h2>
<p>Bandar Sharkh, fondateur de BAS Digital Solutions, est spécialiste en conception mécanique et compte plus de 15 ans d'expérience en produits manufacturés et en systèmes industriels. Il conçoit des processus de demandes de prix et de demandes de clients que votre équipe approuve à chaque étape.</p>
</div></section>"""


def audit(lang):
    if lang == "en":
        return """<section id="audit" class="band"><div class="wrap">
<h2>Start with a free 30-minute RFQ audit</h2>
<p>We look at one type of request, the details that often go missing and the possible next steps. No ERP access or confidential documents are needed for this call.</p>
<p><a class="btn" href="#contact">Request the free audit</a> <a class="btn alt" href="rfq-checklist-en.pdf">Download the RFQ readiness checklist (PDF)</a></p>
</div></section>"""
    return """<section id="audit" class="band"><div class="wrap">
<h2>Commencez par un audit gratuit de 30 minutes</h2>
<p>Nous examinons un type de demande, les renseignements qui manquent souvent et les prochaines étapes possibles. Aucun accès à l'ERP ni document confidentiel n'est nécessaire pour cet appel.</p>
<p><a class="btn" href="#contact">Demander l'audit gratuit</a> <a class="btn alt" href="rfq-checklist-fr.pdf">Télécharger la liste de préparation (PDF)</a></p>
</div></section>"""


def section(h, inner, cls="", id_=""):
    return f'<section{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}><div class="wrap narrow"><h2>{h}</h2>{inner}</div></section>'


def faq_section(lang, items):
    return f'<section id="faq"><div class="wrap narrow"><h2>{"Questions before you start" if lang == "en" else "Questions avant de commencer"}</h2>{faq(items)}</div></section>'


PAGES = []


def add(*a, **k):
    PAGES.append((a, k))


# ---------- Home ----------
add("index.html", "en", "fr.html",
    "RFQ & Workflow Automation for Industrial Companies | Montreal | BAS Digital Solutions",
    "Montreal RFQ automation: capture requests, flag missing details and prepare quotes for human review. Book a free 30-min call.",
    audit("en") + demo("en") + services("en") + pilot("en") + about("en") + resources("en") + faq_section("en", FAQ_EN),
    "RFQs stuck in an inbox? Prepare them for your ERP, with review before the quote.",
    "For manufacturers and industrial suppliers in Quebec and Canada. Drawings, revisions, materials and handoff to your ERP in one controlled process, with Dynamics 365, Outlook or Teams after assessment.",
    hero_extra=CTA["en"] + steps("en") + trust("en"), schema=faq_schema(FAQ_EN), kind="home")
add("fr.html", "fr", "index.html",
    "Automatisation des demandes de prix | Montréal | BAS Digital Solutions",
    "Automatisation des demandes de prix à Montréal : réception structurée, renseignements manquants signalés, approbation humaine. Appel gratuit.".replace(" :", NB + ":"),
    audit("fr") + demo("fr") + services("fr") + pilot("fr") + about("fr") + resources("fr") + faq_section("fr", FAQ_FR),
    "Vos demandes de prix, prêtes pour votre ERP et révisées avant la soumission.",
    "Pour les manufacturiers et fournisseurs industriels du Québec et du Canada. Dessins, révisions, matériaux et transfert vers votre ERP dans un processus contrôlé, avec Dynamics 365, Outlook ou Teams après évaluation.",
    hero_extra=CTA["fr"] + steps("fr") + trust("fr"), schema=faq_schema(FAQ_FR), kind="home")

# ---------- RFQ ----------
RFQ_FAQ_EN = [FAQ_EN[0], FAQ_EN[1], ("Where is our data stored?", "Our inquiry form provider (Tally) reports storage in Europe. For project data, storage locations are agreed before any transfer, and a Law 25 assessment is part of project preparation. We do not promise Quebec-only hosting unless it is confirmed for your project."), FAQ_EN[4]]
RFQ_FAQ_FR = [FAQ_FR[0], FAQ_FR[1], ("Où nos données sont-elles stockées?", "Notre fournisseur de formulaire (Tally) indique un stockage en Europe. Pour les données de projet, les lieux de stockage sont convenus avant tout transfert, et une évaluation selon la Loi 25 fait partie de la préparation. Nous ne promettons pas un hébergement exclusivement au Québec, sauf s'il est confirmé pour votre projet."), FAQ_FR[4]]
add("rfq.html", "en", "rfq-fr.html",
    "Industrial RFQ Automation | Montreal | BAS Digital Solutions",
    "RFQ automation for Montreal and Quebec manufacturers: capture requests, flag missing information and prepare quotes for human review.",
    section("Built for industrial quoting", "<p>Requests arrive by email, PDF and web form. Someone retypes them, chases missing drawings and checks revisions by hand. BAS gives each request a clear, reviewed path.</p><p>Built for fabricators, machine shops and industrial suppliers who quote custom parts and equipment.</p>")
    + pilot("en") + faq_section("en", RFQ_FAQ_EN),
    "From incoming RFQ to a quote your team can approve.",
    "Capture requests in one place, flag what is missing and prepare a draft for your estimator. Nothing is quoted automatically.",
    hero_extra=CTA["en"] + steps("en"), schema=faq_schema(RFQ_FAQ_EN))
add("rfq-fr.html", "fr", "rfq.html",
    "Automatisation des demandes de prix industrielles | BAS Digital Solutions",
    "Automatisation des demandes de prix pour les manufacturiers de Montréal et du Québec : réception, renseignements manquants signalés et révision humaine.".replace(" :", NB + ":"),
    section("Conçu pour la soumission industrielle", "<p>Les demandes arrivent par courriel, en PDF et par formulaire Web. Quelqu'un les ressaisit, court après les dessins manquants et vérifie les révisions à la main. BAS donne à chaque demande un parcours clair et révisé.</p><p>Pour les ateliers de fabrication, d'usinage et les fournisseurs industriels qui soumissionnent des pièces et de l'équipement sur mesure.</p>")
    + pilot("fr") + faq_section("fr", RFQ_FAQ_FR),
    "De la demande de prix reçue à une soumission que votre équipe peut approuver.",
    "Recevez les demandes au même endroit, signalez ce qui manque et préparez un brouillon pour votre estimateur. Aucune soumission n'est faite automatiquement.",
    hero_extra=CTA["fr"] + steps("fr"), schema=faq_schema(RFQ_FAQ_FR))

# ---------- Dynamics 365 ----------
D_EN = """<section><div class="wrap"><h2>Assess, test, then approve</h2><div class="grid">
<div class="card"><h3>Assessment</h3><p>We review your entities, processes, volumes and access, and choose an integration approach. Microsoft documents OData and data management APIs for Finance and Supply Chain Management.</p></div>
<div class="card"><h3>Sandbox</h3><p>We build and test against a non-production environment with sample requests before anything touches live data.</p></div>
<div class="card"><h3>Approval</h3><p>Production writes start only after you approve the tested workflow, and your estimator still reviews every quote.</p></div>
</div>
<p class="note">This is not a preinstalled or certified connector. The approach depends on your entities and processing volume. <a href="https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/data-entities/integration-overview" rel="noopener">Microsoft integration overview</a></p>
</div></section>"""
D_FR = f"""<section><div class="wrap"><h2>Évaluer, tester, puis approuver</h2><div class="grid">
<div class="card"><h3>Évaluation</h3><p>Nous examinons vos entités, processus, volumes et accès, puis choisissons une approche d'intégration. Microsoft documente des API OData et de gestion des données pour Finance et Supply Chain Management.</p></div>
<div class="card"><h3>Environnement de test</h3><p>Nous réalisons et testons dans un environnement hors production avec des exemples de demandes, avant de toucher aux données réelles.</p></div>
<div class="card"><h3>Approbation</h3><p>Les écritures en production commencent seulement après votre approbation du processus testé, et votre estimateur vérifie toujours chaque soumission.</p></div>
</div>
<p class="note">Il ne s'agit pas d'un connecteur préinstallé ou certifié. L'approche dépend de vos entités et de votre volume de traitement. <a href="https://learn.microsoft.com/fr-ca/dynamics365/fin-ops-core/dev-itpro/data-entities/integration-overview" rel="noopener">Aperçu de l'intégration (Microsoft)</a></p>
</div></section>"""
add("dynamics365.html", "en", "dynamics365-fr.html",
    "Dynamics 365 Integration for RFQ Workflows | BAS Digital Solutions",
    "Assess a Dynamics 365 Finance and Supply Chain integration for RFQ workflows in Montreal and Quebec. Approval before production writes.",
    D_EN, "Connect your intake to Dynamics 365, after assessment.",
    "Send reviewed RFQ data into Dynamics 365 Finance and Supply Chain Management, without risking your production system.",
    hero_extra=CTA["en"] + steps("en"))
add("dynamics365-fr.html", "fr", "dynamics365.html",
    "Intégration Dynamics 365 pour les demandes de prix | BAS Digital Solutions",
    "Évaluer une intégration Dynamics 365 Finance et Supply Chain pour vos demandes de prix à Montréal et au Québec. Approbation avant toute écriture en production.",
    D_FR, "Reliez la réception à Dynamics 365, après évaluation.",
    "Transférez les demandes de prix révisées vers Dynamics 365 Finance et Supply Chain Management, sans risque pour votre système de production.",
    hero_extra=CTA["fr"] + steps("fr"))

# ---------- Customer support ----------
CS_EN = """<section><div class="wrap"><h2>What the assistant does</h2><div class="grid">
<div class="card"><h3>Approved answers</h3><p>Answers come only from information your team has reviewed, in English and French.</p></div>
<div class="card"><h3>Human handoff</h3><p>Pricing, commitments and exceptions go to the right person, with the conversation attached.</p></div>
<div class="card"><h3>Organized follow-up</h3><p>Requests are captured with the details needed and placed in your tracker or CRM.</p></div>
</div></div></section>"""
CS_FR = """<section><div class="wrap"><h2>Ce que fait l'assistant</h2><div class="grid">
<div class="card"><h3>Réponses approuvées</h3><p>Les réponses proviennent uniquement d'information révisée par votre équipe, en français et en anglais.</p></div>
<div class="card"><h3>Transfert à une personne</h3><p>Les prix, les engagements et les exceptions sont transférés à la bonne personne, avec la conversation.</p></div>
<div class="card"><h3>Suivi organisé</h3><p>Les demandes sont reçues avec les renseignements nécessaires et placées dans votre outil de suivi ou votre CRM.</p></div>
</div></div></section>"""
add("customer-support.html", "en", "service-client.html",
    "AI Customer Support Assistants | Montreal | BAS Digital Solutions",
    "Bilingual AI support assistants for Montreal and Quebec businesses: approved answers, request capture and clear handoff to your team.",
    CS_EN, "Helpful support. Your team stays in control.",
    "Answer routine questions in English and French, capture requests and hand complex cases to the right person.",
    hero_extra=CTA["en"])
add("service-client.html", "fr", "customer-support.html",
    "Assistants IA de service à la clientèle | Montréal | BAS Digital Solutions",
    "Assistants IA bilingues pour les entreprises de Montréal et du Québec : réponses approuvées, réception des demandes et transfert clair à votre équipe.".replace(" :", NB + ":"),
    CS_FR, "Un soutien utile. Votre équipe garde le contrôle.",
    "Répondez aux questions courantes en français et en anglais, recevez les demandes et transférez les cas complexes à la bonne personne.",
    hero_extra=CTA["fr"])

# ---------- Guides ----------
G1_EN = (section("One focused first workflow", "<p>Start with one recurring request type. Use a few redacted examples, including an incomplete request and one with a revised drawing.</p>")
         + section("Define the required information", "<p>For each request, list the fields to capture: customer, part, quantity, material, revision, drawing and requested date. Keep information that was received separate from information that was inferred.</p>")
         + section("Design for exceptions", "<p>Missing drawings, duplicates and new revisions should go to human review. Test these cases before expanding the workflow, and check who can access the documents.</p>")
         + section("Keep an approval step", "<p>Place the draft record in a review queue so an estimator checks it before a quote is sent. Measure corrections and time at each stage to guide the next phase.</p>"))
G1_FR = (section("Un premier processus ciblé", "<p>Commencez par un type de demande récurrent. Utilisez quelques exemples caviardés, dont une demande incomplète et une avec un dessin révisé.</p>")
         + section("Définir les renseignements requis", "<p>Pour chaque demande, dressez la liste des champs à recueillir : client, pièce, quantité, matériau, révision, dessin et date demandée. Séparez les renseignements reçus de ceux qui sont déduits.</p>".replace(" :", NB + ":"))
         + section("Prévoir les exceptions", "<p>Les dessins manquants, les doublons et les nouvelles révisions doivent passer par une révision humaine. Testez ces cas avant d'élargir le processus et vérifiez qui peut accéder aux documents.</p>")
         + section("Conserver une étape d'approbation", "<p>Placez la fiche provisoire dans une file de révision pour qu'un estimateur la vérifie avant l'envoi d'une soumission. Mesurez les corrections et le temps à chaque étape pour orienter la phase suivante.</p>"))
add("rfq-intake.html", "en", "reception-demandes-prix.html",
    "How to Automate RFQ Intake | BAS Digital Solutions",
    "A practical RFQ intake guide for Montreal and Quebec manufacturers: required fields, exceptions and approval before a quote is sent.",
    G1_EN, "How to automate RFQ intake", "A practical starting point for Montreal and Quebec manufacturers.", kind="guide")
add("reception-demandes-prix.html", "fr", "rfq-intake.html",
    "Automatiser la réception des demandes de prix | BAS Digital Solutions",
    "Guide pratique pour les manufacturiers de Montréal et du Québec : champs requis, exceptions et approbation avant l'envoi d'une soumission.".replace(" :", NB + ":"),
    G1_FR, "Automatiser la réception des demandes de prix", "Un point de départ pratique pour les manufacturiers de Montréal et du Québec.", kind="guide")

CAI = "https://www.cai.gouv.qc.ca/protection-renseignements-personnels/sujets-et-domaines-dinteret/principaux-changements-loi-25"
G2_EN = (section("Questions to resolve before a pilot", "<p>Before adding AI to intake, identify the personal information in emails, signatures and attachments. A drawing can be confidential even when it contains no personal information.</p>")
         + section("Plan data handling first", f"<p>The Commission d'accès à l'information describes privacy impact assessments for certain projects and for disclosures outside Quebec. List authorized people, providers, storage, retention and deletion; start with redacted samples; and have the person responsible for the protection of personal information approve the rules.</p><p>A general “Law 25 compliant” claim does not replace this assessment. This guide is not legal advice.</p><p class=\"note\">Source: <a href=\"{CAI}\" rel=\"noopener\">Commission d'accès à l'information, main changes under Law 25</a></p>"))
G2_FR = (section("Questions à régler avant un projet pilote", "<p>Avant d'ajouter l'IA à la réception, repérez les renseignements personnels dans les courriels, les signatures et les pièces jointes. Un dessin peut être confidentiel même sans renseignement personnel.</p>")
         + section("Planifier d'abord le traitement des données", f"<p>La Commission d'accès à l'information décrit les évaluations des facteurs relatifs à la vie privée pour certains projets et pour les communications à l'extérieur du Québec. Dressez la liste des personnes autorisées, des fournisseurs, du stockage, de la conservation et de la destruction; commencez avec des exemples caviardés; et faites approuver les règles par la personne responsable de la protection des renseignements personnels.</p><p>Une affirmation générale de « conformité à la Loi 25 » ne remplace pas cette évaluation. Ce guide ne constitue pas un avis juridique.</p><p class=\"note\">Source{NB}: <a href=\"{CAI}\" rel=\"noopener\">Commission d'accès à l'information, principaux changements de la Loi 25</a></p>"))
add("law25-ai.html", "en", "loi25-ia.html",
    "Law 25 and Industrial AI in Quebec | BAS Digital Solutions",
    "Law 25 and RFQ automation in Quebec: personal information, access and storage questions to settle before an industrial AI pilot.",
    G2_EN, "Law 25 and AI for Quebec manufacturers", "Plan how information is handled before you automate incoming requests.", kind="guide")
add("loi25-ia.html", "fr", "law25-ai.html",
    "Loi 25 et IA industrielle au Québec | BAS Digital Solutions",
    "Loi 25 et automatisation des demandes de prix : renseignements personnels, accès et stockage à régler avant un projet pilote en IA.".replace(" :", NB + ":"),
    G2_FR, "Loi 25 et IA pour les manufacturiers du Québec", "Planifiez le traitement de l'information avant d'automatiser la réception des demandes.", kind="guide")

add("quebec-en.html", "en", "quebec.html",
    "RFQ Automation in Montreal and Quebec | BAS Digital Solutions",
    "RFQ automation for Montreal and Quebec manufacturers, with a free audit, a focused pilot and human approval before any quote is sent.",
    section("Your RFQ, with a clear next step", steps("en") + trust("en")) + pilot("en"),
    "Industrial RFQ automation for Montreal and Quebec.",
    "For Quebec manufacturers, machine shops and industrial suppliers. Start in English or French with a free audit, then a pilot with an agreed scope.",
    hero_extra=CTA["en"], kind="guide")
add("quebec.html", "fr", "quebec-en.html",
    "Automatisation industrielle à Montréal et au Québec | BAS Digital Solutions",
    "Automatisation des demandes de prix pour les manufacturiers de Montréal et du Québec : audit gratuit, projet pilote ciblé et approbation humaine.".replace(" :", NB + ":"),
    section("Votre demande de prix, avec une prochaine étape claire", steps("fr") + trust("fr")) + pilot("fr"),
    "Automatisation industrielle des demandes de prix à Montréal et au Québec.",
    "Pour les manufacturiers, ateliers d'usinage et fournisseurs industriels du Québec. Commencez en français ou en anglais par un audit gratuit, puis un projet pilote à portée convenue.",
    hero_extra=CTA["fr"], kind="guide")

# ---------- Checklists ----------
CHECK_EN = ["Choose one recurring request type", "Identify intake emails and forms", "List part, quantity and material requirements",
            "Define the authoritative drawing and revision", "Capture the requested delivery date", "Plan for incomplete requests and duplicates",
            "Name the reviewer and approver", "Identify tools: ERP, Outlook, Teams or CRM", "Check access, storage and retention",
            "Prepare redacted sample requests", "Agree on scope, price and acceptance criteria"]
CHECK_FR = ["Choisir un type de demande récurrent", "Repérer les courriels et formulaires de réception", "Lister les exigences de pièce, de quantité et de matériau",
            "Définir le dessin et la révision qui font foi", "Recueillir la date de livraison demandée", "Prévoir les demandes incomplètes et les doublons",
            "Nommer le réviseur et l'approbateur", f"Repérer les outils{NB}: ERP, Outlook, Teams ou CRM", "Vérifier les accès, le stockage et la conservation",
            "Préparer des exemples de demandes caviardés", "Convenir de la portée, du prix et des critères d'acceptation"]


def checklist_body(items, lang):
    lis = "".join(f'<li><label><input type="checkbox"> {x}</label></li>' for x in items)
    pdf = "rfq-checklist-en.pdf" if lang == "en" else "rfq-checklist-fr.pdf"
    lab = "Download the PDF" if lang == "en" else "Télécharger le PDF"
    return f'<section><div class="wrap narrow"><ul class="check">{lis}</ul><p><a class="btn" href="{pdf}">{lab}</a></p></div></section>'


add("rfq-checklist-en.html", "en", "rfq-checklist-fr.html", "RFQ Readiness Checklist | BAS Digital Solutions",
    "An 11-point checklist to prepare one RFQ workflow for automation: fields, exceptions, reviewers, tools and data handling.",
    checklist_body(CHECK_EN, "en"), "RFQ readiness checklist", "A starting point for your free 30-minute call.", kind="guide")
add("rfq-checklist-fr.html", "fr", "rfq-checklist-en.html", "Liste de préparation aux demandes de prix | BAS Digital Solutions",
    f"Une liste en 11 points pour préparer un processus de demandes de prix à l'automatisation{NB}: champs, exceptions, réviseurs, outils et données.",
    checklist_body(CHECK_FR, "fr"), "Liste de préparation aux demandes de prix", "Un point de départ pour votre appel gratuit de 30 minutes.", kind="guide")

# ---------- Privacy ----------
PRIV_EN = """<section><div class="wrap narrow prose">
<p class="note">Last updated: October 20, 2026</p>
<h2>Person responsible for personal information</h2>
<p>Bandar Sharkh, Founder, BAS Digital Solutions. Contact: <a href="mailto:info@basdigitalsolutions.ca">info@basdigitalsolutions.ca</a>.</p>
<h2>What we collect</h2>
<p>When you submit the inquiry form or email us, we collect your name, contact details, company and the project description you provide. Do not send passwords, payment details or confidential drawings through the public form.</p>
<h2>Why we use it</h2>
<p>To review and answer your request, discuss fit and scope, and send a proposal. We do not sell personal information.</p>
<h2>Service providers and storage</h2>
<p>We use these providers: Tally for the inquiry form (Tally reports storage in Europe); Web Hosting Canada for our email (Canada); GitHub Pages to host this website (United States), which keeps basic technical logs such as IP addresses for security; and Google tools to keep track of inquiries (data may be stored in the United States or elsewhere). Your information may therefore be stored outside Quebec.</p>
<h2>Retention</h2>
<p>We keep inquiry information for 24 months after our last contact with you, unless you become a client or a longer period is agreed for an active project. We then delete or anonymize it.</p>
<h2>Your rights</h2>
<p>You may ask to access or correct your information, ask that it be deleted, or withdraw your consent, by emailing <a href="mailto:info@basdigitalsolutions.ca">info@basdigitalsolutions.ca</a>. You may also contact the <a href="https://www.cai.gouv.qc.ca/" rel="noopener">Commission d'accès à l'information</a>.</p>
<h2>Cookies and analytics</h2>
<p>This website does not use analytics or advertising cookies. The embedded Tally form may set its own cookies when you use it.</p>
<h2>Project data</h2>
<p>Before you share drawings or other project data, we agree in writing on who may access it, which providers are used, where it is stored and how long it is kept.</p>
</div></section>"""
PRIV_FR = f"""<section><div class="wrap narrow prose">
<p class="note">Dernière mise à jour{NB}: 20 octobre 2026</p>
<h2>Personne responsable de la protection des renseignements personnels</h2>
<p>Bandar Sharkh, fondateur, BAS Digital Solutions. Contact{NB}: <a href="mailto:info@basdigitalsolutions.ca">info@basdigitalsolutions.ca</a>.</p>
<h2>Renseignements recueillis</h2>
<p>Lorsque vous remplissez le formulaire ou nous écrivez, nous recueillons votre nom, vos coordonnées, votre entreprise et la description de projet que vous fournissez. N'envoyez pas de mots de passe, de renseignements de paiement ni de dessins confidentiels par le formulaire public.</p>
<h2>Utilisation</h2>
<p>Pour examiner votre demande et y répondre, discuter de la pertinence et de la portée, et vous envoyer une proposition. Nous ne vendons pas de renseignements personnels.</p>
<h2>Fournisseurs et stockage</h2>
<p>Nous faisons appel aux fournisseurs suivants{NB}: Tally pour le formulaire (Tally indique un stockage en Europe); Hébergement Web Canada pour notre courriel (Canada); GitHub Pages pour l'hébergement de ce site (États-Unis), qui conserve des journaux techniques de base, comme les adresses IP, à des fins de sécurité; et des outils Google pour le suivi des demandes (les données peuvent être stockées aux États-Unis ou ailleurs). Vos renseignements peuvent donc être stockés à l'extérieur du Québec.</p>
<h2>Conservation</h2>
<p>Nous conservons les renseignements des demandes pendant 24 mois après notre dernier contact avec vous, sauf si vous devenez client ou si une durée plus longue est convenue pour un projet actif. Nous les détruisons ou les anonymisons ensuite.</p>
<h2>Vos droits</h2>
<p>Vous pouvez demander l'accès à vos renseignements, leur rectification ou leur suppression, ou retirer votre consentement, en écrivant à <a href="mailto:info@basdigitalsolutions.ca">info@basdigitalsolutions.ca</a>. Vous pouvez aussi communiquer avec la <a href="https://www.cai.gouv.qc.ca/" rel="noopener">Commission d'accès à l'information</a>.</p>
<h2>Témoins et analytique</h2>
<p>Ce site n'utilise aucun témoin d'analytique ni de publicité. Le formulaire Tally intégré peut déposer ses propres témoins lorsque vous l'utilisez.</p>
<h2>Données de projet</h2>
<p>Avant que vous partagiez des dessins ou d'autres données de projet, nous convenons par écrit des personnes autorisées, des fournisseurs, du lieu de stockage et de la durée de conservation.</p>
</div></section>"""
add("privacy.html", "en", "confidentialite.html", "Privacy Policy | BAS Digital Solutions",
    "How BAS Digital Solutions collects, uses, stores and protects personal information under Quebec's Law 25.",
    PRIV_EN, "Privacy policy", "How we handle personal information.", contact=False, kind="guide")
add("confidentialite.html", "fr", "privacy.html", "Politique de confidentialité | BAS Digital Solutions",
    "Comment BAS Digital Solutions recueille, utilise, stocke et protège les renseignements personnels en vertu de la Loi 25.",
    PRIV_FR, "Politique de confidentialité", "Comment nous traitons les renseignements personnels.", contact=False, kind="guide")

# ---------- 404 ----------
add("404.html", "en", None, "Page not found | BAS Digital Solutions", "This page does not exist.",
    '<section><div class="wrap narrow"><p><a class="btn" href="/">Go to the homepage</a> <a class="btn alt" href="/fr.html" lang="fr">Aller à l\'accueil</a></p></div></section>',
    "Page not found", "The page you are looking for has moved or does not exist. / Cette page n'existe pas.", contact=False, kind="guide")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    here = os.path.dirname(os.path.abspath(__file__))
    for f in ["styles.css", "site.js", "favicon.svg", "bas-logo.svg"]:
        shutil.copy(os.path.join(here, "assets", f), os.path.join(OUT, f))
    for a, k in PAGES:
        slug = a[0]
        html = page(*a, **k)
        if slug == "404.html":
            html = html.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
        with open(os.path.join(OUT, slug), "w", encoding="utf-8") as fh:
            fh.write(html)
    # sitemap
    urls = []
    for a, k in PAGES:
        slug, lang, alt = a[0], a[1], a[2]
        if slug == "404.html":
            continue
        loc = f"{SITE}/" if slug == "index.html" else f"{SITE}/{slug}"
        alts = ""
        if alt:
            altloc = f"{SITE}/" if alt == "index.html" else f"{SITE}/{alt}"
            en, fr = (loc, altloc) if lang == "en" else (altloc, loc)
            alts = (f'\n    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>'
                    f'\n    <xhtml:link rel="alternate" hreflang="fr" href="{fr}"/>')
        urls.append(f"  <url>\n    <loc>{loc}</loc>{alts}\n  </url>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                 + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        fh.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    with open(os.path.join(OUT, "CNAME"), "w") as fh:
        fh.write("basdigitalsolutions.ca\n")
    print(f"Built {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    main()
