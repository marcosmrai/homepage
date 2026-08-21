<%
// team-theme.ejs.md — a reusable "theme" for a grouped team/people page.
//
// Paired with team-theme.css. Reads a `group` metadata field straight off
// each person's own .qmd front matter (no folders, no hardcoded lists) and
// renders one titled, alternating section per distinct group value, each a
// grid of photo cards — mirroring how band-sections.lua turns plain "##"
// headings into alternating full-bleed bands elsewhere on the site.
//
// Required listing config on the page that uses this theme:
//   listing:
//     id: people
//     contents: "*.qmd"
//     type: custom
//     template: team-theme.ejs.md
//     fields: [image, title, subtitle, description, group]
//
// To reuse elsewhere: copy this file + team-theme.css into the target
// site's people/ folder, add the listing config above, and set
// `css: team-theme.css` in that page's front matter. Adjust groupOrder
// below to the desired group names/order.

const groupOrder = [
  "Principal Investigator",
  "Ph.D. Students",
  "Master Students",
  "Undergrad Research Assistants",
  "Former Researchers",
];

const groups = {};
for (const item of items) {
  const g = item.group || "Other";
  if (!groups[g]) groups[g] = [];
  groups[g].push(item);
}

for (const g of Object.keys(groups)) {
  groups[g].sort((a, b) => (a.title || "").localeCompare(b.title || ""));
}

const orderedGroups = groupOrder.filter((g) => groups[g]);
for (const g of Object.keys(groups)) {
  if (!orderedGroups.includes(g)) orderedGroups.push(g);
}
%>

::: {.people-grid}

<% for (const groupName of orderedGroups) { %>

## <%= groupName %>

::: {.list .grid .quarto-listing-cols-3}
<% for (const item of groups[groupName]) { %>

::: {.g-col-1}

```{=html}
<a href="<%- item.path %>" class="quarto-grid-link">
<div class="quarto-grid-item card h-100 card-left">
<p class="card-img-top">
<img src="<%- item.image %>" class="thumbnail-image card-img" loading="lazy">
</p>
<div class="card-body post-contents">
<h5 class="no-anchor card-title listing-title"><%= item.title %></h5>
<div class="card-subtitle listing-subtitle"><%= item.subtitle ?? "" %></div>
<div class="card-text listing-description delink"><%= item.description ?? "" %></div>
</div>
</div>
</a>
```

:::

<% } %>
:::

<% } %>

:::
