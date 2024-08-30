from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Optional,Any
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage

class Title(BaseModel):
    title: str = Field(..., description="Title of the story book")

class Chapter(BaseModel):
    chapter_title: str = Field(..., description="Title of the chapter")
    description: str = Field(..., description="Summary description of the chapter")

    @property
    def as_str(self) -> str:
        return f"## {self.chapter_title}\n\n{self.description}".strip()


class Outline(BaseModel):
    """
        Outline class to format the LLM output
    """
    page_title: str = Field(..., description="Title of the comics book")
    chapters: List[Chapter] = Field(
        default_factory=list,
        max_items=10,
        description="Titles and descriptions for each chapter of the comics book.",
    )

    @property
    def as_str(self) -> str:
        chapter = "\n\n".join(chapter.as_str for chapter in self.chapters)
        return f"# {self.page_title}\n\n{chapter}".strip()
    
    
class Persona(BaseModel):
    """
        Persona class to format the LLM output
    """
    # affiliation: str = Field(
    #     description="Primary affiliation of the character.",
    # )
    name: str = Field(
        description="only first name of character, need to match with '^[a-zA-Z0-9_-]{1,64}$'",
    )
    role: str = Field(
        description="Role of the character in the story.",
    )
    background: str = Field(
        description="background of the person in the story, such as personality, hobbies, etc..",
    )
    figure: str = Field(
        description="figure representing such as a boy,a girl,a man, a women, a young woman,an old man or etc",
    )
    appearance: str = Field(
        description="appearance, attire of the character in the story.",
    )

    @property
    def persona(self) -> str:
        return f"Name: {self.name}\nRole: {self.role}\nBackground: {self.background}\nFigure:{self.figure}\nAppearance: {self.appearance}\n"
    
class Character(BaseModel):
    """
        Character class to format the LLM output
    """
    main_character: Persona = Field(
        description="the main character in the story.",
    )
    
    supporting_character: List[Persona] = Field(
        description="Comprehensive list of supporting characters in the story.",
        min_items=1,
        max_items=10,
    )
    @property
    def as_str(self) -> str:
        return "\n".join([e.persona for e in self.supporting_character])+'\n'+self.main_character.persona
    
    

class Paragragh(BaseModel):
    """
        Content of the Paragrah
    """
    content: str = Field(..., description="Content of the Paragrah")

class DetailChapter(BaseModel):
    """
        Content of the Chapter
    """
    chapter_title: str = Field(..., description="Title of the chapter")
    content: str = Field(..., description="Content of the chapter")
    # paragraphs: List[Paragragh] = Field(max_items=1, 
    #                                     description="List of paragraghs of the chapter, limits to maximum 1 item")
    
    @property
    def as_str(self) -> str:
        # chapter_content = "\n".join([p.content for p in self.paragraphs])
        return f"## {self.chapter_title}\n\n{self.content}".strip()
    
class EditorSuggestion(BaseModel):
    """
        editor's suggestions, max 10 is allowed
    """
    suggestions: List[str] = Field(
      description="suggestion list",
    )
    @property
    def as_str(self) -> str:
        return "\n".join([f"{i+1}.{e}" for i,e in enumerate(self.suggestions)])

    
class Story(BaseModel):
    """
        the full story object
    
    """
    story_title: str = Field(..., title="Title of the comics book")
    chapters: List[DetailChapter] = Field(
        default_factory=list,
        title="Titles and descriptions for each chapter of the comics book.",
    )
    images: Optional[List[Any]] = Field(default=[], title="List of illustration for each chapter")
    
    def as_str(self) -> str:
        chapter_content = "\n".join([p.content for p in self.paragraphs])
        return f"## {self.chapter_title}\n\n{chapter_content}".strip()