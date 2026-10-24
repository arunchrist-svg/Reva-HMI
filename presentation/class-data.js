/**
 * Class gallery: single source of truth.
 * To add Session 3: copy a session object, update fields, and (optionally) add an assignment.
 * Published at: /  (arun-hmi.vercel.app)
 */
window.CLASS_GALLERY = {
  program: {
    title: "UI/UX Design in Practice",
    school: "REVA University",
    instructor: "Arun Murugesan",
    role: "Head of Design, Moneyview",
    email: "arun.jpeg@gmail.com"
  },
  sessions: [
    {
      id: "session-1",
      number: "01",
      date: "25 September 2026",
      title: "HCI foundations",
      focus: "UX, UI, usability, learned through three paper wallet versions.",
      status: "published",
      slides: [
        { label: "Sprint deck", href: "sprint.html", note: "Standard" },
        { label: "Sprint (large type)", href: "sprint-v2.html", note: "Classroom" }
      ],
      notes: { label: "Class notes", href: "notes.html#session-1" },
      assignmentIds: ["assign-wallet-prd"]
    },
    {
      id: "session-2",
      number: "02",
      date: "2 October 2026",
      title: "User research",
      focus: "Evidence before design: interviews, methods, synthesis, research sheet.",
      status: "published",
      slides: [
        { label: "Session 2 deck", href: "session-2.html", note: "Large type" }
      ],
      notes: { label: "Class notes", href: "notes.html#session-2" },
      assignmentIds: ["assign-research-sheet"]
    },
    {
      id: "session-3",
      number: "03",
      date: "9 October 2026",
      title: "Working with AI",
      focus: "From prompt to published research plan.",
      status: "published",
      slides: [
        { label: "Before class setup", href: "setup-guide.html", note: "Gemini + GitHub" },
        { label: "Session 3 deck", href: "session-3.html?v=md1", note: "Classroom short" },
        { label: "Session 3 (full)", href: "session-3-v2.html?v=md1", note: "Full deck" },
        { label: "Prompt sheet", href: "session-3-guide.html?v=cc2", note: "Copy prompts" }
      ],
      assignmentIds: ["assign-project-page"]
    },
    {
      id: "session-4",
      number: "04",
      date: "24 October 2026",
      title: "Open an app",
      focus: "Phone first: what is this screen, why does it exist. Then draw that job in Figma.",
      status: "published",
      slides: [
        { label: "Session 4 deck", href: "session-4.html", note: "Classroom" },
        { label: "Studio sheet", href: "session-4-guide.html", note: "Keep open" }
      ],
      notes: { label: "Class notes", href: "notes.html#session-4" },
      assignmentIds: ["assign-primary-screen"]
    }
  ],
  assignments: [
    {
      id: "assign-wallet-prd",
      session: "01",
      title: "Design a wallet PRD",
      due: "After Session 1",
      summary: "Research one real user. Prototype three versions. Submit PRD, journey, test log, and reflection.",
      href: "notes.html#s1-assignment"
    },
    {
      id: "assign-research-sheet",
      session: "02",
      title: "Research sheet",
      due: "End of Session 2 lab",
      summary: "One research question, two interviews, five quotes, three insights, one HMW.",
      href: "notes.html#s2-deliverable"
    },
    {
      id: "assign-project-page",
      session: "03",
      title: "Published research plan",
      due: "End of Session 3",
      summary: "Groups publish a project plan, research plan, and discussion guide as one public link.",
      href: "session-3-guide.html?v=rtf"
    },
    {
      id: "assign-primary-screen",
      session: "04",
      title: "Primary screen in Figma",
      due: "Before Session 5",
      summary: "One phone frame. Version 1, Version 2, empty and after, a playable Pay-to-after prototype, three law-backed changes. Share a view link.",
      href: "notes.html#s4-assignment"
    }
  ]
};
