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

Open [http://localhost:8080](http://localhost:8080) (site) or [http://localhost:8080/deck.html](http://localhost:8080/deck.html) (slide deck).

**Live (Vercel)**

- **Full site:** [https://arun-hmi.vercel.app/](https://arun-hmi.vercel.app/)
- **Slide deck:** [https://arun-hmi.vercel.app/deck](https://arun-hmi.vercel.app/deck)

Connected to `main` on GitHub. Every push redeploys automatically.

Project dashboard: [arun-hmi on Vercel](https://vercel.com/arunchrist-svgs-projects/arun-hmi)

### Change the `vercel.app` subdomain

The default URL is `{project-name}.vercel.app`. To use `arun-hmi.vercel.app`:

1. Open [reva-hmi project settings](https://vercel.com/arunchrist-svgs-projects/reva-hmi/settings) (or your current project).
2. Go to **Settings → General**.
3. Under **Project Name**, change `reva-hmi` to `arun-hmi` and save.
4. Production becomes `https://arun-hmi.vercel.app` (the old `reva-hmi.vercel.app` URL stops working).

Alternatively, keep the project name and add a domain under **Settings → Domains** if you prefer both URLs.
