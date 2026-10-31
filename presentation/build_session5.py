#!/usr/bin/env python3
"""Generate session-5.html from the ChatGPT production blueprint."""
import re
from pathlib import Path

KIT_ANDROID = "https://www.figma.com/design/8wLehGECxWD4DxvWRcP7Ge/Android-UI-Kit--Community-?node-id=337-23462"
KIT_MIND = "https://www.figma.com/design/f9j5dYKE7QLi5E1NFxeW4I/Meditation-App---UI-Kit--Community-?node-id=57-2065"

def meta(kicker, right):
    return f'<div class="slide-meta"><span>{kicker}</span><span>{right}</span></div>'

def attrs(n, title, act, notes, timer="", learn="", trans="", extra=""):
    bits = [
        f'data-title="{title}"',
        f'data-act="{act}"',
        f'data-slide="{n:02d}"',
        f'data-notes="{notes}"',
    ]
    if timer:
        bits.append(f'data-timer="{timer}"')
    if learn:
        bits.append(f'data-learn="{learn}"')
    if trans:
        bits.append(f'data-transition="{trans}"')
    if extra:
        bits.append(extra)
    return " ".join(bits)

def cover(n, title, act, notes, h1, kicker="SESSION 05", right="", cls="cover title-only", lede=""):
    body = meta(kicker, right or act)
    body += '<div class="grid-lines"></div><div class="cover-content">'
    body += f"<h1>{h1}</h1>"
    if lede:
        body += f'<p class="lede">{lede}</p>'
    body += "</div>"
    return f'<section class="slide {cls} is-active" {attrs(n, title, act, notes)}>{body}</section>' if n == 1 else f'<section class="slide {cls}" {attrs(n, title, act, notes)}>{body}</section>'

def lime(n, title, act, notes, h2, lede="", timer="", kicker="", right="", trans="", learn=""):
    body = meta(kicker or act.split("·")[0].strip(), right or "")
    body += '<div class="approach-intro-content">'
    body += f"<h2>{h2}</h2>"
    if lede:
        body += f'<p class="approach-intro-lede">{lede}</p>'
    body += "</div>"
    return f'<section class="slide approach-intro" {attrs(n, title, act, notes, timer, learn, trans)}>{body}</section>'

LEVELS = ("Playground", "UI Universe", "Thinkers", "Builders", "Evolution")

def level(n, title, act, notes, stage, world, lede, timer="", right=""):
    body = meta(f"LEVEL {stage:02d}", right or "UNLOCKED")
    body += '<div class="approach-intro-content level-unlock">'
    body += f'<p class="level-stage" aria-hidden="true">{stage:02d}</p>'
    body += '<p class="level-stamp">Unlocked</p>'
    body += f"<h2>{world}</h2>"
    if lede:
        body += f'<p class="approach-intro-lede">{lede}</p>'
    body += '<ol class="level-track" aria-label="Five levels">'
    for i, name in enumerate(LEVELS, 1):
        cls = "is-now" if i == stage else ("is-cleared" if i < stage else "")
        body += f'<li class="{cls}"><b>{i:02d}</b><span>{name}</span></li>'
    body += "</ol></div>"
    return f'<section class="slide approach-intro" {attrs(n, title, act, notes, timer)}>{body}</section>'

def studio(n, title, act, notes, h2, p, time_label, timer, kicker="NOW"):
    body = meta(kicker, time_label.upper())
    num, unit = time_label.split(" ", 1) if " " in time_label else (time_label, "")
    body += f'<div class="time-box" aria-hidden="true"><strong>{num}</strong><span>{unit}</span></div>'
    body += f"<div><h2>{h2}</h2>"
    if p:
        body += f"<p>{p}</p>"
    body += "</div>"
    return f'<section class="slide studio-make" {attrs(n, title, act, notes, timer)}>{body}</section>'

def lesson(n, title, act, notes, h2, subtitle="", cols=None, rules=None, grades=None, kicker="", right="", timer="", learn=""):
    body = meta(kicker or "LAB", right or "")
    body += '<div class="lp-body"><div class="lp-heading">'
    body += f"<h2>{h2}</h2>"
    if subtitle:
        body += f'<p class="lp-subtitle">{subtitle}</p>'
    body += "</div>"
    if cols:
        ncol = " three" if len(cols) >= 3 else ""
        body += f'<div class="lp-cols{ncol}">'
        for label, items in cols:
            body += f'<div><p class="lp-col-label">{label}</p><ul class="lp-list">'
            for item in items:
                body += f"<li><span>{item}</span></li>"
            body += "</ul></div>"
        body += "</div>"
    if rules:
        body += '<ol class="lp-rules lp-rules-standalone">'
        for i, item in enumerate(rules, 1):
            body += f'<li><span class="lp-rule-num">{i:02d}</span><span>{item}</span></li>'
        body += "</ol>"
    if grades:
        body += '<div class="lp-grading">'
        for pct, label in grades:
            body += f'<div class="lp-grade-item"><p class="lp-grade-pct">{pct}</p><p class="lp-grade-label">{label}</p></div>'
        body += "</div>"
    body += "</div>"
    return f'<section class="slide lesson-plan" {attrs(n, title, act, notes, timer, learn)}>{body}</section>'

def phone(n, title, act, notes, src, cap, h2, extra_html="", better=False, kicker="SEE", timer="", right="", alt=None, wide=False):
    cls = "is-better" if better else ""
    label = cap if alt is None else alt
    cap_html = f"<figcaption>{cap}</figcaption>" if cap else ""
    slide_cls = "phone-see is-pair" if wide else "phone-see"
    body = meta(kicker, right)
    body += f'<figure class="phone-frame {cls}"><img src="{src}" alt="{label}">{cap_html}</figure>'
    body += f'<div class="phone-copy"><h2>{h2}</h2>{extra_html}</div>'
    return f'<section class="slide {slide_cls}" {attrs(n, title, act, notes, timer)}>{body}</section>'

def pair(n, title, act, notes, left, right, kicker="SEE", light=False, extra_cls=""):
    body = meta(kicker, "")
    body += '<div class="pair-row">'
    for src, cap, better in (left, right):
        cls = "is-better" if better else ""
        body += f'<figure class="phone-frame {cls}"><img src="{src}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'
    body += "</div>"
    slide_cls = "phone-pair is-light-cards" if light else "phone-pair"
    if extra_cls:
        slide_cls = f"{slide_cls} {extra_cls}"
    return f'<section class="slide {slide_cls}" {attrs(n, title, act, notes)}>{body}</section>'

def kit_items(items):
    html = '<ul class="lp-list">'
    for item in items:
        html += f"<li><span>{item}</span></li>"
    html += "</ul>"
    return html

def principle(n, i, name, line, bad, good):
    body = meta(f"{i:02d} / 10", "PRINCIPLE")
    body += '<div class="ui-prin-body">'
    body += f'<div class="ui-prin-head"><h2>{name}</h2><p>{line}</p></div>'
    body += '<div class="ui-prin-pair">'
    body += f'<figure class="ui-prin-card is-bad"><div class="ui-prin-phone">{bad}</div><figcaption>Bad</figcaption></figure>'
    body += f'<figure class="ui-prin-card is-good"><div class="ui-prin-phone">{good}</div><figcaption>Good</figcaption></figure>'
    body += "</div></div>"
    return (
        f'<section class="slide ui-prin" {attrs(n, name, "ACT 4 · TEN RULES", "Point at bad. Then good. Carry it into the build.")}>{body}</section>'
    )

def wide(n, title, act, notes, src, cap, kicker="SEE", href="", alt=""):
    body = meta(kicker, "")
    img_alt = alt or re.sub(r"<[^>]+>", "", cap)
    img = f'<img src="{src}" alt="{img_alt}">'
    extra_cls = ""
    if href:
        extra_cls = " kit-file"
        img = (
            f'<a class="kit-file-shot" data-kit-file href="{href}" target="_blank" rel="noopener">'
            f"{img}</a>"
        )
    body += f'<figure class="wide-frame">{img}<figcaption>{cap}</figcaption></figure>'
    if href:
        body += (
            f'<a class="kit-open-file" data-kit-file href="{href}" target="_blank" rel="noopener">'
            f"Open file</a>"
        )
    return f'<section class="slide wide-see{extra_cls}" {attrs(n, title, act, notes)}>{body}</section>'

def quote(n, title, act, notes, text, detail=""):
    body = meta(act, "")
    body += f'<div class="quote-wrap"><blockquote>{text}</blockquote>'
    if detail:
        body += f'<p class="quote-detail">{detail}</p>'
    body += "</div>"
    return f'<section class="slide quote-slide" {attrs(n, title, act, notes)}>{body}</section>'

def ask(n, title, act, notes, question, kicker="ASK", right="", qnum="", src=""):
    extra = " has-phone" if src else ""
    body = meta(kicker, right)
    if src:
        body += f'<figure class="ux-example-shot"><img src="{src}" alt=""></figure>'
    body += '<div class="ux-example-body">'
    if qnum:
        body += f'<p class="rapid-qn">{qnum}</p>'
    body += f'<p class="ux-example-question">{question}</p></div>'
    return f'<section class="slide ux-example ux-example-ask ux-example-question-only{extra}" {attrs(n, title, act, notes)}>{body}</section>'

def answered(n, title, act, notes, question, answer, kicker="ANSWER", right="+5 · +3 · −3", qnum=""):
    body = meta(kicker, right)
    body += '<div class="rapid-answer-body">'
    if qnum:
        body += f'<p class="rapid-qn">{qnum}</p>'
    body += f'<p class="rapid-q">{question}</p>'
    body += f'<p class="rapid-a">{answer}</p>'
    body += "</div>"
    return f'<section class="slide rapid-answer" {attrs(n, title, act, notes)}>{body}</section>'

def desk_wall(n, title, act, notes, items, kicker="BEFORE YOU MOVE", right="A–H"):
    body = meta(kicker, right)
    body += '<div class="desk-wall-grid">'
    for letter, name, task in items:
        body += (
            f"<article><b>{letter}</b><div><strong>{name}</strong>"
            f"<p>{task}</p></div></article>"
        )
    body += "</div>"
    return f'<section class="slide desk-wall" {attrs(n, title, act, notes)}>{body}</section>'

def cards(n, title, act, notes, h2, items, kicker="MAP", cols="four", subtitle="", learn=""):
    grid = {"two": "two", "three": "three", "six": "six", "four": ""}.get(cols, "")
    body = meta(kicker, "")
    body += f'<div class="lp-body"><div class="lp-heading"><h2>{h2}</h2>'
    if subtitle:
        body += f'<p class="lp-subtitle">{subtitle}</p>'
    body += f'</div><div class="s5-grid {grid}">'
    for span, strong, p in items:
        body += f"<article><span>{span}</span><strong>{strong}</strong><p>{p}</p></article>"
    body += "</div></div>"
    return f'<section class="slide lesson-plan" {attrs(n, title, act, notes, learn=learn)}>{body}</section>'

def process(n, title, act, notes, h2, steps, kicker="PROCESS"):
    body = meta(kicker, "")
    body += f'<div class="lp-body"><div class="lp-heading"><h2>{h2}</h2></div><div class="s5-process"><ol>'
    for i, step in enumerate(steps, 1):
        body += f"<li><span>{i:02d}</span><b>{step}</b></li>"
    body += "</ol></div></div>"
    return f'<section class="slide lesson-plan" {attrs(n, title, act, notes)}>{body}</section>'

def choices(buttons):
    html = '<div class="game-choices">'
    for label, right, pts in buttons:
        ans = "right" if right else "wrong"
        html += f'<button type="button" data-answer="{ans}" data-points="{pts}">{label}</button>'
    html += "</div>"
    return html

def reveal(text):
    return f'<p class="reveal-line" data-reveal>{text}</p>'

slides = []

