import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.elements.elements_page import ElementsPage
from playwright_tests.pages.elements.upload_download_page import (
    UploadDownloadPage,
)
from playwright_tests.pages.home_page import HomePage

pytestmark = pytest.mark.regression

JPEG_START = b"\xff\xd8\xff"
JPEG_END = b"\xff\xd9"


@pytest.fixture
def upload_download_page(open_page):
    return open_page(UploadDownloadPage)


@pytest.fixture
def make_file(tmp_path):
    """Return a function that creates a small text file to upload."""

    def _make(name: str):
        path = tmp_path / name
        path.write_text("Test file for upload.\n")
        return path

    return _make


class TestUploadDownloadNavigation:
    @pytest.mark.smoke
    def test_upload_and_download_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_elements()
        expect(page).to_have_url("https://demoqa.com/elements")

        elements_page = ElementsPage(page)
        elements_page.go_to_upload_and_download()
        expect(page).to_have_url("https://demoqa.com/upload-download")
        expect(elements_page.heading).to_have_text("Upload and Download")


class TestUploadDownloadInitialState:
    def test_download_button_is_shown(self, upload_download_page):
        expect(upload_download_page.download_button).to_be_visible()

    def test_no_uploaded_file_is_shown_at_first(self, upload_download_page):
        expect(upload_download_page.upload_field).to_be_visible()
        expect(upload_download_page.uploaded_file_path).to_have_count(0)


class TestDownload:
    @pytest.mark.smoke
    def test_download_saves_sample_file(self, upload_download_page, tmp_path):
        path = upload_download_page.download(tmp_path)

        assert path.name == "sampleFile.jpeg"
        assert path.exists()

    def test_downloaded_file_is_complete_jpeg(
        self, upload_download_page, tmp_path
    ):
        data = upload_download_page.download(tmp_path).read_bytes()

        assert data.startswith(JPEG_START)
        assert data.endswith(JPEG_END)


class TestUpload:
    @pytest.mark.parametrize(
        "file_name",
        [
            pytest.param("notes.txt", marks=pytest.mark.smoke),
            "résumé file (1).txt",
        ],
    )
    def test_upload_shows_file_name(
        self, upload_download_page, make_file, file_name
    ):
        upload_download_page.upload(make_file(file_name))

        # Browsers hide the real folder and always show C:\fakepath\.
        expect(upload_download_page.uploaded_file_path).to_have_text(
            f"C:\\fakepath\\{file_name}"
        )

    def test_new_upload_replaces_previous_file(
        self, upload_download_page, make_file
    ):
        upload_download_page.upload(make_file("first.txt"))
        expect(upload_download_page.uploaded_file_path).to_have_text(
            "C:\\fakepath\\first.txt"
        )

        upload_download_page.upload(make_file("second.txt"))

        expect(upload_download_page.uploaded_file_path).to_have_text(
            "C:\\fakepath\\second.txt"
        )

    def test_clearing_upload_removes_file_name(
        self, upload_download_page, make_file
    ):
        upload_download_page.upload(make_file("notes.txt"))
        expect(upload_download_page.uploaded_file_path).to_be_visible()

        upload_download_page.clear_upload()

        expect(upload_download_page.uploaded_file_path).to_have_count(0)
