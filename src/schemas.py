from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw contract text to analyze (cannot be empty)")


class Party(BaseModel):
    role: str = Field(..., description="Role of the party in the contract")
    potential_risks: list[str] = Field([], min_length=0,
                                       description="Potential risks associated with the party (at least one required)")

    @field_validator('role')
    @classmethod
    def validate_role_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Role cannot be empty')
        return v.strip()

    @field_validator('potential_risks')
    @classmethod
    def validate_potential_risks(cls, v: list[str]) -> list[str]:
        validated = [item.strip() for item in v]
        if any(not item for item in validated):
            raise ValueError('Potential risks cannot contain empty strings')
        return validated


class AnalyzeResponse(BaseModel):
    is_contract: bool = Field(..., description="Whether the text is a contract")
    about: str = Field(..., min_length=1, description="Summary, what is this contract about? (cannot be empty)")
    key_clauses: list[str] = Field(..., min_length=1,
                                   description="List of key clauses in the contract (at least one required)")
    parties: list[Party] = Field(..., min_length=1,
                                 description="List of parties in the contract (at least one required)")

    @field_validator('about')
    @classmethod
    def validate_about_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('About field cannot be empty')
        return v.strip()

    @field_validator('key_clauses')
    @classmethod
    def validate_key_clauses(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError('At least one key clause must be provided')
        cleaned = [item.strip() for item in v]
        if any(not item for item in cleaned):
            raise ValueError('Key clauses cannot contain empty strings')
        return cleaned

    @field_validator('parties')
    @classmethod
    def validate_parties(cls, v: list[Party]) -> list[Party]:
        if not v:
            raise ValueError('At least one party must be provided')
        return v
