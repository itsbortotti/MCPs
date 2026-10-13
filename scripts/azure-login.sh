#!/usr/bin/env bash
set -euo pipefail
echo "Opening Azure login (browser)..."
az login
echo
echo "Subscriptions available:"
az account list -o table
echo
echo "Set the active subscription with:"
echo "  az account set --subscription \"<name-or-id>\""
