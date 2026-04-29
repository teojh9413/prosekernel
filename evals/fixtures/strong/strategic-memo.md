# Strong strategic memo fixture

Decision: build evals before the LLM adapter.

Reason: without evals, a drafting adapter only proves that the model can produce fluent text. It does not prove that Humanprint improved the text. The moat is corpus plus patterns plus tests, not another wrapper around an API.

Evidence from the current repo: 60 examples and 12 pattern families already give us retrieval inputs. The missing piece is a benchmark loop that shows weak drafts scoring low, strong drafts scoring high, and rewrites improving across specificity, proof, structure, reader fit, memorability, and non-genericness.

Tradeoff: this delays provider integration by one phase. That is acceptable because the adapter will be easier to trust once `humanprint eval` can catch smart-sounding emptiness.
