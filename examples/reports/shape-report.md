# ProseKernel Shape Report

## Overall diagnosis

AI structure risk: High
Shape score: 25/100 — default AI document shape

The draft is clear in places, but its architecture looks assembled from a default AI template. The issue is the document shape before sentence polish, not only the headings.

## Shape scorecard
- Reader fit: 10/15 — Checks whether the structure feels written to a real reader and situation.
- Intent fit: 6/15 — Checks whether the document shape fits what the piece is trying to cause.
- Structure originality: 5/15 — Penalizes inherited article/proposal ladders and generic containers.
- Judgment and prioritization: 2/15 — Rewards selective emphasis and penalizes fake completeness or equal-weight thinking.
- Rhythm naturalness: 0/10 — Checks one-sentence paragraph rhythm, em dashes, and repeated formulas.
- Heading quality: 0/10 — Checks whether headings are situated moves rather than topic labels.
- Ending strength: 2/10 — Checks whether the ending creates a next step, decision, risk, question, or judgment.
- AI template risk: 0/10 — Reversed score: higher means lower template risk.

## Detected issues
1. Detected a generic proposal ladder: Executive Summary, Market Opportunity, Proposed Solutions, Implementation Roadmap, Challenges, Future Outlook, Conclusion. The issue is the default AI document shape, not only the heading names. Severity: high. Evidence: Executive Summary, Market Opportunity, Proposed Solutions, Implementation Roadmap, Challenges, Future Outlook, Conclusion.
2. The sections have unusually even weight. Human writing usually varies emphasis based on judgment. Severity: warning. Evidence: 41, 15, 28, 29, 19, 19, 13, 14.
3. Too many one sentence paragraphs. This creates the default AI dramatic rhythm. Severity: severe. Evidence: 17/18 paragraphs (94%).
4. Frequent em dashes can make the prose feel AI polished rather than naturally written. Severity: warning. Evidence: 4.
5. Repeated not-X/but-Y contrast formulas become obvious AI writing when reused. Severity: warning. Evidence: 3.
6. Generic signposting makes the piece sound assembled instead of situated. Severity: high. Evidence: in today's rapidly evolving landscape, there are several key, in conclusion, ultimately, moreover, additionally, this represents a significant opportunity.
7. The draft may be trying to close the entire argument on paper. For this intent, leave more for the conversation. Severity: warning. Evidence: 8 major headings.
8. The ending mostly summarizes or gestures at a generic future. Strong endings create a decision, next step, consequence, question, or sharper judgment. Severity: warning. Evidence: the future of payments is bright.  in conclusion, by embracing ai, companies can drive meaningful transformation and create scalable value..
9. Several headings are containers rather than situated claims. Do not simply rewrite them as thesis sentences; ask whether each section belongs in that position. Severity: warning. Evidence: Executive Summary, Market Opportunity, Proposed Solutions, Implementation Roadmap, Challenges, Future Outlook, Conclusion.

## Automatic metrics
- word count: 192
- heading count: 8
- generic heading count: 7
- paragraph count: 18
- one-sentence paragraph share: 94%
- em dash count: 4
- repeated contrast formula count: 3
- generic signpost count: 7

## Recommended structure

Use Curiosity Proposal.

1. A quick observation
2. The opportunity behind it
3. Why this may matter for your company
4. Three possible directions
5. The one most worth discussing
6. What I would like to explore with you

Secondary option: Direct Advisory Note.

## Rewrite instructions for the agent

- Restructure the piece as a Curiosity Proposal.
- Do not simply rename headings. Change the order, emphasis, and what is left unsaid.
- Open with the specific observation, not market background or an executive summary.
- Collapse broad opportunity and transformation sections into one commercial tension.
- Do not close with a summary. Close with what the first conversation should decide.
- Use one-sentence paragraphs only for real emphasis, not as the default rhythm.
- Reduce decorative em dashes; prefer cleaner sentences, colons, commas, or full stops.
- Use contrast formulas at most once; replace repeated not-X/but-Y turns with concrete judgment.
- Keep the tone direct, senior, and specific. Frame the work as better editorial judgment and structure, not deception or AI-undetectability.

No model call was made. This is a deterministic editorial architecture diagnostic, not a hard quality gate.
