$servers = copilot mcp list

if ($servers -notmatch 'work-iq') {
    copilot mcp add work-iq -- npx -y @microsoft/workiq mcp
}

if ($servers -notmatch 'microsoft-learn') {
    copilot mcp add --transport http microsoft-learn https://learn.microsoft.com/api/mcp
}

copilot mcp list

npx -y @microsoft/workiq accept-eula
npx -y @microsoft/workiq auth login
npx -y @microsoft/workiq search-paths --filter "sites|lists"
