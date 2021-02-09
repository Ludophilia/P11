import time

from django.test import tag
from tests.assistance.frontend_tests import AssistanceClassForSLSTC

@tag("t9")
class TestAutocompleteFeature(AssistanceClassForSLSTC):

    def setMoreThingsUp(self):

        self.driver.get(f"{self.live_server_url}")

        self.expectations = [("ab", "Abricots Pelés"), ("orangi", "Orangina"), ("nut", "Nutella"), 
        ("pom'p", "Pom'Potes (Pomme)"), ("extrê", "Extrême Chocolat"), ("q", "Quinoa Lentilles"), 
        ("ac", "Activia vanille"), ("velouté F", "Velouté Fruix"), ("c", "Camembert"), 
        ("bn", "BN goût chocolat")]

        self.search_inputs = self.f("form.input-group > input"), self.f("form.input-group-fake > input")

    @tag("t9-p1")
    def test_if_the_autocomplete_feature_work_on_homepage_search_bar(self):
                
        self.setMoreThingsUp()

        time.sleep(0.5)
        
        for search_input in self.search_inputs:
                
            for query, expect in self.expectations:

                for q in query : search_input.send_keys(q) ; time.sleep(1)
                suggestions = [sug.text for sug in self.ff(".ac-item")]
                self.assertIn(expect, suggestions)
                search_input.clear()

    @tag("t9-p2")
    def test_if_the_autocomplete_window_appear_and_disappear_when_the_user_puts_the_focus_in_and_out_the_search_in_put(self):

        self.setMoreThingsUp()

        for search_input in self.search_inputs:

            for _ in range(2):

                search_input.send_keys("ex" if _ == 0 else "c")

                time.sleep(0.5)

                self.assertEqual("autocomplete-items", self.f(".autocomplete-items").get_attribute("class"))
                self.f("body").click()

                time.sleep(0.5)
                
                self.assertEqual("autocomplete-items d-none", self.f(".autocomplete-items").get_attribute("class"))

    @tag("t9-p3")
    def test_if_clicking_on_one_the_autocomplete_suggestion_lead_the_user_to_the_product(self):
        
        self.setMoreThingsUp()

        for search_target in ["form.input-group > input", "form.input-group-fake > input"]:

            for query, expect in self.expectations:

                for q in query : self.f(search_target).send_keys(q) ; time.sleep(0.5)
                item = self.f(".ac-item:first-child")
                item.click()

                time.sleep(0.5)

                self.assertIn(expect.upper(), self.f("h1").text)
                self.assertIn("/search?query=", self.driver.current_url)

                self.driver.get(f"{self.live_server_url}")

                time.sleep(0.5)

