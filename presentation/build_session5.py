#!/usr/bin/env python3
"""Generate session-5.html from the ChatGPT production blueprint."""
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

def studio(n, title, act, notes, h2, p, time_label, timer, kicker="NOW"):
    body = meta(kicker, time_label.upper())
    num, unit = time_label.split(" ", 1) if " " in time_label else (time_label, "")
    body += f'<div class="time-box" aria-hidden="true"><strong>{num}</strong><span>{unit}</span></div>'
    body += f"<div><h2>{h2}</h2><p>{p}</p></div>"
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

def phone(n, title, act, notes, src, cap, h2, extra_html="", better=False, kicker="SEE", timer="", right=""):
    cls = "is-better" if better else ""
    body = meta(kicker, right)
    body += f'<figure class="phone-frame {cls}"><img src="{src}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'
    body += f'<div class="phone-copy"><h2>{h2}</h2>{extra_html}</div>'
    return f'<section class="slide phone-see" {attrs(n, title, act, notes, timer)}>{body}</section>'

def pair(n, title, act, notes, left, right, kicker="SEE"):
    body = meta(kicker, "")
    body += '<div class="pair-row">'
    for src, cap, better in (left, right):
        cls = "is-better" if better else ""
        body += f'<figure class="phone-frame {cls}"><img src="{src}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'
    body += "</div>"
    return f'<section class="slide phone-pair" {attrs(n, title, act, notes)}>{body}</section>'

def wide(n, title, act, notes, src, cap, kicker="SEE"):
    body = meta(kicker, "")
    body += f'<figure class="wide-frame"><img src="{src}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'
    return f'<section class="slide wide-see" {attrs(n, title, act, notes)}>{body}</section>'

def quote(n, title, act, notes, text, detail=""):
    body = meta(act, "")
    body += f'<div class="quote-wrap"><blockquote>{text}</blockquote>'
    if detail:
        body += f'<p class="quote-detail">{detail}</p>'
    body += "</div>"
    return f'<section class="slide quote-slide" {attrs(n, title, act, notes)}>{body}</section>'

