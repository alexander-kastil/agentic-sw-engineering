# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: order.spec.ts >> Food Shop Order Flow >> should order 1 falafel and 1 pad kra pao and submit to API
- Location: e2e\order.spec.ts:4:7

# Error details

```
TimeoutError: page.waitForSelector: Timeout 5000ms exceeded.
Call log:
  - waiting for locator('[class*="shop-item"]') to be visible

```

# Page snapshot

```yaml
- generic [ref=e4]:
  - heading "Error loading catalog" [level=2] [ref=e5]
  - paragraph [ref=e6]: Failed to fetch
  - button "Retry" [ref=e7] [cursor=pointer]
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Food Shop Order Flow', () => {
  4  |   test('should order 1 falafel and 1 pad kra pao and submit to API', async ({
  5  |     page,
  6  |   }) => {
  7  |     let orderRequest: any = null;
  8  |     let orderResponse: any = null;
  9  | 
  10 |     page.on('request', (request) => {
  11 |       if (request.url().includes('/orders') && request.method() === 'POST') {
  12 |         try {
  13 |           orderRequest = request.postDataJSON();
  14 |         } catch (e) {
  15 |           orderRequest = null;
  16 |         }
  17 |       }
  18 |     });
  19 | 
  20 |     page.on('response', async (response) => {
  21 |       if (response.url().includes('/orders') && response.request().method() === 'POST') {
  22 |         orderResponse = {
  23 |           status: response.status(),
  24 |           url: response.url(),
  25 |         };
  26 |       }
  27 |     });
  28 | 
  29 |     await page.goto('/');
  30 | 
> 31 |     await page.waitForSelector('[class*="shop-item"]', { timeout: 5000 });
     |                ^ TimeoutError: page.waitForSelector: Timeout 5000ms exceeded.
  32 | 
  33 |     const falafelItem = page.locator('[class*="shop-item"]').filter({
  34 |       has: page.locator('h3:has-text("Falafel Plate")'),
  35 |     });
  36 | 
  37 |     await expect(falafelItem).toBeVisible();
  38 | 
  39 |     const falafelAddBtn = falafelItem.locator('button[title="Add"]').first();
  40 |     await falafelAddBtn.click();
  41 | 
  42 |     const padKraPaoItem = page.locator('[class*="shop-item"]').filter({
  43 |       has: page.locator('h3:has-text("Pad Kra Pao")'),
  44 |     });
  45 | 
  46 |     await expect(padKraPaoItem).toBeVisible();
  47 | 
  48 |     const padKraPaoAddBtn = padKraPaoItem.locator('button[title="Add"]').first();
  49 |     await padKraPaoAddBtn.click();
  50 | 
  51 |     const cartItems = page.locator('[class*="cart-items"]');
  52 |     await expect(cartItems).toContainText('Items 2 in cart');
  53 | 
  54 |     const cartTotal = page.locator('[class*="cart-total"]');
  55 |     await expect(cartTotal).toContainText('28.00');
  56 | 
  57 |     const checkoutBtn = page.locator('[class*="checkout-btn"]');
  58 |     await expect(checkoutBtn).not.toBeDisabled();
  59 |     await checkoutBtn.click();
  60 | 
  61 |     const checkoutMessage = page.locator('[data-testid="checkout-message"]');
  62 |     await expect(checkoutMessage).toBeVisible({ timeout: 5000 });
  63 |     await expect(checkoutMessage).toContainText('created successfully');
  64 | 
  65 |     await page.waitForTimeout(500);
  66 | 
  67 |     expect(orderResponse).toBeTruthy();
  68 |     expect(orderResponse?.status).toBe(200);
  69 |     expect(orderResponse?.url).toContain('/orders');
  70 | 
  71 |     expect(orderRequest).toBeTruthy();
  72 |     expect(orderRequest.items).toHaveLength(2);
  73 | 
  74 |     const falafelInOrder = orderRequest.items.find(
  75 |       (item: any) => item.name.includes('Falafel')
  76 |     );
  77 |     expect(falafelInOrder).toBeTruthy();
  78 |     expect(falafelInOrder.quantity).toBe(1);
  79 |     expect(falafelInOrder.price).toBe(12);
  80 | 
  81 |     const padKraPaoInOrder = orderRequest.items.find(
  82 |       (item: any) => item.name.includes('Pad Kra Pao')
  83 |     );
  84 |     expect(padKraPaoInOrder).toBeTruthy();
  85 |     expect(padKraPaoInOrder.quantity).toBe(1);
  86 |     expect(padKraPaoInOrder.price).toBe(16);
  87 | 
  88 |     expect(
  89 |       orderRequest.items[0].price * orderRequest.items[0].quantity +
  90 |         orderRequest.items[1].price * orderRequest.items[1].quantity
  91 |     ).toBe(28);
  92 |   });
  93 | });
  94 | 
```