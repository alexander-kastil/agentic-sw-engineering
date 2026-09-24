import { test, expect } from '@playwright/test';

test.describe('Food Shop Order Flow', () => {
  test('should order 1 falafel and 1 pad kra pao and submit to API', async ({
    page,
  }) => {
    let orderRequest: any = null;
    let orderResponse: any = null;

    page.on('request', (request) => {
      if (request.url().includes('/orders') && request.method() === 'POST') {
        try {
          orderRequest = request.postDataJSON();
        } catch (e) {
          orderRequest = null;
        }
      }
    });

    page.on('response', async (response) => {
      if (response.url().includes('/orders') && response.request().method() === 'POST') {
        orderResponse = {
          status: response.status(),
          url: response.url(),
        };
      }
    });

    await page.goto('/');

    await page.waitForSelector('[class*="shop-item"]', { timeout: 5000 });

    const falafelItem = page.locator('[class*="shop-item"]').filter({
      has: page.locator('h3:has-text("Falafel Plate")'),
    });

    await expect(falafelItem).toBeVisible();

    const falafelAddBtn = falafelItem.locator('button[title="Add"]').first();
    await falafelAddBtn.click();

    const padKraPaoItem = page.locator('[class*="shop-item"]').filter({
      has: page.locator('h3:has-text("Pad Kra Pao")'),
    });

    await expect(padKraPaoItem).toBeVisible();

    const padKraPaoAddBtn = padKraPaoItem.locator('button[title="Add"]').first();
    await padKraPaoAddBtn.click();

    const cartItems = page.locator('[class*="cart-items"]');
    await expect(cartItems).toContainText('Items 2 in cart');

    const cartTotal = page.locator('[class*="cart-total"]');
    await expect(cartTotal).toContainText('28.00');

    const checkoutBtn = page.locator('[class*="checkout-btn"]');
    await expect(checkoutBtn).not.toBeDisabled();
    await checkoutBtn.click();

    const checkoutMessage = page.locator('[data-testid="checkout-message"]');
    await expect(checkoutMessage).toBeVisible({ timeout: 5000 });
    await expect(checkoutMessage).toContainText('created successfully');

    await page.waitForTimeout(500);

    expect(orderResponse).toBeTruthy();
    expect(orderResponse?.status).toBe(200);
    expect(orderResponse?.url).toContain('/orders');

    expect(orderRequest).toBeTruthy();
    expect(orderRequest.items).toHaveLength(2);

    const falafelInOrder = orderRequest.items.find(
      (item: any) => item.name.includes('Falafel')
    );
    expect(falafelInOrder).toBeTruthy();
    expect(falafelInOrder.quantity).toBe(1);
    expect(falafelInOrder.price).toBe(12);

    const padKraPaoInOrder = orderRequest.items.find(
      (item: any) => item.name.includes('Pad Kra Pao')
    );
    expect(padKraPaoInOrder).toBeTruthy();
    expect(padKraPaoInOrder.quantity).toBe(1);
    expect(padKraPaoInOrder.price).toBe(16);

    expect(
      orderRequest.items[0].price * orderRequest.items[0].quantity +
        orderRequest.items[1].price * orderRequest.items[1].quantity
    ).toBe(28);
  });
});
