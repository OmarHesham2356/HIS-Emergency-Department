#!/usr/bin/env bash
# Launch the ED HIS Streamlit app using nix develop
DIR="$(cd "$(dirname "$0")" && pwd)"
nix develop "$DIR" --command streamlit run "$DIR/app/app.py" "$@"
