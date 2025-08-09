# Whirly UI/UX Design Guide

A comprehensive approach to building Whirly’s user interface, blending mid-century nostalgia with modern usability.

---

## 1. Core UI Elements

### Document Upload & Scanning
- **Drag-and-drop Zone:**  
  - Large, pill-shaped area with pastel background (mint, peach, soft blue).
  - Animated glowing border for active drag.
  - Vintage scanner icon (rounded edges, chrome highlights).
  - Feedback: Animated progress bar in retro style; checkmark or “Scan Complete!” badge with script font.

### Component List
- **Layout:**  
  - Sidebar or main panel with rounded corners.
  - Search bar with magnifying glass icon styled after 1950s appliances.
  - Filter buttons: Soft, pill-shaped, pastel colors.
  - List items: Card-style with subtle drop shadow, rounded type, and appliance-inspired icons.

### Training Options
- **Progress Indicators:**  
  - Horizontal progress bars with vintage dial textures.
  - Stepper UI with numbered pastel circles and connecting lines.
- **Access:**  
  - Dedicated “Train” section, tabbed or as a menu button with a whisk or gear icon.

### Database Integration
- **Structured Table:**  
  - Borders with subtle texture (canvas or linen).
  - Row hover highlights in soft yellow or blue.
- **Actions:**  
  - Rounded buttons with 1950s script labels (“Edit”, “Delete”, “Add”).
  - Quick filter and sort controls with appliance-style toggles.

---

## 2. Visual & Branding Elements

### Retro Logo Design
- **Typography:**  
  - Custom logotype using 1950s Whirlpool script as base.
  - Slight slant, long tails, and chrome effect.
- **Color Scheme:**  
  - Pastel palette: mint, coral, butter yellow, powder blue.
- **Icon:**  
  - Whirling lines or starbursts, reminiscent of vintage ads.

### Nostalgic Aesthetic
- **Color:**  
  - Predominantly pastel backgrounds, accent colors for calls to action.
- **Typography:**  
  - Rounded sans-serifs and decorative script for headers.
- **Textures:**  
  - Linen, canvas, or subtle paper textures as background overlays.
- **Illustrations:**  
  - Simple, flat illustrations of documents and appliances with a hand-drawn look.
- **Icons:**  
  - Appliance-inspired (dial, knob, whisk, scanner), outlined and filled options.

---

## 3. Responsive Layout

- **Grid System:**  
  - CSS grid/flexbox for adaptive multi-column layouts.
- **Breakpoints:**  
  - Desktop: Spacious, multi-pane.
  - Tablet: Single column, collapsible panels.
  - Mobile: Stacked navigation, large touch targets.
- **Navigation:**  
  - Hamburger menu for mobile, persistent sidebar or tabs for desktop/tablet.
- **Consistency:**  
  - Icon and font sizes scale with viewport.
  - Maintain pastel palette and textures across devices.

---

## 4. Usability & Accessibility

- **Contrast:**  
  - Sufficient contrast for text and icons (retro doesn’t mean hard to read).
- **Keyboard Navigation:**  
  - Tab order, focus states with soft glows.
- **ARIA Labels:**  
  - Screen reader support for all interactive elements.
- **Feedback:**  
  - Clear, animated responses for uploads, actions, and errors.

---

## 5. Example File Structure & Starter Assets

```
/ui/
  /assets/
    logo.svg            # Custom retro logo
    icons/              # Appliance-inspired SVGs
    textures/           # Linen/canvas PNG overlays
    illustrations/      # Document & appliance art
  /components/
    DocumentUpload.jsx
    ComponentList.jsx
    TrainingOptions.jsx
    DatabaseTable.jsx
    RetroButton.jsx
    ProgressBar.jsx
  /styles/
    palette.css         # Pastel colors
    typography.css      # Fonts & scripts
    textures.css        # Overlays
    layout.css          # Grid/flex
  App.jsx
  index.jsx
```

---

## 6. Actionable Recommendations

- Design logo and icons first for instant brand recognition.
- Prototype document upload and component list—these are the most interactive.
- Use CSS variables for easy palette and theme changes.
- Regularly test on multiple devices/emulators for true retro-responsiveness.
- Source or create fonts with vintage flair (e.g., “Pacifico”, “Great Vibes”, custom script).
- Consider adding a “Vintage Mode” toggle for extra retro textures and effects.