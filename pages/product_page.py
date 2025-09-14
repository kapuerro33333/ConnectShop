import re
import allure
from playwright.sync_api import Page, expect


class ProductPage:
    def __init__(self, page: Page):
        self.page = page

        # Перший лінк на продукт в overlay (predictive search)
        self.overlay_first_link = page.locator(
            "predictive-search .predictive-search__results a.full-unstyled-link[href*='/products/']"
        ).first

        # Перший лінк на продукт у гріді /search
        self.grid_first_link = page.locator(
            "main a.full-unstyled-link[href*='/products/']"
        ).first

        # Кнопка Add to cart на PDP
        self.pdp_add_btn = page.locator(
            "product-form form[action*='/cart/add'] button[name='add']"
        ).first

        # Бейджик кількості в корзині
        self.cart_badge = page.locator(
            "a[href*='/cart'] .cart-count-bubble, .cart-icon-bubble, .header__cart-count-bubble"
        ).first

        # Повідомлення "No results found"
        self.no_results_msg = page.locator("p.alert.alert--warning").first

    # ---------------- Навігація на PDP ----------------
    def _go_to_pdp(self) -> None:
        """Якщо ще не на PDP — відкриваємо перший продукт (overlay → grid)."""
        if "/products/" in self.page.url:
            return

        if self.overlay_first_link.count() > 0 and self.overlay_first_link.is_visible():
            self.overlay_first_link.click()
        else:
            self.grid_first_link.wait_for(state="visible", timeout=10000)
            self.grid_first_link.click()

        self.page.wait_for_url("**/products/**", timeout=10000)
        expect(self.pdp_add_btn).to_be_visible(timeout=10000)

    # ---------------- Додавання у кошик ----------------
    @allure.step("Add product to cart and validate")
    def add_to_cart(self) -> None:
        # Гарантовано переходимо на PDP
        self._go_to_pdp()

        expect(self.pdp_add_btn).to_be_enabled(timeout=10000)
        self.pdp_add_btn.click()

        try:
            self.page.wait_for_selector("div.cart-notification", state="visible", timeout=10000)
            text = self.page.locator("div.cart-notification").inner_text()
            allure.attach(body=text, name="Cart notification", attachment_type=allure.attachment_type.TEXT)
            assert "added to your cart" in text
        except Exception:
            expect(self.cart_badge).to_be_visible(timeout=10000)
            expect(self.cart_badge).to_have_text(re.compile(r"\d+"), timeout=10000)

    # ---------------- Негативний пошук ----------------
    @allure.step("Validate 'No results found' message is visible")
    def validate_no_product_found(self) -> None:
        expect(self.no_results_msg).to_be_visible(timeout=5000)
        text = self.no_results_msg.text_content() or ""
        allure.attach(body=text, name="No results message", attachment_type=allure.attachment_type.TEXT)
        assert "no results" in text.lower(), f"Unexpected no-results message: '{text}'"

    # ---------------- Кошик: допоміжні дії ----------------
    @allure.step("Open cart page")
    def open_cart(self) -> None:
        """Відкриває /cart і чекає, поки форма корзини буде видима."""
        if "/cart" not in self.page.url:
            self.page.goto("/cart")
        self.page.wait_for_selector(
            "form[action*='/cart'], .cart__items, cart-items",
            state="visible",
            timeout=10_000,
        )

    @allure.step("Set cart quantity to {value}")
    def set_quantity(self, value: int) -> None:
        """
        Ставить кількість першого товару у кошику.
        Для value < 1 перевіряє, що магазин не приймає негатив/нуль.
        """
        self.open_cart()

        qty_input = self.page.locator(
            "input[name='quantity'], input[id^='Quantity-'], input[name='updates[]'], cart-items input[type='number']"
        ).first
        expect(qty_input).to_be_visible(timeout=5000)

        before = qty_input.input_value() or "1"
        qty_input.fill(str(value))

        # Тригеримо події
        try:
            qty_input.dispatch_event("input")
            qty_input.dispatch_event("change")
        except Exception:
            pass
        self.page.keyboard.press("Tab")

        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass

        after = qty_input.input_value() or before
        allure.attach(
            body=f"Before: {before}, After: {after}, Tried: {value}",
            name="Quantity change details",
            attachment_type=allure.attachment_type.TEXT,
        )

        if value < 1:
            try:
                assert int(after) >= 1, f"Cart accepted invalid quantity ({after})!"
            except ValueError:
                assert after.strip() != "", "Cart accepted invalid empty quantity!"
        else:
            try:
                assert int(after) == int(value), f"Quantity not set correctly: {after} != {value}"
            except ValueError:
                raise AssertionError(f"Quantity input is not numeric after change: '{after}'")

    @allure.step("Remove first item from cart")
    def remove_from_cart(self) -> None:
        """Видаляє перший товар і перевіряє, що кошик спорожнів або кількість позицій зменшилась."""
        self.open_cart()

        remove_btn = self.page.locator(
            "button[aria-label^='Remove'], a.cart__remove, button[name='remove'], button:has(.icon-remove)"
        ).first

        if remove_btn.count() == 0:
            qty_input = self.page.locator(
                "input[name='quantity'], input[id^='Quantity-'], input[name='updates[]'], cart-items input[type='number']"
            ).first
            expect(qty_input).to_be_visible(timeout=5000)
            qty_input.fill("0")
            try:
                qty_input.dispatch_event("input")
                qty_input.dispatch_event("change")
            except Exception:
                pass
            self.page.keyboard.press("Tab")
        else:
            remove_btn.click()

        self.page.wait_for_load_state("networkidle", timeout=10_000)

        empty_msg = self.page.locator(
            "div.cart__empty, p:has-text('Your cart is empty'), #cart .is-empty, cart-items:has-text('Your cart is empty')"
        )
        items = self.page.locator(".cart__items .cart-item, tr.cart__row, cart-items .cart-item")

        is_empty = (empty_msg.count() > 0) and empty_msg.first.is_visible()
        rows_count = items.count()
        no_rows = rows_count == 0

        allure.attach(
            body=f"is_empty_msg={is_empty}, item_rows={rows_count}",
            name="Remove result",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert is_empty or no_rows, "Cart not empty after removing product!"