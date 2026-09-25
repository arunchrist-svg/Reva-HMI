# REVA HCI: Visiting Faculty Brief

Teaching brief and frontend presentation for **Human-Computer Interaction (M25DA304D)**: M.Arch III Semester, REVA University.

**Author:** Arun Murugesan · Head of Design, MoneyView

## Contents

- [`Arun_Murugesan_HCI_Visiting_Faculty_Brief.md`](./Arun_Murugesan_HCI_Visiting_Faculty_Brief.md): Full written brief (Medium-style essay)
- [`presentation/`](./presentation/): Working frontend presentation

## View the presentation

**Local**

```bash
cd presentation && python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080) (site), [http://localhost:8080/deck.html](http://localhost:8080/deck.html) (faculty deck), or [http://localhost:8080/sprint.html](http://localhost:8080/sprint.html) (one-day UX sprint teaching deck).

**Live (Vercel)**

- **Full site:** [https://arun-hmi.vercel.app/](https://arun-hmi.vercel.app/)
- **Slide deck:** [https://arun-hmi.vercel.app/deck](https://arun-hmi.vercel.app/deck)
- **One-day sprint (teaching):** [https://arun-hmi.vercel.app/sprint](https://arun-hmi.vercel.app/sprint)

Connected to `main` on GitHub. Every push to `main` redeploys automatically.

**Project dashboard:** [arun-hmi on Vercel](https://vercel.com/arunchrist-svgs-projects/arun-hmi)

If `arun-hmi.vercel.app` shows a 404, open the dashboard → **Deployments** and confirm a production deploy exists. If the project is new, use **Settings → Git** to connect `arunchrist-svg/Reva-HMI` and deploy `main` (root directory `.`, framework **Other**; `vercel.json` handles the rest).