# 01
slides.append(cover(
    1, "The Mindspace Design Lab", "ACT 1 · OPENING",
    "Welcome them. Do not explain the day. Then meet Arya.",
    "The<br>Mindspace<br>Design Lab.",
    right="8 TEAMS · 6 HOURS",
))
# 02
slides.append(lime(
    2, "Hired", "ACT 1 · OPENING",
    "Do not explain the class. Hire them. Arya is waiting. Scoring starts when they sit.",
    "You are on her team now.",
    "She has five minutes. You have until four.",
    kicker="ACT 1", right="00:00–00:15"
))
# 03
slides.append(ask(
    3, "The stakes", "ACT 1 · OPENING",
    "Let the room sit with it. Eight desks only work if she can walk between them.",
    "Eight desks. If she gets lost between them, it is not a product."
))
# 04
slides.append(cards(
    4, "How you score", "ACT 1 · OPENING",
    "These are the ways they earn points. Not job titles. Not learning outcomes.",
    "Points for",
    [
        ("01", "The need", "If you ignore it, the day fails."),
        ("02", "The path", "She can walk it without a tour."),
        ("03", "The piece", "A component with a job."),
        ("04", "The trade-off", "You can defend it out loud."),
        ("05", "The kill", "Version 1 does not survive."),
        ("06", "The seam", "The next desk can take her."),
    ],
    cols="six", kicker="SCORE"
))
# 05
slides.append(lesson(
    5, "Lab laws", "ACT 1 · OPENING",
    "Six laws on the wall. They stay up all day. Not slogans — constraints.",
    "The lab laws.",
    rules=[
        "No screen before the problem.",
        "If you cannot defend it, it does not stay.",
        "Steal from the kit. Do not invent a third look.",
        "Talk to the desk that hands Arya to you.",
        "Name the reason out loud.",
        "Version 1 is the one you will have to kill.",
    ],
    kicker="LAWS", right="ALL DAY"
))
# 06
slides.append(wide(
    6, "Meet the product", "ACT 1 · OPENING",
    "This is the product. Before we begin, we need the people who will use it. Authentic kit cover from the connected Meditation App file.",
    "assets/figma-kits/meditation-thumb-view.png",
    "Connected kit preview · Meditation App UI Kit · Mindspace. Open the live file for real screens."
))
# 07
slides.append(lesson(
    7, "Meet Arya", "ACT 1 · OPENING",
    "Every team designs for the same person. Each desk solves a different moment.",
    "Arya, 30.",
    "Working professional. New to meditation. Busy. Usually 5–15 minutes. Wants less stress, better sleep, a habit that survives a week.",
    cols=[
        ("Arya will", ["Open the app in a corridor.", "Give you minutes, not an hour.", "Quit if the first screen lectures."]),
        ("Arya will not", ["Learn specialist vocabulary to start.", "Fill a novel before Arya tries.", "Forgive streak shame for one missed day."]),
    ],
    kicker="PERSONA", right="ONE USER"
))
# 08
slides.append(cards(
    8, "A day in Arya's life", "ACT 1 · OPENING",
    "When would she actually use Mindspace? What would she expect at each moment? Context matters more than features.",
    "A day in Arya's life.",
    [
        ("7:30 AM", "Rushes to work", "Can the app meet her in five minutes?"),
        ("1:00 PM", "Struggles to focus", "What is the next obvious action?"),
        ("7:00 PM", "Mentally exhausted", "Does the home screen still feel kind?"),
        ("10:30 PM", "Wants to sleep", "Can she find quiet without searching like a librarian?"),
    ],
    kicker="CONTEXT", learn="Context matters more than features."
))
# 09
slides.append(lesson(
    9, "What Arya wants", "ACT 1 · OPENING",
    "Ask the room: if the player is perfect and she still cannot sleep, who failed?",
    "What Arya wants.",
    "She wants to sleep. Feel calmer. Last a week.",
    cols=[
        ("If this is all you ship", ["A player.", "A streak.", "A library.", "A settings page."]),
        ("If she actually stays", ["She sleeps.", "She feels calmer.", "She can focus.", "She comes back tomorrow.", "She can find the reminder."]),
    ],
    kicker="STAKES", right="ASK THE ROOM"
))
# 10
slides.append(lesson(
    10, "Know. Guess. Find out.", "ACT 1 · OPENING",
    "These are preliminary workshop hypotheses, not verified interview findings. A good designer doesn't mistake an assumption for a fact.",
    "Know. Guess. Find out.",
    subtitle="Every line on the brief is a workshop hypothesis until someone tests it.",
    cols=[
        ("What we know", ["Arya is new to meditation.", "She has limited time.", "She wants consistency."]),
        ("What we hypothesise", ["Too much information may overwhelm her.", "Short sessions may suit her.", "Missed days may affect motivation."]),
        ("What we need to explore", ["What is essential at onboarding?", "How does she choose a session?", "How can progress be encouraging?"]),
    ],
    kicker="RESEARCH", right="LITERACY",
    learn="Research literacy: evidence vs assumption."
))
slides.append(lesson(
    78, "The game", "ACT 1 · OPENING",
    "Eight desks. One product. Hands up all day. Five levels. Scoring starts in the playground.",
    "How today runs.",
    cols=[
        ("The game", [
            "Hands up. First hand answers.",
            "Exact 5. Close 3. Wrong −3.",
            "If you cannot defend it, it does not stay.",
        ]),
        ("The teams", [
            "Eight desks. A through H.",
            "One Arya. Eight moments.",
            "If Arya gets lost between desks, it is not a product.",
        ]),
    ],
    kicker="WORKSHOP", right="8 TEAMS · 6 HOURS"
))
# 11
slides.append(process(
    11, "Warm-up", "ACT 1 · OPENING",
    "Do not lecture a process. Tell them the warm-up, then scoring starts.",
    "Warm-up. Then we keep score.",
    ["Frame", "Align", "Reuse", "Adapt", "Name it", "Defend it"],
    kicker="NEXT"
))

# ACT 2
slides.append(level(
    12, "Level 1 unlocked", "ACT 2 · THE PLAYGROUND",
    "Do not say 'get comfortable with Figma.' Give them a screen and a clock.",
    1, "The Playground.",
    "Ten minutes. Recreate one screen. No screenshots.",
    timer="30", right="00:15–00:45"
))
slides.append(phone(
    13, "Recreate this screen", "ACT 2 · THE PLAYGROUND",
    "One simple mobile welcome: heading, supporting text, illustration, primary button, secondary action, carousel indicator. Open Figma and recreate it. Ten minutes.",
    "assets/mindspace/recreate-pair.png",
    "",
    "Recreate this screen.",
    extra_html="<p>Heading. Supporting text. Illustration. Primary button. Secondary action. Carousel indicator. Ten minutes.</p>",
    alt="Two screens: a meditation welcome with Sign Up and Sign In, and a Sign Up form.",
    better=True, wide=True, kicker="MISSION · 10 MIN", timer="10", right="LEVEL 01"
))
slides.append("""<section class="slide rulebook" %s>%s
<button type="button" class="rulebook-clock" data-clock title="Click start or pause. Double-click reset">10:00</button>
<div class="rulebook-copy">
<p class="lp-col-label">Points rule book</p>
<h2>How teams score.</h2>
<ol class="rulebook-list">
<li><b>10</b><div><strong>Speed</strong><span>First correct call.</span></div></li>
<li><b>20</b><div><strong>Accuracy</strong><span>The right name.</span></div></li>
<li><b>20</b><div><strong>Understanding</strong><span>What the tool is for.</span></div></li>
</ol>
</div>
</section>""" % (
    attrs(14, "Points rule book", "ACT 2 · THE PLAYGROUND",
          "Click the big clock. It counts down from ten. First correct call: 10 speed. Right name: 20 accuracy. What the tool is for: 20 understanding. Then five rapid-fire questions: exact 5, close 3, wrong −3.",
          timer="10"),
    meta("10 MIN", "LEVEL 01")
))

slides.append("""<section class="slide quiz-time" %s>%s
<div class="quiz-time-body">
<h2>Quiz time.</h2>
<ol class="quiz-time-rules">
<li><b>01</b><div><strong>Hand up.</strong><span>Question on the wall. Hands go up. No shouting the answer.</span></div></li>
<li><b>02</b><div><strong>First hand.</strong><span>I call the first hand. One answer. Sit if I don’t call you.</span></div></li>
</ol>
<div class="quiz-score">
<div><b>+5</b><strong>Exact</strong><span>The words on the wall.</span></div>
<div><b>+3</b><strong>Close</strong><span>Right idea. Wrong name.</span></div>
<div><b>−3</b><strong>Wrong</strong><span>Next hand.</span></div>
</div>
</div>
</section>""" % (
    attrs(79, "Quiz time", "ACT 2 · THE PLAYGROUND",
          "Hands only. First hand answers. Exact 5. Close 3. Wrong −3 and next hand. Then Q1."),
    meta("QUIZ TIME", "+5 · +3 · −3")
))

RAPID = [
    (
        "Name the six parts of the welcome screen.",
        "Illustration. Heading. Supporting text. Primary button. Secondary action. Carousel indicator.",
        "Wait. Six parts on the welcome they just built. Do not list them.",
    ),
    (
        "On the first screen, which button is louder?",
        "Sign Up. Filled primary. Sign In stays outlined.",
        "They just drew both. If they say both, no points.",
    ),
    (
        "Email and password. Name the component.",
        "Text fields. Label above. Value inside.",
        "If they say boxes, push for the name: text field.",
    ),
    (
        "“I agree to the Terms.” Name the component.",
        "A checkbox.",
        "Do not offer radio or switch. Let them name it.",
    ),
    (
        "“Already have an account? Log In.” Name the component.",
        "A text link. She’s already on Sign Up. Don’t compete with the primary.",
        "Wait for text link. If they say button, −3. Then: it must not fight Sign Up.",
    ),
]
WELCOME = "assets/mindspace/welcome.png"
SIGNUP = "assets/mindspace/signup.png"
WELCOME_PARTS = [
    "Illustration",
    "Heading",
    "Supporting text",
    "Primary button",
    "Secondary action",
    "Carousel indicator",
]
for i, (question, answer, note) in enumerate(RAPID, 1):
    qnum = f"Q{i}"
    slides.append(ask(
        80 + i * 2 - 1, f"Question {i}", "ACT 2 · THE PLAYGROUND",
        f"Exact 5. Close 3. Wrong −3. {note} Then reveal.",
        question, kicker=qnum, right="+5 · +3 · −3", qnum=qnum,
        src=WELCOME if i in (1, 2) else SIGNUP if i in (4, 5) else "",
    ))
    if i == 1:
        marks = "".join(f'<li class="m{n}">{n}</li>' for n in range(1, 7))
        names = "".join(
            f"<li><b>{n:02d}</b><span>{name}</span></li>"
            for n, name in enumerate(WELCOME_PARTS, 1)
        )
        slides.append("""<section class="slide rapid-answer has-phone ans-welcome-slide" %s>%s
<figure class="ans-welcome">
<img src="%s" alt="Welcome screen with six numbered parts">
<ol class="ans-welcome-marks" aria-hidden="true">%s</ol>
</figure>
<div class="rapid-answer-body">
<p class="rapid-qn">Q1</p>
<ol class="ans-welcome-list">%s</ol>
</div>
</section>""" % (
            attrs(80 + i * 2, f"Answer {i}", "ACT 2 · THE PLAYGROUND",
                  f"Award 5, 3, or −3. Open Score, click the team, then + / − pts. {answer}"),
            meta(qnum, "+5 · +3 · −3"),
            WELCOME, marks, names
        ))
    else:
        slides.append(answered(
            80 + i * 2, f"Answer {i}", "ACT 2 · THE PLAYGROUND",
            f"Award 5, 3, or −3. Open Score, click the team, then + / − pts. {answer}",
            question, answer, kicker=qnum, right="+5 · +3 · −3", qnum=qnum
        ))

slides.append(lime(
    80, "Check scores", "ACT 2 · THE PLAYGROUND",
    "Check scores. Then Level 02.",
    "Check scores.",
    kicker="QUIZ", right="THE BOARD"
))

slides.append(phone(
    15, "Build the frame", "ACT 2 · THE PLAYGROUND",
    "Create a mobile frame. Frames, dimensions, constraints.",
    "assets/figma/frame.svg",
    "Teaching diagram · mobile frame",
    "Your phone screen starts here.",
    extra_html="<p>Create a mobile frame. 390-wide is fine. Name it with Arya's sentence.</p>",
    better=True, kicker="MISSION"
))
slides.append(wide(
    16, "Build the interface", "ACT 2 · THE PLAYGROUND",
    "Shape. Text. Image. Colour. Add the basic elements.",
    "assets/figma/shapes.svg",
    "Teaching diagram · progressive construction of a welcome screen."
))
slides.append(pair(
    17, "Make it align", "ACT 2 · THE PLAYGROUND",
    "Good design is not placing things anywhere. Fix spacing, alignment, grouping. Alignment, proximity, consistency.",
    ("assets/ui-group-weak.svg", "Misaligned · teaching diagram", False),
    ("assets/ui-group-good.svg", "Aligned · teaching diagram", True),
    kicker="MISSION"
))
slides.append(lesson(
    18, "Make it reusable", "ACT 2 · THE PLAYGROUND",
    "Quiz. 15 points if they can say why a component, not twenty copies, before the clock.",
    "What if you need 20 identical buttons?",
    subtitle="Individual copies versus a reusable component. Quiz: 15 points if they answer before the clock.",
    rules=[
        "Draw one primary button.",
        "Make it a component.",
        "Place three instances.",
        "Change the master. Watch the copies follow.",
    ],
    grades=[("15", "Quiz · answer before the clock")],
    kicker="QUIZ", right="15 PTS"
))
slides.append(pair(
    19, "Let the layout adapt", "ACT 2 · THE PLAYGROUND",
    "What happens when the text becomes longer? Fixed positioning versus Auto Layout. Create a simple Auto Layout structure.",
    ("assets/figma/constrain.svg", "Fixed position · teaching diagram", False),
    ("assets/figma/type-size.svg", "Auto Layout · teaching diagram", True),
    kicker="AUTO LAYOUT"
))
slides.append(studio(
    20, "Mission complete", "ACT 2 · THE PLAYGROUND",
    "One neighbour. One fix. Then Level 02.",
    "One neighbour. One fix.",
    "Point at theirs. Name one thing you would change. Then we score you.",
    "3 min", "3", kicker="CHECKPOINT"
))
slides.append(lesson(
    21, "Check yours", "ACT 2 · THE PLAYGROUND",
    "Punch list, not a lesson recap. If they cannot find these on their frame, they are not ready to score.",
    "Check yours.",
    rules=["A named frame.", "Things that align.", "A component, not twenty copies.", "Spacing you can count.", "One thing louder than the rest.", "Text that can grow."],
    kicker="CHECKPOINT", right="LEVEL 01"
))

