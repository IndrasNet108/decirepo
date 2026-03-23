#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$ROOT_DIR/site-dist"

mkdir -p "$DIST_DIR"

copy_file_if_exists() {
  local rel="$1"
  if [[ -f "$ROOT_DIR/$rel" ]]; then
    mkdir -p "$DIST_DIR/$(dirname "$rel")"
    cp "$ROOT_DIR/$rel" "$DIST_DIR/$rel"
  fi
}

copy_tree_if_exists() {
  local rel="$1"
  if [[ -d "$ROOT_DIR/$rel" ]]; then
    mkdir -p "$DIST_DIR"
    cp -a "$ROOT_DIR/$rel" "$DIST_DIR/"
  fi
}

# Core public site surface.
copy_file_if_exists "index.html"
copy_tree_if_exists ".well-known"
copy_tree_if_exists "pages"
copy_tree_if_exists "assets"
copy_tree_if_exists "components"
copy_tree_if_exists "api"
copy_tree_if_exists "artifacts"

# Optional top-level web assets, if present in the repository.
copy_file_if_exists "favicon.ico"
copy_file_if_exists "favicon-32x32.png"
copy_file_if_exists "favicon-16x16.png"
copy_file_if_exists "apple-touch-icon.png"
copy_file_if_exists "site.webmanifest"
copy_file_if_exists "robots.txt"
copy_file_if_exists "CNAME"

printf 'site-dist build complete at %s\n' "$DIST_DIR"
