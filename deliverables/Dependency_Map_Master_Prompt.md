# Dependency Map Generator -- Master Prompt

Copy everything below the line and paste into Claude with your own data.

---

Create an interactive HTML dependency map with the following specifications:

## Visual Design
- Dark theme (background: #0f0e17)
- SVG-based node-and-edge diagram inside a responsive viewBox
- Nodes: rounded rectangles with colored borders, containing:
  - Phase tag (e.g., P1, P2, P3, Future)
  - English label (bold)
  - Chinese/secondary label (muted)
- Edges: curved paths (quadratic bezier) with arrow markers
- Color-coded by phase:
  - Phase 1 (quick wins): green (#34d399)
  - Phase 2: blue (#60a5fa)
  - Phase 3: purple (#a78bfa)
  - Future: gray (#6b7280)

## Interaction
- Click any node to highlight it + all directly connected nodes
- Dim unrelated nodes/edges (opacity 0.15)
- Bottom info panel slides up showing:
  - Node name (English + Chinese)
  - Department and phase
  - Upstream dependencies (who feeds this node)
  - Downstream impacts (who this node feeds)
- Click background to deselect

## Layout
- Horizontal tiers (top = upstream root, bottom = downstream aggregation)
- Tier labels on left side with dashed separator lines
- Top tier: nodes with zero dependencies
- Bottom tier: nodes with the most dependencies

## Data Structure (REPLACE WITH YOUR OWN)

```javascript
const NODES = [
  { id: 'node_1', label: 'English Name', label2: 'Secondary Label', dept: 'Department', phase: 'P1', color: '#34d399', x: 525, y: 100 },
  { id: 'node_2', label: 'Another Node', label2: '另一個節點',       dept: 'QA',         phase: 'P2', color: '#60a5fa', x: 300, y: 230 },
];

// [from, to] means "from" enables/feeds "to"
const EDGES = [
  ['node_1', 'node_2'],
];
```

## Positioning Guide
- SVG viewBox: 1050 x 680
- X range: 150-900, Y range: 100-645
- Tier spacing: ~120-130px vertical
- Node spacing: ~250px horizontal
- Node box: 170w x 52h

## Technical
- Single self-contained HTML file
- No dependencies except Google Fonts
- Edge curves: quadratic bezier with perpendicular offset
- Arrow markers in SVG defs
- Adjacency built from EDGES for upstream/downstream lookups

---

## HOW TO USE

1. Replace NODES with your items
2. Replace EDGES with your dependencies
3. Update tier labels, title, subtitle, legend
4. Paste this entire prompt + your data into Claude

## TIPS

- Ask: "which items MUST exist before this one can work?" -- that gives you edges
- Zero upstream dependencies = top tier
- Most upstream dependencies = bottom tier
- Keep 3-5 nodes per tier for readability
- Works for: system architecture, project tasks, process flows, supply chains, course prerequisites
