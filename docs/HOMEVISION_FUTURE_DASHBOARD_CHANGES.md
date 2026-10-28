# HomeVision / Homebase — Future dashboard change

**Deferred requirement:** On the Homebase Controls page (`/tv-home-v3/controls`),
pressing the Fire TV remote's short **Back** button should navigate to the
Homebase Morning page (`/tv-home-v3/morning`) when no overlay, popover, or edit
mode is active.

Implement this in the **Homebase dashboard JavaScript**, not the Android native
Back-key handler. HomeVision already forwards short Back as a bubbling `Escape`
keydown event in kiosk mode; the page should consume overlays first and then
navigate Controls → Morning as its fallback. Verify on the Living Room Fire Stick
before rolling out to the other TVs.

This is deliberately NOT implemented by the navigation-mode patch.
