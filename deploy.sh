#!/bin/bash
#
# Substitui o fluxo antigo (Hugo) por Quarto:
#   --render  -> equivalente a `hugo` (build do site) -> `quarto render`
#   --update  -> git add + commit + push, depois entra no servidor via SSH
#                e faz `git pull` na pasta do site (antes "Hugo", agora
#                "homepage")
#
# Uso:
#   ./deploy.sh --render                  # só renderiza o site localmente
#   ./deploy.sh --update                  # commit+push+pull remoto (usa uma
#                                          # mensagem de commit padrão com a
#                                          # data/hora)
#   ./deploy.sh --update "mensagem"       # commit+push+pull remoto com
#                                          # mensagem de commit específica
#   ./deploy.sh --render --update         # renderiza e, se der certo, publica

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

SSH_HOST="mraimundo@ssh.ic.unicamp.br"
REMOTE_DIR="homepage"

do_render() {
  echo "🚀 Renderizando o site (quarto render)..."
  # O quarto tem uma falha conhecida e intermitente neste projeto: um erro
  # de "rename"/"stat" no fim do render, mesmo com o site inteiro já
  # construído corretamente (visto repetidamente nesta sessão) — tentamos
  # de novo automaticamente antes de desistir de verdade.
  local attempt
  for attempt in 1 2 3; do
    if quarto render; then
      echo "✅ Site renderizado (_site/)."
      return 0
    fi
    echo "⚠️  Falha na tentativa $attempt/3 (pode ser a falha conhecida do quarto ao final do render) — tentando de novo..."
  done
  echo "❌ Render falhou 3 vezes seguidas. Confira o erro acima."
  return 1
}

do_update() {
  local message="${1:-"Update $(date '+%Y-%m-%d %H:%M')"}"

  echo "📦 git add..."
  git add -A

  if git diff --cached --quiet; then
    echo "ℹ️  Nada para commitar."
  else
    echo "📝 git commit -m \"$message\"..."
    git commit -m "$message"
  fi

  echo "⬆️  git push..."
  git push

  echo "🌐 Atualizando o servidor ($SSH_HOST, pasta $REMOTE_DIR)..."
  ssh "$SSH_HOST" -t "cd $REMOTE_DIR; git pull"

  echo "✅ Publicado."
}

if [[ $# -eq 0 ]]; then
  echo "Uso: $0 [--render] [--update [\"mensagem de commit\"]]"
  exit 1
fi

RENDER=false
UPDATE=false
COMMIT_MESSAGE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --render)
      RENDER=true
      shift
      ;;
    --update)
      UPDATE=true
      shift
      # a mensagem de commit é opcional: só consome o próximo argumento se
      # ele não for outra flag
      if [[ $# -gt 0 && "$1" != --* ]]; then
        COMMIT_MESSAGE="$1"
        shift
      fi
      ;;
    *)
      echo "Opção desconhecida: $1"
      exit 1
      ;;
  esac
done

if [[ "$RENDER" == true ]]; then
  do_render
fi

if [[ "$UPDATE" == true ]]; then
  do_update "$COMMIT_MESSAGE"
fi