# ACT 3
slides.append(level(
    22, "Level 2 unlocked", "ACT 3 · THE UI UNIVERSE",
    "Scoring starts. Rapid challenges. Do not lecture every widget.",
    2, "The UI Universe.",
    "",
    timer="45", right="00:45–01:30"
))
slides.append(wide(
    23, "Components", "ACT 3 · THE UI UNIVERSE",
    "Open the kit. Components are building blocks. Action, containment, communication, navigation, selection, text input.",
    "assets/m3/overview.png",
    "Material 3 Design Kit · Components overview."
))
slides.append(lesson(
    24, "Game rules", "ACT 3 · THE UI UNIVERSE",
    "See it. Understand it. Choose it. Defend it. Do not award points for finishing first.",
    "How you score.",
    grades=[
        ("3", "Correct identification"),
        ("8", "Correct component choice"),
        ("8", "Strong reasoning"),
        ("6", "Spotting a usability issue"),
        ("10", "Excellent improvement"),
    ],
    kicker="SCORING", right="LEVEL 02"
))

ACT3 = "ACT 3 · THE UI UNIVERSE"
PTS = "+5 · +3 · −3"

def universe_qa(n, num, family, question, answer, note):
    qnum = f"Q{num}"
    slides.append(ask(
        n, f"{family} question", ACT3, note, question,
        kicker=qnum, right=PTS, qnum=qnum
    ))
    slides.append(answered(
        n + 1, f"{family} answer", ACT3,
        f"Award 5, 3, or −3. {answer}",
        question, answer, kicker=family.upper(), right=PTS, qnum=qnum
    ))

# 01 Buttons
universe_qa(
    91, 1, "Button",
    "One press starts the next step. Sign Up. Play. Start sleep. Name the component.",
    "A button. It starts an action. One tap.",
    "Wait for button, not the look. Then reveal.",
)
slides.append("""<section class="slide phone-pair btn-usage" %s>%s
<div class="pair-row">
<figure class="bu-card">
<div class="bu-form" aria-hidden="true">
<p class="bu-title">Sign in</p>
<div class="bu-field">Email</div>
<div class="bu-field">Password</div>
<div class="bu-actions">
<span class="bt is-filled bu-full">Sign in</span>
<span class="bt is-filled bu-full">Create account</span>
<span class="bt is-filled bu-full">Forgot password?</span>
</div>
</div>
<figcaption>Bad</figcaption>
</figure>
<figure class="bu-card is-better">
<div class="bu-form" aria-hidden="true">
<p class="bu-title">Sign in</p>
<div class="bu-field">Email</div>
<div class="bu-field">Password</div>
<div class="bu-actions">
<span class="bt is-filled bu-full">Sign in</span>
<span class="bt is-outlined bu-full">Create account</span>
<span class="bt is-text bu-quiet">Forgot password?</span>
</div>
</div>
<figcaption>Good</figcaption>
</figure>
</div>
</section>""" % (
    attrs(
        93, "Button usage", ACT3,
        "One primary. The rest stay quiet. Three equal buttons hide the next step.",
    ),
    meta("USAGE", ""),
))
_BT_PENCIL = (
    '<svg class="bt-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'd="M14.2 5.2l4.6 4.6M4 20l1.4-5.2L16.6 3.6a2 2 0 0 1 2.8 2.8L8.2 17.6 4 20z"/>'
    "</svg>"
)
_BT_PLUS = (
    '<svg class="bt-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" d="M12 5v14M5 12h14"/>'
    "</svg>"
)
_BT_CHECK = (
    '<svg class="bt-ico bt-ico-sm" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l5 5 9-10"/>'
    "</svg>"
)
slides.append("""<section class="slide lesson-plan btn-types" %s>%s
<div class="lp-body">
<div class="lp-heading">
<h2>Types of button.</h2>
<p class="bt-lede">Filled is the verb. The rest stay quiet.</p>
</div>
<div class="bt-grid">
<figure class="bt-spec">
<div class="bt-stage" aria-hidden="true"><span class="bt is-elevated">Begin</span></div>
<figcaption class="bt-name">Elevated Button</figcaption>
</figure>
<figure class="bt-spec">
<div class="bt-stage" aria-hidden="true"><span class="bt is-filled">Begin</span></div>
<figcaption class="bt-name">Filled Button</figcaption>
</figure>
<figure class="bt-spec">
<div class="bt-stage" aria-hidden="true"><span class="bt is-tonal">Save</span></div>
<figcaption class="bt-name">Filled Tonal Button</figcaption>
</figure>
<figure class="bt-spec">
<div class="bt-stage" aria-hidden="true"><span class="bt is-outlined">Message</span></div>
<figcaption class="bt-name">Outlined Button</figcaption>
</figure>
<figure class="bt-spec">
<div class="bt-stage" aria-hidden="true"><span class="bt is-text">Skip</span></div>
<figcaption class="bt-name">Text Button</figcaption>
</figure>
<figure class="bt-spec">
<div class="bt-stage" aria-hidden="true"><span class="bt is-icon">%s</span></div>
<figcaption class="bt-name">Icon Button</figcaption>
</figure>
<figure class="bt-spec">
<div class="bt-stage" aria-hidden="true"><span class="bt is-fab">%s</span></div>
<figcaption class="bt-name">FAB Button</figcaption>
</figure>
<figure class="bt-spec">
<div class="bt-stage" aria-hidden="true"><span class="bt is-fab-ext">%s Add</span></div>
<figcaption class="bt-name">Extended FAB Button</figcaption>
</figure>
<figure class="bt-spec is-wide">
<div class="bt-stage" aria-hidden="true">
<div class="bt-seg">
<span class="is-on">%s Sleep</span>
<span>Focus</span>
<span>Calm</span>
</div>
</div>
<figcaption class="bt-name">Segmented Button</figcaption>
</figure>
</div>
</div>
</section>""" % (
    attrs(
        94, "Button types", ACT3,
        "Filled is the verb. Outlined and text stay secondary. FAB is one obvious create. Icon is a tool, not the next step. Point at filled first - one primary, the rest stay quiet. Elevated is the same verb with a lift. Tonal is important, not the loudest. Segmented is one of a set on the same row."
    ),
    meta("KIT", "BUTTON"),
    _BT_PENCIL,
    _BT_PLUS,
    _BT_PLUS,
    _BT_CHECK,
))
slides.append("""<section class="slide lesson-plan btn-states" %s>%s
<div class="lp-body">
<div class="lp-heading">
<h2>Button states.</h2>
<p class="bs-lede">Variants are looks. States are what is happening.</p>
</div>
<ol class="bs-list" aria-label="Five states of the same Begin button">
<li>
<div class="bs-demo">
<span class="bs-btn">Begin</span>
</div>
<p class="bs-name">Enabled</p>
<p class="bs-line">She can use it.</p>
</li>
<li>
<div class="bs-demo">
<span class="bs-btn is-focus">Begin</span>
<span class="bs-tab">Tab</span>
</div>
<p class="bs-name">Focus</p>
<p class="bs-line">Keyboard is on it.</p>
</li>
<li>
<div class="bs-demo">
<span class="bs-btn is-hover">Begin</span>
<svg class="bs-pointer" viewBox="0 0 32 32" aria-hidden="true">
<path fill="#ece9e1" stroke="#101116" stroke-width="2.2" stroke-linejoin="round" d="M7 3l18 13.2-8.2 1.6 3.4 11.2-5.6-3.6-5.2 7.4z"/>
</svg>
</div>
<p class="bs-name">Hover</p>
<p class="bs-line">Pointer is on it.</p>
</li>
<li>
<div class="bs-demo">
<span class="bs-btn is-down">Begin</span>
</div>
<p class="bs-name">Pressed</p>
<p class="bs-line">The press is happening.</p>
</li>
<li>
<div class="bs-demo">
<span class="bs-btn is-off">Begin</span>
</div>
<p class="bs-name">Disabled</p>
<p class="bs-line">Cannot tap it now.</p>
</li>
</ol>
</div>
</section>""" % (
    attrs(
        95, "Button states", ACT3,
        "Same component. Different moment. Variants are looks. States are what is happening. Walk the five from the last bench: ready, keyboard, pointer, press, locked. Disabled must look unavailable. Ask: is this five buttons, or one Begin in five moments?"
    ),
    meta("STATES", "BUTTON")
))

# 02 Text fields
universe_qa(
    96, 2, "Text field",
    "A labelled box Arya fills with words or a number. Name the component.",
    "A text field. Arya types. Label above. Value inside.",
    "If they say box, push for text field.",
)
slides.append(pair(
    98, "Text field usage", ACT3,
    "A field without a label is a guess. Error must explain, not just turn red.",
    ("assets/ds/field-bare.svg", "Bad · no label", False),
    ("assets/ds/field-named.svg", "Good · label on the field", True),
    kicker="USAGE"
))
slides.append("""<section class="slide lesson-plan field-states-slide" %s>%s
<div class="lp-body field-states-body">
<div class="lp-heading"><h2>Types and states.</h2></div>
<div class="field-states-grid" id="field-states-grid">
<article class="field-states-cell">
<label class="field-states-label" for="fs-inactive">Your name</label>
<input class="field-states-input" id="fs-inactive" type="text" name="fs-inactive" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
<p class="field-states-help" aria-hidden="true">&nbsp;</p>
<p class="field-states-caption">Inactive</p>
</article>
<article class="field-states-cell is-hover-demo">
<label class="field-states-label" for="fs-hover">Your name</label>
<input class="field-states-input" id="fs-hover" type="text" name="fs-hover" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
<p class="field-states-help" aria-hidden="true">&nbsp;</p>
<p class="field-states-caption">Hover</p>
</article>
<article class="field-states-cell is-disabled">
<label class="field-states-label" for="fs-disabled">Reminder time</label>
<input class="field-states-input" id="fs-disabled" type="text" name="fs-disabled" value="7:00 AM" disabled>
<p class="field-states-help" aria-hidden="true">&nbsp;</p>
<p class="field-states-caption">Disabled</p>
</article>
<article class="field-states-cell">
<label class="field-states-label" for="fs-focus">Your name</label>
<input class="field-states-input" id="fs-focus" type="text" name="fs-focus" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
<p class="field-states-help" aria-hidden="true">&nbsp;</p>
<p class="field-states-caption">Focus / active</p>
</article>
<article class="field-states-cell is-validate">
<label class="field-states-label" for="fs-validate">Display name</label>
<input class="field-states-input" id="fs-validate" type="text" name="fs-validate" value="Arya" data-fs-validate autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" aria-describedby="fs-validate-help">
<p class="field-states-help is-checking" id="fs-validate-help" data-fs-status><span class="field-states-spin" aria-hidden="true"></span>Checking...</p>
<p class="field-states-caption">Validation</p>
</article>
<article class="field-states-cell is-error">
<label class="field-states-label" for="fs-error">Display name</label>
<input class="field-states-input" id="fs-error" type="text" name="fs-error" value="A" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" aria-invalid="true" aria-describedby="fs-error-help">
<p class="field-states-help" id="fs-error-help"><span class="field-states-x" aria-hidden="true"></span>Already taken</p>
<p class="field-states-caption">Error</p>
</article>
</div>
</div>
</section>""" % (
    attrs(
        99, "Text field types", ACT3,
        "Click empty. Hover the next so the back row sees the border jump. Disabled cannot type. Focus: the lime ring must read from the last bench. Checking is a wait, not a lock. Error says what to fix. Filled or outlined is a look. State is the moment."
    ),
    meta("KIT", "TEXT FIELD")
))

