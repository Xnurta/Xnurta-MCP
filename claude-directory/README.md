# Xnurta MCP · Claude plugin

Amazon Sponsored Ads intelligence for Claude: query advertising data, manage AI managed groups, create SP/SB/SD campaigns and portfolios, and edit supported live ad entities through Xnurta MCP.

This folder is the version submitted to the Claude plugin directory.

## Sign-in

The plugin connects to `https://mcp.xnurta.com/mcp` with OAuth. The first time a tool is used, Claude opens the Xnurta sign-in page; approve the stores and permissions you want to share. No token is stored in the plugin.

## Skills

21 Skills are included, including the MCP-only versions of `xnurta-sqp-insight` and
`xnurta-category-scorecard`. These two Skills use the remote MCP connection for
scoped read-only analysis and do not install or run local scripts.

## Maintainers

`skills/` here is generated. Edit the Skills at their source, then run `python tools/sync_claude_directory.py` from the repository root.

Privacy policy: https://www.xnurta.com/privacy-policy
