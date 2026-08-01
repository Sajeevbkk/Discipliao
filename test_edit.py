from playwright.sync_api import sync_playwright

def run(page):
    # 1. Login
    page.goto("http://localhost:8000/login")
    page.get_by_label("Username").fill("admin")
    page.get_by_label("Password").fill("password")
    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(500)

    # 2. Check edit page
    page.goto("http://localhost:8000/edit/")
    print(page.title())

    # 3. Check delete page
    page.goto("http://localhost:8000/delete/")
    print(page.title())

    # 4. Check timetable index page
    page.goto("http://localhost:8000/timetable/")
    print(page.title())

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    try:
        run(page)
    except Exception as e:
        print(f"Error: {e}")
    browser.close()
