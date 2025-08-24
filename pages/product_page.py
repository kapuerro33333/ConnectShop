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

    def _go_to_pdp(self) -> None:
        """Якщо ще не на PDP — відкриваємо перший продукт (overlay → grid)."""
        if "/products/" in self.page.url:
            return

        # Спробувати клікнути з overlay, якщо він видимий
        if self.overlay_first_link.count() > 0 and self.overlay_first_link.is_visible():
            self.overlay_first_link.click()
        else:
            # Інакше — з гріда
            self.grid_first_link.wait_for(state="visible", timeout=10000)
            self.grid_first_link.click()

        # Очікуємо перехід на PDP і появу кнопки Add to cart
        self.page.wait_for_url("**/products/**", timeout=10000)
        expect(self.pdp_add_btn).to_be_visible(timeout=10000)

    @allure.step("Add product to cart and validate")
    def add_to_cart(self) -> None:
        # Гарантовано переходимо на PDP
        self._go_to_pdp()

        # Якщо є селекти з варіантами — спробувати вибрати перший доступний
        variant_select = self.page.locator("form[action*='/cart/add'] select").first
        if variant_select.count() > 0:
            try:
                variant_select.select_option(index=1)  # пропустимо placeholder
            except Exception:
                pass  # якщо немає — ігноруємо

        # Клік по Add to cart
        expect(self.pdp_add_btn).to_be_enabled(timeout=10000)
        self.pdp_add_btn.click()

        # Перевірка, що корзина оновилась (з'явився бейдж або число > 0)
        expect(self.cart_badge).to_be_visible(timeout=10000)
        expect(self.cart_badge).to_have_text(re.compile(r"\d+"), timeout=10000)