#!/usr/bin/env bash
# LabX Remote - Unix/macOS Automated Installer
set -e

INSTALL_DIR="${HOME}/.local/bin"
RELEASE_URL="${LABX_RELEASE_URL:-https://labx-remote.netlify.app/downloads/labx-linux}"

echo "=========================================================="
echo " LabX Remote - Linux / macOS Installer"
echo "=========================================================="

mkdir -p "${INSTALL_DIR}"
TARGET="${INSTALL_DIR}/labx"

echo "Downloading LabX..."
if command -v curl >/dev/null 2>&1; then
    curl -fsSL "${RELEASE_URL}" -o "${TARGET}"
elif command -v wget >/dev/null 2>&1; then
    wget -qO "${TARGET}" "${RELEASE_URL}"
else
    echo "Error: curl or wget is required." >&2
    exit 1
fi

chmod +x "${TARGET}"

# Configure PATH in shell rc if not already present
case ":${PATH}:" in
    *:"${INSTALL_DIR}":*) ;;
    *)
        SHELL_RC="${HOME}/.bashrc"
        if [ -n "$ZSH_VERSION" ] || [ -f "${HOME}/.zshrc" ]; then
            SHELL_RC="${HOME}/.zshrc"
        fi
        echo "export PATH=\"${INSTALL_DIR}:\$PATH\"" >> "${SHELL_RC}"
        echo "Added ${INSTALL_DIR} to ${SHELL_RC}."
        ;;
esac

echo "=========================================================="
echo " LabX Remote installed to ${TARGET}"
echo " Run 'labx list' to get started."
echo "=========================================================="

