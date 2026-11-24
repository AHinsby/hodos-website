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
    ("Læringsvejen", "/saadan-fungerer-det/"),
    ("Forløb", "/kurser/"),
    ("Om HODOS", "/om-hodos/"),
]

COURSES = {
    "familie-survival-1": {
        "title": "Familie Survival 1 — Bål, lejr og retning",
        "audience": "For familier · Niveau 1",
        "summary": "Et praktisk friluftsforløb, hvor familien lærer at tænde bål, lave enkel mad, bygge en lejrbase og finde vej sammen.",
        "experience": "For begyndere og nysgerrige familier",
        "intro": "I arbejder med de færdigheder, der gør en dag eller aften ude mere overskuelig: varme, mad, læ, retning og samarbejde. Kurset foregår i naturen og tager udgangspunkt i enkle opgaver, som børn og voksne løser sammen.",
        "outcomes": ["vælge og indrette en enkel lejrbase", "tænde og slukke bål på egnede bålpladser", "lave et enkelt måltid over bål", "finde vej på en kort rute med kort og kompas"],
        "for_whom": "Familier, der vil have et roligt og praktisk udgangspunkt for mere friluftsliv sammen.",
    },
    "familie-survival-2": {
        "title": "Familie Survival 2 — Vejr, mørke og plan B",
        "audience": "For familier · Niveau 2",
        "summary": "For familier, der vil være mere sikre, når vejret skifter, lyset forsvinder, eller den oprindelige plan må ændres.",
        "experience": "For familier med lyst til at bygge videre",
        "intro": "Her bruger familien sine grundfærdigheder i mere skiftende forhold. I arbejder med læ, lys, rutevalg, varme og fælles beslutninger, når der opstår et behov for en plan B.",
        "outcomes": ["vurdere lejrplads, vind og læ", "bruge lys og varme med omtanke", "tilpasse rute og tidspunkt, når forholdene ændrer sig", "fordele roller og holde overblik som familie"],
        "for_whom": "Familier, der vil øve sig i at tage rolige, praktiske beslutninger ude.",
    },
    "familie-survival-3": {
        "title": "Familie Survival 3 — 24 timer ude",
        "audience": "For familier · Niveau 3",
        "summary": "En samlet friluftsoplevelse, hvor familien planlægger, laver lejr, navigerer og bruger sine færdigheder over et døgn i naturen.",
        "experience": "For familier, der vil samle færdighederne i praksis",
        "intro": "Familien gennemfører en overskuelig tur med tid til at planlægge, etablere en lejr, lave mad og bruge kortet undervejs. Fokus er på fælles ansvar, ro og erfaringer, I kan tage med på egne ture.",
        "outcomes": ["pakke og planlægge en enkel tur sammen", "lave lejr og måltider ude", "finde vej på en overskuelig rute", "evaluere turen og bruge erfaringerne næste gang"],
        "for_whom": "Familier, der ønsker en større fælles outdoor-oplevelse.",
    },
    "outdoor-survival-1": {
        "title": "Outdoor Survival 1 — Bål, lejr og navigation",
        "audience": "For voksne · Niveau 1",
        "summary": "Et begyndervenligt outdoor-forløb om bål, lejr, enkel mad, kort, kompas og plan B på egne eventyr.",
        "experience": "Ingen tidligere erfaring nødvendig",
        "intro": "Du bygger et praktisk fundament til ture i naturen. Vi arbejder med enkle, brugbare færdigheder og gode beslutninger, så du kan blive mere selvstændig, når ruten, vejret eller tiden ændrer sig.",
        "outcomes": ["etablere en enkel lejrbase", "lave enkel mad over bål", "bruge kort og kompas til rutevalg", "lave en realistisk plan B for en tur"],
        "for_whom": "Voksne, der vil opbygge konkrete outdoor-færdigheder i et begyndervenligt tempo.",
    },
    "outdoor-survival-2": {
        "title": "Outdoor Survival 2 — Mørke, kulde og fokus",
        "audience": "For voksne · Niveau 2",
        "summary": "Et outdoor-forløb for voksne, der vil bevare overblik og træffe gode valg, når kulde, mørke eller koldt vand ændrer situationen.",
        "experience": "For voksne, der vil bygge videre på grundfærdighederne",
        "intro": "I arbejder med varme, læ, lys, tempo og opmærksomhed i mere krævende forhold. I øver en rolig, praktisk håndtering af at blive våd og kold: komme ud af kulden, skifte til tørt, begrænse yderligere varmetab og træffe den rigtige beslutning i tide.",
        "outcomes": ["vurdere kulde, vind, mørke og vand i forhold til turens plan", "etablere læ, tørre lag og varme efter at være blevet våd", "prioritere energi, pauser og udstyr", "genkende faresignaler og søge hjælp, når situationen kræver det"],
        "for_whom": "Voksne, der vil have mere ro og handlekraft på ture i køligere, mørkere eller mere skiftende forhold.",
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
    <nav id="site-navigation" class="site-nav" aria-label="Hovednavigation">{links}<a class="button button-small" href="{prefix}kurser/">Se forløb</a></nav>
  </div>
</header>'''


def footer(slug: str) -> str:
    prefix = asset_prefix(slug)
    return f'''<footer class="site-footer">
  <div class="shell footer-grid">
    <div><a class="wordmark" href="{prefix}">{SITE_NAME}</a><p>Praktiske færdigheder. Sikkerhed. Eventyr.</p></div>
    <div><h2>Find vej</h2><a href="{prefix}familier/">For familier</a><a href="{prefix}voksne/">For voksne</a><a href="{prefix}kurser/">Forløb</a></div>
    <div><h2>Praktisk</h2><a href="{prefix}saadan-fungerer-det/">Læringsvejen</a><a href="{prefix}praktisk/">Praktisk</a></div>
  </div>
  <div class="shell footer-note">HODOS — praktiske færdigheder til et liv mere ude.</div>
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
    secondary_html = "" if not secondary else f'<a class="text-link hero-secondary" href="{secondary[1]}">{secondary[0]} <span aria-hidden="true">→</span></a>'
    prefix = asset_prefix(slug)
    width, height = IMAGE_DIMENSIONS[image]
    return f'''<section class="hero hero-home">
  <div class="shell hero-grid">
    <div class="hero-copy"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="hero-lead">{intro}</p><div class="hero-actions"><a class="button" href="{primary[1]}">{primary[0]} <span aria-hidden="true">→</span></a>{secondary_html}</div><p class="hero-note">Bål · Lejr · Mad · Navigation · Plan B</p></div>
    <figure class="hero-media hero-media--portrait"><img src="{prefix}assets/images/{image}" alt="{image_alt}" width="{width}" height="{height}" fetchpriority="high"></figure>
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
    body = hero("home", "Friluftsliv · Sikkerhed · Eventyr", "Fra første skridt til egne eventyr.", "HODOS lærer familier og voksne bål, lejr, mad og navigation — færdigheder, der giver mere frihed i naturen og mere ro, når strøm, GPS eller den oprindelige plan ikke er nok.", ("Se forløb", "kurser/"), "family-explorer-path.webp", "Kort og kompas i forgrunden, mens en familie bevæger sig gennem et nordisk skovlandskab", ("Vælg familie eller voksen", "#veje-ind"))
    body += '''<section id="veje-ind" class="section home-section audience-section"><div class="shell"><div class="section-heading section-heading--split"><div><p class="eyebrow">Vælg dit udgangspunkt</p><h2>Samme metode. To forskellige veje ind.</h2></div><p>HODOS starter der, hvor I er. Vælg den vej, der passer til jeres hverdag, erfaring og mål.</p></div><div class="audience-grid"><article class="audience-card audience-card--family"><p class="card-kicker">For familier</p><h3>Lær sammen — og brug det sammen.</h3><p>Familie Survival samler bål, lejr, mad, navigation og plan B i en tydelig progression, hvor børn og voksne deltager aktivt.</p><ul><li>Bål, lejr og mad ude</li><li>Kort, kompas og retning</li><li>Fælles ansvar og gode beslutninger</li></ul><a class="text-link" href="familier/">Se familieforløbet <span aria-hidden="true">→</span></a></article><article class="audience-card audience-card--adult"><p class="card-kicker">For voksne</p><h3>Bliv mere selvstændig på tur.</h3><p>Et praktisk fundament i navigation, turplanlægning og gode beslutninger, når forholdene ændrer sig.</p><ul><li>Begyndervenligt tempo</li><li>Navigation og plan B</li><li>Fokus på egne ture og mål</li></ul><a class="text-link" href="voksne/">Se forløb for voksne <span aria-hidden="true">→</span></a></article></div></div></section>
<section class="section section-tint home-section journey-section"><div class="shell"><div class="section-heading"><p class="eyebrow">HODOS’ læringsvej</p><h2>Et fundament, du kan bygge videre på.</h2><p>Progression er en mulighed — ikke et krav. Du kan tage ét kursus, fordybe dig i en færdighed eller bygge videre, når det giver mening.</p></div><ol class="signature-journey"><li><span class="journey-number">01</span><p class="step-label">Explorer</p><h3>Start med det, der gør en forskel.</h3><p>Forberedelse, udstyr, navigation og konkrete valg i overskuelige rammer.</p></li><li><span class="journey-number">02</span><p class="step-label">Færdigheder</p><h3>Øv det, du vil kunne mere af.</h3><p>Fordyb dig i navigation, turplanlægning eller andre praktiske moduler, når de er klar.</p></li><li><span class="journey-number">03</span><p class="step-label">Egne eventyr</p><h3>Brug det, når det tæller.</h3><p>Planlæg og gennemfør ture, der passer til din erfaring, dine rammer og situationen.</p></li></ol><a class="text-link section-link" href="saadan-fungerer-det/">Se hele læringsvejen <span aria-hidden="true">→</span></a></div></section>
<section class="section home-section method-section"><div class="shell method-grid"><div class="method-intro"><p class="eyebrow">HODOS-metoden</p><h2>Planlæg. Vurder. Tilpas.</h2><p>Godt friluftsliv handler ikke om at presse planen igennem. Det handler om at kunne læse situationen og vælge klogt undervejs.</p><a class="text-link" href="om-hodos/">Læs om HODOS <span aria-hidden="true">→</span></a></div><ol class="principle-list"><li><span>01</span><div><h3>Planlæg</h3><p>Gør turen overskuelig med en enkel rute, det rigtige udstyr og en plan B.</p></div></li><li><span>02</span><div><h3>Vurder</h3><p>Se på vejr, terræn, energi og den gruppe, du er en del af.</p></div></li><li><span>03</span><div><h3>Tilpas</h3><p>Vælg en ny vej, kortere rute eller pause, når det er den gode beslutning.</p></div></li></ol></div></section>
<section class="section home-cta"><div class="shell home-cta-grid"><div><p class="eyebrow">Næste skridt</p><h2>Find den vej, der passer til dig.</h2><p>Se HODOS’ forløb og begynd med de færdigheder, I vil bruge først.</p></div><div class="home-cta-actions"><a class="button button-light" href="kurser/">Se forløb <span aria-hidden="true">→</span></a><a class="text-link text-link--light" href="saadan-fungerer-det/">Sådan fungerer HODOS <span aria-hidden="true">→</span></a></div></div></section>'''
    return layout("home", "Fra første skridt til egne eventyr", "Outdoor survival og friluftslivskurser med bål, lejr, mad og navigation for familier og voksne.", body)


def families() -> str:
    body = page_intro("For familier", "Byg en familie, der kan mere sammen.", "HODOS’ familieforløb giver børn og voksne fælles færdigheder i naturen. I begynder roligt, bygger videre i et tydeligt Explorer-forløb og vælger selv, hvilke færdigheder der giver mening bagefter.")
    body += '''<section class="section family-hero-panel"><div class="shell family-feature-grid"><div><p class="eyebrow">Forløbet i én sætning</p><h2>Start sammen. Øv jer. Brug det på jeres egne ture.</h2><p>Familier skal ikke vælge mellem hygge og læring. På HODOS løser I konkrete opgaver sammen: I finder vej, pakker til tur, vurderer forhold og taler om gode beslutninger, når planen ændrer sig.</p><p>Explorer 1, 2 og 3 er et sammenhængende fundament. Skill-kurser og ekspeditionsture er næste muligheder – ikke noget, alle skal igennem.</p></div>''' + visual("familier", "family-explorer-path.webp", "Kort og kompas på et bord ved en skovsti, mens en familie går i baggrunden", "family-feature-image") + '''</div></section>
<section class="section section-tint"><div class="shell"><div class="section-heading"><p class="eyebrow">Explorer-forløbet</p><h2>Tre trin, der gør familien mere selvstændig.</h2><p>Hvert trin bygger på det forrige. I kan stoppe efter et trin eller fortsætte, når det passer til jeres erfaring, lyst og de konkrete rammer.</p></div><ol class="family-journey"><li><span class="journey-number">01</span><p class="step-label">Explorer 1</p><h3>Kom godt i gang</h3><p>Et fælles udgangspunkt med enkle opgaver, grundlæggende forberedelse og trygge rammer for at være på tur sammen.</p></li><li><span class="journey-number">02</span><p class="step-label">Explorer 2</p><h3>Byg færdigheder</h3><p>Familien øver sig mere målrettet og tager gradvist mere ansvar for navigation, udstyr og beslutninger undervejs.</p></li><li><span class="journey-number">03</span><p class="step-label">Explorer 3</p><h3>Sæt det sammen</h3><p>Færdighederne bruges i en større helhed, hvor familien planlægger, samarbejder og reflekterer over egne valg.</p></li></ol></div></section>
<section class="section"><div class="shell"><div class="section-heading"><p class="eyebrow">Efter Explorer</p><h2>Vælg den vej, der passer til familien.</h2><p>Explorer-forløbet er fundamentet. Herfra kan I fordybe jer i én færdighed eller på sigt bruge erfaringen på en større tur.</p></div><div class="card-grid two"><article class="content-card visual-card">''' + visual("familier", "skills-map-compass-card.webp", "Kort og kompas på et træbord ved en skovsti", "card-image") + '''<p class="card-kicker">Skill-kurser</p><h2>Fordyb jer i én færdighed</h2><p>Korte, målrettede kurser kan bygge videre på Explorer-forløbet eller tages, når familien har et konkret behov. Hvert forløb giver familien konkrete færdigheder, I kan bygge videre på.</p><a class="text-link" href="../kurser/">Se alle forløb <span aria-hidden="true">→</span></a></article><article class="content-card visual-card">''' + visual("familier", "expedition-map-reading.webp", "Vandrer studerer et kort ved en rolig kyststi", "card-image") + '''<p class="card-kicker">Ekspeditionsture</p><h2>Brug færdighederne i en større sammenhæng</h2><p>Ekspeditionsture er ikke en automatisk belønning eller et fast slutmål. De samler færdighederne i en større fælles outdoor-oplevelse.</p><a class="text-link" href="../saadan-fungerer-det/">Læs om læringsvejen <span aria-hidden="true">→</span></a></article></div></div></section>
<section class="section"><div class="shell"><div class="section-heading"><p class="eyebrow">Familie Survival</p><h2>Tre niveauer. Ét fælles mål.</h2><p>Lær bål, lejr, mad og navigation sammen — og byg videre i jeres eget tempo.</p></div><div class="card-grid two">''' + card("Familien finder vej", COURSES["familie-survival-1"]["summary"], "../kurser/familie-survival-1/", "Se forløbet") + card("Tryg på tur med børn", COURSES["familie-survival-2"]["summary"], "../kurser/familie-survival-2/", "Se forløbet") + '''</div></div></section>
<section class="section section-dark"><div class="shell cta-block"><p class="eyebrow">Praktisk</p><h2>Familiekurser er fælles aktiviteter.</h2><p>Begynderforløb er ikke generelle børnepasningstilbud. Børn og voksne deltager sammen og løser praktiske opgaver som familie.</p><a class="button button-light" href="../praktisk/">Læs praktisk information <span aria-hidden="true">→</span></a></div></section>'''
    return layout("familier", "For familier", "Explorer 1, 2 og 3 samt færdighedskurser og ekspeditionsture for familier.", body)


def adults() -> str:
    body = page_intro("For voksne", "Gør dig klar til dit næste eventyr.", "Du behøver ikke være erfaren friluftsentusiast for at begynde. Lær navigation, turplanlægning og sikkerhed – eller brug færdighederne som fundament for et konkret mål.")
    body += '''<section class="section"><div class="shell card-grid two"><article class="content-card"><p class="card-kicker">Jeg er ny</p><h2>Kom godt i gang</h2><p>Start med kort, kompas, rutevalg og en enkel turplan. Byg grundfærdighederne, før du gør planen større.</p><a class="text-link" href="../kurser/outdoor-survival-1/">Se navigation og turplanlægning <span aria-hidden="true">→</span></a></article><article class="content-card"><p class="card-kicker">Jeg har et mål</p><h2>Forbered dig bedre</h2><p>Et større mål kan begynde med samme grundlag: dømmekraft, realistisk planlægning og praktiske færdigheder, der passer til turen.</p><a class="text-link" href="../saadan-fungerer-det/">Læs om læringsvejen <span aria-hidden="true">→</span></a></article></div></section>
<section class="section section-tint"><div class="shell split"><div><p class="eyebrow">Når planen ændrer sig</p><h2>En god beslutning er ikke altid at fortsætte.</h2></div><div><p>HODOS fokuserer på at kunne læse terræn og forhold, planlægge en alternativ rute og ændre beslutning i tide. Det er forberedelse – ikke en garanti for en bestemt præstation eller gennemførelse.</p><a class="text-link" href="../om-hodos/">Læs om vores tilgang <span aria-hidden="true">→</span></a></div></div></section>
<section class="section"><div class="shell"><div class="section-heading"><p class="eyebrow">Outdoor Survival</p><h2>Byg videre, når forholdene kræver mere.</h2><p>Vælg et niveau, der passer til din erfaring og den type ture, du vil kunne gennemføre.</p></div><div class="card-grid two">''' + card("Outdoor Survival 1 — Bål, lejr og navigation", COURSES["outdoor-survival-1"]["summary"], "../kurser/outdoor-survival-1/", "Se forløbet") + card("Outdoor Survival 2 — Mørke, kulde og fokus", COURSES["outdoor-survival-2"]["summary"], "../kurser/outdoor-survival-2/", "Se forløbet") + '''</div></div></section>'''
    return layout("voksne", "For voksne", "Praktiske færdigheder i navigation og turplanlægning for voksne begyndere og eventyrere.", body)


def method() -> str:
    body = page_intro("Se læringsvejen", "Først lærer du. Så øver du. Til sidst gør du det selv.", "HODOS kombinerer korte forklaringer med praktiske opgaver, så færdighederne kan bruges på dine egne ture.")
    body += '''<section class="section"><div class="shell"><ol class="progression detailed"><li><span>01</span><div><p class="step-label">Explorer</p><h2>Skab et fælles fundament</h2><p>Du lærer principperne og prøver dem i overskuelige opgaver. For familier kan det være at orientere et kort sammen. For voksne kan det være at planlægge en kort rute med et alternativ.</p></div></li><li><span>02</span><div><p class="step-label">Færdigheder</p><h2>Gør øvelsen mere målrettet</h2><p>Du vælger de områder, som giver mest mening for dig: navigation, turplanlægning eller andre praktiske færdigheder, når de er klar til at blive tilbudt.</p></div></li><li><span>03</span><div><p class="step-label">Ekspedition</p><h2>Brug det i en større sammenhæng</h2><p>Større ture er ikke et automatisk næste trin. De kræver passende forberedelse, konkrete rammer og en vurdering af situationen.</p></div></li></ol></div></section>
<section class="image-break"><div class="shell">''' + visual("saadan-fungerer-det", "method-rain-map-wide.webp", "Kort, kompas og blyant på et bord i en regnvåd skov", "wide-image") + '''</div></section>
<section class="section section-tint"><div class="shell split"><div><p class="eyebrow">Læring med omtanke</p><h2>Praktiske valg frem for præstation.</h2></div><div><p>Vi øver det, der hjælper, når noget uventet sker: at læse situationen, tale om muligheder og vælge en ny plan. Det kan være lige så relevant at afbryde som at fortsætte.</p><p>Du kan altid tage et enkelt kursus. Progressionen er et tilbud, ikke en adgangsbillet.</p></div></div></section>'''
    return layout("saadan-fungerer-det", "Se læringsvejen", "HODOS’ læringsvej: Explorer, færdigheder og ekspedition.", body)


def courses() -> str:
    cards = "".join(f'''<article class="course-card" data-audience="{"familier" if "familier" in data["audience"].lower() else "voksne"}"><p class="card-kicker">{data["audience"]}</p><h2>{data["title"]}</h2><p>{data["summary"]}</p><dl><div><dt>Erfaring</dt><dd>{data["experience"]}</dd></div></dl><a class="text-link" href="{slug}/">Se forløbet <span aria-hidden="true">→</span></a></article>''' for slug, data in COURSES.items())
    body = page_intro("Forløb", "Praktiske færdigheder til et liv mere ude.", "HODOS’ forløb samler bål, lejr, mad, navigation og plan B i konkrete outdoor-oplevelser for familier og voksne.")
    body += f'''<section class="section"><div class="shell"><div class="filter-bar" aria-label="Filtrér kurser"><button class="filter-button is-active" type="button" data-filter="alle" aria-pressed="true">Alle</button><button class="filter-button" type="button" data-filter="familier" aria-pressed="false">For familier</button><button class="filter-button" type="button" data-filter="voksne" aria-pressed="false">For voksne</button></div><div class="course-grid" data-course-grid>{cards}</div><p class="filter-empty" data-filter-empty hidden>Der er ingen forløb i denne kategori.</p></div></section>
<section class="section section-tint"><div class="shell narrow"><p class="eyebrow">Ærlig status</p><h2>Færdigheder, I kan tage med jer.</h2><p>Hvert forløb handler om at gøre noget konkret: finde vej, skabe varme, lave mad, bygge lejr og vælge en god vej videre.</p></div></section>'''
    return layout("kurser", "Kurser", "Forløb i friluftsliv, navigation og turplanlægning for familier og voksne.", body)


def course_page(slug: str, data: dict) -> str:
    body = page_intro(data["audience"], data["title"], data["summary"])
    outcomes = "".join(f"<li>{item}</li>" for item in data["outcomes"])
    body += f'''<section class="section"><div class="shell course-layout"><article><h2>Om forløbet</h2><p>{data["intro"]}</p><h2>Det lærer I</h2><ul class="check-list">{outcomes}</ul><h2>Hvem er det for?</h2><p>{data["for_whom"]}</p></article><aside class="course-facts"><dl><div><dt>Spor</dt><dd>{data["audience"]}</dd></div><div><dt>Erfaring</dt><dd>{data["experience"]}</dd></div><div><dt>Fokus</dt><dd>Praktiske færdigheder ude</dd></div></dl></aside></div></section>
<section class="section section-tint"><div class="shell narrow"><p class="eyebrow">Næste skridt</p><h2>Byg videre i dit eget tempo.</h2><p>Start med det, du vil kunne nu, og brug erfaringerne på jeres egne ture.</p><div class="hero-actions"><a class="button" href="../">Se alle forløb <span aria-hidden="true">→</span></a><a class="text-link" href="../../saadan-fungerer-det/">Se læringsvejen <span aria-hidden="true">→</span></a></div></div></section>'''
    return layout(f"kurser/{slug}", data["title"], data["summary"], body)


def about() -> str:
    body = page_intro("Om HODOS", "Faglighed, der kan bruges i virkeligheden.", "HODOS kombinerer friluftsliv og praktisk undervisning med fokus på sikkerhed, ansvar og gode beslutninger.")
    body += '''<section class="image-break"><div class="shell">''' + visual("om-hodos", "about-navigation-still-life.webp", "Kort og kompas ved en skovsti", "wide-image") + '''</div></section>
<section class="section"><div class="shell split"><div><p class="eyebrow">Vores formål</p><h2>Fra tilskuer til mere selvstændig.</h2></div><div><p>Naturen er et læringsrum. HODOS er ikke bygget som passiv underholdning eller som en samling opmøde-badges. Målet er, at deltagere kan bruge det, de lærer, på egne ture.</p><p>Undervisningen er civil, jordnær og tilrettelagt, så flere kan være med. Vi arbejder med praktiske opgaver i kontrollerede rammer og med refleksion bagefter.</p></div></div></section>
<section class="section section-tint"><div class="shell card-grid three"><article class="content-card"><h2>Praktiske færdigheder</h2><p>Du øver dig i virkeligheden og ikke kun i teorien.</p></article><article class="content-card"><h2>God dømmekraft</h2><p>Du lærer at vurdere muligheder, usikkerhed og grænser.</p></article><article class="content-card"><h2>Større selvstændighed</h2><p>Målet er, at du kan planlægge og gennemføre egne eventyr.</p></article></div></section>
<section class="section"><div class="shell narrow"><p class="eyebrow">Status</p><h2>Et projekt under opbygning.</h2><p>HODOS er for mennesker, der vil lære bål, lejr, mad og navigation gennem praktiske opgaver ude i naturen.</p></div></section>'''
    return layout("om-hodos", "Om HODOS", "Om HODOS’ formål, metode og tilgang til læring i naturen.", body)


def practical() -> str:
    faq = [("Kan man være nybegynder?", "Ja. HODOS-forløbene starter med grundfærdigheder og et tempo, hvor alle kan være med."), ("Hvad med vejr og aflysning?", "I lærer at planlægge, vurdere forholdene og vælge en god plan B på turen."), ("Hvad skal man have med?", "Du får en konkret pakkeliste, så udstyret passer til aktiviteten og årstiden."), ("Kan børn deltage uden voksne?", "Begynderforløb for familier er fælles aktiviteter med deltagende forældre eller værger. Det er ikke et børnepasningstilbud."), ("Er der booking eller betaling?", "HODOS’ forløb handler om praktisk læring ude — bål, lejr, mad, navigation og plan B.")]
    faq_html = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faq)
    body = page_intro("Praktisk", "Det skal være let at vide, hvad du går ind til.", "Her finder du svar på de vigtigste spørgsmål om HODOS’ outdoor-forløb.")
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
}
for slug, data in COURSES.items():
    PAGES[f"kurser/{slug}/index.html"] = course_page(slug, data)

for relative, html in PAGES.items():
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")

print(f"Generated {len(PAGES)} HTML pages.")