# 03 Checkbox
universe_qa(
    100, 3, "Checkbox",
    "More than one yes can stay on. Sleep and stress. Name the component.",
    "A checkbox. Tick one or many. Each choice stands alone.",
    "Do not offer radio. Let them name checkbox.",
)
_CB_X = (
    '<svg class="cb-flag-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" d="M6 6l12 12M18 6L6 18"/>'
    "</svg>"
)
_CB_OK = (
    '<svg class="cb-flag-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l5 5 9-10"/>'
    "</svg>"
)
_CB_NEEDS = (
    ("Sleep", True),
    ("Stress", True),
    ("Focus", False),
    ("Anxiety", False),
    ("Energy", False),
    ("Mood", False),
    ("Breath", True),
    ("Gratitude", False),
    ("Journal", False),
    ("Walking", False),
    ("Evening", False),
    ("Morning", False),
    ("Night", False),
    ("Weekend", False),
)
_cb_tiny = "".join(
    '<li class="%s"><span class="cb-box%s" aria-hidden="true"></span>%s</li>'
    % ("is-on" if on else "", " is-on" if on else "", label)
    for label, on in _CB_NEEDS
)
_cb_pills = "".join(
    '<span class="cb-pill%s"><span class="cb-box%s" aria-hidden="true"></span>%s</span>'
    % (" is-on" if on else "", " is-on" if on else "", label)
    for label, on in _CB_NEEDS
)
slides.append("""<section class="slide lesson-plan checkbox-usage" %s>%s
<div class="lp-body cb-usage-body">
<div class="cb-usage">
<article class="cb-card is-bad">
<p class="cb-flag is-bad">%s Bad</p>
<p class="cb-screen">I want help with</p>
<div class="cb-bad-body">
<ul class="cb-tiny">%s</ul>
<p class="cb-hits"><span>Harder to tap</span><span>A tall list</span><span>Too many boxes</span></p>
</div>
<p class="cb-cap">Tiny ticks. A long list.</p>
</article>
<article class="cb-card is-good">
<p class="cb-flag is-good">%s Good</p>
<p class="cb-screen">I want help with</p>
<div class="cb-pills">%s</div>
<p class="cb-cap">Big targets. Easy to tap.</p>
</article>
</div>
</div>
</section>""" % (
    attrs(
        102, "Checkbox usage", ACT3,
        "Tiny ticks hide in a long list. Same yeses as bigger targets. She can hit sleep and stress with a thumb. Days of week is the same miss."
    ),
    meta("USAGE", "CHECKBOX"),
    _CB_X,
    _cb_tiny,
    _CB_OK,
    _cb_pills,
))
# 04 Radio
universe_qa(
    104, 4, "Radio",
    "Only one choice can stay on. Morning or evening. Name the component.",
    "Radio. One of a set. Pick one. The others clear.",
    "If they say checkbox, −3. Exclusive pick is radio.",
)
_CHEV_UP = (
    '<svg class="sel-chev" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
    'stroke-linejoin="round" d="M6 15l6-6 6 6"/>'
    "</svg>"
)
slides.append("""<section class="slide lesson-plan pick-pair" %s>%s
<div class="lp-body cb-usage-body">
<div class="cb-usage">
<article class="cb-card">
<h2 class="pick-title">One</h2>
<p class="cb-screen">Session length</p>
<div class="pick-list" data-pick>
<label class="pick-opt"><input type="radio" name="pick-len" value="5"><span class="sel-radio" aria-hidden="true"></span>5 min</label>
<label class="pick-opt"><input type="radio" name="pick-len" value="10" checked><span class="sel-radio" aria-hidden="true"></span>10 min</label>
<label class="pick-opt"><input type="radio" name="pick-len" value="20"><span class="sel-radio" aria-hidden="true"></span>20 min</label>
</div>
<p class="cb-cap">Radio</p>
</article>
<article class="cb-card">
<h2 class="pick-title">Many</h2>
<p class="cb-screen">I want help with</p>
<div class="pick-list" data-pick>
<label class="pick-opt"><input type="checkbox" name="pick-need" value="sleep" checked><span class="cb-box" aria-hidden="true"></span>Sleep</label>
<label class="pick-opt"><input type="checkbox" name="pick-need" value="stress" checked><span class="cb-box" aria-hidden="true"></span>Stress</label>
<label class="pick-opt"><input type="checkbox" name="pick-need" value="focus"><span class="cb-box" aria-hidden="true"></span>Focus</label>
</div>
<p class="cb-cap">Checkbox</p>
</article>
</div>
</div>
</section>""" % (
    attrs(
        106, "One or many", ACT3,
        "One pick is radio. Many independent yeses are checkbox. Session length is 5, 10 or 20. Sleep and stress can both stay on."
    ),
    meta("USAGE", "RADIO / CHECKBOX"),
))
slides.append("""<section class="slide lesson-plan pick-pair" %s>%s
<div class="lp-body cb-usage-body">
<div class="cb-usage">
<article class="cb-card is-bad">
<p class="cb-flag is-bad">%s Bad</p>
<p class="cb-screen">Session length</p>
<div class="sel-menu" aria-hidden="true">
<p class="sel-menu-btn">Choose a length... %s</p>
<ul class="sel-menu-list">
<li>5 min</li>
<li>10 min</li>
<li>20 min</li>
</ul>
</div>
</article>
<article class="cb-card is-good">
<p class="cb-flag is-good">%s Good</p>
<p class="cb-screen">Session length</p>
<ul class="pick-list is-static">
<li class="pick-opt"><span class="sel-radio" aria-hidden="true"></span>5 min</li>
<li class="pick-opt is-on"><span class="sel-radio is-on" aria-hidden="true"></span>10 min</li>
<li class="pick-opt"><span class="sel-radio" aria-hidden="true"></span>20 min</li>
</ul>
</article>
</div>
</div>
</section>""" % (
    attrs(
        132, "Radios not a menu", ACT3,
        "Three lengths. Keep them on the screen. A short exclusive list is radio, not Choose a length."
    ),
    meta("USAGE", "RADIO"),
    _CB_X,
    _CHEV_UP,
    _CB_OK,
))

def _state_cell(kind, caption, on=False, hover=False, focus=False, disabled=False, label="10 min"):
    mark = "sel-radio" if kind == "radio" else "cb-box"
    extras = []
    if on:
        extras.append("is-on")
    if hover:
        extras.append("is-hover-demo")
    if focus:
        extras.append("is-focus-demo")
    if disabled:
        extras.append("is-disabled")
    cls = (" " + " ".join(extras)) if extras else ""
    tab = ' tabindex="0"' if focus else ""
    on_cls = " is-on" if on else ""
    return (
        '<article class="sel-cell%s"%s>'
        '<div class="sel-demo"><span class="%s%s" aria-hidden="true"></span>%s</div>'
        '<p class="sel-caption">%s</p></article>'
    ) % (cls, tab, mark, on_cls, label, caption)

_SS_CAPS = (
    ("Unselected", {}),
    ("Selected", {"on": True}),
    ("Hover / focus", {"hover": True, "focus": True}),
    ("Disabled", {"disabled": True}),
)
_ss_radio = "".join(_state_cell("radio", cap, **kw) for cap, kw in _SS_CAPS)
_ss_check = "".join(
    _state_cell("check", cap, label="Sleep", **kw) for cap, kw in _SS_CAPS
)
slides.append("""<section class="slide lesson-plan sel-states" %s>%s
<div class="lp-body sel-states-body">
<div class="lp-heading"><h2>States.</h2></div>
<div class="sel-band">
<p class="sel-band-name">Radio</p>
<div class="sel-row">%s</div>
</div>
<div class="sel-band">
<p class="sel-band-name">Checkbox</p>
<div class="sel-row">%s</div>
</div>
</div>
</section>""" % (
    attrs(
        107, "Selection states", ACT3,
        "Walk unselected, selected, hover, focus, disabled from the last bench. Radio stays a group. Checkbox stands alone."
    ),
    meta("STATES", "SELECT"),
    _ss_radio,
    _ss_check,
))

# 05 Switch
universe_qa(
    108, 5, "Switch",
    "A setting that flips on or off and takes effect now. Reminders. Name the component.",
    "A switch. On or off. It takes effect now.",
    "Switch is not a form submit. Immediate.",
)
slides.append(pair(
    110, "Switch usage", ACT3,
    "Switch for a setting that flips now. Not a list of goals. Not a single exclusive pick.",
    ("assets/m3/switch-bad.svg", "Bad · agree as a switch", False),
    ("assets/mindspace/switch.svg", "Good · one setting, now", True),
    kicker="USAGE"
))
slides.append("""<section class="slide lesson-plan toggle-states" %s>%s
<div class="lp-body toggle-states-body">
<div class="lp-heading">
<h2>Switch states.</h2>
</div>
<ul class="toggle-states-grid" id="toggle-states-grid">
<li>
<button type="button" class="toggle-states-switch" role="switch" aria-checked="false" aria-label="Default">
<span class="toggle-states-thumb" aria-hidden="true"></span>
</button>
<p class="toggle-states-name">Default</p>
</li>
<li>
<button type="button" class="toggle-states-switch is-on" role="switch" aria-checked="true" aria-label="Active">
<span class="toggle-states-thumb" aria-hidden="true"></span>
</button>
<p class="toggle-states-name">Active</p>
</li>
<li>
<button type="button" class="toggle-states-switch is-focused" role="switch" aria-checked="false" aria-label="Focused" data-locked="true">
<span class="toggle-states-thumb" aria-hidden="true"></span>
</button>
<p class="toggle-states-name">Focused</p>
</li>
<li class="is-disabled">
<button type="button" class="toggle-states-switch is-disabled" role="switch" aria-checked="false" aria-label="Disabled" disabled>
<span class="toggle-states-thumb" aria-hidden="true"></span>
</button>
<p class="toggle-states-name">Disabled</p>
</li>
</ul>
</div>
</section>""" % (
    attrs(
        111, "Switch states", ACT3,
        "Default is off. Active is on now. Focused is the keyboard ring. Disabled cannot flip. No third choice. If they must confirm, it is not a switch. Click Default or Active to feel the flip. Arrows still turn the deck."
    ),
    meta("STATES", "SWITCH"),
))

def _card_ux(title, badge, sub, copy, cta="Begin", cls="", more=False):
    more_html = ' <span class="card-ux-more">Show more</span>' if more else ""
    return (
        f'<article class="card-ux {cls}">'
        f'<div class="card-ux-preview" aria-hidden="true"></div>'
        f'<div class="card-ux-body">'
        f'<div class="card-ux-title-row">'
        f'<p class="card-ux-title">{title}</p>'
        f'<span class="card-ux-badge">{badge}</span>'
        f"</div>"
        f'<p class="card-ux-sub">{sub}</p>'
        f'<p class="card-ux-copy">{copy}{more_html}</p>'
        f"</div>"
        f'<div class="card-ux-foot"><span class="card-ux-cta">{cta}</span></div>'
        "</article>"
    )


def _card_ux_stack(title, badge, sub, copy, cta="Begin", cls="", more=False):
    more_html = '<span class="card-ux-more">Show more</span>' if more else ""
    return (
        f'<article class="card-ux is-stack {cls}">'
        f'<div class="card-ux-body">'
        f'<div class="card-ux-title-row">'
        f'<p class="card-ux-title">{title}</p>'
        f'<span class="card-ux-badge">{badge}</span>'
        f"</div>"
        f'<p class="card-ux-sub">{sub}</p>'
        f"</div>"
        f'<div class="card-ux-preview" aria-hidden="true"></div>'
        f'<p class="card-ux-copy">{copy}</p>'
        f"{more_html}"
        f'<div class="card-ux-foot"><span class="card-ux-cta">{cta}</span></div>'
        "</article>"
    )


def _card_ux_panel(inner, better=False, cap="Bad"):
    cls = "card-ux-panel is-better" if better else "card-ux-panel"
    return f'<figure class="{cls}">{inner}<figcaption>{cap}</figcaption></figure>'


# 06 Cards
universe_qa(
    112, 6, "Card",
    "One session on its own. Image, title, one tap. Name the component.",
    "A card. One object. One tap. Containment.",
    "Containment, not decoration. Then reveal.",
)
slides.append("""<section class="slide lesson-plan card-ux-anatomy" %s>%s
<div class="lp-body card-ux-anatomy-body">
<div class="card-ux-anatomy-stage">
<article class="card-ux card-ux-anatomy-card">
<div class="card-ux-preview" aria-hidden="true"></div>
<div class="card-ux-title-row">
<p class="card-ux-title">Breath for stress</p>
<span class="card-ux-badge">10 min</span>
</div>
<p class="card-ux-sub">Guided</p>
<p class="card-ux-copy">A short reset before her desk.</p>
<div class="card-ux-foot"><span class="card-ux-cta">Begin</span></div>
</article>
<ul class="card-ux-callouts">
<li><i></i>Preview</li>
<li><i></i>Title <b>Badge</b></li>
<li><i></i>Subtitle</li>
<li><i></i>Supporting</li>
<li><i></i>CTA</li>
</ul>
</div>
</div>
</section>""" % (
    attrs(
        114, "Card anatomy", ACT3,
        "One object. Preview, title, badge, subtitle, supporting, CTA. Point from the last bench. Then the pairs.",
    ),
    meta("ANATOMY", "CARD"),
))
slides.append("""<section class="slide phone-pair card-ux-pair" %s>%s
<div class="pair-row">
%s
%s
</div>
</section>""" % (
    attrs(
        115, "Card type", ACT3,
        "Headline louder than subhead louder than body. The button is a verb, not a shout.",
    ),
    meta("TYPE", "CARD"),
    _card_ux_panel(_card_ux(
        "Breath for stress", "10 min", "Guided",
        "A short reset before her desk.",
        cls="is-type-bad",
    ), cap="Bad"),
    _card_ux_panel(_card_ux(
        "Breath for stress", "10 min", "Guided",
        "A short reset before her desk.",
        cls="is-type-good",
    ), True, "Good"),
))
slides.append("""<section class="slide phone-pair card-ux-pair" %s>%s
<div class="pair-row">
%s
%s
</div>
</section>""" % (
    attrs(
        140, "Card spacing", ACT3,
        "Even rhythm. If the gaps argue, she cannot scan. No rulers. Feel the beat.",
    ),
    meta("SPACE", "CARD"),
    _card_ux_panel(_card_ux(
        "Sleep stories", "15 min", "Night",
        "Dim, quiet, and done in time.",
        cls="is-space-bad is-sleep",
    ), cap="Bad"),
    _card_ux_panel(_card_ux(
        "Sleep stories", "15 min", "Night",
        "Dim, quiet, and done in time.",
        cls="is-space-good is-sleep",
    ), True, "Good"),
))
slides.append("""<section class="slide phone-pair card-ux-pair" %s>%s
<div class="pair-row">
%s
%s
</div>
</section>""" % (
    attrs(
        141, "Card loading", ACT3,
        "A spinner is a shrug. The skeleton is the card arriving.",
    ),
    meta("LOADING", "CARD"),
    _card_ux_panel(
        '<article class="card-ux is-wait" aria-hidden="true">'
        '<span class="card-ux-spin"></span>'
        "<p>Please wait</p>"
        "</article>",
        cap="Bad",
    ),
    _card_ux_panel(
        '<article class="card-ux is-skel" aria-hidden="true">'
        '<div class="card-ux-preview"></div>'
        '<div class="card-ux-body">'
        '<span class="card-ux-bar is-wide"></span>'
        '<span class="card-ux-bar is-mid"></span>'
        '<span class="card-ux-bar is-long"></span>'
        "</div>"
        '<div class="card-ux-foot"><span class="card-ux-bar is-btn"></span></div>'
        "</article>",
        True, "Good",
    ),
))
slides.append("""<section class="slide phone-pair card-ux-pair" %s>%s
<div class="pair-row">
%s
%s
</div>
</section>""" % (
    attrs(
        142, "Card alignment", ACT3,
        "Same height. Clamp the title. Images and CTAs share a line. Long copy gets Show more.",
    ),
    meta("ALIGN", "CARD"),
    _card_ux_panel(
        '<div class="card-ux-row">'
        + _card_ux_stack(
            "Breath for stress", "10 min", "Guided",
            "A short reset.",
            cls="is-align-bad",
        )
        + _card_ux_stack(
            "Evening wind-down she can actually finish tonight", "20 min", "Night",
            "A longer session for when the day ran her over and she still wants a close.",
            cls="is-align-bad is-sleep",
        )
        + "</div>",
        cap="Bad",
    ),
    _card_ux_panel(
        '<div class="card-ux-row is-even">'
        + _card_ux_stack(
            "Breath for stress", "10 min", "Guided",
            "A short reset before her desk.",
            cls="is-align-good",
            more=True,
        )
        + _card_ux_stack(
            "Evening wind-down she can actually finish tonight", "20 min", "Night",
            "A longer session for when the day ran her over.",
            cls="is-align-good is-sleep",
            more=True,
        )
        + "</div>",
        True, "Good",
    ),
))
slides.append("""<section class="slide lesson-plan card-ux-states" %s>%s
<div class="lp-body card-ux-states-body">
<div class="lp-heading"><h2>Card states.</h2></div>
<ul class="card-ux-states-grid">
<li>
<article class="card-ux is-compact is-live">
<div class="card-ux-preview" aria-hidden="true"></div>
<p class="card-ux-title">Breath for stress</p>
</article>
<p class="card-ux-state-name">Default</p>
</li>
<li>
<article class="card-ux is-compact is-hover">
<div class="card-ux-preview" aria-hidden="true"></div>
<p class="card-ux-title">Breath for stress</p>
</article>
<p class="card-ux-state-name">Hover</p>
</li>
<li>
<article class="card-ux is-compact is-down">
<div class="card-ux-preview" aria-hidden="true"></div>
<p class="card-ux-title">Breath for stress</p>
</article>
<p class="card-ux-state-name">Active</p>
</li>
<li>
<article class="card-ux is-compact is-focus">
<div class="card-ux-preview" aria-hidden="true"></div>
<p class="card-ux-title">Breath for stress</p>
</article>
<p class="card-ux-state-name">Focused</p>
</li>
</ul>
</div>
</section>""" % (
    attrs(
        143, "Card states", ACT3,
        "Default waits. Hover leans in. Active is the press. Focused is the keyboard ring. Hover the Default card. Arrows still turn the deck.",
    ),
    meta("STATES", "CARD"),
))

