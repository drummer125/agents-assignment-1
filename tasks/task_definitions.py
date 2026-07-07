"""
Task Definitions for Research Crew

TODO: Define the four sequential tasks:
1. Query Expansion - Break down the research question
2. Source Hunting - Search the paper corpus
3. Synthesis - Analyze and synthesize findings
4. Report Writing - Generate the literature review

Each task should:
- Have a clear description telling the agent what to do
- Specify the agent responsible
- Define expected_output format
- Use context parameter to pass information between tasks
"""

from crewai import Task
from agents import query_expander, source_hunter, synthesizer, report_writer


def create_research_tasks(research_question: str) -> list[Task]:
    """
    Create the task pipeline for a research question.

    Args:
        research_question: The user's research question

    Returns:
        List of 4 tasks in execution order

    TODO: Implement the four tasks below
    """

    # =========================================================
    # Task 1: Query Expansion
    # =========================================================
    expand_task = Task(
        description=(
            f"Research question:\n"
            f'"{research_question}"\n\n'
            "Your job is to design a search strategy for this question. "
            "Do NOT attempt to answer the question yourself and do NOT search "
            "the corpus — a downstream agent will do that. Produce the "
            "following as a structured plan:\n\n"
            "1. **Core concept map** — 2-3 sentences identifying the central "
            "concepts in the question and how they relate.\n"
            "2. **Sub-questions** — 3-5 focused sub-questions that, if "
            "answered together, would fully address the main question. Each "
            "sub-question should be independently searchable.\n"
            "3. **Keyword clusters** — for each sub-question, list 4-8 "
            "keywords/phrases including technical terms, common synonyms, "
            "and adjacent terminology used across sub-fields.\n"
            "4. **Alternative angles** — 2-3 alternative framings of the "
            "question a search system might otherwise miss (e.g., from a "
            "safety angle, a systems angle, an evaluation angle)."
        ),
        agent=query_expander,
        expected_output=(
            "A structured markdown search strategy containing (a) a concept "
            "map, (b) 3-5 sub-questions, (c) keyword clusters for each "
            "sub-question, and (d) 2-3 alternative angles. Formatted for a "
            "human collaborator to read at a glance."
        ),
    )
 
    # =========================================================
    # Task 2: Source Hunting
    # =========================================================
    search_task = Task(
        description=(
            "Using the search strategy produced by the Query Strategist, "
            "search the paper corpus with the `Search Research Papers` tool "
            "and collect 8-12 highly relevant AND DIVERSE passages.\n\n"
            "The corpus contains 15 papers spanning both broad surveys and "
            "specific technique papers. Known paper concepts in the corpus "
            "(use these as query hints — they exist as separate papers):\n"
            "  - ReAct: reasoning + acting interleaved traces\n"
            "  - Chain-of-Thought (CoT) prompting\n"
            "  - Tree of Thoughts (ToT) deliberative search\n"
            "  - Reflexion: verbal reinforcement learning\n"
            "  - Toolformer: self-taught tool use\n"
            "  - Retrieval-Augmented Generation (RAG) — original and survey\n"
            "  - Constitutional AI: harmlessness from AI feedback\n"
            "  - AutoGen: multi-agent conversation framework\n"
            "  - CAMEL: role-playing communicative agents\n"
            "  - Generative Agents: interactive simulacra of human behavior\n"
            "  - Planning abilities of LLMs\n"
            "  - Broad surveys: Wooldridge (foundational), Wang, Xi\n\n"
            "HARD REQUIREMENTS (grading depends on this):\n"
            "1. Issue AT LEAST 6 separate searches — one per sub-question is "
            "the minimum. Do NOT stop after 2-3 queries.\n"
            "2. AT LEAST 3 of your queries must be TECHNIQUE-SPECIFIC — i.e. "
            "they name a concrete method from the list above (e.g. "
            "'ReAct interleaved reasoning trace', 'chain of thought "
            "prompting exemplars', 'tree of thoughts deliberate search'). "
            "Generic queries like 'AI agent reasoning' will over-rank "
            "surveys and MUST be complemented by narrower queries.\n"
            "3. DIVERSITY RULE: no single paper_id may account for more than "
            "25% of your final passages. If after 3-4 searches you notice "
            "one paper dominating, IMMEDIATELY reformulate to pull passages "
            "from other papers.\n"
            "4. COVERAGE CHECK: after your initial searches, look at which "
            "paper_ids you have collected. If any of the technique papers "
            "listed above are absent, issue targeted queries naming those "
            "techniques directly before finalising the dossier.\n"
            "5. Preserve full metadata for every passage kept: paper_id, "
            "paper_title, section, and relevance score.\n"
            "6. Discard passages with relevance below 0.35 UNLESS coverage "
            "for a sub-question is otherwise missing.\n\n"
            "You MUST NOT fabricate passages or citations. Only include "
            "passages you actually retrieved via the tool. If a technique "
            "genuinely has no relevant passages after a targeted query, "
            "note that in the dossier rather than inventing content."
        ),
        agent=source_hunter,
        context=[expand_task],
        expected_output=(
            "A markdown-formatted evidence dossier with:\n"
            "  (a) A brief header summarising which queries were issued\n"
            "      and which paper_ids were retrieved (coverage summary).\n"
            "  (b) 8-12 numbered passages, each with: paper_id, paper_title, "
            "      section, relevance score, the passage excerpt, and one "
            "      sentence explaining which sub-question or angle it "
            "      addresses.\n"
            "  (c) Passages grouped under the sub-question they primarily "
            "      support.\n"
            "No single paper_id should dominate the dossier."
        ),
    )
 
    # =========================================================
    # Task 3: Synthesis
    # =========================================================
    synthesis_task = Task(
        description=(
            "Analyze the evidence dossier and produce a structured synthesis "
            "of the literature retrieved. Do NOT re-search — reason over what "
            "the Source Investigator collected.\n\n"
            "Your synthesis must include:\n"
            "1. **Themes** — 3-5 major themes that emerge across the "
            "passages. For each theme give a 1-2 sentence description and "
            "list the paper_ids that support it.\n"
            "2. **Points of consensus** — claims multiple papers agree on.\n"
            "3. **Contradictions and debates** — cases where papers "
            "disagree, use the same term differently, or reach conflicting "
            "conclusions. If none exist in the retrieved passages, say so "
            "explicitly rather than inventing one.\n"
            "4. **Gaps** — questions raised by the research question that "
            "the retrieved corpus does not answer, or answers only partially.\n"
            "5. **Evidence map** — for each theme, name which specific "
            "passage indices from the dossier support it.\n\n"
            "Ground every claim in a specific passage. Never introduce facts "
            "that are not in the dossier."
        ),
        agent=synthesizer,
        context=[expand_task, search_task],
        expected_output=(
            "A structured markdown synthesis with sections for Themes, "
            "Consensus, Contradictions, Gaps, and Evidence Map. Each theme "
            "and claim is annotated with the paper_ids and passage indices "
            "that support it."
        ),
    )
 
    # =========================================================
    # Task 4: Report Writing
    # =========================================================
    report_task = Task(
        description=(
            "Write the final literature review in markdown, drawing on the "
            "search strategy, the evidence dossier, and the synthesis. The "
            "review must follow this EXACT 7-section structure:\n\n"
            "1. **Executive Summary** — 3-5 sentences answering the "
            "research question at a high level, grounded in the retrieved "
            "literature.\n"
            "2. **Introduction** — frame the research question, define key "
            "terms as used in the retrieved papers, and preview the review.\n"
            "3. **Methodology** — briefly describe the search strategy "
            "(sub-questions, angles) and note that findings are drawn from "
            "a curated corpus of 15 papers on AI agents.\n"
            "4. **Findings** — organized by the themes from the synthesis. "
            "Use `##` for the Findings header and `###` for each theme. "
            "Discuss what the literature says on each theme, weaving in "
            "inline citations of the form `[paper_id]`.\n"
            "5. **Discussion** — surface consensus, disagreements, and gaps "
            "identified in the synthesis. Where the retrieved corpus is "
            "silent on part of the question, say so explicitly.\n"
            "6. **Conclusion** — 2-4 sentences summarising what was learned "
            "and what remains open.\n"
            "7. **References** — a complete list of every paper_id cited "
            "anywhere in the review, one per line, formatted as "
            "`- [paper_id] — paper_title`.\n\n"
            f"The research question being answered is:\n"
            f'"{research_question}"\n\n'
            "Citation rules (STRICT):\n"
            "- Every non-trivial claim must have an inline citation.\n"
            "- Cite by paper_id in square brackets, e.g. [react_2023].\n"
            "- Do NOT cite any paper_id that is not in the evidence dossier.\n"
            "- Do NOT introduce facts from your own training knowledge.\n"
            "- If the retrieved passages don't support a point, omit it or "
            "flag it as a gap rather than filling it from memory."
        ),
        agent=report_writer,
        context=[expand_task, search_task, synthesis_task],
        expected_output=(
            "A complete literature review in markdown with the 7 required "
            "sections in order, inline `[paper_id]` citations on every "
            "substantive claim, and a References section listing every "
            "paper_id cited. Ready to be saved as a .md file with no "
            "further editing."
        ),
    )
 
    return [expand_task, search_task, synthesis_task, report_task]
 
