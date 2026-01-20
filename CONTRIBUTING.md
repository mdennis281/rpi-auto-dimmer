# Contributing to rpi-auto-dimmer

Thank you for your interest in contributing! We welcome bug reports, feature requests, and pull requests.

## How to Contribute

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally.
3. **Create a new branch** for your feature or bug fix.
4. **Make your changes** and commit them.
5. **Push to your fork** and submit a **Pull Request**.

## Testing Non-Main Branches

If you are testing a development branch that exists in the main repository (or if you are a maintainer), you can use the installation and update scripts to target a specific branch instead of `main`.

### Installing a specific branch

Use the `-b` (or `--branch`) flag with the installation script:

```bash
# Replace 'dev-branch' with the branch name you want to install
curl -sSL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/install.sh | bash -s -- -b dev-branch
```

### Updating to a specific branch

If you already have the tool installed, you can switch/update to a specific branch:

```bash
# Replace 'feature-branch' with the branch name you want to test
curl -sSL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/update.sh | bash -s -- -b feature-branch
```

> **Note:** The scripts currently retrieve files from the `mdennis281/rpi-auto-dimmer` repository. If you are testing changes from a **fork**, you will need to modify the script manually or download your fork's version of the files.