def ask(n, title, act, notes, question, kicker="ASK"):
    body = meta(kicker, "")
    body += f'<div class="ux-example-body"><p class="ux-example-question">{question}</p></div>'
    return f'<section class="slide ux-example ux-example-ask ux-example-question-only" {attrs(n, title, act, notes)}>{body}</section>'

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
    body += f'<div class="lp-body"><div class="lp-heading"><h2>{h2}</h2></div><div class="s5-process">'
    for step in steps:
        body += f"<b>{step}</b>"
    body += "</div></div>"
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
    "Welcome them. Do not explain the day. The next slide hires them.",
    "The<br>Mindspace<br>Design Lab.",
    right="8 TEAMS · 6 HOURS",
    lede="She downloaded it this morning."
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
        "Talk to the desk that hands her to you.",
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
        ("She will", ["Open the app in a corridor.", "Give you minutes, not an hour.", "Quit if the first screen lectures."]),
        ("She will not", ["Learn specialist vocabulary to start.", "Fill a novel before she tries.", "Forgive streak shame for one missed day."]),
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
    "She did not download a player.",
    "She wants to sleep. Feel calmer. Last a week.",
    cols=[
        ("If this is all you ship", ["A player.", "A streak.", "A library.", "A settings page."]),
        ("If she actually stays", ["She sleeps.", "She feels calmer.", "She can focus.", "She comes back tomorrow.", "She can find the reminder."]),
    ],
    kicker="STAKES", right="ASK THE ROOM"
))
# 10
slides.append(lesson(
    10, "Research behind the challenge", "ACT 1 · OPENING",
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
# 11
slides.append(process(
    11, "Warm-up", "ACT 1 · OPENING",
    "Do not lecture a process. Tell them the warm-up, then scoring starts.",
    "Warm-up. Then we keep score.",
    ["Frame", "Align", "Reuse", "Adapt", "Name it", "Defend it"],
    kicker="NEXT"
))

# ACT 2
slides.append(lime(
    12, "Level 1 unlocked", "ACT 2 · THE PLAYGROUND",
    "Do not say 'get comfortable with Figma.' Give them a screen and a clock.",
    "Level 01<br>The Playground.",
    "Ten minutes. Recreate one screen. No screenshots.",
    timer="30", kicker="LEVEL 01", right="00:15–00:45"
))
slides.append(phone(
    13, "Recreate this screen", "ACT 2 · THE PLAYGROUND",
    "One simple mobile welcome: heading, supporting text, illustration, primary button, secondary action. Open Figma and recreate it. Ten minutes.",
    "assets/mindspace/welcome.svg",
    "Teaching diagram · heading, supporting text, illustration, primary, secondary. Recreate this, do not screenshot it.",
    "Recreate this screen.",
    extra_html="<p>Heading. Supporting text. Illustration. Primary button. Secondary action. Ten minutes.</p>",
    better=True, kicker="MISSION · 10 MIN", timer="10", right="LEVEL 01"
))
slides.append(wide(
    14, "Discover your workspace", "ACT 2 · THE PLAYGROUND",
    "Explain where things are, not every feature. Canvas, layers, toolbar, properties, pages.",
    "assets/figma/three-parts.svg",
    "Teaching diagram of Figma workspace regions · not a live file screenshot."
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
    "Demonstrate: create a component, show how instances update. Reusability and design systems.",
    "What if you need 20 identical buttons?",
    subtitle="Individual copies versus a reusable component.",
    rules=[
        "Draw one primary button.",
        "Make it a component.",
        "Place three instances.",
        "Change the master. Watch the copies follow.",
    ],
    kicker="COMPONENT", right="LIVE DEMO"
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
slides.append(lime(
    22, "Level 2 unlocked", "ACT 3 · THE UI UNIVERSE",
    "Scoring starts. Rapid challenges. Do not lecture every widget.",
    "Level 02<br>The UI Universe.",
    "See it. Pick it. Defend it. Points if the room believes you.",
    timer="45", kicker="LEVEL 02", right="00:45–01:30"
))
slides.append(wide(
    23, "Material Design 3", "ACT 3 · THE UI UNIVERSE",
    "A design system is more than a collection of components. Components, variants, properties, tokens, states, consistency. Open the Android UI Kit live.",
    "assets/figma-kits/android-thumb-view.png",
    "Connected kit cover · Android UI Kit / Material. Open the live file in class."
))
slides.append(lesson(
    24, "Game rules", "ACT 3 · THE UI UNIVERSE",
    "See it. Understand it. Choose it. Defend it. Do not award points for finishing first.",
    "How you score.",
    grades=[
        ("10", "Correct identification"),
        ("20", "Correct component choice"),
        ("20", "Strong reasoning"),
        ("15", "Spotting a usability issue"),
        ("25", "Excellent improvement"),
    ],
    kicker="SCORING", right="LEVEL 02"
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
slides.append("""<section class="slide lesson-plan" %s>%s
<div class="lp-body"><div class="lp-heading"><h2>No winner yet.</h2><p class="lp-subtitle">Read the board. Strongest defence. Best catch. Do not crown anyone. Click a team, then + pts.</p></div>
<p class="lp-subtitle">N notes · B missions · S score · R reveal · T twist · + / − points.</p>
</div></section>""" % (
    attrs(35, "Scoreboard", "ACT 3 · THE UI UNIVERSE", "Open the scoreboard. Celebrate reasoning, not speed."),
    meta("SCORE", "NO WINNER YET")
))
slides.append(lime(
    36, "Wrong piece", "ACT 3 · THE UI UNIVERSE",
    "If they cannot say when Arya uses it, they picked the wrong piece. Then the brief.",
    "When does she use it?",
    "If you cannot say, you picked the wrong piece.",
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
    "How might we keep her coming back for a week?"
))
slides.append(cards(
    39, "Your eight missions", "ACT 4 · MISSION BRIEFING",
    "Eight teams. Eight parts of Arya's experience. One product. Open Missions (B) for the full briefs.",
    "Pick a desk. Keep her alive until four.",
    [
        ("A", "Getting started", "Help Arya begin without a novel of fields."),
        ("B", "Personalisation", "Understand her needs in everyday language."),
        ("C", "Home", "Guide the next action in five minutes."),
        ("D", "Discover", "Find content without specialist words."),
        ("E", "Meditation", "Make the session effortless."),
        ("F", "Goals", "Build a habit without guilt."),
        ("G", "Journal", "Reflect without another chore."),
        ("H", "Profile", "Give her control she can find."),
    ],
    kicker="TEAMS"
))
slides.append("""<section class="slide lesson-plan" %s>%s
<div class="lp-body"><div class="lp-heading"><h2>She has to survive this map.</h2><p class="lp-subtitle">Not a rigid sequence. Journal and goals can open from Home. Find the real entry, the skip, and who you hand her to.</p></div>
<div class="s5-flow">
<b>Registration</b><i>→</i><b>Personalisation</b><i>→</i><b>Home</b><i>→</i><b>Discover</b><i>→</i><b>Meditation</b><i>→</i><b>Goals</b><i>→</i><b>Journal</b><i>→</i><b>Profile</b>
</div>
<p class="lp-subtitle" style="margin-top:1.2rem">Ask: Where does Arya enter? Where next? Can she return? What if she skips?</p>
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
    kicker="RULE"
))
slides.append(wide(
    42, "Design system is the constraint", "ACT 4 · MISSION BRIEFING",
    "Don't invent a new design language. Use Mindspace: colour, type, buttons, cards, inputs, navigation, icons, spacing. Creativity is the experience, not eight visual languages.",
    "assets/figma-kits/meditation-thumb-view.png",
    f"Mindspace look comes from the Meditation kit. Duplicate <a class='figma-link' href='{KIT_MIND}'>this file</a> and stay there."
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
        "Write the handoff: who you take her from, who you give her to.",
        "Same Arya. No extra hero.",
        "Talk to the desks on either side of you.",
    ],
    kicker="COLLAB", right="NON-NEGOTIABLE"
))
slides.append(studio(
    45, "Team assignment", "ACT 4 · MISSION BRIEFING",
    "Reveal teams. Open Missions (B) for research, situation, challenge, success. Move into groups.",
    "Find your desk.",
    "Read her moment before you touch Figma. If you skip this, you will decorate.",
    "4 min", "4", kicker="MOVE"
))

# ACT 5
slides.append(lime(
    46, "The mission begins", "ACT 5 · PRODUCT THINKERS",
    "Paper first. Figma after the checkpoint. Do not say 'understand before you create.'",
    "Level 03<br>The Product Thinkers.",
    "Paper first. Figma after the checkpoint.",
    timer="60", kicker="LEVEL 03", right="01:45–02:45"
))
slides.append(studio(
    47, "Research mission", "ACT 5 · PRODUCT THINKERS",
    "Circle the one need that would make the rest of the day fail.",
    "Circle the one need that would sink the day.",
    "Read the mission card. If you ignore this one, the rest of your screens are decoration.",
    "5 min", "5", kicker="RESEARCH"
))
slides.append(lesson(
    48, "Evidence from assumptions", "ACT 5 · PRODUCT THINKERS",
    "Put the assigned research insight into three categories. Ask whether they are treating workshop hypotheses as verified facts.",
    "What we know / assume / need to learn.",
    cols=[
        ("Watch for", ["Treating the brief as interview proof.", "Designing a screen to justify an assumption."]),
        ("Do this", ["Park unknowns on the third column.", "Say hypothesis out loud before you draw."]),
    ],
    kicker="5 MIN", right="FACILITATE", timer="5"
))
slides.append(lesson(
    49, "The opportunity question", "ACT 5 · PRODUCT THINKERS",
    "Write one specific How Might We. Examples on screen.",
    "How might we…?",
    subtitle="One specific question. Five minutes.",
    cols=[
        ("Examples", ["Help Arya get started without feeling overwhelmed?", "Help Arya find a meditation that fits her mood?", "Help Arya stay consistent without feeling guilty?"]),
        ("Test", ["Would Arya recognise herself in this sentence?", "Can you sketch two answers to it?"]),
    ],
    kicker="HMW", right="5 MIN", timer="5"
))
slides.append(studio(
    50, "Map the journey", "ACT 5 · PRODUCT THINKERS",
    "START → ACTION → DECISION → OUTCOME. Draw the complete journey before designing screens.",
    "Start → action → decision → outcome.",
    "Draw the whole path, including the skip and the dead end, before Figma.",
    "10 min", "10", kicker="MAP"
))
slides.append(studio(
    51, "Sketch before Figma", "ACT 5 · PRODUCT THINKERS",
    "Ideas first. Pixels later. Sketch two alternative approaches.",
    "Two sketches. Then you may open Figma.",
    "If you only have one idea, you do not have a choice yet.",
    "15 min", "15", kicker="SKETCH"
))
slides.append(lesson(
    52, "Choose your direction", "ACT 5 · PRODUCT THINKERS",
    "Compare alternatives using user value, simplicity, feasibility, consistency, accessibility.",
    "Which idea best solves Arya's problem?",
    grades=[
        ("01", "User value"),
        ("02", "Simplicity"),
        ("03", "Feasibility"),
        ("04", "Consistency + access"),
    ],
    kicker="DECIDE", right="5 MIN", timer="5"
))
slides.append(studio(
    53, "Design system inspection", "ACT 5 · PRODUCT THINKERS",
    "Don't reinvent. Discover what already exists. Find required components in the Mindspace library.",
    "Steal from the kit.",
    "Ten minutes. Write the names you will actually use. If you are drawing a new purple, you have left the team.",
    "10 min", "10", kicker="KIT"
))
slides.append(studio(
    54, "Sprint 1 checkpoint", "ACT 5 · PRODUCT THINKERS",
    "Stop. Show. Explain. Problem, flow, sketches, component choices. Scoring: 10 problem, 10 flow, 10 reasoning.",
    "Stop. Show. Explain.",
    "Problem. Proposed flow. Sketches. Component choices. Ten points each for clarity, logic, reasoning.",
    "10 min", "10", kicker="CHECKPOINT"
))

# ACT 6
slides.append(lime(
    55, "Welcome back", "ACT 6 · INTERFACE BUILDERS",
    "Break is over if they took one. Pixels now. She is still waiting.",
    "Level 04<br>The Interface Builders.",
    "Pixels. She is still waiting.",
    timer="45", kicker="LEVEL 04", right="03:00–03:45"
))
slides.append(lesson(
    56, "Your Figma workspace", "ACT 6 · INTERFACE BUILDERS",
    "Shared product page plus team pages A–H. If the source file differs, document existing structure. Do not reorganise the source library destructively.",
    "One file. Eight pages. Do not wreck the library.",
    rules=[
        "Shared product page.",
        "Team A through Team H pages.",
        "Steal components. Do not restyle the masters.",
        "If the kit's page map is different, write it down and use an approved workspace.",
    ],
    kicker="FILE", right="STRUCTURE"
))
slides.append(studio(
    57, "Build your first screen", "ACT 6 · INTERFACE BUILDERS",
    "Start with the most important moment in your journey. Build the primary screen using existing styles and components.",
    "Start with the most important moment.",
    "One primary screen, kit styles only. If you are drawing a new purple, you have left the team.",
    "12 min", "12", kicker="PRIMARY"
))
slides.append(studio(
    58, "Build the flow", "ACT 6 · INTERFACE BUILDERS",
    "A screen is not an experience. Connect 3–5 meaningful screens or states.",
    "If Play does nothing, it is still a poster.",
    "Three to five connected frames. Prototype the tap that matters.",
    "12 min", "12", kicker="FLOW"
))
slides.append(lesson(
    59, "Missing states", "ACT 6 · INTERFACE BUILDERS",
    "What happens when things don't go as planned? Empty, loading, error, success, disabled, selected. Identify at least two non-default states.",
    "What happens when things don't go as planned?",
    grades=[
        ("Empty", "Nothing here yet."),
        ("Loading", "Work is happening."),
        ("Error", "Recovery, not blame."),
        ("Success", "She knows it worked."),
    ],
    kicker="STATES", right="AT LEAST TWO"
))
slides.append(studio(
    60, "The 10-second test", "ACT 6 · INTERFACE BUILDERS",
    "A student from another team inspects without explanation. What is this for? What next? What happens on the primary tap? Understandability and visual hierarchy.",
    "Give the file. Stay quiet.",
    "One visitor. Ten seconds. What is this, what next, what happens when I tap.",
    "8 min", "8", kicker="TEST"
))
slides.append(studio(
    61, "Sprint 2 checkpoint", "ACT 6 · INTERFACE BUILDERS",
    "Show your product, not just progress. Working screens, clear flow, consistent styling, states, prototype connections.",
    "Show the path. Not the effort.",
    "Working screens. Flow. Kit. Two states. Play, if you can.",
    "5 min", "5", kicker="CHECKPOINT"
))

# ACT 7
slides.append(lime(
    62, "Walk her", "ACT 7 · ASSEMBLY",
    "Walk her from A to H. If she gets lost, the seam is theirs.",
    "Walk her from A to H.",
    "If she gets lost, the seam is yours.",
    timer="15", kicker="ACT 7", right="03:45–04:00"
))
slides.append(lesson(
    63, "The integration challenge", "ACT 7 · ASSEMBLY",
    "Do the journeys actually connect? Teams must not overwrite another team's work. Integration is a coordinated handoff.",
    "Do the journeys actually connect?",
    rules=[
        "Consistent header.",
        "Shared navigation.",
        "Consistent buttons, type, spacing.",
        "Correct screen transitions.",
        "Consistent language.",
        "No duplicate or contradictory patterns.",
    ],
    kicker="CHECKLIST", right="SEAMS"
))
slides.append(wide(
    64, "The product map", "ACT 7 · ASSEMBLY",
    "One representative per team: where Arya enters, what she accomplishes, where she exits, who she hands to.",
    "assets/mindspace/journeys.svg",
    "Teaching diagram of eight journeys · replace with the live assembled map in class."
))

# ACT 8
slides.append(lime(
    65, "Mindspace is live", "ACT 8 · FIRST LAUNCH",
    "No spoken tour. She walks it. Keep the energy high.",
    "She's tapping it now.",
    "No spoken tour.",
    timer="15", kicker="ACT 8", right="04:00–04:15"
))
slides.append(studio(
    66, "The launch showcase", "ACT 8 · FIRST LAUNCH",
    "90 seconds each. User problem, design solution, one UX decision, one component decision, one unsolved limitation. Keep the pace high.",
    "Ninety seconds. Then sit down.",
    "Problem. Solution. One UX decision. One component decision. One thing you have not solved.",
    "12 min", "12", kicker="SHOWCASE"
))
slides.append(lesson(
    67, "First product review", "ACT 8 · FIRST LAUNCH",
    "Does it work as one product? Do not turn this into a popularity contest.",
    "Does it work as one product?",
    cols=[
        ("Ask the class", ["Does it feel consistent?", "Is Arya's journey clear?", "What is confusing?"]),
        ("Do not", ["Vote for the prettiest screen.", "Skip the gaps.", "Let one team dominate the airtime."]),
    ],
    kicker="REVIEW", right="ONE PRODUCT"
))

# ACT 9
slides.append(quote(
    68, "The design director enters", "ACT 9 · CRITIQUE",
    "Become the design director. Don't simply tell them what is wrong. Ask questions. Good design is knowing what to improve.",
    "What would she tap first?",
    "What would she miss?"
))
slides.append(lesson(
    69, "Critique framework", "ACT 9 · CRITIQUE",
    "Five design director questions. Use them on an actual student screen.",
    "Five questions. Use them on a real screen.",
    rules=[
        "Is the user's problem being solved?",
        "Is the next action obvious?",
        "Is the experience unnecessarily complicated?",
        "Is the design consistent?",
        "What happens when something goes wrong?",
    ],
    kicker="FRAMEWORK", right="15 MIN", timer="15"
))
slides.append(studio(
    70, "The UX teardown", "ACT 9 · CRITIQUE",
    "Pick one screen from the assembled application. Critique the design, never the designer. Confusing content, extras, weak hierarchy, inconsistent components, missing feedback, access issues.",
    "Break it before she does.",
    "One shared screen. Name the miss. Protect the person who made it.",
    "6 min", "6", kicker="TEARDOWN"
))
slides.append(cards(
    71, "The opportunity board", "ACT 9 · CRITIQUE",
    "Keep. Fix. Remove. Improve. Each team identifies three highest-priority improvements.",
    "Keep. Fix. Remove. Improve.",
    [
        ("Keep", "What already serves Arya", "Do not restyle it for sport."),
        ("Fix", "Broken or unclear", "Name the principle."),
        ("Remove", "Noise", "If it has no job, it goes."),
        ("Improve", "The next version", "Three priorities only."),
    ],
    kicker="BOARD"
))

# ACT 10
slides.append(lime(
    72, "Level 5 unlocked", "ACT 10 · DESIGN EVOLUTION",
    "She already used v1. Fix what she hit. Do not add a fifth screen.",
    "Level 05<br>The Design Evolution.",
    "She already used v1. Fix what she hit.",
    timer="60", kicker="LEVEL 05", right="04:30–05:30"
))
slides.append(studio(
    73, "Refinement mission", "ACT 10 · DESIGN EVOLUTION",
    "Don't add more. Make it better. Review the three improvement priorities from critique.",
    "If you are adding a fifth screen, you are hiding.",
    "Re-read your three priorities. Kill, merge, or fix. Do not decorate.",
    "5 min", "5", kicker="MISSION"
))
slides.append(studio(
    74, "Improve the journey", "ACT 10 · DESIGN EVOLUTION",
    "Where can we remove friction? Revisit the user flow. Eliminate unnecessary steps or confusing decisions.",
    "Where can we remove friction?",
    "Kill a step. Merge a decision. Name what Arya no longer has to think about.",
    "10 min", "10", kicker="JOURNEY"
))
slides.append(studio(
    75, "Improve the interface", "ACT 10 · DESIGN EVOLUTION",
    "Hierarchy, clarity, consistency. Improve visual hierarchy, spacing, typography, component usage.",
    "One thing louder. The rest quieter.",
    "Type from the kit. Spacing you can count. No new purple.",
    "15 min", "15", kicker="INTERFACE"
))
slides.append(studio(
    76, "Improve the interaction", "ACT 10 · DESIGN EVOLUTION",
    "What happens after the tap? Selected, validation, error, success, loading, empty, recovery.",
    "What happens after the tap?",
    "Add or refine: selected, validation, error, success, loading, empty, recovery.",
    "15 min", "15", kicker="INTERACTION"
))
slides.append(studio(
    77, "Cross-team usability test", "ACT 10 · DESIGN EVOLUTION",
    "Swap prototypes. Give a task based on Arya's scenario. Observe hesitation, misunderstanding, expectation, stuck moments.",
    "Swap. Stay quiet.",
    "Give Arya's task. Watch where they hesitate. Do not rescue them with a speech.",
    "10 min", "10", kicker="TEST"
))
slides.append(studio(
    78, "The final polish", "ACT 10 · DESIGN EVOLUTION",
    "Fix the most important usability issue and check consistency with the Mindspace library.",
    "One seam. Then we ship.",
    "Fix the worst miss. Then check you still look like Mindspace.",
    "5 min", "5", kicker="POLISH"
))

# ACT 11
slides.append(lime(
    79, "The final launch", "ACT 11 · SHOWCASE",
    "Walk the live prototype. No spoken tour. Two minutes per desk.",
    "Walk it.",
    "No spoken tour.",
    timer="20", kicker="ACT 11", right="05:30–05:50"
))
slides.append(cards(
    80, "Eight journeys, one Arya", "ACT 11 · SHOWCASE",
    "Two minutes per team: original problem, first solution, feedback, what changed, why the final is better.",
    "Two minutes. Then sit down.",
    [
        ("A", "Getting started", "Problem → first → change."),
        ("B", "Personalisation", "Problem → first → change."),
        ("C", "Home", "Problem → first → change."),
        ("D", "Discover", "Problem → first → change."),
        ("E", "Meditation", "Problem → first → change."),
        ("F", "Goals", "Problem → first → change."),
        ("G", "Journal", "Problem → first → change."),
        ("H", "Profile", "Problem → first → change."),
    ],
    kicker="PRESENT"
))
slides.append(pair(
    81, "Before and after", "ACT 11 · SHOWCASE",
    "The power of iteration. Use actual first-version and refined screens from the room. Teaching pair until student work is on the wall.",
    ("assets/mindspace/home-clutter.svg", "First version energy · teaching diagram until student work is pinned", False),
    ("assets/mindspace/home-calm.svg", "Refined · teaching diagram until student work is pinned", True),
    kicker="ITERATION"
))
slides.append(wide(
    82, "Final product walkthrough", "ACT 11 · SHOWCASE",
    "Demonstrate the connected prototype from onboarding through journeys. Use a real clickable prototype if available. Otherwise a prepared sequence labelled as a visual walkthrough.",
    "assets/figma-kits/meditation-thumb-view.png",
    "Walk the live prototype if it exists. If not, this kit sequence is a visual walkthrough, not a clickable product."
))

# ACT 12
slides.append("""<section class="slide lesson-plan" %s>%s
<div class="lp-body"><div class="lp-heading"><h2>Awards follow what the room saw.</h2><p class="lp-subtitle">Not the prettiest screen. Click to mark.</p></div>
<div class="award-grid">
<button type="button" data-award><strong>Best UX thinking</strong><span>Strongest understanding of the user.</span></button>
<button type="button" data-award><strong>Best design decision</strong><span>Most thoughtful component or interaction choice.</span></button>
<button type="button" data-award><strong>Best visual design</strong><span>Strongest visual execution in the kit.</span></button>
<button type="button" data-award><strong>Best problem solver</strong><span>Best response to a complex challenge.</span></button>
<button type="button" data-award><strong>Best collaboration</strong><span>Strongest teamwork across desks.</span></button>
<button type="button" data-award><strong>Best iteration</strong><span>Biggest improvement after feedback.</span></button>
<button type="button" data-award><strong>Best accessibility</strong><span>Most inclusive decisions.</span></button>
<button type="button" data-award><strong>Product champion</strong><span>Strongest overall contribution.</span></button>
</div></div></section>""" % (
    attrs(83, "The design awards", "ACT 12 · CLOSING",
          "Awards based on observed work and reasoning, not invented scores. 05:50–06:00.", timer="10"),
    meta("AWARDS", "05:50–06:00")
))
slides.append(lesson(
    84, "One decision", "ACT 12 · CLOSING",
    "Do not recap nine skills. Ask for one decision they would now make differently.",
    "Name one decision you would now make differently.",
    cols=[
        ("Ask", ["What would you cut?", "What would you steal again?", "What would you test first?"]),
        ("Pass when", ["They can name the miss.", "They can name the law.", "They do not say 'it looks better.'"]),
    ],
    kicker="ASK THE ROOM", right="ONE LINE"
))
slides.append("""<section class="slide closing" %s>
<div class="grid-lines"></div>
%s
<div class="closing-content">
<h2>You are still<br>the designer.</h2>
<p>The file is the evidence. She still has five minutes.</p>
<div class="contact">
<a href="session-5-guide.html">Studio sheet</a>
<a href="notes.html#session-5">Class notes</a>
<a href="%s" target="_blank" rel="noopener">Mindspace kit</a>
</div>
</div>
</section>""" % (
    attrs(85, "Closing thought", "ACT 12 · CLOSING",
          "Same close as Session 4. The file is the evidence. Do not end on a slogan."),
    meta("SESSION 05", "CLOSE"),
    KIT_MIND
))

assert len(slides) == 85, len(slides)
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
  <link rel="stylesheet" href="deck-v2.css?v=11">
  <link rel="stylesheet" href="mobile.css?v=9">
  <link rel="stylesheet" href="session-5.css?v=6">
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
    <p class="lp-subtitle" style="margin-top:.8rem">10 identify · 20 decision · 20 reasoning · 15 issue · 25 improvement · 15 deliverable · 15 collaboration · 20 observation · 25 iteration. Never for finishing first.</p>
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
    {''.join(slides)}
  </main>

  <aside class="controls" aria-label="Slide navigation">
    <button class="prev" aria-label="Previous slide">←</button>
    <span class="counter">01 / 85</span>
    <button class="next" aria-label="Next slide">→</button>
  </aside>
  <div class="progress"><span></span></div>
  <script src="deck.js"></script>
  <script src="session-5.js?v=5"></script>
</body>
</html>
"""

out = Path(__file__).with_name("session-5.html")
out.write_text(html)
print(f"wrote {out} slides={len(slides)} bytes={out.stat().st_size}")