# 07 Lists
universe_qa(
    116, 7, "List",
    "Same row, stacked. Scan a set of sessions. Name the component.",
    "A list. Same row, stacked. Scan, then tap.",
    "Repeating rows are a list. A unique story is a card.",
)
slides.append("""<section class="slide phone-pair list-m2 list-usage-redo" %s>%s
<div class="list-redo-head"><h2>Same rows. Picture on the edge.</h2></div>
<div class="pair-row">
<figure class="phone-frame"><img src="assets/lists/usage-caution.png" alt="Picture in the middle"><figcaption>Bad</figcaption></figure>
<figure class="phone-frame is-better"><img src="assets/lists/usage-do.png" alt="Picture on the edge"><figcaption>Good</figcaption></figure>
</div>
</section>""" % (
    attrs(118, "List usage", ACT3,
          "Same rows, stacked. Picture on the edge so Arya can scan. Picture in the middle is harder."),
    meta("USAGE", "LIST"),
))
slides.append("""<section class="slide phone-pair list-types" %s>%s
<div class="list-redo-head"><h2>One line. Two. Three.</h2></div>
<div class="list-types-row">
<figure class="phone-frame">
<img src="assets/lists/one-line.png" alt="Single-line list">
<figcaption>One line</figcaption>
</figure>
<figure class="phone-frame">
<img src="assets/lists/two-line.png" alt="Two-line list">
<figcaption>Two line</figcaption>
</figure>
<figure class="phone-frame">
<img src="assets/lists/three-line.png" alt="Three-line list">
<figcaption>Three line</figcaption>
</figure>
</div>
</section>""" % (
    attrs(
        119, "List types", ACT3,
        "One line, two line, three line. Same row, stacked. Point from the last bench.",
    ),
    meta("TYPES", "LIST"),
))
slides.append(pair(
    219, "List anatomy", ACT3,
    "1 is the whole list. 2 is one row. 3 is the item. Icon, words, extra.",
    ("assets/lists/anatomy.png", "1 list · 2 row · 3 item", False),
    ("assets/lists/content.png", "1 icon · 2 words · 3 extra", False),
    kicker="ANATOMY", extra_cls="list-m2 list-anatomy"
))

# 08 Navigation bar
universe_qa(
    120, 8, "Navigation",
    "Always on screen. Three to five places Arya can go. Name the component.",
    "A navigation bar. Destinations, not actions.",
    "Destinations live in the bar. Actions live in buttons.",
)
slides.append(pair(
    122, "Navigation usage", ACT3,
    "Destinations live in the bar. Do not stuff every page into the top. Primary few up top. The rest below.",
    ("assets/mindspace/nav-usage-bad.svg", "Bad", False),
    ("assets/mindspace/nav-usage-good.svg", "Good", True),
    kicker="USAGE"
))
slides.append(phone(
    123, "Navigation types", ACT3,
    "Navigation bar is destinations. Top app bar is the screen title and the local tools.",
    "assets/m3/navigation-bar.png",
    "Material 3 kit · Navigation bar",
    "Bar versus app bar.",
    extra_html=kit_items([
        "Navigation bar — where you can go.",
        "Top app bar — where you are.",
        "Three to five destinations.",
        "Never put Sign Up in the bar.",
    ]),
    better=True, wide=True, kicker="KIT", right="NAV"
))
_AB_BACK = (
    '<svg class="appbar-types-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" '
    'stroke-linejoin="round" d="M15 5l-7 7 7 7"/>'
    "</svg>"
)
_AB_SEARCH = (
    '<svg class="appbar-types-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<circle cx="11" cy="11" r="6.2" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    '<path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" d="M16.2 16.2L21 21"/>'
    "</svg>"
)
_AB_MORE = (
    '<svg class="appbar-types-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<circle cx="6.5" cy="12" r="1.7" fill="currentColor"/>'
    '<circle cx="12" cy="12" r="1.7" fill="currentColor"/>'
    '<circle cx="17.5" cy="12" r="1.7" fill="currentColor"/>'
    "</svg>"
)
_AB_EDIT = (
    '<svg class="appbar-types-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" '
    'stroke-linejoin="round" d="M14.2 5.2l4.6 4.6M4 20l1.4-5.2L16.6 3.6a2 2 0 0 1 2.8 2.8L8.2 17.6 4 20z"/>'
    "</svg>"
)
_AB_MENU = (
    '<svg class="appbar-types-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" '
    'd="M5 7h14M5 12h14M5 17h14"/>'
    "</svg>"
)
_AB_MOON = (
    '<svg class="appbar-types-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" '
    'stroke-linejoin="round" d="M16.5 13.2A6.2 6.2 0 0 1 11 6.2 6.4 6.4 0 1 0 17.8 15a5.2 5.2 0 0 1-1.3-1.8z"/>'
    "</svg>"
)
slides.append("""<section class="slide lesson-plan appbar-types" %s>%s
<div class="lp-body appbar-types-body">
<div class="lp-heading">
<h2>Types of app bar.</h2>
<p class="appbar-types-lede">Where you are. Local tools.</p>
</div>
<div class="appbar-types-cols">
<div class="appbar-types-col">
<figure class="appbar-types-spec">
<div class="appbar-types-bar" aria-hidden="true">
<span class="appbar-types-hit">%s</span>
<p class="appbar-types-title">Mindspace</p>
<span class="appbar-types-cta">Begin</span>
</div>
<figcaption class="appbar-types-name">Small</figcaption>
</figure>
<figure class="appbar-types-spec">
<div class="appbar-types-bar" aria-hidden="true">
<span class="appbar-types-hit">%s</span>
<div class="appbar-types-copy">
<p class="appbar-types-title">Mindspace</p>
<p class="appbar-types-sub">Today’s session</p>
</div>
<span class="appbar-types-hit">%s</span>
</div>
<figcaption class="appbar-types-name">Title + subtitle</figcaption>
</figure>
<figure class="appbar-types-spec">
<div class="appbar-types-bar" aria-hidden="true">
<span class="appbar-types-hit">%s</span>
<div class="appbar-types-search">%s Search</div>
</div>
<figcaption class="appbar-types-name">Search</figcaption>
</figure>
<figure class="appbar-types-spec">
<div class="appbar-types-bar" aria-hidden="true">
<p class="appbar-types-title">Sleep</p>
<div class="appbar-types-tools">
<span class="appbar-types-hit">%s</span>
<span class="appbar-types-hit">%s</span>
<span class="appbar-types-hit">%s</span>
</div>
</div>
<figcaption class="appbar-types-name">Icons</figcaption>
</figure>
</div>
<div class="appbar-types-col">
<figure class="appbar-types-spec">
<div class="appbar-types-bar is-loud is-stack" aria-hidden="true">
<div class="appbar-types-row">
<span class="appbar-types-hit">%s</span>
<span class="appbar-types-cta is-ink">Begin</span>
</div>
<div class="appbar-types-copy">
<p class="appbar-types-title">Today</p>
<p class="appbar-types-sub">Afternoon session</p>
</div>
</div>
<figcaption class="appbar-types-name">Prominent</figcaption>
</figure>
<figure class="appbar-types-spec">
<div class="appbar-types-bar is-stack" aria-hidden="true">
<div class="appbar-types-row">
<span class="appbar-types-hit">%s</span>
<p class="appbar-types-title">Sleep</p>
<span class="appbar-types-ava">A</span>
</div>
<div class="appbar-types-search">%s Search</div>
</div>
<figcaption class="appbar-types-name">Search below</figcaption>
</figure>
<figure class="appbar-types-spec">
<div class="appbar-types-bar" aria-hidden="true">
<p class="appbar-types-title">Mindspace</p>
<div class="appbar-types-tools">
<span class="appbar-types-ava">A</span>
<span class="appbar-types-cta">Share</span>
</div>
</div>
<figcaption class="appbar-types-name">Avatar + action</figcaption>
</figure>
</div>
</div>
</div>
</section>""" % (
    attrs(
        135, "App bar types", ACT3,
        "Walk the last bench across seven bars. Small is back, title, one action. Subtitle names the moment. Search is a field. Icons are local tools. Prominent shouts the screen name. Search can sit under the bar. Avatar or Share is extra, not the title. Mindspace, Today, Sleep, Search. Not a shop kit.",
    ),
    meta("KIT", "APP BAR"),
    _AB_BACK,
    _AB_BACK,
    _AB_MORE,
    _AB_BACK,
    _AB_SEARCH,
    _AB_SEARCH,
    _AB_MOON,
    _AB_EDIT,
    _AB_MENU,
    _AB_BACK,
    _AB_SEARCH,
))

# 09 Chips
universe_qa(
    124, 9, "Chip",
    "A compact choice Arya can turn on. Sleep. Mood. Not the main verb. Name the component.",
    "A chip. A compact choice. Not the primary verb.",
    "If they say button, push: the verb is filled. This is a chip.",
)

_CHIP_X = (
    '<svg class="chip-example-x" viewBox="0 0 12 12" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" d="M3 3l6 6M9 3L3 9"/>'
    "</svg>"
)

def _chip_svg(inner):
    return (
        '<svg class="chip-example-svg" viewBox="0 0 24 24" aria-hidden="true">'
        f"{inner}</svg>"
    )

_CHIP_MARKS = {
    "Sleep": _chip_svg(
        '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" d="M16.6 13.4A6.1 6.1 0 0 1 11 6.4 6.5 6.5 0 1 0 18 15.2a5.3 5.3 0 0 1-1.4-1.8z"/>'
    ),
    "Stress": _chip_svg(
        '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" d="M4 12h3.2l2-6 3.2 12 2.2-6H20"/>'
    ),
    "Focus": _chip_svg(
        '<circle cx="12" cy="12" r="7.2" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<circle cx="12" cy="12" r="2.4" fill="currentColor"/>'
    ),
    "Calm": _chip_svg(
        '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" d="M12 3.5c3.6 4.4 6.2 7.2 6.2 11.1A6.2 6.2 0 1 1 5.8 14.6C5.8 10.7 8.4 7.9 12 3.5z"/>'
    ),
    "Breath": _chip_svg(
        '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'd="M4 9.2h10.2a2.8 2.8 0 1 0-2.6-2.8M4 14.8h12.4a2.8 2.8 0 1 1-2.6 2.8"/>'
    ),
    "Night": _chip_svg(
        '<path fill="currentColor" d="M12 3.2l1.15 3.55H17l-2.95 2.15.95 3.7L12 10.55 8.99 12.6l.95-3.7L7 6.75h3.85z"/>'
    ),
    "Rest": _chip_svg(
        '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" d="M4 16.5V10.2A2.2 2.2 0 0 1 6.2 8h7.1V16.5M4 16.5h16M17.4 16.5V11.4h2.4"/>'
    ),
}

