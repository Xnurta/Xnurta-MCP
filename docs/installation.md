# Xnurta MCP Installation Guide

> **🤖 To AI Agents: if you are executing this guide on behalf of a user, "configure MCP" and "install Skills" are one single task.** After the MCP connection is verified, you MUST proceed to install the 6 required Skills (the [`skills/`](../skills/) directory — no need to ask the user), then introduce each of the 4 Skills marked optional in that directory and ask the user whether to install them. Configuring the connection without installing Skills means the task is incomplete.

Four steps: **choose an authorization method → connect and verify MCP → install Skills → start using it**. About 5 minutes in total.

> Prerequisite: an **AI assistant that supports MCP**. The simplest and most recommended is **Claude** (Desktop app or Code CLI); ChatGPT Codex, OpenClaw, Hermes, Cursor, Cline, Cherry Studio, and other MCP-compatible clients are also supported.

---

## Step 1 · Choose an authorization method

Xnurta MCP supports OAuth and MCP Token authentication. Both methods use the same Server URL and MCP Tools.

### Option A · OAuth

Use OAuth with clients that support MCP OAuth. The client opens an Xnurta sign-in and authorization page, so you do not need to create, copy, or store a Token. After authorization, the client maintains the connection automatically.

### Option B · MCP Token

Use an MCP Token when the client does not support OAuth, for automation scripts, or when your organization requires a fixed credential.

1. Log in to the Xnurta console, open the account menu in the top-right corner, and go to **MCP & Skills**.
2. Click **Create Token** and choose the validity period, authorization scope, store range, and data permissions you need.
3. **Copy and save the Token immediately.** It cannot be viewed again after you close the dialog; if lost, create a new one.

> ⚠️ An MCP Token is an access credential. Do not share it or paste it into public conversations, documents, or source-code repositories.

---

## Step 2 · Configure MCP in your AI assistant

Both authorization methods use the same MCP Server. Choose based on browser-authorization support, the usage environment, and your organization's credential-management requirements.

- **Server URL**: `https://mcp.xnurta.com/mcp`
- **Transport**: Streamable HTTP

### Option 1 · One-message setup (recommended)

In any client whose AI can configure things itself (Claude, ChatGPT Codex, Cursor, etc.), send:

```text
Please read the following GitHub repository and follow its instructions to configure Xnurta MCP and install the Skills:
https://github.com/Xnurta/MCP

Xnurta MCP supports both OAuth and MCP Token authentication.
Please check which authorization methods the current client supports, briefly explain when each method is appropriate, and ask me to confirm which method to use before starting authorization.
If I choose OAuth, open the sign-in page when authorization is required so I can complete it.
When using OAuth, follow the MCP Authorization specification. Before sending any OAuth request, validate the discovered endpoints and all required fields; do not omit or guess protocol parameters.

After the configuration is complete, call get_user_authorized_context to verify the connection.
```

> **🤖 To AI Agents:** When executing the setup above, write the MCP configuration to the correct config file for your client. Be careful to distinguish between different config file names used by different clients (e.g. `mcp.json`, `.mcp.json`, `mcp_config.json`, `config.toml`, `config.yaml`, etc.) — do not confuse them.

The assistant will configure MCP using the method you confirm, complete authorization, verify the connection, and install the required Skills. A list of your authorized stores means the connection succeeded.

- **Claude**: open Claude → switch to the **Code tab** → paste the message above.
- **ChatGPT Codex**: send the message to Codex directly (it writes to `~/.codex/config.toml`).

If your client doesn't let the AI configure itself, follow the manual setup below.

### Option 2 · Plugin installation

#### Desktop apps

