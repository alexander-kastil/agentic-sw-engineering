import { test, expect } from '@playwright/test'

// Mirrors unit tests in src/App.test.tsx

test.describe('App E2E', () => {
    test('renders heading text', async ({ page }) => {
        await page.goto('/')
        await expect(page.getByRole('heading', { level: 1, name: 'React Food Shop' })).toBeVisible()
    })

    test('renders image with correct src', async ({ page }) => {
        await page.goto('/')
        const img = page.locator('img')

        await expect(img).toBeVisible()
        await expect(img).toHaveAttribute('src', 'food.png')
    })

    test('increments count on button click', async ({ page }) => {
        await page.goto('/')
        const button = page.getByRole('button', { name: 'Click Me!' })
        const paragraph = page.locator('p')

        await expect(paragraph).toContainText('Button clicked 0 times')
        await button.click()
        await expect(paragraph).toContainText('Button clicked 1 times')
    })
})
