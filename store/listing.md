# Neon Focus: store listing kit

Everything to paste into Google Play Console and App Store Connect. Graphics are generated automatically into `store/graphics/` and `store/screenshots/` by the **Store assets** GitHub Action.

## Shared details

| Field | Value |
|---|---|
| Developer / seller | After Hours Co LLC |
| App ID / bundle ID | `com.afterhoursco.neonfocus` |
| Price | Free, with one in-app purchase: **Neon Focus Pro**, $4.99, one-time (non-consumable) |
| Product ID for Pro | `neonfocus_pro` |
| Category | Google Play: Game → Puzzle · Apple: Games, with game subcategories Puzzle and Casual (don't use Health & Fitness or Medical) |
| Website | https://neonfocus.afterhoursco.dev |
| Support URL | https://neonfocus.afterhoursco.dev/support/ |
| Privacy policy URL | https://neonfocus.afterhoursco.dev/privacy/ |
| Support email | hq@afterhoursco.dev |
| Ads | No |
| Content rating | Everyone (IARC) · Apple 4+ |
| Target audience (Google) | 13+ (do **not** select under-13 age groups, which would put the app under the Families policy) |
| Languages | English (US) |

## Name

- **Google Play title (30 max):** `Neon Focus: ADHD Focus Game` (27)
- **App Store name (30 max):** `Neon Focus: ADHD Focus Game` (27)
- **App Store subtitle (30 max):** `60-second focus game for ADHD` (29)

## Short description (Google Play, 80 max)

`60-second focus runs. The rule keeps flipping. No ads, no subscription.` (71)

## Promotional text (Apple, 170 max)

`Sixty seconds. One rule. Then it flips. A fast, bright focus game built for brains that crave novelty. No ads, no subscription, no sign-up.`

## Full description (both stores)

```
Neon Focus is a 60-second arcade game built for ADHD brains: fast, bright, and over before you get bored.

Slide your orb. Catch only what the rule says. Then the rule flips.

HOW IT WORKS
• One rule at a time: catch a color or a shape
• The rule keeps flipping, so you have to switch fast
• HANDS OFF rounds: dodge everything and hold back for a bonus
• Good catches add time, and the game speeds up as you get better
• It eases off when you struggle, so it stays fun instead of frustrating

SEE YOUR BRAIN AT WORK
After every run you get a breakdown of focus, switching, self-control and speed, plus one simple tip for next time.

MADE TO KEEP YOU COMING BACK
• Daily quests, XP, levels and streaks (with a streak shield, because life happens)
• Daily Challenge: the same run for everyone, every day
• Zen mode: no timer, no penalties, just flow
• Stats screen that charts your last 30 runs
• Neon, Sunset and Ice themes

COMFORTABLE FOR EVERYONE
• Colorblind mode with marks inside every shape
• Reduce-motion mode (no shake or flashes)
• Sound, music and vibration toggles
• Works offline

NO NONSENSE
• No ads. Ever.
• No subscription. Neon Focus Pro is a single $4.99 unlock.
• No account and no data collection. Your progress stays on your phone.

Neon Focus is a game designed to be fun for ADHD brains. It is not a medical device and does not diagnose or treat any condition.

Made by After Hours Co, a small independent studio.
```

## Apple keywords (100 max, comma-separated, no spaces)

`adhd,focus,attention,brain,game,reflex,arcade,switch,neon,concentration,quick,offline,no ads,daily`

## What's new (first release)

`First release. Catch, flip, focus. Thanks for playing!`

## Screenshot captions (already baked into the images)

1. One rule. Sixty seconds. / Catch only what the rule says
2. The rule keeps flipping / Switch fast. Stay sharp.
3. HANDS OFF / Hold back. Dodge everything.
4. See your focus skills / Accuracy, switching and self-control
5. Track your progress / Every run, charted
6. No ads. No subscription. / Daily challenge, Zen mode and more

## Graphics checklist

| Asset | Size | File |
|---|---|---|
| Google Play app icon | 512×512 PNG | `store/graphics/icon-512.png` |
| Google Play feature graphic | 1024×500 PNG | `store/graphics/feature-graphic-1024x500.png` |
| Google Play phone screenshots (2–8) | 1080×1920 | `store/screenshots/play/*.png` |
| App Store icon | 1024×1024, no transparency | built into the app; copy in `store/graphics/icon-1024.png` |
| App Store iPhone 6.9" screenshots (1–10) | 1320×2868 | `store/screenshots/apple-6.9/*.png` |

## Google Play: Data safety form

- Does your app collect or share any of the required user data types? **No**
- Is all user data encrypted in transit? **Not applicable (no data collected)**
- Account creation: **No accounts**
- Data deletion: not applicable

## Apple: App Privacy ("nutrition label")

- **Data Not Collected**

## Apple: export compliance

- Uses encryption? **No** (only standard HTTPS, and the app makes no network calls). `ITSAppUsesNonExemptEncryption = NO` is set in Info.plist by the build.

## Content-rating questionnaire answers (both stores)

Violence: none (abstract shapes) · Sexual content: none · Profanity: none · Drugs/alcohol/tobacco: none · Gambling or simulated gambling: none · User-generated content / chat: none · Shares location: no · Digital purchases: yes (one-time Pro unlock) · Unrestricted web access: no.

## Review notes (Apple)

`Neon Focus needs no login. Tap PLAY for a 60-second run, or How to play → Practice round for a guided tutorial. Pro (Zen, Daily, Stats, themes) is unlocked with the in-app purchase "Neon Focus Pro".`

## Wording rules (both stores)

Never say the app treats, improves, trains or cures ADHD or any condition. Allowed: "built for ADHD brains", "focus game", "fun for ADHD brains". Keep the not-a-medical-device line in the description.
