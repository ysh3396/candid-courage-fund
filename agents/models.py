"""Data models for the Life Deck pipeline."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TimelineEvent:
    year: str
    title: str
    description: str
    significance: str
    category: str  # "failure", "recovery", "growth", "turning_point"


@dataclass
class ResearchOutput:
    """Output from the Researcher agent."""

    identity_keywords: list[str] = field(default_factory=list)
    life_themes: list[str] = field(default_factory=list)
    timeline: list[dict] = field(default_factory=list)
    values: list[str] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    failure_recovery_cycles: list[dict] = field(default_factory=list)
    ccf_mapping: dict[str, list[str]] = field(default_factory=dict)
    raw_analysis: str = ""


@dataclass
class ConsultantOutput:
    """Output from the Consultant agent."""

    q1_who_am_i: dict = field(
        default_factory=dict
    )  # core_message, supporting_points, narrative_angle
    q2_how_lived: dict = field(default_factory=dict)
    q3_how_will_live: dict = field(default_factory=dict)
    q4_why_funding: dict = field(default_factory=dict)
    overall_narrative_arc: str = ""
    raw_framing: str = ""


@dataclass
class CopywriterOutput:
    """Output from the Copywriter agent."""

    hero_name: str = ""
    hero_tagline: str = ""
    hero_quote: str = ""
    section_01: str = ""  # 나는 누구인가
    section_02: str = ""  # 어떻게 살아왔는가
    section_03: str = ""  # 어떻게 살 것인가
    section_04: str = ""  # 용기자금이 필요한 이유
    closing_quote: str = ""
    raw_draft: str = ""


@dataclass
class ReviewFeedback:
    """Output from the Reviewer agent."""

    completeness_score: int = 0  # 0-100
    covered_areas: list[str] = field(default_factory=list)
    missing_areas: list[str] = field(default_factory=list)
    questions_for_user: list[dict] = field(
        default_factory=list
    )  # {priority, question, context}
    improvement_suggestions: list[str] = field(default_factory=list)
    raw_review: str = ""
