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

    # 2. Check edit subjects page
    page.goto("http://localhost:8000/edit/")
    page.wait_for_timeout(500)

    # We click the first link to check if edit page opens properly with bootstrap
    try:
        page.locator(".list-group-item").first.click()
        page.wait_for_timeout(1000)
        page.screenshot(path="/home/jules/verification/screenshots/edit_subject.png")
    except Exception as e:
        print(f"Could not click edit link: {e}")
        pass

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
