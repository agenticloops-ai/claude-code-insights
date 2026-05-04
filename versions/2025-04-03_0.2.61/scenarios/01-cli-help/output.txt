Usage: claude [options] [command] [prompt]

Claude Code - starts an interactive session by default, use -p/--print for
non-interactive output

Arguments:
  prompt                          Your prompt

Options:
  -d, --debug                     Enable debug mode
  --verbose                       Override verbose mode setting from config
  -p, --print                     Print response and exit (useful for pipes)
  --json                          Output JSON in the shape {cost_usd: number,
                                  duration_ms: number, duration_api_ms: number,
                                  result: string} (only works with --print)
  --mcp-debug                     Enable MCP debug mode (shows MCP server
                                  errors)
  --dangerously-skip-permissions  Bypass all permission checks. Only works in
                                  Docker containers with no internet access.
  --allowedTools <tools...>       Comma or space-separated list of tool names
                                  to allow (e.g. "Bash(git*) Edit Replace")
  -v, --version                   output the version number
  -h, --help                      display help for command

Commands:
  config                          Manage configuration (eg. claude config set
                                  -g theme dark)
  mcp                             Configure and manage MCP servers
  migrate-installer               Migrate from global npm installation to local
                                  installation
  doctor                          Check the health of your Claude Code
                                  auto-updater
  update                          Check for updates and install if available
