import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
    testDir: './e2e/playwright',
    timeout: 30_000,
    expect: { timeout: 5_000 },
    retries: 0,
    reporter: [['list'], ['html'], ['junit', { outputFile: 'test-results/junit.xml' }]],
    use: {
        baseURL: 'http://localhost:4173',
        trace: 'on-first-retry',
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
    },
    webServer: {
        command: 'npm run dev -- --host --port 4173',
        url: 'http://localhost:4173',
        reuseExistingServer: true,
        timeout: 120_000,
    },
    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
        },
    ],
})