def _chip_btn(label, on=False):
    cls = "chip-example-chip is-on" if on else "chip-example-chip"
    pressed = "true" if on else "false"
    return (
        f'<button type="button" class="{cls}" aria-pressed="{pressed}" aria-label="{label}">'
        f'<span class="chip-example-ico">{_CHIP_MARKS[label]}</span>'
        f'<span class="chip-example-label">{label}</span>'
        f"{_CHIP_X}"
        "</button>"
    )

_chip_row = "".join(
    _chip_btn(name, on)
    for name, on in (
        ("Sleep", True),
        ("Stress", False),
        ("Focus", True),
        ("Calm", False),
        ("Breath", False),
        ("Night", False),
        ("Rest", False),
    )
)
slides.append("""<section class="slide lesson-plan chip-example" %s>%s
<div class="lp-body chip-example-body">
<div class="lp-heading">
<h2>Chips.</h2>
</div>
<div class="chip-example-group" role="group" aria-label="Mood chips">
%s
</div>
</div>
</section>""" % (
    attrs(
        126, "Chip example", ACT3,
        "Selected is filled. The outline waits. The X lets her drop a choice. Click to flip. Arrows still turn the deck. Not the primary verb.",
    ),
    meta("EXAMPLE", "CHIP"),
    _chip_row,
))

# 10 Dialogs
universe_qa(
    128, 10, "Dialog",
    "The screen waits. Arya must confirm or dismiss. Name the component.",
    "A dialog. The screen waits. Confirm or dismiss.",
    "If they say snackbar, −3. Irreversible needs a decision.",
)
slides.append(pair(
    130, "Dialog usage", ACT3,
    "Dialog stops the screen. Snackbar is a whisper after something already happened.",
    ("assets/ds/toast.svg", "Bad · a whisper for a hard stop", False),
    ("assets/ds/dialog.svg", "Good · the screen waits", True),
    kicker="USAGE"
))
_DT_INFO = (
    '<svg class="dialog-types-ico" viewBox="0 0 24 24" aria-hidden="true">'
    '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/>'
    '<path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" d="M12 11v5"/>'
    '<circle cx="12" cy="7.4" r="1.15" fill="currentColor"/>'
    "</svg>"
)
slides.append("""<section class="slide lesson-plan dialog-types" %s>%s
<div class="lp-body dialog-types-body">
<div class="lp-heading">
<h2>Types of dialog.</h2>
<p class="dialog-types-lede">One confirm. One quiet dismiss.</p>
</div>
<div class="dialog-types-grid">
<figure class="dialog-types-spec">
<div class="dialog-types-phone" aria-hidden="true">
<article class="dialog-types-card">
<p class="dialog-types-kicker">Note</p>
<p class="dialog-types-title">We need your consent</p>
<p class="dialog-types-copy">Private notes stay in this session.</p>
<div class="dialog-types-actions">
<span class="dialog-types-btn is-quiet">Cancel</span>
<span class="dialog-types-btn is-fill">Got it</span>
</div>
</article>
</div>
<figcaption class="dialog-types-name">Alert</figcaption>
</figure>
<figure class="dialog-types-spec">
<div class="dialog-types-phone" aria-hidden="true">
<article class="dialog-types-card">
<span class="dialog-types-mark">%s</span>
<p class="dialog-types-title">Permission required</p>
<p class="dialog-types-copy">Ask a facilitator to open this session.</p>
<div class="dialog-types-actions">
<span class="dialog-types-btn is-quiet">Cancel</span>
<span class="dialog-types-btn is-fill">Got it</span>
</div>
</article>
</div>
<figcaption class="dialog-types-name">Permission</figcaption>
</figure>
<figure class="dialog-types-spec">
<div class="dialog-types-phone" aria-hidden="true">
<article class="dialog-types-card">
<p class="dialog-types-title">Archive session</p>
<p class="dialog-types-copy">After 30 days, this session is gone.</p>
<div class="dialog-types-actions is-stack">
<span class="dialog-types-btn is-fill is-wide">Archive</span>
<span class="dialog-types-btn is-quiet is-wide">Cancel</span>
</div>
</article>
</div>
<figcaption class="dialog-types-name">Archive</figcaption>
</figure>
<figure class="dialog-types-spec">
<div class="dialog-types-phone" aria-hidden="true">
<article class="dialog-types-card">
<p class="dialog-types-title">Session shared</p>
<p class="dialog-types-copy">Anyone with the link can read it.</p>
<div class="dialog-types-actions is-stack">
<span class="dialog-types-btn is-fill is-wide">Got it</span>
</div>
</article>
</div>
<figcaption class="dialog-types-name">Got it</figcaption>
</figure>
<figure class="dialog-types-spec">
<div class="dialog-types-phone" aria-hidden="true">
<article class="dialog-types-card">
<p class="dialog-types-title">Share session</p>
<p class="dialog-types-label">Full name</p>
<p class="dialog-types-field">Arya</p>
<div class="dialog-types-actions">
<span class="dialog-types-btn is-quiet">Previous</span>
<span class="dialog-types-btn is-fill">Confirm</span>
</div>
</article>
</div>
<figcaption class="dialog-types-name">Form</figcaption>
</figure>
<figure class="dialog-types-spec">
<div class="dialog-types-phone" aria-hidden="true">
<article class="dialog-types-card">
<p class="dialog-types-title">Choose a length</p>
<p class="dialog-types-kicker">Now 10 min</p>
<div class="dialog-types-choice is-on"><span class="dialog-types-radio"></span><span>20 min · evening</span></div>
<div class="dialog-types-choice"><span class="dialog-types-radio"></span><span>40 min · shared</span></div>
<div class="dialog-types-actions">
<span class="dialog-types-btn is-quiet">Cancel</span>
<span class="dialog-types-btn is-fill">Confirm</span>
</div>
</article>
</div>
<figcaption class="dialog-types-name">Choice</figcaption>
</figure>
</div>
</div>
</section>""" % (
    attrs(
        131, "Dialog types", ACT3,
        "Six templates. Point from the last bench: alert, permission, archive, got it, form, choice. Filled is the verb. Quiet dismiss never matches it. Never two filled buttons of equal weight. Archive stacks the loud action over Cancel.",
    ),
    meta("KIT", "DIALOG"),
    _DT_INFO,
))

slides.append(phone(
    25, "Spot the component", "ACT 3 · THE UI UNIVERSE",
    "60 seconds. Identify buttons, cards, navigation, inputs, selection, feedback. Then reveal annotations. Correct identification: 10 points.",
    "assets/mindspace/home-calm.svg",
    "Teaching diagram used as a quiz · find the real pieces in the Android kit",
    "What's on this screen?",
    extra_html=choices([
        ("Four custom widgets we invented", False, 0),
        ("App bar, cards, filled button, navigation", True, 10),
        ("A dashboard of equal tiles", False, 0),
    ]) + reveal("Buttons, cards, navigation, inputs, selection, feedback. Open the Android kit and point at each live."),
    better=True, kicker="GAME 1 · 8 MIN"
))
slides.append("""<section class="slide lesson-plan" %s>%s<div class="lp-body"><div class="lp-heading"><h2>Point at a family. Then pick a piece.</h2><p class="lp-subtitle">Every family is in play. Not every widget gets its own slide. Open the Android kit and steal from here.</p></div>
<div class="family-map">
<article><span>Selection</span><p>Radio, checkbox, switch, chips.</p></article>
<article><span>Input</span><p>Text fields, search, sliders, date pickers.</p></article>
<article><span>Actions</span><p>Filled, outlined, text, icon, FAB.</p></article>
<article><span>Navigation</span><p>Bottom bar, tabs, app bar, drawer.</p></article>
<article><span>Containment</span><p>Cards, lists, dividers, dialogs.</p></article>
<article><span>Feedback</span><p>Snackbar, progress, tooltip, badge.</p></article>
<article><span>Information</span><p>Typography, icons, empty states.</p></article>
<article><span>Layout</span><p>Grid, spacing tokens, hierarchy.</p></article>
</div></div></section>""" % (
    attrs(26, "Component family map", "ACT 3 · THE UI UNIVERSE",
          "Explain that components solve different interaction problems. Cards, lists, dividers, chips, dropdowns, sliders, date pickers, search, tabs, nav bars, app bars, dialogs, snackbars, progress, tooltips, icon buttons, badges, FABs must be represented in this family."),
    meta("MAP", "FAMILIES")
))
slides.append(phone(
    27, "One choice or many", "ACT 3 · THE UI UNIVERSE",
    "Arya is asked about her meditation goals. Can she choose one or multiple? Radio: single. Checkbox: multiple independent. Selection behaviour should match intent.",
    "assets/ui-choice-one.svg",
    "Teaching diagram · single versus multiple selection. Confirm the real Material 3 radio and checkbox in the Android kit.",
    "Arya is asked about her goals.",
    extra_html=choices([
        ("Radio · she may pick only one", False, 0),
        ("Checkbox · goals can stack", True, 20),
        ("Switch · goals are on or off as a bundle", False, 0),
    ]) + reveal("Radio: single choice. Checkbox: multiple independent choices. If the product wants one primary goal, radio. If several goals are valid, checkbox."),
    kicker="GAME 2 · 5 MIN"
))
slides.append(phone(
    28, "What about switches", "ACT 3 · THE UI UNIVERSE",
    "Arya wants to enable daily reminders. Switch for an immediate on/off setting. Component behaviour and user expectations.",
    "assets/mindspace/switch.svg",
    "Teaching diagram · confirm the Material 3 switch in the Android kit.",
    "Reminders: checkbox, radio, or switch?",
    extra_html=choices([
        ("Checkbox · a task she might complete", False, 0),
        ("Radio · yes or no as a pair of options", False, 0),
        ("Switch · on or off, takes effect now", True, 20),
    ]) + reveal("Switch for an immediate on/off setting. Radio is for choosing one of a set. Checkbox is for independent items."),
    better=True, kicker="SWITCH · 4 MIN"
))
slides.append(phone(
    29, "The input challenge", "ACT 3 · THE UI UNIVERSE",
    "Arya enters her mobile number. Default, focused, filled, error, disabled. What should the app communicate when the number is invalid? Helpful validation, clear error, recovery path.",
    "assets/mindspace/field-states.svg",
    "Teaching diagram of field states · find Default / Focused / Error in the Android kit.",
    "The number is invalid. What should she see?",
    extra_html=choices([
        ("A red field and no explanation", False, 0),
        ("Helpful error text and a way to retry", True, 20),
        ("A dialog that blocks the whole screen", False, 0),
    ]) + reveal("Helpful validation, clear error text, and a recovery path. Default waits. Focused listens. Invalid explains."),
    kicker="GAME 3 · 5 MIN"
))
slides.append(phone(
    30, "Choose the action", "ACT 3 · THE UI UNIVERSE",
    "Arya finishes a meditation session. Which action should be most prominent? Primary versus secondary.",
    "assets/laws/primary.svg",
    "Teaching diagram · one primary verb",
    "She finishes a session. What is the loudest button?",
    extra_html=choices([
        ("Filled primary: Done / continue", True, 20),
        ("Three equal outlined buttons", False, 0),
        ("Text button only, no filled action", False, 0),
    ]) + reveal("One filled primary. Outlined or text for secondary. Do not make Skip as loud as Continue."),
    better=True, kicker="GAME 4 · 4 MIN"
))
slides.append(phone(
    31, "Navigation detective", "ACT 3 · THE UI UNIVERSE",
    "Arya moves between Home, Discover, Journal and Profile. Bottom navigation is appropriate for a small set of top-level destinations.",
    "assets/mindspace/nav.svg",
    "Teaching diagram of four destinations · confirm Material bottom navigation in the Android kit.",
    "Four major destinations. Which pattern?",
    extra_html=choices([
        ("Navigation drawer for everything", False, 0),
        ("Tabs hidden under Discover", False, 0),
        ("Bottom navigation for the four", True, 20),
    ]) + reveal("Bottom navigation fits a small set of top-level destinations. Drawer is for more. Player and onboarding have no tabs."),
    kicker="NAV · 4 MIN"
))
slides.append(phone(
    32, "Feedback or interruption", "ACT 3 · THE UI UNIVERSE",
    "Progress for ongoing work. Snackbar for lightweight feedback. Dialog for an important decision requiring attention.",
    "assets/mindspace/profile-pair.svg",
    "Teaching diagram · confirm snackbar, dialog, and progress in the Android kit.",
    "She is about to delete her account.",
    extra_html=choices([
        ("Snackbar: Account deleted", False, 0),
        ("Progress spinner until it is gone", False, 0),
        ("Dialog: this needs a decision", True, 20),
    ]) + reveal("Progress while a session saves. Snackbar when a preference changes. Dialog for irreversible decisions. Never bury delete in a snackbar."),
    kicker="GAME 5 · 5 MIN"
))
slides.append(lesson(
    33, "The state challenge", "ACT 3 · THE UI UNIVERSE",
    "Is this the same component? Yes — default, pressed, focused, disabled. Teach variants versus interaction states.",
    "Is this the same component?",
    rules=[
        "Default — waiting.",
        "Pressed — the finger is down.",
        "Focused — keyboard or talkback is here.",
        "Disabled — the action is unavailable, and it must look unavailable.",
    ],
    kicker="STATES", right="VARIANTS ≠ STATES"
))
slides.append(pair(
    34, "Accessibility detective", "ACT 3 · THE UI UNIVERSE",
    "Which is more accessible and why? Contrast, readability, touch target, clear labels, colour-independent meaning.",
    ("assets/ui-contrast-weak.svg", "Weak contrast · teaching diagram", False),
    ("assets/ui-contrast-good.svg", "Readable contrast · teaching diagram", True),
    kicker="A11Y"
))
slides.append(lime(
    35, "Check scores again", "ACT 3 · THE UI UNIVERSE",
    "Check scores. Then Look first.",
    "Check scores.",
    kicker="QUIZ", right="THE BOARD"
))
GV_SHOTS = [
    ("assets/gv/01.png", "Call controls"),
    ("assets/gv/02.png", "Notification badges"),
    ("assets/gv/03.png", "Form layout"),
    ("assets/gv/04.png", "Categories"),
    ("assets/gv/05.png", "Photo contrast"),
    ("assets/gv/06.png", "Nav bar colour"),
    ("assets/gv/07.png", "Plans"),
    ("assets/gv/08.png", "Thumb zone"),
    ("assets/gv/09.png", "Progress"),
    ("assets/gv/10.png", "Name the miss"),
    ("assets/gv/11.png", "Text alignment"),
    ("assets/gv/12.png", "Name the miss"),
    ("assets/gv/13.png", "Inactive contrast"),
    ("assets/gv/14.png", "Name the miss"),
    ("assets/gv/16.png", "Hero and CTAs"),
    ("assets/gv/17.png", "Name the miss"),
    ("assets/gv/18.png", "Tab colours"),
    ("assets/gv/19.png", "Name the miss"),
    ("assets/gv/20.png", "Name the miss"),
]
slides.append(lime(
    147, "Look first", "ACT 3 · LOOK FIRST",
    "Nineteen same-shot comparisons. Ask what is wrong on the left. Then: does Arya use it.",
    "Look first.",
    "Nineteen shots. Same frame. Then we check.",
    kicker="LOOK FIRST", right="19 SHOTS"
))
for i, (src, cap) in enumerate(GV_SHOTS, 1):
    slides.append(
        '<section class="slide wide-see gv-shot" %s>%s'
        '<figure class="wide-frame"><img src="%s" alt="%s"></figure>'
        "</section>" % (
            attrs(147 + i, cap, "ACT 3 · LOOK FIRST",
                  "What is wrong on the left? Then next."),
            meta(f"{i:02d} / 19", "BAD · GOOD"),
            src, cap
        )
    )
