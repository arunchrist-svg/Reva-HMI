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
    }
  ]
};
