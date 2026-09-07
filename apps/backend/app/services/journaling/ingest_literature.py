"""Literature knowledge base ingestion script for pgvector.
Extracts and chunks foundational works from Minsky, Kahneman, Taleb, Shiller, Le Bon, and Soros.
"""

import uuid
from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

SAMPLE_LITERATURE_CORPUS = [
    {
        "author": "Hyman Minsky",
        "title": "Stabilizing an Unstable Economy (1986)",
        "discipline": "Macroeconomics",
        "affinity": "Alpha",
        "chunks": [
            "Over periods of prolonged prosperity, the economy transits from financial relations that make for a stable system to financial relations that make for an unstable system. In particular, economic units go from hedge financing units to speculative financing units and ultimately to Ponzi financing units.",
            "Stability is destabilizing. The fundamental instability of capitalist finance arises from the transformation of cash-flow expectations and debt commitments during sustained growth phases."
        ],
    },
    {
        "author": "Daniel Kahneman",
        "title": "Thinking, Fast and Slow (2011)",
        "discipline": "Behavioral Psychology",
        "affinity": "Beta",
        "chunks": [
            "Loss aversion is a powerful cognitive asymmetry: losses loom larger than corresponding gains. The response to losses is consistently more intense than the response to gains in retail trading populations.",
            "The confidence that individuals have in their beliefs depends mostly on the quality of the story they can tell about what they see, even if they see very little. Retail market herds substitute coherence for evidence."
        ],
    },
    {
        "author": "Nassim Nicholas Taleb",
        "title": "Antifragile: Things That Gain from Disorder (2012)",
        "discipline": "Complexity & Risk",
        "affinity": "Gamma",
        "chunks": [
            "Antifragility is beyond resilience or robustness. The resilient resists shocks and stays the same; the antifragile gets better. To survive in markets, one must eliminate exposure to ruin before seeking optimization.",
            "Crucially, if a strategy has asymmetric downside exposure or is fragile to a tail event, no degree of past statistical success justifies taking the position. Fragility must be unilaterally vetoed."
        ],
    },
    {
        "author": "Robert J. Shiller",
        "title": "Narrative Economics (2019)",
        "discipline": "Narrative Economics",
        "affinity": "Beta",
        "chunks": [
            "Stories drive economic events. Viral narratives spread like epidemics through retail investor networks, sparking price movements that cannot be justified by conventional discounting models.",
            "A contagious narrative around sudden wealth or corporate catalysts acts as a social contagion, dramatically shortening investor time horizons."
        ],
    },
    {
        "author": "Gustave Le Bon",
        "title": "The Crowd: A Study of the Popular Mind (1895)",
        "discipline": "Crowd Psychology",
        "affinity": "Beta",
        "chunks": [
            "In a crowd, every emotion and act is contagious, and contagious to such a degree that an individual readily sacrifices his personal interest to the collective interest. In financial panics or bubbles, critical thinking dissolves."
        ],
    },
    {
        "author": "George Soros",
        "title": "The Alchemy of Finance (1987)",
        "discipline": "Epistemology",
        "affinity": "Gamma",
        "chunks": [
            "Reflexivity posits that market participants' biases distort pricing, and distorted prices subsequently alter market fundamentals. Markets are not passive discount mechanisms; they actively shape outcomes in circular feedback loops."
        ],
    },
    {
        "author": "Karl Popper",
        "title": "The Logic of Scientific Discovery (1934)",
        "discipline": "Epistemology",
        "affinity": "Gamma",
        "chunks": [
            "A theory that is not refutable by any conceivable event is non-scientific. In trading, an investment thesis must declare in advance what future events will falsify it, or it constitutes dogma rather than risk management."
        ],
    },
]


class LiteratureIngestor:
    """Manages ingestion of core texts into the literature_knowledge table."""

    async def seed_knowledge_base(self, session: AsyncSession):
        """Seeds chunked literature passages into PostgreSQL."""
        for book in SAMPLE_LITERATURE_CORPUS:
            for idx, chunk in enumerate(book["chunks"]):
                # Synthetic 1536-dimensional embedding vector or zero-initialized vector
                zero_vector = "[" + ",".join(["0.001"] * 1536) + "]"
                stmt = text("""
                    INSERT INTO literature_knowledge (
                        id, author, work_title, route_affinity, chunk_index, chunk_text, embedding
                    ) VALUES (
                        :id, :author, :title, :affinity, :chunk_idx, :text, :embedding::vector
                    )
                """)
                await session.execute(
                    stmt,
                    {
                        "id": str(uuid.uuid4()),
                        "author": book["author"],
                        "title": book["title"],
                        "affinity": book["affinity"],
                        "chunk_idx": idx,
                        "text": chunk,
                        "embedding": zero_vector,
                    },
                )
        await session.commit()


literature_ingestor = LiteratureIngestor()
