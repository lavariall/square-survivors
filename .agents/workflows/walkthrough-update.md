---
description: How to update README.md and architecture-guideline.md after a feature update
---

This workflow ensures that all technical documentation remains in sync with the codebase after a new feature or architectural change is implemented.

1. **Analyze the Change**: Identify if the change affects:
    - User-facing controls (keyboard/mouse).
    - The "How to Add" extension patterns (Upgrades, Enemies, etc.).
    - Core architectural principles (FSM, Entity base classes, coordinate systems).

2. **Update README.md**:
    - **Controls**: If input mappings changed, update the `🕹️ Controls` table.
    - **Extensibility**: If a new system was added (e.g., a new type of Entity or System), update the `🛠️ How to Add` section with examples.
    - **Diagrams**: Update the Mermaid class diagram if there were structural changes to the core classes.

3. **Update architecture-guideline.md**:
    - Navigate to `.agents/rules/architecture-guideline.md`.
    - Locate the relevant section (e.g., `## 3. Modular Upgrade System` or `## 5. UI & Presentation`).
    - Update the guidelines to reflect new requirements or best practices established by the feature.
    - Use code snippets where appropriate to illustrate the expected implementation pattern.

4. **Cross-Verify**:
    - Ensure that the descriptions in `README.md` match the technical constraints defined in `architecture-guideline.md`.
    - Verify that all relative file links in the documentation are still valid.
