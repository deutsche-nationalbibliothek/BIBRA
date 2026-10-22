from pydantic import BaseModel, ConfigDict, Field


class Version(BaseModel):
    """Response model for the root endpoint."""

    version: str = Field(
        ..., description="Current BIBRA version string", examples=["0.1.0"]
    )
    message: str = Field(
        ..., description="Welcome message", examples=["Welcome to BIBRA API v0"]
    )


class ProjectInfo(BaseModel):
    """Summary information for a single configured project."""

    id: str = Field(..., description="Project identifier", examples=["my_project"])
    name: str = Field(
        ..., description="Human-readable project name", examples=["My Project"]
    )
    description: str = Field(
        ...,
        description="Short description of the project",
        examples=["Project using dummy backend"],
    )


class Projects(BaseModel):
    """Response model for the list-projects endpoint."""

    projects: list[ProjectInfo] = Field(..., description="List of configured projects")


# class PublicationMetadata(BaseModel):
#     """Response model for publication metadata extraction."""

#     model_config = ConfigDict(populate_by_name=True)

#     language: str | None = None
#     title: str | None = None
#     alt_title: str | None = None
#     creator: list[str] = []
#     year: str | None = None
#     publisher: list[str] = []
#     doi: str | None = None
#     e_isbn: list[str] = Field(default=[], alias="e-isbn")
#     p_isbn: list[str] = Field(default=[], alias="p-isbn")
#     e_issn: str | None = Field(default=None, alias="e-issn")
#     p_issn: str | None = Field(default=None, alias="p-issn")
#     type_coar: str | None = None


class PublicationMetadata(BaseModel):
    """Response model for publication metadata extraction."""

    model_config = ConfigDict(populate_by_name=True)

    # Title information
    title: str | None = Field(
        default=None, 
        description="The main title of the work as presented on the title page. Extract the principal title, excluding the subtitle and other bibliographic information. Preserve the source language. Return null if the title cannot be determined."
        ) 
    subtitle: str | None = Field(
        default=None,
        description="The secondary title element that qualifies, explains, or further specifies the main title. It is part of the formal title, not merely descriptive text. Preserve the source language. Return null if no subtitle is present."
        )
    original_title: str | None = Field(
        default=None,
        description="The title of the original work in its original language, when the publication is a translation. Extract the original title only when it is explicitly stated in the publication. Do not infer it from external knowledge. Preserve the source language. Return null if no original title can be determined."
        )

    # Creators and contributors
    creator: str | None = Field(
        default=None,
        description="The person primarily responsible for the intellectual or artistic creation of the work. Extract the person's name as presented in the publication. Preserve the source language. Return null if no primary individual creator can be determined."
        )
    additional_creators: list[str] = Field(
        default=list,
        description="People explicitly credited with additional intellectual or artistic contributions to the work other than the primary creator. Examples include translators, editors, illustrators, etc. Extract each person's name separately. Preserve the source language. Do not duplicate the primary creator. Return an empty list if no additional creators can be identified."
        )
    corporate_body: str | None = Field(
        default=None,
        description="The name of the corporate body primarily responsible for the intellectual or artistic creation of the work. A corporate body is an organization or collective entity, such as a university, government agency, association, institution, or conference. Extract its name as presented in the publication. Preserve the source language. Do not classify a publisher as a creator solely because it publishes the work. Return null if no primary corporate body can be determined."
        )
    additional_corporate_bodies: list[str] = Field(
        default=list,
        description="Additional corporate bodies explicitly credited with intellectual or artistic responsibility for the work, other than the primary creative responsibility. Extract each corporate body's name separately. Preserve the source language. Do not classify a publisher as a creator solely because it publishes the work. Do not duplicate the primary corporate body. Return an empty list if no other corporate bodies can be identified."
        )

    # Identifiers
    p_isbn: list[str] = Field(
        default=list,
        description="The ISBN or ISBNs explicitly assigned to the printed edition represented by the publication. Extract each ISBN exactly as printed, normalizing only formatting such as spaces or hyphens. Do not infer, reconstruct, or obtain ISBNs from external sources. Return an empty list if no print ISBN can be determined."
        )

    # Publication details
    language_publication: str | None = Field(
        default=None,
        description="The language in which the publication is presented. Return as ISO 639-2/B code. For a translation, identify the language of the translated text, not the language of the original work. Return null if the publication language cannot be determined."
        )
    year: str | None = Field(
        default=None,
        description="The year in which the publication was published. Do not confuse it with the publication year of the original work, reprint year, or year of translation. If no publication year is stated but a copyright year is available, return the copyright year in square brackets, for example [2024]. Return null if no year can be determined."
        )
    publication_place: list[str] | None = Field(
        default=list,
        description="The place of publication, typically a city or town. Extract the city/place associated with the publisher in the publication statement. Extract the place as presented in the publication. Preserve the source language. Return an empty list if no publication place can be determined."
        )
    publisher: str = Field(
        default=str,
        description="The publishing entity responsible for publishing the specific publication. Prefer the publisher name as presented on the title page over publisher name given in the imprint. Preserve the source language and letter case. Return null if no publisher can be determined."
        )
    edition: str | None = Field(
        default=None,
        description="The edition statement identifying the specific edition of the work. Extract the edition as presented in the publication. Preserve the source language. Return null if no edition statement is given."
        )
    page_extent: str | None = Field(
        default=None,
        description="The pagination or page extent of the specific publication, as stated in the publication. Do not count the pages present in the scanned PDF, since the scan may contain only selected pages of the publication. Preserve complex pagination statements when necessary, for example “xii, 245 Seiten”. Return the statement in German. Return null if the page extent cannot be determined."
        )


# Extraction template matching nuextract3 expectations
NUEXTRACT_TEMPLATE = {
    "title": "string",
    "subtitle": "string",
    "original_title": "string",
    "creator": "string",
    "additional_creators": ["string"],
    "corporate_body": "string",
    "additional_corporate_bodies": ["string"],
    "p_isbn": ["string"],
    "language_publication": "language",
    "year": "date",
    "publication_place": ["string"],
    "publisher": "string",
    "edition": "string",
    "page_extent": "string"
}