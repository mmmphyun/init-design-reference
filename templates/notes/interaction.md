# Interaction Specifications

## 1. Interactive States
- **Hover / Focus**: 150ms ease-out transitions on borders, background colors, and subtle transforms.
- **Active / Pressed**: Immediate visual scale depression (e.g. `scale-95` or `scale-[0.98]`).
- **Focus Rings**: Strict `:focus-visible` styling with high-contrast 2px outline and 2px offset.

## 2. Overlays & Dialogs
- **Backdrop**: Semi-transparent dark wash with subtle backdrop-filter blur.
- **Dismissal**: Must support `Escape` key and click outside.
- **Focus Trap**: Traps keyboard focus within modal while active; restores focus upon close.
