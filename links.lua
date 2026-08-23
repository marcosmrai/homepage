-- Preenche ::: {#links} ::: no perfil de uma pessoa (people/*.qmd) OU nos
-- botões de recurso de uma publicação (publications/*.qmd — Google
-- Scholar, PDF, Slides, código) a partir de uma lista "links:" no front
-- matter, na mesma ordem em que foi declarada. Nunca escreve nada de
-- volta no .qmd — o HTML só existe no documento renderizado, do mesmo
-- jeito que um listing nativo do Quarto (::: {#publications} :::) nunca
-- grava as fotos/textos que mostra de volta na página que os lista.
--
-- Front matter esperado (uma lista, não campos soltos no topo — um mapa
-- YAML comum não preserva a ordem de declaração ao chegar no Lua, uma
-- lista sim):
--
--     links:
--       - scholar-id: ibe0jfQAAAAJ
--       - github: marcosmrai
--       - linkedin: marcos-medeiros-raimundo-866b8731
--       - twitter: marcosmrai
--       - lattes: "1605909137233786"
--       - email: mraimundo@ic.unicamp.br
--
-- Numa publicação, os mesmos campos "github"/"pdf"/"slides"/"scholar"
-- guardam a URL completa (repositório do código, PDF do artigo, slides da
-- apresentação, página de citação no Scholar) — sem formato fixo pra
-- templatizar a partir de um handle, igual "website"/"email" acima.

local FIELD_DEFS = {
  ["scholar-id"] = {
    icon = "bi-mortarboard-fill",
    label = "Google Scholar",
    url = function(v) return "https://scholar.google.com/citations?user=" .. v .. "&hl=pt-BR" end,
  },
  github = {
    icon = "bi-github",
    label = "GitHub",
    url = function(v) return "https://github.com/" .. v end,
  },
  linkedin = {
    icon = "bi-linkedin",
    label = "LinkedIn",
    url = function(v) return "https://www.linkedin.com/in/" .. v .. "/" end,
  },
  twitter = {
    icon = "bi-twitter-x",
    label = "Twitter",
    url = function(v) return "https://twitter.com/" .. v end,
  },
  instagram = {
    icon = "bi-instagram",
    label = "Instagram",
    url = function(v) return "https://www.instagram.com/" .. v end,
  },
  website = {
    icon = "bi-globe2",
    label = "Website",
    url = function(v)
      if v:match("^https?://") then return v end
      return "https://" .. v
    end,
  },
  lattes = {
    icon = "bi-award",
    label = "Lattes",
    url = function(v) return "http://lattes.cnpq.br/" .. v end,
  },
  email = {
    icon = "bi-envelope",
    label = "Email",
    url = function(v) return "mailto:" .. v end,
  },
  -- Botões de recurso de uma publicação (::: {#links} ::: também é
  -- reutilizado em publications/*.qmd) — os três abaixo guardam a URL
  -- completa, como "website"/"email" acima, já que não têm um formato
  -- fixo pra templatizar a partir de um handle.
  scholar = {
    icon = "bi-mortarboard-fill",
    label = "Google Scholar",
    url = function(v) return v end,
  },
  pdf = {
    icon = "bi-file-earmark-pdf-fill",
    label = "PDF",
    url = function(v) return v end,
  },
  slides = {
    icon = "bi-easel-fill",
    label = "Slides",
    url = function(v) return v end,
  },
}

-- Pandoc chama as funções Div() de um filtro durante a mesma passagem em que
-- monta o Meta, mas na ordem dos blocos do documento — que vem ANTES do
-- front matter na travessia interna. Um filtro com Meta() e Div() separados
-- vê o Div antes do Meta ter rodado. Por isso tudo roda dentro de um único
-- Pandoc(doc), que já recebe doc.meta pronto antes de percorrer os blocos.
function Pandoc(doc)
  local links_meta = doc.meta.links
  if links_meta == nil then
    return doc
  end

  doc.blocks = doc.blocks:walk({
    Div = function(div)
      if div.identifier ~= "links" then
        return nil
      end

      local parts = {}
      for _, item in ipairs(links_meta) do
        for key, value in pairs(item) do
          local def = FIELD_DEFS[key]
          if def then
            local raw = pandoc.utils.stringify(value)
            -- e-mail não abre em nova aba (é mailto:, não um site externo)
            local attrs = key == "email" and "" or ' target="_blank" rel="me"'
            table.insert(parts, string.format(
              '<a href="%s" class="about-link"%s><i class="bi %s"></i> <span class="about-link-text">%s</span></a>',
              def.url(raw), attrs, def.icon, def.label
            ))
          end
        end
      end

      if #parts == 0 then
        return nil
      end

      div.content = {pandoc.RawBlock("html", table.concat(parts, "\n"))}
      return div
    end,
  })

  return doc
end
