---
name: MediFind
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#42474f'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#727780'
  outline-variant: '#c2c7d1'
  surface-tint: '#2d6197'
  primary: '#00355f'
  on-primary: '#ffffff'
  primary-container: '#0f4c81'
  on-primary-container: '#8ebdf9'
  inverse-primary: '#a0c9ff'
  secondary: '#006a65'
  on-secondary: '#ffffff'
  secondary-container: '#90f0e8'
  on-secondary-container: '#006f6a'
  tertiary: '#1509ad'
  on-tertiary: '#ffffff'
  tertiary-container: '#3332c2'
  on-tertiary-container: '#b2b3ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d2e4ff'
  primary-fixed-dim: '#a0c9ff'
  on-primary-fixed: '#001c37'
  on-primary-fixed-variant: '#07497d'
  secondary-fixed: '#93f3eb'
  secondary-fixed-dim: '#76d6cf'
  on-secondary-fixed: '#00201e'
  on-secondary-fixed-variant: '#00504c'
  tertiary-fixed: '#e1e0ff'
  tertiary-fixed-dim: '#c0c1ff'
  on-tertiary-fixed: '#07006c'
  on-tertiary-fixed-variant: '#2f2ebe'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg:
    fontFamily: Public Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.3'
  headline-md:
    fontFamily: Public Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Public Sans
    fontSize: 20px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Public Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  label-lg:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 64px
  touch-target: 48px
---

## Brand & Style
The brand personality of this design system is rooted in medical authority, empathetic care, and technological precision. It is designed to evoke a sense of immediate safety and reliability, catering to a diverse demographic that includes elderly patients and healthcare professionals. 

The visual style is **Corporate / Modern** with high-clarity functionalism. It utilizes generous white space to reduce cognitive load, ensuring that users navigating stressful health decisions feel calm and focused. To signify the "intelligent" discovery aspect, the system incorporates subtle **Glassmorphism** and soft luminescence for AI-driven recommendation modules, distinguishing them from static clinical data without sacrificing professional integrity.

## Colors
The palette is built on "Clinical Blue" as the primary anchor to establish trust and stability. "Healing Green" is used as a secondary color for success states, health indicators, and "Verified" status badges, providing a psychological link to wellness. 

To represent intelligent features, a "Discovery Indigo" is introduced as a tertiary accent, often applied as a soft glow or a subtle gradient. For maximum accessibility, the neutral palette favors high-contrast slate tones over soft greys to ensure text remains legible against the stark white backgrounds. Backgrounds use off-white tints to reduce screen glare for sensitive eyes.

## Typography
This design system prioritizes **Public Sans** for its institutional clarity and exceptional readability in government and health contexts. The scale is intentionally enlarged: the default body text starts at 18px to accommodate elderly users and those with visual impairments.

High contrast ratios (minimum 7:1 for body text) are strictly enforced. For Urdu localization, the system utilizes a compatible Noto Sans Arabic typeface, ensuring that line heights are increased by 20% to prevent the collision of characters and maintain the same level of legibility as the English counterparts.

## Layout & Spacing
The layout follows a **Fixed Grid** on desktop (12 columns, 1200px max-width) to maintain a centered, readable line length for medical articles, while transitioning to a **Fluid Grid** on mobile. 

A strict 8px rhythm governs all spatial relationships. Spacing is designed to be symmetrical to facilitate Right-to-Left (RTL) flipping for Urdu without requiring layout re-engineering. Generous margins and gutters prevent visual clutter, which is critical for users processing complex medical information. Every interactive element maintains a minimum touch target of 48px to support users with limited fine motor control.

## Elevation & Depth
Depth is communicated through **Tonal Layers** and **Ambient Shadows**. Surfaces are kept mostly flat to maintain a "clean" clinical feel, with elevation reserved for critical interactive layers like search bars and floating action buttons.

1.  **Low Elevation:** Used for cards containing medicine details; features a soft, diffused 4% opacity shadow.
2.  **High Elevation:** Used for modals and dropdown menus; features a structured shadow with a larger blur radius (16px) to clearly separate the interaction from the content below.
3.  **Intelligence Glow:** AI-powered discovery features utilize a soft, 8px outer glow in the tertiary Indigo color rather than a traditional shadow, signaling a "smart" layer of the interface.

## Shapes
The shape language uses **Rounded** (8px) corners as the standard. This approach balances the approachability of a consumer app with the structural discipline of a medical tool. 

Larger containers like profile cards or search modules use "rounded-xl" (24px) to feel more inviting. Pills and tags (such as medicine categories) use full "pill" roundedness to distinguish them as clickable, discrete items of information.

## Components
- **Buttons:** Primary buttons are high-contrast Clinical Blue with white text. They use a bold weight and 8px rounded corners.
- **Verified Badges:** A signature component featuring a Healing Green checkmark inside a shield or circle, accompanied by a subtle "Verified" label in semibold typography.
- **Cards:** Medicine cards feature a clean white background with a 1px soft grey border. Information is tiered using typography rather than colors to keep the interface clean.
- **Search Bar:** Prominent and centrally located with a high-elevation shadow. It includes a clear 'clear' (X) button and voice-input capability for accessibility.
- **Input Fields:** Use 2px borders on focus in Primary Blue to provide clear visual feedback. Error states use a high-contrast medical red.
- **Chips/Tags:** Used for filtering by symptoms or drug classes. These utilize a light tint of the secondary color for an active state to remain distinct but calm.
- **RTL Switches:** All icons (like arrows or progress bars) are designed to flip for Urdu, except for brand-specific marks or universal medical symbols (like the Red Cross/Crescent).