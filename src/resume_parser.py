import io


# ==========================================
# JOBINSIGHT - RESUME PARSER
# ==========================================


def read_resume(uploaded_file):

    if uploaded_file is None:

        return ""


    filename = (
        uploaded_file.name.lower()
    )


    # ======================================
    # TXT FILE
    # ======================================

    if filename.endswith(".txt"):

        text = (
            uploaded_file
            .read()
            .decode(
                "utf-8",
                errors="ignore"
            )
        )

        return text


    # ======================================
    # PDF FILE
    # ======================================

    if filename.endswith(".pdf"):

        import PyPDF2


        file_bytes = (
            uploaded_file.read()
        )


        reader = PyPDF2.PdfReader(

            io.BytesIO(
                file_bytes
            )
        )


        text = ""


        for page in reader.pages:

            page_text = (
                page.extract_text()
            )


            if page_text:

                text += (
                    page_text
                    + "\n"
                )


        return text


    # ======================================
    # DOCX FILE
    # ======================================

    if filename.endswith(".docx"):

        from docx import Document


        file_bytes = (
            uploaded_file.read()
        )


        document = Document(

            io.BytesIO(
                file_bytes
            )
        )


        text = ""


        for paragraph in (
            document.paragraphs
        ):

            text += (
                paragraph.text
                + "\n"
            )


        return text


    # ======================================
    # UNSUPPORTED FILE
    # ======================================

    return ""