slides.append(lime(
    168, "Ten rules", "ACT 4 · TEN RULES",
    "Ten rules. One example each. Then Hands on.",
    "Ten rules.",
    "One line. One example. Then we build.",
    kicker="BEFORE THE PROJECT", right="10 RULES"
))
PRINCIPLES = [
    (169, 1, "Simplicity", "One job on the screen.",
     '<p class="ui-prin-tiny">Mindspace</p><div class="ui-prin-chips"><i></i><i></i><i></i><i></i><i></i><i></i></div><b class="ui-prin-banner">Offer</b><b class="ui-prin-banner">Tip</b><span class="ui-prin-btn">Start</span><span class="ui-prin-btn">Browse</span><span class="ui-prin-btn">Join</span>',
     '<p class="ui-prin-kicker">Tonight</p><h3>Sleep</h3><span class="ui-prin-btn is-fill">Start</span>'),
    (170, 2, "Consistency", "Same control. Same place.",
     '<div class="ui-prin-bar"><b>✕</b><span>Close</span></div><div class="ui-prin-bar is-mid"><span>Back</span></div><div class="ui-prin-bar is-end"><b>Done</b></div>',
     '<div class="ui-prin-bar is-same"><b>←</b><span>Home</span></div><div class="ui-prin-bar is-same"><b>←</b><span>Sleep</span></div><div class="ui-prin-bar is-same"><b>←</b><span>Player</span></div>'),
    (171, 3, "Hierarchy", "Arya sees the next tap first.",
     '<p class="ui-prin-flat">Sleep</p><p class="ui-prin-flat">10 min</p><p class="ui-prin-flat">Start</p><p class="ui-prin-flat">4.8</p>',
     '<h3>Sleep</h3><p class="ui-prin-muted">10 minutes</p><span class="ui-prin-btn is-fill">Start</span>'),
    (172, 4, "Feedback", "Arya taps. The UI answers.",
     '<p class="ui-prin-msg">See you tomorrow.</p><span class="ui-prin-btn">Send</span><p class="ui-prin-ghost">…</p>',
     '<p class="ui-prin-msg">See you tomorrow.</p><p class="ui-prin-tick">Sent</p><p class="ui-prin-tick">Delivered</p><p class="ui-prin-tick is-read">Read</p>'),
    (173, 5, "Access", "If Arya can’t read it, it is not there.",
     '<p class="ui-prin-wash">Start session</p><p class="ui-prin-wash">10 min guided</p>',
     '<h3>Start session</h3><p class="ui-prin-muted">10 min guided</p><span class="ui-prin-btn is-fill">Play</span>'),
    (174, 6, "Clarity", "Words Arya already knows.",
     '<h3 class="ui-prin-jargon">Initiate nocturnal protocol</h3><span class="ui-prin-btn">Confirm execution</span>',
     '<h3>Start sleep session</h3><span class="ui-prin-btn is-fill">Start</span>'),
    (175, 7, "Control", "Arya can leave. Arya can undo.",
     '<p class="ui-prin-kicker">Playing</p><h3>Please wait</h3><p class="ui-prin-ghost">Locked</p>',
     '<p class="ui-prin-kicker">Playing</p><h3>Sleep</h3><div class="ui-prin-controls"><b>−10</b><b class="is-fill">❚❚</b><b>+10</b></div>'),
    (176, 8, "Recover", "Stop the miss. Then help Arya fix it.",
     '<p class="ui-prin-err">ERROR 422</p><p class="ui-prin-err">INVALID PAYLOAD</p>',
     '<p class="ui-prin-warn">That email needs an @</p><span class="ui-prin-field">me</span><span class="ui-prin-btn is-fill">Fix it</span>'),
    (177, 9, "Quiet", "Quiet. Not decoration.",
     '<p class="ui-prin-loud">MIND★SPACE</p><p class="ui-prin-loud is-alt">Breathe!!!</p><span class="ui-prin-btn is-hot">GO</span><span class="ui-prin-btn is-alt">NOW</span>',
     '<p class="ui-prin-kicker">Mindspace</p><h3>Breathe</h3><span class="ui-prin-btn is-fill">Start</span>'),
    (178, 10, "Fit", "Phone first. Still works bigger.",
     '<div class="ui-prin-squeeze"><i>Rec</i><i>Sleep</i><i>Focus</i></div>',
     '<b class="ui-prin-stack">Recent</b><b class="ui-prin-stack">Sleep</b><b class="ui-prin-stack">Focus</b>'),
]
for n, i, name, line, bad, good in PRINCIPLES:
    slides.append(principle(n, i, name, line, bad, good))
slides.append(lime(
    36, "Does Arya use it", "ACT 3 · THE UI UNIVERSE",
    "If they cannot say when Arya uses it, they picked the wrong piece. Then the brief.",
    "Does Arya use it.",
    "If Arya never uses it, drop it.",
    kicker="CHECKPOINT", right="LEVEL 02"
))

# ACT 4
slides.append(lime(
    37, "The brief is live", "ACT 4 · MISSION BRIEFING",
    "Do not recap what they learned. Open the brief. Eight missions. One Arya.",
    "The brief is live.",
    "Eight missions. One Arya. The file is shared.",
    timer="15", kicker="ACT 4", right="01:30–01:45"
))
slides.append(ask(
    38, "The problem statement", "ACT 4 · MISSION BRIEFING",
    "Keep it short. She has to last a week. The rest is their job.",
    "How might we keep Arya coming back for a week?"
))
slides.append(cards(
    39, "Pick a desk. Keep Arya.", "ACT 4 · MISSION BRIEFING",
    "Eight teams. Eight parts of Arya's experience. One product. Open Missions (B) for the full briefs.",
    "Pick a desk. Keep Arya.",
    [
        ("A", "Getting started", "Help Arya begin without a novel of fields."),
        ("B", "Personalisation", "Understand Arya’s needs in everyday language."),
        ("C", "Home", "Guide the next action in five minutes."),
        ("D", "Discover", "Find content without specialist words."),
        ("E", "Meditation", "Make the session effortless."),
        ("F", "Goals", "Build a habit without guilt."),
        ("G", "Journal", "Reflect without another chore."),
        ("H", "Profile", "Control Arya can find."),
    ],
    kicker="TEAMS"
))
slides.append("""<section class="slide lesson-plan" %s>%s
<div class="lp-body"><div class="lp-heading"><h2>Arya has to survive this map.</h2><p class="lp-subtitle">Not a rigid sequence. Journal and goals can open from Home. Find the real entry, the skip, and who you hand Arya to.</p></div>
<div class="s5-flow">
<b>Registration</b><i>→</i><b>Personalisation</b><i>→</i><b>Home</b><i>→</i><b>Discover</b><i>→</i><b>Meditation</b><i>→</i><b>Goals</b><i>→</i><b>Journal</b><i>→</i><b>Profile</b>
</div>
<p class="lp-subtitle" style="margin-top:1.2rem">Ask: Where does Arya enter? Where next? Can Arya return? What if Arya skips?</p>
</div></section>""" % (
    attrs(40, "The product journey", "ACT 4 · MISSION BRIEFING",
          "Where does Arya enter? Where does she go next? Can she return? What happens if she skips something?"),
    meta("MAP", "NOT A RIGID SEQUENCE")
))
slides.append(process(
    41, "The research rule", "ACT 4 · MISSION BRIEFING",
    "You are not receiving a screen to copy. You are receiving a person to understand. No screen before the problem.",
    "No screen before the problem.",
    ["Insight", "Opportunity", "Journey", "Sketch", "Interface"],
    kicker="PROCESS"
))
slides.append(wide(
    42, "Design system is the constraint", "ACT 4 · MISSION BRIEFING",
    "Don't invent a new design language. Use Mindspace: colour, type, buttons, cards, inputs, navigation, icons, spacing. Creativity is the experience, not eight visual languages.",
    "assets/mindspace/stylesheet.png",
    "Mindspace type and colour. Duplicate this file and stay there.",
    href=KIT_MIND,
    alt="Mindspace stylesheet: Poppins type scale and colour tokens."
))
slides.append("""<section class="slide approach-intro jtbd-card" %s>%s
<div class="approach-intro-content">
<h2>The job.</h2>
<ol class="jtbd">
<li><p class="jtbd-line"><b>When</b><i></i></p><p class="jtbd-ex">the corridor is loud</p></li>
<li><p class="jtbd-line"><b>I want to</b><i></i></p><p class="jtbd-ex">ten quiet minutes</p></li>
<li><p class="jtbd-line"><b>so I can</b><i></i></p><p class="jtbd-ex">sleep</p></li>
</ol>
</div></section>""" % (
    attrs(145, "The job", "ACT 4 · MISSION BRIEFING",
          "Write one job on paper for their moment. Then sit. No screen before the problem."),
    meta("JOB", "PAPER")
))
slides.append(lesson(
    43, "Team deliverables", "ACT 4 · MISSION BRIEFING",
    "Every team must deliver all of this by the first launch.",
    "On the desk at first launch",
    rules=[
        "The sentence: who, task, barrier.",
        "Know / guess / find out — labelled.",
        "One How Might We.",
        "A path with a skip and a dead end.",
        "Two sketches, not one.",
        "Screens from the kit, not a new brand.",
        "Two states that are not the happy path.",
        "Play: the tap that matters lands.",
        "One reason, said out loud.",
    ],
    kicker="DELIVER", right="FIRST LAUNCH"
))
slides.append(lesson(
    44, "Rules of collaboration", "ACT 4 · MISSION BRIEFING",
    "One product. Shared language. Shared responsibility.",
    "If two desks disagree, Arya loses.",
    rules=[
        "One shared file, or approved team pages.",
        "Name frames so the next desk can find them.",
        "Do not restyle the masters.",
        "Steal styles. Do not invent a third look.",
        "Write the handoff: who you take Arya from, who you give Arya to.",
        "Same Arya. No extra hero.",
        "Talk to the desks on either side of you.",
    ],
    kicker="COLLAB", right="NON-NEGOTIABLE"
))

YT_HANDS = "https://www.youtube.com/watch?v=eeGVBhZURUI"
slides.append("""<section class="slide hands-all" %s>%s
<div class="hands-all-body">
<h2>Hands on. All eight.</h2>
<p class="hands-all-video">Figma Interactive Components For Beginners</p>
<a class="hands-all-play" data-yt-play href="%s" target="_blank" rel="noopener">Play</a>
<p class="hands-all-lede">Follow along. Same steps. Then we split.</p>
</div></section>""" % (
    attrs(146, "Hands on. All eight.", "ACT 4 · MISSION BRIEFING",
          "All eight desks. Same video. Same file. Follow along, then split to A–H."),
    meta("ALL EIGHT", "THEN SPLIT"),
    YT_HANDS
))
slides.append(desk_wall(
    179, "Eight desks", "ACT 4 · MISSION BRIEFING",
    "Read A to H out loud. Point at the room. Then move.",
    [
        ("A", "Getting started", "Begin without a novel of fields."),
        ("B", "Personalisation", "Arya’s words. Not jargon."),
        ("C", "Home", "One next tap. Five minutes."),
        ("D", "Discover", "Find sleep. Not a term."),
        ("E", "Meditation", "Play. Close Arya’s eyes."),
        ("F", "Goals", "Miss a day. No shame."),
        ("G", "Journal", "A mood is enough."),
        ("H", "Profile", "Find the reminder."),
    ],
))
slides.append(studio(
    45, "Find your desk", "ACT 4 · MISSION BRIEFING",
    "Reveal desks A–H. Open Missions (B). Move. Then sit.",
    "Find your desk.",
    "",
    "4 min", "4", kicker="MOVE"
))

