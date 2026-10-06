# Third-Party Notices & Licenses

This project incorporates and builds upon ideas, architectures, specifications, and code from the open-source community. We gratefully acknowledge the following works in accordance with their respective licenses.

---

## 1. pbakaus/impeccable
- **Author**: Paul Bakaus
- **Repository**: [https://github.com/pbakaus/impeccable](https://github.com/pbakaus/impeccable)
- **License**: Apache License, Version 2.0
- **Usage in this project**:
  - The deterministic rule concepts, anti-cliché detector logic, and command lifecycle architecture are ported in `scripts/lint_ui.py` and referenced in `SKILL.md`.
- **Notice**:
  ```
  Copyright 2025 Paul Bakaus

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
  ```

---

## 2. emilkowalski/skills
- **Author**: Emil Kowalski
- **Repository**: [https://github.com/emilkowalski/skills](https://github.com/emilkowalski/skills)
- **License**: MIT License
- **Usage in this project**:
  - Micro-interaction motion principles (spring physics, layout thrashing avoidance, active press feedback) incorporated into `templates/tokens/motion.json` and `templates/patterns/micro-interactions.md`.
- **Notice**:
  ```
  MIT License

  Copyright (c) 2025 Emil Kowalski

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
  ```

---

## 3. leonxlnx/taste-skill
- **Author**: Leon Linz
- **Repository**: [https://github.com/Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
- **License**: MIT License
- **Usage in this project**:
  - The 3-Dial Taste configuration framework (`DESIGN_VARIANCE`, `VISUAL_DENSITY`, `MOTION_INTENSITY`) incorporated into `templates/root/DESIGN.md` and `scripts/adapter.py`.
- **Notice**:
  ```
  MIT License

  Copyright (c) 2025 Leon Linz

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
  ```

---

## 4. frontend-design
- **Author**: Anthropic, PBC
- **Repository / Source**: Anthropic Official Prompt & Skill Guidelines
- **License**: Complete terms in Anthropic Skill Specification
- **Usage in this project**:
  - The Gate 0 brief intake interview protocol, anti-cliché rules, and single signature element principle incorporated into `templates/notes/do-not-copy.md`, `templates/notes/visual-direction.md`, and `SKILL.md`.

---

## 5. Playwright
- **Author**: Microsoft Corporation
- **Repository**: [https://github.com/microsoft/playwright](https://github.com/microsoft/playwright)
- **License**: Apache License, Version 2.0
- **Usage in this project**:
  - Headless Chromium capture integration in `scripts/capture_ui.py`.
- **Notice**:
  ```
  Copyright (c) Microsoft Corporation.

  Licensed under the Apache License, Version 2.0.
  ```

---

## 6. Figma REST API / Figma MCP
- **Platform**: Figma, Inc.
- **Reference**: Figma Developer Platform & Model Context Protocol Specifications
- **Usage in this project**:
  - Variables and design tokens extraction bridge in `scripts/sync_figma.py`.
