from selenium.webdriver.common.by import By

class UploadLocators:
    # The file input element (where you send_keys the file path)
    # This is directly visible in your HTML: <input id="file-upload" type="file" name="file">
    FILE_INPUT = (By.ID, "file-upload")

    # The upload button
    # This is directly visible in your HTML: <input class="button" id="file-submit" type="submit" value="Upload">
    UPLOAD_BUTTON = (By.ID, "file-submit")

    # The main heading for the page
    # Based on your HTML: <h3>File Uploader</h3>
    # Using XPATH with normalize-space() for exact text match.
    MAIN_HEADING = (By.XPATH, "//h3[normalize-space()='File Uploader']")

    # The dynamically created element where the filename appears after upload.
    # From your provided HTML's #preview-template:
    # <div class="dz-details"> <div class="dz-filename"><span data-dz-name=""></span></div> </div>
    UPLOADED_FILES_DISPLAY = (By.CSS_SELECTOR, ".dz-preview.dz-file-preview .dz-filename [data-dz-name]")

    # The success message header that appears after a successful upload (on a new page).
    # This page usually shows an H2 with text "File Uploaded!".
    SUCCESS_MESSAGE_HEADER = (By.TAG_NAME, "h2")