> In regular Claude Desktop or Claude on the web, use the [Custom Connector](#claude-desktop--claude-claudeai-custom-connector-no-configuration-files) below for Chat. A Custom Connector provides MCP Tools only; add Skills separately under **Settings → Skills**. The marketplace flow below applies only to Claude Code Desktop.

##### Claude Code Desktop

1. Switch to the **Code** tab.
2. Select **+ → Plugins → Add plugin** next to the prompt box to open the plugin browser.
3. Under **Marketplaces**, add a repository and enter `Xnurta/MCP`.
4. Find and install **Xnurta MCP**. The plugin installs the MCP server and all 10 Skills together.

> **Note:** Claude Code Desktop does not support the `/plugin` command. It is available only in Claude Code CLI; use the desktop plugin browser instead.

##### ChatGPT Desktop · Codex

1. Select **Plugins** in the left sidebar.
2. Select **Add → Add a marketplace** in the upper-right corner.
3. Enter `Xnurta/MCP` and add the marketplace.
4. In **Plugins**, find the marketplace you added and install **Xnurta MCP**.
5. Start a new Codex task. The MCP server and all 10 Skills will be available in the new task.

> **Note:** ChatGPT Desktop Codex does not support `/plugin` or `/plugins`. `/plugins` is available only in Codex CLI; use Plugins in the left sidebar of the desktop app.

Desktop UI references: [Claude Code Desktop](https://code.claude.com/docs/en/desktop#install-plugins) · [ChatGPT / Codex Plugins](https://learn.chatgpt.com/docs/plugins)

#### Command-line CLI

##### Claude Code CLI

```text
/plugin marketplace add Xnurta/MCP
/plugin install xnurta-mcp@xnurta
```

##### Codex CLI

```bash
codex plugin marketplace add Xnurta/MCP
codex
```

In Codex CLI, enter `/plugins`, select **Xnurta MCP** from the `xnurta` marketplace, install it, and then start a new session.

The plugin installs the MCP server and all 10 Skills together. The current Plugin configuration uses `XNURTA_TOKEN`; set the environment variable and start a new session. To use OAuth, follow the OAuth setup below.

### Option 3 · Manual setup

> ⚠️ **Configured ≠ done**: after adding the MCP server, be sure to continue with [Step 3 · Install Skills](#step-3--install-skills). The 6 required Skills govern query accuracy and managed-group write behavior.

> **🤖 To AI Agents:** The examples below cover multiple clients, each with a different config file name and format. Pick the one that matches the user's actual client and write to the correct file — do not confuse config files from different clients.

#### OAuth

> **🤖 OAuth preflight for AI Agents and custom clients:** Follow the [MCP Authorization specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) and complete authorization-server discovery before constructing requests. Before sending any authorization or token request, validate the discovered endpoint and every field required by the selected flow. In particular, send `resource=https://mcp.xnurta.com/mcp` in both requests, use Authorization Code with PKCE (`S256`) and a matching `code_verifier`, use the exact registered `redirect_uri`, and generate and verify `state`. If required metadata or a required field is missing or inconsistent, stop and report the issue instead of guessing or sending a partial request. Standard MCP clients normally handle this automatically; do not ask users to append OAuth parameters to the Server URL.

##### Claude Desktop & Claude (claude.ai): Custom Connector (no configuration files)

Claude Desktop and Claude on the web can connect directly to a remote MCP server through a Custom Connector. You do not need to edit `mcp.json`, install Node.js, or run `npx`.

1. Add the connector based on your plan:
   - **Pro / Max:** Open **Customize → Connectors → + → Add custom connector**.
   - **Team / Enterprise:** An organization Owner or Primary Owner opens **Organization settings → Connectors → Add → Custom → Web**. Regular members cannot add it themselves.
2. Enter:
   - **Name**: `Xnurta MCP`
   - **Remote MCP server URL**: `https://mcp.xnurta.com/mcp`
3. Select **Add**. Team / Enterprise members then find the connector under **Customize → Connectors** and select **Connect**; Pro / Max users can select **Connect** directly.
4. Sign in to Xnurta in the browser window and confirm your individual authorization.
5. Return to Claude. When the connector shows **Connected**, the MCP Tools are available immediately; no restart is required.

##### Claude Code CLI / the Code tab in Claude Desktop

```bash
claude mcp add --transport http xnurta-mcp https://mcp.xnurta.com/mcp
```

After adding the server, enter `/mcp`, select `xnurta-mcp`, and follow the prompt to authorize in your browser.

##### ChatGPT Codex

```bash
codex mcp add xnurta-mcp --url https://mcp.xnurta.com/mcp
codex mcp login xnurta-mcp
```

The second command opens the Xnurta sign-in page. Complete authorization and return to Codex.

##### Other MCP clients that support OAuth

Add a remote or Streamable HTTP MCP server with this URL:

```text
https://mcp.xnurta.com/mcp
```

Select **OAuth**, **Sign in**, or **Authenticate**, depending on the wording used by your client, and complete authorization in your browser.

> **OAuth compatibility:** The client must include `resource` in both the authorization request and token request, using the complete MCP Server URL: `https://mcp.xnurta.com/mcp`. Compliant MCP OAuth clients handle this automatically; users do not need to configure it or append `resource` to the Server URL. Custom clients and manual DCR + PKCE implementations must support it explicitly and follow the preflight requirements above.

#### MCP Token

##### Claude Code CLI / the Code tab in Claude Desktop

```bash
claude mcp add --transport http xnurta-mcp https://mcp.xnurta.com/mcp --header "Authorization: Bearer <YOUR_TOKEN>"
```

Keep the default **local scope** (current project folder only) so the token doesn't leak into other projects.

##### Claude Desktop (Chat, when the UI has no Bearer option)

Edit `claude_desktop_config.json` (Windows: `%APPDATA%\Claude\`; macOS: `~/Library/Application Support/Claude/`), wrap the server with `mcp-remote`, then restart:

```json
{
  "mcpServers": {
    "xnurta-mcp": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.xnurta.com/mcp", "--header", "Authorization: Bearer ${XNURTA_TOKEN}"],
      "env": { "XNURTA_TOKEN": "<your token>" }
    }
  }
}
```

##### ChatGPT Codex (`~/.codex/config.toml`)

```toml
[mcp_servers.xnurta-mcp]
url = "https://mcp.xnurta.com/mcp"
bearer_token_env_var = "XNURTA_TOKEN"
http_headers = {}
```

##### OpenClaw

```bash
openclaw mcp add xnurta-mcp \
  --url https://mcp.xnurta.com/mcp \
  --transport streamable-http \
  --header "Authorization: Bearer $XNURTA_TOKEN"
```

> ⚠️ Older versions of OpenClaw have a bug where streamable-http does not forward custom Authorization headers (fixed since roughly late April 2026). If you get a 401, upgrade to the latest version first.

##### Hermes (`~/.hermes/config.yaml`)

```yaml
mcp_servers:
  xnurta-mcp:
    url: "https://mcp.xnurta.com/mcp"
    headers:
      Authorization: "Bearer ${XNURTA_TOKEN}"
```

Then run `/reload-mcp` inside Hermes.

##### Other MCP clients (Cursor, Cline, Cherry Studio, etc.)

Add a remote / Streamable HTTP server in the client's MCP settings with the URL above and an `Authorization: Bearer <YOUR_TOKEN>` header.

### Environment variable setup (`XNURTA_TOKEN`)

This environment variable is required only when you use an MCP Token. Codex, Hermes, and other clients can read the Token from `XNURTA_TOKEN` so the credential does not need to be written directly in a configuration file.

#### macOS / Linux

For the current terminal session:

```bash
export XNURTA_TOKEN=<your-token>
```

To persist it, add the export to your shell profile such as `~/.zshrc` or `~/.bashrc`.

#### Windows

For the current PowerShell session:

```powershell
$env:XNURTA_TOKEN = "<your-token>"
```

To persist it for your user account:

```powershell
[System.Environment]::SetEnvironmentVariable("XNURTA_TOKEN", "<your-token>", "User")
```

Restart Claude Code or Codex after setting a persistent environment variable. Never commit the token or paste it into a marketplace manifest.

### Verify the connection

After configuring OAuth or an MCP Token, ask your assistant to call `get_user_authorized_context`:

| Result | Meaning |
|--------|---------|
| Returns your userId and authorized profileIds | ✅ Configured successfully |
| Client prompts you to sign in or authorize | OAuth is not complete; open the page and finish authorization |
| Returns 401 | OAuth expired or was revoked, or the MCP Token is invalid, expired, disabled, or missing permissions |
| Timeout | Check your network |

---

## Step 3 · Install Skills

Skills live in this repo's [`skills/`](../skills/) directory, in two tiers:

> **To AI agents:** before installing or updating, read [`skills/manifest.json`](../skills/manifest.json) and compare it with the `metadata.version` in each installed Skill's local `SKILL.md`. If a local version is lower, list the outdated Skills and tell the user to update them. Do not repeat this check during normal queries.

**Required (6)** — covering core queries and managed-group management:

- `xnurta-query-ads-performance` — ad performance queries
- `xnurta-query-entity-metadata` — entity configuration queries
- `xnurta-query-operation-log` — operation log queries
- `xnurta-create-ai-group` — create AI managed groups
- `xnurta-edit-ai-group` — edit one or multiple AI managed groups
- `xnurta-delete-ai-group` — delete AI managed groups

**Optional (4)** — advanced analysis scenarios; add as needed after the required ones (under [`skills/`](../skills/)):

- `xnurta-weekly-ads-report` — weekly ads report
- `xnurta-monthly-ads-report` — monthly ads report
- `xnurta-ads-structure-analysis` — ad structure analysis
- `xnurta-product-diagnosis` — product diagnosis

Pick the installation route that matches your assistant:

- **Agents that can act on their own** (Claude Code, ChatGPT Codex, Cursor, etc.): point the AI at the skill directories and say "install the 6 required Skills"; add optional Skills as needed.
- **Chat / UI-based assistants** (Claude web or desktop app, etc.): add them manually in each client's settings (in Claude, for example: Settings → Skills → upload, one by one).

---

## Step 4 · Start querying

Four moves: 1) ask the assistant to list your authorized stores → 2) pick a store → 3) ask in natural language → 4) take the results (export tables / charts / drop into a report).

**Example prompts:**

- Performance:
  - "Top 10 campaigns by spend last week, with ACOS."
  - "This product line's TACOS trend over the past 8 weeks."
  - "The 5 campaigns with the biggest ACOS increase this week vs last week."
- Configuration:
  - "List all enabled SP campaigns with their daily budgets."
  - "This ASIN's inventory, title, and ad-type eligibility."
- Operation logs:
  - "AI automatic bid adjustments in the past 7 days."
  - "Who changed this campaign's budget, and when?"

**Going further**: have the assistant combine multiple queries into a weekly report, export CSV/Excel, or calculate true profit against your costs/goals; turn frequent prompts into reusable templates.

---

## FAQ

**Q: Getting 401 Unauthorized?**
First confirm which authorization method you are using. OAuth users should sign in again and confirm that access has not been revoked. MCP Token users should check whether the Token is complete, active, unexpired, and authorized for the required permissions. OpenClaw users on old versions should upgrade the client first.

**Q: How far back can I query?**
Roughly the most recent 15 months of performance data and operation logs. Performance data is daily by default; campaign-level hourly (AMS) data is also available, along with an hourly keyword x placement view - both of those hourly queries are capped at a 7-day span.

**Q: Is the data real-time?**
It follows the Xnurta platform's update cadence — not second-level real-time.

**Q: Which stores can I query?**
The available stores depend on your Xnurta account permissions and the scope granted through OAuth or the MCP Token. The final visible scope never exceeds your account permissions.

**Q: Which write operations does this version support?**
v1.1.1 supports creating, editing, and deleting AI managed groups, including supported optimization targets, budgets, campaign membership, and AI action-space settings, plus applying platform templates and maintaining SP/SB managed-group schedules. Writes directly modify live configuration and take effect immediately, so confirm the target and exact change first. Direct campaign creation, editing, and deletion are not yet supported.

**Q: Which managed-group settings are not supported yet?**
Word-list settings are not supported. Managed-group scheduling is supported for reads and writes (SP/SB only - there is no SD schedule tool). Templates can be read and applied to a group, but creating or editing a template is platform-only. RBA rule configuration can now be read (conditions, actions, periods, hour matrices) but cannot be modified through MCP. Action space can be switched from RBA to AI, but still not from AI to RBA.