# ACT 5
slides.append(level(
    46, "The Product Thinkers", "ACT 5 · PRODUCT THINKERS",
    "Paper first. Figma after the checkpoint.",
    3, "The Product Thinkers.",
    "Paper first. Figma after the checkpoint.",
    timer="60", right="01:45–02:45"
))
slides.append(studio(
    47, "Paper first", "ACT 5 · PRODUCT THINKERS",
    "Need. Path. Two sketches. Then the checkpoint.",
    "Need. Path. Two sketches.",
    "",
    "30 min", "30", kicker="PAPER"
))
slides.append(studio(
    48, "Paper checkpoint", "ACT 5 · PRODUCT THINKERS",
    "Stop. Show. Explain. Problem, flow, two sketches. Score 10 / 10 / 10.",
    "Stop. Show. Explain.",
    "Problem. Flow. Two sketches.",
    "10 min", "10", kicker="CHECKPOINT"
))

# ACT 6
slides.append(level(
    49, "The Interface Builders", "ACT 6 · INTERFACE BUILDERS",
    "Pixels. Arya is still waiting.",
    4, "The Interface Builders.",
    "Pixels. Arya is still waiting.",
    timer="45", right="03:00–03:45"
))
slides.append(studio(
    50, "Build it", "ACT 6 · INTERFACE BUILDERS",
    "One file. Shared product page. Team pages A–H. Do not wreck the library.",
    "Build it.",
    "Shared page. Team pages A–H. Do not wreck the library.",
    "30 min", "30", kicker="FIGMA"
))

# ACT 7
slides.append(lime(
    51, "Walk Arya", "ACT 7 · ASSEMBLY",
    "Walk Arya from A to H. If Arya gets lost, the seam is theirs.",
    "Walk Arya.",
    timer="15", kicker="ACT 7", right="03:45–04:00"
))

# ACT 9
slides.append(studio(
    52, "Critique", "ACT 9 · CRITIQUE",
    "Name the miss. Protect the person. Keep / fix / remove / improve. Open Score.",
    "Break it before Arya does.",
    "",
    "10 min", "10", kicker="CRITIQUE"
))

# ACT 10
slides.append(level(
    53, "The Design Evolution", "ACT 10 · DESIGN EVOLUTION",
    "Arya already used v1. Fix what Arya hit. Do not add a fifth screen.",
    5, "The Design Evolution.",
    "",
    timer="60", right="04:30–05:30"
))
slides.append(studio(
    54, "Improve it", "ACT 10 · DESIGN EVOLUTION",
    "One improve beat. Kill a step. Fix the tap. No fifth screen.",
    "Make v1 die.",
    "Kill a step. Fix the tap. No fifth screen.",
    "30 min", "30", kicker="IMPROVE"
))
slides.append(studio(
    55, "Swap test", "ACT 10 · DESIGN EVOLUTION",
    "Swap. Stay quiet. Give Arya's task. Watch where they hesitate.",
    "Swap. Stay quiet.",
    "Give Arya's task. Watch where they hesitate.",
    "10 min", "10", kicker="TEST"
))

# ACT 11 — eight on-stage cards, then one prototype
STAGE = [
    (56, "A", "Getting started."),
    (57, "B", "Personalisation."),
    (58, "C", "Home."),
    (59, "D", "Discover."),
    (60, "E", "Meditation."),
    (61, "F", "Goals."),
    (62, "G", "Journal."),
    (63, "H", "Profile."),
]
for n, letter, journey in STAGE:
    slides.append(lime(
        n, f"Team {letter} · {journey[:-1]}", "ACT 11 · SHOWCASE",
        f"Leave this up while Team {letter} talks. Two minutes. Then sit.",
        journey,
        timer="2", kicker=f"TEAM {letter}", right="2 MIN"
    ))
slides.append(lime(
    64, "One prototype", "ACT 11 · SHOWCASE",
    "Different members from A–H walk one working product. Play the live file. No spoken tour.",
    "One prototype.",
    "A through H. One Arya. Play it. No spoken tour.",
    timer="10", kicker="FINALE", right="ONE FILE"
))

# ACT 12
slides.append(lime(
    65, "Close", "ACT 12 · CLOSING",
    "Hold. Eight desks. One Arya. Thank them. Then dismiss.",
    "You kept Arya in the product.",
    "Eight desks. One Arya. Thank you.",
    kicker="SESSION 05", right="CLOSE"
))

assert len(slides) == 158, len(slides)
# only first slide should have is-active in cover(); others shouldn't. Fix if any extra.
# cover() already handles n==1.

TEAMS = [
    ("A Getting started", "Not started"),
    ("B Personalisation", "Not started"),
    ("C Home", "Not started"),
    ("D Discover", "Not started"),
    ("E Meditation", "Not started"),
    ("F Goals", "Not started"),
    ("G Journal", "Not started"),
    ("H Profile", "Not started"),
]

MISSIONS = [
    ("A · Getting started", "Downloaded for the first time.",
     "Too many fields create friction. She needs the next step to feel safe.",
     "I just want to try meditation. Why so many questions?",
     "Help Arya get started without feeling overwhelmed?",
     "Welcome, registration, mobile, OTP, success. Validation, privacy, errors, progress."),
    ("B · Personalisation", "Wants relevance, does not know the jargon.",
     "Everyday language. Too many questions feel like an interrogation. Preferences must be editable later.",
     "I don't know what kind of meditation I need. I just want to feel less stressed.",
     "Understand Arya's needs without a lengthy questionnaire?",
     "Intro, goals, experience, duration, reminders, completion. Radio, checkbox, chips, switch, optional."),
    ("C · Home", "Opens before work. Five minutes.",
     "She wants to continue quickly. Too many options delay the decision. Progress should encourage.",
     "Just tell me what I can do today.",
     "Make Arya's next action immediately understandable?",
     "Dashboard, daily recommendation, continue, inspiration, quick actions. Hierarchy, cards, empty."),
    ("D · Discover", "Wants help sleeping. Does not know the search term.",
     "She may search by mood. Duration matters. Browsing still needs guidance.",
     "I don't know what to search for. I just want something to help me sleep.",
     "Help Arya find content even when she doesn't know the name?",
     "Explore, categories, search, results, filters, details. Chips, IA, empty results."),
    ("E · Meditation", "Ten-minute guided session selected.",
     "Minimal distraction. Reliable controls. Interruptions happen. Completion should be obvious.",
     "I just want to press play, close my eyes and listen.",
     "Make the meditation experience effortless and dependable?",
     "Details, intro, player, pause, resume, completion, feedback."),
    ("F · Goals", "Meditated four days. Missed yesterday.",
     "Missed days hurt motivation. Unrealistic goals shame her. Progress should encourage, not scold.",
     "I missed one day. Does that mean I've failed?",
     "Help Arya build a habit without making her feel guilty?",
     "Goal setup, daily goal, progress, challenges, achievements, missed-day recovery."),
    ("G · Journal", "Session done. Wants to reflect.",
     "She may not have words. Mood chips may be enough. Reflections feel private.",
     "Sometimes I don't know what I'm feeling. I just want a simple way to capture it.",
     "Help Arya reflect without making journaling another task?",
     "Landing, mood, prompts, writing, save, past entries. Privacy, skip, empty."),
    ("H · Profile", "Wants to change reminder time.",
     "Settings are hard to find. Controls must be predictable. Account actions need clarity.",
     "I changed something when I joined. I can't remember where.",
     "Give Arya confidence and control over her experience?",
     "Profile, details, preferences, notifications, account. Switches, lists, confirmations."),
]

chips = "".join(
    f'<button type="button" class="team-chip" data-status="idle"><strong>{name}</strong><span>{status}</span></button>'
    for name, status in TEAMS
)
mission_html = "".join(
    f'<article><span>{title}</span><p><em>{moment}</em> {hyp} Voice: “{voice}” HMW: {hmw} Build: {build}</p></article>'
    for title, moment, hyp, voice, hmw, build in MISSIONS
)
score_rows = "".join(
    f'<button type="button" data-score-team="{letter}"><b>Team {letter}</b><span class="pts">0</span></button>'
    for letter in "ABCDEFGH"
)

DROP = {2, 3, 4, 5, 6, 11, 15, 16, 17, 18, 19, 20, 21, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 39, 54, 55, 110, 123, 219}
slides = [
    s for s in slides
    if int(re.search(r'data-slide="(\d+)"', s).group(1)) not in DROP
]
slides = [
    re.sub(r'data-slide="\d+"', f'data-slide="{i:02d}"', s, count=1)
    for i, s in enumerate(slides, 1)
]
body = "".join(slides)

html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#101116">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <title>The Mindspace Design Lab: Session 5</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="deck.css?v=23">
  <link rel="stylesheet" href="deck-v2.css?v=12">
  <link rel="stylesheet" href="mobile.css?v=9">
  <link rel="stylesheet" href="session-5.css?v=53">
</head>
<body class="deck-v2 s5" data-deck-title="Session 5 · The Mindspace Design Lab">
  <div class="hud" aria-label="Facilitator">
    <div class="hud-act" id="hud-act">SESSION 05</div>
    <button type="button" class="hud-timer" id="hud-timer" title="Click start/pause. Double-click reset">Timer</button>
    <button type="button" id="hud-notes">Notes</button>
    <button type="button" id="hud-board">Missions</button>
    <button type="button" id="hud-score">Score</button>
    <button type="button" id="hud-reveal">Reveal</button>
    <button type="button" id="hud-twist">Twist</button>
    <button type="button" id="hud-plus">+ pts</button>
    <button type="button" id="hud-minus">− pts</button>
    <span class="hud-act" id="room-score">Room 0</span>
  </div>
  <aside class="notes-panel" id="notes-panel">
    <h3>Speaker</h3>
    <p id="notes-body"></p>
  </aside>
  <aside class="teams-panel" id="teams-panel">
    <h3>Eight desks · click to advance status</h3>
    <div class="team-grid">{chips}</div>
    <div class="s5-grid two" style="margin-top:1rem">{mission_html}</div>
  </aside>
  <aside class="score-panel" id="score-panel">
    <h3>Scoreboard · click a team, then + / −</h3>
    <div class="score-rows">{score_rows}</div>
    <p class="lp-subtitle" style="margin-top:.8rem">3 identify · 8 decision · 8 reasoning · 6 issue · 10 improvement · 6 deliverable · 6 collaboration · 8 observation · 10 iteration. Never for finishing first.</p>
  </aside>
  <aside class="twist-panel" id="twist-panel">
    <h3>Surprise mechanics · inside existing sprint time</h3>
    <div class="twist-list">
      <button type="button" data-twist="The twist · two minutes" data-detail="Arya has only two minutes. Strip the journey to one action."><strong>Two minutes</strong><span>Arya has only two minutes available.</span></button>
      <button type="button" data-twist="The twist · offline" data-detail="Arya has lost internet. What still works?"><strong>No internet</strong><span>Arya has lost connectivity.</span></button>
      <button type="button" data-twist="The twist · skip" data-detail="Arya skips personalisation. Can Home still help?"><strong>She skips</strong><span>Arya skips personalisation.</span></button>
      <button type="button" data-twist="The twist · OTP" data-detail="Invalid OTP. Show recovery, not a dead end."><strong>Invalid OTP</strong><span>The code is wrong.</span></button>
      <button type="button" data-twist="The twist · reminder" data-detail="She changes reminder time. Can she find it?"><strong>Reminder change</strong><span>She edits a preference.</span></button>
      <button type="button" data-twist="User interruption" data-detail="Phone call during meditation. What happens when she returns?"><strong>Phone call</strong><span>Interrupted mid-session.</span></button>
      <button type="button" data-twist="Accessibility check" data-detail="Name the contrast, target, or label failure and fix it."><strong>Accessibility</strong><span>Find and fix one access issue.</span></button>
      <button type="button" data-twist="Design rescue" data-detail="One team asks another for feedback. Reward useful help."><strong>Design rescue</strong><span>Cross-team help, then points.</span></button>
      <button type="button" data-twist="Design director's pick" data-detail="Bonus for a particularly thoughtful decision. Click the team, then + pts."><strong>Director's pick</strong><span>Bonus for reasoning, not polish.</span></button>
    </div>
  </aside>
  <div id="twist-banner" hidden>
    <p><strong></strong> <span></span></p>
    <button type="button" id="twist-dismiss">Clear</button>
  </div>

  <main class="deck" aria-live="polite">
    {body}
  </main>

  <aside class="controls" aria-label="Slide navigation">
    <button class="prev" aria-label="Previous slide">←</button>
    <span class="counter">01 / {len(slides):02d}</span>
    <button class="next" aria-label="Next slide">→</button>
  </aside>
  <div class="progress"><span></span></div>
  <script src="deck.js"></script>
  <script src="session-5.js?v=14"></script>
</body>
</html>
"""

out = Path(__file__).with_name("session-5.html")
out.write_text(html, encoding="utf-8")
print(f"wrote {out} slides={len(slides)} bytes={out.stat().st_size}")
