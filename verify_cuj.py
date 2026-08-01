from playwright.sync_api import sync_playwright

def run_cuj(page):
    # 1. Login
    page.goto("http://localhost:8000/login")
    page.wait_for_timeout(500)
    page.get_by_label("Username").fill("admin")
    page.get_by_label("Password").fill("password")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(500)

    # 2. Add subject
    page.get_by_role("link", name="Add", exact=True).click()
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Add Subject").click()
    page.wait_for_timeout(500)
    page.get_by_label("Subject Name").fill("Math")
    page.get_by_label("Priority (1-10)").fill("5")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Add Subject").click()
    page.wait_for_timeout(500)

    # 3. Add chapter
    page.get_by_role("link", name="Add Chapter").click()
    page.wait_for_timeout(500)
    page.locator("#subject_id").select_option(label="Math")
    page.get_by_label("Chapter Name").fill("Algebra")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Add Chapter").click()
    page.wait_for_timeout(500)

    # 4. Add topic
    page.get_by_role("link", name="Add Topic").click()
    page.wait_for_timeout(500)
    # Select subject (which submits a form via onchange)
    page.locator("#subject_id").select_option(label="Math")
    page.wait_for_timeout(500)

    # Wait for page reload and subject to be selected
    page.locator("#chapter_id").select_option(label="Algebra")
    page.get_by_label("Topic Name").fill("Linear Equations")
    page.get_by_label("Priority (1-10)").fill("8")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Add Topic").click()
    page.wait_for_timeout(1000)

    # Take screenshot at the Add Topic page (to verify the redirect issue was fixed)
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    import os
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()  # MUST close context to save the video
            browser.close()