import re

import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.draggable_page import DraggablePage
from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.interactions_page import InteractionsPage

pytestmark = pytest.mark.regression

# The site spells the page "Dragabble". Passing tests accept either spelling;
# only the xfail asks for the correct one.
EITHER_SPELLING = re.compile(r"^(Dragabble|Draggable)$")
# How far, at most, the "top left" box sits from the cursor (5px seen).
TOP_LEFT_GAP_PX = 10
# Known bugs are checked with a short limit, as their outcome shows at once.
QUICK_TIMEOUT_MS = 2_000


@pytest.fixture
def draggable_page(open_page):
    return open_page(DraggablePage)


def moved_by(draggable_page, name, dx, dy):
    """Drag a box by dx, dy and return how far it actually moved."""
    box = draggable_page.box(name)
    start_x, start_y = draggable_page.position_of(box)
    draggable_page.drag_by(box, dx, dy)
    end_x, end_y = draggable_page.position_of(box)
    return end_x - start_x, end_y - start_y


class TestDraggableNavigation:
    @pytest.mark.smoke
    def test_draggable_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_interactions()
        expect(page).to_have_url("https://demoqa.com/interaction")

        interactions_page = InteractionsPage(page)
        interactions_page.go_to_draggable()
        expect(page).to_have_url("https://demoqa.com/dragabble")
        expect(interactions_page.heading).to_have_text(EITHER_SPELLING)


class TestSimpleDrag:
    @pytest.mark.smoke
    def test_box_moves_as_far_as_it_is_dragged(self, draggable_page):
        assert moved_by(draggable_page, "simple", 200, 100) == (200, 100)


class TestAxisRestricted:
    def test_only_x_box_moves_only_sideways(self, draggable_page):
        draggable_page.show("Axis Restricted")

        assert moved_by(draggable_page, "only x", 150, 120) == (150, 0)

    def test_only_y_box_moves_only_up_and_down(self, draggable_page):
        draggable_page.show("Axis Restricted")

        assert moved_by(draggable_page, "only y", 150, 120) == (0, 120)


class TestContainerRestricted:
    def test_box_stays_inside_its_container(self, draggable_page):
        draggable_page.show("Container Restricted")

        moved = moved_by(draggable_page, "in container", 2000, 2000)

        left, top, right, bottom = draggable_page.edges_of(
            draggable_page.box("in container")
        )
        c_left, c_top, c_right, c_bottom = draggable_page.edges_of(
            draggable_page.container
        )
        assert moved[0] > 0 and moved[1] > 0
        assert c_left <= left and right <= c_right
        assert c_top <= top and bottom <= c_bottom


class TestCursorStyle:
    def test_centre_box_stays_under_the_cursor(self, draggable_page):
        draggable_page.show("Cursor Style")
        box = draggable_page.box("cursor centre")

        x, y = draggable_page.hold_moved_by(box, 300, 150)

        left, top, right, bottom = draggable_page.edges_of(box)
        expect(draggable_page.body).to_have_css("cursor", "move")
        assert left <= x <= right and top <= y <= bottom
        draggable_page.release()

    def test_top_left_box_hangs_just_below_the_cursor(self, draggable_page):
        draggable_page.show("Cursor Style")
        box = draggable_page.box("cursor top left")

        x, y = draggable_page.hold_moved_by(box, 300, 150)

        left, top, _, _ = draggable_page.edges_of(box)
        expect(draggable_page.body).to_have_css("cursor", "crosshair")
        assert 0 < left - x <= TOP_LEFT_GAP_PX
        assert 0 < top - y <= TOP_LEFT_GAP_PX
        draggable_page.release()

    def test_bottom_box_sits_on_the_cursor(self, draggable_page):
        draggable_page.show("Cursor Style")
        box = draggable_page.box("cursor bottom")

        x, y = draggable_page.hold_moved_by(box, 300, 150)

        left, _, right, bottom = draggable_page.edges_of(box)
        assert round(bottom) == round(y)
        assert round((left + right) / 2) == round(x)
        draggable_page.release()


class TestDraggableKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: the heading misspells \"Draggable\" as \"Dragabble\"."
        ),
    )
    def test_heading_is_spelled_correctly(self, draggable_page):
        expect(draggable_page.heading).to_have_text(
            "Draggable", timeout=QUICK_TIMEOUT_MS
        )

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: \"I'm contained within my parent\" takes the drag "
            "but never moves."
        ),
    )
    def test_text_moves_within_its_parent(self, draggable_page):
        draggable_page.show("Container Restricted")

        assert moved_by(draggable_page, "in parent", 0, 40) != (0, 0)
