#!/usr/bin/env bash
# Publica las páginas de docs/wiki/ en la Wiki de GitHub del repositorio.
#
# Pasos:
# 1. Deduce la URL de la wiki a partir del remoto "origin" y la clona al
#    mismo nivel que este repositorio (<repositorio>.wiki/); si ya está
#    clonada, la actualiza.
# 2. Reemplaza su contenido por las páginas de docs/wiki/ y las imágenes de
#    docs/figuras/, para que la wiki quede igual a esas carpetas. No se
#    copia nada más.
# 3. Hace commit y push; si nada cambió, no publica nada.
#
# Requisito: la Wiki debe estar activada en GitHub y tener al menos una
# página creada desde la web (hasta entonces el repositorio no existe).
#
# Uso:
#   scripts/publish_wiki.sh            copia, hace commit y push
#   scripts/publish_wiki.sh --no-push  hace todo salvo el push, para revisar
#                                      el commit en la carpeta de la wiki
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

push=true
case "${1:-}" in
    "") ;;
    --no-push) push=false ;;
    *) echo "Opción desconocida: $1 (use --no-push)" >&2; exit 2 ;;
esac

origin="$(git -C "$ROOT" remote get-url origin)"
WIKI_URL="${origin%.git}.wiki.git"
repo_name="$(basename "${origin%.git}")"
WIKI_DIR="$(dirname "$ROOT")/$repo_name.wiki"
wiki_page="${origin%.git}/wiki"
wiki_page="${wiki_page/#git@github.com:/https://github.com/}"

if [ -d "$WIKI_DIR/.git" ]; then
    echo "Actualizando la wiki en $WIKI_DIR"
    git -C "$WIKI_DIR" pull --quiet --ff-only
else
    echo "Clonando la wiki en $WIKI_DIR"
    if ! git clone --quiet "$WIKI_URL" "$WIKI_DIR"; then
        repo_page="${wiki_page%/wiki}"
        cat >&2 <<EOF
No se pudo clonar la wiki: GitHub no crea su repositorio hasta que exista
la primera página. Antes de volver a ejecutar este script:
  1. En $repo_page/settings, sección Features, marque "Wikis".
  2. En $wiki_page, pulse "Create the first page" y guárdela con
     cualquier texto (este script la reemplaza por docs/wiki/Home.md).
EOF
        exit 1
    fi
fi

# Se borra lo anterior para que no queden páginas ni imágenes eliminadas.
rm -rf "$WIKI_DIR"/*.md "$WIKI_DIR/images"
cp "$ROOT"/docs/wiki/*.md "$WIKI_DIR/"
mkdir "$WIKI_DIR/images"
cp "$ROOT"/docs/figuras/*.png "$ROOT"/docs/figuras/*.jpg "$WIKI_DIR/images/"

cd "$WIKI_DIR"
git add --all
if ! git diff --cached --quiet; then
    git commit --quiet -m "Actualizar la wiki desde docs/wiki"
    git show --stat --format="Commit: %h %s" HEAD
fi

# Commits sin publicar, incluidos los de una ejecución con --no-push.
pending="$(git rev-list --count '@{upstream}..HEAD')"
if [ "$pending" -eq 0 ]; then
    echo "La wiki ya está actualizada; no hay nada que publicar."
elif $push; then
    git push --quiet
    echo "Wiki publicada: $wiki_page"
else
    echo "Push omitido (--no-push): $pending commit(s) sin publicar" \
        "en $WIKI_DIR"
fi
