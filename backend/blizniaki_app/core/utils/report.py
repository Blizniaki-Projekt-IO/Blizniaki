import os
import uuid

import fitz
import plotly.graph_objects as go

from blizniaki_app.settings import MEDIA_ROOT

CONTENT = {
    "kot": "Koty to nie tylko mistrzowie elegancji, ale także mają w sobie niezaprzeczalną tajemniczość i "
           "niezależność. Podobnie jak te zwierzęta, cechuje Cię delikatna finezja w działaniu, a także zdolność do "
           "wyczucia subtelnych niuansów w otaczającym Cię świecie. Twoja intuicja jest Twoim sprzymierzeńcem, "
           "a chwilami potrafisz być niezwykle towarzyski, choć czasami wolisz schować się w cichym zakątku, "
           "by cieszyć się samotnością.",
    "pies": "Towarzyski duch towarzyszy Ci zawsze. Cechuje Cię lojalność i gotowość do niesienia pomocy innym, "
            "a Twoja radość z życia jest zaraźliwa. Jesteś wierny przyjaciel, gotów na każdą przygodę, a jednocześnie "
            "potrafisz dostosować się do różnych sytuacji. Twoja otwartość na nowe relacje sprawia, "
            "że łatwo nawiązujesz przyjaźnie, a Twoja energiczna natura sprawia, że jesteś sercem każdej grupy.",
    "lis": "Jesteś jak lis - zwinny, inteligentny i pełen sprytu. Twoja zdolność adaptacji sprawia, że potrafisz "
           "radzić sobie w różnych sytuacjach, a Twoja charyzma przyciąga uwagę innych. Lis to także symbol dowcipu i "
           "zdolności rozwiązania problemów, co sprawia, że jesteś doskonałym strategiem. Twoje umiejętności "
           "spostrzegawcze pozwalają Ci dostrzegać niuanse, które inni mogą przeoczyć. Twoja elastyczność umysłowa "
           "czyni Cię doskonałym towarzyszem w każdej sytuacji.",
    "niedzwiedz": "Jesteś jak niedźwiedź - silny, niezależny i pełen siły. Twoja determinacja i zdolność do "
                  "koncentracji pozwalają Ci osiągać cele, które sobie stawiasz. Podobnie jak niedźwiedzie, "
                  "potrafisz być czuły i opiekuńczy, szczególnie wobec tych, których kochasz. Twój spokojny "
                  "temperament sprawia, że jesteś stabilnym punktem wsparcia dla innych, a jednocześnie potrafisz "
                  "cieszyć się chwilami beztroski i radości, podobnie jak te majestatyczne istoty w swoim naturalnym "
                  "środowisku.",
    "surykatka": "Tak jak te ciekawskie stworzenia, "
                 "jesteś niezwykle spostrzegawczy i zawsze gotów na przygodę. Twoja społeczna natura sprawia, "
                 "że świetnie funkcjonujesz w grupie, a także masz zdolność do dzielenia się informacjami i "
                 "współpracy z innymi. Surykatki są mistrzami komunikacji, a Ty, podobnie jak one, potrafisz "
                 "dostosować się do zmieniających się sytuacji, utrzymując przy tym pozytywne podejście do życia.",
}


def create_report(scores: dict):
    scores_sorted = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    animals = list(scores_sorted.keys())
    values = list(scores_sorted.values())
    fig = go.Figure(go.Bar(
        x=values,
        y=animals,
        text=[str(x) + "%" for x in values],
        orientation='h',
        textposition='inside',
        insidetextanchor="middle",
        insidetextfont=dict(
            size=16,
        ),
        marker=dict(
            color=[12, 24, 48, 64, 128],
            colorscale='haline'
        )
    ))
    fig.update_yaxes(ticksuffix="   ")
    fig.update_xaxes(visible=False)
    fig.update_layout({
        "plot_bgcolor": "rgba(255, 255, 255, 255)",
    })
    report_id = uuid.uuid4()
    path = os.path.join(MEDIA_ROOT, f'reports/output_{report_id}.png')
    fig.write_image(path)

    HTML = f"""
    <html>
    <head>
    <title>Raport zwierzęcia - bliżniaki</title>
    </head>
    <body>
    <h1 style="font-weight: bold; font-size: 24px; margin-bottom: 16px;">Jakim zwierzęciem jesteś?</h1>
    <p>Czy kiedykolwiek zastanawiałeś się, jakie zwierzę idealnie odzwierciedla Twoją osobowość? Teraz masz okazję to sprawdzić! Nasza aplikacja skrupulatnie przeanalizowała Twoje zdjęcie, by dopasować Cię do pięciu fascynujących przedstawicieli zwierzęcego świata. Wyniki tej analizy, która pozwoli Ci poznać, z jakimi zwierzętami dzielisz najwięcej charakterystycznych cech znajdziesz poniżej na wykresie!</p>
    <img src="http://localhost:8000/media/reports/output_{report_id}.png" style="width: 100%; margin-left: 10px;">
    <p>Twoje zwierzę to<span style="font-weight: bold; margin-bottom: 16px; color: red;"> {animals[0]}</span>!</p>
    <p>{CONTENT.get(animals[0])}</p>
    </body>
    </html>
    """

    HTML_PDF = f"""
        <html>
        <head>
        <title>Raport zwierzęcia - bliżniaki</title>
        </head>
        <body>
        <h1 style="font-weight: bold; font-size: 24px; margin-bottom: 16px;">Jakim zwierzęciem jesteś?</h1>
        <p>Czy kiedykolwiek zastanawiałeś się, jakie zwierzę idealnie odzwierciedla Twoją osobowość? Teraz masz okazję to sprawdzić! Nasza aplikacja skrupulatnie przeanalizowała Twoje zdjęcie, by dopasować Cię do pięciu fascynujących przedstawicieli zwierzęcego świata. Wyniki tej analizy, która pozwoli Ci poznać, z jakimi zwierzętami dzielisz najwięcej charakterystycznych cech znajdziesz poniżej na wykresie!</p>
        <img src="output_{report_id}.png" style="width: 100%; margin-left: 10px;">
        <p>Twoje zwierzę to<span style="font-weight: bold; margin-bottom: 16px; color: red;"> {animals[0]}</span>!</p>
        <p>{CONTENT.get(animals[0])}</p>
        </body>
        </html>
        """

    MEDIABOX = fitz.paper_rect("letter")
    WHERE = MEDIABOX + (36, 36, -36, -36)
    filename = f'reports/raport_{report_id}.pdf'
    filename_html = filename.replace("pdf", "html")
    with open(os.path.join(MEDIA_ROOT, filename_html), "w") as f:
        f.write(HTML)
    story = fitz.Story(html=HTML_PDF, archive=os.path.join(MEDIA_ROOT, "reports"))
    writer = fitz.DocumentWriter(os.path.join(MEDIA_ROOT, filename))

    more = 1

    while more:
        device = writer.begin_page(MEDIABOX)
        more, _ = story.place(WHERE)
        story.draw(device)
        writer.end_page()

    writer.close()
    return {
        "raport_pdf": filename,
        "raport_html": filename_html,
    }
