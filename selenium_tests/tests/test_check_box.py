import pytest

from selenium_tests.pages.check_box_page import CheckBoxPage
from selenium_tests.pages.elements_page import ElementsPage
from selenium_tests.pages.home_page import HomePage

pytestmark = pytest.mark.regression

# The React sibling misspelled "Veu" is left out here and covered as a known
# bug below, so that fixing the typo does not fail these tests.
TREE_WITHOUT_MISSPELLED_NODE = [
    "Home",
    "Desktop",
    "Notes",
    "Commands",
    "Documents",
    "WorkSpace",
    "React",
    "Angular",
    "Office",
    "Public",
    "Private",
    "Classified",
    "General",
    "Downloads",
    "Word File.doc",
    "Excel File.doc",
]
TOTAL_NODES = 17
DOCUMENTS_NODES = 10


@pytest.fixture
def check_box_page(open_page):
    return open_page(CheckBoxPage)


@pytest.fixture
def expanded_page(check_box_page):
    check_box_page.expand_all()
    return check_box_page


class TestCheckBoxNavigation:
    @pytest.mark.smoke
    def test_check_box_is_reached_from_home_page(self, driver):
        home_page = HomePage(driver)
        home_page.open()

        home_page.go_to_elements()
        elements_page = ElementsPage(driver)
        assert elements_page.wait_for_url("https://demoqa.com/elements")

        elements_page.go_to_check_box()
        check_box_page = CheckBoxPage(driver)
        assert check_box_page.wait_for_url("https://demoqa.com/checkbox")
        assert check_box_page.heading == "Check Box"


class TestCheckBoxTree:
    def test_tree_starts_collapsed_with_nothing_selected(self, check_box_page):
        assert check_box_page.visible_nodes() == ["Home"]
        assert check_box_page.checkbox_state("Home") == "false"
        assert check_box_page.selected_items() == set()

    def test_expanding_home_shows_its_children(self, check_box_page):
        check_box_page.expand("Home")

        assert check_box_page.visible_nodes() == [
            "Home",
            "Desktop",
            "Documents",
            "Downloads",
        ]

    def test_collapsing_home_hides_its_children(self, check_box_page):
        check_box_page.expand("Home")

        check_box_page.collapse("Home")

        assert check_box_page.visible_nodes() == ["Home"]

    def test_expanding_every_folder_shows_the_full_tree(self, expanded_page):
        nodes = expanded_page.visible_nodes()

        assert len(nodes) == TOTAL_NODES
        assert [
            node for node in nodes if node in TREE_WITHOUT_MISSPELLED_NODE
        ] == TREE_WITHOUT_MISSPELLED_NODE


class TestCheckBoxSelection:
    @pytest.mark.parametrize(
        ("node", "result_name", "folder"),
        [
            ("Notes", "notes", "Desktop"),
            ("Commands", "commands", "Desktop"),
            ("React", "react", "WorkSpace"),
            ("Angular", "angular", "WorkSpace"),
            ("Public", "public", "Office"),
            ("Private", "private", "Office"),
            ("Classified", "classified", "Office"),
            ("General", "general", "Office"),
        ],
    )
    def test_checking_a_file_selects_only_that_file(
        self, expanded_page, node, result_name, folder
    ):
        expanded_page.toggle(node)

        assert expanded_page.wait_for_selected_items() == {result_name}
        assert expanded_page.checkbox_state(node) == "true"
        assert expanded_page.checkbox_state(folder) == "mixed"
        assert expanded_page.checkbox_state("Home") == "mixed"

    def test_unchecking_a_file_clears_the_selection(self, expanded_page):
        expanded_page.toggle("Notes")
        assert expanded_page.wait_for_selected_items() == {"notes"}

        expanded_page.toggle("Notes")

        assert expanded_page.wait_for_selected_items_to_be(set()) == set()
        assert expanded_page.checkbox_state("Desktop") == "false"
        assert expanded_page.checkbox_state("Home") == "false"

    def test_checking_every_child_fully_checks_the_folder(self, expanded_page):
        expanded_page.toggle("Notes")
        assert expanded_page.wait_for_selected_items() == {"notes"}

        expanded_page.toggle("Commands")

        expected = {"notes", "commands", "desktop"}
        shown = expanded_page.wait_for_selected_items_to_be(expected)
        assert shown == expected
        assert expanded_page.checkbox_state("Desktop") == "true"
        assert expanded_page.checkbox_state("Home") == "mixed"

    def test_checking_a_folder_selects_everything_inside(self, expanded_page):
        expanded_page.toggle("Documents")

        selected = expanded_page.wait_for_selected_items()
        assert len(selected) == DOCUMENTS_NODES
        assert {"documents", "workspace", "office", "react"} <= selected
        assert expanded_page.checkbox_state("Office") == "true"
        assert expanded_page.checkbox_state("Desktop") == "false"
        assert expanded_page.checkbox_state("Home") == "mixed"

    def test_unchecking_a_child_makes_the_folder_partly_checked(
        self, expanded_page
    ):
        expanded_page.toggle("Desktop")
        assert "notes" in expanded_page.wait_for_selected_items()

        expanded_page.toggle("Notes")

        expected = {"commands"}
        shown = expanded_page.wait_for_selected_items_to_be(expected)
        assert shown == expected
        assert expanded_page.checkbox_state("Desktop") == "mixed"

    @pytest.mark.smoke
    def test_checking_home_selects_every_node(self, expanded_page):
        expanded_page.toggle("Home")

        assert len(expanded_page.wait_for_selected_items()) == TOTAL_NODES
        assert expanded_page.checked_count() == TOTAL_NODES

    def test_unchecking_home_clears_every_node(self, expanded_page):
        expanded_page.toggle("Home")
        assert len(expanded_page.wait_for_selected_items()) == TOTAL_NODES

        expanded_page.toggle("Home")

        assert expanded_page.wait_for_selected_items_to_be(set()) == set()
        assert expanded_page.checked_count() == 0

    def test_collapsing_a_folder_keeps_the_selection(self, expanded_page):
        expanded_page.toggle("Home")
        assert len(expanded_page.wait_for_selected_items()) == TOTAL_NODES

        expanded_page.collapse("Home")
        assert len(expanded_page.selected_items()) == TOTAL_NODES

        expanded_page.expand("Home")
        assert expanded_page.checkbox_state("Desktop") == "true"

    def test_refreshing_the_page_resets_the_tree(self, expanded_page):
        expanded_page.toggle("Notes")
        assert expanded_page.wait_for_selected_items() == {"notes"}

        expanded_page.driver.refresh()

        assert expanded_page.visible_nodes() == ["Home"]
        assert expanded_page.selected_items() == set()


class TestCheckBoxKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the 'Vue' folder item is misspelled 'Veu'.",
    )
    def test_vue_is_spelled_correctly(self, expanded_page):
        assert "Vue" in expanded_page.visible_nodes()

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the result shows internal names such as excelFile.",
    )
    @pytest.mark.parametrize("label", ["Word File.doc", "Excel File.doc"])
    def test_result_shows_the_file_label(self, expanded_page, label):
        expanded_page.toggle(label)

        assert expanded_page.wait_for_selected_items() == {label}
