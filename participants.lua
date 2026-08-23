-- Preenche ::: {#participants} ::: na página de um projeto a partir da
-- lista "participants:" no front matter (ids de people/ ou scholar-ids
-- crus). Nunca escreve nada de volta no .qmd — o HTML só existe no
-- documento renderizado, do mesmo jeito que links.lua preenche
-- ::: {#links} ::: e que um listing nativo do Quarto (::: {#publications}
-- :::) nunca grava o que mostra de volta na página que os lista.
--
-- Front matter esperado — uma lista simples de ids:
--
--     participants: [mraimundo, pH1HRJoAAAAJ]
--
-- Cada id é ou um slug de people/<id>.qmd (alguém da equipe) ou um
-- scholar-id cru (colaborador externo, resolvido via
-- coauthors/coauthors.json — sem essa entrada ainda, aparece com ícone
-- genérico e o próprio id como nome, até alguém rodar
-- projects/_retreiver/fetch_participant_names.py).
--
-- O cabeçalho "Participants" só aparece quando há pelo menos um
-- participante resolvido — nada de seção vazia com título e sem conteúdo
-- (mesmo cuidado que levou ::: {#links} ::: a não ter heading próprio).

local IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}

-- io.open usa caminhos de sistema de arquivos relativos ao diretório do
-- ARQUIVO sendo renderizado (confirmado ao vivo: para projects/moml.qmd
-- o cwd é projects/, não a raiz do projeto) — diferente dos hrefs/srcs no
-- HTML gerado, que são raiz-relativos (começam com "/", resolvidos pelo
-- navegador a partir da raiz do site publicado, não do sistema de
-- arquivos). quarto.project.offset dá o caminho relativo do arquivo atual
-- até a raiz do projeto (".." para projects/moml.qmd, "../.." para a
-- cópia symlinkada projects/<username>/moml.qmd), mas só está disponível
-- de verdade dentro de uma função de filtro (não no topo do script) — por
-- isso é lido dentro de Pandoc(doc), não como local de módulo.
local root = "."

local function file_exists(path)
  local f = io.open(root .. "/" .. path, "rb")
  if f then
    f:close()
    return true
  end
  return false
end

local function read_file(path)
  local f = io.open(root .. "/" .. path, "rb")
  if not f then
    return nil
  end
  local content = f:read("*a")
  f:close()
  return content
end

local function find_person_image(person_id)
  for _, ext in ipairs(IMAGE_EXTENSIONS) do
    local candidate = "people/" .. person_id .. "." .. ext
    if file_exists(candidate) then
      return candidate:match("([^/]+)$")
    end
  end
  return person_id .. ".jpg"
end

local function person_title(person_id)
  local content = read_file("people/" .. person_id .. ".qmd")
  if not content then
    return person_id
  end
  local title = content:match('\ntitle:%s*"([^"]+)"') or content:match('^title:%s*"([^"]+)"')
  return title or person_id
end

local coauthors_cache = nil

local function load_coauthors()
  if coauthors_cache ~= nil then
    return coauthors_cache
  end
  local content = read_file("coauthors/coauthors.json")
  if not content then
    coauthors_cache = {}
    return coauthors_cache
  end
  local ok, decoded = pcall(pandoc.json.decode, content)
  coauthors_cache = ok and decoded or {}
  return coauthors_cache
end

local function render_card(person_id)
  if file_exists("people/" .. person_id .. ".qmd") then
    local name = person_title(person_id)
    local image = find_person_image(person_id)
    return string.format(
      '<a href="/people/%s.html"><img src="/people/%s" alt="%s"><span>%s</span></a>',
      person_id, image, name, name
    )
  end

  local registry = load_coauthors()
  local entry = registry[person_id]
  local name = (entry and entry.name) or person_id
  local href = string.format("https://scholar.google.com/citations?user=%s&hl=pt-BR", person_id)
  local img_or_icon
  if entry and entry.photo then
    img_or_icon = string.format('<img src="/coauthors/%s" alt="%s">', entry.photo, name)
  else
    img_or_icon = '<i class="bi bi-person-circle"></i>'
  end
  return string.format('<a href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>', href, img_or_icon, name)
end

function Pandoc(doc)
  local participants = doc.meta.participants
  if participants == nil then
    return doc
  end

  root = (quarto and quarto.project and quarto.project.offset) or "."

  local cards = {}
  for _, item in ipairs(participants) do
    table.insert(cards, render_card(pandoc.utils.stringify(item)))
  end

  if #cards == 0 then
    return doc
  end

  local html = "<h2>Participants</h2>\n<div class=\"project-participants\">\n"
    .. table.concat(cards, "\n") .. "\n</div>"

  doc.blocks = doc.blocks:walk({
    Div = function(div)
      if div.identifier ~= "participants" then
        return nil
      end
      div.content = {pandoc.RawBlock("html", html)}
      return div
    end,
  })

  return doc
end
