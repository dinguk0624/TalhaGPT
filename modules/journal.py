import datetime
import os

from modules.rag import add_document_to_memory


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

NOTES_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "notes.txt"
)


# ============================================================
# SAVE NOTE
# ============================================================

def save_note(note: str) -> str:
    """
    Save a user note permanently.

    The note is:
    1. Cleaned from common note-taking phrases.
    2. Saved to data/notes.txt.
    3. Added to the RAG long-term memory.
    """

    # --------------------------------------------------------
    # VALIDATE NOTE
    # --------------------------------------------------------

    if not note or not note.strip():
        return (
            "[Note Error]: "
            "Empty note cannot be saved."
        )

    # --------------------------------------------------------
    # CLEAN NOTE
    # --------------------------------------------------------

    cleaned_note = note.strip()

    keywords = [
        "şunu not al:",
        "şunu not al",
        "not al:",
        "not al",
        "not tut:",
        "not tut",
        "şunu kaydet:",
        "şunu kaydet",
        "remember:",
        "remember",
        "save this:",
        "save this",
    ]

    lower_note = cleaned_note.lower()

    for keyword in keywords:

        if lower_note.startswith(keyword):

            cleaned_note = (
                cleaned_note[len(keyword):]
                .strip()
            )

            break

    if not cleaned_note:

        cleaned_note = note.strip()

    # --------------------------------------------------------
    # TIMESTAMP
    # --------------------------------------------------------

    current_time = (
        datetime.datetime.now()
        .strftime("%Y-%m-%d %H:%M:%S")
    )

    log_entry = (
        f"[{current_time}] -> "
        f"{cleaned_note}\n"
    )

    # --------------------------------------------------------
    # CREATE DATA DIRECTORY
    # --------------------------------------------------------

    try:

        os.makedirs(
            os.path.dirname(NOTES_FILE),
            exist_ok=True
        )

    except Exception as e:

        return (
            "[Note Error]: "
            f"Failed to create notes directory: {e}"
        )

    # --------------------------------------------------------
    # SAVE TO NOTES FILE
    # --------------------------------------------------------

    try:

        with open(
            NOTES_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(log_entry)

    except Exception as e:

        return (
            "[Note Error]: "
            f"Failed to save note: {e}"
        )

    # --------------------------------------------------------
    # ADD NOTE TO RAG MEMORY
    # --------------------------------------------------------

    rag_warning = None

    try:

        # RAG'ın dosya tabanlı API'sini kullanıyoruz.
        rag_result = add_document_to_memory(
            NOTES_FILE
        )

        if (
            not rag_result
            or "[RAG Error]" in str(rag_result)
            or "[Error]" in str(rag_result)
        ):

            rag_warning = str(
                rag_result
            )

    except Exception as e:

        rag_warning = str(e)

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    if rag_warning:

        return (
            "[Note Warning]: "
            "Note was saved successfully to "
            f"'{NOTES_FILE}', but RAG memory could "
            f"not be updated: {rag_warning}"
        )

    return (
        "[Note]: Note saved successfully. "
        "The information was also added to "
        "long-term RAG memory."
    )