import { test, expect } from '@playwright/test';

test.describe('Food Shop Order Flow', () => {
    test('should order 1 falafel and 1 pad kra pao and submit to API', async ({ page }) => {
        await page.goto('/food');

        const falafel = page.locator('app-shop-item').filter({ hasText: 'Falafel Plate' });
        await expect(falafel).toBeVisible();
        await falafel.locator('mat-icon', { hasText: 'add_circle_outline' }).click();

        const padKraPao = page.locator('app-shop-item').filter({ hasText: 'Pad Kra Pao' });
        await expect(padKraPao).toBeVisible();
        await padKraPao.locator('mat-icon', { hasText: 'add_circle_outline' }).click();

        const sidebar = page.locator('app-sidebar');
        await expect(sidebar).toContainText('2 items in cart');
        await expect(sidebar).toContainText('28.00 €');

        await sidebar.locator('button', { hasText: 'Checkout' }).click();
        await expect(page).toHaveURL(/\/food\/checkout$/);

        const orderResponsePromise = page.waitForResponse(
            (response) => response.url().includes('/orders') && response.request().method() === 'POST'
        );

        const completeBtn = page.getByRole('button', { name: 'Complete Checkout' });
        await expect(completeBtn).toBeEnabled();
        await completeBtn.click();

        const orderResponse = await orderResponsePromise;
        expect(orderResponse.status()).toBe(200);
        expect(orderResponse.url()).toContain('/orders');

        const orderRequest = orderResponse.request().postDataJSON();
        expect(orderRequest.items).toHaveLength(2);

        const falafelInOrder = orderRequest.items.find((item: any) => item.name.includes('Falafel'));
        expect(falafelInOrder).toBeTruthy();
        expect(falafelInOrder.quantity).toBe(1);
        expect(falafelInOrder.price).toBe(12);

        const padKraPaoInOrder = orderRequest.items.find((item: any) =>
            item.name.includes('Pad Kra Pao')
        );
        expect(padKraPaoInOrder).toBeTruthy();
        expect(padKraPaoInOrder.quantity).toBe(1);
        expect(padKraPaoInOrder.price).toBe(16);

        await expect(page.locator('app-checkout-response')).toContainText('Your order was submitted');
    });
});
