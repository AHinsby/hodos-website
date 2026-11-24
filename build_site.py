#!/usr/bin/env python3
"""Generate the static HODOS MVP website from one reviewed source file."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
SITE_NAME = "HODOS"  # Keep the working name centralised for a future rename.
IMAGE_DIMENSIONS = {
    "home-family-trail.webp": (1536, 1024),
    "family-explorer-path.webp": (960, 1200),
    "skills-map-compass-card.webp": (960, 640),
    "expedition-map-reading.webp": (1536, 1024),
    "about-navigation-still-life.webp": (1536, 1024),
    "method-rain-map-wide.webp": (1448, 966),
}

NAV = [
    ("For familier", "/familier/"),
    ("For voksne", "/voksne/"),
    ("Kurser", "/kurser/"),
    ("Sådan fungerer det", "/saadan-fungerer-det/"),
    ("Om HODOS", "/om-hodos/"),
]

COURSES = {
    "familien-finder-vej": {
        "title": "Familien finder vej",
        "audience": "For familier · Explorer",
        "summary": "En introduktion til kort, kompas og fælles rutevalg for familier, der vil lære at finde vej sammen.",
        "status": "Pilot under afprøvning",
        "duration": "Varighed afklares",
        "experience": "Ingen erfaring nødvendig",
        "intro": "Kurset er tænkt som en rolig, praktisk introduktion til navigation. Børn og voksne løser små opgaver sammen og bruger kortet til at tale om retning, rute og valg undervejs.",
        "outcomes": ["finde de vigtigste tegn på et kort", "bruge verdenshjørner og kompas i en enkel øvelse", "vælge en kort rute sammen", "tale om, hvornår planen skal ændres"],
        "for_whom": "Familier med deltagende forældre eller værger. Aldersramme, holdstørrelse og praktiske forhold fastlægges før et åbent hold.",
    },
    "tryg-paa-tur-med-boern": {
        "title": "Tryg på tur med børn",
        "audience": "For familier · Explorer",
        "summary": "Praktiske valg om påklædning, udstyr, vejr og en enkel plan, der gør familiens næste tur lettere at overskue.",
        "status": "Pilot under afprøvning",
        "duration": "Varighed afklares",
        "experience": "Ingen erfaring nødvendig",
        "intro": "Et familieforløb om de små beslutninger før og under en tur: hvad der er godt at have med, hvordan I reagerer på kulde eller regn, og hvordan I sætter en enkel ramme, som alle kan være trygge i.",
        "outcomes": ["pakke til en kort tur med børn", "vurdere vejr og påklædning", "lave en enkel kontakt- og alternativplan", "bruge stop/go-beslutninger i familien"],
        "for_whom": "Familier med deltagende forældre eller værger. Det er ikke et børnepasningstilbud og indeholder ikke formel førstehjælpscertificering.",
    },
    "navigation-og-turplanlaegning": {
        "title": "Navigation og turplanlægning",
        "audience": "For voksne · Explorer",
        "summary": "Et begyndervenligt forløb om kort, kompas, rutevalg og en plan B, når forholdene ændrer sig.",
        "status": "Pilot under afprøvning",
        "duration": "Varighed afklares",
        "experience": "Ingen erfaring nødvendig",
        "intro": "For voksne, der gerne vil begynde med friluftsliv eller blive mere selvstændige på deres egne ture. Fokus er praktiske valg: at læse terrænet, planlægge en overskuelig rute og holde fast i en god beslutning, også når den er at vende om.",
        "outcomes": ["læse centrale informationer på et kort", "bruge kompas som støtte til rutevalg", "lave en enkel plan og alternativplan", "vurdere, hvornår en rute bør ændres"],
        "for_whom": "Voksne begyndere. Sted, holdstørrelse og øvrige praktiske rammer offentliggøres kun, når de er fastlagt.",
    },
}


def page_path(slug: str) -> str:
    return "/" if slug == "home" else f"/{slug}/"


def asset_prefix(slug: str) -> str:
    if slug == "home":
        return ""
    return "../" * (slug.count("/") + 1)


def header(slug: str) -> str:
    links = "".join(
        f'<a class="nav-link {"is-active" if href == page_path(slug) else ""}" href="{asset_prefix(slug)}{href.lstrip("/")}">{label}</a>'
        for label, href in NAV
    )
    prefix = asset_prefix(slug)
    return f'''<a class="skip-link" href="#indhold">Spring til indhold</a>
<header class="site-header">
  <div class="shell header-inner">
    <a class="wordmark" href="{prefix}" aria-label="{SITE_NAME} forside">{SITE_NAME}</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-navigation">Menu<span class="menu-icon" aria-hidden="true"></span></button>
    <nav id="site-navigation" class="site-nav" aria-label="Hovednavigation">{links}<a class="button button-small" href="{prefix}kurser/">Se kurser</a></nav>
  </div>
</header>'''


def footer(slug: str) -> str:
    prefix = asset_prefix(slug)
    return f'''<footer class="site-footer">
  <div class="shell footer-grid">
    <div><a class="wordmark" href="{prefix}">{SITE_NAME}</a><p>Praktiske færdigheder. Sikkerhed. Eventyr.</p></div>
    <div><h2>Find vej</h2><a href="{prefix}familier/">For familier</a><a href="{prefix}voksne/">For voksne</a><a href="{prefix}kurser/">Kurser</a></div>
    <div><h2>Praktisk</h2><a href="{prefix}saadan-fungerer-det/">Sådan fungerer det</a><a href="{prefix}praktisk/">Praktisk</a><a href="{prefix}kontakt/">Kontakt</a></div>
  </div>
  <div class="shell footer-note">HODOS er et arbejdsnavn. Kurser offentliggøres først med bekræftede praktiske rammer.</div>
</footer>'''


def layout(slug: str, title: str, description: str, body: str) -> str:
    prefix = asset_prefix(slug)
    canonical = page_path(slug)
    return f'''<!doctype html>
<html lang="da">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description)}">
  <meta name="theme-color" content="#1b3025">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="{prefix}assets/site.css">
  <script defer src="{prefix}assets/site.js"></script>
  <title>{escape(title)} | {SITE_NAME}</title>
</head>
<body>
{header(slug)}
<main id="indhold">{body}</main>
{footer(slug)}
</body>
</html>'''


def hero(slug: str, eyebrow: str, title: str, intro: str, primary: tuple[str, str], image: str, image_alt: str, secondary: tuple[str, str] | None = None) -> str:
    secondary_html = "" if not secondary else f'<a class="text-link" href="{secondary[1]}">{secondary[0]} <span aria-hidden="true">→</span></a>'
    prefix = asset_prefix(slug)
    return f'''<section class="hero">
  <div class="shell hero-grid">
    <div class="hero-copy"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="hero-lead">{intro}</p><div class="hero-actions"><a class="button" href="{primary[1]}">{primary[0]} <span aria-hidden="true">→</span></a>{secondary_html}</div></div>
    <figure class="hero-media"><img src="{prefix}assets/images/{image}" alt="{image_alt}" width="1536" height="1024" fetchpriority="high"></figure>
  </div>
</section>'''


def visual(slug: str, image: str, alt: str, class_name: str = "content-image") -> str:
    prefix = asset_prefix(slug)
    width, height = IMAGE_DIMENSIONS[image]
    return f'<figure class="{class_name}"><img src="{prefix}assets/images/{image}" alt="{alt}" width="{width}" height="{height}" loading="lazy" decoding="async"></figure>'


def card(title: str, text: str, href: str, label: str = "Læs mere", status: str | None = None) -> str:
    status_html = "" if status is None else f'<p class="status-badge">{status}</p>'
    return f'<article class="content-card"><h3>{title}</h3>{status_html}<p>{text}</p><a class="text-link" href="{href}">{label} <span aria-hidden="true">→</span></a></article>'


def page_intro(eyebrow: str, title: str, intro: str) -> str:
    return f'<section class="page-intro"><div class="shell narrow"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="hero-lead">{intro}</p></div></section>'


def home() -> str:
    body = hero("home", "Friluftsliv · Sikkerhed · Eventyr", "Fra første skridt til egne eventyr.", "HODOS er en færdigheds- og eventyrskole for familier og voksne. Vi lærer praktiske færdigheder, så du kan færdes tryggere, træffe bedre beslutninger og gennemføre dine egne eventyr.", ("Se kurser", "kurser/"), "home-family-trail.webp", "Familie går sammen på en rolig skovsti ved åbent landskab", ("Sådan fungerer det", "saadan-fungerer-det/"))
    body += '''<section class="section"><div class="shell"><div class="section-heading"><p class="eyebrow">To veje ind</p><h2>Én fælles idé: at kunne mere selv.</h2><p>Du behøver ikke erfaring for at begynde. Du behøver lysten til at lære, øve dig og tage gode valg sammen med andre.</p></div><div class="card-grid two">'''
    body += card("For familier", "Lær at finde vej, pakke til tur og løse små opgaver sammen. Børn og voksne deltager i fælles læring – med ansvar, der passer til situationen.", "familier/", "Se forløb for familier")
    body += card("For voksne", "Kom godt i gang med navigation og turplanlægning, eller byg et praktisk fundament for en større personlig udfordring.", "voksne/", "Se forløb for voksne")
    body += '''</div></div></section>
<section class="section section-tint"><div class="shell"><div class="section-heading"><p class="eyebrow">Vores læringsvej</p><h2>Ét fundament. Flere veje. Egne eventyr.</h2><p>Progression er en mulighed, ikke et krav. Du kan tage ét kursus eller bygge videre, når det giver mening.</p></div><ol class="progression"><li><span>01</span><div><p class="step-label">Explorer</p><h3>Find dit fundament</h3><p>Kom godt i gang med sikkerhed, udstyr, navigation og praktiske valg på tur.</p></div></li><li><span>02</span><div><p class="step-label">Færdigheder</p><h3>Øv det, du vil blive bedre til</h3><p>Fokuser på eksempelvis navigation, turplanlægning eller andre relevante moduler.</p></div></li><li><span>03</span><div><p class="step-label">Ekspedition</p><h3>Brug færdighederne selv</h3><p>Større ture bliver først relevante, når forberedelse og rammer passer til opgaven.</p></div></li></ol><a class="text-link" href="saadan-fungerer-det/">Læs om metoden <span aria-hidden="true">→</span></a></div></section>
<section class="section"><div class="shell split"><div><p class="eyebrow">Faglighed i praksis</p><h2>Vi øver det, der betyder noget, når planen ændrer sig.</h2></div><div><p>At færdes godt handler ikke om at tage størst mulig risiko. Det handler om at være forberedt, læse situationen og kunne vælge en ny vej, når det er det rigtige.</p><p>HODOS bruger praktiske opgaver, refleksion og overskuelige scenarier, så læringen kan bruges efter kurset.</p><a class="text-link" href="om-hodos/">Om HODOS <span aria-hidden="true">→</span></a></div></div></section>
<section class="section section-dark"><div class="shell cta-block"><p class="eyebrow">Næste skridt</p><h2>Find det næste, du gerne vil kunne.</h2><p>Se de kursusidéer, der er under afprøvning. Der vises ikke datoer, priser eller tilmelding, før rammerne er på plads.</p><a class="button button-light" href="kurser/">Se kurser <span aria-hidden="true">→</span></a></div></section>'''
    return layout("home", "Fra første skridt til egne eventyr", "Praktiske kurser i friluftsliv, sikkerhed og navigation for familier og voksne.", body)


def families() -> str:
    body = page_intro("For familier", "Byg en familie, der kan mere sammen.", "HODOS’ familieforløb giver børn og voksne fælles færdigheder i naturen. I begynder roligt, bygger videre i et tydeligt Explorer-forløb og vælger selv, hvilke færdigheder der giver mening bagefter.")
    body += '''<section class="section family-hero-panel"><div class="shell family-feature-grid"><div><p class="eyebrow">Forløbet i én sætning</p><h2>Start sammen. Øv jer. Brug det på jeres egne ture.</h2><p>Familier skal ikke vælge mellem hygge og læring. På HODOS løser I konkrete opgaver sammen: I finder vej, pakker til tur, vurderer forhold og taler om gode beslutninger, når planen ændrer sig.</p><p>Explorer 1, 2 og 3 er et sammenhængende fundament. Skill-kurser og ekspeditionsture er næste muligheder – ikke noget, alle skal igennem.</p></div>''' + visual("familier", "family-explorer-path.webp", "Kort og kompas på et bord ved en skovsti, mens en familie går i baggrunden", "family-feature-image") + '''</div></section>
<section class="section section-tint"><div class="shell"><div class="section-heading"><p class="eyebrow">Explorer-forløbet</p><h2>Tre trin, der gør familien mere selvstændig.</h2><p>Hvert trin bygger på det forrige. I kan stoppe efter et trin eller fortsætte, når det passer til jeres erfaring, lyst og de konkrete rammer.</p></div><ol class="family-journey"><li><span class="journey-number">01</span><p class="step-label">Explorer 1</p><h3>Kom godt i gang</h3><p>Et fælles udgangspunkt med enkle opgaver, grundlæggende forberedelse og trygge rammer for at være på tur sammen.</p></li><li><span class="journey-number">02</span><p class="step-label">Explorer 2</p><h3>Byg færdigheder</h3><p>Familien øver sig mere målrettet og tager gradvist mere ansvar for navigation, udstyr og beslutninger undervejs.</p></li><li><span class="journey-number">03</span><p class="step-label">Explorer 3</p><h3>Sæt det sammen</h3><p>Færdighederne bruges i en større helhed, hvor familien planlægger, samarbejder og reflekterer over egne valg.</p></li></ol></div></section>
<section class="section"><div class="shell"><div class="section-heading"><p class="eyebrow">Efter Explorer</p><h2>Vælg den vej, der passer til familien.</h2><p>Explorer-forløbet er fundamentet. Herfra kan I fordybe jer i én færdighed eller på sigt bruge erfaringen på en større tur.</p></div><div class="card-grid two"><article class="content-card visual-card">''' + visual("familier", "skills-map-compass-card.webp", "Kort og kompas på et træbord ved en skovsti", "card-image") + '''<p class="card-kicker">Skill-kurser</p><h2>Fordyb jer i én færdighed</h2><p>Korte, målrettede kurser kan bygge videre på Explorer-forløbet eller tages, når familien har et konkret behov. Aktuelle temaer offentliggøres kun, når indhold, instruktør og praktiske rammer er klar.</p><a class="text-link" href="../kurser/">Se aktuelle kursusidéer <span aria-hidden="true">→</span></a></article><article class="content-card visual-card">''' + visual("familier", "expedition-map-reading.webp", "Vandrer studerer et kort ved en rolig kyststi", "card-image") + '''<p class="card-kicker">Ekspeditionsture</p><h2>Brug færdighederne i en større sammenhæng</h2><p>Ekspeditionsture er ikke en automatisk belønning eller et fast slutmål. De bliver først relevante, når forberedelse, familieerfaring og konkrete sikkerhedsrammer passer til turen.</p><a class="text-link" href="../saadan-fungerer-det/">Læs om læringsvejen <span aria-hidden="true">→</span></a></article></div></div></section>
<section class="section"><div class="shell"><div class="section-heading"><p class="eyebrow">Pilotforløb</p><h2>To kursusidéer under afprøvning.</h2><p>De er ikke åbne for booking. Praktiske rammer offentliggøres først, når de er fastlagt.</p></div><div class="card-grid two">''' + card("Familien finder vej", COURSES["familien-finder-vej"]["summary"], "../kurser/familien-finder-vej/", "Se kursusidéen", COURSES["familien-finder-vej"]["status"]) + card("Tryg på tur med børn", COURSES["tryg-paa-tur-med-boern"]["summary"], "../kurser/tryg-paa-tur-med-boern/", "Se kursusidéen", COURSES["tryg-paa-tur-med-boern"]["status"]) + '''</div></div></section>
<section class="section section-dark"><div class="shell cta-block"><p class="eyebrow">Praktisk</p><h2>Familiekurser er fælles aktiviteter.</h2><p>Begynderforløb er ikke generelle børnepasningstilbud. Aldersrammer, voksenledsagelse og øvrige forhold beskrives på det enkelte kursus, når de er bekræftet.</p><a class="button button-light" href="../praktisk/">Læs praktisk information <span aria-hidden="true">→</span></a></div></section>'''
    return layout("familier", "For familier", "Explorer 1, 2 og 3 samt færdighedskurser og ekspeditionsture for familier.", body)


def adults() -> str:
    body = page_intro("For voksne", "Gør dig klar til dit næste eventyr.", "Du behøver ikke være erfaren friluftsentusiast for at begynde. Lær navigation, turplanlægning og sikkerhed – eller brug færdighederne som fundament for et konkret mål.")
    body += '''<section class="section"><div class="shell card-grid two"><article class="content-card"><p class="card-kicker">Jeg er ny</p><h2>Kom godt i gang</h2><p>Start med kort, kompas, rutevalg og en enkel turplan. Byg grundfærdighederne, før du gør planen større.</p><a class="text-link" href="../kurser/navigation-og-turplanlaegning/">Se navigation og turplanlægning <span aria-hidden="true">→</span></a></article><article class="content-card"><p class="card-kicker">Jeg har et mål</p><h2>Forbered dig bedre</h2><p>Et større mål kan begynde med samme grundlag: dømmekraft, realistisk planlægning og praktiske færdigheder, der passer til turen.</p><a class="text-link" href="../saadan-fungerer-det/">Læs om læringsvejen <span aria-hidden="true">→</span></a></article></div></section>
<section class="section section-tint"><div class="shell split"><div><p class="eyebrow">Når planen ændrer sig</p><h2>En god beslutning er ikke altid at fortsætte.</h2></div><div><p>HODOS fokuserer på at kunne læse terræn og forhold, planlægge en alternativ rute og ændre beslutning i tide. Det er forberedelse – ikke en garanti for en bestemt præstation eller gennemførelse.</p><a class="text-link" href="../om-hodos/">Læs om vores tilgang <span aria-hidden="true">→</span></a></div></div></section>
<section class="section"><div class="shell"><div class="section-heading"><p class="eyebrow">Pilotforløb</p><h2>Navigation og turplanlægning.</h2><p>En kursusidé for voksne begyndere. Den er under afprøvning og ikke åben for booking.</p></div><div class="card-grid one">''' + card("Navigation og turplanlægning", COURSES["navigation-og-turplanlaegning"]["summary"], "../kurser/navigation-og-turplanlaegning/", "Se kursusidéen", COURSES["navigation-og-turplanlaegning"]["status"]) + '''</div></div></section>'''
    return layout("voksne", "For voksne", "Praktiske færdigheder i navigation og turplanlægning for voksne begyndere og eventyrere.", body)


def method() -> str:
    body = page_intro("Sådan fungerer det", "Først lærer du. Så øver du. Til sidst gør du det selv.", "HODOS kombinerer korte forklaringer med praktiske opgaver, så færdighederne kan bruges på dine egne ture.")
    body += '''<section class="section"><div class="shell"><ol class="progression detailed"><li><span>01</span><div><p class="step-label">Explorer</p><h2>Skab et fælles fundament</h2><p>Du lærer principperne og prøver dem i overskuelige opgaver. For familier kan det være at orientere et kort sammen. For voksne kan det være at planlægge en kort rute med et alternativ.</p></div></li><li><span>02</span><div><p class="step-label">Færdigheder</p><h2>Gør øvelsen mere målrettet</h2><p>Du vælger de områder, som giver mest mening for dig: navigation, turplanlægning eller andre praktiske færdigheder, når de er klar til at blive tilbudt.</p></div></li><li><span>03</span><div><p class="step-label">Ekspedition</p><h2>Brug det i en større sammenhæng</h2><p>Større ture er ikke et automatisk næste trin. De kræver passende forberedelse, konkrete rammer og en vurdering af situationen.</p></div></li></ol></div></section>
<section class="image-break"><div class="shell">''' + visual("saadan-fungerer-det", "method-rain-map-wide.webp", "Kort, kompas og blyant på et bord i en regnvåd skov", "wide-image") + '''</div></section>
<section class="section section-tint"><div class="shell split"><div><p class="eyebrow">Læring med omtanke</p><h2>Praktiske valg frem for præstation.</h2></div><div><p>Vi øver det, der hjælper, når noget uventet sker: at læse situationen, tale om muligheder og vælge en ny plan. Det kan være lige så relevant at afbryde som at fortsætte.</p><p>Du kan altid tage et enkelt kursus. Progressionen er et tilbud, ikke en adgangsbillet.</p></div></div></section>'''
    return layout("saadan-fungerer-det", "Sådan fungerer det", "HODOS’ læringsvej: Explorer, færdigheder og ekspedition.", body)


def courses() -> str:
    cards = "".join(f'''<article class="course-card" data-audience="{"familier" if "familier" in data["audience"].lower() else "voksne"}"><p class="card-kicker">{data["audience"]}</p><h2>{data["title"]}</h2><p>{data["summary"]}</p><dl><div><dt>Status</dt><dd>{data["status"]}</dd></div><div><dt>Erfaring</dt><dd>{data["experience"]}</dd></div></dl><a class="text-link" href="{slug}/">Se kursusidéen <span aria-hidden="true">→</span></a></article>''' for slug, data in COURSES.items())
    body = page_intro("Kurser", "Find dit næste skridt.", "Her er de kursusidéer, der aktuelt er under afprøvning. Der er ingen booking, datoer eller priser, før de faktiske rammer er på plads.")
    body += f'''<section class="section"><div class="shell"><div class="filter-bar" aria-label="Filtrér kurser"><button class="filter-button is-active" type="button" data-filter="alle" aria-pressed="true">Alle</button><button class="filter-button" type="button" data-filter="familier" aria-pressed="false">For familier</button><button class="filter-button" type="button" data-filter="voksne" aria-pressed="false">For voksne</button></div><div class="course-grid" data-course-grid>{cards}</div><p class="filter-empty" data-filter-empty hidden>Der er ingen kurser i denne kategori endnu.</p></div></section>
<section class="section section-tint"><div class="shell narrow"><p class="eyebrow">Ærlig status</p><h2>Et kursus er først åbent, når rammerne er klare.</h2><p>Et åbent kursus skal have fastlagt sted, dato, pris, antal pladser, undervisning og en reel mulighed for tilmelding. Indtil da beskriver vi kun kursusidéer og deres aktuelle status.</p></div></section>'''
    return layout("kurser", "Kurser", "Kursusidéer i friluftsliv, navigation og turplanlægning for familier og voksne.", body)


def course_page(slug: str, data: dict) -> str:
    body = page_intro(data["audience"], data["title"], data["summary"])
    outcomes = "".join(f"<li>{item}</li>" for item in data["outcomes"])
    body += f'''<section class="section"><div class="shell course-layout"><article><h2>Om kursusidéen</h2><p>{data["intro"]}</p><h2>Det kan deltagerne øve</h2><ul class="check-list">{outcomes}</ul><h2>Hvem er det for?</h2><p>{data["for_whom"]}</p></article><aside class="course-facts"><p class="status-badge">{data["status"]}</p><dl><div><dt>Spor</dt><dd>{data["audience"]}</dd></div><div><dt>Varighed</dt><dd>{data["duration"]}</dd></div><div><dt>Erfaring</dt><dd>{data["experience"]}</dd></div><div><dt>Dato og pris</dt><dd>Offentliggøres kun, når de er bekræftet.</dd></div><div><dt>Tilmelding</dt><dd>Ikke åben endnu.</dd></div></dl></aside></div></section>
<section class="section section-tint"><div class="shell narrow"><p class="eyebrow">Næste skridt</p><h2>Praktiske rammer kommer først.</h2><p>HODOS offentliggør kun dato, sted, pris og tilmelding, når de nødvendige forhold er afklaret. Indtil da kan du se de øvrige kursusidéer og læse om metoden.</p><div class="hero-actions"><a class="button" href="../">Se alle kurser <span aria-hidden="true">→</span></a><a class="text-link" href="../../saadan-fungerer-det/">Sådan fungerer det <span aria-hidden="true">→</span></a></div></div></section>'''
    return layout(f"kurser/{slug}", data["title"], data["summary"], body)


def about() -> str:
    body = page_intro("Om HODOS", "Faglighed, der kan bruges i virkeligheden.", "HODOS kombinerer friluftsliv og praktisk undervisning med fokus på sikkerhed, ansvar og gode beslutninger.")
    body += '''<section class="image-break"><div class="shell">''' + visual("om-hodos", "about-navigation-still-life.webp", "Kort og kompas ved en skovsti", "wide-image") + '''</div></section>
<section class="section"><div class="shell split"><div><p class="eyebrow">Vores formål</p><h2>Fra tilskuer til mere selvstændig.</h2></div><div><p>Naturen er et læringsrum. HODOS er ikke bygget som passiv underholdning eller som en samling opmøde-badges. Målet er, at deltagere kan bruge det, de lærer, på egne ture.</p><p>Undervisningen er civil, jordnær og tilrettelagt, så flere kan være med. Vi arbejder med praktiske opgaver i kontrollerede rammer og med refleksion bagefter.</p></div></div></section>
<section class="section section-tint"><div class="shell card-grid three"><article class="content-card"><h2>Praktiske færdigheder</h2><p>Du øver dig i virkeligheden og ikke kun i teorien.</p></article><article class="content-card"><h2>God dømmekraft</h2><p>Du lærer at vurdere muligheder, usikkerhed og grænser.</p></article><article class="content-card"><h2>Større selvstændighed</h2><p>Målet er, at du kan planlægge og gennemføre egne eventyr.</p></article></div></section>
<section class="section"><div class="shell narrow"><p class="eyebrow">Status</p><h2>Et projekt under opbygning.</h2><p>HODOS er fortsat et arbejdsnavn. Kursusudbud, instruktørroller, konkrete rammer og eventuelle kvalifikationer beskrives først offentligt, når de kan verificeres.</p></div></section>'''
    return layout("om-hodos", "Om HODOS", "Om HODOS’ formål, metode og tilgang til læring i naturen.", body)


def practical() -> str:
    faq = [("Kan man være nybegynder?", "Ja. De første kursusidéer er bygget til begyndere. Forudsætninger beskrives tydeligt på hvert kursus, når det åbner."), ("Hvad med vejr og aflysning?", "Praktiske rammer, vejrpolitik og eventuelle aflysningsvilkår offentliggøres sammen med et konkret åbent kursus."), ("Hvad skal man have med?", "En konkret medbringeliste kommer med det enkelte kursus. HODOS vil holde den enkel og relevant for aktiviteten."), ("Kan børn deltage uden voksne?", "Begynderforløb for familier er fælles aktiviteter med deltagende forældre eller værger. Det er ikke et børnepasningstilbud."), ("Er der booking eller betaling?", "Ikke endnu. HODOS viser først tilmelding eller betaling, når kursus, kapacitet, betingelser og praktiske forhold er klar.")]
    faq_html = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faq)
    body = page_intro("Praktisk", "Det skal være let at vide, hvad du går ind til.", "Her samler vi de praktiske spørgsmål, der skal være afklaret, når et kursus åbner.")
    body += f'<section class="section"><div class="shell narrow"><div class="faq">{faq_html}</div></div></section>'
    return layout("praktisk", "Praktisk", "Praktiske spørgsmål om HODOS’ kurser for familier og voksne.", body)


def contact() -> str:
    body = page_intro("Kontakt", "Har du spørgsmål – eller vil du samle din egen gruppe?", "HODOS’ kontaktvej er under etablering. Vi offentliggør først en formular eller e-mailadresse, når modtagelse, databehandling og svarproces er testet.")
    body += '''<section class="section"><div class="shell narrow notice"><h2>Kontaktmulighed kommer, når den virker.</h2><p>En offentlig kontaktformular skal kunne modtage henvendelser sikkert, vise en korrekt bekræftelse og have en tydelig databeskyttelsesramme. Derfor vises den ikke som aktiv endnu.</p><p>Indtil da kan du læse om kursusidéerne, metoden og de praktiske principper.</p><div class="hero-actions"><a class="button" href="../kurser/">Se kurser <span aria-hidden="true">→</span></a><a class="text-link" href="../praktisk/">Læs praktisk information <span aria-hidden="true">→</span></a></div></div></section>'''
    return layout("kontakt", "Kontakt", "Kontakt og praktiske henvendelser til HODOS.", body)


PAGES = {
    "index.html": home(),
    "familier/index.html": families(),
    "voksne/index.html": adults(),
    "saadan-fungerer-det/index.html": method(),
    "kurser/index.html": courses(),
    "om-hodos/index.html": about(),
    "praktisk/index.html": practical(),
    "kontakt/index.html": contact(),
}
for slug, data in COURSES.items():
    PAGES[f"kurser/{slug}/index.html"] = course_page(slug, data)

for relative, html in PAGES.items():
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")

print(f"Generated {len(PAGES)} HTML pages.")
