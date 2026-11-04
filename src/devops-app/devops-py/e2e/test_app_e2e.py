from playwright.sync_api import Page, expect


def test_renders_heading_text(page: Page):
    page.goto("/")

    expect(page.get_by_role("heading", level=1, name="Python Food Shop")).to_be_visible()


def test_renders_image_with_correct_src(page: Page):
    page.goto("/")
    img = page.locator("img")

    expect(img).to_be_visible()
    expect(img).to_have_attribute("src", "food.png")


def test_increments_count_on_button_click(page: Page):
    page.goto("/")
    button = page.get_by_role("button", name="Click Me!")
    paragraph = page.locator("p")

    expect(paragraph).to_contain_text("Button clicked 0 times")
    button.click()
    expect(paragraph).to_contain_text("Button clicked 1 times")
