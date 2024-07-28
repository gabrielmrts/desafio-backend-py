from pydantic import BaseModel, ConfigDict

class TaskBase(BaseModel):
	title: str
	description: str
	completed: bool = False

class TaskCreate(BaseModel):
	title: str
	description: str

class TaskPatch(BaseModel):
	completed: bool

class TaskRead(TaskBase):
	id: int

	model_config = ConfigDict(from_attributes=True)