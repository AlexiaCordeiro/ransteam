# RANSTEAM

**RANSTEAM** is a command-line tool that fetches a random game from a Steam user's public library. It can pick any game, or filter by those played *above* or *below* the average playtime.

---

## Features

- Fetch a **completely random** game from a user's library.
- Filter for **most-played** games (above average playtime).
- Filter for **least-played** games (below average playtime).
- Secure API key handling via environment variables.

---

## Prerequisites

- A **Steam API Key** (free to obtain).
- The target user's **Steam ID** (must have a public profile).

---

## Obtaining a Steam API Key

1. Go to [Steam Web API Key page](https://steamcommunity.com/dev/apikey).
2. Log in with your Steam account.
3. Enter a domain.
4. Click **Register**.
5. Copy your API key (a long alphanumeric string).

---

## Adding Your API Key 
Copy the example configuration:

```bash
cp .env.example .env
```

Edit the .env file and paste your actual Steam API key:

```
STEAM_KEY=YOUR_ACTUAL_API_KEY_HERE
```
