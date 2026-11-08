from pathlib import Path

from playwright.sync_api import Locator

from playwright_tests.pages.elements.elements_page import ElementsPage


class UploadDownloadPage(ElementsPage):
    PATH = "/upload-download"

    @property
    def download_button(self) -> Locator:
        return self.page.get_by_role("button", name="Download", exact=True)

    @property
    def upload_field(self) -> Locator:
        # The field has no label, so it has no accessible name to find.
        return self.page.locator("#uploadFile")

    @property
    def uploaded_file_path(self) -> Locator:
        return self.page.locator("#uploadedFilePath")

    def download(self, folder: Path) -> Path:
        """Click Download, save the file in the folder and return its path."""
        with self.page.expect_download() as download_info:
            self.download_button.click()
        download = download_info.value
        path = folder / download.suggested_filename
        download.save_as(path)
        return path

    def upload(self, file: Path) -> None:
        self.upload_field.set_input_files(file)

    def clear_upload(self) -> None:
        self.upload_field.set_input_files([])
