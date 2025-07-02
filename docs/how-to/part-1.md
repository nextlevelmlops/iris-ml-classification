# <b>Creating the Development Environment</b>

## <b>How to install Git</b>
=== "Windows"

    ```
    winget install --id Git.Git -e --source winget
    ```

=== "macOS"

    ```
    brew install git
    ```

=== "Linux (Debian/Ubuntu)"

    ```
    sudo apt update
    sudo apt install git
    ```

## <b>How to install VsCode</b>
=== "Windows"

    ```bash
    # Download and install VS Code for Windows
    winget install --id Microsoft.VisualStudioCode
    ```

=== "macOS"

    ```
    # Download and install VS Code for macOS using Homebrew
    brew install --cask visual-studio-code
    ```

=== "Linux"

    ```
    # Download and install VS Code for Linux (Debian/Ubuntu example)
    sudo apt update
    sudo apt install wget gpg
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
    sudo install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/
    sudo sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
    sudo apt update
    sudo apt install code
    ```

---
## <b>How to Install the uv Python Package Manager</b>

The [`uv`](https://docs.astral.sh/uv/) package manager is a modern, ultra-fast tool for managing Python environments and dependencies. It’s written in Rust and can be installed on Windows, macOS, or Linux.

=== "Windows"

    ```
    # Install uv using PowerShell (recommended)
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

=== "macOS"

    ```
    # Install uv using the official install script
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Or with Homebrew
    brew install uv
    ```

=== "Linux"

    ```
    # Install uv using the official install script
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Or with wget if curl is not available
    wget -qO- https://astral.sh/uv/install.sh | sh
    ```

!!! warning "Security Tip"
    Before running any installation script from the internet, you can always inspect it first:
    - For bash: `curl https://astral.sh/uv/install.sh`
    - For PowerShell: `irm https://astral.sh/uv/install.ps1`

### Verifying Your Installation

After installing, check your `uv` version:

```
uv --version
```

You should see output like:
`uv 0.7.18 (abcdef12 2025-06-30)`

## What’s Next?

- [Official uv documentation](https://docs.astral.sh/uv/getting-started/installation/)
- [Getting started video tutorial](https://www.youtube.com/watch?v=QKVQQCx-gi4)

> **Tip:**
> uv is not only a package manager—it can also create and manage virtual environments, install Python itself, and much more. Try `uv --help` for an overview of its features.


## <b>How to SignUp Databricks Free Edition</b>

Getting started is refreshingly simple:

1. **Visit the [Databricks Free Edition signup page](https://www.databricks.com/product/data-intelligence-platform)**
   This is where you’ll begin your registration process.

2. **Choose your preferred signup method**
   You can sign up using Google, Microsoft, or your email address for maximum flexibility.

3. **Complete the registration**
   Fill in the required details. Databricks will provision your personal workspace immediately after you finish.

4. **Start exploring your workspace**
   Once inside, you’ll have access to a personal workspace with serverless compute and default storage, so you can begin experimenting and building right away.

!!! info "What is Databricks Free Edition?"
    Databricks Free Edition is a no-cost version of Databricks designed for students, educators, hobbyists, and anyone interested in learning or experimenting with data and AI. It’s ideal for learning, prototyping, and collaborative exploration, and includes many of the same features as the full Databricks platform in a serverless, quota-limited environment.

**Want a visual walkthrough?**
[Watch this step-by-step video guide on YouTube.](https://www.youtube.com/watch?v=4bV7k_5o7Zg)

## <b>How to create a Personal Access Token - PAT in Databricks Free Edition</b>
For Step-by-Step Instructions (Standard Workflow), follow these steps:

1. **Click your username in the top bar**
   This opens your user menu.

2. **Select User Settings**
   This brings you to your account and workspace configuration options.

3. **Navigate to Developer and the Access tokens, then click Manage**
   Here, you can view and manage your existing tokens.

4. **Click Generate new token and follow the prompts**
   You’ll be asked to name your token and set an optional expiration.

5. **Copy and save your new token**
   You will only see the token once. Store it securely!

!!! warning "Security Reminder"
    - **Do not share your personal access token with anyone.**
    - If you lose your token, you cannot retrieve it again—you must generate a new one.
    - Store your token in a secure location, such as a password manager.
    - If you believe your token has been compromised, revoke it immediately in the Access Tokens tab.

> **Tip:**
> You can also [watch this short video walkthrough](https://youtube.com/shorts/W_JgII34sBo?si=xbA9ZRsmi_8ReH2x) for a visual guide.

## <b>How to install Databricks CLI</b>
=== "Windows"

    ```
    # Using winget (recommended)
    winget search databricks
    winget install Databricks.DatabricksCLI

    # Or using Chocolatey (experimental)
    choco install databricks-cli

    # Alternatively, install via Windows Subsystem for Linux (WSL)
    # Then follow Linux instructions below inside WSL
    ```

=== "macOS"

    ```
    # Using Homebrew tap and install
    brew tap databricks/tap
    brew install databricks

    # Or using curl to download and install
    curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sudo sh
    ```

=== "Linux"

    ```
    # Using Homebrew (Linuxbrew)
    brew tap databricks/tap
    brew install databricks

    # Or using curl to download and install
    curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sudo sh
    ```

## <b>How to Authenticate the CLI with a Personal Access Token</b>
To use the CLI, you need to authenticate it with your Databricks workspace. The most common method is with a Personal Access Token.

How to Authenticate
Generate a Personal Access Token in your Databricks workspace (navigate to User Settings > Access Tokens).

Configure the CLI by running:

```bash
databricks configure
```
You’ll be prompted for:

Databricks Host: Enter your workspace URL (e.g., https://dbc-xxxx.cloud.databricks.com).

Personal Access Token: Paste the token you generated.

This creates a .databrickscfg configuration file in your home directory (%USERPROFILE% on Windows, ~ on macOS/Linux).

“After you enter your Databricks personal access token, a corresponding configuration profile is added to your .databrickscfg file. You can now use the Databricks CLI’s --profile option to specify different configurations.”

!!! warning "Common Pitfalls and How to Avoid Them"
    - Forgetting to set permissions: Always manage access at the catalog and schema levels to prevent unauthorized data access.
    - Losing your access token: Store it securely. If lost, revoke and regenerate it.
    - CLI installation issues: Ensure your package manager is up-to-date and that your PATH includes the CLI binary.
