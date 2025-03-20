from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel

class Json(BaseModel):
    """Custom JSON type that can handle nested structures"""
    __root__: Union[str, int, bool, None, Dict[str, Any], List[Any]]

class AdminAction(BaseModel):
    action_type: str
    details: Optional[str] = None
    id: Optional[int] = None
    timestamp: Optional[str] = None
    user_id: Optional[int] = None

class Answer(BaseModel):
    answer: str
    correct: bool
    id: Optional[int] = None
    question_id: int
    quiz_id: int
    timestamp: str
    user_id: int

class ChatHistory(BaseModel):
    id: Optional[int] = None
    messages: Json
    session_start: Optional[str] = None
    user_id: int

class ChatbotResponse(BaseModel):
    created_at: Optional[str] = None
    id: Optional[int] = None
    response: str
    user_id: int

class Conversation(BaseModel):
    conversation_number: int
    id: str
    timestamp: Optional[str] = None
    title: Optional[str] = None
    user_id: str

class CurriculumPlan(BaseModel):
    created_at: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None
    plan_name: str
    status: Optional[str] = None
    subjects: Json
    type: Optional[str] = None
    user_id: int

class Feedback(BaseModel):
    comment: str
    id: Optional[int] = None
    rating: Optional[int] = None
    timestamp: Optional[str] = None
    user_id: int

class Homework(BaseModel):
    assignment: str
    details: Optional[str] = None
    due_date: Optional[str] = None
    id: Optional[int] = None
    user_id: int

class KnowledgeUpdate(BaseModel):
    id: Optional[int] = None
    new_information: str
    topic_id: int

class Message(BaseModel):
    content: Optional[str] = None
    conversation_id: Optional[str] = None
    id: Optional[int] = None
    role: Optional[str] = None
    timestamp: Optional[str] = None
    user_id: str

class Notification(BaseModel):
    id: Optional[int] = None
    is_dismissed: Optional[bool] = None
    message: str
    timestamp: Optional[str] = None
    user_id: int

class PerformanceAnalytics(BaseModel):
    average_score: float
    completion_rate: float
    difficulty_level: Optional[str] = None
    id: Optional[int] = None
    subject: str

class PracticeTest(BaseModel):
    answer_explanation: Optional[str] = None
    choices: Optional[Json] = None
    correct_answer: Optional[str] = None
    difficulty: Optional[str] = None
    domain: Optional[str] = None
    equation: Optional[str] = None
    figure_description: Optional[str] = None
    id: Optional[int] = None
    image: Optional[str] = None
    practice_test: Optional[str] = None
    question_content: Optional[str] = None
    question_number: Optional[int] = None
    skill: Optional[str] = None
    sub_topic: Optional[str] = None
    svg: Optional[str] = None
    tabular_data: Optional[Json] = None
    topic: Optional[str] = None
    type: Optional[str] = None

class QuestionBank(BaseModel):
    answer_explanation: Optional[str] = None
    choices: Optional[Json] = None
    correct_answer: Optional[str] = None
    equation: Optional[str] = None
    figure_description: Optional[str] = None
    id: Optional[int] = None
    image: Optional[str] = None
    question_content: Optional[str] = None
    question_number_in_subtopic: Optional[int] = None
    sub_topic: Optional[str] = None
    svg: Optional[str] = None
    tabular_data: Optional[Json] = None
    topic: Optional[str] = None
    type: Optional[str] = None

class QuestionType(BaseModel):
    question_type_id: Optional[int] = None
    question_type_name: str

class Reminder(BaseModel):
    id: Optional[int] = None
    message: str
    reminder_time: str
    user_id: int

class SessionSummary(BaseModel):
    chat_id: int
    highlights: Json
    id: Optional[int] = None

class TestAttempt(BaseModel):
    attempt_id: Optional[int] = None
    created_at: Optional[str] = None
    responses: Json
    status: str
    test_id: int
    user_id: int

class UsageAnalytics(BaseModel):
    feature_name: str
    id: Optional[int] = None
    last_used: Optional[str] = None
    usage_count: int

class UserMessage(BaseModel):
    content: str
    created_at: Optional[str] = None
    id: Optional[int] = None
    user_id: int

class UserPracticeTest(BaseModel):
    completed_at: Optional[str] = None
    practice_test_id: int
    score: Optional[float] = None
    user_id: int

class UserProgress(BaseModel):
    id: Optional[int] = None
    quiz_id: int
    score: float
    session_id: Optional[str] = None
    timestamp: Optional[str] = None
    user_id: int

class UserQuestionProgress(BaseModel):
    progress: float
    question_type_id: int
    user_id: str

class UserSettings(BaseModel):
    id: Optional[int] = None
    setting: str
    setting_type: str
    user_id: int

class User(BaseModel):
    access_token: Optional[str] = None
    additional_info: Optional[Json] = None
    created_at: Optional[str] = None
    email: str
    full_name: Optional[str] = None
    password_hash: str
    profile_picture: Optional[str] = None
    role: Optional[str] = None
    status: Optional[bool] = None
    token_type: Optional[str] = None
    updated_at: Optional[str] = None
    user_id: str
    username: str

# List of all models for reference
ALL_MODELS = [
    AdminAction,
    Answer,
    ChatHistory,
    ChatbotResponse,
    Conversation,
    CurriculumPlan,
    Feedback,
    Homework,
    KnowledgeUpdate,
    Message,
    Notification,
    PerformanceAnalytics,
    PracticeTest,
    QuestionBank,
    QuestionType,
    Reminder,
    SessionSummary,
    TestAttempt,
    UsageAnalytics,
    UserMessage,
    UserPracticeTest,
    UserProgress,
    UserQuestionProgress,
    UserSettings,
    User
]

# Mapping of models to their corresponding Supabase table names
TABLE_MAPPING = {
    AdminAction: "admin_actions",
    Answer: "answers",
    ChatHistory: "chat_history",
    ChatbotResponse: "chatbot_responses",
    Conversation: "conversations",
    CurriculumPlan: "curriculum_plans",
    Feedback: "feedback",
    Homework: "homework",
    KnowledgeUpdate: "knowledge_updates",
    Message: "messages",
    Notification: "notifications",
    PerformanceAnalytics: "performance_analytics",
    PracticeTest: "practice_tests",
    QuestionBank: "question_bank",
    QuestionType: "question_types",
    Reminder: "reminders",
    SessionSummary: "session_summaries",
    TestAttempt: "test_attempts",
    UsageAnalytics: "usage_analytics",
    UserMessage: "user_messages",
    UserPracticeTest: "user_practice_tests",
    UserProgress: "user_progress",
    UserQuestionProgress: "user_question_progress",
    UserSettings: "user_settings",
    User: "users"
}
