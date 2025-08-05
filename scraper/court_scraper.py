# court_scraper.py — Delhi High Court scraper using Playwright + BeautifulSoup

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Main async function to extract data from Delhi High Court portal
async def fetch_case_data_async(case_type, case_number, filing_year, use_mock=False):
    # Mock data shortcut (✔️ Used in web testing)
    if use_mock:
        return {
            "parties": "A vs B",
            "filling_date": "2023-01-10",
            "next_hearing_date": "2023-08-10",
            "pdf_link": "https://example.com/order1.pdf"
        }, "<html>Mock raw HTML response</html>"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to the case search form page
        await page.goto("https://delhihighcourt.nic.in/app/get-case-type-status", timeout=60000)

        # Example: fill in form fields — you will need to inspect the actual form field names/IDs
        await page.select_option("select[name='ddlCaseType']", case_type)
        await page.fill("input[name='txtCaseNo']", case_number)
        await page.fill("input[name='txtCaseYear']", filing_year)

        await page.click("input[name='btnSubmit']")
        await page.wait_for_load_state("networkidle")

        # Extract page content and parse with BeautifulSoup
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')

        # Extract required data (update selectors as per actual content)
        case_data = {
            "parties": soup.find('span', id='lblParties').text.strip() if soup.find('span', id='lblParties') else "N/A",
            "filing_date": soup.find('span', id='lblFilingDate').text.strip() if soup.find('span', id='lblFilingDate') else "N/A",
            "next_hearing_date": soup.find('span', id='lblNextDate').text.strip() if soup.find('span', id='lblNextDate') else "N/A",
            "pdf_link": None
        }

        # Try to find the latest judgment/order PDF link
        pdf_link_tag = soup.find('a', href=True, text=lambda t: t and 'Order' in t or 'Judgment' in t)
        if pdf_link_tag:
            case_data["pdf_link"] = "https://delhihighcourt.nic.in/" + pdf_link_tag['href'].lstrip("./")

        await browser.close()
        return case_data, html

# Synchronous wrapper for Flask integration
def fetch_case_data(case_type, case_number, filing_year, use_mock=False):
    return asyncio.run(fetch_case_data_async(case_type, case_number, filing_year, use_mock=use_mock))

"""
CAPTCHA Handling

The Delhi High Court portal does not use any image- or puzzle-based CAPTCHA on the public case status page (https://delhihighcourt.nic.in/case.asp).

Therefore, no CAPTCHA-solving service was required.

However, the site relies on ASP.NET Web Forms, which include dynamic fields like `__VIEWSTATE`, `__EVENTVALIDATION`, and postback logic. These fields are essential to simulate a real user interaction.

To legally and reliably bypass this complexity, we used **Playwright**, which launches a headless browser and behaves exactly like a human user — clicking the dropdown, filling form fields, and submitting the case search form.

This ensures compatibility without violating terms of service or needing manual CAPTCHA-solving methods.
"""
