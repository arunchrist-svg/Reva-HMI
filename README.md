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

**Vercel (live)**

1. Sign in at [vercel.com](https://vercel.com) with your GitHub account.
2. Click **Add New… → Project** and import `arunchrist-svg/Reva-HMI`.
3. Leave defaults: `vercel.json` already points Vercel at `presentation/` (no build step).
4. Click **Deploy**.

After deploy:

- **Slide deck:** `https://<your-project>.vercel.app/deck`
- **Full site:** `https://<your-project>.vercel.app/`

Every push to `main` redeploys automatically.
