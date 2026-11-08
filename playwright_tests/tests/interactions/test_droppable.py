import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.interactions.droppable_page import DroppablePage
from playwright_tests.pages.interactions.interactions_page import (
    InteractionsPage,
)

pytestmark = pytest.mark.regression

DROPPED = "Dropped!"
DROPPED_COLOUR = "rgb(70, 130, 180)"
READY_COLOUR = "rgb(60, 179, 113)"
# Known bugs are checked with a short limit, as their outcome shows at once.
QUICK_TIMEOUT_MS = 2_000


@pytest.fixture
def droppable_page(open_page):
    return open_page(DroppablePage)


def expect_dropped(droppable_page, target):
    expect(droppable_page.text_of(target)).to_have_text(DROPPED)
    expect(target).to_have_css("background-color", DROPPED_COLOUR)


class TestDroppableNavigation:
    @pytest.mark.smoke
    def test_droppable_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_interactions()
        expect(page).to_have_url("https://demoqa.com/interaction")

        interactions_page = InteractionsPage(page)
        interactions_page.go_to_droppable()
        expect(page).to_have_url("https://demoqa.com/droppable")
        expect(interactions_page.heading).to_have_text("Droppable")


class TestSimpleDrop:
    def test_target_asks_for_a_drop_at_first(self, droppable_page):
        expect(droppable_page.text_of(droppable_page.simple_target)
               ).to_have_text("Drop Here")

    @pytest.mark.smoke
    def test_drop_marks_the_target(self, droppable_page):
        droppable_page.drag_onto(
            droppable_page.simple_box, droppable_page.simple_target
        )

        expect_dropped(droppable_page, droppable_page.simple_target)


class TestAcceptDrop:
    def test_acceptable_box_lights_target_while_dragged(self, droppable_page):
        droppable_page.show("Accept")

        droppable_page.hold_over(
            droppable_page.acceptable_box, droppable_page.accept_target
        )

        expect(droppable_page.accept_target).to_have_css(
            "background-color", READY_COLOUR
        )
        droppable_page.release()

    def test_acceptable_box_is_accepted(self, droppable_page):
        droppable_page.show("Accept")

        droppable_page.drag_onto(
            droppable_page.acceptable_box, droppable_page.accept_target
        )

        expect_dropped(droppable_page, droppable_page.accept_target)

    def test_not_acceptable_box_is_refused(self, droppable_page):
        droppable_page.show("Accept")

        droppable_page.drag_onto(
            droppable_page.not_acceptable_box, droppable_page.accept_target
        )

        # A wait cannot prove nothing happened, so make an accepted drop
        # elsewhere and wait for it; by then this drop has been handled.
        droppable_page.show("Simple")
        droppable_page.drag_onto(
            droppable_page.simple_box, droppable_page.simple_target
        )
        expect_dropped(droppable_page, droppable_page.simple_target)
        droppable_page.show("Accept")

        expect(droppable_page.text_of(droppable_page.accept_target)
               ).to_have_text("Drop here")


class TestPreventPropagation:
    def test_not_greedy_inner_drop_marks_both_boxes(self, droppable_page):
        droppable_page.show("Prevent Propagation")

        droppable_page.drag_onto(
            droppable_page.propagation_box,
            droppable_page.nested_box("not greedy inner"),
        )

        for name in ["not greedy inner", "not greedy outer"]:
            expect(droppable_page.nested_box_text(name)).to_have_text(
                DROPPED
            )

    def test_greedy_inner_drop_marks_only_that_box(self, droppable_page):
        droppable_page.show("Prevent Propagation")

        droppable_page.drag_onto(
            droppable_page.propagation_box,
            droppable_page.nested_box("greedy inner"),
        )

        expect(droppable_page.nested_box_text("greedy inner")).to_have_text(
            DROPPED
        )
        expect(droppable_page.nested_box_text("greedy outer")).to_have_text(
            "Outer droppable"
        )

    def test_outer_drop_marks_only_the_outer_box(self, droppable_page):
        droppable_page.show("Prevent Propagation")

        droppable_page.drop_on_outer_only("greedy outer")

        expect(droppable_page.nested_box_text("greedy outer")).to_have_text(
            DROPPED
        )
        expect(droppable_page.nested_box_text("greedy inner")).to_have_text(
            "Inner droppable (greedy)"
        )


class TestRevertDraggable:
    def test_will_revert_box_slides_back(self, droppable_page):
        droppable_page.show("Revert Draggable")

        droppable_page.drag_onto(
            droppable_page.revert_box, droppable_page.revert_target
        )

        expect_dropped(droppable_page, droppable_page.revert_target)
        expect(droppable_page.revert_box).to_have_css("left", "0px")
        expect(droppable_page.revert_box).to_have_css("top", "0px")

    def test_not_revert_box_stays_where_dropped(self, droppable_page):
        droppable_page.show("Revert Draggable")
        droppable_page.drag_onto(
            droppable_page.no_revert_box, droppable_page.revert_target
        )

        # Let a reverting box finish sliding back, so the other box has had
        # as long to move back too, had it been going to.
        droppable_page.drag_onto(
            droppable_page.revert_box, droppable_page.revert_target
        )
        expect(droppable_page.revert_box).to_have_css("left", "0px")

        expect(droppable_page.no_revert_box).not_to_have_css("left", "0px")


class TestDroppableKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: the tab misspells \"Propagation\" as "
            "\"Propogation\"."
        ),
    )
    def test_propagation_tab_is_spelled_correctly(self, droppable_page):
        expect(
            droppable_page.tab_named_exactly("Prevent Propagation")
        ).to_have_count(1, timeout=QUICK_TIMEOUT_MS)
