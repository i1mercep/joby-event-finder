#!/bin/bash

# Exit immediately if a pipeline exits with a non-zero status.
set -e

# function to compile a given requirements*.in file using `uv pip compile``
# $(1) - output file to generate
# $(2+) - extra / optional dependancies
uv_compile_reqfile() {
    echo "Compiling ${1}"
    if [ -n "${2}" ]; then
        uv pip compile -q --extra "${@:2}" --output-file "${1}" pyproject.toml
    else
        uv pip compile -q --output-file "${1}" pyproject.toml
    fi
    chown "${EXTERNAL_UID}:${EXTERNAL_GID}" "${1}"
}

uv_compile_reqfile "requirements.txt"
uv_compile_reqfile "requirements_dev.txt" "dev"
