# Frontend Wireframes & UX Ideas for Brand-Filtered Gamified Tech Sheet System

## Technician Dashboard

- **Upload Tech Sheet**
  - [ ] Drag-and-drop PDF/image
  - [ ] Brand auto-detection (shows warning if not Whirlpool, Maytag, KitchenAid, Jenn-Air)
  - [ ] Summary of extracted symbols, diagrams, documentation
  - [ ] "Submit" button
  - [ ] Instant badge notification (e.g., 🎉 "Symbol Scout unlocked!")

- **My Achievements**
  - [ ] Badges earned (with tooltip descriptions)
  - [ ] Upload count, last upload date
  - [ ] Recent badge events (with appliance, timestamp)
  - [ ] Download my badge event history as CSV

- **Leaderboard**
  - [ ] Top contributors (uploads, badges)
  - [ ] Filter by brand, time period

- **Feedback Loop**
  - [ ] Submit feedback on search results or uploads
  - [ ] See my feedback history

---

## Admin Dashboard

- **System Summary**
  - [ ] Total uploads, unique users, badge count
  - [ ] Uploads by brand
  - [ ] Trending symbols/keywords
  - [ ] Feedback volume

- **Reports**
  - [ ] Download leaderboard CSV
  - [ ] Download badge event CSV

- **Audit Trail**
  - [ ] Browse badge events by user/brand/date
  - [ ] Export filtered badge events

---

## UX Flow (Technician)

1. Login → "Upload Tech Sheet"
2. Drag file → Brand detected → Extract preview
3. Submit → Badges awarded → Notification
4. View "My Achievements" for badge/event details
5. Check leaderboard for friendly competition
6. Give feedback on search/upload experience

---

## UX Flow (Admin)

1. Login → View system stats on dashboard
2. Download CSV reports for compliance/analytics
3. Browse audit trail for badge events
4. Review feedback for improvement opportunities

---

## Accessibility & Compliance

- All badge, leaderboard, and feedback features strictly filter to supported brands.
- Uploads for unsupported brands show clear warnings and are excluded from gamification.

---

## Next Steps

- Sketch wireframes for each dashboard page.
- Map API endpoints to UI actions.
- Plan React/Vue components for each feature.

---