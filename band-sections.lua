-- band-sections.lua
--
-- Turns every "## Heading" section into a full-bleed band that alternates
-- gray/white background, with the heading fixed in a narrow left column
-- and the rest of the section's content in a wider column to the right —
-- the pattern used across the site (home, CV pages) — driven purely by
-- '##' headings in the source, no manual div wrapping required.
--
-- Content before the first "##" (e.g. the profile card / bio) is left
-- untouched. Enable per-page with:
--   filters:
--     - band-sections.lua

local band_index = 0

local function make_band(header, content_blocks)
  local color = (band_index % 2 == 0) and "band-gray" or "band-white"
  band_index = band_index + 1

  local label = pandoc.Div({ header }, pandoc.Attr("", { "section-label" }))
  local content = pandoc.Div(content_blocks, pandoc.Attr("", { "section-content" }))
  local row = pandoc.Div({ label, content }, pandoc.Attr("", { "column-body", "section-row" }))
  local band = pandoc.Div({ row }, pandoc.Attr("", { "column-screen", "band", color }))
  return band
end

function Pandoc(doc)
  local new_blocks = {}
  local current_header = nil
  local current_content = {}

  local function flush()
    if current_header ~= nil then
      table.insert(new_blocks, make_band(current_header, current_content))
    else
      for _, b in ipairs(current_content) do
        table.insert(new_blocks, b)
      end
    end
    current_header = nil
    current_content = {}
  end

  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" and block.level == 2 then
      flush()
      current_header = block
    else
      table.insert(current_content, block)
    end
  end
  flush()

  doc.blocks = new_blocks
  return doc
end
