import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: './e2e/playwright',
    timeout: 30_000,
    expect: { timeout: 5_000 },
    retries: 0,
    reporter: [['list'], ['html']],
    use: {
        baseURL: 'http://localhost:4200',
        trace: 'on-first-retry',
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
    },
    webServer: {
        command: 'npm start',
        url: 'http://localhost:4200',
        reuseExistingServer: true,
        timeout: 120_000,
    },
    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
        },
    ],
});
