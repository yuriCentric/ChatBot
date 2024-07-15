from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class UMXFormAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=MMz41rvepkGceAUWwYX6DarzE7_JLf5NhG5bjg7XEetUNTBPMTZFR1g5U1Y5NVc2Q1BBT0VDQTVOUS4u")
        print("Navigated to UMX form URL.")

    def scroll_down(self):
        try:
            self.driver.execute_script("window.scrollBy(0, 900);")
            print("Scrolled down one screen size (900 pixels).")
            return True
        except Exception as e:
            print(f"Error scrolling down: {e}")
            return False

    def select_role(self, role):
        try:
            role = role.lower()
            if role == "client":
                client_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox' and @title='Client']")
                client_checkbox.click()
                print("Selected 'Client' checkbox.")
            elif role == "employee":
                employee_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox' and @title='Employee']")
                employee_checkbox.click()
                print("Selected 'Employee' checkbox.")
            return True
        except Exception as e:
            print(f"Error selecting role: {e}")
            return False

    def enter_name(self, name):
        try:
            name_field = self.driver.find_element(By.XPATH, "//input[@type='text' and @aria-label='Who is this Unmatched Minute about? Please include first and last names (or \"self\", if applicable)']")
            name_field.send_keys(name)
            print("Entered name.")
            return True
        except Exception as e:
            print(f"Error entering name: {e}")
            return False

    def enter_description(self, description):
        try:
            description_field = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Tell us what you or someone else did that was unmatched:']")
            description_field.send_keys(description)
            print("Entered description.")
            return True
        except Exception as e:
            print(f"Error entering description: {e}")
            return False

    def select_category(self, category):
        try:
            category_map = {
                "being human": "//input[@type='checkbox' and @title='Being Human']",
                "centric value: delivery excellence": "//input[@type='checkbox' and @title='Centric Value: Delivery Excellence']",
                "centric value: embracing integrity & openness": "//input[@type='checkbox' and @title='Centric Value: Embracing Integrity & Openness']",
                "centric value: investing in an exceptional culture": "//input[@type='checkbox' and @title='Centric Value: Investing in an Exceptional Culture']",
                "centric value: responsible stewardship": "//input[@type='checkbox' and @title='Centric Value: Responsible Stewardship']",
                "centric value: strive to innovate": "//input[@type='checkbox' and @title='Centric Value: Strive to Innovate']",
                "centric value: passion for greater good": "//input[@type='checkbox' and @title='Centric Value: Passion for Greater Good']",
                "knowledge sharing": "//input[@type='checkbox' and @title='Knowledge Sharing']",
                "showing gratitude": "//input[@type='checkbox' and @title='Showing Gratitude']",
                "unmatched communication": "//input[@type='checkbox' and @title='Unmatched Communication']",
                "unmatched leadership": "//input[@type='checkbox' and @title='Unmatched Leadership']",
                "other": "//input[@type='checkbox' and @title='Other']"
            }

            category_xpath = category_map.get(category.lower())
            if category_xpath:
                category_checkbox = self.driver.find_element(By.XPATH, category_xpath)
                category_checkbox.click()
                print(f"Selected category '{category}'.")
                return True
            else:
                print("Invalid category provided.")
                return False
        except Exception as e:
            print(f"Error selecting category: {e}")
            return False

    def submit_form(self):
        try:
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            print("Form submitted.")
            return True
        except Exception as e:
            print(f"Error submitting form: {e}")
            return False

    def close(self):
        self.driver.quit()

# Example usage:
automation = UMXFormAutomation()
automation.scroll_down()  # Scroll down one screen size
automation.select_role("client")
automation.enter_name("John Doe")
automation.enter_description("Provided excellent customer service.")
automation.scroll_down()  # Scroll down to make the category visible
automation.select_category("being human")
automation.submit_form()
automation.close()
